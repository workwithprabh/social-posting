"""Download the white client logos used on review cards into the current folder and crop them to the artwork.

Run from the working folder that holds card.html (never inside the repo): python fetch_logos.py
"""
import sys
sys.path.insert(0, __file__.rsplit('/statics/', 1)[0] + '/scripts')
import drive_folder
from PIL import Image

LOGOS = {  # file name used by cards.json -> Drive file id (folders in statics/clients.json)
    'CH_cap.png': '1jP9yI7-VeE_OPEiFY5COH36x_AyPOihL',          # Capital Hyundai, white
    'DEH_white.png': '1ORTfE9aVdmiM68vKmEkeDqdnOnhrq1T9',       # Dee Emm Hyundai, white
    'MRH_3.png': '1Lzn99WH2W5xm8N07vDIqvBWw2HzPtSfd',           # M R Hyundai, white stacked (used on cards)
    'AM_group1.png': '1-fHaW4_84yWTnCWsmojVEXWepUuDfIA4',       # Mahindra Arav, white
    'DEM_transparent.png': '1yGX8NLHbupLmkPcNU3wEtphWIvwdyZ07', # Dee Emm Mahindra EV logo: EV posts only
    'DEM_ice_white.png': '1LMRsS3JY-HEZhHkTAVvna7CbTo6v4s-u',   # Dee Emm Mahindra twin peaks, white: all other posts
}
def mrh_one_line():
    # M R Hyundai posts use a one-line logo; the Drive copy is only 100px, so rebuild it from the stacked logo's pieces
    im = Image.open('MRH_3.png').convert('RGBA'); import numpy as np
    rows = np.where((np.array(im)[..., 3] > 20).any(1))[0]; g = np.where(np.diff(rows) > 3)[0][0]
    tight = lambda x: x.crop(x.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    emb, txt = tight(im.crop((0, 0, im.size[0], rows[g] + 1))), tight(im.crop((0, rows[g + 1], im.size[0], im.size[1])))
    h = txt.size[1]; e = emb.resize((round(emb.size[0] * h * 1.05 / emb.size[1]), round(h * 1.05)), Image.LANCZOS)
    gap = round(h * .55); out = Image.new('RGBA', (e.size[0] + gap + txt.size[0], max(e.size[1], h)))
    out.paste(e, (0, (out.size[1] - e.size[1]) // 2), e); out.paste(txt, (e.size[0] + gap, (out.size[1] - h) // 2), txt)
    out.save('MRH_line.png')


for name, fid in LOGOS.items():
    drive_folder.download(fid, name)
    im = Image.open(name)
    im.crop(im.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()).save(name)
    print(name, im.size)
mrh_one_line()
print("MRH_line.png built")

# High-resolution logos for the 2160x2700 masters (8 Nov 2026). Drive only has small Dee Emm Hyundai (313px),
# M R Hyundai (280px) and Capital Hyundai (703px) files, so their flat white shapes are rebuilt at 2-4x with
# upscale_logo.py (same shapes, crisp edges). Mahindra Arav uses its 2200px black file, turned white.
import subprocess, numpy as np
here = __file__.rsplit('/', 1)[0]
for src, dst, k in [('DEH_white.png', 'DEH_white_hr.png', 4), ('MRH_3.png', 'MRH_3_hr.png', 3), ('CH_cap.png', 'CH_cap_hr.png', 2)]:
    subprocess.run(['python3', f'{here}/upscale_logo.py', src, dst, str(k), 'white'], check=True)
drive_folder.download('1cuCmyzYMvy3TX4X4YcJ5lAQePQVPGi4U', 'AM_black.png')
a = np.array(Image.open('AM_black.png').convert('RGBA'))
bb = Image.fromarray(a[..., 3]).point(lambda v: 255 if v > 20 else 0).getbbox(); a = a[bb[1]:bb[3], bb[0]:bb[2]]; a[..., :3] = 255
Image.fromarray(a, 'RGBA').save('AM_hr.png'); print('AM_hr.png built')
