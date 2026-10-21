# Social posting

Reel covers and helper scripts for posting edited client videos to Instagram and Facebook.

## How posting works

1. Edited videos live in each client's Drive folder, one folder per month.
2. Every video has a row in the **Social Posting Tracker** sheet with a Video ID such as `CH-2610-04`
   (client code, year and month, then a running number).
3. The team marks a row **Approved**, writes the caption in the sheet, and puts the thumbnail in the
   Thumbnail Drive folder, named by Video ID, for example `CH-2610-04.jpg`.
4. When asked to upload a Video ID, `scripts/fetch_thumbnail.py` copies the thumbnail into `thumbnails/`.
   Instagram only accepts a cover image as a public link, so the raw GitHub URL of that file is what gets sent.
5. After posting, the row is set to **Posted** with the date and post links.

## Client codes

| Code | Client |
|---|---|
| CH | Capital Hyundai |
| DEH | Dee Emm Hyundai |
| DEM | Dee Emm Mahindra |
| AM | Arav Mahindra |
| MRH | M R Hyundai |
| CB | Car and Bike |

## Scripts

- `scripts/list_videos.py` lists every video in the client month folders and writes `videos.json`.
- `scripts/fetch_thumbnail.py CH-2610-04` copies that video's thumbnail from Drive into `thumbnails/`.
- `scripts/check_access.py` lists the Pages and Instagram accounts each Meta token can reach (read-only).

Both read Drive folders shared as "Anyone with the link can view", so keep that sharing setting on the
video and thumbnail folders.

No access tokens are stored in this repository. Meta tokens are kept in the session environment settings.
