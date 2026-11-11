#!/usr/bin/env python3
"""Render light/dark specimen images from compiled Afterbyte outlines."""
from render_afterbyte import Page

def render():
    for theme, colors in {
        'light': ('#f7f8fa','#1e293b','#596779','#375de8','#ffffff','#dce2eb'),
        'dark': ('#10151e','#e9eef7','#b0bfd3','#9bb5ff','#171e2a','#303c4f'),
    }.items():
        bg,ink,muted,accent,surface,line=colors
        page=Page(1280,640,'Afterbyte Mono — Precision with character.',
            'Afterbyte Mono v5.0.0. 2,500 glyphs including 2,499 Unicode characters. Four formats. Actual compiled font outlines.',bg,ink,muted,accent)
        page.text('afterbyte / mono',54,64,23)
        page.text('V5.0.0 / REGULAR',1010,62,15,muted)
        page.rect(54,95,1172,1,line)
        page.text('A CONSIDERED MONOSPACE',54,178,15,muted)
        page.text('Precision.',50,280,76)
        page.text('With character.',50,376,76,accent)
        page.text('For interfaces, ideas, and everything in between.',54,443,17,muted)
        page.rect(835,145,390,340,surface)
        for x in range(855,1210,30):page.rect(x,165,1,300,line)
        for y in range(165,470,30):page.rect(855,y,350,1,line)
        page.text('Aa',860,406,240,accent)
        page.text('ORIGINAL FORM STUDY / 650 U',858,467,11,muted)
        page.rect(54,537,1172,1,line)
        page.text('2,500 GLYPHS',54,587,20)
        page.text('FOUR FORMATS',397,587,20)
        page.text('SIL OFL 1.1',740,587,20)
        page.save('website-preview-'+theme)
        print('Rendered '+theme+' website specimen.')

if __name__=='__main__':render()
