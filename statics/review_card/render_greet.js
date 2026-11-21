// node render_greet.js [ID] -> out_greet/<ID>.png at 2160x2700 (4:5 at 2x). Festival greetings from cards_greet.json.
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const cards=JSON.parse(fs.readFileSync(path.join(__dirname,'cards_greet.json'))); const only=process.argv[2];
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:2});
 fs.mkdirSync(path.join(__dirname,'out_greet'),{recursive:true});
 for(const c of cards){ if(only&&c.id!==only) continue;
  await p.goto('file://'+path.join(__dirname,'greeting.html'));
  await p.evaluate(async()=>{for(const f of ['400 20px Anton','500 20px Mont','600 20px Mont','700 20px Mont','800 20px Mont','700 20px Gur']) await document.fonts.load(f,'ੴ A'); await document.fonts.ready;});
  const r=await p.evaluate(c=>render(c),c); await p.waitForTimeout(300);
  await p.screenshot({path:path.join(__dirname,'out_greet',c.id+'.png')}); console.log(c.id,JSON.stringify(r)); }
 await b.close();})();
