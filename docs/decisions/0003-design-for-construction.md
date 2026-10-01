---
doc_id: CRS-DDR-003
title: CrossSafe design for construction
project: CrossSafe
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are "Proposed, awaiting Amish" and are listed as open decisions in the design decisions register (`docs/06-design-decisions.md`, CRS-DEC-001).

## Context

On 2026-09-30 Amish approved the build plan format and asked for it across every repo, writing: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The CrossSafe model of CRS-DDR-002 showed what the beacon does, with the right heights, sizes and wind areas, but almost nothing in it was fixed to anything. The pole clamps were 8 mm thick rings that passed straight through every bracket they were meant to hold; each bracket touched the round pole along a single line; the sign stood on two solid blocks 92 mm deep; the battery, charger and controller floated inside the enclosure; the sun shield had no fixing; and the panel's tilt plate hung 7.5 mm below the panel and 10 mm above its stem, touching neither. A build123d check of the concept model found the parts that overlapped or floated; Table 1 lists them as P1 to P11.

The changes keep what CrossSafe does: the same sign, light bar, LED heads, flash pattern, button, radar, PIR, panel, battery, enclosure, sun shield and radio, at the same heights above the sidewalk (button 1,050 mm, light bar bottom 2,100 mm, sign 2,250 to 3,311 mm, enclosure 2,850 to 3,150 mm, radar 2,600 mm, panel centre 3,930 mm). Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 101 constructability checks on the existing-pole kit and 103 on the new-post variant (`python cad/src/model.py --check`): no two of the 55 components (56 with the new post) overlap, every joint that must touch does, the stated clearances hold, both ends of the pole range seat in the saddle's V, and the heights of R14 hold. All pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The seven "pole clamps" were rings 8 mm thick and 30 mm wide drawn round the pole. Each passed through the bracket it was meant to hold (light bar block, sign saddles, enclosure back plate, button station, radar arm), and every bracket met the round pole along one line. | One part holds everything to the pole: eight identical **keyed pole saddles** (line 20), each a block 80 wide, 40 deep and 60 tall sawn from 80 x 40 mm aluminium bar, with a 120° V in the back whose faces are keyed with saw cuts, a 21 x 1 mm band groove across the front and two tapped M8 holes 20 mm above and below the groove. A 19 x 0.76 mm stainless band (line 13) runs round the pole and across the saddle's front in the groove; the part fixed to the saddle covers the band. | Tightening the band pulls the V onto the pole; the pole touches both V faces 6.4 mm inside the back corners on a 114.3 mm pole and 20 mm inside on a 60 mm pole, so one saddle fits the whole R10 range. One part made eight times keeps the workshop simple. 19 x 0.76 mm is the common size of stainless banding with a buckle. |
| P2 | The sign stood 92 mm in front of the pole on two solid blocks 92 x 80 x 60 mm (about 1.2 kg of aluminium each), with nothing that made them or fixed them. | The sign lies flat on the front of its two saddles, 28.6 mm in front of the pole surface, held by two M8 security bolts into each saddle (four 9 mm holes on the sign's vertical centre line). The sign is now 63.4 mm nearer the pole. | The saddle is the stand-off. The light bar is still directly under the sign point, 20 mm below it; it now stands 70 mm proud of the sign's plane, which IA-21 allows. |
| P3 | The light bar was a solid box fixed by a 16 x 80 x 100 mm block that touched the pole on one line; the LED heads were 8 mm slabs stuck on its faces. | A folded 2 mm aluminium channel (back, top, front, with 10 mm inward lips), a screwed bottom cover with a cable gland and two riveted end caps. Each head's flange sits on the outside of its wall over a 128 x 50 mm cut-out, with its body inside. The back wall bolts to the bar's saddle with two M8 bolts put in from inside, reached by taking the cover off. | A housing that can be folded, opened and sealed. The bar's back face moves 12.6 mm further from the pole (onto the saddle); its height, length and the head positions are unchanged. |
| P4 | The enclosure was a hollow box held off the pole by a 5 x 120 x 200 mm block touching the pole on one line; the battery, charger and controller floated inside it. | A 4 mm aluminium **mounting plate** (line 21), 350 x 300 mm with a 90 x 90 mm tab above and below, bolted to two saddles by its tabs. The enclosure hangs on its front by the box maker's four lugs (M5 screws, nyloc nuts behind). Inside, the box's own internal plate sits on four bosses; the charger, controller and a fuse block stand on it on 6 mm stand-offs; the battery stands on the floor against it under a bent aluminium **battery strap** (line 23). | The box back stays sealed. The enclosure's back face is now 32.6 mm from the pole surface (was 5 mm), so the enclosure moves 27.6 mm further out; its height and size are unchanged. |
| P5 | (Found in checking) With the saddles behind the enclosure, the bolts holding the plate to them would be hidden behind the box. | The saddles sit on the plate's tabs, above and below the box: their bolts are at 3,190 and 3,230 mm, above the shield roof, and at 2,770 and 2,810 mm, below the box. | The enclosure, plate and shield can be bolted to the pole, and taken off it, as one unit. |
| P6 | The sun shield had no fixing. | A 15 mm flange folded out along the plate edge of each side sheet lies flat on the mounting plate and takes two M5 security screws into tapped holes. The roof's air gap stays open toward the post above the plate's top edge; the bottom stays open. | The 25 mm air gap at the back, sides and roof is unchanged, so the thermal result of CRS-CAL-001 stands. |
| P7 | The radar sat on a 24 mm rod that touched the pole on one line; the PIR hung under the radar. | A **radar arm** (line 22): 40 x 5 mm aluminium bar bent to an L. The short leg stands on its saddle (two M8 bolts); the long leg runs 251 mm toward the kerb with the radar screwed on top of its end and the PIR under it. | The radar stays at 2,600 mm and 240 mm from the pole surface. The PIR's underside drops 5 mm, to 2,515 mm, still above R14's 2.5 m line. |
| P8 | The panel bracket was a sleeve over the post top, a block standing on it and a tilt plate 7.5 mm below the panel and 10 mm above the block, touching neither. | A welded steel **panel bracket** (line 7): a 139.7 x 4 mm socket over the post top with a 6 mm cap that rests on the pole, three welded M10 nuts with security set screws, and two 6 mm cheeks standing on the cap. Two 40 x 40 x 4 mm aluminium **rails** bolt across the panel frame's back lip and to the outside of the cheeks by a pivot bolt and a bolt in a 20° tilt slot. | Every joint is face to face and bolted; the tilt can be set from 20 to 40° as the BOM always said. The panel's centre, size and 30° tilt are unchanged. |
| P9 | The push-button station touched the pole on one line; the instruction plate stood flat against a round pole with no fixing. | The station bolts to its own saddle at 1,050 mm; the instruction plate to a saddle of its own at 1,300 mm (two M8 bolts). | This is why there are eight saddles and bands, not seven. |
| P10 | The enclosure's bottom face had no positions for its cable glands, and gland nuts inside would have sat under the battery. | Four M20 glands (panel, light bar, button, radar and PIR) in two rows, 40 and 100 mm from the back face, 105 mm each side of the centre line, clear of the battery; the membrane vent at the lid end. Glands are now in line 15. | Each gland and its inside nut clear the battery by at least 5 mm. |
| P11 | On new posts the anti-rotation bolt ended inside the saddle, with nothing holding it. | The M10 bolt replaces the upper sign saddle's upper M8 bolt: through the sign, the saddle (drilled through 10.5 mm) and both post walls, nyloc nut behind. Its length is 160 mm (was 200 mm). | The bolt still carries the sign's torsion as two bearing loads on the post walls (CRS-CAL-001, [G6b], unchanged). |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Wind | Along the road, the enclosure group now includes the mounting plate's edges beside the shield and its two tabs: base moment 3,521 N·m (was 3,434), the 114.3 mm post at 45 % of yield (was 44 %), embedment needed 1,791 mm (1,800 modelled), moment added to an existing pole 2,601 N·m (was 2,514). R9's status is unchanged. | Follows the model (CRS-CAL-001 v0.3, [G1] to [G8]). |
| Cost | Lines 1, 7, 13, 15, 19 and 20 changed and lines 21 to 23 added: $360.00 per assembly on an existing pole (was $332.00), $433.00 with a new post (was $405.00); $720.00 and $866.00 per crossing. **R15 is now not met on paper: $10.00 over the $350 budget, and $20.00 over its $700 per crossing.** | Parts that every buildable version needs; see Table 3, A1. |
| Heights | PIR underside 2,515 mm (was 2,520 mm). Everything else unchanged. | P7. |
| Drawing | CRS-DWG-001 Rev P4; making sketches CRS-DWG-101 to 109 added. | Follows the model. |
| Documents | CRS-CAL-001 v0.3, CRS-PRC-001 v0.5, CRS-REQ-001 v0.5, `bom/bom.csv` (23 lines), `bom/bom-notes.md`. | Follows the model. |
| Heat, energy, radio, light | Unchanged. The enclosure, shield and air gaps keep their sizes; nothing electrical changed. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The parts that make the design buildable take one assembly on an existing pole to $360.00, $10.00 over `budget_usd` ($350), so R15 is not met on paper. | (a) raise `budget_usd` to $375; (b) look for $10.00 of savings now (for example a cheaper box or sign quote); (c) keep $350 and accept R15 not met until prices are quoted at TRL 4. | (a): the added parts are needed for any buildable version, and the prices are indicative either way. |
| A2 | The post-top socket fits poles of about 114 mm with an open or capped top. Existing poles in R10's range (60 to 114.3 mm), or poles that are taller or carry a luminaire, cannot take it. | (a) reducing sleeves for 76 and 89 mm poles; (b) a side-of-pole panel arm on two more saddles; (c) limit the existing-pole kit to free-topped poles of about 114 mm. | (b), designed when the pilot site's poles are known (O1); the prototype uses (c). |
| A3 | The changes in Table 1 are visible: the sign sits nearer the pole, the light bar stands proud of it, the saddles, bands, plate and bracket are new. | (a) accept them; (b) ask for a different arrangement of any of them. | (a). The photoreal renders and the appearance model then need updating on Amish's Mac. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CRS-BLD-001 (`docs/05-build-plan.md`) shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: one not met (R15, cost, Table 3 A1), one at risk (R9, small poles, unchanged), three not verifiable at TRL 3, four met on paper, six met by design (CRS-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept sign stand-off, clamps and bracket; they are stale until regenerated on Amish's Mac, where Blender is.
- The keyed saddle's grip friction (0.4) and the band tension (1,000 N) remain assumptions to be measured at TRL 4, which is on hold.
