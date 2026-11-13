"""Boost an Instagram reel as an ad (Instagram only, Advantage+ audience, profile visits), following config/boost.json.

Usage:
  python scripts/boost_reel.py plan   <CLIENT> <ig_media_id>        # show what would be created and which account pays
  python scripts/boost_reel.py create <CLIENT> <ig_media_id>        # create campaign/ad set/ad, all PAUSED (no spend)
  python scripts/boost_reel.py activate <campaign_id> <adset_id> <ad_id>   # only after the user says yes
  python scripts/boost_reel.py delete <campaign_id>                 # remove a test boost
  python scripts/boost_reel.py results <campaign_id> ...            # read-only: spend, reach, profile visits so far

Budget: a lifetime budget of daily_budget_inr x days over exactly that many days, so the total can't exceed the rule.
Uses META_SYSTEM_USER_TOKEN. Never prints the token.
"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH = 'https://graph.facebook.com/v24.0'
CFG = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'config', 'boost.json')))
TOK = os.environ['META_SYSTEM_USER_TOKEN'].strip()


def call(method, path, **params):
    data = None
    url = f'{GRAPH}/{path}'
    enc = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items()}
    if method == 'GET':
        url += '?' + urllib.parse.urlencode(enc)
    else:
        data = urllib.parse.urlencode(enc).encode()
    req = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'OAuth {TOK}'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e).get('error', {})
        raise RuntimeError(f"{method} {path}: {err.get('code')}/{err.get('error_subcode')}: "
                           f"{err.get('error_user_msg') or err.get('message')}") from None


def room(act):
    """smallest of available prepaid balance and spend-cap headroom, in rupees"""
    a = call('GET', f'act_{act}', fields='amount_spent,spend_cap,funding_source_details')
    disp = (a.get('funding_source_details') or {}).get('display_string', '')
    bal = None
    if 'Available Balance' in disp:
        import re
        bal = float(re.search(r'₹\s*([\d,]+(?:\.\d+)?)', disp).group(1).replace(',', ''))
    cap = int(a['spend_cap']) / 100 - int(a['amount_spent']) / 100 if a.get('spend_cap') not in (None, '0') else None
    vals = [v for v in (bal, cap) if v is not None]
    return (min(vals) if vals else float('inf')), bal, cap


def pick_account(client):
    c = CFG['clients'][client]; need = CFG['per_reel_inr']
    r, bal, cap = room(c['ad_account'])
    if r >= need:
        return c['ad_account'], r, None
    if c.get('fallback'):
        fr, _, _ = room(c['fallback'])
        if fr >= need:
            return c['fallback'], fr, f"{c['name']}'s own account has only Rs {r:,.2f} available"
    raise RuntimeError(f"No account can cover Rs {need} for {c['name']}: own account has Rs {r:,.2f} available"
                       + (" and the fallback is short too" if c.get('fallback') else " (no fallback allowed)"))


def ig_and_page(client, media_id, permalink=None):
    c = CFG['clients'][client]
    try:
        m = call('GET', media_id, fields='owner{id,username},permalink,caption')
        return m['owner']['id'], m['owner'].get('username'), c.get('page_id'), m.get('permalink'), (m.get('caption') or '')[:40]
    except RuntimeError:   # IG account not shared with the system user (e.g. DEM, MRH): use the saved details
        return c['ig_user'], c['ig_username'], c.get('page_id'), permalink or f'https://www.instagram.com/{c["ig_username"]}/{media_id}', ''


def plan(client, media_id, permalink=None):
    act, r, why = pick_account(client)
    ig, user, page, link, cap = ig_and_page(client, media_id, permalink)
    start = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=10)
    end = start + dt.timedelta(days=CFG['days'])
    loc = CFG['clients'][client]['locations']
    return dict(client=client, ad_account=act, fallback_reason=why, room_inr=round(r, 2), ig_user=ig, ig_username=user,
                page_id=page, media=media_id, permalink=link, caption_start=cap,
                budget_inr=CFG['per_reel_inr'], start=start.isoformat(timespec='seconds'), end=end.isoformat(timespec='seconds'),
                locations=loc)


def create(p):
    name = f"Boost {p['client']} {p['permalink'].rstrip('/').split('/')[-1]}"
    camp = call('POST', f"act_{p['ad_account']}/campaigns", name=name, objective='OUTCOME_TRAFFIC', status='PAUSED',
                special_ad_categories=[], buying_type='AUCTION', is_adset_budget_sharing_enabled='false')['id']
    try:
        return _rest(p, name, camp)
    except RuntimeError:
        call('DELETE', camp)          # remove only the campaign this run just created
        raise


def _rest(p, name, camp):
    targeting = {
        'geo_locations': {'custom_locations': [dict(latitude=l['lat'], longitude=l['lng'], radius=l['km'], distance_unit='kilometer')
                                               for l in p['locations']]},
        'publisher_platforms': ['instagram'],
        'instagram_positions': ['stream', 'story', 'reels', 'explore_home', 'profile_feed'],
        'targeting_automation': {'advantage_audience': 1},
    }
    adset = call('POST', f"act_{p['ad_account']}/adsets", name=name, campaign_id=camp, status='PAUSED',
                 lifetime_budget=p['budget_inr'] * 100, start_time=p['start'], end_time=p['end'],
                 billing_event='IMPRESSIONS', optimization_goal='VISIT_INSTAGRAM_PROFILE', destination_type='INSTAGRAM_PROFILE',
                 bid_strategy='LOWEST_COST_WITHOUT_CAP', targeting=targeting)['id']
    spec = dict(name=name, instagram_user_id=p['ig_user'], source_instagram_media_id=p['media'],
                call_to_action={'type': 'VIEW_INSTAGRAM_PROFILE', 'value': {'link': f"https://www.instagram.com/{p['ig_username']}/"}})
    if p.get('page_id'):
        spec['object_id'] = p['page_id']
    creative = call('POST', f"act_{p['ad_account']}/adcreatives", **spec)['id']
    ad = call('POST', f"act_{p['ad_account']}/ads", name=name, adset_id=adset, creative={'creative_id': creative}, status='PAUSED')['id']
    return dict(campaign_id=camp, adset_id=adset, creative_id=creative, ad_id=ad, status='PAUSED')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd in ('plan', 'create'):
        p = plan(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        print(json.dumps(p, indent=1, ensure_ascii=False))
        if cmd == 'create':
            try:
                print(json.dumps(create(p)))
            except RuntimeError as e:
                print(json.dumps({'error': str(e)}))
    elif cmd == 'activate':
        for i in sys.argv[2:]:
            call('POST', i, status='ACTIVE')
        print('activated', sys.argv[2:])
    elif cmd == 'delete':
        call('DELETE', sys.argv[2]); print('deleted', sys.argv[2])
    elif cmd == 'results':   # read-only: lifetime results of each campaign id given
        for cid in sys.argv[2:]:
            try:
                c = call('GET', cid, fields='name,effective_status,start_time,stop_time')
                ins = call('GET', f'{cid}/insights', date_preset='maximum',
                           fields='spend,reach,impressions,frequency,cpm,actions,instagram_profile_visits,results,cost_per_result').get('data') or [{}]
                i = ins[0]
                acts = {a['action_type']: a['value'] for a in i.get('actions', [])}
                print(json.dumps(dict(campaign=cid, name=c.get('name'), status=c.get('effective_status'),
                                      start=c.get('start_time'), stop=c.get('stop_time'), spend=i.get('spend'),
                                      reach=i.get('reach'), impressions=i.get('impressions'),
                                      frequency=i.get('frequency'), cpm=i.get('cpm'), profile_visits=i.get('instagram_profile_visits'),
                                      cost_per_visit=((i.get('cost_per_result') or [{}])[0].get('values') or [{}])[0].get('value'),
                                      link_clicks=acts.get('link_click'), video_views=acts.get('video_view'),
                                      likes=acts.get('onsite_conversion.post_net_like')), ensure_ascii=False))
            except RuntimeError as e:
                print(json.dumps(dict(campaign=cid, error=str(e))))
