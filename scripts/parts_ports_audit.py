"""Validate and publish the bounded, visually reviewed parts-and-ports audit."""
import json
import re
from pathlib import Path
from html import escape
from rdflib import RDF, RDFS, Literal, URIRef
from rdflib.namespace import DCTERMS, XSD
from build_inventory import ROOT, ID, INV

AUDIT=ROOT/'data/parts-ports-audit.json'
SECTIONS={'8.2.3.11','8.2.3.12'}
PDF='https://www.omg.org/spec/SysML/2.0/Language/PDF'


def validate_audit(index,audit,assets):
    if audit['source']['sha256']!=index['source']['sha256'] or audit['source']['omg_file_id']!=index['source']['omg_file_id']:
        raise ValueError('Audit source identity mismatch')
    expected={u['id']:u for kind in ['productions','table_cells'] for u in index[kind] if u['section'] in SECTIONS}
    units=audit['units'];ids=[u['id'] for u in units]
    if len(ids)!=len(set(ids)) or set(ids)!=set(expected):raise ValueError('Audit must cover exactly the selected source units')
    asset_ids={s['id'] for s in assets['shapes']}
    for unit in units:
        if unit['review_status']!='LocalAlternativesAudited' or expected[unit['id']]['pdf_page'] not in unit['source_pages']:
            raise ValueError('Audit review status or source page missing')
        if unit['printed_pages']!=[p-32 for p in unit['source_pages']]:raise ValueError('Audit printed pages mismatch')
        alternatives=unit['alternatives'];names=[a['id'] for a in alternatives]
        if not names or len(names)!=len(set(names)):raise ValueError('Audit alternatives missing or duplicated')
        for alt in alternatives:
            if not re.fullmatch(r'[a-z][a-z0-9-]*',alt['id']):raise ValueError('Alternative ID must be a stable slug')
            for key in ['geometry','line_style','labels','context']:
                if not alt.get(key):raise ValueError('Alternative lacks '+key)
            if not set(alt['represented_by'])<=asset_ids:raise ValueError('Alternative cites unknown asset')
            if not alt['represented_by'] and not alt.get('deferred_reason'):raise ValueError('Alternative has neither asset nor deferral')
            if alt['represented_by'] and not alt.get('representation_scope'):raise ValueError('Alternative asset needs a scoped claim')
    return audit


def load_audit(index):
    return validate_audit(index,json.loads(AUDIT.read_text()),json.loads((ROOT/'data/svg-shapes.json').read_text()))


def unit_kind(unit):return 'cell' if unit['id'].startswith('table-') else 'production'


def disposition(alt):
    return 'PartialRendering' if alt['represented_by'] and alt.get('deferred_reason') else ('RepresentativeAsset' if alt['represented_by'] else 'DeferredRendering')


def audit_counts(audit):
    alternatives=[a for u in audit['units'] for a in u['alternatives']]
    return {'audited_source_cells':sum(unit_kind(u)=='cell' for u in audit['units']),
            'audited_production_occurrences':sum(unit_kind(u)=='production' for u in audit['units']),
            'alternative_records':len(alternatives),
            **{k:sum(disposition(a)==v for a in alternatives) for k,v in [('representative_asset_records','RepresentativeAsset'),('partially_rendered_records','PartialRendering'),('deferred_records','DeferredRendering')]},
            'units_with_source_issues':sum(bool(u['source_issues']) for u in audit['units'])}


def add_audit_rdf(g,index,audit):
    artifact=ID['source/sha256/'+index['source']['sha256']]
    batch=ID['notation-audit/parts-ports'];g.add((batch,RDF.type,INV.NotationAuditBatch));g.add((batch,RDFS.label,Literal(audit['title'])))
    g.add((batch,DCTERMS.description,Literal(audit['method'])));g.add((batch,INV.sourceArtifact,artifact))
    for unit in audit['units']:
        node=ID['notation-audit/parts-ports/'+unit['id']]
        source=ID[('notation-source/' if unit_kind(unit)=='cell' else 'graphical-production/')+unit['id']]
        g.add((batch,INV.hasUnitAudit,node));g.add((node,RDF.type,INV.SourceUnitAudit));g.add((node,RDFS.label,Literal(unit['id'])))
        g.add((node,INV.auditsUnit,source));g.add((node,INV.reviewStatus,INV.LocalAlternativesAudited));g.add((node,INV.sourceArtifact,artifact))
        for page in unit['source_pages']:
            g.add((node,DCTERMS.source,URIRef(PDF+f'#page={page}')));g.add((node,INV.pdfPage,Literal(page,datatype=XSD.integer)))
        for dep in unit['dependencies']:g.add((node,INV.dependencyNote,Literal(dep)))
        for issue in unit['source_issues']:g.add((node,INV.sourceIssue,Literal(issue)))
        for alt in unit['alternatives']:
            variant=ID['notation-alternative/'+unit['id']+'/'+alt['id']]
            g.add((node,INV.hasAlternative,variant));g.add((variant,RDF.type,INV.NotationAlternative));g.add((variant,RDFS.label,Literal(alt['id'])))
            g.add((variant,INV.renderingStatus,INV[disposition(alt)]))
            for key,pred in [('geometry','geometry'),('line_style','lineStyle'),('labels','labelRule'),('context','condition'),('representation_scope','representationScope'),('deferred_reason','deferredReason')]:
                if alt.get(key):g.add((variant,INV[pred],Literal(alt[key])))
            for asset in alt['represented_by']:g.add((variant,INV.representedByAsset,ID['svg-shape/'+asset]))
            for dep in alt.get('dependencies',[]):g.add((variant,INV.dependencyNote,Literal(dep)))


def render_audit(audit):
    c=audit_counts(audit)
    lines=['# Parts and ports notation audit','',audit['scope'],'',
           f"**{c['audited_source_cells']} source cells and {c['audited_production_occurrences']} production occurrences reviewed.** The {c['alternative_records']} alternative records are source-local bookkeeping entries, not unique symbols or required SVG counts.",'',
           '## What reviewed means','',audit['method'],'',
           'Every selected unit has a visual review, identified local forms, source pages, and an explicit rendering disposition. Imported grammar and arbitrary prefix combinations are separate dependencies; recording a deferral does not implement them. An asset match is limited to its stated representation scope. Source inconsistencies remain visible.','',
           f"Rendering dispositions: **{c['representative_asset_records']} representative asset records**, **{c['partially_rendered_records']} partially rendered records**, **{c['deferred_records']} deferred records**. {c['units_with_source_issues']} units record source issues.",'',
           '[Concept reference](parts-and-ports.md) · [Coverage dashboard](notation-coverage.md) · [Machine-readable ledger](../data/parts-ports-audit.json) · [SPARQL alternatives query](../queries/notation-alternatives.rq)','']
    def cell(value):return str(value).replace('|','\\|').replace('\n',' ')
    for section,title in [('8.2.3.11','Parts'),('8.2.3.12','Ports')]:
        lines+=['## '+title,'']
        for unit in audit['units']:
            if not (unit['id'].startswith(section+'/') or unit['id'].startswith('table-9/' if title=='Parts' else 'table-10/')):continue
            lines+=['### '+unit['id'],'','Source: '+', '.join(f'[PDF {p} / printed {p-32}]({PDF}#page={p})' for p in unit['source_pages'])+'.','']
            if unit['dependencies']:lines+=['Dependencies: '+', '.join('`'+d+'`' for d in unit['dependencies'])+'.','']
            for issue in unit['source_issues']:lines+=['Source issue: '+issue,'']
            lines+=['| Local alternative | Appearance and labels | Context | Rendering disposition |','|---|---|---|---|']
            for alt in unit['alternatives']:
                assets=', '.join(f"[{a}](../shapes/svg/{a}.svg)" for a in alt['represented_by'])
                status=assets+(' — '+alt.get('representation_scope','') if assets else '')
                if alt.get('deferred_reason'):status+=(' / ' if status else '')+'Deferred: '+alt['deferred_reason']
                appearance=alt['geometry']+'; '+alt['line_style']+'; '+alt['labels']
                lines.append('| '+' | '.join(map(cell,[alt['id'],appearance,alt['context'],status]))+' |')
            lines.append('')
    lines+=['## Source and reproducibility','',f"Pinned OMG document `{audit['source']['omg_file_id']}`, SHA-256 `{audit['source']['sha256']}`. Original [SysML Language PDF]({PDF}).",'',
            'Research notes: [Parts](research/parts-notation-audit.md), [ports](research/ports-notation-audit.md), [shared rules](research/parts-ports-shared-rules.md).','',
            'Rebuild with `uv run --locked python scripts/build_notation.py`; validate with `uv run --locked python scripts/check_inventory.py`. No SysML parser, OCL evaluator or execution engine was run.','']
    (ROOT/'docs/parts-ports-notation-audit.md').write_text('\n'.join(lines))
