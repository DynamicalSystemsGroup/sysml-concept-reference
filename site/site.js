/* Progressive reading aids. Source content and native disclosures work without JS. */
(() => {
  if (location.protocol === 'file:') {
    for (const link of document.querySelectorAll('[data-offline-href]')) link.href=link.dataset.offlineHref;
  }
  const navs=[...document.querySelectorAll('.section-nav')];
  let observer;
  function observeSections(){
    if(!navs.length||!('IntersectionObserver' in window))return;
    observer?.disconnect();
    const links=navs.flatMap(nav=>[...nav.querySelectorAll('a[href^="#"]')]);
    for(const link of links)link.hidden=!document.getElementById(link.dataset.sectionTarget||link.hash.slice(1));
    const targets=links.map(link=>document.getElementById(link.dataset.sectionTarget||decodeURIComponent(link.hash.slice(1)))).filter(Boolean);
    observer=new IntersectionObserver(entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);
      if(!visible.length)return;
      for(const link of links){if((link.dataset.sectionTarget||link.hash.slice(1))===visible[0].target.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');}
    },{rootMargin:'-5% 0px -65% 0px',threshold:0});
    targets.forEach(target=>observer.observe(target));
  }
  if(document.body.classList.contains('page-browser')){
    for(const nav of navs)nav.addEventListener('click',event=>{
      const link=event.target.closest('a[href^="#"]');if(!link)return;
      const target=document.getElementById(link.dataset.sectionTarget||link.hash.slice(1));if(!target)return;
      event.preventDefault();target.scrollIntoView({block:'start'});target.tabIndex=-1;target.focus({preventScroll:true});
    });
  }
  document.addEventListener('reference:updated',observeSections);observeSections();
  // Opening reference disclosures for printing preserves their complete evidence.
  let printOpen=[],printing=false;
  addEventListener('beforeprint',()=>{if(printing)return;printing=true;printOpen=[...document.querySelectorAll('main details:not([open])')];printOpen.forEach(node=>node.open=true)});
  addEventListener('afterprint',()=>{printOpen.forEach(node=>node.open=false);printOpen=[];printing=false});
})();
