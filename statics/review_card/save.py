"""Turn the rendered PNG masters into the files we keep and post.
<ID>.jpg     2160x2700, JPEG q95, 4:4:4 chroma (no colour bleed on red/blue text): stored in Drive, used for Facebook.
<ID>_IG.jpg  1080x1350 (Instagram's native 4:5 size, Lanczos), JPEG q95 4:4:4: made at publish time for Instagram,
             so Instagram does not resize it again.
usage: python save.py out/ [--ig]"""
import sys, glob, os
from PIL import Image
d = sys.argv[1]
for png in sorted(glob.glob(os.path.join(d, '*.png'))):
    im = Image.open(png).convert('RGB'); base = png[:-4]
    im.save(base + '.jpg', quality=95, subsampling=0, optimize=True)
    if '--ig' in sys.argv:
        im.resize((1080, 1350), Image.LANCZOS).save(base + '_IG.jpg', quality=95, subsampling=0, optimize=True)
    os.remove(png); print(os.path.basename(base), im.size)
