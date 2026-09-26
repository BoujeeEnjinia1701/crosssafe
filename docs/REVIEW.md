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
