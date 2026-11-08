# Daily sheet sync (scheduled task)

A scheduled task on claude.ai runs every day at **8:45 India time** and keeps the tracker sheet up to date. It
starts a fresh session with only the **Google Drive** and **Google Sheets** connectors (signed in as
workwithprabh@gmail.com) and no repository.

| | |
|---|---|
| Name | Daily sheet sync |
| ID | `trig_01A36aTAyZBTeD5J2yijSm2a` |
| Schedule | `CRON_TZ=Asia/Kolkata 45 8 * * *` |
| Writes to | Tracker sheet tabs `Videos` and `Reviews` only |
| Reads | Client video folders (Drive), DMU GBP sheet `Reviews_Raw` (read-only) |
| Created by | the account "Jiti" on 1 Nov 2026; prompt last changed 8 Nov 2026 |

What it does:
- **Part A, videos:** finds this month's and last month's folder in each client's root folder, adds a `Pending`
  row for every new video (Video ID, Added to Drive date, HYPERLINK to the file), keeps the rows sorted by Added to
  Drive and restores the filter that hides Posted/Skip rows. It never changes Status, captions, links or IDs.
- **Part B, reviews:** copies up to 3 new 5-star Dee Emm Hyundai reviews per branch per day from the DMU sheet into
  the `Reviews` tab, with the rules in `statics/CONTENT_BUCKETS.md`.

After each run a push notification goes to the Claude app on the owner's phone (turned on in the claude.ai
scheduled tasks screen on 8 Nov 2026). The full run summary is in the run's session (claude.ai/code → scheduled
tasks → Daily sheet sync → last run).

To see or change it, ask Claude in a session that has the claude-code-remote tools: "show the daily sync task" or
"update the daily sync prompt". If the task is ever lost, recreate it from the prompt below (same schedule,
Drive + Sheets connectors). Keep this copy in step with the live prompt whenever it changes.

## Prompt (as of 8 Nov 2026)

````text
Daily sync of the "Social Posting Tracker" Google Sheet: (A) new edited client videos from Google Drive, and (B) new good Google reviews for Dee Emm Hyundai. Use only the Google Drive and Google Sheets connectors. Do not post anything to social media, do not create thumbnails or captions, and do not write anywhere except the tracker sheet. The DMU review sheet in part B is read-only: never write to it. If either connector is not available in this session, stop and report that instead of trying another way.

## Where things are
- Sheet: spreadsheet id `1bcx0yZ-5C7F6e_WLg9Kbw8FRQQ4jUaPQ_SRGnJts_NY`, tab `Videos` (sheetId 589291894). Columns A-M: A Video ID, B Client, C Added to Drive, D Month, E Video file, F Status, G Platforms, H Caption, I Thumbnail link, J Post date, K Instagram post link, L Facebook post link, M Notes. Rows are sorted by Added to Drive (column C), oldest at the top and newest at the bottom, then by Video ID for the same date. Clients are mixed together.
- The `Dashboard` tab is all formulas that read the Videos tab. Never write to it. Leave the `Calendar` tab alone.
- The Videos tab has a filter that hides Posted and Skip rows. Leave the filter as it is; read with get_spreadsheet / get_values, which return hidden rows too.
- Column E holds a formula like `=HYPERLINK("https://drive.google.com/file/d/<FILE_ID>/view","<file name>")`. Read it with Google Sheets get_spreadsheet (includeGridData, fields `sheets.data.rowData.values.userEnteredValue`) to get each row's Drive file ID.
- Column C "Added to Drive" is the date the video file was uploaded to Google Drive: the file's `createdTime` from Drive, converted to India time (UTC+5:30), written like `7 Nov 2026`. The column is formatted as a date (d mmm yyyy).
- Column D "Month" is written like `Nov 2026` (the sheet stores it as a date and shows it as mmm yyyy).
- Client root folders in Drive (owned by becarrotsocial@gmail.com), one subfolder per month:
  - CH, Capital Hyundai: 150lMiEOdNYDFoTrGrQN_t58GWPEXBFX_
  - DEH, Dee Emm Hyundai: 1gsVkvsqjy89O8K2Tc0rVQCl5p3N80ixP
  - DEM, Dee Emm Mahindra: 1CumF3EbcvxfNhxwIPwZBC6LXlhDEV-1h
  - AM, Arav Mahindra: 1njpvbueNFwJILVlVXStz85jmqulNNlSX
  - MRH, M R Hyundai: 1Tl4Ru87CdTSHUUggIygbYekEKlEWtwxR
  - CB, Car and Bike: 1YQZiRlRM70XV2OvxDQi9BYDxqo9AuOFY

## Part A: videos
1. For each client, list the subfolders of its root folder (Drive search_files with `parentId = '<id>' and mimeType = 'application/vnd.google-apps.folder'`; follow next_page_token until it is exhausted, because pages are small). Keep only month folders for the current calendar month and the previous one (India time), matched by month name and year in the folder name, e.g. "oct 2026", "Oct 2026", "Sept 2026", "Nov 2026". Ignore 2025 folders and anything else.
2. List every video file (mp4/mov) in those month folders, including any subfolders inside them (`parentId = '<month folder id>'`, paginate fully). Keep each file's `createdTime`.
3. Read the sheet as described above and build the set of Drive file IDs already in column E.
4. For each video whose file ID is not in the sheet, prepare a new row (columns A-M in this order):
   - A Video ID: `<CODE>-<YYMM>-<NN>`, YYMM from the folder's month (Oct 2026 = 2610, Nov 2026 = 2611), NN = 1 + the highest existing NN for that code and YYMM, two digits. Assign numbers in file-name order. Before writing, check that no other row already uses the ID.
   - B Client = full client name above; C Added to Drive = the file's createdTime as an India-time date, e.g. "7 Nov 2026"; D Month = "Mon YYYY" of the folder (e.g. "Nov 2026"); E Video file = the HYPERLINK formula with `https://drive.google.com/file/d/<id>/view` and the file name; F Status = "Pending"; G Platforms = "IG + FB"; H Caption, I Thumbnail link, J Post date, K Instagram post link, L Facebook post link left empty.
   - M Notes, only when it applies: "1:1 (square) version of <ID>" for a file whose name ends in "1-1" when the matching non-square file exists; "File name says <Mon>, but it is in the <Mon> folder" when the month in the name differs from the folder; "Possibly a revised version of <name>" for names with "new", "v2"/"v3", "_1" next to a same-named file.
5. Add the new rows directly below the last filled row (no blank rows in between), in Added to Drive order, oldest first. Insert the rows with update_spreadsheet insertDimension (ROWS, inheritFromBefore true) right after the last filled row so they pick up the formatting, then write columns A-M with update_formulas so the HYPERLINK formulas stay live. Then sort the data rows (row 2 to the last filled row, columns A-M) with update_spreadsheet in one batch: clearBasicFilter on sheetId 589291894; sortRange by column C (dimensionIndex 2) ascending, then column A (dimensionIndex 0) ascending; then setBasicFilter with range A1:M1000 (startRowIndex 0, endRowIndex 1000, startColumnIndex 0, endColumnIndex 13) and filterSpecs [{columnIndex 5, filterCriteria {hiddenValues ["Posted","Skip"]}}], so the filter is exactly as before.
6. For existing rows whose Drive file is now in a different month folder than the Month column (D) says, update ONLY the Month cell and clear a Notes cell (M) that is now wrong about the folder. Never change Video IDs. If an existing row's Added to Drive cell (column C) is empty, fill it from the file's createdTime (and re-sort as in step 5).
7. Never delete rows and never change Status, Caption, Thumbnail link, Post date, post links, or Platforms of existing rows. If a row's file can no longer be found in its month folder, leave the row alone and just mention it in the summary.
8. Read the sheet back to confirm the writes landed, the rows are in date order, and the row count went up by exactly the number of videos added.

## Part B: Dee Emm Hyundai Google reviews
Source (READ-ONLY): the "DMU GBP Intelligence & Review Audit" sheet, id `1r9c4Bhjsya3kDnBbUldHnZyeg-0T30tP3hPaJpI_3p4`, tab `Reviews_Raw`, filled every 3 hours by a GitHub job. Columns: A Review_ID, C Location_Name, E Reviewer_Name, F Star_Rating, G Review_Text, H Review_Create_Time, O Review_URL, R Current_Status, U Review_Date, W Duplicate_Flag. Newest reviews are at the top.
Target: tracker tab `Reviews` (columns A-M: Review ID, Client, Location, Stars, Reviewer (on Google), Name for post, Review text, Review date, Google link, Use?, Posted on, Notes, Text for post).
The goal is reviews that make a genuine, good-looking post: meaningful, a bit long, in clear English, about this dealership.
9. Read Reviews_Raw!A2:W400 from the DMU sheet and the tracker's Reviews!A2:A3000 (the IDs already there).
10. Candidates: Review_ID not already in the tracker; Star_Rating = FIVE; Current_Status is not Removed; Duplicate_Flag is empty; Review_Create_Time within the last 7 days; the text, after removing Google's translation (if it contains "(Original)", keep only what follows it; otherwise drop everything from "(Translated by Google)" on), has at least 25 words and at most 500 characters.
11. Read each candidate yourself and keep it only if: it is in English (skip Hinglish/Hindi); it is about the experience at this dealership (skip generic essays about Hyundai cars or prices); it does not look pasted or templated (skip text with curly quotes “ ”, a leading "Google Review", or star emojis at the start; skip near-identical reviews from the same family or day praising the same person, keeping one); and it reads clearly enough that at most typo-level fixes are needed (spelling, capital letters, spacing, punctuation, "u" -> "you"). If it would need any rewording, skip it. Prefer reviews that name staff or describe the delivery, purchase or service. Keep at most 3 per branch per day.
12. Append each kept review as a new row directly below the last filled row of the Reviews tab: A Review_ID; B "Dee Emm Hyundai"; C Location_Name without the "DM Hyundai " prefix; D 5; E Reviewer_Name; F Name for post = first name + last initial with a full stop, capitalised, with digits removed and honorifics ("ji", "sir", "Mr", "Ms", "Dr") ignored (e.g. "pooja sehgal" -> "Pooja S.", "SACHIN YADAV8826" -> "Sachin Y.", "Shivam Veram ji" -> "Shivam V.", "Rahul 123" -> "Rahul"); G the review text exactly as written (after step 10's translation removal), never edited; H Review_Date (e.g. "7 Nov 2026"); I Review_URL; J "New"; K empty; L "From the DMU GBP sheet. Text for post: " followed by the fixes made, or "no changes." (add "Check first: reviewer name may be a staff account." if the reviewer name looks like a role or business, e.g. "CRE", "Sales", "Service", "Studio"); M Text for post = the review with only the typo-level fixes from step 11, same words and meaning.
13. Never change existing rows in the Reviews tab (the team edits Use?, Posted on, Notes and Text for post).

## Report
End with a short summary: how many videos were added per client with their new Video IDs and their Added to Drive dates, any Month corrections, anything flagged (square copies, multiple versions, files missing from Drive, new month folders seen), and how many Dee Emm Hyundai reviews were added per branch (and how many candidates were skipped for English or authenticity). If nothing changed, say "No new videos or reviews today."
````
