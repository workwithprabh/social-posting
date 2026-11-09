const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
 const cards=JSON.parse(fs.readFileSync(path.join(__dirname,'cards_emi.json')));
 const only=process.argv[2]; const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
 await p.goto('file://'+path.join(__dirname,'emi.html')); await p.evaluate(async()=>{for(const f of ['500 20px Play','italic 500 20px Play','400 20px Anton','500 20px Mont','600 20px Mont','700 20px Mont','800 20px Mont']) await document.fonts.load(f); await document.fonts.ready;});
 for(const c of cards){ if(only&&c.id!==only) continue;
  const r=await p.evaluate(c=>render(c),c); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(150);
  await p.screenshot({path:path.join(__dirname,'out',c.id+'.png'),type:'png'});   // 2160x2700 master; save.py makes the JPEGs
  console.log(c.id,JSON.stringify(r)); }
 await b.close();})();
