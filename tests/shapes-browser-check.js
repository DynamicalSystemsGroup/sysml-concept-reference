async page => {
  const base='http://127.0.0.1:8000';
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  const assert=(condition,message)=>{if(!condition)throw new Error(message)};
  await page.goto(base+'/docs/svg-shapes.html');
  assert(await page.locator('.shape-card').count()===9,'Expected nine cards');
  await page.locator('#shape-search').fill('boundary');
  assert(await page.locator('.shape-card:visible').count()===1,'Search did not filter to glyph');
  await page.locator('#shape-search').fill('');
  await page.locator('#shape-family').selectOption('Connections');
  assert(await page.locator('.shape-card:visible').count()===4,'Family filter failed');
  await page.locator('#shape-search').fill('no-such-shape');
  assert(await page.locator('#shape-empty').isVisible(),'Empty state missing');
  await page.locator('#shape-search').fill('');await page.locator('#shape-family').selectOption('');
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.__copiedSVG=text}}}));
  await page.getByRole('button',{name:'Copy SVG for Composite part usage',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#copy-status').textContent.includes('SVG copied'));
  assert(await page.evaluate(()=>window.__copiedSVG.includes('Apache-2.0')&&window.__copiedSVG.includes('<svg')),'Copy omitted SVG/license metadata');
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('Unavailable')}}}));
  await page.getByRole('button',{name:'Copy SVG for Composite part usage',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('#copy-status').textContent.includes('Use Download SVG'));
  await page.setViewportSize({width:390,height:844});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile page overflow');
  await page.setViewportSize({width:1280,height:900});
  const response=await page.request.get(base+'/shapes/renderer.mjs');
  assert(response.ok()&&response.headers()['content-type'].includes('javascript'),'Module MIME invalid');
  await page.goto(base+'/shapes/examples/renderer.html');
  await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('(252, 120)'));
  assert(await page.locator('#drawing > svg').count()===3,'Composition failed');
  await page.locator('#theme').click();
  await page.waitForFunction(()=>document.querySelector('#drawing > svg').style.getPropertyValue('--sysml-stroke')==='#7f601b');
  await page.evaluate(()=>{
    const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg'),use=document.createElementNS(ns,'use');
    svg.id='sprite-test';svg.setAttribute('viewBox','0 0 240 140');svg.setAttribute('width','240');svg.setAttribute('height','140');
    use.setAttribute('href','../shapes.svg#sysml-part-usage');svg.append(use);document.body.append(svg);
  });
  await page.waitForFunction(()=>document.querySelector('#sprite-test use').getBBox().width>200);
  const result=await page.evaluate(async()=>{
    const {createShape}=await import('../renderer.mjs');
    const literal='<script>untrusted label</script>';
    const svg=await createShape('part-reference',{labels:{label:literal},theme:{stroke:'#7f601b'},title:'Safe label test'});
    document.querySelector('#drawing').append(svg);
    const repeat=await createShape('part-reference');document.querySelector('#drawing').append(repeat);
    const failures=[];
    for(const [id,options] of [['missing',{}],['part-usage',{labels:{unknown:'text'}}],['part-usage',{width:0}],['part-usage',{theme:{unknown:'red'}}]]){
      try{await createShape(id,options);failures.push(id)}catch(error){}
    }
    const ids=[...document.querySelectorAll('[id]')].map(node=>node.id);
    return {literal:svg.querySelector('[data-slot]').textContent===literal,noScript:!svg.querySelector('script'),
      keyword:[...svg.querySelectorAll('text')].some(node=>node.textContent==='«ref part»'),
      stroke:getComputedStyle(svg.querySelector('rect')).stroke,duplicateIds:ids.length-new Set(ids).size,failures};
  });
  assert(result.literal&&result.noScript&&result.keyword,'Unsafe label edit or changed keyword');
  assert(result.stroke==='rgb(127, 96, 27)','Theme not applied');
  assert(result.duplicateIds===0&&result.failures.length===0,'Invalid API option accepted or duplicate IDs');
  const staticContext=await page.context().browser().newContext({javaScriptEnabled:false});
  try{
    const staticPage=await staticContext.newPage();await staticPage.goto(base+'/docs/svg-shapes.html');
    assert(await staticPage.locator('.shape-card').count()===9,'Static cards missing');
    assert(await staticPage.getByRole('link',{name:'Download SVG',exact:true}).count()===9,'Static downloads missing');
    assert(await staticPage.locator('.shape-filters').isHidden(),'Inactive static filters visible');
    assert(await staticPage.locator('[data-copy]:visible').count()===0,'Inactive static copy buttons visible');
  }finally{await staticContext.close()}
  assert(errors.length===0,errors.join('\n'));
  return {galleryCards:9,connectionFilter:4,copyHandler:'passed',composition:'passed',safeLabels:'passed',theme:'passed',cloneIds:'passed',invalidOptions:'passed'};
}
