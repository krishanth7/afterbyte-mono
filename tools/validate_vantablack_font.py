#!/usr/bin/env python3
"""Validate the actual alpha binaries, source geometry, shaping and rasterization."""
import hashlib
import json
from pathlib import Path

import uharfbuzz as hb
from PIL import ImageFont
from shapely.geometry import Polygon
from shapely.ops import unary_union
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
FONTS=ROOT/'fonts/vantablack-gothic'


def require(condition,message):
    if not condition: raise ValueError(message)


def validate():
    config=json.loads((ROOT/'docs/vantablack-gothic/system.json').read_text())
    source=json.loads((ROOT/'sources/vantablack-gothic/glyphs.json').read_text())
    ttf_path=FONTS/'VantablackGothic-Regular.ttf'
    ttf=TTFont(ttf_path,checkChecksums=2)
    woff=TTFont(FONTS/'VantablackGothic-Regular.woff2',checkChecksums=2)
    required={'head','hhea','maxp','OS/2','hmtx','cmap','loca','glyf','name','post'}
    require(required.issubset(ttf.keys()),'Missing required TrueType table')
    require(ttf['head'].unitsPerEm==1000,'Wrong UPEM')
    require(ttf.getGlyphOrder()[0]=='.notdef','Missing glyph must be first')
    require(len(ttf.getGlyphOrder())==96,'Expected 95 ASCII glyphs plus .notdef')
    require(set(ttf.getBestCmap())==set(range(32,127)),'ASCII coverage mismatch')
    require(ttf.getBestCmap()==woff.getBestCmap(),'WOFF2 cmap mismatch')
    require(ttf['hmtx'].metrics==woff['hmtx'].metrics,'WOFF2 advances mismatch')
    require(ttf['post'].isFixedPitch==0,'Must be proportional')
    require('fvar' not in ttf,'No variable font axis is advertised')
    require((ttf['hhea'].ascent,ttf['hhea'].descent,ttf['hhea'].lineGap)==(820,-200,0),'Wrong hhea metrics')
    os2=ttf['OS/2']
    require((os2.sTypoAscender,os2.sTypoDescender,os2.sTypoLineGap)==(820,-200,0),'Wrong typo metrics')
    require((os2.sCapHeight,os2.sxHeight)==(780,580),'Wrong cap/x-height metadata')
    require(os2.fsType==0,'Unexpected embedding restrictions')
    require(ttf['name'].getDebugName(1)=='Vantablack Gothic','Wrong family name')
    require('MIT License' in ttf['name'].getDebugName(13),'Missing embedded license')
    require(ttf['name'].getDebugName(6)=='VantablackGothic-Regular','Wrong PostScript name')
    mapping=ttf.getBestCmap()
    shapes={}
    for record in source['glyphs']:
        name=record['glyph_name']
        require(name in ttf.getGlyphOrder(),f'{name}: absent from binary')
        actual=ttf['glyf'][name]
        require(not actual.isComposite(),f'{name}: unexpected composite')
        require(actual.numberOfContours==len(record['contours']),f'{name}: source/binary contour count mismatch')
        source_points=[]
        parts=[]; shell=None; holes=[]
        for contour in record['contours']:
            pts=contour['points'];source_points.extend(map(tuple,pts))
            require(len(pts)>=3,f'{name}: short contour')
            area=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(pts,pts[1:]+pts[:1]))
            require(area!=0,f'{name}: zero-area contour')
            require((area<0)==(contour['role']=='outer'),f'{name}: wrong contour winding')
            for a,b in zip(pts,pts[1:]+pts[:1]):
                dx,dy=b[0]-a[0],b[1]-a[1]
                require(dx!=0 or dy!=0,f'{name}: zero-length edge')
                require(not dx or not dy or abs(dx)==abs(dy),f'{name}: non-axis/45-degree edge {a,b}')
                require(all(type(n) is int for n in a),f'{name}: fractional coordinate')
            if contour['role']=='outer':
                if shell is not None: parts.append(Polygon(shell,holes))
                shell,holes=pts,[]
            else:
                require(shell is not None,f'{name}: counter before shell')
                holes.append(pts)
        if shell is not None:parts.append(Polygon(shell,holes))
        for part in parts: require(part.is_valid and part.area>0,f'{name}: invalid source topology')
        if record['codepoint']==32:
            require(not parts and actual.numberOfContours==0,'Space must be blank')
            continue
        require(parts,f'{name}: missing outlines')
        shape=unary_union(parts);shapes[name]=shape
        require(abs(sum(p.area for p in parts)-shape.area)<0.01,f'{name}: overlapping filled components')
        x0,y0,x1,y1=shape.bounds
        require(y0>=-200 and y1<=820,f'{name}: clipping bounds')
        require(os2.usWinAscent>=y1 and os2.usWinDescent>=-y0,f'{name}: Windows clipping')
        require(x0==24 and record['advance']-x1==24,f'{name}: side bearings')
        coords,ends,flags=actual.getCoordinates(ttf['glyf'])
        require(list(map(tuple,coords))==source_points,f'{name}: source/binary point mismatch')
        require(all(int(flag)&1 for flag in flags),f'{name}: unexpected curve control point')
        other=woff['glyf'][name].getCoordinates(woff['glyf'])
        require(list(coords)==list(other[0]) and list(ends)==list(other[1]),f'{name}: WOFF2 outline mismatch')
        require(ttf['hmtx'].metrics[name]==(record['advance'],24),f'{name}: metrics mismatch')
    for item in config['glyphs']:
        require(ttf['hmtx'].metrics[mapping[item['codepoint']]][0]==item['advance'],'Contract/binary advance mismatch')
    for a,b in [('0','O'),('1','I'),('I','l'),('i','l'),('S','5'),('a','e')]:
        require(not shapes[mapping[ord(a)]].equals(shapes[mapping[ord(b)]]),f'Indistinguishable outlines: {a}/{b}')
    # H is the exact control for the two disconnected 15-unit crossbar gaps.
    h=shapes[mapping[ord('H')]]
    require(len(h.geoms)==3,'H must contain two stems and detached bar')
    components=sorted(h.geoms,key=lambda p:p.bounds[0])
    require(components[1].bounds[0]-components[0].bounds[2]==15,'H left micro-gap')
    require(components[2].bounds[0]-components[1].bounds[2]==15,'H right micro-gap')
    face=hb.Face(ttf_path.read_bytes());hbfont=hb.Font(face)
    buffer=hb.Buffer();buffer.add_str(''.join(chr(i) for i in range(32,127)));buffer.guess_segment_properties()
    hb.shape(hbfont,buffer)
    require(len(buffer.glyph_infos)==95 and all(g.codepoint for g in buffer.glyph_infos),'HarfBuzz missing glyph or unexpected shaping')
    for size in (32,48,64,80,120,240):
        rendered=ImageFont.truetype(str(ttf_path),size)
        for code in range(33,127):
            require(rendered.getmask(chr(code)).getbbox() is not None,f'U+{code:04X}: empty raster at {size}px')
    for line in (FONTS/'SHA256SUMS').read_text().splitlines():
        expected,filename=line.split()
        require(hashlib.sha256((FONTS/filename).read_bytes()).hexdigest()==expected,'Checksum mismatch: '+filename)
    print('PASS: 96 glyphs; 95 ASCII mappings; topology, integer/45-degree edges, bearings, metrics, license, WOFF2 equivalence, HarfBuzz shaping, 6-size FreeType raster smoke checks, checksums.')
    print('Alpha limits: no hinting, kerning, extended language coverage, platform installation audit, or WCAG certification.')


if __name__=='__main__': validate()
