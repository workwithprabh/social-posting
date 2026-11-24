// node render_gurpurab.js [ID] -> out_gp/<ID>.png at 2160x2700 (4:5 at 2x), from cards_gurpurab.json.
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const cards=JSON.parse(fs.readFileSync(path.join(__dirname,'cards_gurpurab.json'))); const only=process.argv[2];
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
 fs.mkdirSync(path.join(__dirname,'out_gp'),{recursive:true});
 for(const c of cards){ if(only&&c.id!==only) continue;
  await p.goto('file://'+path.join(__dirname,c.tpl||'gurpurab.html'));
  await p.evaluate(async()=>{for(const f of ['500 20px Mont','600 20px Mont','700 20px Mont','800 20px Mont','italic 700 20px Play','600 20px Play','700 20px Gur','400 20px Anton']) await document.fonts.load(f,'ਕ A'); await document.fonts.ready;});
  const r=await p.evaluate(c=>render(c),c); await p.waitForTimeout(300);
  await p.screenshot({path:path.join(__dirname,'out_gp',c.id+'.png')}); console.log(c.id,JSON.stringify(r)); }
 await b.close();})();
