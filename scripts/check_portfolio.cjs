const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
const os=require('node:os');
const base=process.env.PORTFOLIO_URL || 'http://127.0.0.1:8766/';
(async()=>{const browser=await chromium.launch({headless:true});
for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844],['small',320,800]]){
 const page=await browser.newPage({viewport:{width,height}}); const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base,{waitUntil:'networkidle'});
 assert.equal(await page.locator('.portfolio-card:visible').count(),16);
 await page.getByRole('button',{name:'Sound & music',exact:true}).click();assert.equal(await page.locator('.portfolio-card:visible').count(),8);
 await page.locator('input[type=search]').fill('Neon');assert.equal(await page.locator('.portfolio-card:visible').count(),1);
 await page.locator('input[type=search]').fill('zznothing');assert.equal(await page.locator('.portfolio-card:visible').count(),0);
 assert.match(await page.locator('.collection-count').innerText(),/No apps/);
 await page.locator('input[type=search]').fill('');await page.getByRole('button',{name:'All apps',exact:true}).click();
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,name+' overflow');
 await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(os.tmpdir(),'praxis-portfolio-'+name+'.png'),fullPage:true});
 await page.getByRole('button',{name:'Dark theme',exact:true}).click();assert.equal(await page.locator('html').getAttribute('data-theme'),'black');
 await page.screenshot({path:path.join(os.tmpdir(),'praxis-portfolio-'+name+'-dark.png'),fullPage:true});assert.deepEqual(errors,[]);await page.close();console.log(name+' passed');
}
const page=await browser.newPage({javaScriptEnabled:false});await page.goto(base);assert.equal(await page.locator('.portfolio-card:visible').count(),16);await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
