"""Read Google Business Profile reviews for the clients' locations (read-only).

Needs three environment variables (set in the environment settings, never in chat or the repo):
  GBP_CLIENT_ID, GBP_CLIENT_SECRET  - the OAuth client from Google Cloud
  GBP_REFRESH_TOKEN                 - refresh token with the business.manage scope (see statics/GBP_SETUP.md)

Usage:
  python scripts/gbp_reviews.py check                          # token works? which accounts/locations can it see
  python scripts/gbp_reviews.py reviews [--min-stars 5] [--since 2026-10-01] [--out reviews.json]

`reviews` prints candidate rows in the column order of the sheet's Reviews tab (A-M). A person then keeps only
good reviews and writes column M (Text for post) in correct English: grammar corrected or rephrased, keeping the
customer's meaning and facts (statics/CONTENT_BUCKETS.md). Never prints a token.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

STARS = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4, 'FIVE': 5}
CLIENTS = [  # location title keyword -> client name used in the sheet
    (r'capital\s*hyundai', 'Capital Hyundai'),
    (r'dee\s*emm\s*hyundai|deeemm\s*hyundai|dm\s*hyundai', 'Dee Emm Hyundai'),
    (r'\bm\.?\s*r\.?\s*hyundai', 'M R Hyundai'),
    (r'arav', 'Mahindra Arav'),
    (r'dee\s*emm\s*mahindra|deeemm\s*mahindra|dm\s*mahindra|mahindra\b.*\bdee\s*emm', 'Dee Emm Mahindra'),
    (r'car\s*(&|and)\s*bike|first\s*choice', 'Car and Bike'),
]
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def access_token():
    try:
        body = urllib.parse.urlencode(dict(client_id=os.environ['GBP_CLIENT_ID'].strip(),
                                           client_secret=os.environ['GBP_CLIENT_SECRET'].strip(),
                                           refresh_token=os.environ['GBP_REFRESH_TOKEN'].strip(),
                                           grant_type='refresh_token')).encode()
    except KeyError as e:
        sys.exit(f'{e.args[0]} is not set in this session (add it in the environment settings, then start a new session)')
    try:
        with urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token', data=body), timeout=30) as r:
            return json.load(r)['access_token']
    except urllib.error.HTTPError as e:
        err = json.load(e)
        sys.exit(f"Token refresh failed: {err.get('error')}: {err.get('error_description', '')}")


def get(url, tok, **params):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {tok}'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            msg = json.load(e).get('error', {}).get('message', '')
        except ValueError:
            msg = e.reason
        raise RuntimeError(f'{e.code} {url.split("?")[0]}: {msg}') from None


def paged(url, tok, key, stop=None, **params):
    """All pages of `key`; `stop(page_items)` returning True ends paging early (e.g. past the --since date)."""
    out, token = [], None
    while True:
        p = dict(params, **({'pageToken': token} if token else {}))
        d = get(url, tok, **p)
        out += d.get(key, [])
        token = d.get('nextPageToken')
        if not token or (stop and stop(d.get(key, []))):
            return out


def locations(tok):
    accts = paged('https://mybusinessaccountmanagement.googleapis.com/v1/accounts', tok, 'accounts')
    locs = []
    for a in accts:
        try:
            ls = paged(f"https://mybusinessbusinessinformation.googleapis.com/v1/{a['name']}/locations", tok, 'locations',
                       readMask='name,title,storefrontAddress,metadata', pageSize=100)
        except RuntimeError as e:
            print(f"# {a['name']} ({a.get('accountName')}): {e}", file=sys.stderr)
            continue
        for l in ls:
            client = next((c for pat, c in CLIENTS if re.search(pat, l.get('title', ''), re.I)), '')
            addr = l.get('storefrontAddress') or {}
            locs.append(dict(account=a['name'], account_name=a.get('accountName'), location=l['name'], title=l.get('title'),
                             client=client, area=', '.join(filter(None, [*(addr.get('addressLines') or [])[-1:], addr.get('locality')])),
                             maps=(l.get('metadata') or {}).get('mapsUri', '')))
    return locs


def post_name(n):
    """'pooja sehgal' -> 'Pooja S.'; digits and honorifics dropped ('SACHIN YADAV8826' -> 'Sachin Y.', 'Shivam Veram ji' -> 'Shivam V.')."""
    words = [re.sub(r'\d+', '', w) for w in (n or '').split()]
    parts = [w for w in words if w.isalpha() and w.lower() not in ('ji', 'sir', 'mr', 'mrs', 'ms', 'dr')]
    if not parts:
        return 'A Google user'
    first = parts[0].capitalize()
    return first if len(parts) == 1 else f'{first} {parts[-1][0].upper()}.'


def original_text(comment):
    """Google adds '(Translated by Google) ... (Original) ...'; keep what the reviewer wrote."""
    if '(Original)' in (comment or ''):
        return comment.split('(Original)', 1)[1].strip()
    return re.sub(r'\s*\(Translated by Google\).*$', '', comment or '', flags=re.S).strip()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['check', 'reviews'])
    ap.add_argument('--min-stars', type=int, default=5)
    ap.add_argument('--min-words', type=int, default=25)
    ap.add_argument('--max-chars', type=int, default=500)
    ap.add_argument('--since')
    ap.add_argument('--out')
    a = ap.parse_args()
    tok = access_token()
    locs = locations(tok)
    if a.cmd == 'check':
        print(f'Token OK. {len(locs)} locations:')
        for l in locs:
            print(f"  [{l['client'] or 'NOT MAPPED'}] {l['title']} | {l['area']} | {l['account_name']} | {l['location']}")
        sys.exit(0)
    since = dt.datetime.fromisoformat(a.since).replace(tzinfo=IST) if a.since else None
    rows = []
    for l in locs:
        if not l['client']:
            continue
        loc_id = l['location'].split('/')[-1]
        try:
            # newest-updated first, and a review is created no later than it is updated, so once a page ends
            # before --since every later page is older too
            past = (lambda page: bool(page) and page[-1]['updateTime'] < since.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')) if since else None
            revs = paged(f"https://mybusiness.googleapis.com/v4/{l['account']}/locations/{loc_id}/reviews", tok, 'reviews',
                         stop=past, pageSize=50, orderBy='updateTime desc')
        except RuntimeError as e:
            print(f"# {l['title']}: {e}", file=sys.stderr)
            continue
        for r in revs:
            stars = STARS.get(r.get('starRating'), 0)
            when = dt.datetime.fromisoformat(r['createTime'].replace('Z', '+00:00')).astimezone(IST)
            if stars < a.min_stars or (since and when < since):
                continue
            text = original_text(r.get('comment'))
            if len(text.split()) < a.min_words or len(text) > a.max_chars:
                continue          # too thin to look genuine, or too long to quote in full on a card
            who = (r.get('reviewer') or {})
            display = 'A Google user' if who.get('isAnonymous') else who.get('displayName', '')
            photos = '\n'.join(re.sub(r'=[^/=]*$', '=s0', m['thumbnailUrl']) for m in r.get('reviewMediaItems', []) if m.get('thumbnailUrl'))
            rows.append([r.get('name') or r['reviewId'], l['client'], l['area'] or l['title'], stars, display, post_name(display), text,
                         when.strftime('%-d %b %Y'), l['maps'], 'New', '', '', text, photos, '', ''])   # M: Text for post (correct English, by a person); N photos; O, P by a person
    rows.sort(key=lambda x: dt.datetime.strptime(x[7], '%d %b %Y'), reverse=True)
    if a.out:
        json.dump(rows, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(rows, ensure_ascii=False, indent=1))
