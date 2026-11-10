# Afterbyte Mono — Design brief

## Intent

Create an original pixel monospace family with a crisp terminal aesthetic and enough personality for display use. The first milestone is a coherent, readable Regular master.

## Construction study

Start with an 8-column by 12-row cell study. This is a proposed exploration grid, not a finalized font metric. Investigate a one-cell horizontal margin, a 7-row capital height, a 5-row x-height, and a 2-row descender. Confirm the design with actual drawings before locking the grid.

Every spacing glyph must share one advance width. Space must use the same advance as letters. Font units, ascender, descender, line gap, baseline, and pixel-to-unit scale must be recorded alongside the source once adopted.

## Recognizable details

- Explore a slashed zero and open counters.
- Give lowercase l a foot and uppercase I clear horizontal terminals.
- Keep the lowercase i dot distinct at intended rendering sizes.
- Align brackets and braces around the same visual center.
- Keep period, comma, colon, and semicolon distinct.
- Review diagonal joins at native grid sizes and enlarged display sizes.

These are proposals to validate, not claims about completed glyphs.

## Coverage sequence

1. Establish H, O, n, o, 0, 1, I, and l as control characters.
2. Complete uppercase, lowercase, and numerals.
3. Complete all printable ASCII punctuation.
4. Add space and a visible .notdef glyph.
5. Evaluate extended Latin and currency symbols after the core passes review.

## Originality and source policy

Draw original glyphs. Do not trace, rename, or bundle Departure Mono or other third-party font assets. External contributions must identify their author, provenance, and applicable license. Select a dedicated font license before accepting font outlines.

## Proofing

Use specimen/sample.txt at intended native pixel sizes, a larger display size, and on both light and dark backgrounds. Check 0/O, 1/I/l, rn/m, cl/d, quotes, operators, and braces. Record browser/editor version, OS, size, scale, and screenshots.

## Definition of ready

The core design is ready for a first build when coverage is complete, spacing is coherent, control pairs are distinct, sources are editable, and design decisions are documented. Popularity is an aspiration, not an acceptance criterion.
