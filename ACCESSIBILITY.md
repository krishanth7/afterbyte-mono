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

- Interface, editable text, SVG labels, and code specimens use self-hosted Afterbyte Mono, with system monospace fallback while loading or for unsupported input.
- Light and dark themes follow the initial system preference and remember explicit local choices. A small script applies the selected theme before the first stylesheet paint.
- Ambient SVG animations run on 45–100-second cycles. The persistent Pause motion control stops them. System reduced-motion preference disables animation and smooth scrolling; off-screen SVGs pause automatically.
- No flashing, title scrambling, fast starfield, autoplay arcade, or scroll hijacking is present. Movable letter tiles support pointer dragging and keyboard arrow positioning; Enter or a click inserts the letter into the type tester. Position changes are bounded to the board and announced through a status region.
- Native controls support specimen size, tracking, line height, alignment, sample selection, category filters, Unicode search, pagination, theme, and application previews.
- Glyph selection updates a separate inspector. Add to tester announces insertion and preserves focus.
- Every one of the 2,499 mapped characters is searchable; the additional unencoded fallback glyph is shown separately. The full text coverage download remains available.
- Interface mockup values are labeled as sample data. Decorative SVGs are hidden from assistive technology; informative diagrams have descriptive accessible names.
- Entered specimen text remains in the page and is excluded from copied sharing links.
- Phone, tablet, and desktop browser checks supplement automated coverage and website checks; no complete accessibility audit or certification is claimed.
