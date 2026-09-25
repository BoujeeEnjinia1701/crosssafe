# CrossSafe

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $350 USD · **Difficulty:** 3 of 5

A solar crossing beacon that detects a waiting pedestrian and flashes high-visibility lights to warn drivers at unsignalized crossings near schools and markets.

## Concept rationale

An affordable, self-powered beacon can make crossings safer where signals will never be funded.

## Burning platform

Pedestrians account for a large share of road deaths worldwide, concentrated in low- and middle-income countries.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab.

## Problem

Pedestrians die at unsignalized crossings, and full traffic signals are costly and slow to approve.

## Concept

A solar crossing beacon that detects a waiting pedestrian and flashes high-visibility lights to warn drivers at unsignalized crossings near schools and markets.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Presence sensor and push button
- LED beacons
- Solar panel and battery
- Controller
- Pole mount

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> A research prototype; traffic control devices must meet local standards and road authority approval before use on a public road. Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended. Street furniture and pole mounts must be installed only with the asset owner's permission, by trained crews, with fall protection and traffic management as local rules require.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CRS-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CRS-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
