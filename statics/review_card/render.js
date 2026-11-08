const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
 const cards=JSON.parse(fs.readFileSync(path.join(__dirname,'cards.json')));
 const only=process.argv[2]; const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
 await p.goto('file://'+path.join(__dirname,'card.html')); await p.evaluate(()=>document.fonts.ready);
 for(const c of cards){ if(only&&c.id!==only) continue;
  const r=await p.evaluate(c=>render(c),c); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(150);
  await p.screenshot({path:path.join(process.cwd(),'out',c.id+'.jpg'),type:'jpeg',quality:92});
  console.log(c.id,JSON.stringify(r)); }
 await b.close();})();
