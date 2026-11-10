#!/usr/bin/env python3
"""Compile original Afterbyte Mono pixel matrices into TTF and WOFF2. MIT."""
import hashlib
import json
from pathlib import Path

from shapely.geometry import box, Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable
from fontTools.ttLib.tables.O_S_2f_2 import Panose

ROOT=Path(__file__).resolve().parents[1]


def shape_for(record,pixel=100):
    return unary_union([box(record['left']+x*pixel,record['top']-(y+1)*pixel,
                            record['left']+(x+1)*pixel,record['top']-y*pixel)
                        for y,row in enumerate(record['rows']) for x,cell in enumerate(row) if cell=='#'])


def contours_for(shape):
    if shape.is_empty:return []
    parts=[shape] if isinstance(shape,Polygon) else list(shape.geoms)
    contours=[]
    for part in sorted(parts,key=lambda p:p.bounds):
        part=orient(part,sign=-1)
        for ring in [part.exterior,*part.interiors]:
            pts=[(int(x),int(y)) for x,y in list(ring.coords)[:-1]]
            # Collapse redundant collinear vertices without changing the silhouette.
            changed=True
            while changed and len(pts)>3:
                changed=False
                for i,b in enumerate(pts):
                    a,c=pts[i-1],pts[(i+1)%len(pts)]
                    if (b[0]-a[0])*(c[1]-b[1])==(b[1]-a[1])*(c[0]-b[0]):
                        pts.pop(i);changed=True;break
            contours.append(pts)
    return contours


def build():
    source=json.loads((ROOT/'sources/afterbyte-mono/pixels.json').read_text())
    records=[{'character':None,'unicode':None,'left':100,'top':1000,
              'rows':['#######','#.....#','#.....#','#.....#','#..#..#',
                      '#..#..#','#.....#','#.....#','#.....#','#######']},*source['glyphs']]
    glyphs={};metrics={};mapping={};order=[]
    for record in records:
        code=record['unicode']
        name='.notdef' if code is None else 'space' if code==32 else f'uni{code:04X}'
        shape=shape_for(record)
        pen=TTGlyphPen(None)
        for points in contours_for(shape):
            pen.moveTo(points[0])
            for point in points[1:]:pen.lineTo(point)
            pen.closePath()
        glyphs[name]=pen.glyph()
        metrics[name]=(source['advance'],int(shape.bounds[0]) if not shape.is_empty else 0)
        if code is not None:mapping[code]=name
        order.append(name)
    fb=FontBuilder(source['units_per_em'],isTTF=True)
    fb.setupGlyphOrder(order);fb.setupCharacterMap(mapping);fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=1300,descent=-300,lineGap=0)
    license_text=(ROOT/'LICENSE').read_text()
    fb.setupNameTable({'familyName':'Afterbyte Mono','styleName':'Regular',
                      'typographicFamily':'Afterbyte Mono','typographicSubfamily':'Regular',
                      'fullName':'Afterbyte Mono Regular','psName':'AfterbyteMono-Regular',
                      'uniqueFontIdentifier':'Krishanth:AfterbyteMono-Regular:0.2.0-alpha',
                      'version':'Version 0.200; alpha 0.2.0','designer':'Krishanth',
                      'copyright':'Copyright (c) 2026 Krishanth',
                      'description':'Original pixel monospace for code, technical interfaces, and futuristic HUDs. Native grid: 16 px.',
                      'licenseDescription':license_text,
                      'licenseInfoURL':'https://github.com/krishanth7/afterbyte-mono/blob/main/LICENSE',
                      'vendorURL':'https://github.com/krishanth7/afterbyte-mono'})
    panose=Panose();panose.bFamilyType=2;panose.bProportion=9
    fb.setupOS2(version=4,usWeightClass=400,usWidthClass=5,fsType=0,
                fsSelection=0xC0,sTypoAscender=1300,sTypoDescender=-300,sTypoLineGap=0,
                usWinAscent=1300,usWinDescent=300,sCapHeight=1000,sxHeight=700,
                panose=panose,achVendID='KRIS')
    fb.setupPost(isFixedPitch=1,underlinePosition=-200,underlineThickness=100)
    fb.font['gasp']=newTable('gasp');fb.font['gasp'].gaspRange={65535:2}
    fb.font['head'].created=3877200000;fb.font['head'].modified=3877200000
    fb.font['head'].fontRevision=0.2
    out=ROOT/'fonts/afterbyte-mono';out.mkdir(parents=True,exist_ok=True)
    fb.save(out/'AfterbyteMono-Regular.ttf')
    fb.font.flavor='woff2';fb.save(out/'AfterbyteMono-Regular.woff2')
    (out/'LICENSE.txt').write_text(license_text)
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('AfterbyteMono-Regular.*'))}
    (out/'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name,value in manifest.items()))
    (out/'coverage.txt').write_text('Afterbyte Mono Regular / 0.2.0 alpha\n'+
        f'{len(mapping)} Unicode mappings; all spacing glyphs advance 900 units.\n\n'+
        '\n'.join(f'U+{code:04X} {chr(code)}' for code in sorted(mapping))+'\n')
    print(f'Built Afterbyte Mono: {len(order)} glyphs / {len(mapping)} Unicode mappings; fixed 900-unit advance; TTF + WOFF2.')


if __name__=='__main__':build()
