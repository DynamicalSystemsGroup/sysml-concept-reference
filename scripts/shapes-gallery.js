'use strict';
const search=document.querySelector('#shape-search'), family=document.querySelector('#shape-family');
const cards=[...document.querySelectorAll('.shape-card')];
document.querySelector('.shape-filters').hidden=false;
for(const button of document.querySelectorAll('[data-copy]'))button.hidden=false;
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
for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{
  const status=document.querySelector('#copy-status');
  try{
    const response=await fetch(button.dataset.copy);
    if(!response.ok)throw new Error('Download unavailable');
    const text=await response.text();
    if(!navigator.clipboard?.writeText)throw new Error('Clipboard access unavailable');
    await navigator.clipboard.writeText(text);status.textContent='SVG copied, including source and license metadata.';
  }catch(error){status.textContent='Copy unavailable here. Use Download SVG to save the file.';}
});
