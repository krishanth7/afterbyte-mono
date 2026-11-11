# Afterbyte Mono 0.3 — Design specification

## 1. Concept Overview

A continuous-vector technical monospace for corporate software interfaces and digital identities. The design replaces the earlier pixel-grid treatment with smooth bowls, a flat-top A, a dotted zero, and single-storey a/g.

This is a change in construction, proportions, and glyph morphology. It does not claim that a measured visual difference establishes legal clearance.

## 2. Specification Matrix

| Parameter | Current value |
| --- | --- |
| Version / style | 0.3.0 alpha / Regular |
| UPEM / advance | 1000 / 650 |
| Structural stroke | 64 units; selected symbol details 45 |
| Cap / x-height | 700 / 500 |
| Typographic ascender / descender | 820 / −220 |
| Line gap | 0 |
| Windows clipping ascent / descent | 822 / 220 |
| Unicode mappings / glyphs | 196 / 197 |
| Coordinates | Integer-unit final polygons |
| Construction | Original line/cubic centerlines and solid polygons |
| License | MIT for original project materials |

Small optical overshoots are allowed. The highest circumflex join reaches 822; Windows clipping metrics cover it. The typographic line box is 1040 units, hence connected box drawing uses line-height 1.04.

## 3. Glyph Morphology Breakdown

| Forms | Distinguishing construction |
| --- | --- |
| A | Flat upper bridge at y=668, diagonal legs, lower horizontal crossbar |
| O/o | Rounded rectangular bowls, not octagonal or stepped pixels |
| 0 | Narrower rounded bowl with a centered short rectangular dot |
| a/g | Single-storey bowls; g has an open descending hook |
| R | Curved upper chamber and descending diagonal leg |
| Q | Rounded bowl with a separate diagonal tail |
| I/1/l | Symmetric top/bottom bars, flagged numeral, and asymmetric curved terminal |
| e | Open continuous bowl with a horizontal internal rail |
| Figures | Equal advances with individually drawn curves and proportions |
| Punctuation | Continuous strokes; balanced bars, curves, and visible code punctuation |
| Accents | Separate vector marks composed with original base letters |
| Technical symbols | Independently drawn vectors, box connections, solids, and stripe shading |

There are no third-party glyph inputs. See PROVENANCE.md for the source record and scope.

## 4. Implementation Blueprint

1. tools/draw_afterbyte_vector.py defines original M/L/C/Z paths and solids and writes sources/afterbyte-mono/vectors.json.
2. The builder samples each cubic in 24 segments, expands centerlines with controlled stroke width, unions geometry, and snaps to integer units.
3. Final TrueType outlines are polygon approximations of the continuous curves. This is not a bitmap strike and does not use a native pixel grid.
4. FontTools writes cmap, glyf, metrics, fixed-pitch flags, names, license metadata, and standard OpenType tables.
5. TTF, CFF-based OTF, WOFF, and WOFF2 share the same outline geometry and deterministic timestamps. OTF uses reversed CFF contour winding; web containers use the TrueType build.
6. Validation compares source geometry with actual compiled contours, checks signature forms and metrics, and exercises HarfBuzz/FreeType.
7. README SVG specimens reuse actual compiled glyph paths. PNGs are review artifacts.
8. Broader OS/browser tests, independent validation, optical review, and coverage work remain before a stable release.

Direct JSON edits can be compiled without regenerating recipes. The old pixel matrices and generator remain historical files and are not build inputs.
