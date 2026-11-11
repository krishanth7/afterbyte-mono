#!/usr/bin/env python3
"""Render the playful light/dark Afterbyte specimen from actual font outlines."""
from render_afterbyte import Page

def render():
    for theme, colors in {
        'light': ('#fff4df','#29213c','#65596e','#6841c8'),
        'dark': ('#211b2b','#fff2d7','#c7b9ca','#c5adff'),
    }.items():
        bg,ink,muted,accent=colors
        page=Page(1280,640,'Afterbyte Mono — Type with a wild side.',
            'Afterbyte Mono v5.0.0. A playful monospace with 2,500 glyphs and four font formats. Lettering rendered from the compiled font.',bg,ink,muted,accent)
        page.text('afterbyte / mono',50,62,23)
        page.text('V5.0.0 / REGULAR',1000,60,15,muted)
        page.rect(50,92,1180,1,ink)
        page.text('AFTERBYTE MONO / A TYPE PLAYGROUND',50,168,15,muted)
        page.text('TYPE WITH',46,278,82)
        page.rect(44,312,635,101,'#d8ef86')
        page.text('A WILD SIDE.',46,383,82,'#29213c')
        page.text('A technical monospace.',50,462,21,muted)
        page.text('A whole lot of personality.',50,495,21,muted)
        page.rect(780,135,450,375,'#f4b3cc')
        page.rect(804,183,180,191,'#ff8657')
        page.text('A',831,339,169,'#29213c')
        page.rect(1008,164,190,190,'#d8ef86')
        page.text('a',1034,315,169,'#29213c')
        page.rect(923,325,190,167,'#7654c5')
        page.text('g',950,440,158,'#fff4df')
        page.rect(0,550,1280,90,'#ff8657')
        page.text('2,500 GLYPHS / FOUR FORMATS / ONE VERY OPEN MIND.',50,603,27,'#29213c')
        page.save('website-preview-'+theme)
        print('Rendered '+theme+' website specimen.')

if __name__=='__main__':render()
