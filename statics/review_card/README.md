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
- M R Hyundai (MRH-FST-2611-01, `gurpurab4.html`, 24 Nov 2026): night design. Full-bleed night photo of Gurdwara Bangla Sahib and its sarovar (Ken Wieland, CC BY-SA 2.0, Wikimedia Commons, 3840 px thumb, cropped to 2304x2880 centred on the dome, midtones lifted and slightly warmed, then shown at `bs` 128% so the building fills the middle), white logo centred at the top (88 px, 20% under the usual 110), the wish in the dark sky, the teaching (Naam Japo) over the water, thin gold frame, showroom & service footer. No AI.
