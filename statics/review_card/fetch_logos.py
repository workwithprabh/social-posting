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
    'MRH_3.png': '1Lzn99WH2W5xm8N07vDIqvBWw2HzPtSfd',           # M R Hyundai, white stacked
    'AM_group1.png': '1-fHaW4_84yWTnCWsmojVEXWepUuDfIA4',       # Mahindra Arav, white
    'DEM_transparent.png': '1yGX8NLHbupLmkPcNU3wEtphWIvwdyZ07', # Dee Emm Mahindra EV logo: EV posts only
    'DEM_ice_white.png': '1LMRsS3JY-HEZhHkTAVvna7CbTo6v4s-u',   # Dee Emm Mahindra twin peaks, white: all other posts
}
for name, fid in LOGOS.items():
    drive_folder.download(fid, name)
    im = Image.open(name)
    im.crop(im.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()).save(name)
    print(name, im.size)
