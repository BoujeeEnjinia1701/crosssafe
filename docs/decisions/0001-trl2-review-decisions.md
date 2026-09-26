---
doc_id: CRS-DDR-001
title: CrossSafe TRL 2 review decisions
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
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items D1 to D9 are adopted for TRL 3 work pending Amish's review; items O1 and O2 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis CRS-PRC-001 v0.2 marked every key design choice as proposed. On 2026-09-25 Amish asked for this batch of Design Molecule repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. Nothing here is recorded as decided or approved by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CRS-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Budget scope | Option (a): `budget_usd` ($350) covers one assembly on an existing pole, the prototype for TRL 3 and later bench work; the second side follows later. R15 is redefined to match. `budget_usd` is not changed. The recommended rise to $750 before a site trial is not adopted here; see O2. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Autonomy fix | Gate the radar with a low-power PIR sensor (about $3); the 18 Ah battery is kept as a fallback only; R6 stays at 5 days | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Post and sign size | Design for existing poles first; specify a 114.3 x 3.6 mm galvanized post where a new post is needed; the 750 mm sign stays | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Reference rules | FHWA IA-21 as the baseline for indication size and flash pattern, with the pattern configurable for other jurisdictions. The choice of pilot jurisdiction stays open (O1). | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | Triggers | Push button plus passive presence detection, with passive detection switchable off where it is not allowed | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Side-to-side link | LoRa radio, not a cable under the road | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | Shared components | Reuse the FieldNode radio and logging core (STM32WL-class module, FND-DDR-001 D2) for the controller, run in LoRa point-to-point mode; keep CrossSafe's own 12 V power system; CellGuard is a later option in place of the drop-in battery's BMS; SwapCell not used | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D8 | Pedestrian confirmation | Include a small pedestrian-facing pilot light (IA-21 permits one), subject to local rules | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D9 | Pitch and problem | No change was recommended; the pitch and problem lines in `project.yaml` are unchanged | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot partner, site and jurisdiction, including a road authority willing to review the design. The TRL 2 note recommended choosing the jurisdiction early but named none, and no preference was stated. | Proposed, awaiting Amish |
| O2 | Budget for a site trial. The TRL 2 note recommended raising `budget_usd` to $750 for a full two-sided prototype before any site trial. The figure is recorded here and in `docs/REVIEW.md`; `budget_usd` stays at $350. CRS-CAL-001 costs a crossing at $636.00 on existing poles and $776.00 with new posts. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields and the evidence list change. `budget_usd` stays at $350; the pitch and problem are unchanged.
- CRS-PRB-001, CRS-PRC-001 and CRS-REQ-001 are revised to v0.3. The design choices in the precis are no longer described as "proposed"; they are adopted for TRL 3 work pending Amish's review.
- R15 is redefined (D1): parts for one assembly on an existing pole $350 or less, and for a two-sided crossing on existing poles $700 or less; new-post crossings are costed and reported, not held to the target. R1 now refers to the IA-21 pattern and permits the pilot light; R11 names the pilot light; R9 names the adopted post. No other target changes.
- The BOM gains a PIR sensor (line 16) and a pilot light (line 17), and the post line becomes the 114.3 mm new-post variant, excluded from the existing-pole total.
- The TRL 3 calculations (CRS-CAL-001) found two risks that need Amish's decision: enclosure heat (R8) and sign clamp slip (R9). They are listed in `docs/REVIEW.md` as proposed and are not decided by this record.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
