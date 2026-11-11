# Accessibility

Keep documentation and contribution workflows usable with keyboard access, assistive technologies, zoom, and reduced motion. No complete accessibility audit or WCAG certification is claimed.

The current Afterbyte Mono 0.3 has continuous outlines, not a native pixel grid. Let users change font and size, preserve zoom, and provide a readable fallback. Local FreeType tests cover 12/16/24/32/48/96 px but do not prove readability on every system.

## Documentation and specimens

- Keep critical information as real text.
- Give informative images meaningful alternatives and equivalent proofing text.
- Use semantic headings and descriptive links.
- Do not require the custom font to read installation or license guidance.
- Do not rely on color alone for status.
- Preserve focus, keyboard access, and reduced motion in future interactive specimens.
- Document actual Unicode coverage and fallbacks.

The README specimens use compiled glyph paths, include SVG descriptions, and link text equivalents. GitHub renders the surrounding README in its own font.

Box-drawing rows require line-height 1.04 for the current metric envelope; normal text benefits from more spacing. Version 0.3 changes layout metrics from 0.2.

Report barriers using the Accessibility issue form with task, file/page, expected and actual result, and optional environment details. Do not require medical information.
