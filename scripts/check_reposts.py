"""Read-only. Before posting, check that a reel isn't already on the client's Instagram (user, 17 Nov 2026: a reel
marked Approved in the sheet had already been posted by the team on 23 Oct, and was posted again).

Usage: python scripts/check_reposts.py <CLIENT> <video.mp4> [<video.mp4> ...]
  CLIENT is CH, DEH, MRH, AM, DEM or CB (ids and tokens as in config/boost.json and CLAUDE.md).

Compares frames of each local video with every video reel in the account's last 45 posts. A median frame difference
below 15 means the same video (a repost: don't post it): on 17 Nov 2026 the same video scored 5-8 against its
Instagram copy, different reels 20 and up. Reels whose video Instagram won't hand out (licensed music) are listed so their covers can be looked at
by eye. Never prints a token.
"""
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

import numpy as np

GRAPH = 'https://graph.facebook.com/v24.0/'
CFG = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'config', 'boost.json')))['clients']
TOKENS = {'MRH': 'META_PAGE_TOKEN_MRH', 'DEM': 'META_PAGE_TOKEN_DEM'}


def get(path, tok, **p):
    req = urllib.request.Request(GRAPH + path + '?' + urllib.parse.urlencode(p), headers={'Authorization': f'OAuth {tok}'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def frames(path):
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', path, '-vf', 'fps=1,scale=16:28,format=gray',
                        '-f', 'rawvideo', '-'], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.uint8).astype(float).reshape(-1, 28, 16)


def score(a, b):
    d = np.array([[np.abs(x - y).mean() for y in b] for x in a]).min(axis=1)
    return round(float(np.median(d)), 1)


def main():
    client, videos = sys.argv[1], sys.argv[2:]
    tok = os.environ[TOKENS.get(client, 'META_SYSTEM_USER_TOKEN')].strip()
    ig = CFG[client]['ig_user']
    media = get(f'{ig}/media', tok, fields='id,timestamp,permalink,media_type,media_url,caption', limit=45).get('data', [])
    tmp = tempfile.mkdtemp()
    posted, no_video = [], []
    for m in media:
        if m.get('media_type') != 'VIDEO':
            continue
        if not m.get('media_url'):
            no_video.append(m)
            continue
        fn = os.path.join(tmp, m['id'] + '.mp4')
        try:
            urllib.request.urlretrieve(m['media_url'], fn)
        except Exception:
            no_video.append(m)
            continue
        posted.append((m, frames(fn)))
    for v in videos:
        mine = frames(v)
        best = sorted(((score(mine, f), m) for m, f in posted), key=lambda x: x[0])[:1]
        if best and best[0][0] < 15:
            m = best[0][1]
            print(f'{v}: ALREADY POSTED {m["timestamp"][:10]} {m["permalink"]} (difference {best[0][0]})')
        else:
            print(f'{v}: not found in the last {len(posted)} reels (closest difference {best[0][0] if best else "-"})')
    for m in no_video:
        print(f'  check by eye (no video from Instagram): {m["timestamp"][:10]} {m["permalink"]} '
              f'{(m.get("caption") or "")[:60]!r}')


if __name__ == '__main__':
    main()
