"""Copy a video's thumbnail from the Drive thumbnail folder into thumbnails/.

Usage: python scripts/fetch_thumbnail.py CH-2610-04 [MORE-IDS...]

Looks through every subfolder for an image named after the Video ID (CH-2610-04.jpg, .jpeg, .png or .webp)
and saves it as thumbnails/<VIDEO-ID>.<ext>. Its public link for Instagram is then
https://raw.githubusercontent.com/workwithprabh/social-posting/main/thumbnails/<VIDEO-ID>.<ext>
once committed and pushed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_folder import download, walk  # noqa: E402

THUMBNAIL_FOLDER = "1u6J5NUVc51ZufYb6n5AmO7JXd1QL2Y_D"
EXTS = (".jpg", ".jpeg", ".png", ".webp")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "thumbnails")

wanted = {v.upper() for v in sys.argv[1:]}
if not wanted:
    sys.exit(__doc__)

found = {}
for fid, path, _ in walk(THUMBNAIL_FOLDER):
    stem, ext = os.path.splitext(os.path.basename(path))
    vid = stem.strip().upper()
    if vid in wanted and ext.lower() in EXTS:
        if vid in found:
            sys.exit(f"Two thumbnails found for {vid}: {found[vid][1]} and {path}")
        found[vid] = (fid, path, ext.lower())

for vid in sorted(wanted):
    if vid not in found:
        print(f"{vid}: no thumbnail in the Drive folder")
        continue
    fid, path, ext = found[vid]
    dest = os.path.join(OUT, vid + (".jpg" if ext == ".jpeg" else ext))
    download(fid, dest)
    print(f"{vid}: saved {path} -> thumbnails/{os.path.basename(dest)}")
