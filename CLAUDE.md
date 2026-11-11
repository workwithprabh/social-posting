# Social posting: working notes

This repo backs the posting of edited client reels to Instagram and Facebook. Read README.md for the flow.

## Where things are

- **Tracker sheet:** "Social Posting Tracker", Google Sheet id `1bcx0yZ-5C7F6e_WLg9Kbw8FRQQ4jUaPQ_SRGnJts_NY`
  in the workwithprabh@gmail.com Drive. Tab `Videos`, columns A-N: Planned date, Video ID, Client, Added to
  Drive (the video file's Drive upload date, India time), Month, Video file (HYPERLINK to Drive), Status (Pending /
  Approved / Not approved / Posted / Skip; the Dashboard counts these exact words), Platforms (IG + FB / IG only /
  FB only), Caption (Done/Pending, an ARRAYFORMULA in I2 that looks up the `Captions` tab: never type in column I),
  Thumbnail (the thumbnail's Drive link when done, else "Pending"), Post date, Instagram post link, Facebook post
  link, Notes. A filter hides Posted and Skip rows: lift it before bulk copies or clears, because copies and clears
  skip hidden rows. Never reset `textFormat` over the link columns (F, J, L, M): that removes the hyperlinks. A URL
  written through the API stays plain text until its cell gets `textFormat.link`, so set it whenever writing a link.
  Tab `Captions`: ID, Caption (caption text for every video and static, looked up by ID).
  Tab `Statics`: the static-post calendar (see `statics/CONTENT_BUCKETS.md`). Tab `Dashboard` (formulas only; don't type into it except the blue inputs): "Ready to post, by client" (approved
  videos and statics against the posts needed until the plan date, at a post every second day and 2 videos per static,
  and the date the ready content lasts until) and "Posted in the month" (from Post date in Videos and Date in Statics;
  it moves to the new month on the 1st). Client names in Videos C and Statics B must match the `Clients` tab exactly
  ("Arav Mahindra", "Car and Bike"), or the Dashboard won't count them; fill Post date whenever a video is posted.
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
  (Mahindra style; Hyundai and Car & Bike use the same rules in their own colours, refs in `cover/refs/`),
  updated by the v2 rules below.
- **Thumbnail standard (user, 9 Nov 2026: "perfect", use for all future thumbnails).** Recipe in `cover/README.md`
  (sections "v2 style", "Faces: expression rules", "AI expression edit"); reference covers: AM-2610-05 (the user's
  pick) and the finals of DEH-2610-04, DEH-2610-05, AM-2610-07.
  1. Decide the reel's mood first (happy/reassuring = confident closed-mouth smile; shocking news = shocked, brows
     high, eyes wide, round "O" mouth; emotional = soft brows, closed mouth; advice = calm, confident smile).
  2. Pick the clearest, front-facing close-up of the presenter, then edit only the expression with Canva's
     `generate-image` (same person, clothes, setting; no teeth, no mid-word mouth; soft even front light, glowing
     skin). Never use a talking frame with the mouth open or teeth showing. Check with `cover/face_expr.py`.
  3. Build with `cover/build_v2.py`: big bright presenter on the right (face ~26% of the width), thin gold (Mahindra)
     or white-blue (Hyundai) edge glow, lightly blurred real background with no presenter in it, headline of 2 lines
     plus a neon box with the main question, a small tilted card from the reel on the left. No brand logo on reel
     thumbnails (user, 9 Nov 2026); the account posting it already shows the brand. No "WATCH THIS FIRST!" banner
     either (user, 9 Nov 2026: it has been there too long and isn't needed).
  4. Notes on the row say "presenter's expression edited with AI".
  5. Hyundai covers (user, 9 Nov 2026: Capital Hyundai looked dim, no glow): set `strong_rim`, `backlight` 0.6,
     `face_light` 8, `target_L` 66, no `skin_neutral` (it turned the skin white; keep the warm natural tone) (cover/README.md "Hyundai brightness and glow"), and give each
     reel a distinct expression.
  6. **Skin tone (user, 9 Nov 2026: approved on CH-2610-06, "looking good").** Keep the warm, natural skin of the
     earlier covers; never let it go pale or white. Check with `python3 cover/skin_tone.py <cover>`: skin chroma about
     29-38 (the old covers' range), L about 66-80. If an AI edit comes out pale, warm it gently with `skin_ab`
     (e.g. [1.25, 1.05]); stronger values turn the face red and the lips magenta, so look at a face crop every time.
  7. **Skin hue (user, 11 Nov 2026: Car & Bike faces looked "very odd", orange).** Keep skin hue about 48-55 deg (approved
     covers: DEH-2610-05 48, AM-2610-05 50, CH-2610-06 55); above ~60 reads orange/filtered. When warming a pale frame
     with `skin_shift`, add red as well as yellow (CB-2611-02: [16, 21]; CB-2611-03: [10, 8]); a yellow-heavy shift
     ([8, 22]) gave hue 63-72. Too much red tints brown hair and the face pink. Keep the gold backlight low (0.2) on
     Car & Bike covers. Compare face crops with an approved cover before sending.
  8. **Car & Bike reel covers show the car, not the presenter** (user, 11 Nov 2026). Build with `cover/build_car.py`
     (cover/README.md "Car-hero covers"); Capital Hyundai and the other clients keep the presenter covers.
  Captions follow `captions/STYLE.md` and use only facts said in the reel.
- Drafts go to the Drive folder "Claude drafts" (`1KDnTFCTb2SoIW3168M26spmO3htJwX8o`, workwithprabh Drive), sorted
  as `Video thumbnails/` or `Social media posts/`, then `<YYYY-MM Month>/`, then the client (ids in
  `config/drafts_folders.json`; make the month's folders when a new month starts). Thumbnails are named
  `<Video ID>.jpg`; put the caption in the `Captions` tab (row with the Video ID) and the draft's link in the Thumbnail column, and set Notes to
  "Draft by Claude, needs review". Never put drafts in the team's Thumbnail folder: a file there named by Video ID
  is treated as the approved cover.
- Before publishing, show the user the batch (ID, client, caption start, thumbnail, platforms) and wait for a yes.
- Captions are plain text: no bold, no markdown (`**`, `__`), no trailing spaces (user, 9 Nov 2026).
- Review and other static posts are posted by Claude (user, 9 Nov 2026). Before posting each one, check that the
  caption, the image and the footer numbers belong together (same customer, staff, car, branch; showroom vs service
  numbers per `statics/BRAND_SOURCES.md`), and post only the text after "Caption draft:" in the Captions tab.
- Hyundai static posts (user, 9 Nov 2026) follow @hyundaiindia's own look, not ours for Mahindra: sentence-case type,
  big photography, a small Active Blue (#00AAD2) label, thin outline pills; black (like the BAYON series), light studio
  or full photo, mixed so each dealer's feed varies. No heavy red boxes or condensed caps (that is the Mahindra look),
  and no all-over blue gradient (the user found it looked very bad). Template `statics/review_card/hyundai.html`.
- Capital Hyundai Dadri showroom number is 72900 77273 everywhere (user, 9 Nov 2026; matches the reel end card).
- Boosting: rules and ad accounts are in `config/boost.json` (Instagram only, Advantage+ audience, goal profile visits, Rs 100/day for
  2 days). Capital Hyundai and M R Hyundai always use their own ad account; Mahindra Arav and Dee Emm Mahindra fall
  back to the Dee Emm Hyundai / Car & Bike account only when their own can't cover the boost. Create boosts paused,
  show the batch, and activate only after the user says yes. `python scripts/check_ads.py` checks access and balances;
  `python scripts/boost_reel.py plan|create|activate|delete` makes the boost (create = paused, no spend).
- Posting rhythm and static-post rules: `statics/BRAND_SOURCES.md` (a post every second day, cycling 2 videos then 1
  static, flexible when videos are short). Client contacts and logos: `statics/clients.json`.
- Static content buckets and the Calendar/Reviews tabs: `statics/CONTENT_BUCKETS.md`. Google reviews come from
  `scripts/gbp_reviews.py` (setup in `statics/GBP_SETUP.md`; needs GBP_CLIENT_ID, GBP_CLIENT_SECRET, GBP_REFRESH_TOKEN).
- Static footers: service posts show service numbers, showroom posts showroom numbers, general posts both.
  Dee Emm Mahindra uses its EV logo only for EV posts; every other post uses the twin-peaks logo
  (`statics/BRAND_SOURCES.md`, ids in `statics/clients.json`).
- Review posts: whatever goes on social media is in correct English. Column M "Text for post" holds the review with
  its grammar corrected or rephrased in our words, keeping the customer's meaning and facts (names, car, branch,
  what happened) and adding nothing; column G keeps the original. Details in `statics/CONTENT_BUCKETS.md`.
- Both CH-2610-07 and CH-2610-08 (Reel 3 offer and Reel 3) are meant to be posted.

## Video handling

Exports are 1080x1920 H.264 at about 45 Mbps and 95 MB to 1.3 GB, above Instagram's Reels limits. Download with
`drive_folder.download`, then re-encode before upload:
`ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 22 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart out.mp4`
Keep the result small: uploads from the cloud session fail above a size that varies (a 61 MB file never
finished on Instagram; 34 and 41 MB files went through in Oct, but on 11 Nov 2026 a 27 MB file failed twice with
ProcessingFailedError while 17 MB went through). If Instagram fails, re-encode smaller with `-crf 25 -maxrate 3M
-bufsize 6M -b:a 128k` (about 15-20 MB for a 50 s reel) and retry. Without `--cover-url`, `publish_reel.py` makes the
cover link itself from `--cover-file` (an unpublished Page photo, deleted afterwards). Publish with `scripts/publish_reel.py`; for clients on the
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
