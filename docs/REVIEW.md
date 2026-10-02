# Review note: CrossSafe

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CRS-PRB-001 v0.2): problem with cited figures (WHO, NHTSA, UK DfT, FHWA), users, operating environment, constraints, out of scope, prior work (RRFB, FHWA IA-21, FieldNode), open questions; co-design checklist kept.
- `docs/03-requirements.md` (CRS-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, verification and status at TRL 2, a defined design case and assumptions.
- `docs/02-concept.md` (CRS-PRC-001 v0.2): how it works, numbered components, design choices, first-order numbers (flash time, energy, solar, autonomy, latency, wind load, cost), safety, open questions.
- `cad/src/concept_media.py`: massing model of one beacon assembly (14 numbered parts) with the street, zebra markings and far-side assembly as grey context; a 1.75 m scale figure on the sidewalk.
- `media/`: `hero.png`, `concept-blueprint` (PNG, PDF, SVG), `model.glb` and `viewer.html`, `exploded.png` (BOM callouts), `cutaway.png` (pole-top enclosure) and `flow.png` (daily energy, estimates labeled).
- `bom/bom.csv`: 15 lines with indicative prices, items 1 to 14 numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, use tables by industry and region, sparked-by text, problem, concept, key components and safety updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.

Media notes: `render_all` was run with `cut=False`; the cutaway and the exploded view were then rendered with the kit's own functions so small parts stay readable. The cutaway shows only the enclosure zone on a short length of post, and the exploded view shortens the post and moves the push button up 700 mm; both images say so.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Flash time, 7 m crossing | about 13 s (energy case uses 20 s) | R4 met by design |
| Daily load, 300 activations | about 29.8 Wh (LEDs about 15.4, standby about 14.4) | |
| Solar available to store, 20 W at 2.5 peak sun hours | about 38 Wh/day; break-even about 2.0 h | R7 met |
| Recovery 20 % to full at 5 peak sun hours | about 2.7 days | R7 met |
| Autonomy without sun, 12 Ah battery | about 4.1 days | **R6 not met (5 days)** |
| Side-to-side trigger latency | about 0.1 s | R3 met |
| Post stress, 40 m/s gust, 89 x 4 mm post | about 169 MPa, 72 % of S235 yield | **R9 not met (60 %)** |
| Parts per assembly / per crossing | about $361 / about $722 ($311 per assembly on an existing pole) | **R15 not met** |

Requirements not met or at risk:

- **R6 (autonomy) not met:** about 4.1 days against 5.
- **R9 (structure) not met with the modeled post:** 89 x 4 mm reaches about 72 % of yield; a 76 mm post would yield. A 114.3 x 3.6 mm post (about 47 %) or a 600 mm sign (about 59 %) meets it.
- **R15 (cost) not met:** about $361 per assembly against $350, and a crossing needs two.
- **R2 (visibility) and R5 (detection quality) unverified:** these decide whether the device works at all and need photometry and a site trial.

### Proposed, awaiting Amish

Update 2026-09-25: items 1 to 8 are now "Decided by Amish, 2026-09-25: go with recommendation" (CRS-DDR-002); item 9 has no recommendation and stays "Proposed, awaiting Amish".

1. **Budget (pitch-level).** `budget_usd` is $350, but a working crossing needs two assemblies (about $722). Options: (a) keep $350 and define the prototype as one assembly on an existing pole (about $311), with the second side later; (b) raise `budget_usd` to $750 for a full two-sided prototype; (c) cut cost (one-sided light bar, smaller sign) to bring a pair near $600. Recommendation: (a) for TRL 3 and 4 bench work, then (b) before any site trial. `project.yaml` is unchanged.
2. **Autonomy fix.** Options: gate the radar with a PIR sensor (about 6 days, about $3 more, adds detection logic), an 18 Ah battery (about 6.2 days, about $20 more), or relax R6 to 4 days. Recommendation: PIR gating, with the 18 Ah battery as fallback.
3. **Post and sign size.** Options: 114.3 x 3.6 mm post, a 600 mm sign on the 89 mm post, or existing lighting poles only. Recommendation: design for existing poles first and specify 114.3 mm when a new post is needed.
4. **Reference rules.** Use FHWA IA-21 (US) as the baseline for size and flash pattern, with a configurable pattern for other jurisdictions. Recommendation: yes, and choose the pilot jurisdiction early.
5. **Triggers.** Push button plus passive radar, versus button only. Recommendation: both, with passive detection switchable off where not allowed.
6. **Side-to-side link.** LoRa radio versus a cable under the road. Recommendation: LoRa.
7. **Shared components.** Reuse the FieldNode radio and logging core for the controller; keep CrossSafe's own 12 V power system because the FieldNode power stage is too small; consider CellGuard in place of the drop-in battery's closed BMS later. SwapCell is not proposed (48 V class, far too large). Recommendation: FieldNode radio core yes; CellGuard later.
8. **Pedestrian-facing confirmation light** on the back faces. Recommendation: include, subject to local rules.
9. **Pilot partner and site**, including a road authority willing to review the design.

### Safety concerns

- Road safety: a beacon that fails dark, false-triggers often, or gives pedestrians false confidence can cause harm; fail-safe logic (R12) and road authority approval are essential.
- Structure: the post, sign and panel are a falling hazard in high wind or a vehicle strike; the wind load is the controlling case and is not yet met with the modeled post.
- LiFePO4 battery in a sun-heated box: fusing, BMS, charge temperature limits and enclosure temperature need checking.
- Installation is work at height beside live traffic.

### Problems and notes

- WebSearch was unavailable; every cited figure was checked by fetching the source page. Some facts were left out because they could not be verified (commercial RRFB prices, EU pedestrian share, India's latest national figures, a primary source for sign mounting heights and push-button force limits). The 2.1 m sign height and 22 N button force are proposed targets, not cited rules.
- The WHO India figure (about 10 % of global road deaths) comes from an older WHO country page.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- `project.yaml` pitch and problem remain accurate and are unchanged.

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check the energy, photometry, radio link and wind load estimates by calculation and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to go through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CRS-DDR-001 v0.1, status proposed): nine items adopted as recommended for TRL 3, open for Amish's review (D1 to D9), and two left open (O1, O2).
- `docs/04-calcs/01-sizing.md` (CRS-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: flash timing, energy budget, autonomy and sensitivity, harvest and recovery, enclosure heat and charging window, radio time on air, latency, link budget and duty cycle, photometry screening, heights and installation, wind load on three posts, clamp torsion, footing embedment and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, prints every number the note quotes and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model (sign, light bar, four heads, pilot light, button station, radar and PIR on an arm, panel and bracket, enclosure with battery, charger, controller and antenna, seven band clamps, 114.3 mm post and footing), clash check clean. Exports `cad/step/` and `cad/stl/` for `crosssafe-assembly`, `crosssafe-existing-pole`, `sign-and-light-bar` and `pole-top-enclosure`.
- `cad/src/sheets.py` and `cad/drawings/CRS-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:50, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". CRS-DWG-001 was free because the concept blueprint is CRS-DWG-010.
- `bom/bom.csv`: 17 lines, all priced with a supplier type. New lines 16 (PIR) and 17 (pilot light); the post line is the 114.3 mm new-post variant, excluded from the existing-pole total. `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked; temporary `media/_views*` folders deleted. The exploded view draws the PIR and pilot light at three times size so they show, and says so.
- CRS-PRB-001, CRS-PRC-001 and CRS-REQ-001 revised to v0.3; `README.md` (TRL badge and line, links to the drawing and calculations, concept numbers, key components, safety) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (CRS-CAL-001, Table 5)

None not met, 2 at risk, 3 not verifiable at TRL 3, 4 met on paper, 6 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R8 Environment | **At risk** | Enclosure 9.6 K (clean) to 14.7 K (dusty) above ambient in sun; no charging above 30.3 to 35.4 °C ambient; 64.7 °C inside at 50 °C ambient, above the typical 60 °C LiFePO4 discharge limit |
| R9 Structure | **At risk** | 114.3 x 3.6 mm post at 100 MPa, 42 % of yield (met); sign clamp torsion 175 N·m against 144 N·m of friction at an assumed 1,000 N band tension |
| R2 Visibility | Not verifiable at TRL 3 | About 3,939 cd per head (screening); SAE J595 Class 1 yellow figures not available |
| R5 Detection quality | Not verifiable at TRL 3 | Needs a site trial |
| R10 Mounting | Not verifiable at TRL 3 | Fit met (60 to 114.3 mm); install estimate 120 min, exactly the 2 h limit |
| R3, R6, R7, R15 | Met on paper | 48 ms (244 ms with retries); 7.7 days (5.4 at -20 °C); break-even 1.05 peak sun hours, recovery 2.05 days; $318.00 per assembly, $636.00 per crossing |
| R1, R4, R11 to R14 | Met by design | 12.8 s flash for 7 m; button 1.05 m; enclosure bottom 2.85 m |

Key numbers: daily load 16.0 Wh (TRL 2: 29.8), because IA-21 lights each head 25 % of the time (TRL 2 assumed 35 %) and the PIR gating cuts standby to 187 mW; base moment 3.35 kN·m in a 40 m/s gust; footing 500 mm by 1.8 m in clay (screening); 2.43 kN·m added to a host pole. R6 and R15, not met at TRL 2, are met on paper after D2 and D1.

### Decisions recorded (CRS-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation (previously adopted for TRL 3, open for his review): D1 `budget_usd` covers one assembly on an existing pole (R15 redefined; `budget_usd` unchanged at $350); D2 PIR gating of the radar, 18 Ah battery as fallback only; D3 existing poles first, 114.3 x 3.6 mm where a new post is needed; D4 IA-21 baseline, configurable pattern; D5 button plus passive detection, switchable off; D6 LoRa side-to-side link; D7 FieldNode radio core, own 12 V power, CellGuard later, SwapCell not used; D8 pedestrian pilot light where allowed; D9 no change to pitch or problem.

### Still awaiting Amish

Update 2026-09-25: items 2 to 4 and the timed-trial suggestion are now "Decided by Amish, 2026-09-25: go with recommendation" (CRS-DDR-002); item 1 stays "Proposed, awaiting Amish".

1. **O1, pilot partner, site and jurisdiction**, including a road authority. No preference stated.
2. **O2, site-trial budget.** Recommended at TRL 2: raise `budget_usd` to $750 before any site trial. Not applied. Against $750 a crossing is $114.00 under on existing poles and $26.00 over with new posts ($776.00).
3. **New, enclosure heat (R8).** Options: (a) a ventilated white sun shield, about $8 (rise 3.9 K; charging to 41.1 °C ambient); (b) move the enclosure under the panel's shadow; (c) accept the loss of harvest on hot days. Recommendation: (a), with (b) considered when the bracket is detailed. Not applied.
4. **New, sign clamp slip (R9).** Options: an anti-rotation bolt or tab through the sign saddle, or a specified higher band tension. Recommendation: an anti-rotation bolt on new posts and a keyed saddle on existing poles, with band tension measured later. Not applied.

Suggestion only, not in the repo: a timed trial of the 2 h installation would settle R10 early.

### Cross-repo consistency

- FieldNode (FND-DDR-001) adopted an STM32WL-class module and LoRaWAN, and "LoRa point-to-point not used" for FieldNode itself. CrossSafe reuses the same module and logging design but runs the side-to-side link in LoRa point-to-point mode (D6), which the module supports. This is a firmware mode difference, not a hardware conflict; noted here, FieldNode not edited. CrossSafe does not use the FieldNode power stage or its $126.00 core cost.
- CellGuard's review says CrossSafe does not use CellGuard at this stage; consistent with D7. No other shared component (MotionCore, ThermaCart, TwinKit, CalRig) is used.

### Safety concerns

- Road safety: a beacon that fails dark, false-triggers or gives pedestrians false confidence can cause harm. Photometry (R2) and detection (R5) are unproven, and road authority approval is essential.
- Heat: in hot sun the battery may exceed its discharge limit; the 45 °C charge cut-off must never be defeated to recover energy.
- Structure: the sign can rotate on band clamps in a storm at the assumed tension; the host pole of an existing-pole install carries about 2.4 kN·m more, which the owner must check; the footing is a screening size only.
- LiFePO4 battery: 5 A fuse at the terminal, BMS with low-temperature charge protection.
- Installation is work at height beside live traffic.

### Gaps and notes

- Citations: IA-21 was fetched again to confirm the flash sequence (each indication lit 200 ms of 800 ms), SAE J595 Class 1 yellow intensity, night dimming and the permitted pilot light; these are now in the docs. The older WHO India page was fetched and still states "about 10 %"; its date is not shown. SAE J595 itself, commercial RRFB prices and the other facts left out at TRL 2 remain unverified and are still left out. WebSearch was not used.
- Assumptions only tests can settle: LED power and intensity, radar duty under PIR gating, charger self-consumption, band tension and the shield factor (borrowed from WWT-CAL-001).
- Media: the kit's cutaway only cuts near the origin, so, as at TRL 2, the enclosure zone is moved to the origin before cutting; the exploded view shortens the post and moves the button up. Both images say so.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `electronics/` and `firmware/` are empty. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on D1 to D9, O1, O2 and items 3 and 4 above. For the record only, TRL 4 would need: a bench build of one assembly on a pole stub; a lab test report (TST, `environment: lab`) covering LED head power and intensity against SAE J595, standby and energy per activation, radio latency and fault behavior, enclosure temperature in sun with and without a shield, and clamp torsion and band tension; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every CrossSafe item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (CRS-DDR-002 v0.1). CRS-DDR-001 is revised to v0.2 with the new status.

### Decisions applied and what changed

- **D1 to D9 (CRS-DDR-001):** status wording only; the design already reflected them.
- **O2, site-trial budget $750:** decided, on hold with TRL 4. The recommendation was staged ($350 for TRL 3 and bench work under D1, $750 before a site trial), so `budget_usd` stays **$350**. A crossing is now $664.00 on existing poles and $810.00 with new posts against $750.
- **E1, enclosure heat (R8):** ventilated white sun shield added (model part 18, BOM line 18, $8.00). Dusty enclosure rise 14.7 K before, 3.9 K after; interior at 50 °C ambient 64.7 °C before, 53.9 °C after; charging cut-off ambient 30.3 °C before, 41.1 °C after. R8 at risk before, met on paper after.
- **E2, sign clamp slip (R9):** M10 through-bolt on new posts (part 19, BOM line 19, $3.00, variant) and keyed saddles on existing poles (part 20, BOM line 20, 2 x $3.00). Torsion 175 N·m against 144 N·m of plain-saddle friction before; after, the bolt runs at 12 % of bearing and keyed saddles resist 287 N·m on 114.3 mm and 151 N·m on 60 mm poles (grip friction 0.4 assumed). R9 stays at risk, now only for poles under about 70 mm.
- **E3, timed installation trial:** decided, on hold with TRL 4. The estimate stays 120 min with the shield fitted on the ground.
- Knock-on numbers: the shield enlarges the enclosure's wind area, so the base moment rises from 3.35 to 3.43 kN·m and the 114.3 mm post from 42 % to 44 % of yield; embedment needed 1,776 mm (1,800 modeled); host pole moment 2.43 to 2.51 kN·m. Cost per assembly on an existing pole $318.00 before, $332.00 after; with a new post $388.00 before, $405.00 after.
- Files: `cad/src/model.py` (parts 18 to 20; STEP and STL re-exported; clash check clean), `bom/bom.csv` (20 lines) and `bom/bom-notes.md`, `docs/04-calcs/sizing.py` and `01-sizing.md` (CRS-CAL-001 v0.2; checks C3, G6b, G6c), `cad/src/sheets.py` and CRS-DWG-001 at Rev P2, `cad/src/concept_media.py` and all of `media/`, CRS-PRC-001 v0.4, CRS-REQ-001 v0.4, `README.md`, `project.yaml` (evidence list only), PDFs in `docs/pdf/`.
- `README.md`: "What sparked the idea" rewritten around FHWA's termination of IA-11 over the RRFB patents (December 21, 2017) and the reinstatement as IA-21 once the concept was in the public domain (March 20, 2018). All media and PDFs regenerated with the designmolecule.com footer.

### Requirement status (CRS-CAL-001 v0.2, Table 5)

None not met, 1 at risk, 3 not verifiable at TRL 3, 5 met on paper, 6 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R9 Structure | **At risk** (poles under about 70 mm) | Post 44 % of yield; bolt 12 % of bearing; keyed saddles hold from about 70 mm |
| R2 Visibility | Not verifiable at TRL 3 | About 3,939 cd per head (screening) |
| R5 Detection quality | Not verifiable at TRL 3 | Needs a site trial |
| R10 Mounting | Not verifiable at TRL 3 | Install estimate 120 min, at the 2 h limit |
| R3, R6, R7, R8, R15 | Met on paper | 48 ms; 7.7 days; break-even 1.05 h; 53.9 °C inside at 50 °C ambient; $332.00 per assembly, $664.00 per crossing |
| R1, R4, R11 to R14 | Met by design | 12.8 s flash for 7 m; button 1.05 m; enclosure bottom 2.85 m |

### Still awaiting Amish

1. **O1, pilot partner, site and jurisdiction.** No recommendation; no preference stated.
2. **N1 (new), sign rotation on poles under about 70 mm.** Options: (a) a third band at the sign on poles under 76 mm; (b) limit the existing-pole range to 76 mm and up; (c) a through-bolt on existing poles where the owner allows drilling. Recommendation: (a). Not applied.

### Cross-repo actions

- **FieldNode:** note CrossSafe as a user of the FieldNode radio and logging core in LoRa point-to-point mode (D6, D7). No change to FieldNode's hardware is needed. Not edited from here.
- **CellGuard:** later option in place of the drop-in battery's BMS (D7); no action now.

### Safety concerns

- Unchanged from the TRL 3 session, except that the sun shield removes the hot-battery concern on paper (the shield factor is not measured) and sign rotation is now a concern only on small existing poles.
- The through-bolt hole must be drilled before galvanizing; drilling an existing pole needs the owner's consent.

### TRL 4

TRL 4 remains on hold by Amish's instruction. The site-trial budget, the timed installation trial and the measurement of band tension, saddle grip and shielded enclosure temperature are decided but not started. `trl: 3` and `trl_target: 3` are unchanged.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose CrossSafe for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; it does not change the design, the calculations, the drawing or the BOM.

### What was added

- `cad/src/product_model.py`: `product_parts()` (74 parts in the groups shell, internal, accessory and context), `TITLE` and `RENDER_VIEWS` (hero, exploded and detail). It imports `PARAMS` and `derived()` from `cad/src/model.py` and keeps every main dimension, height and interface.
- Finished-product detail: a 750 mm sign with rounded corners, fluorescent yellow-green retroreflective sheeting, a black border and a walking-figure symbol on an aluminium blank, with bracket nuts; a charcoal light bar with a parting line, head visors, bezels, clear lenses and amber LED arrays (the left head on each face lit, as in the wig-wag); a lit pilot light; a radar housing with radome and parting line on a round arm, and a PIR Fresnel dome; stainless band clamps with screw housings and serrated keyed saddles; a push-button station with a stainless piezo button, tactile arrow, lit acknowledgement ring, tone grille and a printed instruction plate with security fasteners; the white sun shield with louvre slots and security fasteners over the IP65 enclosure, glands and membrane vent; the battery, MPPT charger and controller board inside; the antenna; the 20 W panel with frame, cells, busbars and junction box on its bracket; and the M10 anti-rotation bolt.
- Context (not in the BOM): a compact patch of sidewalk, kerb, road and crossing markings with tactile paving, and the shared clay mannequin (1.75 m, stand pose) waiting at the kerb.
- `README.md`: the hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately.

### Where the appearance model differs from model.py

1. **Post split for framing only.** The one 3.7 m post is drawn as three touching sections in different render groups (lower section as context, sign zone as shell, top as accessory) so the detail view can frame the lamp head. The embedded length and footing are not drawn. No geometry change. No decision needed.
2. **Head visors and bezels.** Visors 26 mm deep over each LED head and bezels 14 mm larger than the 140 x 62 mm lens are not in model.py; they add a little frontal area and depth to the light bar. Proposed, awaiting Amish. Recommendation: keep visors in the design intent and add them to model.py and the wind area in the next CRS-CAL-001 revision, since they cut sun phantom on the lenses.
3. **Louvre slots in the sun shield.** model.py and the shield estimate in CRS-CAL-001 treat the shield walls as plain sheet. Proposed, awaiting Amish. Recommendation: keep the slots as appearance only until the shield factor is measured, then decide whether to adopt them.
4. **Sign colour.** The model uses fluorescent yellow-green sheeting, common at school crossings. The BOM says "local sign design". Proposed, awaiting Amish. Recommendation: show fluorescent yellow-green in renders and leave the colour to the local road authority.
5. **Small envelope changes.** The pilot light housing is 36 mm across (model.py 30 mm), the sign saddles carry a bracket flange at the sign back, and the band clamp screw housings are turned away from the enclosure and the anti-rotation bolt. Proposed, awaiting Amish. Recommendation: accept as appearance detail; no calculation is affected.

### Status

This is an appearance model only: no tolerances and no fabrication detail. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: design for construction and the prototype build plan (kit 1.7.0)

Under Amish's 2026-09-30 approval of the build plan format ("this is the correct build plan ... Extend this across all the other repos") and his instruction to make each design physically buildable, kit 1.7.0 was installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`) and `/build-plan` was carried out.

### What was done

- `cad/src/model.py`: rebuilt as a constructable model of 55 components (56 with the new post) with `build_components()`, `pole_context()` and `checks()`; `python cad/src/model.py --check` runs 101 checks on the existing-pole kit and 103 on the new-post variant (no overlaps, every joint touching, clearances, pole range, R14 heights). All pass.
- `docs/decisions/0003-design-for-construction.md` (CRS-DDR-003, Draft): every change and its reason, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `bom/bom.csv` (23 lines) and `bom/bom-notes.md`; `docs/04-calcs/sizing.py` and `01-sizing.md` (CRS-CAL-001 v0.3); CRS-REQ-001 v0.5; CRS-PRC-001 v0.5; `README.md` (links line, "Building the prototype").
- `cad/src/build_plan_media.py`: overview, making sketches CRS-DWG-101 to 109, 13 joint close-ups, 18 assembly step pictures, two drilling layouts and the wiring diagram, in `docs/05-build-plan/` and `cad/drawings/`.
- `docs/05-build-plan.md` (CRS-BLD-001) and `docs/06-design-decisions.md` (CRS-DEC-001); both in `trl_evidence`; `design_state: constructable` in `project.yaml`.
- CRS-DWG-001 at Rev P4; STEP and STL re-exported; concept media regenerated (`hero`, `concept-blueprint`, `model.glb`, `viewer.html`, `exploded`, `cutaway`, `flow`).

### Design changes made for construction (CRS-DDR-003)

1. Pole clamps: eight identical keyed pole saddles (80 x 40 x 60 mm aluminium, 120° keyed V, band groove, two tapped M8 holes) and 19 x 0.76 mm stainless bands replace the concept's rings, which passed through every bracket.
2. Sign: bolted flat on its two saddles, 63.4 mm nearer the pole than the concept's 92 mm stand-off blocks; the light bar now stands 70 mm proud of the sign's plane, still directly under it.
3. Light bar: folded 2 mm channel with lips, screwed bottom cover with a gland, riveted end caps; heads through 128 x 50 mm windows; bolted to its saddle from inside; 12.6 mm further from the pole.
4. Enclosure: hung by its lug kit on a new 4 mm mounting plate with saddle tabs above and below; internal plate on the box's bosses; modules on stand-offs; battery on the floor under a new bent strap; 27.6 mm further from the pole.
5. Enclosure saddles moved to the plate's tabs so their bolts are above the shield roof and below the box.
6. Sun shield: side flanges screwed to the mounting plate; air gap and open bottom unchanged.
7. Radar: on a new bent 40 x 5 mm arm on its own saddle, PIR underneath; PIR underside 2,515 mm (was 2,520 mm).
8. Panel bracket: welded socket, cap and cheeks with a pivot hole and 20° tilt slot; two angle rails on the panel frame lip.
9. Instruction plate on its own saddle (the eighth).
10. Enclosure glands placed in two rows beside the battery; the vent at the lid end.
11. Anti-rotation bolt (new posts): M10 x 160 through the sign, the upper saddle and the post, in place of one sign bolt.

### Key results

- Requirement status (CRS-CAL-001 v0.3): **R15 over the value-engineering target on paper**: $360.00 per assembly on an existing pole against a $350 target ($10.00 over), and $720.00 per crossing against $700 ($20.00 over) (was $332.00 and $664.00). R9 at risk on poles under about 70 mm (unchanged); R2, R5, R10 not verifiable at TRL 3; R3, R6, R7, R8 met on paper; R1, R4, R11 to R14 met by design.
- Wind: base moment 3,521 N·m (was 3,434), 114.3 mm post at 45 % of yield (was 44 %), embedment 1,791 mm needed (1,800 modelled), 2,601 N·m added to an existing pole.

### Proposed, awaiting Amish

All listed in `docs/06-design-decisions.md`: (1) accept the CRS-DDR-003 changes; (2) panel mount for existing poles the socket does not fit (recommended: a side-of-pole arm, designed for the pilot site); and, carried over, N1 (third saddle and band on poles under 76 mm), O1 (pilot partner and jurisdiction) and the four appearance items of 2026-09-26.

### Stale until regenerated on Amish's Mac

The design changed visibly (sign nearer the pole, saddles and bands, mounting plate, radar arm, panel bracket), so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` are stale. They were not regenerated here.

### Safety concerns

- The build plan keeps the battery and its fuse out until safety stops S1 to S4, and stops before the 3.7 m post is stood up (S7) and before any roadside installation (S8).
- The bracket welds and galvanizing need a competent welder; never weld galvanized steel indoors.
- Band tension and keyed saddle grip are still assumptions; they decide whether the sign can turn on small poles.

### Recommended next step

Amish reviews the register, chiefly the CRS-DDR-003 changes (item 1) and the Value engineering section. TRL 4 stays on hold.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved the recommendations for every open decision: "i approve your recommendations for all 555 open decisions." The 8 open decisions of the design decisions register are now in its Decisions made table, dated 2026-10-02.

CRS-DDR-003 (design for construction) is accepted, with A2 and A3 decided as recommended. Item 3 was decided on a changed recommendation: the existing-pole kit is limited to poles of 76 mm and larger until a slip-torque test confirms the keyed saddle's grip, so R10 is restated. CRS-DDR-002 items O1 and N1 are recorded as decided. Also noted: `bom/bom-notes.md` still says raising `budget_usd` to $375 is proposed, which the value-engineering wording of 2026-10-01 superseded; it was left for the next BOM revision.

### Documents changed

- `docs/06-design-decisions.md` (CRS-DEC-001 v0.3)
- `docs/decisions/0003-design-for-construction.md` (CRS-DDR-003 v0.3)
- `docs/decisions/0002-recommendations-accepted.md` (CRS-DDR-002 v0.2)
- `docs/01-problem.md` (CRS-PRB-001 v0.5)
- `docs/02-concept.md` (CRS-PRC-001 v0.7)
- `docs/03-requirements.md` (CRS-REQ-001 v0.7)
- `docs/04-calcs/01-sizing.md` (CRS-CAL-001 v0.5)
- `bom/bom-notes.md` (not a controlled document)
- `README.md` (not a controlled document)

### Follow-up actions to carry approved decisions into the design

1. Decision 2: Model and drawings: design the side-of-pole panel arm on two more saddles once the pilot site's poles are known (not for the prototype).
2. Decision 3: Calculations: change R10's range in `docs/04-calcs/sizing.py` and `results.csv` to 76 to 114.3 mm for the existing-pole kit, and restate R9's status for that range.
3. Decision 3: Plan a slip-torque test of the keyed saddle and band (TRL 4, on hold) before 60 to 75 mm poles return with a third saddle and band; then add that saddle and band to the model and the BOM as a small-pole variant.
4. Decision 3: BOM: change line 13's description from 60 to 114.3 mm poles to the 76 to 114.3 mm range of the existing-pole kit.
5. Decision 5: Model: add the visors and bezels to the LED heads in `cad/src/model.py`.
6. Decision 5: Calculations: add the visors to the light bar wind area at the next CRS-CAL-001 revision and recheck R9.
7. Decision 5: BOM: state on line 3 that the LED heads are bought with visors.
8. Decision 1: Renders: regenerate the photoreal renders, `media/card.png`, `media/social-preview.png` and the appearance model on Amish's Mac to show the accepted design for construction (items 7 and 8 follow with them).

### Points found in the review

1. R10 claims a fit on existing 60 to 114 mm poles, but the panel socket fits only about 114 mm free-topped poles (item 2) and the sign can slip on poles under about 70 mm (item 3); the 'fit met' status overstates what the prototype does.
2. The saddle grip friction (0.4) and band tension (1,000 N) behind R9 on existing poles are assumptions with no planned test until TRL 4, which is on hold.

No CAD model, BOM quantity or price, calculation result or picture was changed. TRL stays at 3; TRL 4 remains on hold.
