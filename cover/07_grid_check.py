"""Preview a cover as Instagram shows it: full 9:16 (Reels tab) and centre 3:4 crop (main profile grid, y 240-1680).
usage: python3 07_grid_check.py cover.png [reference_tile.png ...]  -> grid_check.png"""
import sys
from PIL import Image
c=Image.open(sys.argv[1]).convert('RGB'); refs=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
tiles=[c.resize((360,640)),c.crop((0,240,1080,1680)).resize((360,480))]+[r.resize((360,int(r.height*360/r.width))) for r in refs]
H=max(t.height for t in tiles); out=Image.new('RGB',(len(tiles)*370+10,H+20),(255,255,255))
for i,t in enumerate(tiles): out.paste(t,(10+i*370,10))
out.save('grid_check.png'); print('grid_check.png')
