# Accessibility

## Commitment and scope

Keep documentation, contribution workflows, and future specimens usable with keyboard access, assistive technologies, zoom, and reduced motion. No WCAG certification or complete accessibility audit is claimed.

Afterbyte Mono is a light pixel monospace. Native 16-pixel multiples align to its grid in local tests. Reading comfort varies by context, size, zoom, display scale, and visual needs. Let readers change font and size, preserve browser zoom, and provide a conventional fallback.

## Documentation and specimens

- Keep informative text available as real text.
- Give specimen images descriptive alternatives and link proofing text.
- Use semantic headings and meaningful links.
- Never require the custom font to read download or installation instructions.
- Do not use color alone for status.
- Preserve keyboard access, visible focus, and reduced-motion preferences in future interactive specimens.
- Provide fallback glyphs and state actual Unicode coverage.

The README hero and specimen use original glyph paths, include SVG descriptions, and have linked text equivalents. The surrounding README uses GitHub's own typography.

## Font-specific checks

Current local tests cover fixed advances, distinct 0/O and 1/I/l outlines, source occupancy, and crisp FreeType pixels at 16/32/48/64 px. These do not prove universal readability or equivalent behavior in every browser/OS.

Box-drawing rows need line-height 1 to connect; normal text usually benefits from more spacing. Avoid forcing dense terminal layouts on all users.

## Earlier experiment

The preserved Vantablack Gothic face is a dense display experiment; it is no longer the primary project font and should not carry long body text.

## Report a barrier

Use the Accessibility issue form. Identify the file/page, task, expected outcome, actual barrier, and optional environment information. Do not require personal medical information.
