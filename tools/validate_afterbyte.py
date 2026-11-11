#!/usr/bin/env python3
"""Validate Afterbyte Mono 0.3 continuous-vector source and binary contracts."""
import hashlib
import json
import re
import io
from pathlib import Path
from urllib.parse import unquote

import uharfbuzz as hb
from PIL import ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
from build_afterbyte import shape_for

ROOT=Path(__file__).resolve().parents[1]


def check(value,message):
    if not value:raise ValueError(message)


def glyph_shape(glyph,table):
    coords,ends,flags=glyph.getCoordinates(table)
    check(all(int(flag)&1 for flag in flags),'Unexpected curve point in flattened outline')
    parts=[];shell=None;holes=[];start=0
    for end in ends:
        pts=[tuple(pt) for pt in coords[start:end+1]];start=end+1
        check(len(pts)>=3,'Degenerate contour')
        area=0
        for a,b in zip(pts,pts[1:]+pts[:1]):
            check(a!=b,'Zero-length edge')
            check(all(type(v) is int for v in a),'Non-integer compiled coordinate')
            area+=a[0]*b[1]-a[1]*b[0]
        check(area!=0,'Zero-area contour')
        polygon=Polygon(pts);check(polygon.is_valid,'Self-intersecting contour')
        if area<0:
            if shell is not None:parts.append(Polygon(shell,holes))
            shell,holes=pts,[]
        else:
            check(shell is not None,'Counter without an outer contour')
            holes.append(pts)
    if shell is not None:parts.append(Polygon(shell,holes))
    check(all(p.is_valid for p in parts),'Invalid source component')
    shape=unary_union(parts)
    check(shape.is_valid,'Invalid filled glyph')
    return shape


def cff_shape(glyph):
    """Decode actual CFF charstrings; CFF uses the reversed contour convention."""
    pen=RecordingPen();glyph.draw(pen)
    contours=[];points=[]
    for operator,args in pen.value:
        if operator=='moveTo':
            check(not points,'CFF contour was not closed')
            points=[args[0]]
        elif operator=='lineTo':points.append(args[0])
        elif operator=='closePath':
            contours.append(points);points=[]
        else:raise ValueError('Unexpected CFF outline operator '+operator)
    check(not points,'Unclosed CFF contour')
    parts=[];shell=None;holes=[]
    for points in contours:
        area=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(points,points[1:]+points[:1]))
        check(area!=0 and Polygon(points).is_valid,'Invalid CFF contour')
        if area>0:
            if shell is not None:parts.append(Polygon(shell,holes))
            shell,holes=points,[]
        else:
            check(shell is not None,'CFF counter without shell')
            holes.append(points)
    if shell is not None:parts.append(Polygon(shell,holes))
    check(all(part.is_valid for part in parts),'Invalid CFF topology')
    return unary_union(parts)


def validate():
    source=json.loads((ROOT/'sources/afterbyte-mono/vectors.json').read_text())
    directory=ROOT/'fonts/afterbyte-mono';path=directory/'AfterbyteMono-Regular.ttf'
    license_text=(ROOT/'OFL.txt').read_text()
    check('SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007' in license_text,'Wrong font license')
    check((ROOT/'LICENSE').read_text()==license_text==(directory/'LICENSE.txt').read_text(),'License copies differ')
    check(source['license']=='OFL-1.1','Wrong source license')
    font=TTFont(path,checkChecksums=2);web=TTFont(directory/'AfterbyteMono-Regular.woff2',checkChecksums=2)
    cmap=font.getBestCmap();expected={r['unicode'] for r in source['glyphs']}
    check(len(source['glyphs'])==len(expected)==196,'Coverage mismatch')
    check(set(cmap)==expected and set(range(32,127)).issubset(cmap),'Incomplete mapping')
    check(font.getGlyphOrder()[0]=='.notdef' and len(font.getGlyphOrder())==197,'Glyph order/count')
    check(source['construction']=='original continuous vector centerlines','Wrong source direction')
    check(font['head'].unitsPerEm==1000,'Wrong UPEM')
    check(font['post'].isFixedPitch==1 and font['OS/2'].panose.bProportion==9,'Wrong mono flags')
    check(all(width==650 for width,_ in font['hmtx'].metrics.values()),'Not monospaced')
    check((font['hhea'].ascent,font['hhea'].descent,font['hhea'].lineGap)==(820,-220,0),'Line metrics')
    check((font['OS/2'].sCapHeight,font['OS/2'].sxHeight)==(700,500),'Cap/x-height')
    check(font['OS/2'].usWinAscent==822 and font['OS/2'].usWinDescent==220,'Clipping metrics')
    check(font['name'].getDebugName(1)=='Afterbyte Mono','Family')
    check(font['name'].getDebugName(6)=='AfterbyteMono-Regular','PostScript name')
    check('0.300' in font['name'].getDebugName(5),'Version')
    check(font['name'].getDebugName(13)==license_text and font['OS/2'].fsType==0,'License/embedding')
    check(not {'EBDT','CBDT','sbix','fvar'}&set(font.keys()),'Unexpected bitmap/variation table')
    check(cmap==web.getBestCmap() and font['hmtx'].metrics==web['hmtx'].metrics,'WOFF2 mappings/metrics')
    shapes={}
    for record in source['glyphs']:
        code=record['unicode'];name=cmap[code];glyph=font['glyf'][name]
        check(not glyph.isComposite(),'Unexpected composite')
        shape=glyph_shape(glyph,font['glyf']);shapes[code]=shape
        expected_shape=shape_for(record)
        check(shape.symmetric_difference(expected_shape).area<0.01,f'U+{code:04X}: source/binary mismatch')
        if code in (32,160):check(shape.is_empty,'Space must be blank')
        else:
            check(not shape.is_empty,'Empty non-space')
            x0,y0,x1,y1=shape.bounds
            check(0<=x0<x1<=650 and -220<=y0<y1<=822,f'U+{code:04X}: clipped bounds')
            check(font['hmtx'].metrics[name][1]==x0,'Ink bearing')
        a=font['glyf'][name].getCoordinates(font['glyf'])
        b=web['glyf'][name].getCoordinates(web['glyf'])
        check(list(a[0])==list(b[0]) and list(a[1])==list(b[1]),'WOFF2 outline mismatch')
    check(not glyph_shape(font['glyf']['.notdef'],font['glyf']).is_empty,'Empty .notdef')
    for a,b in [('0','O'),('1','I'),('I','l'),('a','e'),('S','5'),('C','G')]:
        check(not shapes[ord(a)].equals(shapes[ord(b)]),'Identical ambiguity pair')
    check(shapes[ord('0')].contains(Point(325,350)),'Zero must contain its identifying dot')
    check(not shapes[ord('O')].contains(Point(325,350)),'O must have an open counter')
    check(shapes[ord('A')].contains(Point(325,690)),'A must have a flat top')
    for ch in 'ag':
        shape=shapes[ord(ch)]
        count=len(shape.interiors) if isinstance(shape,Polygon) else sum(len(p.interiors) for p in shape.geoms)
        check(count==1,f'{ch}: single-storey counter structure')
    h=shapes[ord('H')]
    check(abs(h.intersection(LineString([(-10,175),(660,175)])).length-128)<0.01,'H stems must be 64 units')
    check(shapes[ord('─')].bounds==(0,318,650,382),'Box horizontal boundaries')
    check(shapes[ord('│')].bounds==(293,-220,357,820),'Box vertical boundaries')
    buffer=hb.Buffer();buffer.add_str(''.join(map(chr,sorted(expected))));buffer.guess_segment_properties()
    hb.shape(hb.Font(hb.Face(path.read_bytes())),buffer)
    check(len(buffer.glyph_infos)==196 and all(g.codepoint for g in buffer.glyph_infos),'Shaping missing glyph')
    check(all(pos.x_advance==650 for pos in buffer.glyph_positions),'Shaped advance')
    for size in (12,16,24,32,48,96):
        face=ImageFont.truetype(str(path),size)
        for code in expected:
            if code not in (32,160):check(face.getmask(chr(code)).getbbox() is not None,'Empty raster')
            check(abs(face.getlength(chr(code))-size*.65)<.02,'FreeType advance')
    # A real CFF OTF, WOFF container, and WOFF2 container must all match the TTF.
    signatures={'otf':b'OTTO','woff':b'wOFF','woff2':b'wOF2','ttf':b'\x00\x01\x00\x00'}
    extra={extension:TTFont(directory/('AfterbyteMono-Regular.'+extension),checkChecksums=2)
           for extension in ('otf','woff','woff2')}
    check('CFF ' in extra['otf'] and 'glyf' not in extra['otf'],'OTF must contain real CFF outlines')
    for extension,signature in signatures.items():
        check((directory/('AfterbyteMono-Regular.'+extension)).read_bytes()[:4]==signature,'Invalid format signature '+extension)
    for extension,variant in extra.items():
        check(variant.getBestCmap()==cmap,'Cmap mismatch '+extension)
        check(variant.getGlyphOrder()==font.getGlyphOrder(),'Glyph order mismatch '+extension)
        check(variant['hmtx'].metrics==font['hmtx'].metrics,'Metric mismatch '+extension)
        check(variant['head'].unitsPerEm==1000 and variant['post'].isFixedPitch==1,'Mono metadata mismatch '+extension)
        check(variant['name'].getDebugName(1)==font['name'].getDebugName(1),'Family mismatch '+extension)
        check(variant['name'].getDebugName(13)==license_text,'Missing or incomplete license '+extension)
        check(variant['name'].getDebugName(14)=='https://openfontlicense.org','Wrong license URL '+extension)
        if extension=='otf':
            glyphs=variant.getGlyphSet()
            for code,name in cmap.items():
                check(cff_shape(glyphs[name]).symmetric_difference(shapes[code]).area<.01,
                      f'U+{code:04X}: CFF/TrueType geometry mismatch')
            check(not cff_shape(glyphs['.notdef']).is_empty,'Empty CFF missing-glyph symbol')
        else:
            for name in font.getGlyphOrder():
                a=font['glyf'][name].getCoordinates(font['glyf'])
                b=variant['glyf'][name].getCoordinates(variant['glyf'])
                check(list(a[0])==list(b[0]) and list(a[1])==list(b[1]),'Web outline mismatch '+extension)
        # Exercise the decoded font in FreeType and HarfBuzz as well as parsing tables.
        variant.flavor=None;payload=io.BytesIO();variant.save(payload)
        decoded=payload.getvalue()
        proof=hb.Buffer();proof.add_str(''.join(map(chr,sorted(expected))));proof.guess_segment_properties()
        hb.shape(hb.Font(hb.Face(decoded)),proof)
        check(len(proof.glyph_infos)==196 and all(item.codepoint for item in proof.glyph_infos),'Shaping failure '+extension)
        check(all(pos.x_advance==650 for pos in proof.glyph_positions),'Shaped advance mismatch '+extension)
        for size in (12,16,24,32,48,96):
            face=ImageFont.truetype(io.BytesIO(decoded),size)
            for code in expected:
                if code not in (32,160):check(face.getmask(chr(code)).getbbox() is not None,'Empty raster '+extension)
                check(abs(face.getlength(chr(code))-size*.65)<.02,'Raster metric mismatch '+extension)
    hashes=(directory/'SHA256SUMS').read_text().splitlines()
    check({line.split()[1] for line in hashes}=={'AfterbyteMono-Regular.'+ext for ext in signatures},'Checksum manifest must cover all four formats')
    for line in hashes:
        digest,name=line.split();check(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'Checksum')
    links=0
    for document in ROOT.rglob('*.md'):
        if '.git' in document.parts:continue
        text=document.read_text()
        destinations=re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text)+re.findall(r'(?:src|srcset)="([^"]+)"',text)
        for destination in destinations:
            destination=destination.strip().split()[0].strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',destination) or destination.startswith('#'):continue
            target=(document.parent/unquote(destination.split('#',1)[0])).resolve()
            check(target.is_relative_to(ROOT) and target.exists(),f'Missing link {destination}')
            links+=1
    print(f'PASS: OTF/CFF, TTF, WOFF, WOFF2; 197 glyphs / 196 mappings; source agreement; topology; mono metrics; signatures; licenses; cross-format outline equivalence; shaping; 6-size raster smoke checks; checksums; {links} links/images.')
    print('Scope: technical validation, not legal clearance or independent certification.')


if __name__=='__main__':validate()
