<div align="center">
<img src="assets/afterbyte-mono/launch-banner.svg" alt="Afterbyte Mono 5.0.0, a technical monospace with 2500 glyphs, a dotted zero and a flat-top A." width="100%">

# Afterbyte Mono

**Type for what comes next.**

A technical monospace with **2,500 glyphs**, four font formats and an open font license.

![Version](https://img.shields.io/badge/version-5.0.0-006577?style=flat-square)
[![Font quality checks](https://github.com/krishanth7/afterbyte-mono/actions/workflows/specification.yml/badge.svg)](https://github.com/krishanth7/afterbyte-mono/actions/workflows/specification.yml)
[![SIL Open Font License](https://img.shields.io/badge/license-OFL--1.1-334A5B?style=flat-square)](OFL.txt)

**[Try the live specimen](https://krishanth7.github.io/afterbyte-mono/)** · **[Download v5.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v5.0.0)** · [v4.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v4.0.0) · [Specimen](#specimen) · [Coverage](#character-coverage) · [Sponsor](https://github.com/sponsors/krishanth7)
</div>

## Try it in a minute

1. **[Open the specimen](https://krishanth7.github.io/afterbyte-mono/)** — type your own text, adjust size, tracking and line height, switch light/dark themes, explore interactive signal/code/editorial scenes, and inspect the character grid.
2. **[Download the complete v5 ZIP](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/AfterbyteMono-v5.0.0.zip)** — choose OTF or TTF for desktop use; WOFF2 or WOFF for the web.
3. **[Put it in a real project](docs/USAGE.md)** — start with web CSS, editor settings or a technical interface. Keep the included OFL and copyright notices with redistributed fonts.

| What you notice | Why it matters |
| --- | --- |
| Dotted zero and distinct 1/I/l | Easier character identification in labels and data |
| Flat-top A, single-storey a/g, rounded bowls | A recognisable technical voice |
| Fixed 650-unit advances | Predictable alignment for structured text |
| Latin, Greek, Cyrillic and technical symbols | A broader, explicitly documented repertoire |
| OTF, TTF, WOFF and WOFF2 | Desktop installation and self-hosted web use |
| Source, coverage contracts and OFL notices | Inspectable builds and clear attribution |

## Overview

Afterbyte Mono combines an original continuous-vector core with a licensed multilingual expansion. A flat-top A, dotted zero, single-storey a/g, rounded bowls, and fixed 650-unit advances give the family a restrained technical character. It is maintained by [Krishanth](https://github.com/krishanth7).

**v5.0.0 contains exactly 2,500 glyphs: 2,499 Unicode-mapped glyphs plus the `.notdef` fallback.** One Regular style is supplied in genuine OpenType/CFF OTF, TTF, WOFF, and WOFF2. The fonts themselves identify as version 5.000; v4 fonts identify as 4.000.

The original 196 mapped glyphs retain their outlines. Selected additional Latin, Greek, Cyrillic and symbols derive from **Noto Sans Mono 2.014**, under the same SIL Open Font License. Braille patterns, additional technical operators and mathematical styles are constructed programmatically. See [provenance and attribution](docs/PROVENANCE.md); the expanded font is not claimed to be wholly drawn from scratch.

## Releases

| Release | Design milestone | Glyphs | Unicode characters | Formats |
| --- | --- | ---: | ---: | --- |
| [v1.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v1.0.0) | Historical pixel design | 197 | 196 | TTF, WOFF2 |
| [v2.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v2.0.0) | Historical vector redesign | 197 | 196 | TTF, WOFF2 |
| [v3.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v3.0.0) | Original four-format package | 197 | 196 | OTF, TTF, WOFF, WOFF2 |
| [v4.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v4.0.0) | Multilingual and technical expansion | **1,705** | **1,704** | OTF, TTF, WOFF, WOFF2 |
| [v5.0.0](https://github.com/krishanth7/afterbyte-mono/releases/tag/v5.0.0) | Extended scripts and mathematical styles | **2,500** | **2,499** | OTF, TTF, WOFF, WOFF2 |

V4 adds **1,508 Unicode mappings** over v3. V5 adds **795** over v4 and retains every v4 mapping. Each release includes its exact coverage, font license, checksum manifest, installation notes, source/build materials and four-format downloads where listed. V1–v3 milestone numbering differs from their historical embedded build versions; v4–v5 align release and binary versions.

## Character coverage

| Character group | v4 | v5 |
| --- | ---: | ---: |
| Printable ASCII | 95 | 95 |
| Additional Latin and Latin extensions | 431 | 716 |
| Greek and Greek Extended | 121 | 354 |
| Cyrillic and extensions | 297 | 377 |
| Punctuation, currencies, arrows, operators, box drawing, blocks and geometry | 504 | 504 |
| Braille patterns | 256 | 256 |
| Selected mathematical alphabet and digit styles | 0 | 197 |
| **Unicode characters** | **1,704** | **2,499** |
| Fallback `.notdef` glyph | 1 | 1 |
| **Total glyphs** | **1,705** | **2,500** |

Examples: `Ł Œ ą ě ŷ Ḃ ẞ` · `Α Ω Δ λ π ἀ ὦ` · `Ж Д Я ж д я` · `€ £ ¥ ₹` · `∑ ∏ ∫ ∞ ≠ ≤ ≥` · `← ↑ → ↓ ↔ ↕` · `┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘` · `⠁ ⠿ ⣿` · `𝐀 𝐁 𝑥 𝒚 𝟘`.

Coverage is an explicit selection, **not all Unicode symbols or complete support for every language**. Combining marks, complex shaping, emoji and CJK are outside this build. Use precomposed supported characters and a fallback font. The mathematical Unicode styles are separate characters, not extra selectable CSS weights. Braille glyphs depict dot patterns; the font is not a Braille translation or tactile-output system.

[Every supported code point and its source](fonts/afterbyte-mono/coverage.txt) · [Machine-readable v5 contract](sources/afterbyte-mono/coverage-v5.json) · [v4 contract](sources/afterbyte-mono/coverage-v4.json) · [Coverage summary](fonts/afterbyte-mono/coverage-summary.json)

## Specimen

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/afterbyte-mono/specimen-dark.svg">
  <img src="assets/afterbyte-mono/specimen-light.svg" alt="Afterbyte Mono 5.0 actual-font specimen: Latin, Greek, Cyrillic, numbers, mathematics, Braille and connected box drawing." width="100%">
</picture>

Specimen lettering comes from the compiled font. The surrounding README uses GitHub's typography. [Text equivalent](specimen/afterbyte-mono.txt).

## Downloads

| Get the font | Use it for |
| --- | --- |
| [Complete ZIP](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/AfterbyteMono-v5.0.0.zip) | All formats, source materials, coverage, license and checksums |
| [OTF](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/AfterbyteMono-Regular.otf) | OpenType/CFF desktop font |
| [TTF](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/AfterbyteMono-Regular.ttf) | Desktop installation and editors |
| [WOFF2](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/AfterbyteMono-Regular.woff2) · [WOFF](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/AfterbyteMono-Regular.woff) | Self-hosted websites and applications |
| [Release checksums](https://github.com/krishanth7/afterbyte-mono/releases/download/v5.0.0/SHA256SUMS) | Verify the downloaded files |

## Installation and usage

Download the complete ZIP from the desired release. Install **either OTF or TTF**; they share the same family and style names. Restart applications after replacing older versions. Keep the included OFL and attribution notices with redistributed font software.

For self-hosted websites, keep the supplied CSS beside the font files:

```css
@font-face {
  font-family: "Afterbyte Mono";
  src: url("./AfterbyteMono-Regular.woff2") format("woff2"),
       url("./AfterbyteMono-Regular.woff") format("woff");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
.technical-text {
  font-family: "Afterbyte Mono", monospace;
  font-size: 16px;
  line-height: 1.75;
  font-synthesis: none;
}
```

All mapped characters advance 650 units on a 1000-UPEM grid. Typographic ascender/descender are **1280/−450**, enlarged to accommodate extended accents; this changes line spacing from v3. Inspect text in your actual application. Original connected box-drawing rows use `line-height: 1.04` and zero letter spacing; do not apply that tight setting to accented prose.

[Current font directory](fonts/afterbyte-mono) · [CSS](fonts/afterbyte-mono/afterbyte-mono.css) · [SHA-256 checksums](fonts/afterbyte-mono/SHA256SUMS)

## Build and validation

Use Python 3.12 and the pinned dependencies. The licensed expansion source is vendored and hash-checked; ordinary builds need no network access.

```sh
python -m pip install -r requirements-font.txt
python tools/draw_afterbyte_vector.py
python tools/build_afterbyte.py --version 4 --output build/v4/fonts
python tools/build_afterbyte.py --version 5
python tools/validate_afterbyte.py
python tools/validate_expansion.py --version 4 --directory build/v4/fonts
python tools/validate_expansion.py --version 5
python tools/render_afterbyte.py
```

`build_core.py` compiles the original 196-character core. `prepare_expansion.py` can reproduce the frozen licensed source from the pinned upstream download and verifies its SHA-256. The coverage contracts determine the exact mapping set. All releases use fixed timestamps and reproducible font containers.

Checks cover every mapped character, glyph counts, coverage inclusion, retained core outlines, Braille dot bits, mathematical style distinctions, full embedded licenses, fixed spacing, bounds, container signatures, webfont outlines, CFF geometry bounds, shaping, rendering, checksums and reproducibility.

The specimen uses Afterbyte Mono throughout, with light/dark themes, an animated signal study, a live typography console, three interactive interface scenes, and a searchable character inspector. Motion can be paused and follows the system reduced-motion preference.

The specimen runs without a framework, remote fonts or tracking scripts. Search, group totals, supplementary Unicode handling, fallback warnings and pagination are checked with `node --test tests/playground.test.mjs`.

These checks do not constitute a complete language, accessibility, OS-installation or browser audit. The font has one Regular style, no variable axes, no combining-mark positioning or ligature system, and no bytecode hinting. See [quality notes](docs/QUALITY.md), [design specification](docs/DESIGN.md) and [roadmap](ROADMAP.md).

## Built something with Afterbyte?

**[Show your project](https://github.com/krishanth7/afterbyte-mono/issues/new?template=showcase.yml).** Share a screenshot you can publish, a short description, and the release/platform/size you used. Permission is requested before featuring your work in the README. The showcase is open for submissions; no third-party adoption is implied.

If the font is useful to you, a GitHub star helps you find it again. Share the [live specimen](https://krishanth7.github.io/afterbyte-mono/) with someone who can use it, or contribute a concrete rendering report. Good places to start:

- **Language review:** compare supported precomposed Greek, Cyrillic and extended Latin in real text.
- **Application proofing:** report version, OS, application, size, display scale, sample and expected result.
- **Documentation:** improve installation instructions with a reproducible example.
- **Design examples:** show a real interface or a clearly labelled concept and explain your typography choices.

[Contribution guide](CONTRIBUTING.md) · [Usage recipes](docs/USAGE.md) · [Launch kit and shareable assets](docs/launch/README.md) · [Roadmap](ROADMAP.md)

## Sponsors

**[Support the maintainer on GitHub Sponsors](https://github.com/sponsors/krishanth7).** Support helps fund type refinement, character coverage, rendering tests, documentation and maintenance across Krishanth's open-source work. Sponsorship is optional; public acknowledgments require verified support and permission. [Sponsorship details](SPONSORSHIP.md).

## Contributing

Report the release, code point, text sample, application, operating system, size and observed behavior. Contributions must document authorship and compatible licensing, including all third-party notices.

[Contributing](CONTRIBUTING.md) · [Issue forms](https://github.com/krishanth7/afterbyte-mono/issues/new/choose) · [Pull request template](.github/pull_request_template.md) · [Code of conduct](CODE_OF_CONDUCT.md) · [Security](SECURITY.md) · [Accessibility](ACCESSIBILITY.md)

## License and attribution

Afterbyte Mono is distributed under the **[SIL Open Font License 1.1](OFL.txt)**. Copyright © 2026 Krishanth; selected expansion glyphs copyright 2022 The Noto Project Authors. Original upstream notices and the OFL are preserved in [sources/upstream](sources/upstream). No Reserved Font Names are declared in the supplied licenses. Dependencies retain their own licenses.

Commercial use and embedding are permitted under the OFL terms. Redistributed font software must retain the license and copyright notices; font software may not be sold by itself. Documents made with the font are not covered by the font license. Earlier distributions retain the permissions previously granted. [Provenance](docs/PROVENANCE.md) records the source inputs and modifications.
