---
doc_id: CRS-PRC-001
title: CrossSafe design precis
project: CrossSafe
doc_type: Design precis
version: "0.5"
status: Draft
date: '2026-09-25'
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
  change: TRL 2 concept (how it works, components, first-order numbers, safety, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; design choices adopted for TRL 3 work (CRS-DDR-001), PIR gating, pilot light, 114.3 mm post, numbers from CRS-CAL-001, model and drawing CRS-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: Constructable design (CRS-DDR-003) with keyed saddles and bands for every part on the pole, mounting plate, radar arm, panel bracket and rails; numbers from CRS-CAL-001 v0.3
---

# CrossSafe design precis

## Summary

CrossSafe is a pair of pole-mounted, solar-powered warning beacons, one on each side of an unsignalized crossing. When a pedestrian presses the button or a small radar sensor sees someone waiting at the kerb, both assemblies flash two amber lights per face under the crossing warning sign for about 13 s, and a small pilot light confirms to the pedestrian that the warning is on. Each assembly runs from a 20 W panel and a 12.8 V 12 Ah LiFePO4 battery, a low-power PIR sensor switches the radar on only when something moves nearby, and the two sides stay in step over a short LoRa link, so no trench or cable across the road is needed. The TRL 3 calculations (CRS-CAL-001) give 16.0 Wh/day of use at 300 activations, 7.7 days without sun, and $360.00 in parts for one assembly on an existing pole, $10.00 over its budget after the parts that make the design buildable (CRS-DDR-003). A ventilated sun shield keeps the battery below its discharge limit, and an anti-rotation bolt (new posts) or keyed saddles (existing poles) stop the sign turning in a storm; only poles under about 70 mm remain at risk.

The concept follows the rectangular rapid flashing beacon (RRFB), which FHWA lists as a proven safety countermeasure ([FHWA](https://highways.dot.gov/safety/proven-safety-countermeasures/rectangular-rapid-flashing-beacons-rrfb)), and uses the US Interim Approval IA-21 as its reference for light size, flash pattern, night dimming and the optional pilot light ([FHWA IA-21](https://mutcd.fhwa.dot.gov/resources/interim_approval/ia21/index.htm)). It is an open reference design, not a certified traffic control device.

![Figure 1. Hero render: one CrossSafe assembly on the near sidewalk of a 7 m two-lane crossing, the far-side assembly in grey, and a 1.75 m person for scale.](../media/hero.png)

## How it works

1. **Idle.** The controller sleeps with its radio listening, the button is armed, and a PIR sensor watches for movement near the kerb. When the PIR sees motion it switches on the radar, which watches a waiting zone of about 1.5 x 2 m; the radar goes off again when nothing has moved for a set time. Passive detection can be switched off where it is not allowed. The battery charges from the panel.
2. **Trigger.** A button press, or a person detected in the waiting zone for 1 s or more, wakes the controller.
3. **Synchronize.** The controller sends a short LoRa packet to the far-side assembly (and listens for the same from it). Both start flashing within 48 ms, or 244 ms if two packets are lost (CRS-CAL-001).
4. **Warn.** Two amber heads per face flash in the IA-21 wig-wag sequence, 75 sequences per minute, for the site's set time (crossing length / 0.9 m/s + 5 s, 12.8 s for 7 m), dimmed at night. A new trigger extends the time. The pilot light on the kerb end of the light bar confirms to the pedestrian that the warning is on, and the button gives a click and a tactile pulse.
5. **Log.** The controller counts activations and records faults and battery state. It stores no images or audio; the radar reports presence only.

Figure 2 shows the daily energy flow and Figure 3 the parts. The general arrangement is drawing CRS-DWG-001 (`cad/drawings/`), generated from the parametric model `cad/src/model.py`.

![Figure 2. Daily energy flow for one assembly, Wh per day. All values are CRS-CAL-001 estimates (2.5 peak sun hours, 300 activations of 20 s).](../media/flow.png)

![Figure 3. Exploded view of one assembly; callout numbers match `bom/bom.csv`.](../media/exploded.png)

## Main components

Table 1. Components of one assembly. Numbers match the exploded view and `bom/bom.csv` (line 15, wiring, glands and fixings, has no callout). Each part is made and fitted as the build plan CRS-BLD-001 (`docs/05-build-plan.md`) shows.

| No. | Component | Concept choice |
| --- | --- | --- |
| 1 | Crossing warning sign | 750 mm diamond, retroreflective, local sign design |
| 2 | Light bar housing | Folded 2 mm aluminium channel with a screwed bottom cover and riveted end caps, double sided, 720 x 130 x 70 mm, bottom at 2.1 m |
| 3 | LED heads (4) | Amber, 140 x 62 mm lens (127 x 51 mm minimum), two per face, with daylight and night levels |
| 4 | Push-button station | Vandal-resistant piezo button with acknowledgement tone and tactile arrow, instruction plate, at about 1.0 m |
| 5 | Presence radar | 24 GHz presence sensor on the radar arm (22) at 2.6 m, aimed at the waiting zone, powered only when the PIR sees motion |
| 6 | Solar panel | 20 W monocrystalline, about 500 x 360 mm, tilted about 30 degrees toward the equator |
| 7 | Panel bracket | Welded steel socket, cap and cheeks on the post top, with two aluminium rails and a 20 to 40 degree tilt slot |
| 8 | Enclosure | IP65 polycarbonate, 150 x 260 x 300 mm, membrane vent, internal plate, lug kit, 2.85 to 3.15 m, behind the post on its mounting plate (21) |
| 9 | Battery | LiFePO4 12.8 V 12 Ah (about 154 Wh) with internal BMS |
| 10 | Charge controller | Small MPPT controller with a LiFePO4 profile and low-temperature charge cut-off |
| 11 | Controller and radio board | FieldNode radio core (STM32WL-class LoRa module) in point-to-point mode, four LED drivers with night dimming, real-time clock, fault indicator |
| 12 | Antenna | Short whip on the enclosure roof |
| 13 | Band clamps | Eight 19 x 0.76 mm stainless bands with buckles, one at each saddle |
| 14 | Post | Existing pole first; where a new post is needed, 114.3 x 3.6 mm galvanized steel, 3.7 m above the sidewalk, 1.8 m in a 500 mm footing |
| 16 | PIR wake sensor | Low-power passive infrared sensor under the radar; switches the radar on |
| 17 | Pedestrian pilot light | Small amber light on the kerb end of the light bar, where local rules allow |
| 18 | Sun shield | Ventilated white aluminium shield over the enclosure roof and three walls, 25 mm air gap, open at the bottom |
| 19 | Anti-rotation bolt | M10 stainless bolt through the sign, the upper sign saddle and the post; new posts only |
| 20 | Keyed pole saddles | Eight identical aluminium blocks with a keyed 120 degree V, a band groove and two M8 holes; every part on the pole bolts to one; fit 60 to 114.3 mm poles |
| 21 | Enclosure mounting plate | 4 mm aluminium, 350 x 300 mm with saddle tabs above and below; carries the enclosure lugs and the sun shield |
| 22 | Radar arm | 40 x 5 mm aluminium bar bent to an L, on its own saddle; radar on top, PIR underneath |
| 23 | Battery strap | Bent aluminium strip holding the battery on the enclosure floor |

![Figure 4. Cutaway of the pole-top enclosure and sun shield: battery low, charger and controller above, antenna through the shield roof.](../media/cutaway.png)

## Key design choices

Each choice below was decided by Amish on 2026-09-25 by accepting the recommendations (CRS-DDR-001 and CRS-DDR-002).

- **RRFB-style amber beacons, not a signal (D4).** Amber warning lights with the standard sign ask drivers to yield; they do not claim to stop traffic, which keeps the device in a simpler approval class in most places. IA-21 is the baseline; the flash pattern is configurable for other jurisdictions.
- **Button plus passive detection, gated by a PIR (D2, D5).** The button is the reliable, accessible trigger; radar catches people who do not press it and can be switched off where passive detection is not allowed. The PIR keeps the radar off when nothing moves, which is what brings autonomy above 5 days. The radar reports presence only, which keeps images and audio off the device.
- **Radio sync instead of a cable (D6).** A LoRa point-to-point link avoids cutting the road. If the link drops, each side still flashes on its own trigger and reports a fault.
- **Own 12 V power system, FieldNode radio core (D7).** The LED load (up to about 26 W at the instant all four heads are lit) is far beyond the FieldNode power stage (6 W panel, 3.2 V cell), so CrossSafe uses a 12.8 V LiFePO4 battery with a built-in BMS. The controller reuses FieldNode's STM32WL-class radio and logging design. CellGuard, the lab's open BMS for 4 to 16 LiFePO4 cells, is a later option in place of the drop-in battery's closed BMS.
- **Existing poles first; 114.3 mm where a new post is needed (D3).** Band clamps fit 60 to 114.3 mm poles; the new-post variant meets the wind target with margin.
- **Pedestrian pilot light (D8).** IA-21 permits a small pilot light on the beacon or push button; it is included where local rules allow.
- **Sun shield on the enclosure (CRS-DDR-002).** A ventilated white shield cuts the enclosure's rise in full sun from 14.7 to 3.9 K when dusty, so the battery stays below its discharge limit and keeps charging on hot days. Placing the enclosure in the panel's shadow is to be considered when the bracket is detailed.
- **Anti-rotation detail (CRS-DDR-002).** An M10 through-bolt locks the sign and its upper saddle to a new post; on existing poles, where drilling needs the owner's consent, keyed saddles with serrated grip faces raise the clamp friction. Band tension and grip are to be measured at TRL 4, which is on hold.
- **One way of fixing everything to the pole (CRS-DDR-003).** Eight identical keyed saddles, each pulled onto the pole by a stainless band that runs across its front, carry the sign, light bar, button, instruction plate, radar arm and enclosure; each part bolts to its saddle over the band. The design is open for Amish's review.
- **Electronics high on the pole.** The enclosure bottom at 2.85 m and the panel at the top deter theft and keep cables out of reach.

## Key numbers (CRS-CAL-001)

The TRL 2 first-order estimates have been replaced by the TRL 3 calculation note CRS-CAL-001, which states every assumption and prints every figure from `docs/04-calcs/sizing.py`. The main results:

- **Flash time.** 12.8 s for a 7 m crossing; the energy case uses 20 s, enough for crossings up to 13.5 m.
- **Energy.** Each head is lit 25 % of each IA-21 sequence, so the LEDs use 10.99 Wh/day at 300 activations. Standby is 187 mW (4.49 Wh/day) with the PIR gating the radar. The daily load is 16.0 Wh, against 38.0 Wh stored in the worst month; break-even is 1.05 peak sun hours, and the battery refills from 20 % in 2.05 days at 5 peak sun hours.
- **Autonomy.** 122.9 Wh usable gives 7.7 days without sun, 5.4 days at -20 °C and 6.2 days at end of life.
- **Heat.** Unshielded, the enclosure would run 9.6 K (clean) to 14.7 K (dusty) above ambient in full sun and a dusty box would reach 64.7 °C at 50 °C ambient. With the sun shield the rise is 3.9 K: 53.9 °C inside at 50 °C ambient, and charging continues up to 41.1 °C ambient (R8 met on paper).
- **Latency and link.** 48 ms side to side, 244 ms with two retries; about 60 dB of link margin across the road with a bus in the way.
- **Wind.** A 40 m/s gust gives 3.52 kN·m at the base. The 114.3 x 3.6 mm post reaches 105 MPa, 45 % of S235 yield; an 88.9 x 4 mm post would reach 65 %. The sign's 175 N·m of torsion is carried by the through-bolt on new posts (12 % of bearing) and by keyed saddles on existing poles of about 70 mm and larger; smaller poles remain at risk (R9). A 500 mm footing needs about 1.8 m of embedment in clay (screening).
- **Cost.** $360.00 per assembly on an existing pole ($350 budget, so R15 is not met on paper) and $720.00 per crossing; $433.00 and $866.00 with new posts (see `bom/bom.csv`). Raising the budget to $375 is proposed, awaiting Amish (`docs/06-design-decisions.md`). The $750 budget for a two-sided site trial is accepted and applies when a trial starts (on hold with TRL 4).

## Safety

> **Safety:** CrossSafe is a research prototype. A traffic control device must meet local standards and have road authority approval before use on a public road. A beacon that fails dark, flashes when no one is there, or gives pedestrians false confidence can cause harm; pedestrians must still check that drivers have stopped.

> **Safety:** Lithium cells can overheat, vent and burn. Use LiFePO4 with a BMS, fuse the battery output close to the terminal, charge only between 0 and 45 °C cell temperature, and shade the enclosure. Never charge a damaged or swollen battery.

> **Safety:** Installing on a pole next to live traffic is work at height and work in the road. Use trained crews, traffic management and fall protection as local rules require, keep clear of overhead power lines, and mount only with the asset owner's permission. A post, sign or panel that falls can kill. CRS-CAL-001 is a screening check only: clamp torsion is at risk on poles under about 70 mm, and a qualified engineer must check the post, clamps, footing or host pole to the local code before installation.

> **Safety:** Sign and panel edges are sharp and heavy; handle with gloves and a second person.

## Open questions

- [ ] Pilot jurisdiction and its rules for beacon color, flash pattern, sign design and mounting height.
- [ ] Measured LED head power and intensity for the chosen modules, and whether 6 W per head is enough in full sun.
- [ ] Radar false-trigger rate with passing pedestrians, cyclists, animals and rain.
- [ ] Radio range and reliability across the road with parked vehicles and buses in the path, and licence-free band rules in the pilot country.
- [ ] Measured enclosure temperature in full sun with the shield fitted, and whether the enclosure can sit in the panel's shadow (CRS-CAL-001, section C).
- [ ] Measured band tension and keyed saddle grip, and the fix for poles under about 70 mm (R9; CRS-DDR-002, N1); host pole checks by the owner; local foundation design.
- [ ] Whether the pedestrian-facing confirmation light is allowed locally.
