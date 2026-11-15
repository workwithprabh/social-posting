"""Share one image or video to the Instagram Story and the Facebook Page Story (user, 15 Nov 2026: every post we
publish also goes to both Stories).

Usage:
  python scripts/publish_story.py --image post.jpg   --token-env META_SYSTEM_USER_TOKEN --system-user \
      --page-id 1796813873933984 --ig-user 17841404103430378 [--platforms ig,fb]
  python scripts/publish_story.py --video reel.mp4   ...same...

Stories are 9:16. A 4:5 static is placed on a 1080x1920 canvas over a blurred, darkened copy of itself. Videos are
cut to the first 60 s (the Stories limit through the API) and sent as 720p, which Instagram accepts from this session.
Instagram needs a public image link, so images go up to the Page as an unpublished photo first (deleted afterwards),
as in publish_static.py. Stories can't carry music or stickers through the API. Prints one JSON line; never the token.
"""
import argparse
import json
import os
import subprocess
import tempfile
import time

from PIL import Image, ImageFilter, ImageEnhance

from publish_reel import GRAPH, V, call, multipart, post_form, upload_binary


def page_token(a, token):
    return call('GET', f'{GRAPH}/{a.page_id}', token, {'fields': 'access_token'})['access_token'] if a.system_user else token


def story_image(src, out):
    im = Image.open(src).convert('RGB')
    bg = im.resize((max(1080, int(1920 * im.width / im.height)), 1920), Image.LANCZOS)
    left = (bg.width - 1080) // 2
    bg = bg.crop((left, 0, left + 1080, 1920)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    fg = im.resize((1080, round(1080 * im.height / im.width)), Image.LANCZOS)
    bg.paste(fg, (0, (1920 - fg.height) // 2))
    bg.save(out, quality=95, subsampling=0)
    return out


def story_video(src, out):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-t', '59.5',
                    '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,fps=30',
                    '-c:v', 'libx264', '-profile:v', 'main', '-level', '4.0', '-preset', 'medium', '-crf', '28',
                    '-maxrate', '1500k', '-bufsize', '3000k', '-g', '60', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '96k', '-ac', '2', '-ar', '44100', '-movflags', '+faststart', out], check=True)
    return out


def wait_ig(cid, token):
    for _ in range(60):
        s = call('GET', f'{GRAPH}/{cid}', token, {'fields': 'status_code,status'})
        if s.get('status_code') == 'FINISHED':
            return
        if s.get('status_code') in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'Instagram story processing failed: {s.get("status")}')
        time.sleep(5)
    raise RuntimeError('Instagram story container never finished')


def ig_story(a, token, ptoken, path, is_video):
    if is_video:
        c = post_form(f'{GRAPH}/{a.ig_user}/media', token, {'media_type': 'STORIES', 'upload_type': 'resumable'})
        upload_binary(f'https://rupload.facebook.com/ig-api-upload/{V}/{c["id"]}', token, path)
        wait_ig(c['id'], token)
    else:
        body, ctype = multipart({'published': 'false'}, 'source', path)
        helper = call('POST', f'{GRAPH}/{a.page_id}/photos', ptoken, data=body, headers={'Content-Type': ctype})['id']
        try:
            imgs = call('GET', f'{GRAPH}/{helper}', ptoken, {'fields': 'images'})['images']
            url = max(imgs, key=lambda i: i['width'])['source']
            c = post_form(f'{GRAPH}/{a.ig_user}/media', token, {'media_type': 'STORIES', 'image_url': url})
            wait_ig(c['id'], token)
        finally:
            try:
                call('DELETE', f'{GRAPH}/{helper}', ptoken)
            except RuntimeError:
                pass
    m = post_form(f'{GRAPH}/{a.ig_user}/media_publish', token, {'creation_id': c['id']})
    return {'ig_story_id': m['id']}


def fb_story(a, ptoken, path, is_video):
    if is_video:
        st = post_form(f'{GRAPH}/{a.page_id}/video_stories', ptoken, {'upload_phase': 'start'})
        upload_binary(f'https://rupload.facebook.com/video-upload/{V}/{st["video_id"]}', ptoken, path)
        r = post_form(f'{GRAPH}/{a.page_id}/video_stories', ptoken, {'upload_phase': 'finish', 'video_id': st['video_id']})
        return {'fb_story_id': r.get('post_id') or st['video_id']}
    body, ctype = multipart({'published': 'false'}, 'source', path)
    photo = call('POST', f'{GRAPH}/{a.page_id}/photos', ptoken, data=body, headers={'Content-Type': ctype})['id']
    r = post_form(f'{GRAPH}/{a.page_id}/photo_stories', ptoken, {'photo_id': photo})
    return {'fb_story_id': r.get('post_id') or photo}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--image'); g.add_argument('--video')
    p.add_argument('--token-env', required=True)
    p.add_argument('--page-id', required=True)
    p.add_argument('--ig-user')
    p.add_argument('--platforms', default='ig,fb')
    p.add_argument('--system-user', action='store_true')
    a = p.parse_args()
    token = os.environ[a.token_env].strip()
    tmp = tempfile.mkdtemp()
    is_video = bool(a.video)
    path = story_video(a.video, os.path.join(tmp, 'story.mp4')) if is_video else story_image(a.image, os.path.join(tmp, 'story.jpg'))
    out = {}
    try:
        ptoken = page_token(a, token)
    except RuntimeError as e:
        print(json.dumps({'error': f'no Page token: {e}'})); return
    for plat in a.platforms.split(','):
        try:
            out.update(ig_story(a, token, ptoken, path, is_video) if plat == 'ig' else fb_story(a, ptoken, path, is_video))
        except RuntimeError as e:
            out[f'{plat}_story_error'] = str(e)
    print(json.dumps(out))


if __name__ == '__main__':
    main()
