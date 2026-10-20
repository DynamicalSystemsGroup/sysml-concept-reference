'use strict';
const search=document.querySelector('#shape-search'), family=document.querySelector('#shape-family');
const cards=[...document.querySelectorAll('.shape-card')];
const catalog=JSON.parse(document.querySelector('#shape-catalog').textContent);
const inspector=document.querySelector('#shape-inspector'), preview=document.querySelector('#inspector-preview');
let selected, rendererPromise, currentSvg, revision=0;
document.querySelector('.shape-filters').hidden=false;
for(const button of document.querySelectorAll('[data-copy],[data-inspect]'))button.hidden=false;
function filterShapes(){
  const query=search.value.trim().toLowerCase();let count=0;
  for(const card of cards){
    card.hidden=!(card.dataset.search.includes(query)&&(!family.value||card.dataset.family===family.value));
    if(!card.hidden)count++;
  }
  document.querySelector('#shape-count').textContent=`${count} shape${count===1?'':'s'} shown`;
  document.querySelector('#shape-empty').hidden=count!==0;
}
search.addEventListener('input',filterShapes);family.addEventListener('change',filterShapes);
async function copyText(text){
  if(!navigator.clipboard?.writeText)throw new Error('Clipboard unavailable');
  await navigator.clipboard.writeText(text);
}
for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{
  const status=document.querySelector('#copy-status');
  try{
    const response=await fetch(button.dataset.copy);if(!response.ok)throw new Error('Download unavailable');
    await copyText(await response.text());status.textContent='SVG copied, including source and license metadata.';
  }catch(error){status.textContent='Copy unavailable here. Use Download SVG to save the file.';}
});
const text=(id,value)=>document.getElementById(id).textContent=value;
function anchorList(shape){
  const list=document.querySelector('#inspector-anchors');list.replaceChildren();
  for(const [name,point] of Object.entries(shape.anchors)){
    const item=document.createElement('li'),code=document.createElement('code');code.textContent=`${name}: (${point.join(', ')})`;item.append(code);list.append(item);
  }
}
async function renderPreview(){
  if(!selected)return;const token=++revision;currentSvg=null;
  const status=document.querySelector('#preview-status'),copy=document.querySelector('#copy-preview');copy.disabled=true;
  try{
    rendererPromise??=import(new URL('../shapes/renderer.mjs',location.href).href);
    const {createShape}=await rendererPromise;
    const dark=document.querySelector('#preview-dark').checked;
    const theme=dark?{stroke:'#ebe6d6',text:'#ebe6d6',fill:'#11113a'}:{};
    const labels=Object.hasOwn(selected.labelSlots,'label')?{label:document.querySelector('#preview-label').value}:{};
    for(const input of document.querySelectorAll('[data-preview-slot]'))labels[input.dataset.previewSlot]=input.value;
    const svg=await createShape(selected.id,{labels,theme,title:selected.name});if(token!==revision)return;
    svg.classList.add('inspector-svg');preview.replaceChildren(svg);preview.dataset.kind=selected.kind;preview.classList.toggle('preview-dark',dark);currentSvg=svg;
    document.querySelector('#preview-label').disabled=!Object.hasOwn(selected.labelSlots,'label');document.querySelector('#preview-dark').disabled=false;for(const input of document.querySelectorAll('[data-preview-slot]'))input.disabled=false;copy.disabled=false;
    const vb=selected.viewBox,overflow=[...svg.querySelectorAll('[data-slot]')].some(node=>{const box=node.getBBox();return box.x<vb[0]||box.x+box.width>vb[0]+vb[2]});
    status.textContent=overflow?'This label exceeds the supplied geometry. Your renderer will need a larger node or text layout.':'Editable preview. Labels and colors do not validate the modeled concept.';
  }catch(error){
    if(token!==revision)return;rendererPromise=undefined;
    status.textContent='Editable preview unavailable. The original SVG and download links remain available.';
  }
}
function selectShape(id,{scroll=false,writeHash=false}={}){
  const shape=catalog.shapes.find(shape=>shape.id===id);if(!shape)return;selected=shape;inspector.hidden=false;
  text('inspector-title',shape.name);text('inspector-id',shape.id);text('inspector-kind',shape.family+' / '+shape.kind);text('inspector-description',shape.description);text('inspector-limits',shape.limits);text('inspector-viewbox',shape.viewBox.join(' '));
  const download=document.querySelector('#inspector-download');download.href='../shapes/'+shape.file;download.download=shape.id+'.svg';
  const input=document.querySelector('#preview-label');input.value=shape.labelSlots.label??'';input.disabled=true;document.querySelector('#preview-dark').disabled=true;
  const extra=document.querySelector('#preview-extra-labels');extra.replaceChildren();
  for(const [slot,value] of Object.entries(shape.labelSlots)){
    if(slot==='label')continue;const label=document.createElement('label'),field=document.createElement('input');label.textContent=slot.startsWith('row')?'Compartment row '+slot.slice(3):'Preview '+slot;field.type='text';field.value=value;field.maxLength=80;field.disabled=true;field.dataset.previewSlot=slot;field.id='preview-'+slot;label.htmlFor=field.id;field.addEventListener('input',renderPreview);label.append(field);extra.append(label);
  }
  const image=document.createElement('img');image.src='../shapes/'+shape.file;image.alt=shape.name;preview.replaceChildren(image);preview.dataset.kind=shape.kind;preview.classList.remove('preview-dark');
  text('preview-status','Loading editable preview…');anchorList(shape);
  const sources=document.querySelector('#inspector-sources');sources.replaceChildren();
  for(const url of shape.source_urls){
    const item=document.createElement('li'),name=document.createElement('span'),link=document.createElement('a'),identity=document.createElement('small');
    name.className='evidence-document';name.textContent='SysML 2.0 Language';link.href=url;link.textContent='Original notation, PDF '+url.split('=').pop();identity.textContent=catalog.source.omg_file_id;item.append(name,link,identity);sources.append(item);
  }
  text('inspector-hash',shape.sha256);
  for(const button of document.querySelectorAll('[data-inspect]'))button.setAttribute('aria-pressed',String(button.dataset.inspect===id));
  if(writeHash)history.replaceState(null,'','#'+encodeURIComponent(id));
  if(scroll){inspector.scrollIntoView({block:'start'});document.querySelector('#inspector-title').focus({preventScroll:true});}
  renderPreview();
}
for(const button of document.querySelectorAll('[data-inspect]'))button.addEventListener('click',()=>selectShape(button.dataset.inspect,{scroll:true,writeHash:true}));
document.querySelector('#preview-label').addEventListener('input',renderPreview);
document.querySelector('#preview-dark').addEventListener('change',renderPreview);
document.querySelector('#copy-preview').addEventListener('click',async()=>{
  try{if(!currentSvg)throw new Error('No preview');await copyText(new XMLSerializer().serializeToString(currentSvg));text('preview-status','Preview SVG copied, including its source and license metadata.');}
  catch(error){text('preview-status','Copy unavailable here. Use Download original SVG to save the original asset.');}
});
function fromShapeHash(){try{const id=decodeURIComponent(location.hash.slice(1));if(catalog.shapes.some(shape=>shape.id===id))selectShape(id,{scroll:true});}catch(error){}}
window.addEventListener('hashchange',fromShapeHash);
selectShape(catalog.shapes[0].id);
fromShapeHash();
