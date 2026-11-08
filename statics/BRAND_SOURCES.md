# Brand sources for static posts (read 8 Nov 2026)

The brand Facebook pages cannot be read from here: Facebook needs a login on the web, and its API needs the
"Page Public Content Access" feature, which this app does not have. The same content is on the brands' Instagram
business accounts, which our Instagram access can read (business discovery, public data only):

| Account | Followers | What it posts |
|---|---|---|
| @hyundaiindia | 2.1M | BAYON launch and "First Drive" day-by-day recaps (reels + carousels), festival and pop-culture posts (SRK birthday, Halloween "Devilishly Stunning."), CSR (Art for Hope, Innovation Challenge), city events. Clean layouts, white or black, HYUNDAI wordmark bottom-right. |
| @mahindra_auto | 347K | Premium cinematic AI-style scenes, big serif/spaced titles ("THE DRIVE / THE DETOUR / THE DIWALI" series), witty lines ("We like our coffee bold", "Take the path less googled", "Some experiences don't need AI"), mahindra wordmark top-right, twin-peaks mark top-left with a red diagonal line. |
| @mahindraelectricsuvs | 250K | BE 6 / XEV 9e / XEV 9S, Charge_iN network maps, "1 lakh eSUVs" milestone, owner stories, illustrated festival posts, feature explainers (NFC key, scheduled charging, tailgate). |
| @mahindrathar | 522K | Thar OG launch (C-shaped DRLs, ELD, interiors), Thar ROXX festive, dark moody night scenes, THAR OG badge bottom-right. |
| @mahindraxuv3xo | 127K | XUV 3XO ZNG campaign: countdown posts ("3/2/1 DAYS TO GO"), "Bookings open", "Choose your ZNG energy", 5-star BNCAP CNG, Gen-Z wordplay ("ZNNNNG", "MAXX-INNNG"), beach/palm-tree look in bright blue and orange. |
| @mahindrapickups | 45K | Commercial range in Hinglish: Veero (CNG 1.1 XXL, comfort features), Maxx Pik-Up City ("Har city route ka MAXX profit partner"), iMAXX telematics (driver score, remote AC), festival posts with the whole pickup line-up, "Soch Se Aage" tagline. |

XUV 7XO, Scorpio and Bolero have no separate Instagram business account; their posts are on @mahindra_auto.

## Current line-ups and starting prices (ex-showroom, from the brand websites, 8 Nov 2026)

**Mahindra SUVs**: XUV 3XO Rs 7.79-15.04L · Thar OG Rs 10.32-18.99L · Scorpio-N Rs 13.69-25.49L · XUV 7XO Rs 13.99-25.94L ·
Thar ROXX Rs 12.52-23.52L · Scorpio Classic Rs 13.43-17.48L · Bolero Neo Rs 9.06-10.85L · Bolero Rs 8.57-9.99L ·
Bolero Neo Plus Rs 11.46-13.56L · XUV400 Rs 17.49L · XUV 3XO EV Rs 13.89-14.96L. eSUVs (BE 6, XEV 9e, XEV 9S) are
on a separate tab.

**Mahindra commercial (Mahindra Arav only)**: Bolero Camper Rs 10.10-11.01L · Bolero Pik-Up Rs 9.35-10.49L ·
Veero Rs 8.25-9.50L · Maxx HD Rs 9.63-11.21L · Maxx City Rs 8.11-8.91L (the site also lists Jeeto, Supro, Treo,
Zor Grand without prices).

**Hyundai** (starting at): Grand i10 Nios Rs 5,59,700 · Exter Rs 5,80,600 (Hy-CNG Duo EX Rs 7,50,700) · Aura
Rs 5,99,990 · i20 Rs 5,99,700 · i20 N Line Rs 9,32,200 · Venue Rs 7,99,900 · Venue N Line Rs 10,66,100 · BAYON
Rs 9,99,900 · Creta Rs 10,90,700 · Verna Rs 10,99,200 · Alcazar Rs 14,50,700 · Creta Electric Rs 18,02,800 · Creta
N Line Rs 19,03,300 · IONIQ 5 Rs 55,70,600 · Prime HB/SD (taxi) Rs 6,40,600 / 7,00,600.

Prices change; re-read the sites before using a price in a post, and label it "ex-showroom, T&C apply".

## Rules the user set for statics

- Capital Hyundai Dadri number: 072900 77380.
- Footer numbers follow the post's topic (user, 8 Nov 2026): a service post (service review, service tip, camp)
  shows the service centre numbers, a showroom/sales post shows the showroom numbers, a general post shows both.
  Service numbers per client are in `statics/clients.json` ("service"); use only ones marked confirmed.
- Dee Emm Mahindra logo depends on the topic (user, 8 Nov 2026): a post or review about EVs (BE 6, XEV 9e, XEV 9S,
  XUV 3XO EV, XUV400, charging) uses the EV logo (white loop mark); everything else, i.e. petrol/diesel/CNG cars,
  service, insurance, uses the twin-peaks "DEE EMM MAHINDRA, SERVING GURGAON SINCE 2019" logo (white version on dark
  backgrounds, black on light). File ids are in `statics/clients.json`.
- Car & Bike phone: 98185 64808; the Dee Emm logo may sit alongside the car&bike logo.
- Dee Emm Mahindra: everyday footer (CTA + phone); add its six locations only when they fit cleanly.
- Mahindra Arav sells personal SUVs and commercial **pickups only** (Bolero Pik-Up, Bolero Camper, Maxx City, Maxx HD,
  Veero), not the small range (Jeeto, Supro, Treo, Zor Grand). No other client sells commercial vehicles, so pickup
  posts go only to Mahindra Arav.
- Informative EMI posts can be location-specific: e.g. an EMI breakdown for Noida on Capital Hyundai, Ghaziabad on
  M R Hyundai, Gurgaon on the Gurgaon dealers.
- Car & Bike posts are designed from the list of available cars the user will provide.
- EMI and on-road numbers come from CarDekho's city price pages (`scripts/emi.py`), labelled indicative.

## Posting rhythm (user, 8 Nov 2026)

- Something goes out on each client's feed **every second day**.
- Default cycle: **2 videos, then 1 static**, repeating (V, V, S, V, V, S ...).
- It is a guide, not a rule: when there are fewer videos, fill the alternate days with statics (or post less often);
  festivals and launches take their own date.
