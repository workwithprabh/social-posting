# Content buckets for static posts

Agreed 8 Nov 2026. Car & Bike is planned separately from its stock list. Videos come from the team; these buckets
are for statics. Rhythm: a post every second day per client, cycling 2 videos then 1 static (see
`BRAND_SOURCES.md`), so about 5 statics per client per month.

| # | Bucket | What it covers | Source |
|---|---|---|---|
| 1 | Model spotlight | a feature, variant, colour or safety rating | brand websites, brand Instagram pages |
| 2 | Money & ownership | EMI by city, on-road breakdown, CNG vs petrol running cost, exchange/scrappage, loan documents | `scripts/emi.py` (CarDekho), brand sites |
| 3 | Customer love | 5-star Google reviews, deliveries ("Welcome to the family"), owner milestones | Reviews tab (Google Business Profile), delivery photos |
| 4 | Offers & launches | bookings open, countdowns, festive/monthly offers | only offers confirmed by the team or the brand |
| 5 | Festivals & moments | festivals, national days, topical moments | festival calendar |
| 6 | Service & care | service tips, camps, genuine parts, warranty, service centres | brand sites, team |
| 7 | Dealership & people | events, awards, milestones, team, new outlets | event photos from the team |
| 8 | Engagement | this-or-that, myth vs fact, which colour, quizzes | brand info |
| 9 | Pickups (Mahindra Arav only) | Bolero Pik-Up, Bolero Camper, Maxx City, Maxx HD, Veero; earnings/business angle, Hinglish | auto.mahindra.com, @mahindrapickups |

## Monthly mix per client (about 5 statics)

1. Model spotlight
2. Money & ownership
3. Customer love
4. Festivals & moments, or Offers & launches (whichever is due)
5. Rotating: Service & care / Dealership & people / Engagement

Mahindra Arav swaps one of these for a Pickups post each month.

## Emphasis per client

- **Capital Hyundai**: English, advisory; comparisons; EMI for Noida, Faridabad, Dadri.
- **M R Hyundai**: service and care (their strongest theme), Ghaziabad EMI, deliveries.
- **Dee Emm Hyundai**: BAYON and models, service and camps, Gurgaon EMI.
- **Dee Emm Mahindra**: XUV 3XO ZNG, eSUVs, events.
- **Mahindra Arav**: SUVs and pickups, Gurgaon/Manesar EMI.

## Rules

- No invented facts: prices, specs and offers come from the brand sites, CarDekho or the team, marked
  "ex-showroom" or "indicative on-road", "T&C apply", and rechecked before posting.
- Brand fence: each client posts only its own brand; pickups only on Mahindra Arav.
- When dealers of the same brand cover the same moment, each gets its own headline and image.
- Google reviews: pick meaningful, longer reviews (25+ words, at most 500 characters) that name staff or describe
  the delivery/service; skip generic product essays and pasted-looking templates. First name + last initial only
  (digits and "ji" dropped), no profile photo.
- Review English (user, 8 Nov 2026): whatever goes on social media must be correct English. Customers often write
  in broken English, so column M "Text for post" is either the review with its grammar corrected, or the review
  rephrased in our words. Keep the customer's meaning and facts: the staff names, car, branch and what happened,
  nothing added (no new praise, claims or numbers). Column G keeps the original text untouched, and Notes says
  "Grammar corrected" or "Rephrased" (with the main changes). Poor English is no longer a reason to skip a good
  review; a Hinglish review may be translated into English (Notes: "Translated from Hinglish"). On a card, quote marks hold column M exactly; shorten only by cutting whole sentences.

## Sheet tabs

- **Calendar**: Date, Day (auto), Client, Format (Video / Static / Carousel), Bucket, Topic, Video ID / asset,
  Brief and source, Status (Planned / Drafted / Approved / Posted / Skipped), Post link, Notes.
- **Reviews**: Review ID, Client, Location, Stars, Reviewer (on Google), Name for post, Review text, Review date,
  Google link, Use? (New / Use / No / Used), Posted on, Notes, Text for post. Filled by `scripts/gbp_reviews.py`; the team sets
  "Use" on the ones to design.

## Where reviews come from

- **Dee Emm Hyundai**: the "DMU GBP Intelligence & Review Audit" sheet (`1r9c4Bhjsya3kDnBbUldHnZyeg-0T30tP3hPaJpI_3p4`,
  tab Reviews_Raw), filled every 3 hours by the GitHub job in `deeemm-hyundai-lp`. Read-only for us: that job posts
  automatic replies signed "Team Dee Emm Hyundai", so never add other dealers to its Locations tab. The daily sync
  copies new qualifying 5-star reviews (max 3 per branch per day) into the tracker's Reviews tab;
  `scripts/dmu_reviews.py` lists candidates from a CSV export. First backfill (8 Nov 2026): 18 hand-checked reviews
  from the last 60 days.
- **Other clients**: `scripts/gbp_reviews.py reviews --since <date>` (GBP OAuth credentials are in the environment; the
  account sees every Capital Hyundai, M R Hyundai, Mahindra Arav and Dee Emm Mahindra listing, none for Car & Bike).
  Skip its Dee Emm Hyundai rows: those come from the DMU sheet. First backfill (8 Nov 2026): 38 hand-checked reviews
  from the last 60 days (Capital Hyundai 27, Dee Emm Mahindra 8, Mahindra Arav 2, M R Hyundai 1).
  Same day, under the correct-English rule: 24 more that had been skipped for their English (Capital Hyundai 20,
  Dee Emm Mahindra 4; 12 grammar corrected, 9 rephrased, 3 translated from Hinglish).
