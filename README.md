<div align="center">

<img src="assets/afterbyte-mono/hero.svg" alt="Afterbyte Mono — actual font specimen. Clear signals. Human-readable systems. Original pixel monospace for intelligent interfaces." width="100%">

# Afterbyte Mono

**A pixel monospace for intelligent interfaces.**

![Version](https://img.shields.io/badge/version-0.2.0_alpha-006577?style=flat-square)
[![Font quality checks](https://github.com/krishanth7/afterbyte-mono/actions/workflows/specification.yml/badge.svg)](https://github.com/krishanth7/afterbyte-mono/actions/workflows/specification.yml)
[![MIT license](https://img.shields.io/badge/license-MIT-334A5B?style=flat-square)](LICENSE)

**[Download TTF](https://github.com/krishanth7/afterbyte-mono/raw/refs/heads/main/fonts/afterbyte-mono/AfterbyteMono-Regular.ttf)** · **[Download WOFF2](https://github.com/krishanth7/afterbyte-mono/raw/refs/heads/main/fonts/afterbyte-mono/AfterbyteMono-Regular.woff2)** · [Specimen](#specimen) · [Usage](#usage) · [Development](#development)

</div>

## Overview

Afterbyte Mono combines the clarity of a pixel grid with the measured character of a cinematic technical interface. Light, consistent strokes, open counters, and a balanced lowercase alphabet keep the typeface approachable. A slashed zero, distinct `1 I l`, precise punctuation, and useful interface symbols give it a technical identity.

Designed for code samples, terminal-inspired layouts, dashboards, creative tools, and futuristic HUDs. Every spacing glyph shares the same advance, including figures, punctuation, accented letters, and interface symbols.

**Current build:** Regular · 0.2.0 alpha · 196 Unicode characters · TTF and WOFF2 · original pixel sources.

Created and maintained by [Krishanth](https://github.com/krishanth7). This is the primary font in this repository. The earlier proportional display experiment is preserved in the [project history](CHANGELOG.md).

## Specimen

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/afterbyte-mono/specimen-dark.svg">
  <img src="assets/afterbyte-mono/specimen-light.svg" alt="Actual Afterbyte Mono: uppercase and lowercase alphabets; slashed zero and distinct 1/I/l; punctuation; accented Latin; currencies; arrows; code at 16, 32 and 48 px; connected box drawing." width="100%">
</picture>

Every letter in the hero and specimen is drawn from the compiled Afterbyte Mono font. The SVGs contain outline paths, so they display without requiring the font to be installed. GitHub uses its own font for the surrounding README text.

[Full proofing text](specimen/afterbyte-mono.txt) · [Exact coverage](fonts/afterbyte-mono/coverage.txt) · [Editable pixel matrices](sources/afterbyte-mono/pixels.json)

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789   0O   1Il   rn m
ÄÖÜ äöü ß   ÀÉÎÑ   æ ø   € £ ¥ ₹
← → ↑ ↓ ↔ ↕   ✓ ■ □
```

## Downloads

| File | Use |
| --- | --- |
| [AfterbyteMono-Regular.ttf](https://github.com/krishanth7/afterbyte-mono/raw/refs/heads/main/fonts/afterbyte-mono/AfterbyteMono-Regular.ttf) | Desktop applications, editors, and local installation |
| [AfterbyteMono-Regular.woff2](https://github.com/krishanth7/afterbyte-mono/raw/refs/heads/main/fonts/afterbyte-mono/AfterbyteMono-Regular.woff2) | Self-hosted websites and applications |
| [afterbyte-mono.css](fonts/afterbyte-mono/afterbyte-mono.css) | Ready-to-use font-face declaration |
| [SHA256SUMS](fonts/afterbyte-mono/SHA256SUMS) | Verify binary integrity |
| [pixels.json](sources/afterbyte-mono/pixels.json) | Original editable character matrices |

The links point to the latest files on `main`. A tagged stable release and package-manager distribution have not been published.

## Usage

### Desktop

Download the TTF, open it in your operating system's font viewer, and choose Install. Select **Afterbyte Mono — Regular** in your application.

Start with **16, 32, 48, or 64 px** for clean alignment to the source pixel grid. Other sizes are valid, but may introduce antialiasing or uneven apparent strokes. Browser zoom, display scaling, and an application's rasterizer can also affect the result.

### Web

Copy the [font directory](fonts/afterbyte-mono) to your project and load its CSS, or add:

```css
@font-face {
  font-family: "Afterbyte Mono";
  src: url("./AfterbyteMono-Regular.woff2") format("woff2"),
       url("./AfterbyteMono-Regular.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

.technical-text {
  font-family: "Afterbyte Mono", monospace;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0;
  font-synthesis: none;
}
```

Resolve the font URLs relative to your CSS file. Serve the files from your own application; GitHub's download URLs are not a production font CDN.

For connected box-drawing rows, use `line-height: 1` and `letter-spacing: 0`. The line glyphs fill their cell boundaries. For normal text, increase line height to suit the reading context.

## Coverage and design

| Property | Value |
| --- | --- |
| Family / style | Afterbyte Mono / Regular |
| Spacing | True monospace; 900-unit advance |
| Grid / em | 100-unit square pixels / 1600 UPEM |
| Native size | 16 px; integer multiples align to the pixel grid |
| Cap / x-height | 1000 / 700 units |
| Ascender / descender | 1300 / −300 units |
| Coverage | 196 Unicode characters + visible missing-glyph symbol |
| Shape language | Light single-pixel strokes; stepped contours; open forms |
| Source and binary license | MIT |

Included: all 95 printable ASCII characters, selected accented Latin letters, German umlauts and ß, Æ/æ and Ø/ø, €, £, ¥ and ₹, typographic punctuation, arrows, status marks, 11 box-drawing characters, and block/shade symbols.

This is **selected Unicode coverage**, not complete Latin-1 or universal language support. Use a fallback for unsupported characters. See the [exact code-point list](fonts/afterbyte-mono/coverage.txt).

## Development

Use Python 3.12 and the pinned dependencies:

```sh
python -m venv .venv
# Activate your environment before installing dependencies.
python -m pip install -r requirements-font.txt

python tools/draw_afterbyte.py
python tools/build_afterbyte.py
python tools/validate_afterbyte.py
python tools/render_afterbyte.py
```

The original matrices live in [pixels.json](sources/afterbyte-mono/pixels.json). Edit that file and run the build to compile your changes. Running `draw_afterbyte.py` regenerates it from the original hand-drawn recipes and will overwrite direct matrix edits.

The compiler merges filled pixel cells into contours, preserves the grid, writes a fixed-pitch TTF, and produces WOFF2 from the same data. It never reads or transforms another font. The specimen generator uses only the compiled Afterbyte font for lettering.

[Design specification](docs/DESIGN.md) · [Validation notes](docs/QUALITY.md) · [Roadmap](ROADMAP.md) · [Changelog](CHANGELOG.md)

## Quality and current scope

Automated checks cover source-pixel occupancy, contour topology, grid alignment, equal advances, line metrics, license metadata, TTF/WOFF2 equivalence, HarfBuzz shaping, binary checksums, documentation links, and crisp native-grid FreeType rasterization at 16/32/48/64 px. Rebuilding the original matrices and binaries is checked for reproducibility.

**Alpha limits:** one Regular style; no variable axes, ligatures, or bytecode hinting. Cross-platform installation, additional browser engines, independent font validation, and wider script coverage remain on the roadmap. Local checks do not establish universal readability or accessibility conformance.

## Contributing

Useful reports include the character or text sample, font version, application and operating system, size, zoom/display scale, and a screenshot when available. Specific glyph comparisons and real usage examples help shape the next version.

[Contribution guide](CONTRIBUTING.md) · [Issue templates](https://github.com/krishanth7/afterbyte-mono/issues/new/choose) · [Pull request template](.github/pull_request_template.md)

[Code of conduct](CODE_OF_CONDUCT.md) · [Security policy](SECURITY.md) · [Accessibility](ACCESSIBILITY.md)

## License and inspiration

Copyright © 2026 Krishanth. Original font sources, binaries, artwork, and project documentation are available under the **[MIT License](LICENSE)**. A copy is included with the font files; third-party build dependencies retain their own licenses.

[Departure Mono](https://github.com/rektdeckard/departure-mono) and [its specimen site](https://departuremono.com/) informed the direction: a pixel monospace with a technical, cinematic character. Afterbyte Mono's matrices and outlines were drawn independently. No Departure Mono font data, source glyphs, or artwork are included. This project is not affiliated with Departure Mono or any fictional assistant franchise.

---

<div align="center">
Afterbyte Mono · Clear signals. Human-readable systems.
</div>
