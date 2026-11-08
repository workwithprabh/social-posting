// usage: node render.js /abs/path/cover.html /abs/path/out.png
// Renders at 1080x1920 (deviceScaleFactor 1). Prints measured headline data (cap heights, head bottom).
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(900);
console.log(await p.evaluate(()=>JSON.stringify(document.body.dataset)));
await p.screenshot({path:process.argv[3]});await b.close();})();
