#!/usr/bin/env python3
"""Validate real Afterbyte Mono binaries against their original pixel matrices."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

import uharfbuzz as hb
from PIL import ImageFont
from fontTools.ttLib import TTFont
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union

ROOT=Path(__file__).resolve().parents[1]


def check(value,message):
    if not value:raise ValueError(message)


def glyph_shape(glyph,table):
    coords,ends,flags=glyph.getCoordinates(table)
    check(all(int(flag)&1 for flag in flags),'Unexpected curve point')
    shells=[];holes=[];start=0
    for end in ends:
        pts=[tuple(pt) for pt in coords[start:end+1]];start=end+1
        check(len(pts)>=4,'Degenerate pixel contour')
        area=0
        for a,b in zip(pts,pts[1:]+pts[:1]):
            dx,dy=b[0]-a[0],b[1]-a[1]
            check((not dx) != (not dy),'Non-axis or zero-length edge')
            check(all(v%100==0 for v in a),'Outline escaped the 100-unit pixel grid')
            area+=a[0]*b[1]-a[1]*b[0]
        check(area!=0,'Zero-area contour')
        polygon=Polygon(pts)
        check(polygon.is_valid,'Self-intersecting contour')
        (shells if area<0 else holes).append(polygon)
    shape=unary_union(shells)
    for hole in holes:shape=shape.difference(hole)
    check(shape.is_valid,'Invalid filled glyph')
    return shape


def validate():
    source=json.loads((ROOT/'sources/afterbyte-mono/pixels.json').read_text())
    directory=ROOT/'fonts/afterbyte-mono'
    path=directory/'AfterbyteMono-Regular.ttf'
    font=TTFont(path,checkChecksums=2)
    web=TTFont(directory/'AfterbyteMono-Regular.woff2',checkChecksums=2)
    cmap=font.getBestCmap();expected={r['unicode'] for r in source['glyphs']}
    check(len(source['glyphs'])==len(expected)==196,'Coverage count or duplicate Unicode mapping')
    check(set(cmap)==expected,'Source/cmap coverage mismatch')
    check(set(range(32,127)).issubset(cmap),'Incomplete printable ASCII')
    check(font.getGlyphOrder()[0]=='.notdef','Missing .notdef')
    check(len(font.getGlyphOrder())==197,'Unexpected glyph count')
    check(font['head'].unitsPerEm==1600,'Wrong UPEM')
    check(font['post'].isFixedPitch==1,'Fixed-pitch flag must be set')
    check(all(width==900 for width,_ in font['hmtx'].metrics.values()),'Not truly monospaced')
    check(font['OS/2'].panose.bProportion==9,'PANOSE must identify monospace')
    check((font['hhea'].ascent,font['hhea'].descent,font['hhea'].lineGap)==(1300,-300,0),'Line metrics mismatch')
    check((font['OS/2'].sCapHeight,font['OS/2'].sxHeight)==(1000,700),'Cap/x-height mismatch')
    check(font['name'].getDebugName(1)=='Afterbyte Mono','Wrong family name')
    check(font['name'].getDebugName(6)=='AfterbyteMono-Regular','Wrong PostScript name')
    check('MIT License' in font['name'].getDebugName(13),'Missing license metadata')
    check(font['OS/2'].fsType==0,'Unexpected embedding restriction')
    check(cmap==web.getBestCmap() and font['hmtx'].metrics==web['hmtx'].metrics,'WOFF2 mapping/advance mismatch')
    shapes={}
    for record in source['glyphs']:
        code=record['unicode'];name=cmap[code];glyph=font['glyf'][name]
        check(not glyph.isComposite(),f'{code}: unexpected composite')
        shape=glyph_shape(glyph,font['glyf']);shapes[code]=shape
        filled=sum(row.count('#') for row in record['rows'])
        check(shape.area==filled*10000,f'U+{code:04X}: incorrect pixel area')
        if not filled:
            check(code in (32,160) and shape.is_empty,'Unexpected blank glyph')
        else:
            x0,y0,x1,y1=shape.bounds
            check(0<=x0<x1<=900 and -300<=y0<y1<=1300,f'U+{code:04X}: clipping/advance bounds')
            check(font['hmtx'].metrics[name][1]==x0,'Ink bearing mismatch')
            for y,row in enumerate(record['rows']):
                for x,cell in enumerate(row):
                    point=Point(record['left']+x*100+50,record['top']-y*100-50)
                    check(shape.contains(point)==(cell=='#'),f'U+{code:04X}: occupied-pixel mismatch at {x,y}')
        a=font['glyf'][name].getCoordinates(font['glyf'])
        b=web['glyf'][name].getCoordinates(web['glyf'])
        check(list(a[0])==list(b[0]) and list(a[1])==list(b[1]),f'U+{code:04X}: WOFF2 outline mismatch')
    check(not glyph_shape(font['glyf']['.notdef'],font['glyf']).is_empty,'Empty missing-glyph symbol')
    for a,b in [('0','O'),('1','I'),('I','l'),('i','l'),('a','e'),('S','5')]:
        check(not shapes[ord(a)].equals(shapes[ord(b)]),f'Identical ambiguity pair: {a}/{b}')
    check(shapes[ord('─')].bounds==(0,400,900,500),'Horizontal box line cannot join cells')
    check(shapes[ord('│')].bounds==(400,-300,500,1300),'Vertical box line cannot join rows')
    buffer=hb.Buffer();buffer.add_str(''.join(map(chr,sorted(expected))));buffer.guess_segment_properties()
    hb.shape(hb.Font(hb.Face(path.read_bytes())),buffer)
    check(len(buffer.glyph_infos)==196 and all(g.codepoint for g in buffer.glyph_infos),'HarfBuzz missing glyph')
    check(all(pos.x_advance==900 for pos in buffer.glyph_positions),'Shaped advances are not fixed')
    for size in (16,32,48,64):
        face=ImageFont.truetype(str(path),size)
        for code in expected:
            mask=face.getmask(chr(code))
            check(not (set(bytes(mask))-{0,255}),f'U+{code:04X}: non-crisp native-grid raster at {size}px')
            if code not in (32,160):check(mask.getbbox() is not None,'Empty non-space raster')
            check(face.getlength(chr(code))==size*9/16,'FreeType advance mismatch')
    for line in (directory/'SHA256SUMS').read_text().splitlines():
        expected_hash,filename=line.split()
        check(hashlib.sha256((directory/filename).read_bytes()).hexdigest()==expected_hash,'Checksum mismatch')
    links=0
    for document in ROOT.rglob('*.md'):
        if '.git' in document.parts:continue
        text=document.read_text()
        destinations=re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text)
        destinations+=re.findall(r'(?:src|srcset)="([^"]+)"',text)
        for destination in destinations:
            destination=destination.strip().split()[0].strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',destination) or destination.startswith('#'):continue
            target=(document.parent/unquote(destination.split('#',1)[0])).resolve()
            check(target.is_relative_to(ROOT) and target.exists(),f'{document.name}: missing link {destination}')
            links+=1
    print(f'PASS: 197 glyphs / 196 Unicode mappings; true monospace; pixel occupancy and topology; metrics; license; TTF/WOFF2 equivalence; shaping; crisp 16/32/48/64 px rasterization; checksums; {links} local links/images.')
    print('Scope: local FreeType/HarfBuzz checks. No independent certification or all-platform rendering claim.')


if __name__=='__main__':validate()
