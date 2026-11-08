"""Pick Dee Emm Hyundai's best 5-star Google reviews from the DMU GBP sheet (Reviews_Raw) for the tracker's Reviews tab.

Usage:
  python scripts/dmu_reviews.py <Reviews_Raw.csv> [--days 60] [--per-branch 8] [--min-words 10] [--exclude ids.txt]

Picks are candidates: a person still reads each one and keeps only reviews in clear English that need at most
typo-level fixes (spelling, capitals, spacing, punctuation) for the "Text for post" column; never reword.
Rules: 5 stars, not Removed, no Duplicate_Flag (Google removes those far more often), the reviewer's own words
(Google's auto-translation dropped), at least --min-words words and at most --max-chars characters. Ranked by detail: length, plus a bonus for
naming staff or describing delivery/service. Prints JSON rows in the Reviews tab's column order.
The DMU sheet (1r9c4Bhjsya3kDnBbUldHnZyeg-0T30tP3hPaJpI_3p4) is filled every 3 hours by the GitHub job in
deeemm-hyundai-lp; this script only reads an export of it.
"""
import argparse
import csv
import datetime as dt
import json
import re

BONUS = re.compile(r'\b(mr|ms|mrs|sir|ma\'?am|advisor|adviser|executive|manager|team|staff|delivery|delivered|service|serviced|'
                   r'explained|patient|helpful|smooth|hassle|recommend)\b', re.I)


def original(t):
    if '(Original)' in t:
        return t.split('(Original)', 1)[1].strip()
    return re.sub(r'\s*\(Translated by Google\).*$', '', t, flags=re.S).strip()


def post_name(n):
    """'pooja sehgal' -> 'Pooja S.'; digits and honorifics dropped ('SACHIN YADAV8826' -> 'Sachin Y.', 'Shivam Veram ji' -> 'Shivam V.')."""
    words = [re.sub(r'\d+', '', w) for w in (n or '').split()]
    parts = [w for w in words if w.isalpha() and w.lower() not in ('ji', 'sir', 'mr', 'mrs', 'ms', 'dr')]
    if not parts:
        return 'A Google user'
    first = parts[0].capitalize()
    return first if len(parts) == 1 else f'{first} {parts[-1][0].upper()}.'


def score(t):
    return min(len(t.split()), 90) + 12 * min(len(BONUS.findall(t)), 3)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('csv'); ap.add_argument('--days', type=int, default=60); ap.add_argument('--per-branch', type=int, default=8)
    ap.add_argument('--min-words', type=int, default=25); ap.add_argument('--max-chars', type=int, default=500)
    ap.add_argument('--exclude')
    a = ap.parse_args()
    skip = set(open(a.exclude).read().split()) if a.exclude else set()
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    picks = {}
    for r in csv.DictReader(open(a.csv, encoding='utf-8')):
        if r['Star_Rating'] != 'FIVE' or r['Current_Status'] == 'Removed' or (r.get('Duplicate_Flag') or '').strip():
            continue
        if r['Review_ID'] in skip:
            continue
        t = original(r['Review_Text'] or '')
        if len(t.split()) < a.min_words or len(t) > a.max_chars:   # long reviews can't be quoted in full on a card
            continue
        if '\u201c' in t or re.match(r'\s*(google review|showroom\s*$)', t, re.I | re.M):   # reads like a pasted template
            continue
        when = dt.datetime.fromisoformat(r['Review_Create_Time'].replace('Z', '+00:00'))
        if when < since:
            continue
        branch = r['Location_Name'].replace('DM Hyundai ', '')
        picks.setdefault(branch, []).append((score(t), when, r, t))
    rows = []
    for branch, lst in picks.items():
        for s, when, r, t in sorted(lst, key=lambda x: (-x[0], -x[1].timestamp()))[:a.per_branch]:
            rows.append([r['Review_ID'], 'Dee Emm Hyundai', branch, 5, r['Reviewer_Name'], post_name(r['Reviewer_Name']), t,
                         r['Review_Date'], r['Review_URL'], 'New', '', 'From the DMU GBP sheet'])
    rows.sort(key=lambda x: dt.datetime.strptime(x[7], '%d %b %Y'), reverse=True)
    print(json.dumps(rows, ensure_ascii=False))
