# Static post analysis (last 30 posts per account, read 8 Nov 2026)

180 posts read with the Graph API (`statics/` work is read-only so far). About half are reels; the statics are
single images (68) and carousels (21). Almost all statics are **4:5 portrait** (1080x1350; some exported at
1122x1402 or 1350x1687, same ratio). Reels covers are 9:16.

## Two kinds of static

1. **Brand (OEM) campaign creatives**: the same artwork appears on all three Hyundai dealers (and on both Mahindra
   dealers) with only the dealer logo, footer and phone swapped. Examples: the Hyundai BAYON teaser series
   ("Intelligence that moves.", "Generating soon...", sketch reveals), Hyundai Super Delight Days (Pankaj Tripathi,
   up to Rs 1 lakh benefits), the Janmashtami exchange offer, Hyundai x UEFA Champions League, Hyundai TQI;
   Mahindra XUV 3XO ZNG ("One life. Make it ZNG.", "6 shades of ZNG", "Bookings now open").
2. **Agency-made posts**, built around the dealer:
   - festival greetings (Dhanteras, Navratri/Durga, Dussehra, Gandhi Jayanti, Ganesh Chaturthi, Janmashtami,
     Raksha Bandhan): an AI-style hero image, usually the dealer's own showroom facade with brand cars, a script or
     serif "Happy <festival>", two lines of wishes, "from <Dealer>", then the normal footer;
   - lifestyle/model posts (Mahindra): AI scenes (beach, desert, mountains, monsoon) with a short witty line
     ("We like our coffee bold", "Take the path less googled", "The new OG Mahindra Thar");
   - event recap carousels (launches, MET City Half Marathon): slide counter "01 / 07", small kicker
     ("HYUNDAI BAYON"), a huge bold headline ("LAUNCH HIGHLIGHTS", "RUNNING WITH THE CITY"), one-line description,
     bottom kicker ("EVENT RECAP", "DESIGN. PRESENCE. IMPACT.");
   - milestones and people (sales awards, new service centre, welcoming an executive), customer deliveries
     ("Congratulations!", M R Hyundai), service and camps;
   - Car & Bike stock posts: car photo, price, spec chips, stock tables.

## The frame each client uses (header + footer)

| Client | Header | Footer |
|---|---|---|
| Capital Hyundai | "CAPITAL HYUNDAI" logo (H + stacked name) top-left, "HYUNDAI" wordmark top-right on OEM posts; on the BAYON series the CH logo sits top-right | (a) a thin rule "Capital Hyundai Showrooms" then 4 columns: Sector 63 Noida 99994 89444, Sector 132 Noida 73031 11937, Dadri 99903 95300, Faridabad 93559 31054; or (b) one line "CAPITAL HYUNDAI SHOWROOMS ... NOIDA \| DADRI \| FARIDABAD" |
| Dee Emm Hyundai | H + "DEE EMM HYUNDAI" stacked, top-left; some posts add a Google Maps pin + search pill "Dee Emm Hyundai" top-right | "DEE EMM HYUNDAI GURGAON" (bold caps) left + "97736 47900" right; second line "SECTOR 16 \| SECTOR 49 · DAULATABAD · SECTOR 18 \| SIKANDERPUR". Service posts: blue bar "Call us to book 97736 47900 \| Your Hyundai, Our Care" (script) |
| Mahindra Arav | Mahindra twin-peaks mark + "Mahindra ARAV" top-left; Maps pin + search pill "Arav Mahindra, Gurgaon" top-right | Left: "BOOK YOUR SUV WITH MAHINDRA ARAV TODAY" (or "...XUV 3XO ZNG...", "...E SUV..."); right: map-pin icon, "GURGAON", "Manesar, Gurgaon / Sector 95, Gurgaon / Sector 83, Gurgaon", "88600 86639". White text over the image, no solid bar |
| Dee Emm Mahindra | twin-peaks mark + "DEE EMM" top-left; Maps pin + search pill "Dee Emm Mahindra" top-right | "BOOK YOUR SUV WITH DEE EMM MAHINDRA" left + "95995 58379" right (no locations). Festival version: phone + "Sec-18 \| Sec-14 \| Sec-53 \| Sec-61 \| Daulatabad \| Pataudi" pill |
| M R Hyundai | Maps pin + search pill "M R Hyundai, Pasonda" top-left; H + "M R HYUNDAI" wordmark top-right | Left: a small CTA ("Book Your Hyundai Bayon", "Visit Us This Festive Season"); right: map-pin icon, "GHAZIABAD / Pasonda, Shalimar Garden", "93128 21182", on a blue bar or over the image. Delivery posts: own frame ("DRIVEN BY PEOPLE, BUILT ON TRUST", address "Loni Rd, opp. Shalimar Garden, Pasonda, Sahibabad, Ghaziabad, UP 201005", icon row, "DRIVE A BETTER TOMORROW") |
| Car & Bike | car&bike logo (yellow "PRE-OWNED CARS" tag) top-centre or top-right | Black bar: phone icon "Call for Inquiry 98185 64808" \| pin "Visit Us Sector 18, Gurgaon" \| "MORE CARS BRIGHTER LIVES"; stock posts end with a yellow pill "Call: 98185 64808" |

Mahindra Arav's corporate posts (service centre, milestones, people) use a second frame: dark background with red
diagonal accents, "ARAV MAHINDRA GURGAON" top-left, "DRIVEN BY SERVICE \| BUILT FOR A BETTER TOMORROW" top-right,
three pillar icons (Expert Care, Customer First, A Greener Tomorrow) and "SERVICE \| PEOPLE \| A GREENER TOMORROW"
along the bottom.

## Look and type

- **Hyundai dealers**: Hyundai's own sans (Hyundai Sans Head/Text style), white or dark backgrounds, BAYON series in
  black and red, offers in the OEM pink-purple sky template, service in Hyundai blue. Headlines short, sentence case,
  often ending in a period ("BAYON.", "Intelligence that moves.").
- **Mahindra dealers**: bold condensed caps for headlines (Anton/Bebas-like), Mahindra's techno model lettering
  ("X U V  3 X O  Z N G" with wide letter spacing), saturated AI scenery, gold or red accents on dark for events.
- **Car & Bike**: its own brand, black + yellow (#FFD400-like), heavy condensed caps in white and yellow, icon chips
  (Genuine Cars, Warranty, All Brand Cars, Easy Finance), a strip of make logos (Maruti Suzuki, Kia, Toyota, Hyundai,
  Mahindra, Honda), and a black-and-yellow showroom render. Stock carousels: 1 hero + price + "Negotiable",
  2 "Quick Details" spec list, 3 exterior grid (Bold front, Rear view, ORVM, Wheel detail), 4 interior.
- Festival posts for every client: warm gold light, script or serif headline, the dealer's showroom rendered in the
  scene, diyas/marigolds/rangoli for Diwali-season festivals, tricolour for national days.
- Fine print sits at the very bottom in tiny text: "Type approval certificate is applied for", "Image used for
  creative representation only", "T&C apply", "Prices may vary...".

## Inconsistencies found (to settle before automating)

- Capital Hyundai's Dadri number appears three ways: 99903 95300 (static footers), 72900 77273 (captions and reel
  end card), 072900 77380 (one BAYON post).
- Car & Bike's phone changed over time: 93193 95919 (Apr-May), 93193 95919 / 92667 30851 (June), 98185 64808 now; the
  April-May posts also carried a Dee Emm logo.
- Dee Emm Hyundai's camp post used 93112 29480 (camp-specific), Arav's Gandhi Jayanti post skipped the footer.
- Dee Emm Mahindra's everyday footer has no locations; the festival footer has six.

## What automation of statics needs

- Each client's logo as a transparent PNG (light and dark versions), and the fonts (Hyundai Sans if licensed).
- One approved contact block per client (numbers, locations, map search name).
- A template per client = header + footer frame (above) + a content area, in three layouts: OEM creative drop-in,
  festival greeting, event/milestone carousel; plus Car & Bike stock posts fed from a stock sheet.
- Source of content: OEM creatives (Drive folder), event photos, stock data, festival calendar.
