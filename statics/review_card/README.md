# Review cards (Customer love statics)

4:5 (1080x1350) cards that quote a Google review: client logo, five stars, "CUSTOMER LOVE", a short headline in our
words, the quote (column M of the Reviews tab, whole sentences only), first name + last initial, branch, and the
client's usual footer from `statics/FEED_ANALYSIS.md`. Hyundai clients use the navy theme, Mahindra clients the
charcoal-and-red theme with Anton headlines. The quote font shrinks to fit (58px down to 26px).

Build in a scratch folder, never inside the repo:

```
cp card.html render.js cards.json fetch_logos.py <scratch>/ && cd <scratch>
npm i -s @fontsource/anton@5.3.0 @fontsource/montserrat@5.3.0 @fontsource/playfair-display@5.2.8
python <repo>/statics/review_card/fetch_logos.py
mkdir -p out && node render.js && python save.py out    # or: node render.js CH-REV-2611-01
```

Resolution (user, 8 Nov 2026: files must look good on Instagram and Facebook): cards render at 2x, 2160x2700, and
`save.py` stores them as JPEG quality 95 with 4:4:4 chroma (no colour bleed on red/blue text). That file goes to
Drive and is what Facebook gets. For Instagram, `python save.py out --ig` (or a resize at publish time) makes an exact
1080x1350 copy, Instagram's native 4:5 size, so Instagram doesn't resize it again. Use only the `_hr` logos
(fetch_logos.py builds them); photos in prints or cutouts should be at least ~900px wide.

Photo layouts (user liked them, 8 Nov 2026): a single customer standing clear of the background gets a cutout
(`"cut"`, optional `"cutH"` height); a group or key-handover photo gets a tilted photo print (`"frame":
"frame_<ID>.jpg"`), because cutting a car out from behind several people leaves pieces. The cutout models keep
only people, so whenever the car matters (deliveries), use the photo print so the car stays in the picture (user,
8 Nov 2026: a lone cutout of the customer without the car looked empty). Pixelate every readable plate,
including parked cars. `"h1W"` limits the headline width when a tall cutout needs the space.
Search all locations for candidates: 5-star reviews with photos where the customer is in the frame, then add them to
the Reviews tab (Customer in photo? = Yes).

Photo layout: add `"cut": "cut_<ID>.png" to a card and the quote narrows to the left while the customer cutout
stands on the right, bleeding off the edge (sample: CH-REV-2611-03-SAMPLE, Sumit G.). Make the cutout with
`python cutout.py photo.jpg cut_<ID>.png --plate ... --crop-right ...` from the review's full-size photo (column N
of the Reviews tab).

Edit `cards.json` for each batch (`theme` hyundai/mahindra, `logo` and `logoH` (logo height, sizes in
`statics/BRAND_SOURCES.md`), `headline`, `quote`, `name`, `place`, `footer`
CH/DEH/MRH/DEM/AM for showroom posts, CH_SVC/DEM_SVC/AM_SVC for service posts). IDs are `<client>-REV-<YYMM>-<nn>`; drafts go to the "Claude drafts" Drive folder and a
Calendar row (Bucket "Customer love", Status "Drafted", caption draft in "Brief and source").
First batch (8 Nov 2026): CH-REV-2611-01/02, DEH-, MRH-, DEM-, AM-REV-2611-01.

## Model spotlight (brand) posts: `spotlight.html` (9 Nov 2026)
`node render_spot.js [ID]` renders `cards_spot.json` (theme `hyundai` = Hyundai Blue #002C5F with Active Blue #00AAD2, `mahindra` = Anton caps
and red; user, 9 Nov 2026: black and red is wrong for Hyundai) with the same header logos and footers as the review cards, then `python save.py out/`. Each card: car photo
(`img`, cropped clean from the brand's Instagram creative or website, no OEM text left in), kicker, headline, sub,
three feature chips, price pill, fine print. Facts and prices come only from the brand's own posts or website,
marked ex-showroom with T&C. The three Hyundai dealers take different angles of the same model (AI ON / Safety ON /
Performance ON) so their feeds don't repeat each other.

## EMI guide posts: `emi.html` (9 Nov 2026)
`node render_emi.js [ID]` renders `cards_emi.json`: car photo, "<Model> in <City>?" headline, a breakdown table
(ex-showroom, registration, insurance, other charges, on-road) and an EMI box. Numbers come from
`scripts/emi.py` (CarDekho's base-variant block for that city, optional accessories left out; 10% down, 9.8% p.a.,
60 months), and the fine print says they are indicative, dated and lender-dependent. Each dealer gets its own city
and a different model where possible.

Hyundai photos shot on black are lifted to Hyundai blue (`.hyundai .car::after`, mix-blend lighten) so they sit in the blue background.

## Hyundai posts: `hyundai.html` (9 Nov 2026, replaces the `hyundai` blue theme)
`node render_hy.js [ID]` renders `cards_hy.json`; `mode` dark / light / photo (with `ink` white or navy), `kind` spot
or emi. Light posts use the Hyundai Blue logos (`*_blue_hr.png`, the white logos recoloured). Modelled on
@hyundaiindia: the user rejected both black-and-red (too close to the Mahindra posts) and an all-blue gradient.

## Posting statics: `scripts/publish_static.py` (first used 9 Nov 2026)
Posts one image to the Facebook Page (2160x2700 master) and Instagram (a 1080x1350 copy). Instagram needs a public
image link, so the copy goes up to the Page as an unpublished photo, its CDN link is passed to Instagram, and the
helper photo is deleted. Same tokens as reels (`--system-user` for CH, DEH, AM, CB; `META_PAGE_TOKEN_MRH` /
`META_PAGE_TOKEN_DEM` without it). Page and Instagram ids are in `config/boost.json`. Before posting: check image,
caption and footer belong together, post only the text after "Caption draft:", then set Statics Status to Posted and
the review's Use? to Used with the date in the Reviews tab.

## Reel covers in the static look: `reelcover.html`, `reelcover_hy.html` (15 Nov 2026)
`node render_reel.js [ID]` renders `cards_reel.json` to `out_reel/<ID>.png` at 1080x1920 (save as JPEG q95 4:4:4).
Cards with `theme` mahindra or carbike use `reelcover.html` (the spotlight look: tag pill, kicker, Anton headline with
an `<em>` accent word, sub, red or gold fact pill, three chips); cards with `mode` (dark) use `reelcover_hy.html` (the
Hyundai look: tag, Active Blue label, sentence-case headline, big fact line, outline pills). No logo, no footer.
`img` is a full-width crop of the reel's own frame (subtitles and watermarks removed, graded brighter); `vars` move
the parts (`ht` head top, `ct`/`ch` picture top/height, `pt` pill top, `chipt`/`pl` chips top, `h1` size). Keep the
headline, picture subject, pill and chips between y 240 and 1680, the 3:4 area the profile grid shows. Facts on the
cover come only from the reel. First set: DEM-2611-02, DEM-2611-04, CB-2611-04, MRH-2611-03.

## Festival greetings: `greeting.html` (21 Nov 2026)
`node render_greet.js [ID]` renders `cards_greet.json` at 2160x2700, then `python save.py out_greet/`. One layout,
three themes: `hyundai` (sentence case, Active Blue label), `mahindra` (Anton caps, red label), `carbike` (black, lime;
logo `CB_logo.png` cut from the reel end card, since the Drive logo files aren't link-shared). Drawn in code (bokeh,
diyas, a gold Ik Onkar in Noto Serif Gurmukhi: `npm i -s @fontsource/noto-serif-gurmukhi@5.2.5`); no AI and no
depiction of religious figures. Mahindra footers read "WARM WISHES FROM ..." instead of the sales CTA. First use:
Guru Nanak Jayanti, `<client>-FST-2611-xx`.
**On hold (user, 21 Nov 2026): don't use one design for every client.** Festival greetings get a different design per
client, built from references the user sends; this shared template was a first draft and is not to be posted.

## Gurpurab posts, one design per client: `gurpurab.html` (24 Nov 2026)
`node render_gurpurab.js [ID]` renders `cards_gurpurab.json` at 2160x2700, then `python save.py out_gp/`. The user
asked (24 Nov 2026) for a different post per client, each with a lesson of Guru Nanak Dev Ji, a wish, a Guru Nanak or
gurdwara visual and the client's branding. First design (Capital Hyundai): night photo of Sri Harmandir Sahib with its
reflection (Sasha India, CC BY-SA 2.0, Wikimedia Commons: credit it on the image), "Happy Gurpurab" with the Punjabi
wish, then the teaching in Gurmukhi (Noto Serif Gurmukhi), its name in Playfair italic, its meaning and one line tying
it to everyday life; no sales message. Lessons are kept different per client (Kirat Karo, Vand Chhako, Naam Japo,
Ek Onkar, Sarbat da bhala / seva, truthful living). Canva's generate-image made full posters with text when asked
for a background, so it isn't used for this.

- Dee Emm Hyundai (DEH-FST-2611-01, `gurpurab3.html`, user 24 Nov 2026: no gurdwara, Guru Nanak illustration and Hyundai cars at the bottom, front faces, new photos from the website): ivory and saffron, the illustration in an arch on a gold glow (`ill`), Ik Onkar crest and mandala in code, a `cars` row of straight-on front views of the BAYON, Creta and Venue (user: BAYON instead of Exter; side cars about the Creta's size, scale 0.64-0.65 against the Creta's 0.62, since the Venue looked too small). Car photos: hyundai.com/in's 360 viewer, transparent PNGs with the real studio shadow, `https://www.hyundai.com/content/dam/hyundai/in/en/data/find-a-car/<Model>/360/<colour>/pc/<colour>_<n>.png` (1120x425 is the largest; n 1-35; the straight front is frame 8 for Creta, Venue and BAYON and frame 9 for Exter; Alcazar and Verna are angled at 8). Upscale 2x with Lanczos and a light unsharp mask, then place every car on one floor line measured from its tyre bottom (lowest row with alpha above 240). Images the card needs (gn_cut_clean.png, car_*.png, logos) live in the build folder, not the repo.
- M R Hyundai (MRH-FST-2611-01, `gurpurab4.html`, 24 Nov 2026): night design. Full-bleed night photo of Gurdwara Bangla Sahib and its sarovar (Ken Wieland, CC BY-SA 2.0, Wikimedia Commons, 3840 px thumb, cropped to 2304x2880 centred on the dome, midtones lifted and slightly warmed, then shown at `bs` 128% so the building fills the middle), white logo centred at the top (88 px, 20% under the usual 110), the wish in the dark sky, the teaching (Naam Japo) over the water, thin gold frame, showroom & service footer. Version 2 (user: "Guru nanak is missing"): the Guru Nanak Dev Ji illustration (`fig`, AI, Canva) rises above the gurdwara in a gold glow with rays, and the gurdwara sits in front of him through `fg`, a copy of the photo with a skyline matte (per column, everything below the first run of 8 pixels brighter than 38 is opaque, median 5, blur 2: mrh_night_fg.png). `veilb` darkens the water again above that layer, the figure fades at the bottom (`m1`/`m2`) and on the right edge where the illustration cuts the shawl off (`r1`/`r2`), and the wish moves down to the water with the teaching (`wishBelow`). Logo top left.
- Arav Mahindra (AM-FST-2611-02, `gurpurab5.html`, 24 Nov 2026): Mahindra red design. Anton caps on deep Mahindra red, the Guru Nanak Dev Ji illustration (`fig`) large on the right in a warm glow with rays, a tilted white photo card of Gurdwara Janam Asthan, Nankana Sahib (his birthplace; Shahzaib Damn Cruze, CC BY-SA 4.0; the overhead wire was removed by fitting its curve on each side of the right dome and inpainting a thin band, with a wire-only mask over the dome), the teaching Ik Onkar with outline chips, charcoal footer with a red call pill. White logo 67 px (20% under the usual 84). `render_gurpurab.js` now also loads Anton.
- Dee Emm Mahindra (DEM-FST-2611-01, `gurpurab6.html`, 24 Nov 2026): full photo + portrait card. The first version (Kartarpur photo cut by a diagonal, Guru Ji as a cut-out on charcoal) was rejected: "this cutout style is not looking good". Now the photo of Gurdwara Darbar Sahib, Kartarpur (Shahzaib Damn Cruze, CC BY-SA 4.0, 3840 px thumb cropped to 4:5 with the gurdwara right of centre so its spire stays clear of the headline) fills the post; the Anton wish sits over the sky on the left; the Guru Nanak Dev Ji illustration is shown inside a gold-framed portrait card on its own warm sunburst background (not cut out on the photo; fit it so the palm with ੴ shows); red label naming the gurdwara and the teaching Sewa over the darkened marble; twin-peaks white logo 86 px; footer with the six locations and the phone. Rejected for this post: the Janamsakhi Sacha Sauda paintings (unclothed ascetics), a 19th-century painting of Guru Nanak with a tilak (may offend), and a langar photo (conflicting credit, identifiable people).
- Car & Bike (CB-FST-2611-01, `gurpurab7.html`, 24 Nov 2026): black and gold. The Guru Nanak Dev Ji illustration gradient-mapped to a gold tone (`gn_gold.png`: luminance mapped black > bronze > gold > cream, 15% of the original colour kept) blending into the black on the right, Playfair italic gold wish on the left, the teaching Sach with Guru Nanak Dev Ji's words "Truth is high, but higher still is truthful living.", a night photo of Sri Harmandir Sahib (Sasha India, CC BY-SA 2.0) across the bottom with a dark `shade` so the place name and credit read over the reflections. car&bike logo 51 px (20% under 64). Caption in English, no emojis (Car & Bike style).

## Capital Hyundai house style v2 (`ch2.html`, 25 Nov 2026)

Client feedback (via the user, 25 Nov 2026): the Capital posts looked "too AI"; the Google reviews did not look like
Google reviews; they want a designer's look, simple but unique and unlike other Hyundai posts, and EMI shown per day
("own a Creta for about ₹800 a day"). What makes posts read as AI and is now avoided: glows, hazy gradients, glass
panels, cinematic smoke. The v2 look: flat warm paper (#F2EEE6) with a fine grain, Hyundai navy (#0B2A55), one yellow
marker highlight (#FFE14D) as the signature, Bricolage Grotesque headlines, Inter for text, Caveat for handwritten notes
and arrows, the navy Hyundai logo. Cards in `cards_ch2.json`, `node render_ch2.js [ID]` -> `out_ch2/`.
Fonts: `npm install @fontsource/bricolage-grotesque @fontsource/inter @fontsource/roboto @fontsource/caveat`.

- `review`: a pull quote from the review as the headline with the key words highlighted; the review itself as a Google
  review card (Google G, avatar initial, five stars, Roboto, the customer's own words verbatim, key phrases marked);
  a handwritten thank-you to the staff the customer named. Keep the review text exactly as on Google (no rewriting:
  it is shown like a screenshot), only the highlights are ours; the name is the tracker's "Name for post".
- `emiday`: "Own a Creta for ₹797 a day*": monthly EMI × 12 ÷ 365, rounded up so the post never understates it,
  with the working typeset as a small table ("How we worked it out": EMI a month, × 12 months, ÷ 365 days, A day;
  Inter with tabular figures; the user, 26 Nov 2026, found the handwritten working "childish"; `calc` is a list of
  [label, value] rows, the last one is the result), the on-road price, down payment, tenure and rate, a comment-EMI pill and
  the assumptions in the fine print.
- `spec`: the model name set huge behind the car, the car (hyundai.com/in 360-viewer studio PNG with its own shadow)
  over its lower part, two handwritten callouts with arrows to real parts (headlamps, alloys), headline and chips.

- `sheet` (v3 for the Creta King and Verna posts, user 25 Nov 2026: "build it in some other way"): a designer's spec sheet.
  The Hyundai tagline as the headline with the last word marked, a pure side view (hyundai.com/in 360 frame 34, front
  to the left) drawn like a technical drawing: dashed extension lines, a length dimension under the car and a height
  dimension beside it with the official figures, numbered navy markers on real parts (`pts`, in 1120-px frame units),
  a three-column numbered legend, one line of further specs, a "Book your test drive at Capital Hyundai" pill. No
  "Spec sheet 01/02" label (user, 25 Nov 2026: not required on the creative).
  Every figure is from the model's page on hyundai.com/in (Creta 4,330 x 1,790 x 1,635 mm, 50 L, R18 alloys, quad-beam
  LED headlamps, dashcam, King and King Knight trims; Verna 4,565 x 1,765 x 1,475 mm, 45 L, 7 airbags, Bose 8 speakers,
  dual 10.25-inch displays, R16 alloys, dual LED projector headlamps, rear spoiler). No power or torque figures: the
  pages don't list them. Cards CH-BRD-2611-02s and -03s.

User feedback, 25 Nov 2026 (second and third rounds): logo 10% smaller (63 px, was 70); EMI headline says "Own a
Creta from **Capital Hyundai** for" with "Capital Hyundai" set 22% larger. Review posts carry no "Straight from our
Google reviews" line (the user: don't write it; the card's G logo is enough), so `kicker` is empty. A Hyundai-style
parametric jewel texture (`pattern: true`) was tried behind the car posts and taken off again so every post, reviews
included, sits on the same plain paper; the option stays in the template, off by default.
