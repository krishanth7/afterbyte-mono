# Font sources

## Current continuous-vector design

[afterbyte-mono/vectors.json](afterbyte-mono/vectors.json) is the current editable centerline source. It contains 196 Unicode records with original M/L/C/Z paths, solids, and stroke settings.

The [vector generator](../tools/draw_afterbyte_vector.py) regenerates the JSON. Compile direct JSON edits with `python tools/build_afterbyte.py` without running the generator.

See [design provenance](../docs/PROVENANCE.md), [design specification](../docs/DESIGN.md), and the root MIT license.

## Historical work

afterbyte-mono/pixels.json and tools/draw_afterbyte.py retain the 0.2 pixel study. They are not inputs to the current build. The separate Vantablack sources preserve the earlier display experiment.
