"""List every video in the client month folders and write videos.json.

The month folders must stay shared as "Anyone with the link can view".
Add a row to FOLDERS when a new month folder is created.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_folder import walk  # noqa: E402

FOLDERS = [  # (client, code, month, folder_id)
    ("Capital Hyundai", "CH", "Sep 2026", "15QzslMAfBn_VQ30J17ZGTtjHjSqwxmZw"),
    ("Capital Hyundai", "CH", "Oct 2026", "1Jl1bHkKOKHipYbflm2fLGloREXwQa-zW"),
    ("Dee Emm Hyundai", "DEH", "Sep 2026", "1qkiORVLdTv2Phn9GW4C7iyx7MzFlAoPG"),
    ("Dee Emm Hyundai", "DEH", "Oct 2026", "1K80rau_PWx7FYsr_KrS61h8x1kLeuVhU"),
    ("Dee Emm Mahindra", "DEM", "Sep 2026", "1zWAlN0Ei_D-NwEcivBTI9LEMfou49fc-"),
    ("Dee Emm Mahindra", "DEM", "Oct 2026", "19zyeNhzWBE1XRPw8BLxDvrQovh6DPfRA"),
    ("Arav Mahindra", "AM", "Sep 2026", "1DoleDQEpIUAer-PIa9rFD7XLq2jR_SUs"),
    ("Arav Mahindra", "AM", "Oct 2026", "1SMI3XogR78A39iBwLu9ww5EQ2glwZ_JX"),
    ("M R Hyundai", "MRH", "Sep 2026", "1InH_mrgt71dePHbBS_EfNQp3zWmSOgXd"),
    ("M R Hyundai", "MRH", "Oct 2026", "1-dPyeVhfZ28VwqINa0meDJLMUESYMn_5"),
    ("Car and Bike", "CB", "Sep 2026", "14scmQB0J46Y-ceurhgOEITmVM6U4EeW7"),
]

rows = []
for client, code, month, folder in FOLDERS:
    files = sorted(walk(folder), key=lambda f: f[1].lower())
    print(f"{client} {month}: {len(files)} files")
    for fid, name, modified in files:
        rows.append(dict(client=client, code=code, month=month, name=name, id=fid, modified=modified,
                         link=f"https://drive.google.com/file/d/{fid}/view"))
json.dump(rows, open("videos.json", "w"), indent=1)
print("total", len(rows))
