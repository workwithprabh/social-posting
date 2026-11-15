// node render_reel.js [ID] -> out_reel/<ID>.png, 1080x1920 reel covers in the static-post look (no logo, no numbers).
// Mahindra and Car & Bike use reelcover.html (theme mahindra / carbike); Hyundai cards (mode set) use reelcover_hy.html.
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const cards=JSON.parse(fs.readFileSync(path.join(__dirname,'cards_reel.json'))); const only=process.argv[2];
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 fs.mkdirSync(path.join(__dirname,'out_reel'),{recursive:true});
 for(const c of cards){ if(only&&c.id!==only) continue;
  await p.goto('file://'+path.join(__dirname,c.mode?'reelcover_hy.html':'reelcover.html'));
  await p.evaluate(async()=>{for(const f of ['400 20px Anton','500 20px Mont','600 20px Mont','700 20px Mont','800 20px Mont']) await document.fonts.load(f); await document.fonts.ready;});
  const r=await p.evaluate(c=>render(c),c); await p.waitForTimeout(200);
  await p.screenshot({path:path.join(__dirname,'out_reel',c.id+'.png')}); console.log(c.id,JSON.stringify(r)); }
 await b.close();})();
