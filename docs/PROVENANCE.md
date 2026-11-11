# Afterbyte Mono — Provenance and attribution

## Original Afterbyte core

The 196-character continuous-vector core was developed for this project with AI assistance and is maintained by Krishanth. `draw_afterbyte_vector.py`, `vectors.json` and `build_core.py` preserve its recipes and compile its outlines. V4 and v5 retain those outlines. The historical pixel study remains separate from the current build inputs.

## Licensed expansion introduced in v4

Selected additional glyphs are derived from **Noto Sans Mono 2.014**. Copyright 2022 The Noto Project Authors (https://github.com/notofonts/latin-greek-cyrillic). The source is licensed under SIL OFL 1.1; its original license is preserved at [sources/upstream/OFL.txt](../sources/upstream/OFL.txt).

Pinned Google Fonts snapshot: `097bc1b8c04c3224087c2ae95f7a923859b778cf`, path `ofl/notosansmono/NotoSansMono[wdth,wght].ttf`.

Original download SHA-256: `2cb2adb378a8f574213e23df697050b83c54c27df465a2015552740b2769a081`.

`prepare_expansion.py` instantiates weight 300 / width 100, subsets the selected 1847 source mappings, removes layout features and fixes timestamps. `NotoSansMono-ExpansionSource.ttf` is a source dependency, not an unmodified Noto product. The expanded compiler decomposes, scales and centers these outlines into Afterbyte’s 650-unit cells. [Machine-readable upstream provenance](../sources/upstream/provenance.json) records the subset hash and transformations.

## Additional programmatic sources

- Three original technical operators: ∏ ∑ ∫.
- All 256 Braille patterns from their Unicode bit definitions, including the intentional blank pattern.
- 197 mathematical-style mappings constructed from original core outlines, with explicit bold, italic and double-struck treatments. The bold nabla has an original triangular recipe.

The v4 and v5 coverage manifests label the origin of every mapped character. Each code point has its own named glyph; no private-use or unassigned mappings are used to reach the requested count. Some Unicode characters legitimately share visual forms, such as sans digits and spaces; the glyph count is not a count of wholly unique designs.

## License and scope

The combined font is released under [SIL OFL 1.1](../OFL.txt), retaining both Krishanth’s and Noto’s copyright notices. The same full notice is embedded in every font container and supplied in each package. No Reserved Font Names are declared in the supplied notices. Third-party tooling retains its own licenses. The Noto project does not endorse this modified font.

The older core’s independent-source description does not apply to the new licensed expansion. No Departure Mono binaries, outlines or source matrices are incorporated. This record documents inputs and changes; it is not a trademark or legal-clearance certification. Earlier licenses already granted for previous distributions remain applicable to those copies.
