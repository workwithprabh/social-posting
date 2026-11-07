"""usage: pick.py video out.jpg t1 t2 ... -> tiles of the upper-body crop at full res, labelled"""
import sys, subprocess, io
from PIL import Image, ImageDraw
v,out,ts=sys.argv[1],sys.argv[2],sys.argv[3:]
tiles=[]
for t in ts:
    png=subprocess.run(['ffmpeg','-v','error','-ss',t,'-i',v,'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True).stdout
    im=Image.open(io.BytesIO(png)).convert('RGB').crop((190,180,890,1000)).resize((350,410))
    d=ImageDraw.Draw(im); d.rectangle((0,0,60,20),fill=(0,0,0)); d.text((4,4),t+'s',fill=(255,255,0)); tiles.append(im)
cols=6; rows=(len(tiles)+cols-1)//cols
s=Image.new('RGB',(cols*350,rows*410),'white')
for i,t in enumerate(tiles): s.paste(t,((i%cols)*350,(i//cols)*410))
s.save(out,quality=88)
