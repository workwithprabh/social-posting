"""Photo card for reelcover_ctr.html: a crop of a reel frame or an official photo, brightened, with a white border,
soft shadow and a slight tilt, on a transparent PNG. Use it when a cut-out car would float (no real floor shadow).
usage: python3 mkcard.py src.jpg out.png x0,y0,x1,y1 angle [brightness=1.08]   (crop box as fractions)"""
import sys
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
src,dst,box,ang=sys.argv[1],sys.argv[2],[float(v) for v in sys.argv[3].split(',')],float(sys.argv[4])
br=float(sys.argv[5]) if len(sys.argv)>5 else 1.08
im=Image.open(src).convert('RGB'); W,H=im.size
im=im.crop((int(box[0]*W),int(box[1]*H),int(box[2]*W),int(box[3]*H)))
im=ImageOps.autocontrast(im,cutoff=0.5)
im=ImageEnhance.Brightness(im).enhance(br); im=ImageEnhance.Color(im).enhance(1.18); im=ImageEnhance.Contrast(im).enhance(1.06)
im=im.filter(ImageFilter.UnsharpMask(2,80,2))
tw=1180; im=im.resize((tw,int(im.height*tw/im.width)),Image.LANCZOS)
b=24; card=Image.new('RGBA',(im.width+2*b,im.height+2*b),(255,255,255,255)); card.paste(im,(b,b))
pad=110; canvas=Image.new('RGBA',(card.width+2*pad,card.height+2*pad),(0,0,0,0))
sh=Image.new('RGBA',canvas.size,(0,0,0,0)); sh.paste(Image.new('RGBA',card.size,(0,0,0,170)),(pad+10,pad+24)); sh=sh.filter(ImageFilter.GaussianBlur(28))
canvas.alpha_composite(sh); canvas.alpha_composite(card,(pad,pad))
canvas=canvas.rotate(ang,resample=Image.BICUBIC,expand=True)
canvas=canvas.crop(canvas.getbbox()); canvas.save(dst); print(dst,canvas.size)
