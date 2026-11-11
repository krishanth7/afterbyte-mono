# Put Afterbyte Mono to work

## Desktop and design tools

Download the v5 release ZIP. Install either `AfterbyteMono-Regular.otf` or `.ttf`; both share the same family/style. Replace earlier installations, restart your application and select Afterbyte Mono Regular. One Regular style is available. Check your actual text at the size and display scale you intend to use.

## Self-hosted web interface

Keep the supplied `afterbyte-mono.css` beside the font files and load it from your own project. Paths resolve relative to the stylesheet. Use WOFF2, with WOFF fallback if needed. A practical starting point is 16 px with 1.75 line height and zero added letter spacing; review the result in context.

```css
.telemetry, .data-label {
  font-family: "Afterbyte Mono", monospace;
  font-weight: 400;
  font-synthesis: none;
  line-height: 1.75;
  font-variant-ligatures: none;
}
```

Font-display swap lets readable fallback text appear while the font loads. Keep user controls for font choice, zoom and size. Do not require a custom font to access critical information.

## Editor configuration

After installing the TTF or OTF, use this VS Code `settings.json` fragment:

```json
{
  "editor.fontFamily": "'Afterbyte Mono', monospace",
  "editor.fontSize": 16,
  "editor.fontLigatures": false
}
```

This is a starting configuration, not a claim that every editor/OS combination has been audited. Mathematical Unicode styles are individual characters, not additional editor font weights.

## Connected box drawing

For the original box-drawing grid, use zero letter spacing and line height 1.04. Keep this setting scoped to connected diagram rows; accented prose needs more vertical space. Mixed box styles from the expanded repertoire still benefit from optical review in your application.

## Multilingual text

Check the exact [coverage](../fonts/afterbyte-mono/coverage.txt). Use supported precomposed characters. Combining-mark positioning and complex shaping are not implemented; use a fallback for unsupported characters and scripts. The live specimen flags code points requiring fallback. Font coverage is not a complete language-support certification.

## Redistribution

Keep [OFL.txt](../OFL.txt), copyright notices and attribution with redistributed font software. The ZIP includes original upstream notices and source provenance. Read the license before repackaging or modifying the font. Documents made using the font are not licensed as font software merely because they use it.
