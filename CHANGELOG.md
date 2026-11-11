# Changelog

## Unreleased — font license and repository cleanup

### Changed
- Adopted SIL Open Font License 1.1 for Afterbyte Mono sources, binaries, build scripts, artwork, and documentation; no Reserved Font Names are declared.
- Embedded the full OFL in OTF, TTF, WOFF, and WOFF2; regenerated checksums and updated license metadata and documentation.
- Removed the retired display-family files, generators, specimens, documentation, templates, and workflow checks.
- Kept the current glyph design, metrics, four-format downloads, and Sponsors configuration.

## Font formats and sponsorship — 2026-11-11

### Added
- Genuine OpenType/CFF OTF and WOFF files alongside the existing TTF and WOFF2 builds.
- Four-format downloads, CSS fallbacks, checksums, and cross-format validation.
- GitHub Sponsors funding configuration for krishanth7 and a README Sponsors section.
- Sponsorship scope and acknowledgment guidance.

### Preserved
- The 0.3 glyph design, family names, and existing TTF/WOFF2 bytes are unchanged.

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
- Afterbyte Mono establishes the primary family and README identity.
- Original light pixel monospace design with 196 Unicode mappings and a fixed 900-unit advance.
- Professional actual-font hero, light/dark specimens, native-size proofs, download table, and usage documentation.

### Added
- Original pixel-matrix sources, TTF/WOFF2 build, CSS, coverage, license metadata, and checksums.
- Selected accented Latin, currencies, arrows, status symbols, box drawing, and shade characters.
- Source occupancy, fixed-pitch, shaping, native raster, binary equivalence, and reproducibility checks.
