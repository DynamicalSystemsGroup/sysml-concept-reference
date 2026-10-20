"""Shared, dependency-free page frame and reference components."""
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/DynamicalSystemsGroup/sysml-concept-reference'
NAV_GROUPS=[
    ('Explore', [('Home','index.html'),('Concept browser','docs/concept-browser.html'),('Parts and ports','docs/parts-and-ports.html'),('SVG shape library','docs/svg-shapes.html'),('Notation coverage','docs/notation-coverage.html')]),
    ('Concept profiles',[('Part usage','docs/concepts/part-usage.html'),('Part definition','docs/concepts/part-definition.html'),('Port usage','docs/concepts/port-usage.html'),('Connection usage','docs/concepts/connection-usage.html')]),
    ('Research and data',[('Notation source register','docs/notation-register.html'),('RDF inventory','docs/rdf-inventory.html'),('Official sources','docs/official-machine-readable-specs.html'),('Language research','docs/language-research.html'),('Data downloads','data/index.html'),('SPARQL queries','queries/index.html')]),
    ('Project',[('Concept-page contract','docs/concept-page-contract.html'),('Roadmap','docs/roadmap.html'),('Publishing','docs/publishing.html')])]
NAV=[item for _,items in NAV_GROUPS for item in items]


def relative(destination,current):
    return Path(os.path.relpath(destination,Path(current).parent)).as_posix()


def link(label,path,current,**attrs):
    extra=''.join(f' {escape(key)}="{escape(str(value),quote=True)}"' for key,value in attrs.items())
    active=' aria-current="page"' if path==current else ''
    source=ROOT/path
    if path=='index.html':source=ROOT/'site/index.md'
    elif path=='docs/repository.html':source=ROOT/'README.md'
    elif path.endswith('.html') and not source.exists():source=source.with_suffix('.md')
    offline=f' data-offline-href="{escape(relative(source.relative_to(ROOT).as_posix(),current))}"' if source.is_file() else ''
    return f'<a href="{escape(relative(path,current))}"{active}{offline}{extra}>{escape(label)}</a>'


def navigation(current):
    parts=[]
    for title,items in NAV_GROUPS:
        links=''.join(link(label,path,current) for label,path in items)
        if title=='Explore':parts.append(f'<div class="nav-group"><p>{title}</p>{links}</div>')
        else:
            opened=' open' if any(path==current for _,path in items) else ''
            parts.append(f'<details class="nav-group"{opened}><summary>{title}</summary>{links}</details>')
    return '<nav aria-label="Research guides">'+''.join(parts)+'</nav>'


def header(current):
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-nav"><a class="dsg-logo" href="https://www.dynamicalsystemsgroup.com/" aria-label="Dynamical Systems Group website"><img src="{relative('assets/brand/dsg-wordmark.png',current)}" alt="Dynamical Systems Group" width="154" height="40"></a>{link('SysML Concept Reference','index.html',current,**{'class':'brand'})}
<nav aria-label="Primary">{link('Explore concepts','docs/concept-browser.html',current)}{link('Research','docs/rdf-inventory.html',current)}<a href="{REPO}">GitHub</a></nav></header>'''


def footer(current):
    return f'''<footer class="site-footer"><div><strong>A Dynamical Systems Group project</strong><p>Source-backed research with explicit interpretation and coverage limits.</p></div><nav aria-label="DSG links"><a href="https://www.dynamicalsystemsgroup.com/">DSG website</a><a href="https://github.com/DynamicalSystemsGroup">DSG on GitHub</a><a href="{REPO}">Source repository</a>{link('Apache 2.0 license','LICENSE',current)}</nav></footer>'''


class Headings(HTMLParser):
    def __init__(self):super().__init__();self.items=[];self.active=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h2' and attrs.get('id'):self.active=[attrs['id'],'']
    def handle_data(self,data):
        if self.active is not None:self.active[1]+=data
    def handle_endtag(self,tag):
        if tag=='h2' and self.active is not None:self.items.append(tuple(self.active));self.active=None


def scope_panel(facts,note=None):
    cells=''.join(f'<div><dt>{escape(label)}</dt><dd>{escape(str(value))}</dd></div>' for label,value in facts)
    return '<aside class="scope-panel" aria-label="Scope and review status"><dl>'+cells+'</dl>'+(f'<p>{escape(note)}</p>' if note else '')+'</aside>'


def page_kind(current):
    if current=='index.html':return 'home'
    if current=='docs/concept-browser.html':return 'browser'
    if current=='docs/svg-shapes.html':return 'gallery'
    if current.startswith('docs/concepts/'):return 'concept'
    if current=='docs/notation-register.html':return 'register'
    if current=='docs/notation-coverage.html':return 'coverage'
    return 'document'


def page_facts(current):
    report=json.loads((ROOT/'data/rdf/extraction-report.json').read_text())
    if current=='index.html':
        return [('Focus concepts',report['focus_metaclasses']),('Draft profiles',len(json.loads((ROOT/'data/concept-profiles.json').read_text())['profiles'])),('Reusable SVGs',len(json.loads((ROOT/'data/svg-shapes.json').read_text())['shapes']))], 'Representative source checks cover a selected slice. Full language coverage and model conformance remain outside this catalogue.'
    if current=='docs/notation-coverage.html':
        c=json.loads((ROOT/'data/notation-coverage.json').read_text())['counts']
        return [('Indexed source cells',c['labeled_table_cells']),('Grammar occurrences',c['production_occurrences']),('Mapped source cells',c['mapped_table_cells']),('Source cells audited',c['fully_audited_table_cells'])], 'Source-unit audits record local alternatives and rendering deferrals. Indexing, representative mapping and rendered support are separate counts.'
    if current=='docs/rdf-inventory.html':
        return [('Focus concepts',report['focus_metaclasses']),('Declared properties',report['declared_properties']),('Validation scope','Catalogue integrity')], 'SHACL checks catalogue records; it does not validate a user’s SysML model.'
    if current.startswith('docs/concepts/'):
        return [('Review state','Draft, source-checked'),('Examples','Source-reviewed'),('Engine execution','Not performed')], None
    return [],None


def evidence_panel(urls):
    manifest=json.loads((ROOT/'data/source-manifest.json').read_text())
    sources=manifest['artifacts']+manifest['supporting_artifacts']
    entries=[]
    for url,label in dict(urls).items():
        source=next((s for s in sources if s['url']==url.split('#')[0]),None)
        if not source:continue
        name=source['language']+' '+source['version']+(' Language' if source.get('id')=='SysMLLanguage' else '')
        identity=source.get('omg_file_id','')
        entries.append(f'<li><span class="evidence-document">{escape(name)}</span><a href="{escape(url,quote=True)}">{escape(label or "Original source")}</a><small>{escape(identity)}</small></li>')
    if not entries:return ''
    return f'<details class="evidence-panel"><summary>Source evidence <span>{len(entries)} location'+('s' if len(entries)!=1 else '')+'</span></summary><ul>'+''.join(entries)+'</ul></details>'


def prepare_body(body,current):
    """Reframe existing HTML, preserving heading IDs and authored content."""
    kind=page_kind(current)
    match=re.search(r'<h1\b[^>]*>.*?</h1>',body,re.S)
    title_html=match[0] if match else ''
    if kind=='home' and 'id="understand-the-concepts-behind-sysml-v2"' not in title_html:
        # Keep the previous homepage title fragment working as its copy evolves.
        title_html='<span id="understand-the-concepts-behind-sysml-v2" aria-hidden="true"></span>'+title_html
    rest=body[:match.start()]+body[match.end():] if match else body
    intro=re.match(r'\s*(<p\b[^>]*>.*?</p>)',rest,re.S)
    lead=intro[1] if intro else ''
    if intro:rest=rest[intro.end():]
    if kind=='concept':
        # The profile generator puts its status before its purpose. Both remain visible.
        purpose=re.match(r'\s*(<p\b[^>]*>.*?</p>)',rest,re.S)
        if purpose:
            status=lead;lead=purpose[1];rest='<div class="profile-status">'+status+'</div>'+rest[purpose.end():]
    lead=lead.replace('<p>','<p class="page-lead">',1)
    label={'home':'Language reference','concept':'Concept profile','coverage':'Notation research','register':'Source register','document':'Research and methods'}.get(kind,'Reference tools')
    facts,note=page_facts(current)
    heading=f'<header class="page-heading"><p class="page-category">{label}</p>{title_html}{lead}</header>'
    if facts and kind!='home':heading+=scope_panel(facts,note)
    if kind=='home':
        heading+=f'''<nav class="entry-routes" aria-label="Choose your path">
<a class="entry-path" href="{relative('docs/concept-browser.html',current)}"><span class="entry-label">Concept reference</span><strong>Understand SysML concepts</strong><p>Understand what concepts mean, how they relate and compose, and how they appear in diagrams. Follow examples and links to the official specification.</p><span class="entry-action">Explore concepts</span></a>
<a class="entry-path" href="{relative('docs/svg-shapes.html',current)}"><span class="entry-label">For building tools</span><strong>Borrow graphical components</strong><p>Download reusable SVG parts, ports and connections for your renderer. Inspect shapes, edit labels and colors, and use attachment coordinates.</p><span class="entry-action">Open the SVG library</span></a>
<a class="entry-evidence" href="{relative('docs/notation-coverage.html',current)}"><strong>Inspect the evidence and coverage</strong><span>Trace notation to official sources and see what has been indexed, illustrated or reviewed.</span></a>
</nav>'''
        if facts:heading+=scope_panel(facts,note)
    chunks=re.split(r'(?=<h2\b)',rest)
    if kind=='concept':
        order=['What to understand','Graphical notation','Relationships and composition','Connected example','Properties','Reconciliation and limits']
        def section_order(chunk):
            match=re.match(r'<h2[^>]*>(.*?)</h2>',chunk,re.S)
            return order.index(match[1]) if match and match[1] in order else -1
        chunks.sort(key=section_order)
    sections=[]
    for chunk in chunks:
        if not chunk.strip():continue
        h=re.match(r'(<h2\b[^>]*>.*?</h2>)(.*)',chunk,re.S)
        if kind=='register' and h:
            index=json.loads((ROOT/'data/notation-source-index.json').read_text())
            name=re.sub('<[^>]+>','',h[1])
            family=next((section['title'] for section in index['sections'] if section['id']==name),None)
            heading_html=h[1].replace('</h2>',' '+escape(family.replace(' Graphical Notation',''))+'</h2>') if family else h[1]
            content=h[2]
            cells=sum(item['section']==name for item in index['table_cells'])
            productions=sum(item['section']==name for item in index['productions'])
            content=f'<details class="source-family"><summary>Browse source entries <span>{cells} source cells · {productions} grammar occurrences</span></summary>'+content+'</details>'
            chunk=heading_html+content
        if kind=='concept':
            def collapse_table(m):
                rows=len(re.findall('<tr>',m[0]))-1
                return '<details class="reference-disclosure"><summary>View '+str(rows)+' property declarations</summary>'+m[0]+'</details>' if rows>40 else m[0]
            chunk=re.sub(r'<div class="table-scroll"[^>]*>.*?</table></div>',collapse_table,chunk,flags=re.S)
        # Exact original links stay inline; a compact panel supplies artifact context.
        links=[]
        for m in re.finditer(r'<a href="(https://www\.omg\.org/[^\"]+)"[^>]*>(.*?)</a>',chunk,re.S):
            links.append((m[1].replace('&amp;','&'),re.sub('<[^>]+>','',m[2])))
        if links and kind not in ('register',):chunk+=evidence_panel(links)
        sections.append('<section class="content-section">'+chunk+'</section>')
    return heading+''.join(sections)


def layout(body,title,current,source=None,*,inline=False,prepared=False,sections=None,kind=None):
    kind=kind or page_kind(current)
    if not prepared:body=prepare_body(body,current)
    parser=Headings();parser.feed(body)
    sections=sections if sections is not None else parser.items
    toc=''
    if len(sections)>1:
        toc='<nav class="section-nav" aria-label="On this page"><p>On this page</p>'+''.join(f'<a href="#{"detail" if kind=="browser" else escape(id,quote=True)}"'+(f' data-section-target="{escape(id,quote=True)}"' if kind=='browser' else '')+f'>{escape(label)}</a>' for id,label in sections)+'</nav>'
    mobile_toc=('<details class="mobile-section-nav"><summary>On this page</summary>'+toc.replace('class="section-nav"','class="section-nav section-nav-mobile"')+'</details>') if toc else ''
    nav=navigation(current)
    compact=kind=='browser'
    rail='' if compact else f'<aside class="sidebar"><div class="desktop-nav">{nav}</div></aside>'
    mobile=f'<details class="mobile-nav"><summary>Browse reference</summary>{nav}</details>'
    if compact:mobile=mobile.replace('class="mobile-nav"','class="mobile-nav workspace-nav"')
    edit=f'<p class="edit"><a href="{REPO}/blob/main/{escape(source,quote=True)}">View this page’s source on GitHub</a></p>' if source else ''
    if inline:
        brand=(ROOT/'site/brand.css').read_text().replace('url("fonts/','url("assets/brand/fonts/')
        styles='<style>'+brand+'\n'+(ROOT/'site/style.css').read_text()+'</style>'
        script='<script data-site-runtime>'+(ROOT/'site/site.js').read_text()+'</script>'
    else:
        styles=f'<link rel="stylesheet" href="{relative("assets/brand/brand.css",current)}"><link rel="stylesheet" href="{relative("assets/style.css",current)}">'
        script=f'<script defer src="{relative("assets/site.js",current)}"></script>'
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | SysML Concept Reference</title><meta name="description" content="Source-backed KerML and SysML v2 concepts, properties, relationships and research.">{styles}<link rel="icon" href="{relative('assets/brand/dsg-logo.png',current)}" type="image/png"></head>
<body class="page-{kind}">{header(current)}{mobile}<div class="shell{' shell-workspace' if compact else ''}">{rail}<main id="main" tabindex="-1">{mobile_toc}<article>{body}{edit}</article></main>{toc}</div>{footer(current)}{script}</body></html>'''
    if inline:
        html=html.replace(relative('assets/brand/dsg-logo.png',current),'assets/brand/dsg-logo.png').replace(relative('assets/brand/dsg-wordmark.png',current),'assets/brand/dsg-wordmark.png')
    return html
