"""Read-only: fetch the latest Instagram posts (caption, date, link) for every client account.

Usage: python scripts/recent_captions.py [count=10] > captions.json

Finds the accounts the same way as check_access.py (system user Pages + the DEM and MRH Page tokens),
then reads /{ig-user}/media. GET requests only; never prints a token.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH = 'https://graph.facebook.com/v24.0'
IG_FIELDS = 'instagram_business_account{id,username}'


def get(path, token, **params):
    req = urllib.request.Request(f'{GRAPH}/{path}?' + urllib.parse.urlencode(params),
                                 headers={'Authorization': f'OAuth {token}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e).get('error', {})
        raise RuntimeError(f"{err.get('type', 'Error')} {err.get('code', '')}: {err.get('message', e.reason)}") from None


N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
accounts = []  # (page name, ig id, ig username, token)
sys_tok = os.environ.get('META_SYSTEM_USER_TOKEN', '').strip()
if sys_tok:
    for p in get('me/accounts', sys_tok, fields=f'id,name,{IG_FIELDS}', limit=100).get('data', []):
        ig = p.get('instagram_business_account')
        if ig:
            accounts.append((p['name'], ig['id'], ig.get('username'), sys_tok))
for var in ('META_PAGE_TOKEN_DEM', 'META_PAGE_TOKEN_MRH'):
    tok = os.environ.get(var, '').strip()
    if tok:
        p = get('me', tok, fields=f'id,name,{IG_FIELDS}')
        ig = p.get('instagram_business_account')
        if ig:
            accounts.append((p['name'], ig['id'], ig.get('username'), tok))

out = []
for name, ig_id, user, tok in accounts:
    try:
        media = get(f'{ig_id}/media', tok, fields='caption,timestamp,permalink,media_product_type', limit=N).get('data', [])
    except RuntimeError as e:
        media, err = [], str(e)
    else:
        err = None
    out.append({'page': name, 'instagram': user, 'error': err, 'posts': media})
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
