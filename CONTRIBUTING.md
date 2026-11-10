# Contributing

This repository currently contains two distinct design studies: Afterbyte Mono (pixel monospace) and Vantablack Gothic (proportional condensed display sans). Neither has installable font binaries. Clearly name the affected design in issues and pull requests.

## Propose a change

Search existing issues, describe a concrete use case, and discuss large changes before implementation. Changes to family identity, licensing, metrics, coverage, or source format need explicit review.

## Design contributions

Submit original work with author and provenance. Never trace, rename, or bundle third-party font outlines. Choose and document a dedicated font license before accepting drawn glyph sources. Current specifications, artwork, and scripts remain under LICENSE.

Vantablack changes must keep docs/vantablack-gothic/SPECIFICATION.md and system.json synchronized. Preserve the 1000 UPEM contract, proposed 820/−200 line metrics, proportional advances, polygon construction, and explicit unfinished status.

## Local validation

Run:

```sh
python3 tools/validate_vantablack_spec.py
```

This standard-library script checks the specification contract, ASCII records, and repository-relative Markdown links. It does not build or validate a font.

For documentation, check headings, links, status claims, and image alternatives. Follow ACCESSIBILITY.md. Future outline contributions must also pass the documented build, geometry, naming, coverage, spacing, and rendering checks.

## Pull requests

Use a focused branch. Explain the problem, resulting change, and checks performed. Include relevant before/after drawings or text, describe limitations, and update CHANGELOG.md when appropriate. Do not claim support or validation that has not been demonstrated.

Read CODE_OF_CONDUCT.md and report vulnerabilities through SECURITY.md. Accessibility barriers have a dedicated issue template.
