# Capital Hyundai video review log

Running log of editor reviews of Capital Hyundai reels before posting. Each entry: date, Video ID, file, verdict,
changes (must-fix first). Timestamps are mm:ss in the Drive file. "Bottom 20%" means y > 1536 of 1920, where
Instagram's caption and buttons cover the frame.

How a reel is reviewed: faster-whisper transcript (English and Hindi passes), frames at 1 fps plus OCR at 4 fps,
ffmpeg blackdetect / freezedetect / silencedetect / ebur128, and offers or specs checked against hyundai.com/in or
press reports.

## Repeating problems (tell the editor once, fix at the source)

From the 15 Nov 2026 review of 10 reels:

1. **The closing call to action isn't subtitled** in 8 of 10 reels (CH-2611-03, -05, -06, -01; CH-2610-07, -09, -10,
   -11). The subtitles stop before the "call / visit Capital Hyundai" line, often the part with the dealer name.
   Fix in the subtitle template: every spoken line up to the end card gets a subtitle.
2. **Audio true peak at or above 0 dBFS** in 8 of 10 (+0.1 / +0.2). Add a -1 dBTP limiter on export. Loudness is also
   uneven: CH-2611-06 is -19.3 and CH-2611-01 is -20.5 LUFS against about -15 for the rest. Normalise every export to
   about -14 LUFS.
3. **End card:** the last two Service Centre lines (Faridabad, Sector 132) sit in the bottom 20%, under Instagram's
   caption, on every reel. Move the list up about 120 px. There are also **two versions of the card**: the Oct reels
   show Sector 132 service as 95600 27864, the Nov reels as 99589 94275. Ask the client which is current and use one
   card file.
4. **The Capital Hyundai logo disappears on white or bright backgrounds** (CH-2611-04, -06, -01, -02; CH-2610-11).
   Add a soft drop shadow to the logo layer.
5. **B-roll from other dealers or foreign markets:** CH-2610-09 shows "JRD Nimbus Hyundai" and "Shivang Hyundai"
   signage and a Creta with an Arabic-script plate. The same stock "CRETA N Line" studio shot appears in CH-2610-07,
   -10 and -11. Check every stock or borrowed clip for signage, plates and logos before using it.
6. **Readable number plates** on customer or pre-owned cars (CH-2611-05, -04, -01). Blur them by default.
7. **Subtitle language is mixed:** the Oct reels use English translations, the Nov reels use Hinglish as spoken. Pick
   one style for Capital Hyundai.

---

## 15 Nov 2026 – CH-2611-03 – Capital Hyundai Nov Reel-5.mp4 (Pending)

33 s, 1080x1920, 30 fps. Topic: November offers (offer card for Creta, Alcazar and Verna), exchange, corporate and finance.

**Verdict: Re-edit needed**

1. 00:10-00:14, offer card. **Must fix:** the card says "Valid until 13 November 2026", but that date has passed and
   the reel isn't posted yet. The figures (Creta ₹1,15,000 "Petrol trims other than E and iVT", Alcazar ₹90,000 petrol,
   Verna ₹1,05,000 "Previous-model Verna iVT") match Autopunditz's November list, and that list says the Diwali bonus
   in them applied only 1-13 Nov 2026. Autocar India gives lower figures (Creta petrol up to ₹1.10 lakh). Neither
   source is hyundai.com/in. Get the current offers and end date from Capital Hyundai sales, then remake the card
   (or drop it).
2. 00:10-00:14, offer card. **Must fix:** there's no "T&C apply" anywhere. Add "*T&C apply" under the validity line.
3. 00:26-00:29. **Must fix:** the last line has no subtitle. She says "Capital Hyundai ko call kijiye ya phir aap
   showroom pe visit kar sakte hain"; add that subtitle.
4. 00:10-00:14, offer card: "Valid until …" and "Check the caption for offers on all other Hyundai cars." sit at
   y 1620-1830, inside the bottom 20%, where Instagram's caption covers them. Move both up (shrink the three car
   panels slightly).
5. 00:15, subtitle "Aur sab discounts hi nahi,". Unsure: the Hindi pass hears "sab", and the meaning ("not just
   discounts") suggests "sirf". The editor should listen once and use "Aur sirf discounts hi nahi," if she says sirf.
6. 00:16, exchange shot: the old car is a Honda Brio, and the Honda "H" badge is visible on the rear wheel cap.
   Blur the badge (small, low priority).
7. 00:00-00:02: she walks in silently and the first line ("Hyundai shortlist kar li?") starts at 00:02. Trim about
   1.5 s from the start so the question opens the reel.
8. Audio: true peak +0.1 dBFS (integrated -15.9 LUFS). Put a limiter at -1 dBTP so Instagram's encode doesn't clip.
9. 00:30-00:33, end card: the last two service lines (Faridabad 93559 31003, Sector 132 99589 94275) are in the
   bottom 20%. Move the list up about 120 px.

Checked and fine: Capital Hyundai logo top-right throughout, showroom exterior with the Capital Hyundai pylon
(00:05), the other subtitles match the audio, no black frames, the 4 s freeze at 00:10-00:14 is the static offer
card (intended), music sits under the voice, and the end card shows for 3.2 s.

## 15 Nov 2026 – CH-2611-05 – Capital Hyundai Nov Reel-7.mp4 (Pending)

30 s, 1080x1920, 30 fps. Topic: pre-owned cars in Capital Hyundai's Hyundai Promise section (skit, then presenter).

**Verdict: Minor changes**

1. 00:20-00:27. **Must fix:** the whole closing call to action has no subtitles. Add: "Toh wait kis baat ka hai?" /
   "Aaj hi Capital Hyundai ko call kijiye," / "available cars check kijiye" / "aur apni favorite car ki test drive
   book kijiye."
2. 00:07 and 00:11. **Must fix (spelling):** the programme is spelled two ways: "Aur woh bhi Hyundai Promise se!"
   (00:07) and "Capital Hyundai ke H-Promise section mein aap" (00:11). The current official name on hyundai.com/in is
   "Hyundai Promise", which is also what the placard at 00:25 says ("H-Promise" is the old name). She says "H Promise";
   make both subtitles say "Hyundai Promise".
3. 00:03-00:08 (black Creta, plate ending "2075") and 00:24 (white Verna, plate "UP 16 …" readable): these are
   pre-owned stock cars, so blur the number plates.
4. 00:00-00:02 and 00:08-00:10: the Capital Hyundai logo is missing in these shots but present everywhere else.
   Keep it on throughout.
5. Audio: true peak +0.1 dBFS (integrated -14.1 LUFS). Put a limiter at -1 dBTP.
6. 00:27-00:30, end card: the last two service lines are in the bottom 20% (same card as CH-2611-03).

Checked and fine: the hook at 00:00 ("Arre wah! Nayi Hyundai le li? Kitne ki padi?"), the rest of the subtitles,
the white flash at 00:16.2-00:16.5 (a transition), no black frames, no dead air, music under the voice, and the end
card shows for 3.1 s.

## 15 Nov 2026 – CH-2611-04 – Capital Hyundai Nov Reel-3.mp4 (Pending)

1:57 (117 s), 1080x1920, 30 fps. Customer testimonial: Creta accident, roadside pickup, cashless repair at
Capital Hyundai service.

**Verdict: Re-edit needed** (too long, plus subtitle grammar)

1. Whole reel. **Must fix (format):** it runs 117 s against our 30-60 s limit. Suggested 55 s cut using his own lines:
   00:00-00:06 (intro, 13 years) + 00:20-00:34 (Chennai trip, son's accident, the call) + 00:47-01:07 (they called
   my son, crane, workshop, daily updates, policy number, no cash paid, car ready) + 01:29-01:34 ("That kind of
   service … anywhere else") + 01:52-01:54 ("it's amazing … things are going very fine for me") + end card.
2. 00:07-00:10. **Must fix:** there's no subtitle while the old photo frame is on screen. He says "jo ki maine Capital
   Hyundai se khareedi thi 2013 mein"; add that subtitle.
3. 00:00-00:02. **Must fix (name):** the subtitle says "Devender Mehas", but both transcription passes hear "Devinder /
   Devendra Manas". Confirm the spelling of the customer's name with Capital Hyundai before posting.
4. 00:12-00:13. **Must fix (spelling):** "Capital Hyundai se khridi hai." Change to "Capital Hyundai se khareedi hai."
5. 00:41-00:42. **Must fix:** "and I just called him and told told complete story." Change to "and I just called him
   and told him the complete story."
6. Must fix (grammar, matching what he says):
   - 00:31-00:33 "he share the complete story with me." Change to "he shared the complete story with me."
   - 00:43-00:44 "I share my son's mobile number to him," Change to "I shared my son's mobile number with him,"
   - 00:47-00:48 "He immediately call back my son." Change to "He immediately called back my son."
   - 00:49-00:53 "He, you know, send the service person over there" Change to "He, you know, sent the service person over there"
   - 01:00-01:02 "& then he started working for that, whereas in I have not paid any cash to this." Change to "and then he started
     working for that, whereas I have not paid any cash for this."
   - 01:32-01:33 "I don't expect is going to come from anywhere else." Change to "I don't expect it's going to come from
     anywhere else."
   - 01:34-01:36 "I am really, happy, the way they are, uh, serving us." Change to "I am really happy the way they are serving us."
   - 01:43-01:44 "…for the service, Whenever you will come…". Lower-case the second "whenever".
7. 01:34-01:36, the "18 years of serving customers" overlay: he doesn't say this. Confirm Capital Hyundai's founding year
   with the client before it goes out.
8. 00:53, B-roll: the Creta in the paint booth has plate "MP04 ZN 7513" readable. It may not be his car (his delivery
   photo shows a UP 16 plate), so blur it.
9. 00:07-00:10 and 01:05-01:08: the white Capital Hyundai logo disappears on the white or bright-sky background. Add a soft
   shadow or move it.
10. Nice to have: 00:36-00:39 "that I just called, service agent which is there in the, Capital,". Drop the stray commas
    ("that I just called the service agent at Capital,"). 01:12-01:13 "as the damage, photographs which is being shown
    to me, is all over." Remove the commas.
11. Audio: true peak +0.1 dBFS (integrated -12.9 LUFS). Put a limiter at -1 dBTP.
12. 01:54-01:57, end card: the last two service lines are in the bottom 20% (same card as the other reels).

Checked and fine: the "24×7 Roadside Assistance", "Repair progress updates" and "Cashless insurance claims" overlays
match what he describes. "5 Service Centre/Bodyshop locations across Noida" matches the end card (Sector 63, 3, 58,
83, 132). No black frames or dead air, and the end card shows for 3.4 s.

## 15 Nov 2026 – CH-2611-06 – Capital Hyundai Nov Reel-8.mp4 (Pending)

45 s, 1080x1920, 30 fps. Topic: Hyundai BAYON HX10 smart features (Gen AI voice assistant, dual screens,
blind-spot view monitor).

Facts checked against hyundai.com/in (BAYON features page, launch press release of 26 Oct 2026, variants blog): the
Generative AI voice assistant (weather, travel), the dual 12.3" curved panoramic displays and the Blind-spot View
Monitor (BVM) are HX10-only. The Surround View Monitor (SVM) is on HX8 and HX10.

**Verdict: Re-edit needed**

1. 00:00-00:07. **Must fix:** the hook has no subtitles. She asks "Hey, aaj weather kaisa rahega?" and the car answers
   "Aaj mausam saaf rahega aur temperature rahega 28 degree Celsius." Without subtitles the joke is lost with the sound
   off. Add both lines (the car's reply styled differently).
2. 00:28-00:35. **Must fix (B-roll vs facts):** she describes the Blind-spot View Monitor (indicator on, side camera
   view), but the screen shows the Surround View Monitor (top view plus rear camera with parking guide lines), and the
   overlay says "360-degree camera in New Hyundai Bayon HX10 variant". Either use a shot of the indicator on with the
   side-camera feed, or keep this shot and change the overlay to "Surround View Monitor (HX8 & HX10)".
3. 00:32-00:35. **Must fix (spelling):** the overlay says "New Hyundai Bayon". Change to "New Hyundai BAYON", matching
   the subtitles and Hyundai's spelling.
4. 00:36-00:41. **Must fix:** the closing call to action has no subtitles. Add "Toh experience kijiye Hyundai BAYON ke
   yeh smart features" / "aur aaj hi test drive book kijiye."
5. 00:08-00:11. **Your call:** "Dekha? Yeh jawab Siri ne nahi, Hyundai BAYON ne diya!" names Apple's Siri on screen and
   in the audio, and our rule is no other brand's name. If the client doesn't want it, change the subtitle to "Yeh
   jawab phone ne nahi, …" (the audio would need a new take).
6. 00:19-00:21: "Aur dekhiye iski dual 12.3-inch curved screens!" These are HX10-only. Add "(HX10)" so buyers of
   other variants aren't misled.
7. 00:12-00:14 vs 00:15: the outfit changes mid-sentence (red top, then blazer) on "BAYON HX10 ke Gen AI Voice
   Assistant se / aap nearby places…". Use takes from one outfit for the sentence, or cut on a B-roll shot.
8. 00:00 and 00:40-00:41: the Capital Hyundai logo is missing. From 00:01 to 00:11 it sits on a blown-out white ceiling
   and the H emblem disappears. Add a shadow or darken the top of the frame.
9. Audio: integrated -19.3 LUFS, about 5 dB quieter than our other reels (-13 to -16). Raise it to about -14 LUFS
   (true peak is -1.8 dBFS, so there's headroom).
10. 00:42-00:45, end card: the last two service lines are in the bottom 20% (same card as the other reels).

Checked and fine: the subtitles that are there match the audio, BAYON is spelled right in them, no black frames, and
the end card shows for 3 s.

## 15 Nov 2026 – CH-2610-07 – Capital Hyundai Oct Reel 3 offer.mp4 (Approved; planned Tue 17 Nov)

31 s, 1080x1920, 29.97 fps. Topic: Creta daily-driving features (auto hold, voice commands, rear camera and
sensors). There's no offer in this video despite the file name.

Facts checked against the hyundai.com/in Creta features table: "Electric parking brake with auto hold" is on S(O),
S(O) Knight, SX Premium, King, King Knight and Lounge Edition, automatic only. "Voice enabled smart panoramic"
sunroof is on SX and above. "Rear camera with dynamic guidelines" is on EX(O) and above. Rear parking sensors are on
every trim.

**Verdict: Minor changes** (approved by the team, but problems found)

1. 00:24-00:28. **Must fix:** the closing call to action has no subtitles. She says "Contact Capital Hyundai and book
   your test drive of Hyundai Creta today"; add that line.
2. 00:05-00:08. **Must fix (facts):** "If auto-hold is on at a traffic signal, there is no need to keep pressing the
   brake." Auto hold is only on automatic S(O)-and-above trims. Add "(select automatic variants)".
3. 00:00-00:03. **Must fix (grammar):** "How easy daily drive can be in Hyundai Creta, see." Change to "See how easy
   daily driving can be in the Hyundai Creta."
4. 00:16-00:20, "REAR CAMERA / DYNAMIC GUIDELINES": not on E or EX. Add "select variants" to the "helps a lot in
   parking" line.
5. 00:12: the B-roll shows a "CRETA N Line" (badge visible) while she talks about the Creta's AC and sunroof. Use a
   regular Creta shot.
6. 00:16 and 00:18: the rear-camera and settings shots come from older Hyundai cabins (different screen and dash from
   the new Creta). Use the new Creta's screen if you have the footage.
7. Subtitle style: this reel uses English translations, while the Nov reels use Hinglish as she speaks. Pick one style
   for Capital Hyundai.
8. 00:28-00:31, end card. FYI, not a change: this older card lists the Sector 132 service centre as 95600 27864, while
   the Nov reels' card says 99589 94275. Ask the editor which card is current.
9. Audio: true peak +0.2 dBFS. Put a limiter at -1 dBTP.

Checked and fine: the voice-command screen at 00:13 shows the car's own climate voice commands (and the subtitle says
"in selected variants"), the hook is in the first 2 s, there's no dead air (00:15-00:20 is music with on-screen
labels), the end card shows for 2.8 s, and there are no other brands.

## 15 Nov 2026 – CH-2610-09 – Capital Hyundai Oct Reel 4.mp4 (Approved; planned Thu 19 Nov)

47 s, 1080x1920, 29.97 fps. Topic: choosing a Hyundai for your parents (entry and exit, seating, visibility,
automatic, camera, safety, rear-seat comfort).

**Verdict: Re-edit needed** (approved by the team, but other dealers' names are on screen)

1. 00:04-00:06. **Must fix (wrong dealer):** a hanging sign reading **"JRD Nimbus Hyundai"** (another Hyundai dealer)
   is readable behind the black Creta. Replace the shot, or blur or crop the sign.
2. 00:31. **Must fix (wrong dealer):** the pylon behind the black Creta reads **"Hyundai Promise – Certified Pre-Owned
   Car / Shivang Hyundai"**, right next to the Capital Hyundai logo. Replace the shot or blur the pylon.
3. 00:29-00:30 and 00:38. **Must fix:** the white Creta has a non-Indian (Arabic-script) number plate, so it's foreign
   stock footage. Replace it with Indian or Capital Hyundai footage.
4. 00:14-00:15. **Must fix (other brand):** the HP logo on her laptop lid is visible. Blur it or angle the laptop away.
5. 00:39-00:44. **Must fix:** the end of the call to action has no subtitles (only the number 7303111937 is on
   screen). She says "…call the number given on the screen, and Capital Hyundai will be happy to assist you". Add
   "call the number on the screen –" / "Capital Hyundai will be happy to assist you."
6. 00:00-00:02: she sits silently on her phone and the first line starts at 00:02.3. Trim about 2 s so "Looking for a
   Hyundai for your parents?" opens the reel.
7. 00:26-00:32, grammar: "because the right Hyundai for parents is the one / feels comfortable and easy in daily use
   alongside being stylish." Change to "…is the one that feels comfortable and easy in daily use, while being stylish."
8. 00:18-00:19 ("REVERSE CAMERA", "PARKING ASSISTANCE"): older Hyundai screens. Fine as general B-roll, but these
   features vary by variant, so consider "on select variants".
9. 00:44-00:47, end card: Sector 132 service centre 95600 27864 (older card, the same as CH-2610-07; the Nov reels show
   99589 94275). Ask which is current. The last two lines are in the bottom 20%.
10. Audio: true peak -0.4 dBFS, integrated -16.4 LUFS. OK, but bring the peak to -1 dBTP.

Checked and fine: the subtitles match the audio (English translation), no black frames, the end card shows for 2.8 s,
and the on-screen number 7303111937 matches the end card's Sector 132 showroom.

## 15 Nov 2026 – CH-2610-10 – Capital Hyundai Oct Reel 5.mp4 (Approved; planned Mon 23 Nov)

42 s, 1080x1920, 29.97 fps. Topic: what to check on a Hyundai test drive (driving position, steering, brakes,
dimensions, seats, rear seat, parking visibility).

**Verdict: Minor changes** (approved by the team, but problems found)

1. 00:35-00:39. **Must fix:** the end of the call to action has no subtitles (only "7303111937" is on screen). She says
   "…call on the number given on the screen, and Capital Hyundai will be happy to assist you". Add "call the number
   on the screen –" / "Capital Hyundai will be happy to assist you." (Same gap as CH-2610-09.)
2. 00:28-00:29: the B-roll is the "CRETA N Line" studio shot (badge readable) under "So if you are planning to buy a
   new Hyundai". Fine as a general shot, but it's the same clip as CH-2610-07 at 00:12, so swap it in one of the two
   reels.
3. 00:39-00:42, end card: Sector 132 service centre 95600 27864 (older card; the Nov reels show 99589 94275). Ask which
   is current. The last two lines are in the bottom 20%.
4. Audio: true peak +0.1 dBFS (integrated -15.4 LUFS). Put a limiter at -1 dBTP.

Checked and fine: no other dealer names or brand logos found (the 00:27 board only reads "Showcasing 5-star excellence
in design, gastronomy, adventure & entertainment", with no name). The hook is in the first second, the subtitles
match the audio (English translation), the red frame at 00:14 is a wipe transition, no black frames, and the end card
shows for 2.8 s.

## 15 Nov 2026 – CH-2610-11 – Capital Hyundai Oct Reel 6.mp4 (Approved; planned Wed 25 Nov)

41 s, 1080x1920, 29.97 fps. Topic: why choose Capital Hyundai as the dealership (Google reviews, four showrooms,
the process from choosing to delivery, after-sales).

Facts checked: the Google review screenshot at 00:06-00:09 ("4.7, 11,555 reviews") matches Capital Hyundai's
Sector 63 Showroom & Service Centre profile (Google Business Profile today: 4.7, 11,685 reviews), so "thousands of
Google reviews" holds. The showrooms named (Sector 63, Sector 132, Dadri, Faridabad) are right.

**Verdict: Minor changes** (approved by the team, but problems found)

1. 00:32-00:37. **Must fix:** the last two lines have no subtitles. Add "Because big decisions mean proper care." (she
   says "means", but write "mean") and "And if you're planning to buy a new Hyundai, you know where to come."
2. 00:10-00:14 and 00:32-00:36: the Capital Hyundai logo washes out against the bright white showroom (only "CAP"
   shows at 00:32). Add a soft shadow behind the logo.
3. 00:00-00:01: the hook shot is the "CRETA N Line" studio clip, also used in CH-2610-07 (00:12) and CH-2610-10
   (00:28). Open on Capital Hyundai's own showroom or a delivery shot instead.
4. 00:38-00:40, end card: Sector 132 service centre 95600 27864 (older card; the Nov reels show 99589 94275). Ask which
   is current. The last two lines are in the bottom 20%.
5. Audio: true peak 0.0 dBFS (integrated -16.1 LUFS). Put a limiter at -1 dBTP.

Checked and fine: the hook is in the first second, the other subtitles match the audio (English translation), the
"1. Service / 2. Ownership Support / 3. Future Assistance" list matches what she says, the "Welcome To The Capital
Hyundai Family" delivery banner is the client's own, no black frames, and the end card shows for 2.8 s.

## 15 Nov 2026 – CH-2611-01 – Capital Hyundai Nov Reel-2.mp4 (Approved; caption and thumbnail still pending)

32 s, 1080x1920, 30 fps. Topic: Capital Hyundai Sector 132, Noida: new cars, service and body shop in one place.

**Verdict: Minor changes** (approved by the team, but problems found)

1. 00:20-00:28. **Must fix:** the whole call to action has no subtitles. She says "So if you live or work near Noida
   Sector 132, then visit Capital Hyundai Sector 132 or you can call us." Add it in two or three lines.
2. 00:09-00:10. **Must fix (spelling):** the title reads "NOIdA SECTOr 132" (lower-case d and r). Change to "NOIDA
   SECTOR 132", or use a font without lower-case glyphs.
3. 00:15-00:17: the body-shop B-roll shows a customer's Grand i10 NIOS with plate "UP65 FU 3817" fully readable.
   Blur it.
4. 00:13-00:19: she says Sector 132 offers "body shop support for denting, painting and accident repair". Google
   lists a Capital Hyundai service centre at Sector 132, but I can't confirm a body shop there. Check with the client
   that the body-shop claim and the footage are from Sector 132.
5. Audio: integrated -20.5 LUFS, about 5-7 dB quieter than the other reels (true peak -2.7 dBFS). Raise it to about
   -14 LUFS.

Checked and fine: the hook is at 00:00 ("Want to see a new Hyundai,"), the 3-panel collage at 00:00-00:01 (the
detector's "letterbox" is the collage borders, not black bars), BAYON is spelled right on the badges, no other dealers
or brands, no black frames, the end card (Nov version, Sector 132 service 99589 94275) shows for 2.7 s, and the other
subtitles match the audio.

## 15 Nov 2026 – CH-2611-02 – Capital Hyundai Nov Reel-6.mp4 (Approved; thumbnail approved 11 Nov)

41 s, 1080x1920, 30 fps. Topic: a BAYON buyer's journey (design, cabin, test drive, delivery) at Capital Hyundai.

**Verdict: Minor changes** (approved by the team; small fixes only)

1. 00:29-00:31, **must fix (matches the audio):** "ek poori experience hai". She says "ek poora experience hai"; change
   to "poora".
2. 00:05 and 00:26: the two glitch transitions (pixel-break with doubled, mirrored Capital Hyundai logos and doubled
   subtitles at 00:26.25) read like file corruption on a phone screen. If they're intended, keep them under 0.3 s;
   otherwise use a clean cut or a whip.
3. 00:22-00:25: the Capital Hyundai logo washes out against the white ceiling. Add a soft shadow.
4. Audio: true peak +0.2 dBFS (integrated -15.1 LUFS). Put a limiter at -1 dBTP.
5. 00:38-00:41, end card: the last two service lines are in the bottom 20% (same card as the other Nov reels).

Checked and fine: the hook at 00:01 ("Main toh sirf Hyundai BAYON dekhne aayi thi…"), BAYON spelled right, every line
subtitled including the call to action ("Toh aap bhi Capital Hyundai visit kijiye / BAYON ko khud explore kijiye / aur
aaj hi apni test drive book kijiye!"), no other dealers or brands, no black frames, no dead air (00:08-00:10 is a
silent B-roll beat), and the end card shows for 2.8 s.

## Summary – 15 Nov 2026

| Video ID | Status | Verdict | Changes | Main problem |
|---|---|---|---|---|
| CH-2611-03 | Pending | Re-edit needed | 9 | Offer card expired ("Valid until 13 November 2026") and has no T&C |
| CH-2611-05 | Pending | Minor changes | 6 | Call to action not subtitled; "Hyundai Promise" spelled two ways |
| CH-2611-04 | Pending | Re-edit needed | 12 | 117 s (limit 60); "told told", "share", "call back" grammar; name to confirm |
| CH-2611-06 | Pending | Re-edit needed | 10 | Hook and CTA not subtitled; Blind-spot View Monitor shown as "360-degree camera" |
| CH-2610-07 | Approved | Minor changes | 9 | CTA not subtitled; auto hold is automatic S(O)+ only |
| CH-2610-09 | Approved | Re-edit needed | 10 | Other dealers' signs: "JRD Nimbus Hyundai" (00:04), "Shivang Hyundai" (00:31) |
| CH-2610-10 | Approved | Minor changes | 4 | CTA not subtitled |
| CH-2610-11 | Approved | Minor changes | 5 | Last two lines not subtitled |
| CH-2611-01 | Approved | Minor changes | 5 | CTA not subtitled; "NOIdA SECTOr 132" title |
| CH-2611-02 | Approved | Minor changes | 5 | "ek poori experience" should be "ek poora experience" |
