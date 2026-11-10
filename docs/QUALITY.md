# Afterbyte Mono — Quality and release notes

## Implemented alpha checks

- 196 Unicode mappings, 197 glyphs, complete printable ASCII, and visible .notdef.
- Source cell occupancy equals the actual outline geometry, not merely a count of records.
- Nonzero, valid contours with correct winding and exclusively axis-aligned 100-unit grid coordinates.
- All advances equal 900; fixed-pitch flag and PANOSE mono proportion.
- Line metrics, cap/x-height, names, embedding flags, and embedded MIT license metadata.
- TTF/WOFF2 mappings, advances, and outline equivalence.
- HarfBuzz shaping with no missing glyphs and uniform advances.
- Binary black/white raster cells at 16, 32, 48, and 64 px in the local FreeType setup.
- Box-drawing horizontal and vertical boundaries connect at the cell edges.
- Checksums, documentation/image links, and reproducible original source/binary generation.
- Visual review of the actual-font hero and light/dark sheets.

## Limits

The font is an alpha, not independently certified. Native-grid checks use a local FreeType/HarfBuzz environment and do not establish identical results under browser scaling, fractional positioning, every display, or every OS. There are no bytecode hints, variable axes, ligatures, or extra styles.

Coverage is selected, not full Latin-1 or complete language support. Missing scripts and code points need a fallback. Font glyphs do not guarantee accessible interfaces; follow ACCESSIBILITY.md.

## Next release gates

1. Run installation and rendering checks on Windows, macOS, Linux, and multiple browser engines.
2. Evaluate native-grid reading comfort in code, tables, product labels, and longer paragraphs.
3. Refine glyphs using actual text samples and ambiguity reports.
4. Run an independent font validator and review licenses/provenance again before wider packaging.
5. Publish a tagged alpha with versioned assets, coverage, source revision, license, checksums, and known issues.
6. Consider package-manager submission only when the corresponding distribution exists.

## Adoption

The project's growth depends on usability, original design, reliable downloads, documentation, and sustained maintenance. A large star count is an ambition, not a product feature or promised result.

Use real demonstrations, transparent release notes, useful examples, and contributor feedback. Track actual downloads, issue quality, repeat use, and contributions alongside stars. Do not invent endorsements, usage figures, distribution packages, or popularity badges.
