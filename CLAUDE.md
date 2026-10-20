# Social posting: working notes

This repo backs the posting of edited client reels to Instagram and Facebook. Read README.md for the flow.

## Where things are

- **Tracker sheet:** "Social Posting Tracker", Google Sheet id `1bcx0yZ-5C7F6e_WLg9Kbw8FRQQ4jUaPQ_SRGnJts_NY`
  in the workwithprabh@gmail.com Drive. Tab `Videos`: Video ID, Client, Month, Video file (HYPERLINK to Drive),
  Status (Pending / Approved / Posted / Skip), Platforms (IG + FB / IG only / FB only), Caption, Thumbnail link,
  Post date, Instagram post link, Facebook post link, Notes. Tab `Clients`: code, client, Drive folder.
  Read it with the Drive connector: `download_file_content` with `exportMimeType: text/csv`.
  Writing to it needs the Google Sheets connector; without it, the user updates the sheet by hand.
- **Edited videos:** owned by becarrotsocial@gmail.com, one folder per client, one subfolder per month,
  shared "Anyone with the link can view". Folder ids are in `scripts/list_videos.py`.
- **Thumbnails:** Drive folder `1u6J5NUVc51ZufYb6n5AmO7JXd1QL2Y_D`, one subfolder per client, files named by
  Video ID. `scripts/fetch_thumbnail.py <ID>` copies one into `thumbnails/`; its raw GitHub URL on `main` is the
  Instagram `cover_url`.

## Rules the user set

- Post only when the user says to upload specific Video IDs. The Post date column is not a schedule.
- Captions and thumbnails come from the team (made in ChatGPT); do not generate them.
- Before publishing, show the user the batch (ID, client, caption start, thumbnail, platforms) and wait for a yes.
- Both CH-2610-07 and CH-2610-08 (Reel 3 offer and Reel 3) are meant to be posted.

## Video handling

Exports are 1080x1920 H.264 at about 45 Mbps and 95 MB to 1.3 GB, above Instagram's Reels limits. Download with
`drive_folder.download`, then re-encode before upload:
`ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 20 -maxrate 20M -bufsize 40M -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart out.mp4`

## Meta access

One system user token for CH, DEH, AM and CB, read from the `META_SYSTEM_USER_TOKEN` environment variable.
Dee Emm Mahindra and M R Hyundai could not be shared into the agency business portfolio, so each uses a
non-expiring Page token from the user's personal access: `META_PAGE_TOKEN_DEM` and `META_PAGE_TOKEN_MRH`.
Those stop working if the user changes their Facebook password or loses access to the Page; if that happens,
the user regenerates them in Graph API Explorer.

Never print, log or commit any token. First step once they exist: a read-only check that lists the Pages and
linked Instagram accounts each token can reach, before any posting code runs.
