---
doc_id: CRS-FEA-001
title: CrossSafe feasibility assessment
project: CrossSafe
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "First feasibility assessment (kit 1.9.1 upgrade) from the TRL 3 calculations and the model"
---

# CrossSafe feasibility assessment

Option A is feasible on paper as a bought-parts build: the model of 117 parts passes the D3 check, 13 of 19 requirements are met on paper or by design, and what remains (visibility, detection, install time, flash area, cost) needs a trial or an Amish decision. Method: STANDARDS section 23.

*Table 1. Feasibility by aspect (option A).*

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | The geometry, energy, heat, wind and radio all close on paper; three STEM rows were fixed (S3 charge limit, S5 bar finish, S22 for option C) | High | Cost is $14.00 over its target; flash area At risk | CRS-STM-001, CRS-CAL-001 v0.7 |
| Materials | Steel post, aluminium bar and plates, polycarbonate enclosure, stainless fasteners, EPDM seals; no exotic materials | High | Corrosion in coastal sites; UV on the polycarbonate; to assess | CRS-CAL-001, BOM |
| Manufacturing and assembly | 65 made or bought parts and 47 fasteners; sheet bending, drilling and a few welds; 18 assembly steps | Medium | Welding skill for 5 welds; 120 min install is at the limit (PR-010) | CRS-BLD-001, cad/fidelity.json |
| Power and controls | 20 W panel and 154 Wh battery give 7.7 days; charge to 55 C needed in the hot box | Medium | Battery life at 55 C; radio band differs in the US (915 MHz) | CRS-CAL-001 B, C4 |
| Supply of parts | Signs, LED heads, enclosure, panel and battery are catalogue items | Medium | Prices are indicative; LED heads with visors and a 55 C battery need quotes | BOM |
| Regulatory and approval | Form follows IA-21; acceptance is the road authority's decision | Low | Whether IA-21 is current, the MUTCD edition and state rules are not checked | CRS-REG-001 |
| Use and acceptance | Passive detection and the button give the pedestrian a trigger; no evidence of effect for this device | Medium | PR-002 and PR-005 not verifiable at TRL 3 | CRS-CAL-001 |

Ratings: High, Medium, Low. Options B and C: B is feasible but costs about $400 and relies on road works (Low-Medium); C is the most feasible to build (40 parts, about $70) and the least proven in effect (CRS-OPT-001).
