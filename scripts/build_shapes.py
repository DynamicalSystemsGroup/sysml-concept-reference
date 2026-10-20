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
    viewbox=[0,0,240,140] if shape['kind']=='node' else ([0,0,24,24] if template=='port-glyph' else [0,0,280,160 if template=='nary' else 72])
    root=ET.Element('{'+NS+'}svg',{'viewBox':' '.join(map(str,viewbox)), 'width':str(viewbox[2]), 'height':str(viewbox[3]),
                    'preserveAspectRatio':'xMidYMid meet','role':'img','aria-label':shape['name']})
    element(root,'title',text=shape['name']);element(root,'desc',text=shape['description']+' '+shape['limits'])
    shape_style='fill:var(--sysml-fill,#fff);stroke:var(--sysml-stroke,#11113a);stroke-width:var(--sysml-stroke-width,2)'
    group=element(root,'g',{'data-layer':'geometry','fill':'#fff','stroke':'#11113a','stroke-width':'2','style':shape_style})
    stroke={'vector-effect':'non-scaling-stroke'}
    slots={}
    if shape['kind']=='node':
        attributes={'x':'8','y':'8','width':'224','height':'124',**stroke}
        if template!='definition':attributes['rx']='14'
        if template=='reference':attributes['stroke-dasharray']='8 5'
        element(group,'rect',attributes)
        anchors={'north':[120,8],'east':[232,70],'south':[120,132],'west':[8,70]}
    elif template=='port-glyph':
        element(group,'rect',{'x':'2','y':'2','width':'20','height':'20','rx':'3',**stroke})
        anchors={'center':[12,12],'north':[12,2],'east':[22,12],'south':[12,22],'west':[2,12]}
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
        element(labels,'text',{'x':'120','y':'58'},shape['keyword'])
        element(labels,'text',{'x':'120','y':'94','data-slot':'label'},shape['label'])
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
    build_gallery(catalog)
    # Explicit distributable allowlist; no downloaded sources or DSG brand assets.
    files=[ROOT/'shapes/LICENSE',ROOT/'shapes/README.md',ROOT/'shapes/catalog.json',ROOT/'shapes/shapes.svg',
           ROOT/'shapes/renderer.mjs',*[ROOT/'shapes'/s['file'] for s in catalog['shapes']],
           ROOT/'shapes/examples/composition.svg',ROOT/'shapes/examples/renderer.html']
    with ZipFile(ROOT/'shapes/catalog.zip','w',compression=ZIP_DEFLATED) as bundle:
        for path in files:
            info=ZipInfo(path.relative_to(ROOT/'shapes').as_posix(),date_time=(2026,1,1,0,0,0))
            info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
            bundle.writestr(info,path.read_bytes())
    print(f"Built {len(catalog['shapes'])} reusable SVGs, sprite, renderer bundle, RDF and gallery")


def build_gallery(catalog):
    cards=[]
    for shape in catalog['shapes']:
        id=escape(shape['id']);file='../shapes/'+shape['file']
        sources=' · '.join(f'<a href="{url}">PDF {url.split("=")[-1]}</a>' for url in shape['source_urls'])
        anchors=', '.join(shape['anchors'])
        cards.append(f'''<section class="shape-card" data-family="{escape(shape['family'])}" data-search="{escape((shape['name']+' '+shape['id']+' '+shape['kind']+' '+shape['description']).lower())}" id="{id}">
<div class="shape-preview"><img src="{file}" alt="{escape(shape['name'])}" loading="lazy"></div>
<div class="shape-detail"><p class="shape-kind">{escape(shape['family'])} / {escape(shape['kind'])}</p><h2>{escape(shape['name'])}</h2><code>{id}</code>
<p>{escape(shape['description'])}</p><p class="shape-limit">{escape(shape['limits'])}</p>
<details><summary>Coordinates and evidence</summary><p>ViewBox: <code>{' '.join(map(str,shape['viewBox']))}</code></p><p>Anchors: {escape(anchors)}</p><p>{sources}</p><a href="../shapes/catalog.json">Full manifest</a></details>
<div class="shape-actions"><a href="{file}" download>Download SVG</a><button type="button" data-copy="{file}" aria-label="Copy SVG for {escape(shape['name'])}">Copy SVG</button></div></div></section>''')
    body=f'''<h1>Reusable SVG shapes</h1><p>Build graphical assets from small, source-backed components. Download a standalone SVG, use the symbol sprite, or set labels and colors with the browser renderer.</p>
<div class="shape-intro"><strong>{len(catalog['shapes'])} shapes · transparent backgrounds · Apache 2.0</strong><p>Original redraws for selected parts, ports and connections. Each card records its scope; a glyph does not cover the full notation grammar.</p>
<nav class="shape-actions" aria-label="Library downloads"><a class="shape-primary" href="../shapes/catalog.zip" download>Download library ZIP</a><a href="svg-shapes.md">Usage guide</a><a href="../shapes/examples/renderer.html">Live renderer example</a><a href="../shapes/shapes.svg" download>SVG sprite</a></nav></div>
<div class="shape-filters"><label>Find a shape<input id="shape-search" type="search" placeholder="Name, ID or appearance"></label><label>Family<select id="shape-family"><option value="">All families</option><option>Parts</option><option>Ports</option><option>Connections</option></select></label></div>
<p id="shape-count" role="status">{len(catalog['shapes'])} shapes shown</p><p id="copy-status" role="status" aria-live="polite"></p><div class="shape-grid">{''.join(cards)}</div><p id="shape-empty" hidden>No shapes match. Try a broader search or another family.</p>
<h2>Use these as components</h2><p>The assets contain geometry and editable text, without a research-page background, branding or source caption. Evidence and licensing stay in SVG metadata and the manifest. The host renderer places labels, routes edges and enforces SysML rules. See the <a href="notation-coverage.md">notation coverage dashboard</a> for the wider inventory.</p>'''
    html=layout(body,'Reusable SVG shapes','docs/svg-shapes.html','data/svg-shapes.json')
    brand=(ROOT/'site/brand.css').read_text().replace('url("fonts/','url("assets/brand/fonts/')
    css=(ROOT/'site/style.css').read_text()
    html=html.replace('<link rel="stylesheet" href="../assets/brand/brand.css"><link rel="stylesheet" href="../assets/style.css">',f'<style>{brand}\n{css}</style>')
    html=html.replace('../assets/brand/dsg-logo.png','assets/brand/dsg-logo.png').replace('../assets/brand/dsg-wordmark.png','assets/brand/dsg-wordmark.png')
    html=html.replace('href="svg-shapes.md"','href="svg-shapes-guide.html"').replace('href="notation-coverage.md"','href="notation-coverage.html"')
    extra=(ROOT/'scripts/shapes-gallery.css').read_text()
    js=(ROOT/'scripts/shapes-gallery.js').read_text()
    html=html.replace('</head>',f'<style>{extra}</style></head>').replace('</body>',f'<script>{js}</script></body>')
    (ROOT/'docs/svg-shapes.html').write_text(html)


if __name__=='__main__':main()
