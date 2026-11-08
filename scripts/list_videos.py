"""List every video in the client month folders and write videos.json.

Usage: python scripts/list_videos.py [Mon YYYY ...]     # default: this month and last month (India time)
e.g.   python scripts/list_videos.py "Oct 2026" "Nov 2026"

Month folders are found by name inside each client's root folder ("oct 2026", "Sept 2026", "Nov 2026" all match),
so nothing needs editing when the team adds a new month. The root folders (owned by becarrotsocial@gmail.com) must
stay shared as "Anyone with the link can view". The daily sync trigger uses the same root folder IDs.
"""
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_folder import entries, walk  # noqa: E402

ROOTS = [  # (client, code, root folder id)
    ("Capital Hyundai", "CH", "150lMiEOdNYDFoTrGrQN_t58GWPEXBFX_"),
    ("Dee Emm Hyundai", "DEH", "1gsVkvsqjy89O8K2Tc0rVQCl5p3N80ixP"),
    ("Dee Emm Mahindra", "DEM", "1CumF3EbcvxfNhxwIPwZBC6LXlhDEV-1h"),
    ("Arav Mahindra", "AM", "1njpvbueNFwJILVlVXStz85jmqulNNlSX"),
    ("M R Hyundai", "MRH", "1Tl4Ru87CdTSHUUggIygbYekEKlEWtwxR"),
    ("Car and Bike", "CB", "1YQZiRlRM70XV2OvxDQi9BYDxqo9AuOFY"),
]
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def folder_month(name):
    """'Sept 2026' -> 'Sep 2026'; 'OCT. 25' -> 'Oct 2025'; anything else -> None."""
    m = re.fullmatch(r'\s*([A-Za-z]{3})[A-Za-z]*\.?\s*(\d{4}|\d{2})\s*', name)
    if not m or m.group(1).lower() not in MONTHS:
        return None
    year = m.group(2) if len(m.group(2)) == 4 else '20' + m.group(2)
    return f"{m.group(1).capitalize()} {year}"


if __name__ == "__main__":
    wanted = [folder_month(a) for a in sys.argv[1:]]
    if not wanted:
        today = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).date().replace(day=1)
        last = today - dt.timedelta(days=1)
        wanted = [last.strftime("%b %Y"), today.strftime("%b %Y")]
    rows = []
    for client, code, root in ROOTS:
        months = {folder_month(name): fid for fid, name, is_dir, _ in entries(root) if is_dir and folder_month(name)}
        for month in wanted:
            if month not in months:
                print(f"{client}: no {month} folder")
                continue
            files = sorted((f for f in walk(months[month]) if f[1].lower().endswith(('.mp4', '.mov'))), key=lambda f: f[1].lower())
            print(f"{client} {month}: {len(files)} files")
            for fid, name, modified in files:
                rows.append(dict(client=client, code=code, month=month, name=name, id=fid, modified=modified,
                                 link=f"https://drive.google.com/file/d/{fid}/view"))
    json.dump(rows, open("videos.json", "w"), indent=1)
    print("total", len(rows))
