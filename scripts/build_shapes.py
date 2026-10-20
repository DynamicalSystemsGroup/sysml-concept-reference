"""Generate portable SVG components, a sprite, manifest, bundle and gallery."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from html import escape
import json
import re
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

from rdflib import Graph, Literal, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS

from build_inventory import ROOT, ID, INV, write_turtle
from build_site import layout

NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
SVG=ROOT/'shapes/svg'
SOURCE_URL='https://www.omg.org/spec/SysML/2.0/Language/PDF'


def element(parent,tag,attrs=None,text=None):
    child=ET.SubElement(parent,'{'+NS+'}'+tag,attrs or {})
    if text is not None:child.text=text
    return child


def geometry(shape):
    """Geometry is an original redraw; source grammar controls semantic restrictions."""
    template=shape['template']
    node_height=220 if template.endswith('-compartments') else 140
    viewbox=[0,0,240,node_height] if shape['kind']=='node' else ([0,0,24,24] if template in ('port-glyph','port-direction') else [0,0,280,160 if template=='nary' else 72])
    root=ET.Element('{'+NS+'}svg',{'viewBox':' '.join(map(str,viewbox)), 'width':str(viewbox[2]), 'height':str(viewbox[3]),
                    'preserveAspectRatio':'xMidYMid meet','role':'img','aria-label':shape['name']})
    element(root,'title',text=shape['name']);element(root,'desc',text=shape['description']+' '+shape['limits'])
    shape_style='fill:var(--sysml-fill,#fff);stroke:var(--sysml-stroke,#11113a);stroke-width:var(--sysml-stroke-width,2)'
    group=element(root,'g',{'data-layer':'geometry','fill':'#fff','stroke':'#11113a','stroke-width':'2','style':shape_style})
    stroke={'vector-effect':'non-scaling-stroke'}
    slots={}
    if shape['kind']=='node':
        attributes={'x':'8','y':'8','width':'224','height':str(node_height-16),**stroke}
        if not template.startswith('definition'):attributes['rx']='14'
        if template=='reference':attributes['stroke-dasharray']='8 5'
        element(group,'rect',attributes)
        anchors={'north':[120,8],'east':[232,node_height/2],'south':[120,node_height-8],'west':[8,node_height/2]}
        if template.endswith('-compartments'):element(group,'path',{'d':'M8 82H232','fill':'none',**stroke})
    elif template in ('port-glyph','port-direction'):
        element(group,'rect',{'x':'2','y':'2','width':'20','height':'20','rx':'3',**stroke})
        anchors={'center':[12,12],'north':[12,2],'east':[22,12],'south':[12,22],'west':[2,12]}
        if template=='port-direction':
            paths={'right':'M6 12H18M13 8L18 12L13 16','left':'M18 12H6M11 8L6 12L11 16',
                   'horizontal-both':'M6 12H18M11 8L6 12L11 16M13 8L18 12L13 16',
                   'up':'M12 18V6M8 11L12 6L16 11','down':'M12 6V18M8 13L12 18L16 13',
                   'vertical-both':'M12 6V18M8 11L12 6L16 11M8 13L12 18L16 13'}
            element(group,'path',{'d':paths[shape['direction_indicator']],'fill':'none',**stroke})
    elif template in ('binary','binding'):
        element(group,'path',{'d':'M12 36H268','fill':'none',**stroke})
        anchors={'start':[12,36],'end':[268,36]}
    elif template=='nary':
        element(group,'path',{'d':'M12 80H140L268 24M140 80L268 136','fill':'none',**stroke})
        element(group,'circle',{'cx':'140','cy':'80','r':'6','fill':'#11113a','stroke':'none','style':'fill:var(--sysml-stroke,#11113a);stroke:none'})
        anchors={'junction':[140,80],'end1':[12,80],'end2':[268,24],'end3':[268,136]}
    else:raise ValueError('Unknown template '+template)
    labels=element(root,'g',{'data-layer':'labels','fill':'#11113a','font-family':'system-ui,sans-serif','font-size':'16','text-anchor':'middle','style':'fill:var(--sysml-text,#11113a);font-family:var(--sysml-font,system-ui,sans-serif);font-size:16px;text-anchor:middle'})
    if shape['kind']=='node':
        compartment=template.endswith('-compartments')
        element(labels,'text',{'x':'120','y':'35' if compartment else '58'},shape['keyword'])
        element(labels,'text',{'x':'120','y':'62' if compartment else '94','data-slot':'label'},shape['label'])
        if compartment:
            element(labels,'text',{'x':'120','y':'105','font-style':'italic','font-size':'14'},shape['compartment'])
            for number,row in enumerate(shape['rows'],1):
                slot='row'+str(number);slots[slot]=row
                element(labels,'text',{'x':'22','y':str(110+number*27),'text-anchor':'start','font-size':'14','data-slot':slot},row)
            element(labels,'text',{'x':'22','y':'196','text-anchor':'start'},'…')
        slots['label']=shape['label']
    elif 'label' in shape:
        coords={'x':'125','y':'65','text-anchor':'end'} if template=='nary' else {'x':'140','y':'24'}
        element(labels,'text',{**coords,'data-slot':'label'},shape['label']);slots['label']=shape['label']
    elif template=='binding':element(labels,'text',{'x':'140','y':'24'},'=')
    if len(labels)==0:root.remove(labels)
    return root,viewbox,anchors,slots


def write_svg(root,path):
    ET.indent(root,space='  ')
    path.write_text(ET.tostring(root,encoding='unicode')+'\n')


def validate_definitions(config,index):
    ids=set();productions={p['id'] for p in index['productions']}
    for shape in config['shapes']:
        if not re.fullmatch(r'[a-z][a-z0-9-]*',shape['id']) or shape['id'] in ids:
            raise ValueError('Invalid or duplicate SVG ID')
        ids.add(shape['id'])
        if not shape['production_ids'] or not set(shape['production_ids'])<=productions:
            raise ValueError('SVG shape lacks indexed production evidence')
        if not shape['limits'] or not shape['evidence_pages']:raise ValueError('SVG shape lacks scope/evidence')
        if shape['template'].endswith('-compartments'):
            if shape['kind']!='node' or len(shape.get('rows',[]))!=2 or not all(isinstance(r,str) for r in shape['rows']) or shape.get('compartment') not in ('parts','ports'):
                raise ValueError('Compartment template requires a node and exactly two literal rows')
        if shape['template']=='port-direction' and (shape['kind']!='glyph' or shape.get('direction_indicator') not in ('left','right','up','down','horizontal-both','vertical-both')):
            raise ValueError('Unknown boundary direction indicator')
    return config


def main():
    config=json.loads((ROOT/'data/svg-shapes.json').read_text())
    index=json.loads((ROOT/'data/notation-source-index.json').read_text())
    validate_definitions(config,index)
    SVG.mkdir(parents=True,exist_ok=True)
    sprite=ET.Element('{'+NS+'}svg')
    catalog={'schema_version':1,'version':config['version'],'license':config['license'],
             'copyright':config['copyright'],'scope':config['scope'], 'source':index['source'],
             'theme_variables':{'--sysml-stroke':'#11113a','--sysml-fill':'#fff','--sysml-text':'#11113a','--sysml-stroke-width':'2','--sysml-font':'system-ui,sans-serif'},
             'shapes':[]}
    roots={};graph=Graph();graph.bind('inv',INV);graph.bind('id',ID);graph.bind('dct',DCTERMS)
    for shape in config['shapes']:
        root,viewbox,anchors,slots=geometry(shape)
        evidence=[SOURCE_URL+f'#page={page}' for page in shape['evidence_pages']]
        metadata={'license':config['license'],'license_url':'https://www.apache.org/licenses/LICENSE-2.0','copyright':config['copyright'],'source':evidence,
                  'source_sha256':index['source']['sha256'],'production_ids':shape['production_ids'],
                  'provenance':'Original reusable redraw; not an official OMG figure or a conformance result.'}
        meta=ET.Element('{'+NS+'}metadata');meta.text=json.dumps(metadata,ensure_ascii=False)
        root.insert(2,meta)
        path=SVG/(shape['id']+'.svg');write_svg(root,path);roots[shape['id']]=deepcopy(root)
        symbol=element(sprite,'symbol',{'id':'sysml-'+shape['id'],'viewBox':' '.join(map(str,viewbox))})
        for child in root:symbol.append(deepcopy(child))
        catalog['shapes'].append({**{k:v for k,v in shape.items() if k not in ('template','label','keyword','evidence_pages')},
                                  'file':'svg/'+path.name,'symbolId':'sysml-'+shape['id'],
                                  'viewBox':viewbox,'anchors':anchors,'labelSlots':slots,
                                  'source_urls':evidence,'verification':'RepresentativeSourceChecked',
                                  'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        n=ID['svg-shape/'+shape['id']]
        graph.add((n,RDF.type,INV.SVGShapeAsset));graph.add((n,RDFS.label,Literal(shape['name'])))
        graph.add((n,DCTERMS.description,Literal(shape['description'])));graph.add((n,INV.caveat,Literal(shape['limits'])))
        graph.add((n,DCTERMS.license,URIRef('https://www.apache.org/licenses/LICENSE-2.0')))
        graph.add((n,INV.asset,Literal('shapes/svg/'+path.name)));graph.add((n,INV.sha256,Literal(catalog['shapes'][-1]['sha256'])))
        graph.add((n,INV.sourceArtifact,ID['source/sha256/'+index['source']['sha256']]))
        for source in evidence:graph.add((n,DCTERMS.source,URIRef(source)))
        for production in shape['production_ids']:graph.add((n,INV.realizesProduction,ID['graphical-production/'+production]))
        if shape.get('notation_record'):graph.add((n,INV.relatedNotation,ID['notation/'+shape['notation_record']]))
    write_svg(sprite,ROOT/'shapes/shapes.svg')
    (ROOT/'shapes/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
    write_turtle(graph,ROOT/'data/rdf/svg-shapes.ttl')
    shutil.copyfile(ROOT/'LICENSE',ROOT/'shapes/LICENSE')
    # An independent composition example: no external images, scripts, or SVG IDs.
    example=ET.Element('{'+NS+'}svg',{'viewBox':'0 0 760 240','role':'img','aria-label':'Two part usages joined by a binary connection'})
    element(example,'title',text='Compose part usages with a binary connection')
    for name,x,y,label in [('connection-binary',240,84,'link'),('part-usage',20,50,'axle : Axle'),('part-usage',500,50,'wheel : Wheel')]:
        node=deepcopy(roots[name]);node.set('x',str(x));node.set('y',str(y))
        next(t for t in node.iter() if t.get('data-slot')=='label').text=label
        example.append(node)
    write_svg(example,ROOT/'shapes/examples/composition.svg')
    build_parts_ports_example(roots)
    build_gallery(catalog)
    # Explicit distributable allowlist; no downloaded sources or DSG brand assets.
    files=[ROOT/'shapes/LICENSE',ROOT/'shapes/README.md',ROOT/'shapes/catalog.json',ROOT/'shapes/shapes.svg',
           ROOT/'shapes/renderer.mjs',*[ROOT/'shapes'/s['file'] for s in catalog['shapes']],
           ROOT/'shapes/examples/composition.svg',ROOT/'shapes/examples/parts-ports.svg',ROOT/'shapes/examples/renderer.html']
    with ZipFile(ROOT/'shapes/catalog.zip','w',compression=ZIP_DEFLATED) as bundle:
        for path in files:
            info=ZipInfo(path.relative_to(ROOT/'shapes').as_posix(),date_time=(2026,1,1,0,0,0))
            info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
            bundle.writestr(info,path.read_bytes())
    print(f"Built {len(catalog['shapes'])} reusable SVGs, sprite, renderer bundle, RDF and gallery")


def build_parts_ports_example(roots):
    """Original component composition; direction choices are explicit drawing inputs."""
    root=ET.Element('{'+NS+'}svg',{'viewBox':'0 0 800 580','role':'img','aria-label':'Parts and ports component composition'})
    element(root,'title',text='Parts, boundary-port directions and textual compartments')
    element(root,'desc',text='Original rendering example, not an official figure or validated model. Arrows and labels are caller-supplied; no direction is inferred. All four boundary placements are shown. Two selected compartments are shown below.')
    def place(id,x,y,label=None):
        node=deepcopy(roots[id]);node.set('x',str(x));node.set('y',str(y))
        if label is not None:next(n for n in node.iter() if n.get('data-slot')=='label').text=label
        root.append(node)
    place('part-usage',260,110,'host : Component')
    for id,x,y in [('right',256,168),('left',480,168),('down',368,106),('up',368,230)]:place('port-arrow-'+id,x,y)
    for text,x,y,anchor in [('pLeft : Interface',245,157,'end'),('pRight : Interface',515,157,'start'),('pTop : Interface',365,91,'end'),('pBottom : Interface',397,275,'start')]:
        element(root,'text',{'x':str(x),'y':str(y),'font-family':'system-ui,sans-serif','font-size':'16','text-anchor':anchor,'fill':'#11113a'},text)
    place('part-definition-parts',100,325)
    place('port-definition-ports',440,325)
    write_svg(root,ROOT/'shapes/examples/parts-ports.svg')


def build_gallery(catalog):
    cards=[]
    for shape in catalog['shapes']:
        id=escape(shape['id']);file='../shapes/'+shape['file']
        sources=' · '.join(f'<a href="{url}">PDF {url.split("=")[-1]}</a>' for url in shape['source_urls'])
        anchors=', '.join(shape['anchors'])
        cards.append(f'''<section class="shape-card" data-kind="{shape['kind']}" data-family="{escape(shape['family'])}" data-search="{escape((shape['name']+' '+shape['id']+' '+shape['kind']+' '+shape['description']).lower())}" id="{id}">
<div class="shape-preview"><img src="{file}" alt="{escape(shape['name'])}" loading="lazy"></div>
<div class="shape-detail"><p class="shape-kind">{escape(shape['family'])} / {escape(shape['kind'])}</p><h2>{escape(shape['name'])}</h2><code>{id}</code>
<details><summary>Scope and source</summary><p>{escape(shape['description'])}</p><p class="shape-limit">{escape(shape['limits'])}</p><p>ViewBox: <code>{' '.join(map(str,shape['viewBox']))}</code></p><p>Anchors: {escape(anchors)}</p><p>{sources}</p><a href="../shapes/catalog.json">Full manifest</a></details>
<div class="shape-actions"><button type="button" hidden data-inspect="{id}" aria-label="Inspect {escape(shape['name'])}" aria-pressed="false">Inspect</button><a href="{file}" download>Download SVG</a><button type="button" hidden data-copy="{file}" aria-label="Copy SVG for {escape(shape['name'])}">Copy SVG</button></div></div></section>''')
    body=f'''<header class="page-heading"><p class="page-category">Renderer components</p><h1>Reusable SVG shapes</h1><p class="page-lead">Build graphical assets from small, source-backed components. Download a standalone SVG, use the symbol sprite, or set labels and colors with the browser renderer.</p></header>
<div class="scope-panel"><dl><div><dt>Reusable components</dt><dd>{len(catalog['shapes'])}</dd></div><div><dt>Original asset license</dt><dd>Apache 2.0</dd></div><div><dt>Rendering scope</dt><dd>Representative</dd></div></dl><p>Original redraws for selected parts, ports and connections. Each component records its limits; a glyph does not cover the full notation grammar.</p></div>
<nav class="shape-actions shape-intro" aria-label="Library downloads"><a class="shape-primary" href="../shapes/catalog.zip" download>Download library ZIP</a><a href="svg-shapes-guide.html">Usage guide</a><a href="../shapes/examples/renderer.html">Live renderer example</a><a href="../shapes/shapes.svg" download>SVG sprite</a></nav>
<section class="shape-inspector" id="shape-inspector" hidden aria-label="Selected shape"><header><h2 id="inspector-title" tabindex="-1"></h2><code id="inspector-id"></code></header><div class="inspector-grid"><div><div class="inspector-preview" id="inspector-preview"></div><div class="preview-controls"><label for="preview-label">Preview label<input id="preview-label" type="text" maxlength="80" disabled></label><div id="preview-extra-labels"></div><label class="checkbox-label"><input id="preview-dark" type="checkbox" disabled> Inspect on a dark surface</label></div><p id="preview-status" role="status"></p><div class="shape-actions"><a id="inspector-download" href="../shapes/catalog.zip" download>Download original SVG</a><button id="copy-preview" type="button" disabled>Copy preview SVG</button></div></div><div class="inspector-info"><p class="shape-kind" id="inspector-kind"></p><p id="inspector-description"></p><p class="notice" id="inspector-limits"></p><details class="evidence-panel"><summary>Source evidence</summary><ul id="inspector-sources"></ul></details><details><summary>Attachment coordinates and file identity</summary><p>ViewBox: <code id="inspector-viewbox"></code></p><ul class="anchor-list" id="inspector-anchors"></ul><p>Original file SHA-256: <code id="inspector-hash"></code></p><a href="../shapes/catalog.json">Full manifest</a></details></div></div></section>
<h2 id="shape-browse" class="shape-browse-title">Browse the library</h2><div class="shape-filters" hidden><label>Find a shape<input id="shape-search" type="search" placeholder="Name, ID or appearance"></label><label>Family<select id="shape-family"><option value="">All families</option><option>Parts</option><option>Ports</option><option>Connections</option></select></label></div>
<p id="shape-count" role="status">{len(catalog['shapes'])} shapes shown</p><p id="copy-status" role="status" aria-live="polite"></p><div class="shape-grid">{''.join(cards)}</div><p id="shape-empty" hidden>No shapes match. Try a broader search or another family.</p>
<section class="content-section"><h2 id="shape-usage">Use these as components</h2><p>The assets contain geometry and editable text, without a research-page background, branding or source caption. Evidence and licensing stay in SVG metadata and the manifest. The host renderer places labels, routes edges and enforces SysML rules. See the <a href="notation-coverage.html">notation coverage dashboard</a> for the wider inventory.</p></section>
<script type="application/json" id="shape-catalog">{json.dumps(catalog,ensure_ascii=True).replace('<',chr(92)+'u003c')}</script>'''
    html=layout(body,'Reusable SVG shapes','docs/svg-shapes.html','data/svg-shapes.json',inline=True,prepared=True,sections=[('shape-browse','Browse the library'),('shape-usage','Use components')])
    extra=(ROOT/'scripts/shapes-gallery.css').read_text();js=(ROOT/'scripts/shapes-gallery.js').read_text()
    html=html.replace('</head>',f'<style>{extra}</style></head>').replace('</body>',f'<script>{js}</script></body>')
    (ROOT/'docs/svg-shapes.html').write_text(html)


if __name__=='__main__':main()
