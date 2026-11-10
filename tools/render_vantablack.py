#!/usr/bin/env python3
"""Render README specimens from the compiled TTF; no replacement display font."""
import html
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
FONT=ROOT/'fonts/vantablack-gothic/VantablackGothic-Regular.ttf'
font=TTFont(FONT)
glyphs=font.getGlyphSet()
cmap=font.getBestCmap()
metrics=font['hmtx'].metrics


class Canvas:
    def __init__(self,width,height,title,description,bg):
        self.width,self.height=width,height
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                  f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>']
        self.image=Image.new('RGB',(width,height),bg)
        self.draw=ImageDraw.Draw(self.image)
        self.rect(0,0,width,height,bg)

    def rect(self,x,y,w,h,color):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
        self.draw.rectangle((x,y,x+w,y+h),fill=color)

    def label(self,text,x,y,size=18,color='#7E8993'):
        self.svg.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}" letter-spacing="2">{html.escape(text)}</text>')
        system=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',size)
        self.draw.text((x,y),text,font=system,fill=color,anchor='ls')

    def text(self,text,x,baseline,size,color):
        scale=size/1000
        self.svg.append(f'<g aria-label="{html.escape(text,quote=True)}" fill="{color}" transform="translate({x} {baseline}) scale({scale} {-scale})">')
        offset=0
        for ch in text:
            name=cmap[ord(ch)]
            pen=SVGPathPen(glyphs)
            glyphs[name].draw(pen)
            path=pen.getCommands()
            if path:
                self.svg.append(f'<path transform="translate({offset} 0)" d="{path}"/>')
            offset+=metrics[name][0]
        self.svg.append('</g>')
        face=ImageFont.truetype(str(FONT),size)
        self.draw.text((x,baseline),text,font=face,fill=color,anchor='ls',features=['-kern'])

    def save(self,name):
        out=ROOT/'assets/vantablack-gothic';out.mkdir(parents=True,exist_ok=True)
        (out/(name+'.svg')).write_text('\n'.join(self.svg+['</svg>'])+'\n')
        # PNG proof is a build-time review artifact; the README uses sharp SVG paths.
        self.image.save(out/(name+'.png'))


def render():
    dark='#090C0F'; ink='#E6E9EA'; acid='#D9FF54'
    c=Canvas(1600,900,'Vantablack Gothic — actual font specimen',
             'VANTABLACK GOTHIC in the original alpha font. Proportional, angular, condensed display type. Regular 0.1.0 alpha; 95 printable ASCII characters; 1000 UPEM.',dark)
    for x in range(64,1600,80): c.rect(x,0,1,900,'#151B20')
    for y in range(70,900,80): c.rect(0,y,1600,1,'#151B20')
    c.rect(64,60,10,26,acid)
    c.label('AFTERBYTE / TYPE LAB',92,81,19,ink)
    c.label('ORIGINAL OUTLINES / 0.1.0 ALPHA',1010,81,18,acid)
    c.text('VANTABLACK',60,350,300,ink)
    c.text('GOTHIC',60,638,300,ink)
    c.rect(1050,425,470,208,'#151C21')
    c.text('REGULAR',1080,493,62,acid)
    c.label('1000 UPEM / 780 CAP',1080,541,17,ink)
    c.label('PROPORTIONAL / ASCII',1080,579,17,ink)
    c.label('TTF + WOFF2',1080,610,17,ink)
    c.rect(64,710,1472,2,acid)
    c.text('MONOLITHIC FORM. DIGITAL SEVERITY.',64,790,68,ink)
    c.label('DESIGNED BY KRISHANTH',64,851,17)
    c.label('RENDERED FROM THE COMPILED FONT',1090,851,15)
    c.save('hero')
    for mode,bg,fg,muted in [('dark',dark,ink,'#86959F'),('light','#F0F0E8','#10171B','#52626B')]:
        s=Canvas(1600,1420,'Vantablack Gothic — '+mode+' glyph proof',
                 'Actual font rendering: uppercase A to Z, lowercase a to z, numerals 0 to 9, all ASCII punctuation, and ambiguity checks. Text equivalents appear in README and proofing.txt.',bg)
        s.label('VANTABLACK GOTHIC / REGULAR / 0.1.0 ALPHA',64,60,18,muted)
        rows=[('UPPERCASE / 780 CAP','ABCDEFGHIJKLM',210),
              ('','NOPQRSTUVWXYZ',370),
              ('LOWERCASE / 580 X-HEIGHT','abcdefghijklm',570),
              ('','nopqrstuvwxyz',740),
              ('PROPORTIONAL LINING FIGURES','0123456789',940)]
        for label,text,baseline in rows:
            if label: s.label(label,64,baseline-135,17,muted)
            s.text(text,64,baseline,130,fg)
        s.label('PUNCTUATION / ALL 32 ASCII MARKS',64,1020,17,muted)
        s.text('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',64,1110,75,fg)
        s.rect(64,1180,1472,1,muted)
        s.label('AMBIGUITY CHECK / OPEN COUNTERS / DETACHED CROSSBARS',64,1220,17,muted)
        s.text('0 O o  1 I l i |  rn m  cl d  a e  H E F A',64,1335,80,fg)
        s.save('glyphs-'+mode)
    print('Rendered three SVG specimens and PNG review proofs from the actual TTF.')


if __name__=='__main__': render()
