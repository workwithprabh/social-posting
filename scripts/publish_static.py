"""Publish one static image post to a Facebook Page and/or its Instagram account.
Usage:
  python scripts/publish_static.py --image CH-REV-2611-04.jpg --caption-file caption.txt \
      --token-env META_SYSTEM_USER_TOKEN --system-user --page-id 1796813873933984 --ig-user 17841404103430378 \
      [--platforms ig,fb]
Facebook gets the 2160x2700 master as a Page photo. Instagram only accepts an image from a public link, so a
1080x1350 copy (Instagram's own 4:5 size) is uploaded to the Page as an unpublished photo, its CDN link is given to
Instagram, and the helper photo is deleted afterwards. Prints one JSON line with the post links; never the token.
"""
import argparse
import json
import os
import tempfile
import time

from PIL import Image

from publish_reel import GRAPH, call, multipart, post_form


def page_token(a, token):
    return call('GET', f'{GRAPH}/{a.page_id}', token, {'fields': 'access_token'})['access_token'] if a.system_user else token


def upload_photo(page_id, token, path, fields):
    body, ctype = multipart(fields, 'source', path)
    return call('POST', f'{GRAPH}/{page_id}/photos', token, data=body, headers={'Content-Type': ctype})


def publish_facebook(a, ptoken, caption):
    r = upload_photo(a.page_id, ptoken, a.image, {'message': caption, 'published': 'true'})
    pid = r.get('post_id') or r['id']
    info = call('GET', f'{GRAPH}/{pid}', ptoken, {'fields': 'permalink_url'})
    return {'fb_post_id': pid, 'fb_link': info.get('permalink_url')}


def publish_instagram(a, token, ptoken, caption):
    ig_copy = os.path.join(tempfile.mkdtemp(), 'ig.jpg')
    Image.open(a.image).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(ig_copy, quality=95, subsampling=0)
    helper = upload_photo(a.page_id, ptoken, ig_copy, {'published': 'false'})['id']
    try:
        imgs = call('GET', f'{GRAPH}/{helper}', ptoken, {'fields': 'images'})['images']
        url = max(imgs, key=lambda i: i['width'])['source']
        c = post_form(f'{GRAPH}/{a.ig_user}/media', token, {'image_url': url, 'caption': caption})
        for _ in range(30):
            s = call('GET', f'{GRAPH}/{c["id"]}', token, {'fields': 'status_code,status'})
            if s.get('status_code') == 'FINISHED':
                break
            if s.get('status_code') in ('ERROR', 'EXPIRED'):
                raise RuntimeError(f'Instagram processing failed: {s.get("status")}')
            time.sleep(4)
        media = post_form(f'{GRAPH}/{a.ig_user}/media_publish', token, {'creation_id': c['id']})
        info = call('GET', f'{GRAPH}/{media["id"]}', token, {'fields': 'permalink'})
        return {'ig_media_id': media['id'], 'ig_link': info.get('permalink')}
    finally:
        try:
            call('DELETE', f'{GRAPH}/{helper}', ptoken)
        except RuntimeError:
            pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--image', required=True)
    p.add_argument('--caption-file', required=True)
    p.add_argument('--token-env', required=True)
    p.add_argument('--page-id', required=True)
    p.add_argument('--ig-user')
    p.add_argument('--platforms', default='ig,fb')
    p.add_argument('--system-user', action='store_true', help='token is the system user token; fetch the Page token')
    a = p.parse_args()
    token = os.environ[a.token_env].strip()
    caption = open(a.caption_file, encoding='utf-8').read().strip()
    result = {}
    try:
        ptoken = page_token(a, token)
    except RuntimeError as e:
        print(json.dumps({'error': f'no Page token: {e}'}))
        return
    for plat in a.platforms.split(','):
        try:
            result.update(publish_instagram(a, token, ptoken, caption) if plat == 'ig' else publish_facebook(a, ptoken, caption))
        except RuntimeError as e:
            result[f'{plat}_error'] = str(e)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
