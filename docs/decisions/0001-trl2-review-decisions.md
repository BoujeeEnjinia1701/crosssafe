---
doc_id: CRS-DDR-001
title: CrossSafe TRL 2 review decisions
project: CrossSafe
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted. On 2026-09-25 Amish accepted every recommendation ("i accept all your recommendations, go with them across all repos"), so D1 to D9 and O2 are "Decided by Amish, 2026-09-25: go with recommendation" (see CRS-DDR-002). O1 has no recommendation and remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis CRS-PRC-001 v0.2 marked every key design choice as proposed. On 2026-09-25 Amish asked for this batch of Design Molecule repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. At v0.1 nothing here was recorded as decided by Amish; he accepted the recommendations later the same day (CRS-DDR-002).

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CRS-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work, since decided by Amish (CRS-DDR-002).*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Budget scope | Option (a): `budget_usd` ($350) covers one assembly on an existing pole, the prototype for TRL 3 and later bench work; the second side follows later. R15 is redefined to match. `budget_usd` is not changed. The recommended rise to $750 before a site trial is not adopted here; see O2. | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Autonomy fix | Gate the radar with a low-power PIR sensor (about $3); the 18 Ah battery is kept as a fallback only; R6 stays at 5 days | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Post and sign size | Design for existing poles first; specify a 114.3 x 3.6 mm galvanized post where a new post is needed; the 750 mm sign stays | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Reference rules | FHWA IA-21 as the baseline for indication size and flash pattern, with the pattern configurable for other jurisdictions. The choice of pilot jurisdiction stays open (O1). | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Triggers | Push button plus passive presence detection, with passive detection switchable off where it is not allowed | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Side-to-side link | LoRa radio, not a cable under the road | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Shared components | Reuse the FieldNode radio and logging core (STM32WL-class module, FND-DDR-001 D2) for the controller, run in LoRa point-to-point mode; keep CrossSafe's own 12 V power system; CellGuard is a later option in place of the drop-in battery's BMS; SwapCell not used | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Pedestrian confirmation | Include a small pedestrian-facing pilot light (IA-21 permits one), subject to local rules | Decided by Amish, 2026-09-25: go with recommendation |
| D9 | Pitch and problem | No change was recommended; the pitch and problem lines in `project.yaml` are unchanged | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items open at v0.1 (O2 since decided, O1 still open).*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot partner, site and jurisdiction, including a road authority willing to review the design. The TRL 2 note recommended choosing the jurisdiction early but named none, and no preference was stated. | Proposed, awaiting Amish |
| O2 | Budget for a site trial. The TRL 2 note recommended raising `budget_usd` to $750 for a full two-sided prototype before any site trial. Accepted as a staged budget: $750 applies when a site trial starts, which is TRL 4 or later work and on hold; `budget_usd` stays at $350 for the current stage (D1). CRS-CAL-001 v0.2 costs a crossing at $664.00 on existing poles and $810.00 with new posts. | Decided by Amish, 2026-09-25: go with recommendation (on hold with TRL 4) |

## Consequences

- `project.yaml`: only the TRL fields and the evidence list change. `budget_usd` stays at $350; the pitch and problem are unchanged.
- CRS-PRB-001, CRS-PRC-001 and CRS-REQ-001 are revised to v0.3. The design choices in the precis are no longer described as "proposed"; they are adopted for TRL 3 work pending Amish's review.
- R15 is redefined (D1): parts for one assembly on an existing pole $350 or less, and for a two-sided crossing on existing poles $700 or less; new-post crossings are costed and reported, not held to the target. R1 now refers to the IA-21 pattern and permits the pilot light; R11 names the pilot light; R9 names the adopted post. No other target changes.
- The BOM gains a PIR sensor (line 16) and a pilot light (line 17), and the post line becomes the 114.3 mm new-post variant, excluded from the existing-pole total.
- The TRL 3 calculations (CRS-CAL-001) found two risks, enclosure heat (R8) and sign clamp slip (R9). Their recommendations were accepted on 2026-09-25 and are recorded in CRS-DDR-002.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
