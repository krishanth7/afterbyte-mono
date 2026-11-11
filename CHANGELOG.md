# Changelog

## 0.3.0 alpha — 2026-11-11

### Changed
- Replaced pixel construction with independently drawn continuous-vector centerlines.
- Added a flat-top A, dotted zero, single-storey a/g, rounded bowls, and redesigned figures and terminals.
- Changed metrics to 1000 UPEM, 650-unit advances, 700 cap height, 500 x-height, and 820/−220 typographic bounds. Existing text layouts may reflow.
- Rebuilt TTF/WOFF2, metadata, checksums, coverage, CSS, and actual-font specimens.
- Updated README, source documentation, provenance, and continuous-vector validation.

### Scope
- 196 Unicode mappings retained. No legal clearance or independent certification is claimed.
- Earlier source studies remain historical files; the current build does not use their glyph geometry.

## 0.2.0 alpha — 2026-11-10

### Changed
- Afterbyte Mono replaces the Gothic direction as the primary family and README identity.
- Original light pixel monospace design with 196 Unicode mappings and a fixed 900-unit advance.
- Professional actual-font hero, light/dark specimens, native-size proofs, download table, and usage documentation.

### Added
- Original pixel-matrix sources, TTF/WOFF2 build, CSS, coverage, license metadata, and checksums.
- Selected accented Latin, currencies, arrows, status symbols, box drawing, and shade characters.
- Source occupancy, fixed-pitch, shaping, native raster, binary equivalence, and reproducibility checks.

### Preserved
- The earlier Vantablack Gothic experiment remains in separate directories for project history.

## 0.1.0 alpha — 2026-11-10

### Added
- Original Vantablack Gothic proportional Regular font with 95 printable ASCII mappings and .notdef.
- Reproducible FontTools TTF/WOFF2 build from original polygon recipes and normalized JSON sources.
- CSS, embedded MIT license metadata, font license copy, and SHA-256 checksums.
- Actual-font outline hero and light/dark glyph sheets in the README.
- Binary, geometry, shaping, raster, and source-contract validators.
- Direct polygon-source compilation through --from-source.

### Changed
- README now presents the latest implemented Vantablack Gothic alpha with downloads and usage.
- The root MIT license is explicitly selected for original font outlines and binaries.
- The specification records implementation decisions and alpha optical adjustments.
- Community docs and automated checks now describe the working alpha.

### Limitations
No hinting, shipped kerning, extended Unicode coverage, extra weights, variable axes, cross-platform installation audit, or independent certification. The downloadable alpha is committed to main; no tagged release is claimed.

## Initial repository setup — 2026-11-10
- Afterbyte Mono identity, design brief, proofing text, roadmap, and contribution templates.
- Security and accessibility policies.
- Vantablack Gothic four-part specification and machine-readable design contract.
