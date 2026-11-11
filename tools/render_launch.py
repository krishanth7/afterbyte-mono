#!/usr/bin/env python3
"""Render an actual-font 1280×640 repository/social preview. OFL-1.1."""
from render_afterbyte import Page

def render():
    page=Page(1280,640,'Afterbyte Mono 5.0 — technical monospace',
        'Afterbyte Mono. 2500 glyphs. OTF, TTF, WOFF and WOFF2. Selected Latin, Greek, Cyrillic and technical symbols. SIL Open Font License 1.1. Lettering uses the actual font.',
        '#101719','#f4f4ed','#b0bcba','#ff9771')
    page.rect(64,54,8,22,page.accent)
    page.text('OPEN-SOURCE TYPE SYSTEM / V5.0.0',88,72,18,page.muted)
    page.rect(64,112,1152,1,'#384648')
    page.text('Afterbyte Mono',58,286,112)
    page.text('Type for what comes next.',64,354,32,page.muted)
    page.text('0O  1Il  Aag  /  ΩΔλπ  ЖДЯ  ∑∫∞',64,444,36)
    page.rect(64,496,1152,1,'#384648')
    page.text('2,500 GLYPHS',64,552,28,page.accent)
    page.text('OTF / TTF / WOFF / WOFF2',480,552,22)
    page.text('SIL OFL 1.1',64,598,16,page.muted)
    page.text('github.com/krishanth7/afterbyte-mono',620,598,16,page.muted)
    page.save('launch-banner')
    print('Rendered 1280x640 launch banner from actual Afterbyte glyphs.')

if __name__=='__main__':render()
