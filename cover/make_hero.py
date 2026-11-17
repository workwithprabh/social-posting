"""Official studio photo -> grounded hero PNG for reelcover_ctr.html (cut-out, glow-up, the photo's real shadow).
usage: python3 make_hero.py studio.jpg out.png [gamma=0.8]   (prints the size and lowest tyre row)"""
import sys, os, subprocess, tempfile
from PIL import Image
from rembg import remove, new_session
here=os.path.dirname(os.path.abspath(__file__)); src,dst=sys.argv[1],sys.argv[2]; g=sys.argv[3] if len(sys.argv)>3 else '0.8'
t=tempfile.mkdtemp(); im=Image.open(src).convert('RGB'); im=im.resize((im.width*2,im.height*2),Image.LANCZOS)
cut=remove(im,session=new_session('isnet-general-use')); cut=cut.crop(cut.getbbox()); cut.save(t+'/cut.png')
subprocess.run([sys.executable,here+'/hero_glow.py',t+'/cut.png',t+'/glow.png',g],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,here+'/hero_studio_shadow.py',src,t+'/cut.png',t+'/glow.png',dst],check=True)
