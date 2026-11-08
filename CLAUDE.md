# Social posting: working notes

This repo backs the posting of edited client reels to Instagram and Facebook. Read README.md for the flow.

## Where things are

- **Tracker sheet:** "Social Posting Tracker", Google Sheet id `1bcx0yZ-5C7F6e_WLg9Kbw8FRQQ4jUaPQ_SRGnJts_NY`
  in the workwithprabh@gmail.com Drive. Tab `Videos`, columns A-M: Video ID, Client, Added to Drive (the video
  file's Drive upload date, India time), Month, Video file (HYPERLINK to Drive), Status (Pending / Approved /
  Posted / Skip), Platforms (IG + FB / IG only / FB only), Caption, Thumbnail link, Post date, Instagram post
  link, Facebook post link, Notes. Tab `Dashboard`: formula-only counts by client and month (never write to it).
  Tab `Clients`: code, client, Drive folder.
  Read it with the Drive connector: `download_file_content` with `exportMimeType: text/csv`.
  Writing to it needs the Google Sheets connector; without it, the user updates the sheet by hand.
- **Edited videos:** owned by becarrotsocial@gmail.com, one folder per client, one subfolder per month,
  shared "Anyone with the link can view". Folder ids are in `scripts/list_videos.py`.
- **Thumbnails:** Drive folder `1u6J5NUVc51ZufYb6n5AmO7JXd1QL2Y_D`, one subfolder per client, files named by
  Video ID. `scripts/fetch_thumbnail.py <ID>` copies one into `thumbnails/`; its raw GitHub URL on `main` is the
  Instagram `cover_url`.

## Rules the user set

- Post only when the user says to upload specific Video IDs. The Post date column is not a schedule.
- Claude drafts captions and thumbnails; the team approves them. Covers follow `cover/PLAYBOOK.md`
  (Mahindra style; Hyundai and Car & Bike use the same rules in their own colours, refs in `cover/refs/`).
  Captions follow `captions/STYLE.md` and use only facts said in the reel.
- Drafts go to the Drive folder "Claude drafts" (`1KDnTFCTb2SoIW3168M26spmO3htJwX8o`, workwithprabh Drive) as
  `<Video ID>.jpg`; write the caption and the draft's link into the sheet and set Notes to
  "Draft by Claude, needs review". Never put drafts in the team's Thumbnail folder: a file there named by Video ID
  is treated as the approved cover.
- Before publishing, show the user the batch (ID, client, caption start, thumbnail, platforms) and wait for a yes.
- Boosting: rules and ad accounts are in `config/boost.json` (Instagram only, Advantage+ audience, goal profile visits, Rs 100/day for
  2 days). Capital Hyundai and M R Hyundai always use their own ad account; Mahindra Arav and Dee Emm Mahindra fall
  back to the Dee Emm Hyundai / Car & Bike account only when their own can't cover the boost. Create boosts paused,
  show the batch, and activate only after the user says yes. `python scripts/check_ads.py` checks access and balances;
  `python scripts/boost_reel.py plan|create|activate|delete` makes the boost (create = paused, no spend).
- Posting rhythm and static-post rules: `statics/BRAND_SOURCES.md` (a post every second day, cycling 2 videos then 1
  static, flexible when videos are short). Client contacts and logos: `statics/clients.json`.
- Static content buckets and the Calendar/Reviews tabs: `statics/CONTENT_BUCKETS.md`. Google reviews come from
  `scripts/gbp_reviews.py` (setup in `statics/GBP_SETUP.md`; needs GBP_CLIENT_ID, GBP_CLIENT_SECRET, GBP_REFRESH_TOKEN).
- Review posts: whatever goes on social media is in correct English. Column M "Text for post" holds the review with
  its grammar corrected or rephrased in our words, keeping the customer's meaning and facts (names, car, branch,
  what happened) and adding nothing; column G keeps the original. Details in `statics/CONTENT_BUCKETS.md`.
- Both CH-2610-07 and CH-2610-08 (Reel 3 offer and Reel 3) are meant to be posted.

## Video handling

Exports are 1080x1920 H.264 at about 45 Mbps and 95 MB to 1.3 GB, above Instagram's Reels limits. Download with
`drive_folder.download`, then re-encode before upload:
`ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 22 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart out.mp4`
Keep the result under 40 MB: uploads from the cloud session fail above roughly that size (a 61 MB file never
finished on Instagram; 34 and 41 MB files went through). Publish with `scripts/publish_reel.py`; for clients on the
system user token add `--system-user` so Facebook gets the Page token.

## Meta access

One system user token for CH, DEH, AM and CB, read from the `META_SYSTEM_USER_TOKEN` environment variable.
Dee Emm Mahindra and M R Hyundai could not be shared into the agency business portfolio, so each uses a
non-expiring Page token from the user's personal access: `META_PAGE_TOKEN_DEM` and `META_PAGE_TOKEN_MRH`.
Those stop working if the user changes their Facebook password or loses access to the Page; if that happens,
the user regenerates them in Graph API Explorer.

The tokens are environment variables in the "BC Social Automation" environment. Never print, log or commit any
token. When the user says "Check Meta access", run `python scripts/check_access.py` (GET requests only) and report
each client's Page and Instagram account, or what is missing, before any posting code is written or run.
