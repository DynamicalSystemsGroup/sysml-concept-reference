/* Run from sandbox/ with playwright-cli run-code --filename=../tests/site-browser-check.js. */
async page => {
  const base='http://127.0.0.1:8000',errors=[],assert=(ok,message)=>{if(!ok)throw new Error(message)};
  page.on('pageerror',error=>errors.push(error.message));
  const routes=['/','/docs/concept-browser.html','/docs/concepts/part-usage.html','/docs/concepts/part-definition.html','/docs/concepts/port-usage.html','/docs/concepts/connection-usage.html','/docs/rdf-inventory.html','/docs/research/property-rules.html','/docs/notation-coverage.html','/docs/notation-register.html','/docs/svg-shapes.html','/data/index.html','/queries/index.html','/docs/concept-page-contract.html','/docs/language-research.html','/docs/official-machine-readable-specs.html','/docs/publishing.html','/docs/repository.html','/docs/research/archify-design-patterns.html','/docs/research/notation-coverage-method.html','/docs/research/notation-evidence.html','/docs/research/site-redesign-audit.html','/docs/roadmap.html','/docs/svg-shapes-guide.html','/docs/parts-and-ports.html','/docs/parts-ports-notation-audit.html','/docs/research/parts-notation-audit.html','/docs/research/ports-notation-audit.html','/docs/research/parts-ports-shared-rules.html'];
  for(const width of [1440,390,320]){
    await page.setViewportSize({width,height:900});
    for(const route of routes){
      assert((await page.goto(base+route)).ok(),route+' failed');await page.evaluate(()=>document.fonts.ready);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+'px overflow on '+route);
      assert(await page.locator('h1').count()===1,'Title: '+route);
      assert(await page.evaluate(()=>{const ids=[...document.querySelectorAll('[id]')].map(n=>n.id);return ids.length===new Set(ids).size}),'Duplicate IDs: '+route);
      assert(await page.locator('.dsg-logo img').evaluate(img=>img.complete&&img.naturalWidth>0),'Logo missing');
      if(width===390){
        assert(await page.locator('.mobile-nav').evaluate(n=>!n.open),'Expanded mobile navigation');
        if(await page.locator('.mobile-section-nav').count()){
        await page.locator('.mobile-section-nav>summary').click();assert(await page.locator('.section-nav-mobile a:visible').count()>1,'Mobile section links missing');
        if(route!=='/docs/concept-browser.html'){const link=page.locator('.section-nav-mobile a:visible').first(),hash=await link.getAttribute('href');await link.click();assert(new URL(page.url()).hash===hash,'Section hash lost');}
        }
      }
      if(width!==320)await page.screenshot({path:'redesign-'+width+'-'+(route==='/'?'home':route.split('/').pop().replace('.html',''))+'.png'});
    }
  }
  await page.setViewportSize({width:1440,height:900});await page.goto(base+'/docs/concept-browser.html');
  for(const [mode,count] of [['effective',113],['properties',1],['allDeclarations',116],['replaced',3]]){await page.locator('#property-view').selectOption(mode);assert(await page.locator('.property-table tbody tr').count()===count,'Property mode '+mode);}
  await page.locator('#property-view').selectOption('replaced');assert(await page.locator('.property-table tbody tr').count()===3,'Replaced view changed');
  await page.locator('#property-search').fill('no-matching-property');assert(await page.locator('.property-table').innerText()==='No declarations match this view.','Property empty state');
  await page.locator('#property-search').fill('');await page.locator('#property-view').selectOption('effective');
  for(const name of ['PortUsage','ConnectionUsage','PartDefinition','PartUsage']){
    await page.locator('#concepts').getByRole('button',{name,exact:true}).click();assert(await page.locator('#detail>h2').innerText()===name,'Concept selection');
    const hash=new URL(page.url()).hash;await page.locator('.shell>.section-nav [data-section-target="properties"]').click();
    assert(new URL(page.url()).hash===hash,'Section replaced concept hash');assert(await page.evaluate(()=>document.activeElement.id)==='properties','Section focus');
  }
  await page.locator('#search').fill('nonexistent concept');assert(await page.locator('#concepts button').count()===0,'Concept empty search');await page.locator('#search').fill('');
  await page.locator('#support').check();await page.locator('#concepts').getByRole('button',{name:'Element',exact:true}).click();
  assert(await page.locator('.shell>.section-nav [data-section-target="notation"]').isHidden(),'Missing section navigable');
  await page.setViewportSize({width:390,height:844});await page.reload();assert(await page.locator('#concept-picker').evaluate(n=>!n.open),'Mobile picker expanded');
  await page.locator('#concept-picker>summary').click();await page.locator('#concepts').getByRole('button',{name:'PartUsage',exact:true}).click();assert(await page.locator('#concept-picker').evaluate(n=>!n.open),'Picker not closed');
  await page.goBack();assert(await page.locator('#detail>h2').innerText()==='Element','History failed');
  await page.goto(base+'/docs/svg-shapes.html#part-reference');await page.waitForFunction(()=>document.querySelector('#inspector-preview svg'));
  assert(await page.locator('#inspector-id').innerText()==='part-reference','Shape deep link');
  await page.locator('#preview-label').fill('<script>label</script>');await page.waitForFunction(()=>document.querySelector('#inspector-preview [data-slot]')?.textContent==='<script>label</script>');assert(await page.locator('#inspector-preview script').count()===0,'Unsafe label');
  await page.locator('#preview-dark').check();await page.waitForFunction(()=>document.querySelector('#inspector-preview').classList.contains('preview-dark'));
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.__previewCopy=text}}));await page.locator('#copy-preview').click();await page.waitForFunction(()=>window.__previewCopy?.includes('Apache-2.0'));
  assert(await page.evaluate(()=>window.__previewCopy.includes('&lt;script&gt;label&lt;/script&gt;')),'Copied label changed');
  await page.locator('[data-inspect="port-glyph"]').click();assert(new URL(page.url()).hash==='#port-glyph','Inspect fragment');
  await page.goto(base+'/docs/svg-shapes.html#%');assert(await page.locator('#shape-inspector').isVisible(),'Malformed fragment broke gallery');
  await page.route('**/renderer.mjs',route=>route.abort());await page.reload();await page.waitForFunction(()=>document.querySelector('#preview-status').textContent.includes('unavailable'));
  assert(await page.locator('#inspector-preview img').isVisible(),'Module fallback missing');assert((await page.locator('#inspector-download').getAttribute('href')).endsWith('/part-definition.svg'),'Fallback download');await page.unroute('**/renderer.mjs');
  await page.goto(base+'/docs/concepts/part-usage.html');const closed=await page.locator('main details:not([open])').count();assert(closed>0,'No disclosures');
  await page.emulateMedia({reducedMotion:'reduce'});assert(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)==='auto','Reduced motion');
  await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));assert(await page.locator('main details:not([open])').count()===0,'Print content hidden');await page.emulateMedia({media:'print'});assert(await page.locator('.site-nav').isHidden(),'Print chrome visible');await page.pdf({path:'redesign-profile-print.pdf'});
  await page.emulateMedia({media:'screen'});await page.evaluate(()=>dispatchEvent(new Event('afterprint')));assert(await page.locator('main details:not([open])').count()===closed,'Print changed state');
  await page.goto(base+'/');await page.keyboard.press('Tab');assert(await page.evaluate(()=>document.activeElement.className)==='skip','Keyboard skip order');await page.keyboard.press('Enter');assert(await page.evaluate(()=>document.activeElement.id)==='main','Skip focus');
  const context=await page.context().browser().newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  try{const p=await context.newPage();for(const route of ['/','/docs/concepts/part-usage.html','/docs/rdf-inventory.html','/docs/notation-coverage.html','/docs/notation-register.html','/docs/svg-shapes.html']){await p.goto(base+route);assert(await p.locator('h1').isVisible(),'No-JS title');await p.locator('.mobile-section-nav>summary').click();assert(await p.locator('.section-nav-mobile a:visible').count()>1,'No-JS sections');}}finally{await context.close()}
  assert(errors.length===0,errors.join('\n'));
  return {routes:routes.length,widths:[1440,390,320],conceptModes:'passed',sectionHashes:'passed',history:'passed',inspector:'passed',moduleFallback:'passed',print:'passed',reducedMotion:'passed',keyboard:'passed',noJavaScript:'passed'};
}
