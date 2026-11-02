"""Publish one edited video as a Reel to Instagram and/or a Facebook Page.

Usage:
  python scripts/publish_reel.py --video out.mp4 --caption-file caption.txt --token-env META_PAGE_TOKEN_MRH \
      --ig-user 17841470355540620 --page-id 423738584167015 \
      --cover-url https://raw.githubusercontent.com/.../thumbnails/MRH-2609-02.jpg --cover-file thumbnails/MRH-2609-02.jpg \
      [--platforms ig,fb]

Instagram: resumable Reels upload with the cover from --cover-url (Instagram only accepts a public link).
Facebook: Page Reels upload, then --cover-file is set as the preferred thumbnail.
Prints one JSON line with the post links. Never prints the token.
"""
import argparse
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

V = 'v24.0'
GRAPH = f'https://graph.facebook.com/{V}'


def call(method, url, token, params=None, data=None, headers=None):
    if params:
        url += ('&' if '?' in url else '?') + urllib.parse.urlencode(params)
    h = {'Authorization': f'OAuth {token}'}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='replace')
        try:
            err = json.loads(body).get('error', {})
            msg = f"{err.get('type', 'Error')} {err.get('code', '')}/{err.get('error_subcode', '')}: {err.get('message', body)}"
        except ValueError:
            msg = body[:500]
        raise RuntimeError(f'{method} {url.split("?")[0]} failed: {msg}') from None


def post_form(url, token, fields):
    return call('POST', url, token, data=urllib.parse.urlencode(fields).encode(),
                headers={'Content-Type': 'application/x-www-form-urlencoded'})


def upload_binary(url, token, path):
    """Upload the whole file. The upload host can report an error even when the upload landed (seen with
    Instagram), so return the error instead of raising: the processing status checked next is what counts."""
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        try:
            return call('POST', url, token, data=f.read(),
                        headers={'offset': '0', 'file_size': str(size), 'Content-Type': 'application/octet-stream'})
        except RuntimeError as e:
            return {'upload_warning': str(e)}


def publish_instagram(a, token, caption):
    c = post_form(f'{GRAPH}/{a.ig_user}/media', token, {
        'media_type': 'REELS', 'upload_type': 'resumable', 'caption': caption,
        'cover_url': a.cover_url, 'share_to_feed': 'true'})
    cid = c['id']
    upload_binary(f'https://rupload.facebook.com/ig-api-upload/{V}/{cid}', token, a.video)
    for _ in range(90):                                   # up to ~15 minutes of processing
        s = call('GET', f'{GRAPH}/{cid}', token, {'fields': 'status_code,status'})
        if s.get('status_code') == 'FINISHED':
            break
        if s.get('status_code') in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'Instagram processing failed: {s.get("status")}')
        time.sleep(10)
    else:
        raise RuntimeError('Instagram processing timed out')
    media = post_form(f'{GRAPH}/{a.ig_user}/media_publish', token, {'creation_id': cid})
    info = call('GET', f'{GRAPH}/{media["id"]}', token, {'fields': 'permalink'})
    return {'ig_media_id': media['id'], 'ig_link': info.get('permalink')}


def multipart(fields, file_field, path):
    b = uuid.uuid4().hex
    out = b''
    for k, v in fields.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        out += (f'--{b}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{os.path.basename(path)}"\r\n'
                f'Content-Type: {ctype}\r\n\r\n').encode() + f.read() + b'\r\n'
    out += f'--{b}--\r\n'.encode()
    return out, f'multipart/form-data; boundary={b}'


def publish_facebook(a, token, caption):
    start = post_form(f'{GRAPH}/{a.page_id}/video_reels', token, {'upload_phase': 'start'})
    vid = start['video_id']
    upload_binary(f'https://rupload.facebook.com/video-upload/{V}/{vid}', token, a.video)
    post_form(f'{GRAPH}/{a.page_id}/video_reels', token, {
        'upload_phase': 'finish', 'video_id': vid, 'video_state': 'PUBLISHED', 'description': caption})
    out = {'fb_video_id': vid}
    if a.cover_file:
        try:
            body, ctype = multipart({'is_preferred': 'true'}, 'source', a.cover_file)
            call('POST', f'{GRAPH}/{vid}/thumbnails', token, data=body, headers={'Content-Type': ctype})
            out['fb_cover'] = 'set'
        except RuntimeError as e:
            out['fb_cover'] = f'not set: {e}'
    for _ in range(60):
        s = call('GET', f'{GRAPH}/{vid}', token, {'fields': 'status,permalink_url'})
        st = s.get('status', {})
        if st.get('video_status') == 'ready' or st.get('publishing_phase', {}).get('status') == 'complete':
            break
        if st.get('video_status') == 'error':
            raise RuntimeError(f'Facebook processing failed: {st}')
        time.sleep(10)
    link = s.get('permalink_url')
    out['fb_link'] = ('https://www.facebook.com' + link) if link and link.startswith('/') else link
    out['fb_status'] = s.get('status', {}).get('video_status')
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--video', required=True)
    p.add_argument('--caption-file', required=True)
    p.add_argument('--token-env', required=True)
    p.add_argument('--ig-user')
    p.add_argument('--page-id')
    p.add_argument('--cover-url')
    p.add_argument('--cover-file')
    p.add_argument('--platforms', default='ig,fb')
    p.add_argument('--system-user', action='store_true',
                   help='token is the system user token: fetch the Page token for Facebook (kept in memory only)')
    a = p.parse_args()
    token = os.environ[a.token_env].strip()
    caption = open(a.caption_file, encoding='utf-8').read().strip()
    result = {}
    for plat in a.platforms.split(','):
        try:
            if plat == 'ig':
                result.update(publish_instagram(a, token, caption))
            else:
                fb_token = call('GET', f'{GRAPH}/{a.page_id}', token, {'fields': 'access_token'})['access_token'] \
                    if a.system_user else token
                result.update(publish_facebook(a, fb_token, caption))
        except RuntimeError as e:
            result[f'{plat}_error'] = str(e)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
