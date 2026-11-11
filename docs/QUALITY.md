# Afterbyte Mono 4.0 / 5.0 — Quality notes

## Automated verification

- Exact v4 contract: 1705 glyphs / 1704 Unicode mappings.
- Exact v5 contract: 2500 glyphs / 2499 Unicode mappings; all v4 mappings retained.
- Every mapped character is assigned Unicode; no private-use, unassigned or combining-mark padding.
- All original 196 core outlines and metrics retained.
- All 256 Braille patterns checked against their Unicode dot-bit count.
- Mathematical bold, italic and double-struck distinctions tested.
- Complete OFL and both copyright notices embedded; vendored source hash checked.
- Genuine CFF OTF, TTF, WOFF and WOFF2 signatures; equal counts, coverage, names and fixed 650-unit advances.
- All glyph bounds inside the declared font envelope; CFF geometry bounds compared with TrueType; webfont outlines compared point for point.
- Each mapped character shaped independently with HarfBuzz in all four formats.
- Nonblank characters rendered with FreeType at 12, 24 and 48 px in every decoded format; spaces and blank Braille are intentional blanks.
- Original core also passes source/topology checks and 12/16/24/32/48/96 px raster smoke checks.
- Checksums, documentation links, deterministic source and binary builds, and actual-font specimen review.

## Limits

These are technical smoke and contract tests, not certification of readability, full language coverage or behavior on every operating system and browser. Selected precomposed Latin, Greek and Cyrillic are supported; combining marks, complex shaping, emoji, CJK, ligatures, variable axes and bytecode hinting are not supplied. Native-speaker review and additional application proofing remain open work.

Long accents require the enlarged 1280/−450 line metrics. Do not reuse v3’s tight prose line settings without inspection. Braille is a visual character repertoire, not a translation or tactile-output service. Mathematical Unicode styles are explicit mappings rather than selectable family weights.
