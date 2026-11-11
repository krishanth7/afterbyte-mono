# Accessibility

Keep documentation and contribution workflows usable with keyboard access, assistive technologies, zoom, and reduced motion. No complete accessibility audit or WCAG certification is claimed.

The current Afterbyte Mono 5.0 has continuous outlines, not a native pixel grid. Let users change font and size, preserve zoom, and provide a readable fallback. Expanded-font FreeType tests cover 12/24/48 px; the original core also covers 12/16/24/32/48/96 px but do not prove readability on every system.

## Documentation and specimens

- Keep critical information as real text.
- Give informative images meaningful alternatives and equivalent proofing text.
- Use semantic headings and descriptive links.
- Do not require the custom font to read installation or license guidance.
- Do not rely on color alone for status.
- Preserve focus, keyboard access, and reduced motion in future interactive specimens.
- Document actual Unicode coverage and fallbacks.

The README specimens use compiled glyph paths, include SVG descriptions, and link text equivalents. GitHub renders the surrounding README in its own font.

Box-drawing rows require line-height 1.04 for the current metric envelope; normal text benefits from more spacing. V4/v5 enlarge line metrics to 1280/−450 for extended accents. Use generous prose line spacing; the 1.04 setting applies only to the original connected box-drawing grid.

Report barriers using the Accessibility issue form with task, file/page, expected and actual result, and optional environment details. Do not require medical information.

## Interactive website

- All site typography uses the self-hosted Afterbyte Mono font, with a system monospace fallback while loading or for unsupported visitor input.
- Light and dark themes follow the initial system preference and remember an explicit choice locally.
- A persistent Pause motion control stops ambient effects. System reduced-motion preference disables animation, pointer tilt, and smooth scrolling. Off-screen ambient scenes pause automatically.
- Specimen size, tracking, line height, alignment, sample selection, signal tuning, glyph search, pagination, theme, and scene controls support keyboard access.
- Critical copy stays visible when JavaScript is unavailable; the full text coverage list and font downloads remain available.
- Character insertion updates the inspector without moving keyboard focus to a distant textarea.
- The signal lab is explicitly labeled as a simulation. Decorative waves, ticker duplicates, and orbital art are hidden from assistive technology.
- Desktop and narrow-screen browser checks supplement the coverage tests; these do not constitute a complete accessibility audit.
