# Afterbyte Mono — Design provenance

## Current design: 0.3.0 alpha / 2026-11-11

The current font is a continuous-vector redesign developed for this project with AI assistance. Krishanth maintains the repository.

### Source inputs

- tools/draw_afterbyte_vector.py: explicit original centerline coordinates, accent compositions, and technical-symbol geometry.
- sources/afterbyte-mono/vectors.json: editable source generated from those recipes.
- tools/build_afterbyte.py: geometry/compiler adapter.
- Root LICENSE: project license metadata and binary license copy.

The generator and compiler do not read another font, font bitmap, glyph outline collection, or website artwork. They do not consume the old Afterbyte pixel matrices. Dependencies such as FontTools, Shapely, and Brotli provide general-purpose geometry/compiler functions.

### Design changes from 0.2

- Continuous curves and diagonals replace pixel staircases.
- 1000 UPEM and 650-unit advances replace 1600 UPEM and 900-unit advances.
- A flat-top A replaces the pixel apex.
- A dotted zero replaces the slashed zero.
- Single-storey a/g, rounded bowls, and new R/Q/terminal geometry replace the earlier matrices.
- Shade symbols use continuous stripe patterns.

These are documented design decisions, not an infringement test or a claimed percentage of uniqueness.

## Earlier work

Version 0.2 was an independently generated pixel study that used Departure Mono as a visual category reference. The pixel source study and commit history are retained for transparency.

No claim is made that all design ideas, generic letter shapes, or naming terms are exclusive to this project.

## Licensing context

Afterbyte Mono font binaries, editable font sources, build scripts, artwork, and documentation are released under the [SIL Open Font License 1.1](../OFL.txt). No Reserved Font Names are declared. Third-party dependencies retain their own licenses.

The full license is included in the repository and font directory and embedded in every distributed font format. Contributors must identify external material and its applicable terms before inclusion. This license change applies to the current distribution; it does not withdraw permissions already granted for earlier versions.

## Limits of this record

This records the inputs and work performed, not a lawyer's determination of copyright eligibility, trademark availability, infringement, or jurisdiction-specific rights. No legal clearance or guarantee against future claims is provided.
