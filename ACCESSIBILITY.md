# Accessibility

## Commitment and current status

Documentation, future specimens, and contribution workflows should remain usable with keyboard input, assistive technologies, zoom, and reduced-motion settings. No WCAG conformance certification or completed accessibility audit is claimed.

Afterbyte Mono and Vantablack Gothic are separate design studies. Vantablack's dense counters, high compression, and 15-unit gaps make it a display face; a conventional readable text font should carry body copy, instructions, errors, and safety-critical information.

## Repository content

- Use descriptive headings, meaningful link text, and text alternatives for informative images.
- Keep exact values and comparisons in real Markdown tables.
- Accompany diagrams or future outline specimens with equivalent text.
- Mark examples and unfinished features clearly.
- Include searchable Unicode text with any glyph illustration.

## Future specimen requirements

- Keep specimen text as real selectable text; do not expose unlabelled outlines as the only representation.
- Provide labelled native inputs and buttons, visible keyboard focus, and logical focus order.
- Preserve zoom and reflow; avoid fixed-height clipping of ascenders and descenders.
- Support light/dark contrast, reduced motion, and a readable fallback while fonts load.
- Do not rely on color alone for errors or selected states.
- Do not animate text continuously or flash content.
- Explain font coverage and fallback behavior.
- Test keyboard access, screen-reader output, 200% zoom, narrow layouts, and high-contrast modes.

## Typeface proofing

For Vantablack, test 32/48/64 px as stress cases and 80/120/240 px as initial display cases. At 48 px a 15-unit gap is 0.72 px; disappearance must be recorded rather than described as universal readability. Check 0/O, 1/I/l, rn/m, c/e, punctuation, and multilingual fallbacks.

These checks are planned; no rendered font has been audited yet.

## Report a barrier

Use the Accessibility issue template. Describe the affected page or file, task, browser/OS, assistive technology if relevant, expected result, and actual result. Screenshots or recordings are optional; never require a diagnosis or personal medical information.
