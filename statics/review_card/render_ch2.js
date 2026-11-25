// node render_ch2.js [ID] -> out_ch2/<ID>.png at 2160x2700 (4:5 at 2x), from cards_ch2.json.
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const cards=JSON.parse(fs.readFileSync(path.join(__dirname,'cards_ch2.json'))); const only=process.argv[2];
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
 fs.mkdirSync(path.join(__dirname,'out_ch2'),{recursive:true});
 for(const c of cards){ if(only&&c.id!==only) continue;
  await p.goto('file://'+path.join(__dirname,c.tpl||'ch2.html'));
  await p.evaluate(async()=>{for(const f of ['700 20px Brico','800 20px Brico','500 20px Inter','600 20px Inter','700 20px Inter','800 20px Inter','400 20px Roboto','500 20px Roboto','700 20px Hand']) await document.fonts.load(f,'ਕ A'); await document.fonts.ready;});
  const r=await p.evaluate(c=>render(c),c); await p.waitForTimeout(300);
  await p.screenshot({path:path.join(__dirname,'out_ch2',c.id+'.png')}); console.log(c.id,JSON.stringify(r)); }
 await b.close();})();
