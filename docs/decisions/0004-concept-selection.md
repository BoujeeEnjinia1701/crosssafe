---
doc_id: CRS-DDR-004
title: CrossSafe concept selection
project: CrossSafe
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "Concept options A, B and C scored against CRS-URS-001 (kit 1.9.1 upgrade); A and C within 10 %, both to Amish; proposed, awaiting Amish"
---

# 0004: Concept selection

- **Date:** 2026-10-31
- **Status:** proposed, awaiting Amish. Option A continues unchanged until he decides.

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements. CrossSafe was designed as one concept (the pole-top beacon). It is option A and is not redesigned. Two options with other working principles were added and all three were modelled to D3 (`cad/fidelity.json`): B moves the warning to road level with a kerbside bollard and solar studs, and C removes the electronics with a pull-up retroreflective panel. The full numbers and the scoring are in CRS-OPT-001.

## Options considered

*Table 1. Options and weighted scores (maximum 185).*

| Option | Principle | Parts | Mass | Cost (USD) | Score | Share |
| --- | --- | --- | --- | --- | --- | --- |
| A | Pole-top flashing beacon with detection | 117 | 27.6 kg | 364.00 (BOM) | 138 | 74.6 % |
| B | Kerbside solar bollard with in-road studs | 156 | 45.5 kg | about 400 (estimate) | 108 | 58.4 % |
| C | Pull-up retroreflective panel, no electricity | 40 | 10.9 kg | about 70 (estimate) | 128 | 69.2 % |

## Decision

Proposed, awaiting Amish: A and C are within 10 % (C is 7.2 % lower), so both go to him without a pick. The author leans to A, because it alone detects, confirms and warns on both sides, which is what the evidence of effect (FHWA) rests on, and because it is the design all TRL 3 work covers. C is the better answer for a crossing with no budget, and B is not recommended. No document, drawing or BOM changes if Amish keeps A. If he picks C, the BOM, build plan and calculations are redone for C at TRL 3, and the repo's pitch changes from a detecting beacon to a low-cost warning aid (a change of pitch, which is his decision).

## Consequences

`project.yaml` keeps `concept_chosen` unset and lists the options. The scoring is the author's judgment and sensitive to the weight of cost (A leads at every weight; the gap is 12 % at weight 1 and 5 % at weight 4). The costs of B and C are estimates by analogy with the BOM of A. Co-design would test the scores for UR-001 and UR-006 first.
