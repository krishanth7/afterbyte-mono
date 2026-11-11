# Afterbyte Mono 4.0 / 5.0 — Design and engineering

The original continuous-vector core keeps the flat-top A, dotted zero, single-storey a/g, rounded bowls and 650-unit rhythm. V4 expands the core with selected OFL Noto glyphs, three original technical operators and algorithmic Braille. V5 adds extended script coverage and mathematical Unicode styles.

| Property | Value |
| --- | --- |
| UPEM / fixed advance | 1000 / 650 |
| Cap / x-height of original core | 700 / 500 |
| Core structural stroke | 64 |
| Typographic ascender / descender | 1280 / −450 |
| v4 glyphs / mapped characters | 1705 / 1704 |
| v5 glyphs / mapped characters | 2500 / 2499 |
| Formats / style | CFF OTF, TTF, WOFF, WOFF2 / Regular |
| License | SIL Open Font License 1.1 |

## Source treatments

- Original core: compiled from centerline recipes without changing prior glyph outlines.
- Noto expansion: pinned Noto Sans Mono 2.014, weight 300, width 100. Outlines are decomposed, scaled vertically by 700/714 and horizontally up to 650/600, centered in the 650-unit cell and narrowed where needed to keep ink inside 16–634. This is a modified, attributed OFL source.
- Technical operators ∏ ∑ ∫: original centerline recipes expanded at 64 units.
- Braille: Unicode bit positions determine eight possible dots; each dot is an original 24-point polygon. U+2800 is intentionally blank.
- Mathematical alphabets: explicit Unicode mappings; bold adds 13 units around core silhouettes, italic shears by 0.18 before fitting, double-struck figures outline the stroke boundary. Sans digits use the family’s sans forms. These are not additional family weights.

## Compiler pipeline

1. Build the original core into `build/core`.
2. Load and hash-check the vendored static Noto source.
3. Read the explicit v4 or v5 coverage contract and choose each glyph’s documented origin.
4. Decompose and normalize contours, fit fixed advances, and construct source-derived glyphs.
5. Compile versioned metadata, complete copyright/OFL notices, cmap, metrics and fixed-pitch flags.
6. Compile CFF OTF, TTF, WOFF and WOFF2 with fixed timestamps; write coverage, summaries and checksums.
7. Validate both versions and render actual-font specimens.

The mapped repertoire intentionally excludes combining marks, private-use padding, format controls and unassigned code points. Unsupported scripts need fallback fonts. Layout features such as mark positioning and contextual substitutions are not implemented in this release.
