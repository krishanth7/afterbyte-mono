# Afterbyte Mono 0.3 — Quality notes

## Technical checks

- 196 Unicode mappings, complete printable ASCII, 197 glyphs including .notdef.
- Actual source-to-binary geometry agreement after integer normalization.
- Valid nonzero contours, winding, no self-intersections, and clipping/advance bounds.
- Equal 650-unit advances, mono metadata, cap/x-height, line metrics, and embedded MIT license text.
- Dotted zero/open O distinction, flat-top A, single-storey a/g, 64-unit H stems, and ambiguity pairs.
- TTF/WOFF2 outline, cmap, and metric equivalence.
- HarfBuzz shaping without missing glyphs or advance changes.
- Nonempty FreeType raster smoke checks at 12/16/24/32/48/96 px.
- Checksums, documentation/image links, SVG syntax, and deterministic source/binary rebuilds.
- Visual review of the actual-font hero and light/dark sheets.

## Limits

Local tests do not establish identical behavior on every OS, browser, zoom factor, or display. They do not prove readability or legal clearance. The current font is a one-style alpha without bytecode hinting, variable axes, or full language coverage.

## Release gates

Before a stable release: independent font validation; OS installation and multiple browser tests; optical spacing and mixed-case review; coverage requests; and a tagged package with source revision, binaries, license, checksums, and known limitations.

See PROVENANCE.md for design inputs and licensing context.
