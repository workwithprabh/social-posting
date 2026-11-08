"""Read-only check of the clients' ad accounts with the system user token.

Usage: python scripts/check_ads.py [act_id ...]

For each ad account: name, status, currency, owning business, payment method / available balance, amount spent,
spend cap, and the Instagram accounts it can run ads for. Also lists the token's granted permissions.
GET requests only; never prints a token.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH = 'https://graph.facebook.com/v24.0'
ACCOUNTS = {
    '180067875407208': 'MR Hyundai / Mahindra Arav (same ID given twice)',
    '768739352110216': 'Dee Emm Hyundai + Car & Bike (fallback for Arav / Dee Emm Mahindra)',
    '1843796949802121': 'Capital Hyundai',
    '213796001764883': 'Dee Emm Mahindra',
}


def get(path, token, **params):
    req = urllib.request.Request(f'{GRAPH}/{path}?' + urllib.parse.urlencode(params),
                                 headers={'Authorization': f'OAuth {token}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e).get('error', {})
        raise RuntimeError(f"{err.get('code', '')}/{err.get('error_subcode', '')}: {err.get('message', e.reason)}") from None


def money(v, cur):
    return f'{int(v) / 100:,.2f} {cur}' if v not in (None, '') else '-'


tok = os.environ.get('META_SYSTEM_USER_TOKEN', '').strip()
if not tok:
    sys.exit('META_SYSTEM_USER_TOKEN is not set in this session')
try:
    perms = [p['permission'] for p in get('me/permissions', tok).get('data', []) if p.get('status') == 'granted']
    print('Token permissions:', ', '.join(perms) or '(none listed)')
    print('  ads_management:', 'yes' if 'ads_management' in perms else 'NO', '| ads_read:', 'yes' if 'ads_read' in perms else 'NO')
except RuntimeError as e:
    print('Token permissions: could not read:', e)
print()
for act in (sys.argv[1:] or ACCOUNTS):
    label = ACCOUNTS.get(act, '')
    print(f'act_{act}  ({label})')
    try:
        a = get(f'act_{act}', tok, fields='name,account_status,disable_reason,currency,business{name},amount_spent,spend_cap,balance,'
                                          'is_prepay_account,funding_source_details,user_tasks')
    except RuntimeError as e:
        print('  NOT reachable with the system user token:', e, '\n')
        continue
    cur = a.get('currency')
    status = {1: 'ACTIVE', 2: 'DISABLED', 3: 'UNSETTLED', 7: 'PENDING_RISK_REVIEW', 9: 'IN_GRACE_PERIOD', 101: 'CLOSED'}.get(a.get('account_status'), a.get('account_status'))
    print(f"  name: {a.get('name')} | business: {(a.get('business') or {}).get('name', '-')} | status: {status} | currency: {cur}")
    fs = a.get('funding_source_details') or {}
    print(f"  payment: {fs.get('display_string', '-')} | prepaid: {a.get('is_prepay_account')} | balance field: {money(a.get('balance'), cur)}")
    print(f"  spent to date: {money(a.get('amount_spent'), cur)} | spend cap: {money(a.get('spend_cap'), cur) if a.get('spend_cap') not in (None, '0') else 'none'}")
    print(f"  system user tasks on this account: {', '.join(a.get('user_tasks') or []) or '-'}")
    for edge in ('instagram_accounts', 'connected_instagram_accounts'):
        try:
            ig = get(f'act_{act}/{edge}', tok, fields='id,username').get('data', [])
            print(f"  {edge}: {', '.join('@' + str(i.get('username')) for i in ig) or 'none'}")
        except RuntimeError as e:
            print(f'  {edge}: could not read ({e})')
    print()
