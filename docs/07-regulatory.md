---
doc_id: CRS-REG-001
title: CrossSafe regulatory and standards register
project: CrossSafe
doc_type: Regulatory register
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "First register (kit 1.9.1 upgrade); nothing verified by a qualified reviewer; unknowns marked to assess"
---

# CrossSafe regulatory and standards register

Which standards and regulations apply, where, and what is needed. The design follows the US FHWA RRFB interim approval (IA-21) for its form; every other row is "to assess" until a qualified reviewer and the pilot road authority have been asked. Not legal advice; CrossSafe is a research and educational prototype and makes no claim of compliance with any standard. Method: STANDARDS section 23. Sources and the date they were checked are listed at the end.

*Table 1. Regulatory and standards register.*

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | FHWA Interim Approval IA-21, rectangular rapid flashing beacons | United States | Indication size (at least 5 x 2 in), SAE J595 class 1 yellow intensity, wig-wag pattern at 75 sequences a minute, mounting | Design basis of PR-001; whether IA-21 is still in force after the MUTCD 11th Edition is not checked | Design lead | To assess |
| G2 | Manual on Uniform Traffic Control Devices (MUTCD) | United States | Sign designs, beacon rules, mounting heights, state supplements | Local rules decide colours, pattern and heights | Pilot road authority | To assess |
| G3 | ADA Standards, operable parts (section 309) | United States | Operable force of 5 lbf (22.2 N) or less, reach range | Push button 0.9 to 1.1 m, 22 N or less (PR-011) | Design lead | Met by design (button not built) |
| G4 | Public right-of-way accessibility guidelines (accessible pedestrian signals) | United States | Audible and tactile pedestrian signals | Button tone and tactile arrow (PR-011) | Design lead | To assess |
| G5 | ASTM D4956, retroreflective sheeting for traffic control | United States | Sheeting classes and performance | The sign sheeting is bought to the local authority's design (CRS-DEC-001) | Pilot road authority | To assess |
| G6 | AASHTO structural supports specification for highway signs, luminaires and traffic signals | United States | Wind loads and support design | 40 m/s gust screening in CRS-CAL-001 section G | Structural reviewer | To assess |
| G7 | 47 CFR Part 15, unlicensed radio | United States | 902 to 928 MHz radios | The sizing assumes 868 MHz; a US pilot needs a 915 MHz radio and a recheck of the link budget | Design lead | To assess |
| G8 | ETSI EN 300 220, short range devices | European Union | Sub-GHz radio, duty cycle (1 % in the 868 MHz sub-band) | Duty cycle 4.3 s against 36 s per hour (STEM check S8) | Design lead | Met by design (paper) |
| G9 | EN 12368 (traffic signals) and EN 12899-1 (fixed vertical signs) | European Union | Signal heads and signs | Applicable only to an EU pilot | Pilot road authority | To assess |
| G10 | IEC 60529, IP code | International | Ingress protection, IP65 | Enclosure and connectors IP65 or better (PR-008) | Design lead | Met by design (datasheet) |
| G11 | UN 38.3 and IEC 62619, lithium batteries | International | Transport tests and safety of industrial lithium cells | The pack is bought; its certificates are to be requested | Design lead | Certification needed later |
| G12 | RoHS Directive 2011/65/EU | European Union | Hazardous substances in electronics | Bought electronics; own board not designed | Design lead | To assess |
| G13 | IEC 62471, photobiological safety of lamps | International | Blue light and retinal hazard classes | LED heads at 3.9 kcd peak; flash area is hazard H5 | Design lead | To assess |
| G14 | Privacy and data protection law of the pilot jurisdiction | Pilot jurisdiction | Personal data | No images or audio; counts only (PR-013) | Design lead | Does not apply by design; confirm with the authority |
| G15 | Local road authority rules and permits | Pilot jurisdiction | Colours, flash pattern, heights, installation permit, pole permission | Decides whether the device may go on a public road | Pilot road authority | To assess |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- FHWA, [Interim Approval IA-21](https://mutcd.fhwa.dot.gov/resources/interim_approval/ia21/index.htm), 20 March 2018, as cited in CRS-PRB-001; current status not checked.
- U.S. Access Board, [Chapter 3: Operable Parts](https://www.access-board.gov/ada/guides/chapter-3-operable-parts/), checked 2026-10-31.
- All other rows name a standard from general knowledge; no link was checked and the edition and clause numbers are not given. They are "to assess" for that reason.
