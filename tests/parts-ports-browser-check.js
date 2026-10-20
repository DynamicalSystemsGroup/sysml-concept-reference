/* Run from sandbox/ against the generated site on port 8000. */
async page => {
  const base='http://127.0.0.1:8000',errors=[],assert=(ok,msg)=>{if(!ok)throw new Error(msg)};
  page.on('pageerror',e=>errors.push(e.message));
  for(const width of [1440,390,320]){
    await page.setViewportSize({width,height:1000});
    for(const route of ['parts-and-ports','parts-ports-notation-audit','notation-coverage','notation-register']){
      assert((await page.goto(base+'/docs/'+route+'.html')).ok(),'Page unavailable');await page.evaluate(()=>document.fonts.ready);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),route+' overflow at '+width);
      if(width!==320)await page.screenshot({path:'parts-ports-'+route+'-'+width+'.png'});
    }
  }
  await page.setViewportSize({width:1440,height:1000});await page.goto(base+'/docs/svg-shapes.html');
  assert(await page.locator('.shape-card').count()===20,'Missing components');
  const ids=await page.locator('.shape-card').evaluateAll(nodes=>nodes.map(n=>n.id));
  for(const id of ids){
    await page.locator('[data-inspect="'+id+'"]').click();await page.waitForFunction(()=>!!document.querySelector('#inspector-preview svg')&&!document.querySelector('#copy-preview').disabled);
    const overflow=await page.locator('#inspector-preview svg').evaluate(svg=>{const v=svg.viewBox.baseVal;return [...svg.querySelectorAll('text')].filter(n=>{const b=n.getBBox();return b.x<v.x||b.x+b.width>v.x+v.width||b.y<v.y||b.y+b.height>v.y+v.height}).map(n=>n.textContent)});
    assert(!overflow.length,id+' default label overflow: '+overflow.join(','));
  }
  await page.locator('[data-inspect="part-definition-parts"]').click();await page.waitForFunction(()=>!document.querySelector('#preview-row1')?.disabled);
  await page.locator('#preview-row1').fill('<script>literal row</script>');await page.waitForFunction(()=>document.querySelector('#inspector-preview [data-slot="row1"]')?.textContent==='<script>literal row</script>');
  assert(await page.locator('#inspector-preview script').count()===0,'Unsafe row');await page.locator('#preview-dark').check();await page.waitForFunction(()=>document.querySelector('#inspector-preview').classList.contains('preview-dark'));
  await page.screenshot({path:'parts-ports-compartment-inspector.png'});
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.__rowCopy=text}}));await page.locator('#copy-preview').click();await page.waitForFunction(()=>window.__rowCopy?.includes('&lt;script&gt;literal row&lt;/script&gt;'));
  await page.locator('[data-inspect="port-arrow-horizontal-both"]').click();await page.waitForFunction(()=>!!document.querySelector('#inspector-preview svg')&&!document.querySelector('#copy-preview').disabled);
  assert(await page.locator('#preview-extra-labels input').count()===0,'Stale row controls');assert(await page.locator('#preview-label').isDisabled(),'Glyph label control active');
  const audit=await (await page.request.get(base+'/data/parts-ports-audit.json')).json();assert(audit.units.length===50,'Ledger incomplete');
  await page.goto(base+'/shapes/examples/parts-ports.svg');await page.screenshot({path:'parts-ports-component-composition.png'});
  const context=await page.context().browser().newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  try{const p=await context.newPage();await p.goto(base+'/docs/parts-and-ports.html');assert(await p.getByRole('heading',{name:'Follow the assembly'}).isVisible(),'Static guide missing');assert(await p.locator('article img').evaluate(n=>n.complete&&n.naturalWidth>0),'Static image missing');await p.goto(base+'/docs/svg-shapes.html');assert(await p.getByRole('link',{name:'Download SVG',exact:true}).count()===20,'Static downloads incomplete');}finally{await context.close()}
  assert(errors.length===0,errors.join('\n'));
  return {widths:[1440,390,320],componentPreviews:ids.length,safeRows:'passed',copy:'passed',controlReset:'passed',publishedUnits:50,noJavaScript:'passed'};
}
