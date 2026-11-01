---
doc_id: CRS-PLN-001
title: CrossSafe project plan
project: CrossSafe
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "First project plan (kit 1.9.1 upgrade); P4 to P6 shown as planned work only, on hold under the stage cap"
---

# CrossSafe project plan

The repo is at stage P3 (TRL 3, constructable design on paper, every option modelled at D3). The next gate is Amish's decision on the concept (O1) and the open items O2 to O4; nothing past TRL 3 is planned for execution while the portfolio cap holds. Method: STANDARDS sections 19 and 23.

## Workstreams

*Table 1. Workstreams.*

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and calculations | Design lead | CRS-CAL-001 v0.7, CRS-STM-001, CRS-OPT-001 | Done at P3 |
| CAD at D3 for every option | Design lead | `cad/src/model.py`, `cad/fidelity.json`, STEP files | Done at P3 |
| Requirements and traceability | Design lead | CRS-URS-001, CRS-PRS-001, CRS-RTM-001 | Done at P3 |
| Build plan | Design lead | CRS-BLD-001 (paper) | Done at P3 |
| Regulatory, risk, market | Design lead | CRS-REG-001, CRS-RSK-001, CRS-MKT-001 | First pass; many rows "to assess" |
| Decisions | Amish | O1 to O4 in CRS-DEC-001 | Awaiting Amish |

## Resources needed

*Table 2. Resources for the planned stages (estimates, to assess; not authorised).*

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Pilot road authority contact | Rules, site, permit (P4) | 2 weeks elapsed | To assess |
| Workshop with sheet-metal tools | Prototype build (P4) | 3 weeks | 364 parts plus labour |
| Photometry and thermal tests | Intensity, flash area, battery temperature (P4) | 2 weeks | To assess |
| Clinical-safety reviewer | Flash area review (H5) | 1 day | To assess |

## Stage gates

*Table 3. Stages (P4 to P6 on hold while the stage cap is P3).*

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P3 | Constructable design, calculations, every option at D3, STEM check, options, requirements, registers | This repo, awaiting Amish's review |
| P4 | Prototype build and bench test | On hold (planned only) |
| P5 | Site trial at a pilot crossing | On hold (planned only) |
| P6 | Release and documentation of a tested design | On hold (planned only) |

## Next steps and decision requested

Amish is asked to decide O1 (concept: A, C or both), O2 (55 C battery limit), O3 (flash area) and O4 (cost over target), all in CRS-DEC-001. The recommended next step is to review them and then ask the portfolio whether CrossSafe is ready for TRL 4; this note does not start it.

## References

- FHWA, IA-21 and RRFB countermeasure pages (CRS-PRB-001).
- Carmanah, BLT Direct and Kirkland pages (CRS-MKT-001).
- U.S. Access Board, Chapter 3: Operable Parts (CRS-REG-001).
