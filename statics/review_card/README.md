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
mkdir -p out && node render.js            # or: node render.js CH-REV-2611-01
```

Photo layouts (user liked them, 8 Nov 2026): a single customer standing clear of the background gets a cutout
(`"cut"`, optional `"cutH"` height); a group or key-handover photo gets a tilted photo print (`"frame":
"frame_<ID>.jpg"`), because cutting a car out from behind several people leaves pieces. The cutout models keep
only people, so whenever the car matters (deliveries), use the photo print so the car stays in the picture (user,
8 Nov 2026: a lone cutout of the customer without the car looked empty). Pixelate every readable plate,
including parked cars. `"h1W"` limits the headline width when a tall cutout needs the space.
Search all locations for candidates: 5-star reviews with photos where the customer is in the frame, then add them to
the Reviews tab with Photo OK? = Ask.

Photo layout: add `"cut": "cut_<ID>.png" to a card and the quote narrows to the left while the customer cutout
stands on the right, bleeding off the edge (sample: CH-REV-2611-03-SAMPLE, Sumit G.). Make the cutout with
`python cutout.py photo.jpg cut_<ID>.png --plate ... --crop-right ...` from the review's full-size photo (column N
of the Reviews tab). Only when "Photo OK?" is Yes.

Edit `cards.json` for each batch (`theme` hyundai/mahindra, `logo` and `logoH` (logo height, sizes in
`statics/BRAND_SOURCES.md`), `headline`, `quote`, `name`, `place`, `footer`
CH/DEH/MRH/DEM/AM for showroom posts, CH_SVC/DEM_SVC/AM_SVC for service posts). IDs are `<client>-REV-<YYMM>-<nn>`; drafts go to the "Claude drafts" Drive folder and a
Calendar row (Bucket "Customer love", Status "Drafted", caption draft in "Brief and source").
First batch (8 Nov 2026): CH-REV-2611-01/02, DEH-, MRH-, DEM-, AM-REV-2611-01.
