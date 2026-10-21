"""Read-only check of which Facebook Pages and Instagram accounts each Meta token can reach.

Usage: python scripts/check_access.py

Reads META_SYSTEM_USER_TOKEN, META_PAGE_TOKEN_DEM and META_PAGE_TOKEN_MRH from the environment.
Makes GET requests only and never prints a token.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com"
IG_FIELDS = "instagram_business_account{id,username}"


def get(path, token, **params):
    url = f"{GRAPH}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"OAuth {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e).get("error", {})
        raise RuntimeError(f"{err.get('type', 'Error')} {err.get('code', '')}: {err.get('message', e.reason)}")


def show_page(page):
    ig = page.get("instagram_business_account")
    ig_text = f"Instagram @{ig.get('username')} ({ig['id']})" if ig else "NO linked Instagram account"
    print(f"  - {page['name']} (Page {page['id']}): {ig_text}")


def check_system_user(token):
    me = get("me", token, fields="id,name")
    print(f"System user: {me.get('name')} ({me['id']})")
    pages = get("me/accounts", token, fields=f"id,name,{IG_FIELDS}", limit=100).get("data", [])
    if not pages:
        print("  No Pages assigned. Check Assign assets for the system user.")
    for page in pages:
        show_page(page)


def check_page_token(label, token):
    page = get("me", token, fields=f"id,name,{IG_FIELDS}")
    print(f"{label} Page token:")
    show_page(page)


checks = [
    ("META_SYSTEM_USER_TOKEN", check_system_user),
    ("META_PAGE_TOKEN_DEM", lambda t: check_page_token("Dee Emm Mahindra", t)),
    ("META_PAGE_TOKEN_MRH", lambda t: check_page_token("M R Hyundai", t)),
]
for var, check in checks:
    token = os.environ.get(var, "").strip()
    if not token:
        print(f"{var}: not set in this session")
        continue
    try:
        check(token)
    except RuntimeError as e:
        print(f"{var}: failed. {e}")
    print()
