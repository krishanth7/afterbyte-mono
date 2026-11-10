# Vantablack Gothic 0.1.0 alpha

This is the first installable font in the repository. The status changed from specification-only to an implemented alpha.

## Included

- 95 printable ASCII mappings and a visible .notdef glyph.
- One proportional Regular style at 1000 UPEM.
- Original polygon recipes, normalized editable JSON, TTF, WOFF2, CSS, and checksums.
- Actual-font path specimens in light and dark modes.
- Contract, geometry, binary, shaping, raster, and reproducibility checks.

## Decisions made during implementation

- The original MIT repository license is explicitly selected for the original Vantablack font sources and binaries as well. No additional font license or Reserved Font Name is introduced.
- The lowercase a/e waist uses y=300…410 instead of the proposed 360…470. With x-height 580 and a 110-unit top rail, a bar ending at 470 would erase the upper counter. The alpha keeps a small visible upper counter.
- Lowercase a is a high-waist two-chamber construction; e opens the lower-right channel. This replaces the earlier single-storey a proposal.
- W/w use a 112-unit shared center join, while their outer beams remain 110. The 2-unit join adjustment makes both modules meet on an exact integer/45-degree grid.
- Question mark's upper return joins at y=726, avoiding half-unit Boolean intersection artifacts.
- Diagonal bands approximate 110-unit perpendicular width through integer offsets; no smooth curves or non-45-degree edges are introduced.
- Quotes, braces, hash bars, percentage counters, and selected narrow punctuation use reduced detail strokes where a 110-unit component would close the form.
- Comma and semicolon advance 158 instead of the proposed 180 after their actual ink bounds are measured. system.json contains the shipped advances.
- Candidate kerning remains unshipped until measured visually. The current TTF/WOFF2 have proportional advances and no GPOS kerning feature.
- The centered zero identifier is a vertical solid bar, not an oblique slash or empty cut.
- The static font has no OpenType variation axis.

## Validation performed

- Source contours and compiled glyph points agree.
- 96 glyphs / 95 ASCII mappings, integer coordinates, axis/45-degree edges.
- Winding, valid polygon topology, no overlapping filled source components.
- 24-unit side bearings, exact 15-unit H crossbar gaps, line bounds, names, embedded MIT license.
- TTF/WOFF2 outline and horizontal-metric equivalence.
- HarfBuzz shaping without missing glyphs for the complete ASCII sequence.
- FreeType raster smoke checks for every printable non-space character at 32/48/64/80/120/240 px.
- Visual review of the hero and light/dark glyph sheets.
- Repeated source and binary generation for deterministic results.

These are local alpha checks. No external certification, full platform installation audit, browser accessibility audit, or production readiness is claimed.

## Known limitations

The font is unhinted and has no kerning, ligatures, expanded language support, extra weights, or variable axis. Tight apertures and micro-gaps can rasterize poorly at small sizes. Extended text needs a fallback font. Refining optical spacing, S/5 and narrow apertures, adding Unicode coverage, and cross-platform proofing are the next milestones.

## Source editing

The geometry recipes in tools/build_vantablack.py and system.json regenerate glyphs.json. To edit polygon contours directly, change glyphs.json and use `python tools/build_vantablack.py --from-source`; running the default build will overwrite that snapshot. A changed advance must be updated in both the glyph source and system.json. Run both validators after edits.
