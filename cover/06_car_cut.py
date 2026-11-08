"""Cut a car out of a reel frame when rembg fails (dark cars / people in front).
usage: python3 06_car_cut.py frame.png car_final.png  [edit the boxes below per frame]
Steps used for Reel 5: blur number plate -> mirror (so the frame-cut side is off the cover edge)
-> u2net finds the person in front -> GrabCut the car with that person marked as background."""
import sys, numpy as np, cv2
from PIL import Image, ImageFilter, ImageOps, ImageDraw
from rembg import remove, new_session
src,dst=sys.argv[1],sys.argv[2]
PLATE=(860,1025,1010,1080)        # number-plate box in the ORIGINAL frame (blurred so mirrored text never shows)
CROP=(0,690,800,1260)             # region of the MIRRORED frame that holds the car
PROB_FG=(0,40,560,520); DEF_FG=(20,230,380,430)   # in CROP coords: probable car area / sure car core (grille)
CLEAN=[(0,0),(240,0),(214,64),(93,150),(14,229),(0,229)]  # polygon of leftover background to erase
im=Image.open(src).convert('RGB'); im.paste(im.crop(PLATE).filter(ImageFilter.GaussianBlur(9)),PLATE[:2])
im=ImageOps.mirror(im); im.save('car_panel.png')
crop=np.array(im.crop(CROP)); H,W=crop.shape[:2]
man=np.array(remove(Image.fromarray(crop),session=new_session('u2net')))[...,3]>40
man=cv2.dilate(man.astype(np.uint8),np.ones((25,25),np.uint8))>0
mask=np.full((H,W),cv2.GC_PR_BGD,np.uint8)
x0,y0,x1,y1=PROB_FG; mask[y0:y1,x0:x1]=cv2.GC_PR_FGD
x0,y0,x1,y1=DEF_FG; mask[y0:y1,x0:x1]=cv2.GC_FGD
mask[:25,:]=cv2.GC_BGD; mask[man]=cv2.GC_BGD; mask[:,700:]=cv2.GC_BGD; mask[545:,:]=cv2.GC_BGD
bgd=np.zeros((1,65)); fgd=np.zeros((1,65))
cv2.grabCut(cv2.cvtColor(crop,cv2.COLOR_RGB2BGR),mask,None,bgd,fgd,8,cv2.GC_INIT_WITH_MASK)
m=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((7,7),np.uint8)); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); m=np.where(lab==k,255,0).astype(np.uint8)
m=cv2.GaussianBlur(m,(0,0),1.5)
cm=Image.new('L',(W,H),255); ImageDraw.Draw(cm).polygon(CLEAN,fill=0); cm=np.array(cm.filter(ImageFilter.GaussianBlur(2)))
a=(m.astype(float)*cm/255).astype(np.uint8)
out=Image.fromarray(np.dstack([crop,a])); out.crop(out.getbbox()).save(dst); print('saved',dst,out.getbbox())
