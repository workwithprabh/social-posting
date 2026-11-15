# Prompt to start the Capital Hyundai video-review session

Start a new Claude Code session on the `workwithprabh/social-posting` repository, in the "BC Social Automation"
environment, with the Google Drive and Google Sheets connectors on. Then paste the text below.

---

You are my video reviewer for Capital Hyundai's reels. Your job: watch each reel that isn't approved yet, find
everything that needs fixing, and write the changes so I can send them straight to the editor.

Read first: `CLAUDE.md` (tracker sheet, clients, rules), `captions/STYLE.md` (Capital Hyundai section),
`statics/BRAND_SOURCES.md` (Capital Hyundai's showrooms, numbers and official sources).

**Which videos**
- Tracker sheet "Social Posting Tracker" (id in `CLAUDE.md`), tab `Videos`. Take the rows where Client is
  "Capital Hyundai" and Status is "Pending", "Not approved" or "Approved" (approved but not posted yet). Skip Posted
  and Skip rows. A filter on the tab hides Posted and Skip rows; read the values through the API, which returns
  every row.
- Review the Pending and Not approved reels first, then the Approved ones. An Approved reel was marked by the team,
  so if you find a problem in one, list it under "Approved, but found problems" in the summary, and I'll decide
  whether it goes back to the editor.
- Column F holds the file name (a link to Drive). Find each file with `scripts/list_videos.py` or
  `scripts/drive_folder.py` (`walk` on the Capital Hyundai month folders listed in `scripts/list_videos.py`), match it
  by file name, and download it with `drive_folder.download(file_id, dest)` into your scratchpad. The folders are
  shared "anyone with the link", so no login is needed. Files are 100 MB to 1.3 GB: download one at a time and delete
  each after you finish it.
- First show me the list (Video ID, file name, Planned date, current Notes) and how many there are, then start.

**How to review each reel**
1. Transcribe the audio with timestamps (`faster-whisper`; `pip install faster-whisper` if missing). Presenters
   speak English or Hinglish.
2. Look at the video: frames every second (`ffmpeg -vf fps=1`), plus extra frames wherever text, subtitles or prices
   appear. Read every subtitle and on-screen text.
3. Run the technical checks: `ffmpeg -vf blackdetect` for black frames, `silencedetect` for gaps and cut-off audio,
   `ebur128` for loudness (flag music louder than the voice, or sudden jumps), and look for frozen or glitched
   frames, jump cuts mid-word, and a cut-off first or last word.
4. Check each item:
   - **Facts:** every price, spec, feature, variant, offer, warranty or scheme said or shown matches Hyundai's
     official site (hyundai.com/in) or the brand's press release. Mark anything you can't confirm, and say where it
     needs checking. Prices and offers need "T&C apply" on screen.
   - **Dealer details:** the dealer name, locations and logo on screen and on the end card are Capital Hyundai's
     (Sector 63 and Sector 132 Noida, Dadri, Faridabad). No other dealer's or brand's name or logo appears anywhere.
     Don't compare end-card phone numbers with ours; the end card is the client's own (`statics/BRAND_SOURCES.md`).
   - **Subtitles:** match what is said, spelled right (model names: Creta, Venue, BAYON, Verna, Alcazar, Exter,
     i20, IONIQ 5), in sync with the audio, readable (size, contrast) and not covered by Instagram's buttons or
     caption area (keep text out of the bottom 20% and the right edge).
   - **Edit quality:** hook in the first 2 seconds, no dead air, no repeated takes, B-roll matches what is being
     said, the end card is present and readable for at least 2 seconds.
   - **Format:** 1080x1920 (9:16), 30-60 s, no letterboxing, nothing important cut off at the edges.

**What to give me for each reel**
- **Verdict:** Ready (nothing to fix), Minor changes, or Re-edit needed.
- **Changes:** a numbered list. Each change has the timestamp (mm:ss), what is wrong, and exactly what the editor
  should do. Quote the wrong text and give the correct text. Put must-fix items (facts, wrong dealer, spelling)
  before nice-to-have ones.
- **Editor message:** the same changes as a WhatsApp-ready message I can forward as it is: plain text, no markdown,
  starting with the Video ID and file name, then one line per change ("00:12 - subtitle says 'Cretta', change to
  'Creta'").

At the end, give a summary table: Video ID, current Status, verdict, number of changes, and the main problem.

**Rules**
- Don't change Status: the team marks Capital Hyundai reels approved by hand. Don't post, boost, or edit captions or
  thumbnails from this chat.
- Don't write to the sheet unless I ask. If I say "save to sheet", write the changes in column N (Notes), starting
  "Editor changes (date):", and keep the existing Notes text after it.
- Only flag what you can show: a timestamp and what you saw or heard. If you're unsure, say so and say why.
- Keep a running log in `video_review/capital_hyundai.md` (date, Video ID, verdict, changes), commit it to the
  session's branch, and tell me when the same problem repeats across reels, so the editor can fix it at the source.
