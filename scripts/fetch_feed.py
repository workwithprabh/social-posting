"""Read-only. usage: python scripts/fetch_feed.py <out_dir>. Last 30 posts of each client IG account -> images + metadata in scratchpad/feed/<user>/"""
import os, json, sys, urllib.request, urllib.parse, urllib.error
OUT = sys.argv[1] if len(sys.argv) > 1 else "feed"
tok = os.environ['META_SYSTEM_USER_TOKEN'].strip()
def get(path, **p):
    r = urllib.request.Request('https://graph.facebook.com/v24.0/' + path + '?' + urllib.parse.urlencode(p), headers={'Authorization': f'OAuth {tok}'})
    return json.load(urllib.request.urlopen(r, timeout=60))
accts = {'capitalhyundai': '17841404103430378', 'hyundaidm': '17841430529180239', 'mahindraarav': '17841457116100505',
         'hyundaimr_sg': '17841470355540620', 'mahindradm': '17841415265612306', 'dm_carandbike': '17841475932990498'}
summary = {}
for user, ig in accts.items():
    d = os.path.join(OUT, user); os.makedirs(d, exist_ok=True)
    try:
        posts = get(f'{ig}/media', fields='id,media_type,media_product_type,caption,timestamp,permalink,media_url,thumbnail_url,children{media_type,media_url,thumbnail_url}', limit=30).get('data', [])
    except urllib.error.HTTPError as e:
        print(user, 'ERROR', json.load(e).get('error', {}).get('message')); continue
    for i, p in enumerate(posts):
        imgs = []
        if p['media_type'] == 'CAROUSEL_ALBUM':
            imgs = [c.get('media_url') if c['media_type'] == 'IMAGE' else c.get('thumbnail_url') for c in (p.get('children') or {}).get('data', [])]
        else:
            imgs = [p.get('media_url') if p['media_type'] == 'IMAGE' else p.get('thumbnail_url')]
        p['files'] = []
        for j, u in enumerate([x for x in imgs if x]):
            fn = os.path.join(d, f'{i:02d}_{j}.jpg')
            try:
                urllib.request.urlretrieve(u, fn); p['files'].append(fn)
            except Exception as ex:
                pass
    json.dump(posts, open(os.path.join(d, 'posts.json'), 'w'), ensure_ascii=False, indent=1)
    kinds = {}
    for p in posts:
        k = 'REEL' if p.get('media_product_type') == 'REELS' else p['media_type']
        kinds[k] = kinds.get(k, 0) + 1
    summary[user] = dict(n=len(posts), kinds=kinds, oldest=posts[-1]['timestamp'][:10] if posts else None)
    print(user, summary[user])
