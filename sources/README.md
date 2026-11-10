# Font sources

## Vantablack Gothic

[vantablack-gothic/glyphs.json](vantablack-gothic/glyphs.json) contains normalized original contours for the 96-glyph alpha: 95 printable ASCII characters plus .notdef.

Original recipe source: [build_vantablack.py](../tools/build_vantablack.py). Metrics: [system.json](../docs/vantablack-gothic/system.json). All original font sources and binaries are under the root MIT license.

The default build regenerates this JSON from recipes. To compile directly edited JSON without overwriting it, use `python tools/build_vantablack.py --from-source`. Update the metric contract when changing advances, validate, and regenerate specimens.

## Afterbyte Mono

The earlier pixel monospace concept is still unbuilt. Its separate [design brief](../docs/DESIGN.md) remains a planning document.
