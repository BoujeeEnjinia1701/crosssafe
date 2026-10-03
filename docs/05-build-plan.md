---
doc_id: CRS-BLD-001
title: CrossSafe prototype build plan
project: CrossSafe
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: First build plan; design made constructable (CRS-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target; cross-references updated
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Bezels and visors on the LED heads, cost $364, pole range 76 to 114.3 mm, no open decisions; pictures of joint 1, steps 1, 2, 9 and 10, the overview and CRS-DWG-101 regenerated
---

# CrossSafe prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions are recorded in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart, numbered in build order and laid out by group.*

The prototype is one CrossSafe assembly, the existing-pole kit, built on a 3.7 m test post of 114.3 x 3.6 mm steel tube that stands in for a site's pole. A crossing warning sign with an amber light bar under it faces the traffic; a push-button station and a radar on a short arm face the kerb; a grey plastic enclosure holding the battery, charger and controller hangs on the back of the pole under a white sun shield; and a solar panel sits on a bracket on the post top. Figure 1 shows the 24 components in the order you make or fit them. Nine are made in a small workshop: the light bar housing, the battery strap, the enclosure mounting plate, two panel rails, eight identical pole saddles, the radar arm, the welded panel bracket and the folded sun shield; the bought enclosure is drilled. Everything else is bought and fitted: the sign, LED heads, pilot light, push-button station and its plate, radar, PIR sensor, panel, battery, charger, controller, glands and stainless bands. The work is sawing, drilling, tapping, filing and folding aluminium bar and sheet, one small steel weldment, drilling a plastic box, and wiring bought modules together with screw terminals. The parts cost about $364 from the bill of materials.

Every part on the pole is held the same way: a saddle with a V in its back sits on the pole, a stainless band runs round the pole and across the saddle's front, and the part bolts to the saddle over the band.

> **Safety:** The prototype holds a 12.8 V lithium iron phosphate battery of about 154 Wh. Keep the battery out of the enclosure and its fuse out of the fuse block until section 6 says otherwise, never charge it below 0 °C or above 45 °C, and never leave a first build charging unattended. The test post weighs about 37 kg and the finished assembly about 30 kg more: build it lying on trestles, and stand it up only as section 6 allows. Sign, sheet and panel edges are sharp: deburr everything and wear gloves. Welding and hot-dip galvanizing are for a trained welder and a galvanizer; never weld galvanized steel indoors.

## 2. What changed to make it buildable

The concept showed what the beacon does; most of its parts were not fixed to anything. Each change below keeps what CrossSafe does, at the same heights, and all of them are recorded in decision record CRS-DDR-003, which Amish accepted on 2 October 2026.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Pole clamps | Rings 8 mm thick drawn through every bracket; each bracket touched the round pole on one line | Eight identical keyed saddles with a V in the back, and a 19 mm stainless band round the pole and across each saddle's front (Figures 15 and 16) | The band pulls the V onto the pole; one saddle fits poles from 76 to 114.3 mm, the range this kit is used on |
| Sign | Standing 92 mm in front of the pole on two solid blocks | Flat on the front of its two saddles, 63 mm nearer the pole, two bolts into each (Figure 18) | The saddle is the stand-off |
| Light bar | A solid box on a block touching the pole on one line; heads stuck on its faces | A folded channel with a screwed bottom cover and riveted end caps; heads through cut-outs; bolted to its saddle from inside (Figures 2, 3 and 17) | A housing that can be made, opened and sealed |
| Enclosure | Held off the pole by a block touching it on one line; battery, charger and controller floating inside | Hung by its lugs on a mounting plate bolted to two saddles; modules on the box's internal plate; battery under a strap (Figures 4 to 11) | Every part has a fixing; the box back stays sealed |
| Enclosure saddles | (Found in checking) bolts that would be hidden behind the box | Saddles on tabs above and below the box (Figure 12) | The enclosure, plate and shield go on and off as one unit |
| Sun shield | No fixing | Side flanges screwed to the mounting plate (Figure 25) | Air gap and open bottom unchanged |
| Radar | On a rod touching the pole on one line | On a bent aluminium arm on its own saddle, PIR underneath (Figure 21) | A part that can be bent and bolted |
| Panel bracket | A sleeve, a block and a tilt plate that touched neither the block nor the panel | A welded socket, cap and two cheeks; two rails on the panel frame, a pivot bolt and a tilt slot (Figures 14, 22 and 23) | Every joint face to face and bolted; tilt 20 to 40° |
| Button and its plate | Touching the pole on one line; the plate with no fixing | Each on its own saddle | The eighth saddle |
| Enclosure bottom | No gland positions; gland nuts under the battery | Four glands in two rows beside the battery; the vent at the lid end (Figures 5 and 6) | Room for every nut |

The parts added for construction and the bezels and visors on the LED heads take the parts cost from $332 to $364.

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Traffic side" is the side the sign faces; "kerb side" is the side the button and radar face; the enclosure is on the "back" of the pole. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Light bar housing

![Figure 2. Making sketch of the light bar housing](../cad/drawings/CRS-DWG-101.png)

*Figure 2. Light bar housing making sketch (CRS-DWG-101).*

**What it is and what it is made from.** The double-sided box under the sign that carries two amber LED heads on each face, each with a bezel frame and a hood visor, and the pilot light on its kerb end. Aluminium sheet 2 mm, 5052 class, in three parts: a folded channel, a bottom cover and two end caps. Outside size 720 long, 70 deep and 130 tall.

**How to make it.**

1. Cut the channel blank 716 x 346. Mark the fold lines across the 346: 10, 138, 208 and 336 from one edge. Make a test bend in an offcut first and move the lines if your folder's bend allowance differs.
2. Before folding, cut the four head windows, 128 wide and 50 tall: two in each wall, centred 200 each side of the middle of the length and 65 up from what will be the underside of the bar. Drill the corners 6 mm and cut between them with a jigsaw and a fine metal blade; file straight.
3. In the back wall, drill two 9 mm holes on the middle of the length, 45 and 85 up from the underside. These take the bolts to the saddle.
4. Fold the 10 lip, the 128 back wall, the 70 top, the 128 front wall and the other 10 lip, all 90° the same way, so both lips point inward.
5. Fit four M4 rivet nuts in each lip, about 100 apart, to take the cover screws.
6. Cover: cut 70 x 716, drill a 16 hole for the cable gland 60 from the middle toward the road-side end (the end away from the pilot light), and drill clearance holes to match the rivet nuts.
7. End caps: cut two blanks 70 x 130 with a 15 flange on three sides (top, front and back), fold the flanges in, and rivet each cap into the channel ends with two 3.2 rivets per flange. In the kerb-end cap, drill a 22 hole at the centre for the pilot light.

**How it fits the parts next to it.**

![Figure 3. Joint 1: the LED heads, bezels and visors on the light bar walls](05-build-plan/joint-01.png)

*Figure 3. Each head's flange sits on the outside of its wall over the window; its body goes inside, and its bezel and visor are already on it.*

Each head's flange, 140 x 62, sits flat on the outside of its wall and overlaps the 128 x 50 window by 6 all round; four M4 screws through the flange and the wall hold it. The bezel frame is 7 wide round the flange, and the visor sits on top of it and reaches 26 out from the wall, with a 15 high lip at its outer edge that sheds rain from the lens. The two bodies facing each other inside the bar are 16 apart. The back wall sits flat on its saddle (Figure 17); the cover seats on both lips with a foam gasket and comes off to reach the two saddle bolts.

**Check before moving on.** The channel is square along its length within 1 mm; the cover seats on both lips without gaps; each head flange covers its window all round.

### 3.2 Enclosure body, drilled

![Figure 4. Drilling sketch of the enclosure body](../cad/drawings/CRS-DWG-102.png)

*Figure 4. Enclosure drilling sketch (CRS-DWG-102), drawn upside down so the top view shows the bottom face.*

![Figure 5. Bottom face drilling layout](05-build-plan/base-holes.png)

*Figure 5. Drilling layout, with the box standing upside down on its roof and its back face toward you.*

**What it is and what it is made from.** A bought grey polycarbonate box, 150 deep, 260 wide and 300 tall, rated IP65, with its lid on the face away from the pole, an internal mounting plate on four bosses inside the back wall, a four-lug mounting kit and a membrane vent. Five holes are drilled in its bottom face and one in its roof.

**How to make it.**

1. Decide the box's kerb side: with the box upright and its back face (the face that goes on the mounting plate) toward you, the kerb side is on your right. Mark it. Stand the box upside down on its roof on a soft cloth, back face toward you; the kerb side is now on your left. Cover the bottom face with masking tape.
2. Mark the holes from Figure 5, measuring from the back face and sideways from the centre line: four 20 holes for the M20 glands, 40 and 100 from the back face and 105 each side of the centre line; one 12 hole for the vent, 130 from the back face on the centre line.
3. Put a block of wood inside under the face. Pilot drill every hole 3 at low speed; do not centre punch hard, since polycarbonate cracks.
4. Open each hole with a step drill, light pressure, low speed. Before the last step, check the size against the gland's and the vent's datasheets.
5. Turn the box over. In the roof, drill a 16 hole for the antenna bulkhead, 75 from the back face and 90 toward the kerb side of the centre line.
6. Deburr inside and out, peel the tape, and clean with water and mild soap only; solvents craze polycarbonate.
7. Fit the four lugs to the box's back corners as the lug kit's maker describes.

**How it fits the parts next to it.**

![Figure 6. Joint 3: the bottom face from below](05-build-plan/joint-03.png)

*Figure 6. Glands in two rows each side of the battery's place; the vent at the lid end.*

Each gland and the vent go in from outside with the sealing washer outside and the nut inside. The glands sit beside the battery, not under it: every inside nut is at least 5 clear of the battery. The panel lead uses the kerb-side gland nearer the back face, the light bar lead the kerb-side gland nearer the lid, the button lead and the radar lead the two road-side glands.

**Check before moving on.** Each part seats flat on its washer; no crack runs out from any hole under a bright lamp.

### 3.3 Battery strap and internal plate

![Figure 7. Making sketch of the battery strap](../cad/drawings/CRS-DWG-103.png)

*Figure 7. Battery strap making sketch (CRS-DWG-103).*

**What it is and what it is made from.** A Z-shaped strip that holds the battery down on the enclosure floor and against the internal plate; and the box's own internal plate, which carries the charger, the controller and the fuse block and lifts out with them. The strap is aluminium strip 25 x 2, 5052 or 6061 class. The internal plate (220 x 270 x 2) comes with the box.

**How to make it.**

1. Strap: cut 180 of strip and round its corners. Bend it to a Z with an inside radius of about 2: a 40 leg that stands on the internal plate, a 97 top that lies on the battery and a 40 leg that comes down the battery's front.
2. Drill two 4 holes on the centre of the plate leg, 15 and 30 above the underside of the top.
3. Internal plate: tap two M4 holes on its centre line, 113 and 128 above the enclosure's inside floor (measure from where the plate sits on its bosses), for the strap.
4. Lay out the charger, the controller board and the fuse block on the plate's front as Figure 9 shows: charger on the road side at 110 to 170 above the floor, fuse block on the kerb side at the same height, controller board across the middle from 180 to 280 above the floor. Keep the area below 110 clear for the battery.
5. Mark each module's holes through the module, drill 3.2, and fit the modules on M3 screws with 6 nylon stand-offs.
6. Wire the modules as Figure 8 shows.

![Figure 8. Block-level wiring](05-build-plan/wiring.png)

*Figure 8. Block-level wiring with wire sizes. No circuit board is laid out at this stage; the controller is the FieldNode radio core on its maker's breakout with bought LED driver modules.*

Wire it with stranded copper and a ferrule on every screw terminal: 1.5 mm² (16 AWG) for the panel to the charger, the charger to the fuse block and the battery to the fuse block; 0.75 mm² for the fuse block to the controller and for the six cores to the light bar; 0.5 mm² for the four-core leads to the button and to the radar and PIR; 0.25 mm² for the charger's status lines. The 5 A battery fuse goes in the fuse block, as near the battery as the leads allow, and stays out until section 6 allows it. Leave each outside lead coiled and labelled at its gland until step 16.

**How it fits the parts next to it.**

![Figure 9. Joint 4: battery, strap and internal plate](05-build-plan/joint-04.png)

*Figure 9. The battery stands on the floor against the internal plate; the strap holds it down and in.*

The internal plate sits on the four moulded bosses inside the back wall, 10 off the wall, held by four M4 screws. The battery (151 wide, 95 deep, 98 tall) stands on the floor with its back against the internal plate, between the two rows of glands. The strap's top lies on the battery and its front leg stops the battery sliding toward the lid; its two M4 screws go into the internal plate.

**Check before moving on.** With the strap screwed down on a dummy block the size of the battery, the block cannot move; every wire is labelled and continues end to end.

### 3.4 Enclosure mounting plate

![Figure 10. Making sketch of the enclosure mounting plate](../cad/drawings/CRS-DWG-104.png)

*Figure 10. Mounting plate making sketch (CRS-DWG-104).*

![Figure 10a. Hole positions on the mounting plate](05-build-plan/plate-holes.png)

*Figure 10a. Every hole, full size figures, measured up from the bottom edge of the lower tab and sideways from the centre line.*

**What it is and what it is made from.** The flat plate the enclosure and the sun shield hang on; its two tabs bolt to two saddles on the back of the pole. Aluminium sheet 4 mm, 5052 class: 350 wide and 300 tall, with a 90 x 90 tab centred above and below, 480 tall overall.

**How to make it.**

1. Cut the outline and round the outside corners to about 5. File the inside corners of the tabs to a small radius so they cannot start a crack.
2. Scribe a centre line down the length. Mark every hole from Figure 10a: heights up from the bottom edge of the lower tab, sideways from the centre line.
3. Saddle bolts: four 9 holes on the centre line, 10 and 50 up (lower tab) and 430 and 470 up (upper tab).
4. Lug screws: four 5.5 holes, 142 each side, 100 and 380 up.
5. Shield screws: four holes 164.5 each side, 140 and 340 up; drill 4.2 and tap M5.
6. Deburr every hole on both faces.

**How it fits the parts next to it.**

![Figure 11. Joint 5: an enclosure lug on the mounting plate](05-build-plan/joint-05.png)

*Figure 11. The box's back sits flat on the plate; each lug lies flat on the plate beside the box and takes one M5 screw, nyloc nut behind.*

The enclosure's back face sits flat on the plate's front between 90 and 390 up. Each lug sits on the plate beside the box and is held by one M5 screw from the front with a nyloc nut behind the plate. The plate's back face sits flat on two saddles, one behind each tab, held by two M8 bolts into each from the front:

![Figure 12. Joint 9: a mounting plate tab on its saddle](05-build-plan/joint-09.png)

*Figure 12. Both bolts of the upper tab sit above the sun shield's roof; both bolts of the lower tab sit below the box.*

**Check before moving on.** Lay a saddle on each tab and look through the holes; lay the box with its lugs on the plate and check all four lug holes line up.

### 3.5 Panel rails (make 2: a left and a right)

![Figure 13. Making sketch of the panel rail](../cad/drawings/CRS-DWG-105.png)

*Figure 13. Panel rail making sketch (CRS-DWG-105).*

**What it is and what it is made from.** Two angles bolted across the back of the panel frame that hang the panel on the bracket's cheeks. Aluminium equal angle 40 x 40 x 4, 6063 class.

**How to make it.**

1. Cut two 360 lengths; square and deburr the ends.
2. Flat leg (the one that goes on the panel frame): two 6.5 holes, 10 from each end, 20 out from the outer face of the upright leg.
3. Upright leg: two 10.5 holes, 22 out from the outer face of the flat leg: the pivot hole at mid-length (180 from each end) and the tilt bolt hole 60 from it, toward the end that will be at the panel's low edge.
4. The two rails are mirror images: clamp the upright legs back to back and drill them together so the holes line up.

**How it fits the parts next to it.**

![Figure 14. Joint 11: a rail on its cheek, seen from inside the bracket](05-build-plan/joint-11.png)

*Figure 14. The pivot bolt and the tilt bolt pass through the rail and the cheek; the nuts are inside the bracket.*

The flat legs lie across the frame's back lip at the panel's two long edges, 61 to 101 each side of the panel's centre line, with two M6 bolts each (nuts inside the frame). The upright legs stand down from the panel, against the outside faces of the bracket's two cheeks: an M10 pivot bolt at the top of each cheek, and an M10 bolt in each cheek's tilt slot.

**Check before moving on.** Hole centres 60 and 340 apart, within 0.5. The panel you buy must have a flat back lip at least 15 wide on its long edges.

### 3.6 Keyed pole saddles (make 8, all the same)

![Figure 15. Making sketch of the keyed pole saddle](../cad/drawings/CRS-DWG-106.png)

*Figure 15. Keyed pole saddle making sketch (CRS-DWG-106).*

**What it is and what it is made from.** The block every part on the pole is fixed to: a V in its back sits on the pole, the band runs across its front, and the part bolts to its front over the band. Aluminium flat bar 80 x 40, 6082 class.

**How to make it.**

1. Saw eight slices 60 thick off the bar and file each to 80 wide, 40 deep and 60 tall. The 80 x 60 face without the V is the front.
2. On each 80 x 40 face, scribe the V: 120° included, centred, 70 wide at the back face, with its point 20.2 in from the back face. Saw just inside both lines and file to them.
3. Key the V faces: hacksaw cuts 1 deep and 3 apart, running the full 60 height on both faces. The ridges bite into the pole's coating and resist the sign turning.
4. Across the front, file or mill a groove 21 wide and 1 deep, centred on the 60 height, for the band.
5. On the front's centre line, 20 above and 20 below the middle, drill 6.8 to 18 deep and tap M8 to 14 deep.
6. Break every sharp edge.

**How it fits the parts next to it.**

![Figure 16. Joint 6: saddle, pole and band seen from above](05-build-plan/joint-06.png)

*Figure 16. Cut through the band. The pole touches both faces of the V; the band runs round the pole and across the saddle's front in its groove.*

The pole touches both V faces, 6.4 in from the back corners on a 114.3 pole and 20 in on a 60 pole; the saddle's front is then 28.6 in front of a 114.3 pole's surface. The band (19 x 0.76 stainless, with a buckle) goes round the back of the pole, runs straight to the saddle's front corners and lies in the groove; tightening it pulls the V onto the pole. The buckle sits behind the pole, turned off the centre line. Whatever bolts to the saddle covers the band:

![Figure 17. Joint 2: the light bar on its saddle](05-build-plan/joint-02.png)

*Figure 17. The light bar's back wall sits flat on the saddle; two M8 bolts go in from inside the bar.*

![Figure 18. Joint 7: the sign on its lower saddle](05-build-plan/joint-07.png)

*Figure 18. The sign lies flat on the saddle's front; two M8 security bolts go through it into the saddle.*

On a new post (not this prototype), the upper sign saddle's upper hole is drilled right through at 10.5 and one M10 bolt passes through the sign, the saddle and both walls of the post, which stops the sign turning:

![Figure 19. Joint 13: the anti-rotation bolt on a new post](05-build-plan/joint-13.png)

*Figure 19. New posts only: the M10 bolt in place of one sign bolt, nyloc nut behind the post.*

**Check before moving on.** On a 114 tube each saddle must not rock; a 60 tube must also touch both V faces; both tapped holes take an M8 bolt by hand.

### 3.7 Radar arm

![Figure 20. Making sketch of the radar arm](../cad/drawings/CRS-DWG-107.png)

*Figure 20. Radar arm making sketch (CRS-DWG-107).*

**What it is and what it is made from.** An L-shaped arm that holds the radar and the PIR sensor out over the kerb side, 240 from the pole. Aluminium flat bar 40 x 5, 6082 class.

**How to make it.**

1. Cut 320 of bar. Bend it 90° across the 5 thickness in a vice over a radius block, to an L with outside legs of 251 and 70.
2. Short leg: two 9 holes on its centre line, 20 and 60 up from the underside of the long leg.
3. Long leg, measured from its far end: a 12 hole on the centre line 40 in, for the PIR's neck; two 4.5 holes on the centre line 15 and 65 in, for the radar housing's screws.
4. Deburr.

**How it fits the parts next to it.**

![Figure 21. Joint 8: the radar arm on its saddle, with the radar and the PIR](05-build-plan/joint-08.png)

*Figure 21. The short leg stands up flat on the saddle; the radar sits on the far end of the long leg and the PIR hangs under it.*

The short leg sits flat on its saddle with two M8 bolts. The long leg points at the kerb, level, 2,555 above the sidewalk at its underside. The radar housing sits on top of its far end with two M4 screws; the PIR's threaded neck passes up through the 12 hole and its nut goes on top. The PIR's underside is 2,515 above the sidewalk.

**Check before moving on.** The legs are square; with the arm on a saddle on a vertical tube, the long leg is level within 1°.

### 3.8 Panel bracket

![Figure 22. Making sketch of the panel bracket](../cad/drawings/CRS-DWG-108.png)

*Figure 22. Panel bracket making sketch (CRS-DWG-108).*

**What it is and what it is made from.** The welded steel bracket on the post top that carries the panel at 30°. Steel tube 139.7 x 4 and plate 6, S235, galvanized or painted after welding.

**How to make it.**

1. Socket: cut 120 of 139.7 x 4 tube. Drill three 10.5 holes 60 below its top, 120° apart, one toward the kerb side. Weld an M10 nut over each hole on the outside.
2. Cap: cut 140 x 140 from 6 plate and weld it on top of the socket all round.
3. Cheeks: cut two from 6 plate to the outline of the right view in Figure 22, 96 wide, with the top edge sloping at 30°. In each, drill the 10.5 pivot hole, and chain drill and file the tilt slot: 10.5 wide, on a 60 radius round the pivot, 20° long.
4. Stand the cheeks on the cap with their inside faces 110 apart, parallel to each other and square to the cap, and weld both sides of each.
5. Clean the welds; send for hot-dip galvanizing, or prime and paint.

**How it fits the parts next to it.**

![Figure 23. Joint 10: the socket on the post top](05-build-plan/joint-10.png)

*Figure 23. The cap rests on the pole's top edge; three set screws close the 8.7 gap round the pole and lock the socket.*

The socket slides over the pole top until the cap sits on it; three M10 security set screws through the welded nuts centre it and lock it. The panel rails bolt to the outside of the cheeks (Figure 14).

**Check before moving on.** The cheeks are parallel within 1 and square to the cap; the socket slides over a 114.3 tube.

### 3.9 Sun shield

![Figure 24. Making sketch of the sun shield](../cad/drawings/CRS-DWG-109.png)

*Figure 24. Sun shield making sketch (CRS-DWG-109).*

**What it is and what it is made from.** A white folded sheet that shades the enclosure on its back, sides and roof with a 25 air gap, open at the bottom and, above the mounting plate, toward the pole. White powder-coated aluminium sheet 2 mm.

**How to make it.**

1. Mark one blank on the protective film: the back, 314 x 327, in the middle; a side 177 deep on each long edge; a roof 177 deep on the top edge with a 10 tab on each end; and a 15 flange along the free edge of each side, 300 long from the bottom.
2. Cut with aviation snips. Drill a 3 relief hole wherever two fold lines cross, so the coating does not tear.
3. Fold the sides and the roof 90° forward, then the roof tabs down over the sides, and rivet each tab with two 3.2 rivets. Fold each flange 90° outward.
4. Flanges: two 5.5 holes each, 7.5 from the fold, 50 and 250 up from the bottom edge.
5. Roof: a 22 hole, 75 back from its front edge and 90 toward the kerb side, for the antenna.
6. Peel the film.

**How it fits the parts next to it.**

![Figure 25. Joint 12: a shield flange on the mounting plate](05-build-plan/joint-12.png)

*Figure 25. The flange lies flat on the mounting plate beside the box and takes an M5 security screw.*

The flanges lie flat on the mounting plate either side of the box and take four M5 security screws into the plate's tapped holes. The shield stands 25 off the enclosure's back, sides and roof; the antenna passes through the roof hole with 3 to spare all round. To open the enclosure lid, undo the four screws and lift the shield away.

**Check before moving on.** On a trial fit over the box, the gap is 25, give or take 3, all round.

### 3.10 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Crossing warning sign (line 1).** 750 diamond, 3 aluminium, retroreflective sheeting to the local sign design, without the maker's brackets. Drill four 9 holes on its vertical centre line, 260, 300, 760 and 800 up from its bottom point.
- **LED heads (line 3).** Four amber modules, lens 140 x 62 (at least 127 x 51 lit), about 6 W at 12 V, dimmable, each with a flange that covers a 128 x 50 window and a body no deeper than 25 behind it, bought with a snap-on bezel frame and a moulded hood visor 26 deep with a drip lip.
- **Push-button station and instruction plate (line 4).** Vandal-resistant piezo button with tone, tactile arrow and LED, in a housing about 70 x 60 x 160 that fixes to a flat face with two bolts; an instruction plate 230 x 300 x 4. Drill two 9 holes in the plate on its centre line, 130 and 170 up from its bottom edge.
- **Radar (line 5) and PIR sensor (line 16).** 24 GHz presence radar in a housing about 80 x 80 x 80 with two screws 50 apart in its base; low-power PIR with a threaded neck of 12 or less.
- **Solar panel (line 6).** 20 W monocrystalline, about 500 x 360 x 25, aluminium frame with a flat back lip at least 15 wide on the long edges.
- **Enclosure (line 8).** As section 3.2.
- **Battery (line 9).** LiFePO4 12.8 V 12 Ah with its own battery management system and low-temperature charge protection, no larger than 151 x 95 x 98.
- **Charger (line 10).** 12 V MPPT charger, 5 A class, LiFePO4 profile, low-temperature charge cut-off, own use 4 mA or less, no larger than 40 x 90 x 60.
- **Controller and radio board (line 11).** FieldNode radio core (STM32WL-class LoRa module) on its maker's breakout, with four LED driver channels with night dimming, a clock, a fault LED and a 12 V to 3.3 V converter, on a board no larger than 180 x 100.
- **Antenna (line 12).** Short whip for the LoRa band of the pilot region, with a 16 bulkhead.
- **Bands (line 13).** Eight 19 x 0.76 stainless bands, about 0.6 long each, with buckles, and a banding tool.
- **Pilot light (line 17).** Small amber panel-mount light, about 0.3 W, with a lens about 30 across and a threaded body for a 22 hole.
- **Wiring and fixings (line 15).** Outdoor cable; a fuse block with a 5 A battery fuse and a 2 A controller fuse; four M20 and one M16 nylon glands with blanking plugs; stainless security fixings: 20 M8 x 16 bolts, 4 M5 x 12 screws with nyloc nuts, 4 M5 x 10 screws, 4 M6 x 12 bolts with nuts, 4 M10 x 30 bolts with nyloc nuts, 3 M10 set screws; M4 and M3 screws, rivet nuts and 3.2 rivets, nylon stand-offs, ferrules, cable ties and a cable cover for the pole.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Steps 1 to 7 are bench work. For steps 8 to 18 the test post lies on two trestles at bench height, turned as each step needs; the pictures show it upright.

### Step 1: LED heads and pilot light into the light bar

![Step 1](05-build-plan/step-01.png)

End caps riveted on first. Each head, with its bezel and visor already on it, from outside through its window, four M4 screws. The pilot light through the kerb-end cap, its nut inside. Lead every wire to the cable gland's position.

### Step 2: close the light bar

![Step 2](05-build-plan/step-02.png)

Fit the M16 gland in the cover and lead the head and pilot wires out through it. Foam gasket on the lips; cover on with its M4 screws. It comes off again in step 9.

### Step 3: glands, vent and antenna into the enclosure

![Step 3](05-build-plan/step-03.png)

Each from outside with its seal outside and its nut inside, to the maker's torque. Blanking plugs in the glands until their cables arrive.

### Step 4: build the internal plate

![Step 4](05-build-plan/step-04.png)

Charger, controller board and fuse block on M3 screws and stand-offs; the strap on its two M4 screws; wire them as Figure 8. **Hold point:** no battery, and the fuses out.

### Step 5: internal plate into the enclosure

![Step 5](05-build-plan/step-05.png)

In through the open lid face, onto the four bosses, four M4 screws. Connect the antenna lead to the board.

### Step 6: enclosure onto the mounting plate

![Step 6](05-build-plan/step-06.png)

Lugs on the box's back corners; the box back flat on the plate's front, centred; four M5 screws from the front, nyloc nuts behind, snug.

### Step 7: rails onto the panel

![Step 7](05-build-plan/step-07.png)

Lay the panel face down on a soft cloth. Place each rail across the back lip at the long edges, its upright leg 61 from the panel's centre line and pointing away from the panel, drill the lip through the rail's holes, keeping clear of the glass and cells, and fit two M6 bolts with the nuts inside the frame.

### Step 8: saddles and bands onto the post

*Table 2. Saddle heights (the saddle's middle, above the sidewalk; on the test post, above its bottom end) and the way each faces.*

| Saddle | Height | Faces |
| --- | --- | --- |
| Push-button station | 1,050 | Kerb side |
| Instruction plate | 1,300 | Kerb side |
| Light bar | 2,165 | Traffic side |
| Sign, lower | 2,530 | Traffic side |
| Radar arm | 2,595 | Kerb side |
| Enclosure, lower | 2,790 | Back |
| Sign, upper | 3,030 | Traffic side |
| Enclosure, upper | 3,210 | Back |

![Step 8](05-build-plan/step-08.png)

Mark each height on the post with tape. Each saddle on its mark, facing as Table 2 says; pass its band round the post, across the saddle's front in the groove, and into the buckle behind the post, turned off the centre line. Pull each band snug with the banding tool so the saddle can still be turned by hand; final tension comes in step 10 (sign) and as each part goes on.

### Step 9: light bar onto its saddle

![Step 9](05-build-plan/step-09.png)

Cover off; the back wall flat on the saddle, centred; two M8 bolts from inside; cover back on. The bar is level and square to the road. Tension the band.

### Step 10: sign onto its two saddles

![Step 10](05-build-plan/step-10.png)

Two M8 security bolts through the sign into each saddle. Check the sign is upright and square to the road, its bottom point 20 above the light bar, then tension both bands.

### Step 11: push-button station and instruction plate

![Step 11](05-build-plan/step-11.png)

The station on its saddle with its own two bolts, its button centre 1,050 above the walking surface; the plate on the saddle above with two M8 security bolts. Tension both bands.

### Step 12: radar arm, radar and PIR

![Step 12](05-build-plan/step-12.png)

On the bench, screw the radar onto the arm and fit the PIR under it. Then the short leg flat on its saddle, two M8 bolts, the long leg level and pointing at the kerb. Tension the band.

### Step 13: enclosure unit onto its saddles

![Step 13](05-build-plan/step-13.png)

Two people. Hold the plate's tabs flat on the two back saddles and fit two M8 bolts into each. Lid still off, battery not fitted. Tension both bands.

### Step 14: panel bracket onto the post top

![Step 14](05-build-plan/step-14.png)

Slide the socket down until the cap sits on the pole. Turn it so the cheeks run square to the road, then tighten the three set screws evenly.

### Step 15: panel onto the bracket

![Step 15](05-build-plan/step-15.png)

With a helper holding the panel, rails outside the cheeks: pivot bolts first, then the tilt bolts in their slots. Set 30° with an angle finder, the panel facing the equator, and tighten all four bolts.

### Step 16: cables into the enclosure

![Step 16](05-build-plan/step-16.png)

Run each cable up the pole to the enclosure: the light bar, button and radar leads up from below, the panel lead down from the top. Fit the cable cover over them on the pole. Each cable in through its gland (section 3.2), the gland cap tightened on it; connect as Figure 8.

### Step 17: battery in, lid on

![Step 17](05-build-plan/step-17.png)

**Hold point:** only after safety stops S1 to S4. Undo the strap's two screws, stand the battery on the floor against the internal plate, refit the strap, connect the battery leads to the fuse block, put the fuses in. Fresh desiccant pack; check the lid gasket is clean with no wire across it; lid on, its screws tightened evenly in a cross pattern.

### Step 18: sun shield

![Step 18](05-build-plan/step-18.png)

Lower the shield over the enclosure from above, the antenna through its roof hole, flanges flat on the plate; four M5 security screws. **Hold point:** safety stop S7.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of CRS-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Heights | R10, R11, R14 | Tape from the post's bottom end (the sidewalk line) | Button centre 1,050; bar bottom 2,100; enclosure bottom 2,850; PIR underside 2,515, each within 10 |
| Saddles on the pole range | R10 | Seat one saddle and band on 60, 89 and 114.3 tubes | Both V faces touch each tube; the band closes with adjustment to spare |
| Band tension and grip | R9 | Banding tool's tension gauge; torque on the sign saddles with a lever arm | The tension and the slipping torque are recorded (the calculation assumes 1,000 N and a grip friction of 0.4) |
| Enclosure seal | R8 | Each washer under a lamp; gland caps tight on their cables | Every washer evenly squeezed; no gaps (the spray test comes later) |
| Charger settings | R6, R7, R8 | Bench supply at 18 V, 2 A limit, in place of the panel; battery out; read the charger's settings and output | LiFePO4 profile; charge voltage as the battery maker states (about 14.4 V); low-temperature cut-off set |
| First charge | R7 | Battery in, bench supply at 18 V, 2 A limit | Current flows; charging ends at the set voltage; battery stays under 45 °C |
| Flash pattern and time | R1, R4 | Press the button; film the heads; stopwatch | Wig-wag at 75 sequences per minute; flashing stops after the set time (12.8 s for 7 m); a second press extends it |
| Pilot light and button | R11 | Press with a force gauge; listen | Pilot light on while flashing; tone and tactile pulse; 22 N or less |
| Radar wake | R5 | Walk into the waiting zone; stand still 1 s | The PIR wakes the radar; the radar's presence output starts the flash |
| Fault indication | R12 | Unplug one head; unplug the antenna | The fault LED shows and the fault is logged; the bar never flashes continuously |
| Panel tilt | R7 | Angle finder; push the panel corners by hand | 30° give or take 1°; nothing moves at any joint |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the battery comes into the workshop.** Its voltage is 12.8 to 13.4 V; no swelling, dents or leaks; a datasheet from its maker. A charging spot ready on a non-combustible surface (ceramic tile or steel tray) with a fire extinguisher for electrical fires within reach.
- **S2. Before any fuse goes in.** With the battery out, the fuse block's battery terminals and every supply read open to ground. The battery leads' polarity matches the fuse block and the charger, checked with a meter, not by wire colour.
- **S3. Before any charging source is connected.** The charger is set to its LiFePO4 profile and its low-temperature cut-off; the panel input polarity is checked at the charger; the charger's maximum input is above the panel's open-circuit voltage at -20 °C.
- **S4. Before the battery is allowed to charge.** The charger settings check of section 5 passes on the bench supply. The supply's current limit is 2 A or less.
- **S5. First charge.** Attended the whole time, lid open, enclosure on the charging spot or the post on its trestles beside it; battery temperature checked every 15 minutes. Stop if the battery passes 45 °C or swells. Never bypass the charge protection to gain energy.
- **S6. Before the radio transmits.** The antenna is connected and matches the pilot region's band. Transmitting without an antenna can damage the radio.
- **S7. Before the post is stood up (outside this plan unless all of this is true).** Every band tensioned and every bolt tight; panel glass whole; sharp edges deburred. The post goes into a base or stand rated for at least 70 kg and a 3.7 m mast, with a lifting plan, two people and the area cleared. Nobody stands under the post while it is raised.
- **S8. Before any installation beside a road (outside this plan).** Road authority approval, the asset owner's permission for an existing pole, trained crews, traffic management and fall protection as local rules require, clear of overhead power lines; a qualified engineer has checked the post, saddles, bands, footing or host pole for about 2.6 kN·m at the sidewalk.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade (or a bandsaw); bench vice with soft jaws and a radius block; bench drill or a drill in a stand; drills 3 to 12 and a 22 hole saw or step drill; step drill to 22; M4, M5 and M8 taps with their tap drills; jigsaw with a fine metal blade; flat, half-round and square files; deburring tool; scriber, engineer's square, protractor, steel rule and calipers; digital angle finder; hand sheet folder (or hardwood bars clamped in a vice) for 2 sheet up to 720 long; aviation snips; hand rivet tool and rivet nut tool; banding tool with tension gauge; socket and spanner set to 17; torque wrench; soldering iron; ferrule crimper and wire strippers; multimeter; bench power supply with an adjustable current limit (0 to 30 V, 0 to 3 A); two trestles and a tape measure. The panel bracket needs a welder (MIG or stick) or a fabricator who will weld it.

**Skills.** Basic metalwork (marking out, sawing, drilling, filing, tapping, folding sheet), through-hole soldering and crimping, safe use of a bench power supply and care with lithium cells. The bracket welds should be made by a competent welder. All circuits are extra-low voltage: 12.8 V at the battery and under about 22 V from the panel. The bench supply must be a certified, undamaged unit; no mains wiring is part of this build.

**Workspace.** A bench about 1.5 x 0.7 m, and floor space about 4.5 x 1.5 m for the post on its trestles; a metalwork corner kept apart from the electronics so chips stay off the modules; the charging spot of S1.

**Personal protective equipment.** Safety glasses for cutting, drilling and soldering; cut-resistant gloves for sheet, the sign and the panel; hearing protection when sawing; safety boots when handling the post; no gloves near a turning drill; welding mask, gloves and jacket for the bracket.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/CRS-DWG-101` to `CRS-DWG-109`.
- General arrangement: `cad/drawings/CRS-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (CRS-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; heights [F1], pole range [F2], wind and clamps [G1] to [G8], cost [H1] to [H3].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (CRS-DDR-003), with CRS-DDR-001 and CRS-DDR-002; decisions made in `docs/06-design-decisions.md` (CRS-DEC-001).
- Requirements: `docs/03-requirements.md` (CRS-REQ-001 v0.6).
