"""Index pinned SysML notation sources and build an evidence-linked coverage register.

Normal builds use committed metadata. --extract requires Poppler and the pinned PDF;
it indexes names/locations, never treats text extraction as recovered graphical BNF.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS, XSD

from build_inventory import ROOT, ID, INV, write_turtle
from parts_ports_audit import load_audit, audit_counts, add_audit_rdf, render_audit, unit_kind

INDEX = ROOT / 'data/notation-source-index.json'
REVIEWS = ROOT / 'data/notation-reviews.json'
PDF_URL = 'https://www.omg.org/spec/SysML/2.0/Language/PDF'
TABLE_SECTIONS = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,17,18,19,20,21,23,24,25,26,26,27]
XHTML = {'x': 'http://www.w3.org/1999/xhtml'}
SVG = {'s': 'http://www.w3.org/2000/svg'}
PRODUCTION = re.compile(r'^([a-z][a-z0-9-]*)\s*(=\|?|\|=)(.*)')
SECTION = re.compile(r'^8\.2\.3\.(\d+) (.+)')


def pdf_source():
    manifest = json.loads((ROOT / 'data/source-manifest.json').read_text())
    return next(a for a in manifest['supporting_artifacts'] if a['id'] == 'SysMLLanguage')


def text_pages(pdf, raw=False):
    result = subprocess.run(['pdftotext', '-raw' if raw else '-layout', str(pdf), '-'],
                            check=True, capture_output=True, text=True)
    return result.stdout.split('\f')


def grammar_index(pages):
    sections, productions = [], []
    active = False
    ordinal = Counter()
    section = None
    for page_number, text in enumerate(pages, 1):
        for line_number, line in enumerate(text.splitlines(), 1):
            if line == '8.2.3 Graphical Notation': active = True
            if line == '8.3 Abstract Syntax': active = False
            if not active: continue
            if m := SECTION.match(line):
                section = '8.2.3.' + m[1]
                sections.append({'id': section, 'title': m[2], 'pdf_page': page_number,
                                 'printed_page': page_number - 32})
            if m := PRODUCTION.match(line):
                ordinal[(section, m[1])] += 1
                productions.append({'id': f"{section}/{m[1]}/{ordinal[(section,m[1])]}",
                                    'name': m[1], 'section': section, 'operator': m[2],
                                    'spaced_bar_after_equals': m[2] == '=' and m[3].lstrip().startswith('|'),
                                    'pdf_page': page_number, 'printed_page': page_number - 32,
                                    'text_line': line_number, 'index_status': 'TextIndexed'})
    if [s['id'] for s in sections] != [f'8.2.3.{i}' for i in range(1,28)]:
        raise ValueError('Missing or repeated graphical grammar section')
    return sections, productions


def grid_cells(svg):
    """Find first-column source cells from Poppler's explicit table-grid paths.

    Does not infer symbols, join equal labels, or extract the graphical column.
    """
    segments, vertical = [], []
    for path in ET.parse(svg).getroot().findall('.//s:path', SVG):
        if path.get('fill') != 'rgb(66.268921%, 66.268921%, 66.268921%)': continue
        points = [(float(x),float(y)) for x,y in re.findall(r'[ML] ([-.\d]+) ([-.\d]+)', path.get('d',''))]
        if not points: continue
        xs,ys = zip(*points)
        if max(xs)-min(xs)<=2 and max(ys)-min(ys)>10:
            vertical.append((min(xs), min(ys), max(ys)))
        for a,b in zip(points, points[1:]):
            if abs(a[1]-b[1])<.1 and abs(a[0]-b[0])>50 and min(a[0],b[0])<73:
                segments.append((min(a[0],b[0]), max(a[0],b[0]), a[1]))
    if not segments or not vertical: return []
    left = min(a for a,b,y in segments)
    rights = [x for x,y1,y2 in vertical if x>left+5]
    if not rights: return []
    right = min(rights)
    ys = sorted(set(round(y,1) for a,b,y in segments if a<=left+1 and b>=right-1))
    bounds = []
    for y in ys:
        if not bounds or y-bounds[-1]>2: bounds.append(y)
    return [[left,y1,right,y2] for y1,y2 in zip(bounds,bounds[1:])]


def table_index(pdf, pages, work):
    bbox = work / 'tables.xml'
    subprocess.run(['pdftotext','-f','45','-l','193','-bbox-layout',str(pdf),str(bbox)],check=True)
    bbox_pages = ET.parse(bbox).getroot().findall('.//x:page', XHTML)
    tables, rows = {}, []
    current = None
    for page_number, page in enumerate(bbox_pages,45):
        lines = []
        for line in page.findall('.//x:line',XHTML):
            words = line.findall('x:word', XHTML)
            text = ' '.join(w.text or '' for w in words)
            if m := re.match(r'Table (\d+)\. (.+)',text):
                n = int(m[1])
                if n<=26:
                    current = n
                    tables[n] = {'id':f'table-{n}', 'number':n, 'title':m[2], 'pdf_page':page_number,
                                 'section':f'8.2.3.{TABLE_SECTIONS[n-1]}',
                                 'role':'SemanticDependency' if n==16 else ('DiagramExample' if n==25 else 'RepresentativeNotation')}
            lines.append((line, text))
        if current is None: continue
        svg = work / f'page-{page_number}.svg'
        subprocess.run(['pdftocairo','-f',str(page_number),'-l',str(page_number),'-svg',str(pdf),str(svg)],
                       check=True,capture_output=True)
        for left,top,right,bottom in grid_cells(svg):
            labels = [text for line,text in lines if left<=float(line.get('xMin')) and float(line.get('xMax'))<right-1
                      and top<=float(line.get('yMin'))<bottom]
            label = ' '.join(labels)
            if not label or label in ('Element','Keyword','Standard View'): continue
            rows.append({'id':f'table-{current}/cell-{1+sum(r["table"]==current for r in rows)}',
                         'table':current, 'section':tables[current]['section'], 'label':label,
                         'pdf_page':page_number, 'printed_page':page_number-32,
                         'label_cell_bbox':[round(v,2) for v in (left,top,right,bottom)],
                         'index_status':'GridLabelIndexed'})
    if sorted(tables)!=list(range(1,27)):
        raise ValueError('Expected all 26 Clause 7 table captions')
    # Cross-check captions independently against layout text, not grid assignment.
    captions = {int(m[1]):pn for pn,p in enumerate(pages,1) for line in p.splitlines()
                if (m:=re.match(r'^\s*Table (\d+)\. ',line)) and 1<=int(m[1])<=26}
    if {n:t['pdf_page'] for n,t in tables.items()} != captions:
        raise ValueError('Table caption locations disagree across extraction modes')
    return list(tables.values()),rows


def extract(pdf):
    source = pdf_source()
    data = pdf.read_bytes()
    if len(data)!=source['bytes'] or hashlib.sha256(data).hexdigest()!=source['sha256']:
        raise ValueError('Pinned SysML PDF mismatch; do not silently repin')
    work = ROOT / 'sandbox/notation-index'
    work.mkdir(parents=True,exist_ok=True)
    pages = text_pages(pdf)
    sections,productions = grammar_index(pages)
    _,raw_productions = grammar_index(text_pages(pdf,raw=True))
    key = lambda p:(p['section'],p['name'],p['operator'],p['pdf_page'])
    if Counter(map(key,productions)) != Counter(map(key,raw_productions)):
        raise ValueError('Production labels disagree between layout and raw extraction')
    tables,rows = table_index(pdf,pages,work)
    result = {'schema_version':1, 'source':source, 'method':{
        'production_index':'Poppler layout and raw label/page agreement, restricted to §8.2.3; no RHS reconstruction',
        'table_index':'Caption agreement plus explicit PDF grid geometry and first-column labels; no deduplication or inferred continuation joins',
        'coordinates':'PDF points from top left; bbox is label cell, not full notation image',
        'tool':subprocess.run(['pdftotext','-v'],capture_output=True,text=True).stderr.splitlines()[0],
        'scope':'§8.2.3 production occurrences and labeled cells in Clause 7 Tables 1–26; not a unique-symbol or graphical-alternative census'},
        'sections':sections, 'tables':tables, 'table_cells':rows, 'productions':productions}
    INDEX.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    return result


def validate_index(index):
    source = pdf_source()
    if index['source'] != source: raise ValueError('Notation index source identity is stale')
    for key in ('sections','tables','table_cells','productions'):
        ids=[r['id'] for r in index[key]]
        if len(ids)!=len(set(ids)): raise ValueError('Duplicate notation source ID')
    sections={s['id'] for s in index['sections']}
    if sections!={f'8.2.3.{i}' for i in range(1,28)}:raise ValueError('Incomplete section inventory')
    tables={t['number']:t for t in index['tables']}
    if set(tables)!=set(range(1,27)):raise ValueError('Incomplete table inventory')
    for p in index['productions']:
        if p['section'] not in sections or p['operator'] not in ('=','=|','|=') or not 225<=p['pdf_page']<=287:
            raise ValueError('Invalid production location')
    for r in index['table_cells']:
        if r['table'] not in tables or r['section']!=tables[r['table']]['section'] or not r['label']:
            raise ValueError('Invalid source table cell')
        b=r['label_cell_bbox']
        if len(b)!=4 or not 0<=b[0]<b[2]<=612 or not 0<=b[1]<b[3]<=792:
            raise ValueError('Invalid source cell coordinates')
        if r['pdf_page']<tables[r['table']]['pdf_page'] or r['printed_page']!=r['pdf_page']-32:
            raise ValueError('Invalid source cell page')
    return index


def validate_reviews(index,reviews,profiles):
    ids = {p['id'] for p in index['productions']}
    cells = {r['id'] for r in index['table_cells']}
    existing = {n['id']:n for p in profiles['profiles'] for n in p['notations']}
    seen=set()
    for r in reviews['notations']:
        if r['id'] in seen or r['id'] not in existing: raise ValueError('Unknown or repeated notation record')
        seen.add(r['id'])
        if not r['production_ids'] or not set(r['production_ids'])<=ids:raise ValueError('Missing production mapping')
        if not set(r['table_cell_ids'])<=cells:raise ValueError('Unknown source table cell')
        for key in ('geometry','line_style','labels','compartments','attachments','applicability','alternatives','represents'):
            if not r.get(key): raise ValueError('Incomplete appearance/applicability record: '+key)
        # Coverage is about the stated illustration scope, never every alternative in a production.
        if r.get('coverage_claim')!='RepresentativeOnly': raise ValueError('Unproven exhaustive notation coverage')
        if r.get('illustrated_forms') and not existing[r['id']].get('asset'):raise ValueError('Illustration claim lacks asset')
    if seen!=set(existing):raise ValueError('Existing profile notation is unmapped')
    for r in reviews['shared_rules']:
        if not r.get('description') or not r.get('evidence_pages'):raise ValueError('Shared rule lacks evidence')
        if not set(r.get('production_ids',[]))<=ids:raise ValueError('Unknown shared rule production')
    return existing


def coverage(index,reviews,existing):
    cells={r['id']:r for r in index['table_cells']}
    audit=load_audit(index);audited={u['id'] for u in audit['units']};ac=audit_counts(audit)
    mapped_productions={p for n in reviews['notations'] for p in n['production_ids']}
    mapped_cells={r for n in reviews['notations'] for r in n['table_cell_ids']}
    return {'scope':index['method']['scope'], 'counts':{
        'grammar_sections':len(index['sections']), 'clause7_tables':len(index['tables']),
        'labeled_table_cells':len(cells), 'representative_notation_cells':sum(tables_role(index,r)=='RepresentativeNotation' for r in cells.values()),
        'production_occurrences':len(index['productions']), 'distinct_production_names':len({p['name'] for p in index['productions']}),
        'explicit_partial_occurrences':sum(p['operator']=='=|' for p in index['productions']),
        'reversed_operator_occurrences_needing_review':sum(p['operator']=='|=' for p in index['productions']),
        'spaced_bar_occurrences_needing_review':sum(p['spaced_bar_after_equals'] for p in index['productions']),
        'curated_notation_records':len(existing), 'source_checked_representative_records':len(reviews['notations']),
        'illustrated_records':sum(bool(n.get('asset')) for n in existing.values()),
        'illustration_files':len({n['asset'] for n in existing.values() if n.get('asset')}),
        'mapped_production_occurrences':len(mapped_productions), 'mapped_table_cells':len(mapped_cells),
        'unmapped_production_occurrences':len(index['productions'])-len(mapped_productions),
        'unmapped_table_cells':len(cells)-len(mapped_cells),
        'fully_audited_production_occurrences':ac['audited_production_occurrences'], 'fully_audited_table_cells':ac['audited_source_cells'],
        'audited_alternative_records':ac['alternative_records'], 'deferred_alternative_records':ac['deferred_records'], 'partially_rendered_alternative_records':ac['partially_rendered_records'],
        'shared_rules_described':len(reviews['shared_rules'])},
        'families':[{'section':s['id'], 'title':s['title'],
                     'production_occurrences':sum(p['section']==s['id'] for p in index['productions']),
                     'table_cells':sum(r['section']==s['id'] for r in cells.values()),
                     'mapped_production_occurrences':sum(p['section']==s['id'] and p['id'] in mapped_productions for p in index['productions']),
                     'mapped_table_cells':sum(r['section']==s['id'] and r['id'] in mapped_cells for r in cells.values()),
                     'audited_production_occurrences':sum(p['section']==s['id'] and p['id'] in audited for p in index['productions']),
                     'audited_table_cells':sum(r['section']==s['id'] and r['id'] in audited for r in cells.values())}
                    for s in index['sections']],
        'limits':['Indexing is not a visual rule audit; mapped does not mean fully covered.',
                  'Text extraction cannot enumerate two-dimensional alternatives, adornments or all imported dependencies.',
                  'Repeated names and same-label cells retain distinct source occurrences.',
                  'Table 16 is a semantic dependency, Table 25 diagram examples; neither is added to representative-notation cell count.',
                  'No unique-symbol or remaining-illustration total is asserted.']}


def tables_role(index,row):
    return next(t['role'] for t in index['tables'] if t['number']==row['table'])


def build_rdf(index,reviews,existing):
    g=Graph();g.bind('inv',INV);g.bind('id',ID);g.bind('dct',DCTERMS)
    artifact=ID['source/sha256/'+index['source']['sha256']]
    def location(node,page):
        g.add((node,DCTERMS.source,URIRef(PDF_URL+f'#page={page}')))
        g.add((node,INV.sourceArtifact,artifact));g.add((node,INV.pdfPage,Literal(page,datatype=XSD.integer)))
    for s in index['sections']:
        n=ID['notation-section/'+s['id']];g.add((n,RDF.type,INV.NotationSection));g.add((n,RDFS.label,Literal(s['title'])))
        location(n,s['pdf_page'])
    for t in index['tables']:
        n=ID['notation-source/'+t['id']];g.add((n,RDF.type,INV.NotationSourceTable));g.add((n,RDFS.label,Literal(t['title'])))
        g.add((n,INV.sourceRole,INV[t['role']]));g.add((n,INV.tableNumber,Literal(t['number'])))
        location(n,t['pdf_page'])
    for p in index['productions']:
        n=ID['graphical-production/'+p['id']];g.add((n,RDF.type,INV.GraphicalProductionOccurrence));g.add((n,RDFS.label,Literal(p['name'])))
        g.add((n,INV.inNotationSection,ID['notation-section/'+p['section']]))
        g.add((n,INV.productionOperator,Literal(p['operator'])))
        g.add((n,INV.indexStatus,INV.TextIndexed));g.add((n,INV.spacedBarAfterEquals,Literal(p['spaced_bar_after_equals'])))
        location(n,p['pdf_page'])
    for r in index['table_cells']:
        n=ID['notation-source/'+r['id']];g.add((n,RDF.type,INV.NotationSourceCell));g.add((n,RDFS.label,Literal(r['label'])))
        g.add((n,INV.inNotationSection,ID['notation-section/'+r['section']]))
        g.add((n,INV.inSourceTable,ID[f"notation-source/table-{r['table']}"]))
        g.add((n,INV.indexStatus,INV.GridLabelIndexed));g.add((n,INV.labelCellBounds,Literal(json.dumps(r['label_cell_bbox']))))
        location(n,r['pdf_page'])
    fields={'geometry':'geometry','line_style':'lineStyle','labels':'labelRule','compartments':'compartmentRule',
            'attachments':'attachmentRule','applicability':'condition','alternatives':'alternativeRule','represents':'representedKinds'}
    for r in reviews['notations']:
        n=ID['notation/'+r['id']]
        for key,pred in fields.items():g.add((n,INV[pred],Literal(r[key])))
        g.add((n,INV.coverageClaim,INV.RepresentativeOnly))
        g.add((n,INV.illustratedForms,Literal(r.get('illustrated_forms','No local redraw'))))
        for p in r['production_ids']:g.add((n,INV.supportingProduction,ID['graphical-production/'+p]))
        for c in r['table_cell_ids']:g.add((n,INV.supportingSourceCell,ID['notation-source/'+c]))
    for r in reviews['shared_rules']:
        n=ID['notation-rule/'+r['id']];g.add((n,RDF.type,INV.SharedNotationRule));g.add((n,RDFS.label,Literal(r['title'])))
        g.add((n,DCTERMS.description,Literal(r['description'])));g.add((n,INV.evidenceStatus,INV.EditorialSummary))
        for page in r['evidence_pages']:g.add((n,DCTERMS.source,URIRef(PDF_URL+f'#page={page}')))
        g.add((n,INV.sourceArtifact,artifact))
        for p in r.get('production_ids',[]):g.add((n,INV.supportingProduction,ID['graphical-production/'+p]))
    add_audit_rdf(g,index,load_audit(index))
    write_turtle(g,ROOT/'data/rdf/notation-register.ttl')


def render(index,reviews,existing,report):
    def link(page,label=None):return f"[{label or ('PDF '+str(page))}]({PDF_URL}#page={page})"
    c=report['counts']
    lines=['# Graphical notation coverage','',
           'A source index and review ledger for OMG SysML 2.0 Part 1, **formal/2026-03-02**. Indexed material is a work queue, not a claim that every visual alternative has been described or drawn.','',
           f"**{c['labeled_table_cells']} labeled source cells** across **26 Clause 7 tables**; **{c['production_occurrences']} graphical grammar production occurrences** under **{c['distinct_production_names']} names**, across **27 subsections**.",'',
           f"Current curated coverage: **{c['curated_notation_records']} grouped notation records**, **{c['illustration_files']} SVG files**, **{c['mapped_production_occurrences']} mapped production occurrences**, **{c['mapped_table_cells']} mapped source cells**. Mappings provide representative support; none establishes exhaustive coverage of a source cell or production.",'',
           'Notation records are counted independently of evidence links. A record may group several forms; a mapping does not exhaust all alternatives in its source.','',
           f"Unmapped work queue: **{c['unmapped_table_cells']} labeled source cells** and **{c['unmapped_production_occurrences']} production occurrences**. These are two overlapping source inventories, not numbers to add into a missing-symbol total.",'',
           '## Counting and review stages','',
           '| Unit | Count | Meaning |','|---|---:|---|',
           f"| Representative notation cells | {c['representative_notation_cells']} | Labeled cells in the 24 representative notation tables; alternatives inside a cell remain to be split |",
           '| Control-node dependency cells | 4 | Table 16 supplies semantic keyword mappings, not graphical figures |',
           '| Diagram-example cells | 6 | Table 25, including two distinct matrix examples |',
           f"| Production occurrences | {c['production_occurrences']} | Every declaration occurrence, including helpers and distributed partial rules |",
           f"| Explicit partial markers | {c['explicit_partial_occurrences']} | Literal `=¦`; five spaced-bar forms and 19 reversed `¦=` forms are flagged for review |",'',
           '**Indexed → described → illustrated → source-checked** applies to a declared variant scope. Source-cell and production mappings are counted separately; a small redraw does not complete all alternatives, compartments or nesting rules in its source. The bounded [parts-and-ports audit](parts-ports-notation-audit.md) records all local alternatives and explicit rendering/dependency deferrals for 12 source cells and 38 production occurrences. Audited does not mean fully rendered, dependency-complete or model-valid. A description can be source-checked without a local illustration.','',
           'The source-cell count retains distinct labeled cells and repeated labels. It excludes column headers and makes no inferred continuation joins. It is not a count of unique symbols, logical variants, or remaining drawings. See the [counting method](research/notation-coverage-method.md) and [machine-readable extraction index](../data/notation-source-index.json).','',
           '## Coverage by family','',
           '| Family | Grammar occurrences | Labeled source cells | Mapped grammar | Mapped cells | Audited grammar | Audited cells |','|---|---:|---:|---:|---:|---:|---:|']
    for f in report['families']:
        lines.append(f"| [{f['section']} {f['title'].replace(' Graphical Notation','')}](notation-register.md#{f['section'].replace('.','')}) | {f['production_occurrences']} | {f['table_cells']} | {f['mapped_production_occurrences']} | {f['mapped_table_cells']} | {f['audited_production_occurrences']} | {f['audited_table_cells']} |")
    lines+=['','## Reviewed representative records','']
    for r in reviews['notations']:
        n=existing[r['id']]
        lines+=['### '+n['title'],'',n['description'],'',
                f"Illustrated forms: {r.get('illustrated_forms','Source description only; no local redraw.')}",'']
        if n.get('asset'):lines += [f"![{n['title']}](assets/notation/{n['asset']})",'']
        lines += ['| Property | Recorded rule |','|---|---|']
        for k in ('geometry','line_style','labels','compartments','attachments','applicability','alternatives','represents'):
            lines.append('| '+k.replace('_',' ').capitalize()+' | '+r[k].replace('|','\\|')+' |')
        lines+=['','Source production mappings: '+', '.join('`'+p+'`' for p in r['production_ids'])+'.','']
    lines+=['## Shared conventions','']
    for r in reviews['shared_rules']:
        lines += ['### '+r['title'],'',r['description'],'', 'Evidence: '+', '.join(link(p) for p in r['evidence_pages'])+'.','']
    lines+=['## Next batches and acceptance','',
            '1. Review shared name/prefix/compartment rules and split source cells into explicit visual alternatives. Retain any uncertain production spelling as a source issue.',
            '2. Complete structure: definitions/usages, items/parts, ports, connections, interfaces, allocations and flows. Audit all boundary positions, optional arrows, proxy/reference restrictions and compartment forms.',
            '3. Review behavior: occurrences and sequence notation, actions/control structures, states/transitions and calculations.',
            '4. Review constraints, requirements, cases, views/viewpoints and metadata. Follow Table 34 standard-view filters and imported textual/KerML rules as separate dependencies.',
            '5. For each batch, record geometry, strokes, labels, represented kinds, compartments, attachments, applicability and alternatives; link exact source occurrences; add original SVG examples; visually compare with the pinned source; validate RDF and publish the revised counts.',
            '', 'A batch is complete only after every source unit is audited, each alternative is represented or explicitly deferred, and the declared illustration scope has evidence. No engine conformance claim follows from this ledger.','',
            '## Reproduce and query','',
            '```bash','uv run --locked python scripts/build_notation.py',
            '# Optional local source audit; requires the pinned PDF and Poppler:',
            'uv run --locked python scripts/build_notation.py --extract',
            'uv run --locked python scripts/check_inventory.py --query queries/notation-coverage.rq','```','',
            '[Full source register](notation-register.md) · [RDF](../data/rdf/notation-register.ttl) · [Coverage JSON](../data/notation-coverage.json) · [Review records](../data/notation-reviews.json)','']
    (ROOT/'docs/notation-coverage.md').write_text('\n'.join(lines))
    register=['# Graphical notation source register','',
              'Names and locations extracted from the hash-pinned official PDF. No graphical right-hand sides are reconstructed from text. Index status is separate from visual review. Repeated labels and productions are intentionally preserved.','',
              '[Coverage dashboard and counting policy](notation-coverage.md) · [JSON source index](../data/notation-source-index.json)','']
    audit_units={u['id']:u for u in load_audit(index)['units']}
    def audit_link(id):
        return '[Audited; rendering scope separate](parts-ports-notation-audit.md)' if id in audit_units else 'Not audited'
    mapped_p=defaultdict(list);mapped_c=defaultdict(list)
    for n in reviews['notations']:
        for p in n['production_ids']:mapped_p[p].append(n['id'])
        for r in n['table_cell_ids']:mapped_c[r].append(n['id'])
    for s in index['sections']:
        register += ['## '+s['id'],'',s['title']+'. '+link(s['pdf_page'])+'.','']
        for t in index['tables']:
            if t['section']!=s['id']:continue
            register+=['### Table '+str(t['number'])+': '+t['title'],'',f"Role: {t['role']}. Caption: {link(t['pdf_page'])}.",'',
                       '| Source cell | Label | Location | Representative mapping | Source audit |','|---|---|---|---|---|']
            for r in index['table_cells']:
                if r['table']==t['number']:
                    register.append(f"| `{r['id']}` | {r['label'].replace('|','/')} | {link(r['pdf_page'])} | {', '.join(mapped_c[r['id']]) or 'Unmapped'} | {audit_link(r['id'])} |")
            register.append('')
        register+=['### Grammar occurrences','', '| Source occurrence | Operator | Location | Representative mapping | Source audit |','|---|---|---|---|---|']
        for p in index['productions']:
            if p['section']==s['id']:
                op='`=¦` (partial)' if p['operator']=='=|' else ('`¦=` (source operator review)' if p['operator']=='|=' else ('`= ¦` (spacing review)' if p['spaced_bar_after_equals'] else '`=`'))
                register.append(f"| `{p['id']}` | {op} | {link(p['pdf_page'])} | {', '.join(mapped_p[p['id']]) or 'Unmapped'} | {audit_link(p['id'])} |")
        register.append('')
    register+=['Operator display uses ¦ for the vertical bar to keep the Markdown table readable; JSON and RDF retain the exact operator.','']
    (ROOT/'docs/notation-register.md').write_text('\n'.join(register))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract',action='store_true')
    args=parser.parse_args()
    index=extract(ROOT/'sandbox/official-sources/SysML-Language.pdf') if args.extract else json.loads(INDEX.read_text())
    validate_index(index)
    reviews=json.loads(REVIEWS.read_text())
    profiles=json.loads((ROOT/'data/concept-profiles.json').read_text())
    existing=validate_reviews(index,reviews,profiles)
    report=coverage(index,reviews,existing)
    (ROOT/'data/notation-coverage.json').write_text(json.dumps(report,indent=2)+'\n')
    build_rdf(index,reviews,existing);render(index,reviews,existing,report)
    render_audit(load_audit(index))
    print(json.dumps(report['counts'],indent=2))


if __name__=='__main__':main()
