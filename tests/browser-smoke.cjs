// Executes the actual generated application against a minimal DOM test double.
// This checks rendering logic and handlers, not browser layout or accessibility.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync(process.argv[2],'utf8');
const json=html.match(/<script type="application\/json" id="inventory-data">([\s\S]*?)<\/script>/)[1];
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.attrs={};this._text='';this._value=null;this.checked=false;}
  set id(id){this._id=id;nodes.set(id,this);} get id(){return this._id;}
  set textContent(value){this._text=String(value);this.children=[];}
  get textContent(){return this._text+this.children.map(n=>typeof n==='string'?n:n.textContent).join(' ');}
  set value(value){this._value=value;} get value(){return this._value??(this.tag==='select'?this.children[0]?.value:'')??'';}
  append(...children){this.children.push(...children);}
  replaceChildren(...children){this.children=[...children];this._text='';}
  setAttribute(key,value){this.attrs[key]=value;}
}
for(const id of ['inventory-data','search','support','results','concepts','detail','counts','sources']){const el=new Element('div');el.id=id;}
nodes.get('inventory-data').textContent=json;
const location={protocol:'file:',hash:''};
const callbacks={};
const context=vm.createContext({
  document:{getElementById:id=>nodes.get(id),createElement:tag=>new Element(tag),createTextNode:text=>String(text)},
  location,history:{pushState:(_,__,hash)=>{location.hash=hash;}},window:{addEventListener:(name,fn)=>{callbacks[name]=fn;}},console
});
vm.runInContext(script,context);
assert.match(nodes.get('detail').textContent,/PartUsage/);
assert.match(nodes.get('detail').textContent,/113 active; 3 replaced/);
assert.match(nodes.get('detail').textContent,/No declared default/);
nodes.get('property-view').value='replaced';nodes.get('property-view').onchange();
assert.match(nodes.get('detail').textContent,/3 declarations shown/);
for(const name of ['PartDefinition','PortUsage','ConnectionUsage']){
  vm.runInContext(`choose(items.find(([,c])=>c.name===${JSON.stringify(name)})[0])`,context);
  const text=nodes.get('detail').textContent;
  assert.match(text,/Relationships and composition/);assert.match(text,/Graphical notation/);
  assert.match(text,/Not parser-validated or executed/);
}
nodes.get('property-search').value='isComposite';nodes.get('property-search').oninput();
assert.match(nodes.get('detail').textContent,/2 declarations shown/);
assert.match(nodes.get('detail').textContent,/Declared on Feature/);
location.hash='#'+encodeURIComponent(JSON.parse(json).concepts[Object.keys(JSON.parse(json).concepts).find(id=>id.endsWith('Systems-Ports-PortUsage'))].id);
callbacks.hashchange();
assert.match(nodes.get('detail').textContent,/PortUsage/);
console.log('Generated application DOM smoke check passed for four profiles, property views, filtering and concept navigation.');
