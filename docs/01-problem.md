---
doc_id: CRS-PRB-001
title: CrossSafe problem statement
project: CrossSafe
doc_type: Problem statement
version: "0.4"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; budget scope per CRS-DDR-001 D1, IA-21 details checked, open questions linked to CRS-DDR-001
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# CrossSafe problem statement

Pedestrians die at unsignalized crossings, and full traffic signals are costly and slow to approve. A driver who does not see a waiting pedestrian, or sees them too late, does not yield. CrossSafe is an open, solar-powered beacon that warns drivers only when someone is actually waiting to cross, at crossings near schools, markets and bus stops that will not get a full signal. Design with, not for: requirements must come from co-design sessions with road users and the road authority through a local partner.

## The problem

About 1.19 million people die on the world's roads each year, and pedestrian deaths rose 3 % to about 274,000 between 2010 and 2021, 23 % of the total ([WHO, 2023](https://www.who.int/news/item/13-12-2023-despite-notable-progress-road-safety-remains-urgent-global-issue)). Nine in ten road deaths occur in low- and middle-income countries ([WHO, 2023](https://www.who.int/news/item/13-12-2023-despite-notable-progress-road-safety-remains-urgent-global-issue)), and road traffic injuries are the leading cause of death for children and young people aged 5 to 29 ([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries)).

High-income countries are not exempt. In the United States, 7,314 pedestrians were killed in 2023; 74 % of those deaths happened away from intersections and 77 % in the dark ([NHTSA, 2025](https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813727)). In Great Britain, pedestrians were 25 % of the 1,624 road deaths in 2023 ([Department for Transport](https://www.gov.uk/government/statistics/reported-road-casualties-great-britain-annual-report-2023/reported-road-casualties-great-britain-annual-report-2023)).

The marked crossing without a signal is where the pedestrian's right of way and the driver's attention most often fail to meet. Three gaps make it hard to fix:

1. **Cost and approval.** A full signal needs a mains connection, a cabinet, foundations and an engineering study. Many crossings will never qualify or be funded.
2. **Static signs fade into the background.** A sign that is always there says nothing about whether someone is waiting now. Warning lights that flash all day teach drivers to ignore them.
3. **Power and maintenance.** Many crossings that need help are on roads without a convenient mains supply, and closed commercial beacons are expensive to buy and hard to repair locally.

There is good evidence that an active, pedestrian-triggered warning works. The US Federal Highway Administration lists the rectangular rapid flashing beacon (RRFB) as a proven safety countermeasure that can reduce pedestrian crashes by up to 47 % and raise driver yielding rates to as high as 98 %, depending on speed, lanes, crossing distance and time of day ([FHWA](https://highways.dot.gov/safety/proven-safety-countermeasures/rectangular-rapid-flashing-beacons-rrfb)). CrossSafe asks whether an open, solar, garage-buildable design can bring that kind of device to crossings and communities that cannot buy one today.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Pedestrian, including children, older people and people with disabilities | Cross safely, with drivers stopping; clear confirmation that the warning is on | School run, market days, bus stops, often at dusk or in the dark |
| Driver | Early, unmistakable warning only when someone is waiting | Urban and peri-urban roads, 30 to 60 km/h, glare and rain |
| School or market community | A safer crossing without waiting years for a signal | Parent groups, school boards, market associations as local champions |
| Road authority or municipal engineer | A device that meets local rules, is reliable, and costs little to maintain | Approval, installation permits, asset registers |
| Local technician | Install, service and repair with ordinary tools and parts | Hand tools, a ladder or bucket truck, a multimeter |

### Operating environment

- **Site:** a marked, unsignalized crossing on a two-lane road, about 7 m kerb to kerb, with a sidewalk or verge on each side. Wider roads need a median assembly (out of scope for the first concept).
- **Climate:** ambient -20 to +50 °C across target regions, direct sun on the enclosure, heavy rain, dust and road spray.
- **Power:** no mains assumed; solar resource from about 2.5 peak sun hours per day in a poor month (estimate for mid latitudes and tropical rainy seasons) upward.
- **Use:** up to about 300 activations per day at a busy school or market crossing (estimate, to be checked in co-design and site counts).
- **Threats:** theft of panels and batteries, vandalism, vehicle strikes on the pole.

## Constraints

- Garage-buildable prototype of one beacon assembly on an existing pole, a value-engineering target of $350 USD in parts (`project.yaml`; scope adopted for TRL 3 in CRS-DDR-001 D1, open for Amish's review). A crossing needs two assemblies; a value-engineering target of $750 applies to a two-sided site trial when one starts (CRS-DDR-002, O2).
- Built from off-the-shelf parts: standard signs, LED modules, a small solar kit, a LiFePO4 battery, an IP65 box and a common microcontroller.
- Needs road authority approval before any use on a public road. Local rules on colors, flash patterns, sign design and mounting heights take precedence over anything in this repo.
- Privacy: counts and activation events only; no images or audio are recorded or leave the device.

## Out of scope

- Full traffic signals, pedestrian hybrid beacons and any device that shows a red indication or stops traffic.
- Enforcement features such as speed cameras.
- Crossings of more than one lane per direction, where a beacon alone is not enough and a median refuge or signal is usually needed.
- Certification to any national standard; the repo can only document how the design relates to one.

## Prior work

- **RRFB.** Amber, rectangular, pedestrian-activated beacons mounted with the crossing warning sign. In the United States they are covered by FHWA Interim Approval IA-21 (20 March 2018), which sets the minimum indication size (at least 5 in wide by 2 in high), daytime intensity to the SAE J595 Class 1 yellow peak, a wig-wag flash pattern at 75 flashing sequences per minute, automatic night dimming, pushbutton or passive detection, an optional pilot light for pedestrians, and use only at uncontrolled marked crosswalks ([FHWA IA-21](https://mutcd.fhwa.dot.gov/resources/interim_approval/ia21/index.htm)). Solar RRFBs are sold commercially; they are closed designs.
- **Evidence of effect.** FHWA's proven safety countermeasure summary for RRFBs (see above) gives the crash and yielding figures used in this repo.
- **Sibling designs in the lab.** FieldNode (a sibling Design Molecule repo) is the lab's shared solar sensor node (6 W panel, 3.2 V LiFePO4 cell, LoRaWAN). Its radio and logging core (an STM32WL-class module) is reused for the CrossSafe controller, but its power stage is too small for the LED load; see CRS-PRC-001 and CRS-DDR-001 D7.

## Open questions

- [ ] Which pilot country and road authority, and which rules apply there (colors, flash pattern, sign type, mounting height)? Open, awaiting Amish (CRS-DDR-001 O1).
- [ ] Is passive detection allowed and trusted locally, or should the button be the only trigger?
- [ ] How many activations per day at the candidate sites, and how dark are they at the busy times?
- [ ] How much theft and vandalism should the design expect, and at what mounting height is the battery safe?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
