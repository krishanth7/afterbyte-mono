## Afterbyte Mono v4.0.0 — Multilingual and technical expansion

**1,705 glyphs: 1,704 Unicode-mapped glyphs plus one `.notdef` fallback.** One Regular style; genuine CFF OTF, TTF, WOFF and WOFF2. Embedded version is **4.000**. This is a regular release.

### Added characters and coverage

**1,508 additional Unicode mappings over v3.0.0.** Adds selected Latin, Greek, Cyrillic, currencies, arrows, mathematical/technical operators, full box-drawing and geometric repertoires available in the selected source, and all 256 Braille patterns. Original Afterbyte recipes supply ∏ ∑ ∫.

| Character group | Count |
| --- | ---: |
| Printable ASCII | 95 |
| Additional Latin and extensions | 431 |
| Greek | 121 |
| Cyrillic | 297 |
| Technical symbols, punctuation, currencies and geometry | 504 |
| Braille patterns | 256 |
| **Unicode mappings** | **1,704** |
| Fallback .notdef | 1 |
| **Total glyphs** | **1,705** |


Examples: `Ł Œ ą ě ŷ` · `Ω Δ λ π` · `Ж Д Я ж д я` · `€ £ ¥ ₹` · `∑ ∏ ∫ ∞ ≠ ≤ ≥` · `← ↑ → ↓ ↔ ↕` · `┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘` · `⠁ ⠿ ⣿`.

The attached coverage file and source contract list every supported code point and its origin. This is selected multilingual and technical coverage, **not all Unicode symbols**. Combining marks, complex shaping, emoji and CJK are not included. Use supported precomposed characters and fallback fonts. Braille is visual dot-pattern coverage, not a translation or tactile-output system.

### Design and engineering

- Retains all 196 original Afterbyte mapped glyph outlines, including the flat-top A, dotted zero and single-storey a/g.
- Selected licensed expansion glyphs derive from **Noto Sans Mono 2.014**, weight 300 / width 100, decomposed and scaled into the Afterbyte grid. This is an attributed OFL expansion, not a wholly new set of original drawings.
- Fixed 650-unit advances on a 1000-UPEM grid; original core cap/x-height 700/500.
- Enlarged shared line metrics: **1280/−450** to accommodate accents. This changes line spacing from v3. Use approximately 1.75 line height for prose and inspect the result in your application.
- Explicit coverage/source manifests, fixed timestamps, all four real font containers, CSS and checksums.

### Files and installation

Download **AfterbyteMono-v4.0.0.zip** for the complete package: four formats, OFL/copyright notices, CSS, exact coverage, coverage summary, source recipes, licensed source dependency, build/validation tools, pinned requirements and installation instructions. Individual font files and a coverage text file are also attached.

Install **either OTF or TTF**, not both; they share the same family/style. Replace cached older installations and restart applications. WOFF2 is preferred for websites, with WOFF fallback. `SHA256SUMS` verifies every attached package/font/coverage/license asset except the checksum file itself.

To rebuild this package's fonts, install `requirements-font.txt` and run `python tools/build_afterbyte.py --version 4`. The vendored source permits offline builds after tooling is installed; upstream reconstruction is optional and hash-checked.

### License and attribution

**SIL Open Font License 1.1.** Copyright 2026 Krishanth; selected expansion glyphs copyright 2022 The Noto Project Authors. The full combined notice is embedded in each font, and the original upstream OFL is retained in the source package. No Reserved Font Names are declared in the supplied notices; dependencies retain their own terms.

### Validation and limits

Exact counts and coverage; retained core outlines; Braille bit patterns; mathematical style checks where applicable; four-format metadata and bounds; source hashes; each character shaped with HarfBuzz; all nonblank mapped glyphs rendered at 12/24/48 px in each decoded format; matching checksums and deterministic rebuilds. Actual-font specimens were reviewed. These are technical checks, not a complete native-language, accessibility or cross-platform certification. One Regular style; no variable axes, combining-mark positioning, ligatures or bytecode hinting.

### Release history

| Version | Glyphs | Unicode mappings | Milestone |
| --- | ---: | ---: | --- |
| [v1.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v1.0.0) | 197 | 196 | Pixel design |
| [v2.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v2.0.0) | 197 | 196 | Vector redesign |
| [v3.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v3.0.0) | 197 | 196 | Four-format package |
| [v4.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v4.0.0) | 1,705 | 1,704 | Multilingual and technical expansion |
| [v5.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v5.0.0) | 2,500 | 2,499 | Extended scripts and mathematical styles |

[Repository and specimens](https://github.com/krishanth7/afterbyte-mono) · [Sponsor the maintainer](https://github.com/sponsors/krishanth7)
