# Contributing

Name the affected project in issues and pull requests: **Vantablack Gothic** is now an installable proportional display alpha; **Afterbyte Mono** remains an unbuilt pixel monospace study.

## Propose and design

Search existing issues. Describe the problem and intended use. Discuss changes to family identity, licensing, core metrics, source format, or coverage before implementing them.

Submit original work with author and provenance. Never trace, rename, or bundle third-party font outlines. The original Vantablack font sources, binaries, recipes, documentation, and artwork are explicitly MIT licensed under LICENSE. Third-party dependencies retain their own terms.

## Sources and build

Use Python 3.12 in an isolated environment and install requirements-font.txt. Run:

```sh
python tools/build_vantablack.py
python tools/validate_vantablack_spec.py
python tools/validate_vantablack_font.py
```

The default build regenerates normalized glyphs.json from geometric recipes. To compile directly edited polygon sources, use `python tools/build_vantablack.py --from-source`; changing an advance also requires updating system.json.

Keep the four-part specification, alpha decision notes, metric contract, sources, binaries, and checksums synchronized. Preserve integer geometry and the documented alpha exceptions.

## Validation and specimens

Run both validators after changes. They cover contract/link checks and actual geometry/binary/shaping/raster checks. They do not establish readability or universal platform support.

For visual changes, regenerate specimens using `python tools/render_vantablack.py` and review light and dark proofs. The optional renderer uses the Linux DejaVu Sans Mono system path for metadata labels. Include before/after glyph comparisons with text descriptions.

Follow ACCESSIBILITY.md and do not claim language coverage, hinting, kerning, or platform support that has not been implemented and tested.

## Pull requests and reporting

Use a focused branch and explain resulting behavior, rationale, validation, and limitations. Update CHANGELOG.md when relevant. Read CODE_OF_CONDUCT.md; use SECURITY.md for vulnerabilities and the Accessibility issue template for barriers.
