# Contributing

Afterbyte Mono 0.3 is the current continuous-vector monospace. Older pixel and proportional studies are historical. Identify the version and family in issues and pull requests.

## Original source and provenance

Submit original work with authorship and provenance. Do not trace or rename third-party fonts or assume a new license file removes existing obligations. Disclose any external material and applicable terms before proposing its inclusion. See docs/PROVENANCE.md.

The original current project sources and binaries use LICENSE (MIT). Dependencies retain their own terms. No legal clearance is claimed by the technical validation process.

## Build and review

Use Python 3.12 and requirements-font.txt:

```sh
python tools/draw_afterbyte_vector.py
python tools/build_afterbyte.py
python tools/validate_afterbyte.py
python tools/render_afterbyte.py
```

The current source is sources/afterbyte-mono/vectors.json. The generator overwrites direct JSON edits; run only the build for direct source changes.

Preserve the fixed advance and metric envelope. Review actual-font light/dark proofs, ambiguity pairs, punctuation, accents, and symbols. Keep binaries, checksums, coverage, docs, and specimens synchronized.

## Reports and pull requests

Include font version, text sample, application/OS, size, zoom/display scale, and optional screenshot. Explain resulting behavior, validation, and limits; add before/after glyph comparisons and update the changelog.

Follow CODE_OF_CONDUCT.md and ACCESSIBILITY.md. Use SECURITY.md for vulnerabilities.
