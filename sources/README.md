# Original font sources

## Afterbyte Mono

[afterbyte-mono/pixels.json](afterbyte-mono/pixels.json) stores 196 original Unicode character matrices. Each # is a 100-unit filled square; each . is empty space.

Edit the JSON and run `python tools/build_afterbyte.py` to compile. Run `python tools/validate_afterbyte.py` and regenerate specimens after changes.

[draw_afterbyte.py](../tools/draw_afterbyte.py) regenerates the JSON from original hand-drawn recipes; running it overwrites direct matrix edits. All original sources and binaries use the root MIT license.

## Earlier experiment

[vantablack-gothic/glyphs.json](vantablack-gothic/glyphs.json) preserves the earlier polygon display study. Its separate build scripts remain available.
