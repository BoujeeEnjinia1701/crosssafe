---
doc_id: CRS-MKT-001
title: CrossSafe market and viability
project: CrossSafe
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "First market and viability note (kit 1.9.1 upgrade); prices cited with the date checked; unknowns marked to assess"
---

# CrossSafe market and viability

CrossSafe would serve road authorities, schools and market associations that need a pedestrian-activated warning at an unsignalized crossing without a mains connection; a complete commercial RRFB system costs about $22,250 installed (Carmanah, citing a 2013 TRB report), against about $364 in parts for one open assembly, which is not a like-for-like price because installation, engineering, approval and warranty are not in the $364. An open design matters because a closed commercial beacon is hard to repair and to adapt to local rules. Method: STANDARDS section 23.

*Table 1. Market segments.*

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Road authorities with no budget for a signal | Small cities and towns, mostly United States first | Complete RRFB system, installed: $22,250 average (TRB 2013 as quoted by [Carmanah](https://carmanah.com/articles/overview-rrfb-cost-effectiveness/), page modified 2024-10-30, checked 2026-10-31) | 364.00 parts per assembly (BOM); 728.00 per crossing; installation and approval not included | Repairable, open, off-grid; two assemblies a crossing |
| Schools and parent groups buying through the authority | School zones | Volunteer pedestrian flags in holders (Kirkland, Washington programme; no price given, to assess; [Kirkland Public Works](https://kirklandwa.gov/depart/Public_Works/Transportation_and_Traffic/Pedestrian_Flags.htm), checked 2026-10-31) | About 70 for option C (estimate) | A cheap tier (option C) for crossings with no funds |
| Markets and bus stops in lower-income regions | Peri-urban roads, off-grid | Solar road studs for consumers: GBP 84.88 including VAT for a pack of four, 0.8 W, rated IP68, no traffic load rating stated ([BLT Direct](https://www.bltdirect.com/products/uniled-solar-led-road-stud-white-4-pack?cat=8779), checked 2026-10-31) | About 400 for option B (estimate) | An alternative form where overhead signs are stolen |
| Makerspaces, universities, NGOs building their own | Worldwide | None found; to assess | Parts only | A documented build and open files |

## Open route

Workshops, makerspaces, universities and NGOs could build the made parts from stock sections with ordinary tools (PR-019, CRS-BLD-001) and buy the electronics from catalogues. It spreads through the repo, a build plan and a pilot partner (CRS-DEC-001). Hardware is CERN-OHL-S-2.0 and software MIT, so improvements stay open. A road authority must approve each use, and no use on a public road is proposed here.

Viability: the cost target is not yet met ($14.00 over), no evidence of effect exists for this device (the FHWA figures are for commercial RRFBs), and the market size is not estimated (to assess). The pitch fits the lab's smart cities area.

## Sources

- Carmanah, "Overview: RRFB cost effectiveness", https://carmanah.com/articles/overview-rrfb-cost-effectiveness/, published 2019-10-07, modified 2024-10-30, checked 2026-10-31. The figure of $22,250 is attributed to TRB, Costs for Pedestrian and Bicyclist Infrastructure Improvements, 2013.
- BLT Direct, solar LED road stud 4 pack, UNILED08-D, checked 2026-10-31.
- City of Kirkland, Pedflags programme page, checked 2026-10-31 (no price on the page).
- FHWA, [rectangular rapid flashing beacons](https://highways.dot.gov/safety/proven-safety-countermeasures/rectangular-rapid-flashing-beacons-rrfb), as cited in CRS-PRB-001.
