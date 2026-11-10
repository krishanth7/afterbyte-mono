# Contributing

Afterbyte Mono is the primary font: a light pixel monospace with a fixed 900-unit advance. Identify the affected family when reporting issues; the earlier Vantablack Gothic experiment is retained separately.

## Proposals

Search existing issues, provide a text sample and use case, and discuss major changes to metrics, identity, source format, license, or coverage before implementation.

For rendering reports include font version, OS, application/browser, size, zoom/display scale, and a screenshot if available. Test native 16-pixel multiples and other sizes separately.

## Sources

Contribute original matrices with clear authorship and provenance. Do not trace, rename, or bundle another font. Original Afterbyte sources, binaries, recipes, documentation, and artwork use LICENSE (MIT); dependencies retain their own licenses.

The editable source is sources/afterbyte-mono/pixels.json. Every glyph must preserve the 900-unit advance, pixel grid, and supported metric envelope.

## Build and validation

Use Python 3.12 in an isolated environment and install requirements-font.txt:

```sh
python tools/build_afterbyte.py
python tools/validate_afterbyte.py
python tools/render_afterbyte.py
```

To change the original generator, edit tools/draw_afterbyte.py, run it, then build and validate. The generator overwrites direct JSON edits.

Review actual-font light/dark proofs, ambiguity pairs, accents, punctuation, and box drawing. Keep documentation, coverage, checksums, and specimens synchronized. A passed raster smoke check does not establish readability on every system.

## Pull requests

Explain the problem, resulting change, validation, and limits. Include before/after glyph comparisons with text descriptions and update CHANGELOG.md. Avoid unimplemented feature, language, or popularity claims.

Follow ACCESSIBILITY.md and CODE_OF_CONDUCT.md. Report vulnerabilities through SECURITY.md. The issue forms include accessibility and design-proposal templates.
