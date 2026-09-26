---
doc_id: CRS-DDR-002
title: CrossSafe recommendations accepted
project: CrossSafe
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below with a recommendation is "Decided by Amish, 2026-09-25: go with recommendation". Items without a recommendation stay "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists every CrossSafe item that carried a recommendation in `docs/REVIEW.md` or CRS-DDR-001, the decision that follows, and what changed in the repo. Where a recommendation offered several options, the recommended option is the decision. Work that belongs to TRL 4 or later (building, testing, measuring, trials, purchasing) is decided but on hold, because TRL 4 is on hold by Amish's instruction. The repo stays at TRL 3.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3) and in CRS-DDR-001.

## Decision

*Table 1. Items decided by Amish on 2026-09-25.*

| # | Item | Decision (the recommendation) | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Budget scope (CRS-DDR-001) | `budget_usd` ($350) covers one assembly on an existing pole for TRL 3 and bench work | Status wording only; R15 already redefined at CRS-REQ-001 v0.3. `budget_usd` stays $350 |
| D2 | Autonomy fix | PIR gating of the radar; 18 Ah battery as fallback only | Status wording only; already in the model, BOM and CRS-CAL-001 |
| D3 | Post and sign size | Existing poles first; 114.3 x 3.6 mm post where a new post is needed; 750 mm sign | Status wording only |
| D4 | Reference rules | FHWA IA-21 baseline, pattern configurable | Status wording only; pilot jurisdiction stays open (O1) |
| D5 | Triggers | Button plus passive detection, switchable off | Status wording only |
| D6 | Side-to-side link | LoRa point-to-point | Status wording only |
| D7 | Shared components | FieldNode radio core; own 12 V power; CellGuard later; SwapCell not used | Status wording only; FieldNode consumer note listed under cross-repo actions in `docs/REVIEW.md` |
| D8 | Pedestrian confirmation | Pilot light where local rules allow | Status wording only |
| D9 | Pitch and problem | No change | `project.yaml` pitch and problem unchanged |
| O2 | Site-trial budget | Raise the budget to $750 for a full two-sided prototype before any site trial (the second stage of the TRL 2 budget recommendation) | Decided but on hold: a site trial is TRL 4 or later work. `budget_usd` stays $350 for the current stage under D1. CRS-CAL-001 v0.2 reports a crossing at $664.00 on existing poles ($86.00 under $750) and $810.00 with new posts ($60.00 over) |
| E1 | Enclosure heat (R8) | Option (a): a ventilated white sun shield, about $8; option (b), the enclosure under the panel's shadow, is considered when the bracket is detailed | Part 18 added to `cad/src/model.py` (roof and three walls, 25 mm air gap, open bottom, antenna hole); BOM line 18 ($8.00); CRS-CAL-001 design case is now the dusty, shielded enclosure: rise 3.9 K (was 14.7 K), 53.9 °C inside at 50 °C ambient (was 64.7 °C), charging to 41.1 °C ambient (was 30.3 °C). R8 moves from at risk to met on paper |
| E2 | Sign clamp slip (R9) | An anti-rotation bolt on new posts and a keyed saddle on existing poles, with band tension measured later | Parts 19 (M10 through-bolt, new posts only) and 20 (two keyed sign saddles) added to the model; BOM lines 19 ($3.00, variant) and 20 (2 x $3.00). CRS-CAL-001 section G: the bolt carries 1,535 N per wall, 12 % of bearing resistance; keyed saddles at an assumed grip friction of 0.4 resist 287 N·m on a 114.3 mm pole and 151 N·m on a 60 mm pole against 175 N·m. Band tension and grip friction measurement is TRL 4 work, on hold |
| E3 | Timed installation trial (suggestion, R10) | A timed trial of the 2 h installation | Decided but on hold (TRL 4). The installation estimate stays 120 min with the shield fitted to the enclosure on the ground |

## Items still open

*Table 2. Items without a recommendation, or new, and still "Proposed, awaiting Amish".*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot partner, site and jurisdiction, including a road authority. No preference stated | Proposed, awaiting Amish |
| N1 | New from CRS-CAL-001 v0.2: keyed saddles hold only on poles of about 70 mm and larger at the assumed grip friction. Options: (a) a third band at the sign on poles under 76 mm; (b) limit the existing-pole range to 76 mm and up; (c) a through-bolt on existing poles where the owner allows drilling. Recommendation: (a), because it keeps small poles usable at about $5 more on those sites | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: evidence list gains this record; `budget_usd` stays $350; `trl: 3` and `trl_target: 3`.
- CRS-REQ-001 v0.4: R8 target unchanged, status met on paper; R9 names the anti-rotation detail and stays at risk only for poles under about 70 mm; R15 met at $332.00 per assembly and $664.00 per crossing.
- CRS-PRC-001 v0.4: components 18 to 20, updated heat, wind and cost numbers; decisions shown as decided.
- CRS-CAL-001 v0.2: sun-shielded heat case (C3), anti-rotation checks (G6b, G6c), wind area of the shielded enclosure (base moment 3.43 kN·m, post 44 % of yield), cost $332.00 and $405.00 per assembly.
- CRS-DWG-001 Rev P2: shield, keyed saddles and bolt in the model and the notes.
- Media regenerated from the model with the new parts.
- TRL 4 stays on hold. Nothing in this record authorizes building, testing, measuring or purchasing.
