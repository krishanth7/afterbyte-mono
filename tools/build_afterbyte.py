#!/usr/bin/env python3
"""Compile original Afterbyte Mono continuous-vector sources. MIT."""
import hashlib
import json
import copy
from pathlib import Path

from shapely import set_precision
from shapely.geometry import LineString,Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.ttLib import newTable
from fontTools.ttLib.tables.O_S_2f_2 import Panose

ROOT=Path(__file__).resolve().parents[1]


def sample_path(path):
    points=[];start=None
    for command in path:
        op=command[0]
        if op=='M':
            points.append(tuple(command[1:3]));start=points[-1]
        elif op=='L':points.append(tuple(command[1:3]))
        elif op=='C':
            p0=points[-1];p1=command[1:3];p2=command[3:5];p3=command[5:7]
            for i in range(1,25):
                t=i/24;u=1-t
                points.append(tuple(u*u*u*p0[k]+3*u*u*t*p1[k]+3*u*t*t*p2[k]+t*t*t*p3[k] for k in (0,1)))
        elif op=='Z':
            if points[-1]!=start:points.append(start)
        else:raise ValueError('Unsupported source command '+op)
    return points


def shape_for(record):
    shapes=[LineString(sample_path(path)).buffer(record['stroke']/2,quad_segs=8,cap_style='flat',join_style='round')
            for path in record['paths']]
    shapes.extend(Polygon(points) for points in record['solids'])
    return set_precision(unary_union(shapes),1)


def contours_for(shape):
    if shape.is_empty:return []
    parts=[shape] if isinstance(shape,Polygon) else list(shape.geoms)
    contours=[]
    for part in sorted(parts,key=lambda p:p.bounds):
        part=orient(part,sign=-1)
        for ring in [part.exterior,*part.interiors]:
            pts=[(int(x),int(y)) for x,y in list(ring.coords)[:-1]]
            clean=[]
            for point in pts:
                if not clean or point!=clean[-1]:clean.append(point)
            changed=True
            while changed and len(clean)>3:
                changed=False
                for i,b in enumerate(clean):
                    a,c=clean[i-1],clean[(i+1)%len(clean)]
                    if (b[0]-a[0])*(c[1]-b[1])==(b[1]-a[1])*(c[0]-b[0]):
                        clean.pop(i);changed=True;break
            contours.append(clean)
    return contours


def build():
    source=json.loads((ROOT/'sources/afterbyte-mono/vectors.json').read_text())
    missing={'character':None,'unicode':None,'stroke':64,'solids':[],
             'paths':[[['M',110,32],['L',110,668],['L',540,668],['L',540,32],['Z']],
                      [['M',230,220],['L',420,480]],[['M',230,480],['L',420,220]]]}
    records=[missing,*source['glyphs']]
    glyphs={};metrics={};mapping={};order=[]
    for record in records:
        code=record['unicode']
        name='.notdef' if code is None else 'space' if code==32 else f'uni{code:04X}'
        shape=shape_for(record)
        if not shape.is_empty:
            if not shape.is_valid:raise ValueError(f'Invalid outline {code}')
            x0,y0,x1,y1=shape.bounds
            if not(0<=x0<=x1<=650 and -220<=y0<=y1<=822):
                raise ValueError(f'Out of bounds {record["character"]!r}: {shape.bounds}')
        pen=TTGlyphPen(None)
        for points in contours_for(shape):
            pen.moveTo(points[0])
            for point in points[1:]:pen.lineTo(point)
            pen.closePath()
        glyphs[name]=pen.glyph()
        metrics[name]=(650,int(shape.bounds[0]) if not shape.is_empty else 0)
        if code is not None:mapping[code]=name
        order.append(name)
    fb=FontBuilder(1000,isTTF=True)
    fb.setupGlyphOrder(order);fb.setupCharacterMap(mapping);fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=820,descent=-220,lineGap=0)
    license_text=(ROOT/'LICENSE').read_text()
    fb.setupNameTable({'familyName':'Afterbyte Mono','styleName':'Regular',
                      'typographicFamily':'Afterbyte Mono','typographicSubfamily':'Regular',
                      'fullName':'Afterbyte Mono Regular','psName':'AfterbyteMono-Regular',
                      'uniqueFontIdentifier':'Krishanth:AfterbyteMono-Regular:0.3.0-alpha',
                      'version':'Version 0.300; alpha 0.3.0','designer':'Krishanth',
                      'copyright':'Copyright (c) 2026 Krishanth',
                      'description':'Original continuous-vector technical monospace. Dotted zero, flat-top A, rounded bowls, and single-storey a/g.',
                      'licenseDescription':license_text,
                      'licenseInfoURL':'https://github.com/krishanth7/afterbyte-mono/blob/main/LICENSE',
                      'vendorURL':'https://github.com/krishanth7/afterbyte-mono'})
    panose=Panose();panose.bFamilyType=2;panose.bProportion=9
    fb.setupOS2(version=4,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0xC0,
                sTypoAscender=820,sTypoDescender=-220,sTypoLineGap=0,
                usWinAscent=822,usWinDescent=220,sCapHeight=700,sxHeight=500,
                panose=panose,achVendID='KRIS')
    fb.setupPost(isFixedPitch=1,underlinePosition=-160,underlineThickness=45)
    fb.font['gasp']=newTable('gasp');fb.font['gasp'].gaspRange={65535:2}
    fb.font['head'].created=3877286400;fb.font['head'].modified=3877286400;fb.font['head'].fontRevision=0.3
    out=ROOT/'fonts/afterbyte-mono';out.mkdir(parents=True,exist_ok=True)
    fb.save(out/'AfterbyteMono-Regular.ttf')
    # CFF is a genuine OpenType/PostScript build of the same outlines.
    # Reverse the TrueType contour convention for the CFF charstrings.
    otf=FontBuilder(1000,isTTF=False)
    otf.setupGlyphOrder(order);otf.setupCharacterMap(mapping)
    charstrings={}
    glyph_set=fb.font.getGlyphSet()
    for name in order:
        pen=T2CharStringPen(650,None)
        glyph_set[name].draw(ReverseContourPen(pen))
        charstrings[name]=pen.getCharString()
    otf.setupCFF('AfterbyteMono-Regular',{
        'FullName':'Afterbyte Mono Regular','FamilyName':'Afterbyte Mono',
        'Weight':'Regular','version':'0.300','isFixedPitch':True,
        'Notice':'Copyright (c) 2026 Krishanth. MIT License; see font name table and LICENSE.txt.',
        'UnderlinePosition':-160,'UnderlineThickness':45,
    },charstrings,{})
    for tag in ('head','hhea','hmtx','name','OS/2'):
        otf.font[tag]=copy.deepcopy(fb.font[tag])
    otf.setupPost(isFixedPitch=1,underlinePosition=-160,underlineThickness=45)
    otf.save(out/'AfterbyteMono-Regular.otf')
    fb.font.flavor='woff';fb.save(out/'AfterbyteMono-Regular.woff')
    fb.font.flavor='woff2';fb.save(out/'AfterbyteMono-Regular.woff2')
    (out/'LICENSE.txt').write_text(license_text)
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('AfterbyteMono-Regular.*'))}
    (out/'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name,value in manifest.items()))
    (out/'coverage.txt').write_text('Afterbyte Mono Regular / 0.3.0 alpha\n'+
        f'{len(mapping)} Unicode mappings; all spacing glyphs advance 650 units.\n\n'+
        '\n'.join(f'U+{code:04X} {chr(code)}' for code in sorted(mapping))+'\n')
    print(f'Built {len(order)} continuous-vector glyphs / {len(mapping)} mappings; OTF (CFF), TTF, WOFF, WOFF2.')


if __name__=='__main__':build()
