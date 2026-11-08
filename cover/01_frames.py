"""Contact sheets for choosing frames.
usage: python3 01_frames.py reel.mp4 [fps=1]
writes frames/f_XXX.jpg and sheet.jpg (9 columns, labelled with the second)."""
import sys, subprocess, glob, os
from PIL import Image, ImageDraw
v=sys.argv[1]; fps=float(sys.argv[2]) if len(sys.argv)>2 else 1
os.makedirs('frames',exist_ok=True)
for f in glob.glob('frames/*.jpg'): os.remove(f)
subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'fps={fps},scale=270:-1','frames/f_%03d.jpg'],check=True)
fs=sorted(glob.glob('frames/*.jpg')); w,h=Image.open(fs[0]).size; cols=9; rows=(len(fs)+cols-1)//cols
s=Image.new('RGB',(cols*w,rows*(h+16)),(255,255,255)); d=ImageDraw.Draw(s)
for i,f in enumerate(fs):
    x,y=(i%cols)*w,(i//cols)*(h+16); s.paste(Image.open(f),(x,y)); d.text((x+4,y+h+2),f'{(i+0.5)/fps:.1f}s',fill=(0,0,0))
s.save('sheet.jpg',quality=85); print('sheet.jpg',s.size,len(fs),'frames')
