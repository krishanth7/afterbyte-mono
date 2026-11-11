#!/usr/bin/env python3
"""Actual-font SVG/PNG identity and proof sheets for Afterbyte Mono. OFL-1.1."""
import html
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
FONT=ROOT/'fonts/afterbyte-mono/AfterbyteMono-Regular.ttf'
tt=TTFont(FONT);glyphs=tt.getGlyphSet();cmap=tt.getBestCmap()


class Page:
    def __init__(self,width,height,title,description,bg,ink,muted,accent):
        self.ink,self.muted,self.accent=ink,muted,accent
        self.definitions={}
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                  '<title id="title">'+html.escape(title)+'</title>',
                  '<desc id="desc">'+html.escape(description)+'</desc>']
        self.image=Image.new('RGB',(width,height),bg);self.draw=ImageDraw.Draw(self.image)
        self.rect(0,0,width,height,bg)

    def rect(self,x,y,w,h,color):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
        self.draw.rectangle((x,y,x+w-1,y+h-1),fill=color)

    def text(self,text,x,y,size=32,color=None):
        color=color or self.ink
        scale=size/1000
        self.svg.append(f'<g aria-label="{html.escape(text,quote=True)}" fill="{color}" transform="translate({x} {y}) scale({scale} {-scale})">')
        for i,ch in enumerate(text):
            name=cmap.get(ord(ch),'.notdef')
            pen=SVGPathPen(glyphs);glyphs[name].draw(pen)
            path=pen.getCommands()
            if path:
                identifier='g_'+name
                self.definitions[identifier]=path
                self.svg.append(f'<use href="#{identifier}" transform="translate({i*650} 0)"/>')
        self.svg.append('</g>')
        face=ImageFont.truetype(str(FONT),size)
        self.draw.text((x,y),text,font=face,fill=color,anchor='ls')

    def frame(self,x,y,w,h):
        self.rect(x,y,w,1,self.muted);self.rect(x,y+h-1,w,1,self.muted)
        self.rect(x,y,1,h,self.muted);self.rect(x+w-1,y,1,h,self.muted)
        for px,py in [(x,y),(x+w-18,y),(x,y+h-2),(x+w-18,y+h-2)]:
            self.rect(px,py,18,2,self.accent)

    def save(self,name):
        out=ROOT/'assets/afterbyte-mono';out.mkdir(parents=True,exist_ok=True)
        definitions=['<defs>']+[f'<path id="{identifier}" d="{path}"/>' for identifier,path in sorted(self.definitions.items())]+['</defs>']
        (out/(name+'.svg')).write_text('\n'.join(self.svg+definitions+['</svg>'])+'\n')
        self.image.save(out/(name+'.png'))


def render():
    dark=('#0C1218','#E4EDF1','#7F939F','#63D9E9')
    c=Page(1600,960,'Afterbyte Mono — continuous-vector technical monospace',
           'Afterbyte Mono. Clarity with a distinct character. Regular 0.2.0 alpha. Original continuous-vector monospace with 196 Unicode characters, a dotted zero, a flat-top A, and rounded bowls. All visible lettering uses the actual compiled font.',*dark)
    c.rect(80,64,8,26,c.accent)
    c.text('AFTERBYTE / TYPE SYSTEM 03',112,88,32)
    c.text('REGULAR / ALPHA',1200,88,32,c.muted)
    c.rect(80,138,1440,1,'#26343E')
    c.text('Afterbyte Mono',70,360,144)
    c.text('Clarity with a distinct character.',80,440,40,c.muted)
    c.frame(80,532,960,300)
    c.text('01 / INTELLIGENT INTERFACES',112,584,24,c.accent)
    c.text('agent.init({',112,644,32)
    c.text("  mode: 'assist',",112,688,32)
    c.text('  signal: 0.98',112,732,32)
    c.text('});',112,776,32)
    c.frame(1080,532,440,300)
    c.text('02 / DESIGN METRICS',1112,584,24,c.accent)
    c.text('650U',1112,678,72)
    c.text('FIXED ADVANCE',1112,718,24,c.muted)
    c.text('196 CHARACTERS',1112,790,32)
    c.text('MONOSPACE / VECTOR / OPEN SOURCE',80,906,32,c.muted)
    c.save('hero')
    for mode,colors in [('dark',dark),('light',('#F6F8FA','#14232E','#536875','#006577'))]:
        s=Page(1600,1750,'Afterbyte Mono — '+mode+' type specimen',
               'Actual-font proof: uppercase, lowercase, numerals, punctuation, selected accented Latin letters, technical symbols, size proofing, and connected box drawing. Text equivalents are in the README and proofing file.',*colors)
        s.text('AFTERBYTE MONO / REGULAR / 0.3.0 ALPHA',80,80,32)
        s.rect(80,116,1440,1,s.muted)
        rows=[('01 / THE ALPHABET','ABCDEFGHIJKLMNOPQRSTUVWXYZ',252,64),
              ('','abcdefghijklmnopqrstuvwxyz',364,64),
              ('02 / NUMERALS & CHARACTER DISTINCTION','0123456789  0O  1Il  a e s',556,64),
              ('03 / PUNCTUATION','!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',740,48),
              ('04 / EXTENDED LABELS','ÄÖÜ äöü ß  ÀÉÎÑ  æ ø  € £ ¥ ₹',924,44),
              ('05 / TECHNICAL SIGNALS','← → ↑ ↓ ↔ ↕  ✓ ■ □  ░▒▓█',1100,48)]
        for label,text,baseline,size in rows:
            if label:s.text(label,80,baseline-92,24,s.muted)
            s.text(text,80,baseline,size)
        s.rect(80,1170,1440,1,s.muted)
        s.text('06 / FIXED ADVANCE / ACTUAL FONT SIZES',80,1230,24,s.muted)
        s.text('16 PX',80,1290,16,s.accent)
        s.text('The quick brown fox jumps over the lazy dog. 0123456789',250,1290,16)
        s.text('28 PX',80,1366,16,s.accent)
        s.text('const status = { ready: true, signal: 0.98 };',250,1366,28)
        s.text('44 PX',80,1460,16,s.accent)
        s.text('A quieter kind of future.',250,1460,44)
        s.text('07 / MONOSPACED UI / 32 PX / LINE HEIGHT 1.04',80,1540,24,s.muted)
        for i,line in enumerate(['┌─────────┬─────────┐','│ SYSTEM  │ ONLINE  │','└─────────┴─────────┘']):
            s.text(line,80,1600+i*33.28,32)
        s.text('All specimens use original Afterbyte Mono outlines.',80,1710,24,s.muted)
        s.save('specimen-'+mode)
    print('Rendered Afterbyte identity and light/dark specimens from the actual font.')


if __name__=='__main__':render()
