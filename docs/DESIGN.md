# Afterbyte Mono — Design specification

## 1. Concept Overview

A light, readable pixel monospace with a restrained futuristic character. The design uses measured spacing, open counters, and clear lowercase forms for code and technical interfaces. HUD character comes from precise symbols, a slashed zero, and a controlled specimen identity rather than heavy slabs or aggressive condensation.

The previous Gothic direction is superseded as the repository's primary typeface. Its sources remain as a historical experiment.

Departure Mono is a category reference for pixel monospace typography. Afterbyte's matrices are drawn independently; no third-party font is loaded or traced.

## 2. Specification Matrix

| Parameter | Value |
| --- | --- |
| Family / style / alpha | Afterbyte Mono / Regular / 0.2.0 |
| Units per em | 1600 |
| Pixel cell | 100 × 100 units |
| Character advance | 900 units, including .notdef and spaces |
| Standard matrix | 7 ink columns, inset 100 units in a 9-column cell |
| Native em size | 16 CSS px |
| Cap height / x-height | 1000 / 700 units |
| Ascender / descender | 1300 / −300 units |
| Line gap | 0 |
| Stroke | One pixel, with intentional intersections |
| Outline directions | Horizontal and vertical edges only |
| Unicode mappings / glyphs | 196 / 197 |
| License | MIT |

All coordinates remain on the 100-unit pixel grid. TrueType outlines describe the union of filled squares, not a bitmap strike. Native sizes of 16/32/48/64 px align each design pixel to whole raster pixels under the tested FreeType setup. Other sizes and transforms may antialias.

## 3. Glyph Morphology Breakdown

| Group | Construction and purpose |
| --- | --- |
| Uppercase | Open, light geometric forms with stepped corners; A has a clear apex and continuous crossbar; C and G retain open apertures. |
| Lowercase | Compact 7-pixel body; recognizable a/e bowls; full-height b/d/h/k/l; descending g/p/q/y; dotted i/j. |
| Ambiguity pairs | Slashed zero vs open O; flagged 1 vs barred I vs asymmetric l; separate dot on i. |
| Diagonals | One-pixel staircases; shallow glyph segments do not turn into thick diagonal slabs. |
| Figures | Fixed-width lining numerals with a slashed zero and full punctuation support for code/data layouts. |
| Accents | Original grave, acute, circumflex, tilde, and dieresis matrices plus cedillas; selected letters only. |
| Interface symbols | Original arrows, check mark, solid/outline squares, directional triangles, and currency signs. |
| Box drawing | 9-column cells spanning the advance; verticals span −300…1300; connected rows require line-height 1. |
| Shading | Native-grid monochrome pixel patterns, not transparency. |

The font contains no spacing-dependent substitutions or kerning. Uniform advances remain intact under shaping.

## 4. Implementation Blueprint

1. Draw original matrices in tools/draw_afterbyte.py, then generate sources/afterbyte-mono/pixels.json.
2. The JSON stores character, Unicode point, top coordinate, left inset, and rows of #/. cells. It is the editable font source.
3. Convert each # into a 100-unit square, Boolean-union neighboring squares, normalize winding, and remove redundant vertices.
4. Compile through FontTools FontBuilder with .notdef first, explicit Unicode mappings, 900-unit advances, fixed-pitch metadata, and MIT license metadata.
5. Generate TTF and WOFF2 with deterministic timestamps; copy the license and calculate SHA-256 hashes.
6. Run tools/validate_afterbyte.py for source occupancy, actual outlines, native raster, shaping, metrics, checksum, and link checks.
7. Generate README artwork from the compiled font with tools/render_afterbyte.py. The SVG lettering consists of actual glyph paths.
8. Review 0/O, 1/I/l, rn/m, punctuation, accents, boxes, and code layouts at both native and enlarged sizes before broader release.

Running draw_afterbyte.py overwrites direct JSON edits. To compile a modified JSON matrix, run build_afterbyte.py directly. Package-manager publishing and a tagged stable release are future work.
