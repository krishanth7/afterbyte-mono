#!/usr/bin/env python3
"""Original polygon recipes for Vantablack Gothic 0.1.0 alpha. MIT licensed.

No external font outlines are loaded. The generated JSON is the editable,
normalized source; these recipes plus system.json reproduce it.
"""
import hashlib
import json
from pathlib import Path

from shapely import affinity
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
EPOCH = 3877200000  # Fixed OpenType timestamp for reproducible alpha builds.


def union(*parts):
    return unary_union([p for p in parts if not p.is_empty])


def rect(x0, y0, x1, y1, cut=0):
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"Empty rectangle: {(x0,y0,x1,y1)}")
    c = min(cut, (x1-x0)//2, (y1-y0)//2)
    return Polygon([(x0+c,y0),(x1-c,y0),(x1,y0+c),(x1,y1-c),
                    (x1-c,y1),(x0+c,y1),(x0,y1-c),(x0,y0+c)])


def ring(l, r, bottom, top, cut=55, stem=110):
    return rect(l,bottom,r,top,cut).difference(
        rect(l+stem,bottom+stem,r-stem,top-stem,min(cut,30)))


def path(points, thickness=110):
    """Expand axis/45-degree centerlines with polygon unions, without curves."""
    pieces = []
    half = thickness//2
    diagonal = round(thickness/(2**0.5)/2)
    for (x0,y0),(x1,y1) in zip(points, points[1:]):
        dx, dy = x1-x0, y1-y0
        if not dx:
            pieces.append(box(x0-half,min(y0,y1),x0+half,max(y0,y1)))
        elif not dy:
            pieces.append(box(min(x0,x1),y0-half,max(x0,x1),y0+half))
        elif abs(dx) == abs(dy):
            ox, oy = diagonal*(1 if dy > 0 else -1), diagonal*(-1 if dx > 0 else 1)
            pieces.append(Polygon([(x0+ox,y0+oy),(x1+ox,y1+oy),
                                   (x1-ox,y1-oy),(x0-ox,y0-oy)]))
        else:
            raise ValueError(f"Non-grid segment: {(x0,y0),(x1,y1)}")
    for x,y in points[1:-1]:
        pieces.append(rect(x-half,y-half,x+half,y+half,24))
    return union(*pieces)


def vshape(l,r,bottom,top):
    m=(l+r)//2
    d=m-l
    # The diagonal band offset 156 yields approximately 110 perpendicular units.
    return Polygon([(l,top),(l+110,top),(l+110,bottom+d+46),
                    (m,bottom+156),(r-110,bottom+(r-m)+46),
                    (r-110,top),(r,top),(r,bottom+r-m),
                    (m,bottom),(l,bottom+d)])


def opened(l,r,bottom,top):
    m=(top+bottom)//2
    opening=Polygon([(r-125,m-15),(r-55,m-15),(r+20,m-90),
                     (r+20,m+90),(r-55,m+15),(r-125,m+15)])
    return ring(l,r,bottom,top).difference(opening)


def serpentine(l,r,h):
    mid=h//2
    return path([(r,h-55),(l+55,h-55),(l+55,mid),
                 (r-55,mid),(r-55,55),(l,55)])


def make_letter(ch, advance):
    l,r=24,advance-24
    c=(l+r)//2
    h=780 if ch.isupper() else 580
    left=lambda top=h,bottom=0: rect(l,bottom,l+110,top)
    right=lambda top=h,bottom=0: rect(r-110,bottom,r,top)
    top=lambda: rect(l,h-110,r,h,30)
    base=lambda: rect(l,0,r,110,30)
    detached=lambda y=335: rect(l+125,y,r-125,y+110,15)
    if ch in 'Oo': return ring(l,r,0,h)
    if ch in 'Cc': return opened(l,r,0,h)
    if ch=='A':
        apex=affinity.scale(vshape(l,r,0,780),1,-1,origin=(0,390))
        return union(apex,detached())
    if ch=='B': return union(left(),ring(l,r,335,780),ring(l,r,0,445))
    if ch=='D': return union(ring(l,r,0,h),left())
    if ch=='E': return union(left(),top(),base(),rect(l+125,335,r,445,15))
    if ch=='F': return union(left(),top(),rect(l+125,335,r,445,15))
    if ch=='G': return union(opened(l,r,0,h),rect(c,280,r,390),right(390,150))
    if ch=='H': return union(left(),right(),detached())
    if ch=='I': return left()
    if ch=='J': return union(right(),base(),left(220))
    if ch in 'Kk':
        cy=h//2
        end=r-55
        start=l+55
        d=end-start
        return union(left(820 if ch=='k' else h),
                     path([(start,cy),(end,cy+d),(end,h)]),
                     path([(start,cy),(end,cy-d),(end,0)]))
    if ch=='L': return union(left(),base())
    if ch=='M': return union(left(),right(),vshape(l,r,280,h))
    if ch=='N':
        d=r-l-110
        return union(left(),right(),path([(l+55,780),(l+55,390+d//2),
                                          (r-55,390-d//2),(r-55,0)]))
    if ch=='P': return union(left(),ring(l,r,335,h))
    if ch=='Q':
        return union(ring(l,r-40,0,h),
                     Polygon([(r-110,55),(r, -55),(r,-110),(r-55,-110),(r-165,0)]))
    if ch=='R':
        return union(left(),ring(l,r,335,h),
                     path([(l+55,390),(r-55,390-(r-l-110)),(r-55,0)]))
    if ch in 'Ss': return serpentine(l,r,h)
    if ch=='T': return union(top(),rect(c-55,0,c+55,h))
    if ch in 'Uu': return union(ring(l,r,0,h).difference(box(l+110,h-110,r-110,h+20)),left(),right())
    if ch in 'Vv': return vshape(l,r,0,h)
    if ch in 'Ww':
        span=(r-l+112)//2
        span-=span%4
        return union(vshape(l,l+span,0,h),vshape(l+span-112,r,0,h))
    if ch in 'Xx':
        a,b=l+55,r-55
        d=b-a
        cy=h//2
        return union(path([(a,h),(a,cy+d//2),(b,cy-d//2),(b,0)]),
                     path([(b,h),(b,cy+d//2),(a,cy-d//2),(a,0)]))
    if ch in 'Yy':
        return union(vshape(l,r,h//2,h),rect(c-55,-200 if ch=='y' else 0,c+55,h//2+156))
    if ch in 'Zz':
        a,b=l+55,r-55
        d=b-a
        cy=h//2
        return union(top(),base(),path([(b,h-55),(b,cy+d//2),
                                       (a,cy-d//2),(a,55)]))
    if ch=='a': return union(ring(l,r,0,h),right(),rect(l+110,300,r-110,410))
    if ch=='b': return union(left(820),ring(l,r,0,h))
    if ch=='d': return union(right(820),ring(l,r,0,h))
    if ch=='e':
        return union(ring(l,r,0,h),rect(l+110,300,r,410)).difference(
            Polygon([(r-125,245),(r-55,245),(r+20,170),(r+20,300),(r-125,300)]))
    if ch=='f': return union(rect(c-55,0,c+55,820),rect(l,470,r,580),rect(c-55,710,r,820,30))
    if ch=='g': return union(ring(l,r,0,h),right(h,-200),rect(l,-200,r,-90,30))
    if ch=='h': return union(left(820),ring(l,r,0,h).difference(box(l+110,-20,r-110,290)))
    if ch in 'ij':
        stem=rect(r-110,-200 if ch=='j' else 0,r,580)
        return union(stem,rect(r-110,670,r,780),rect(l,-200,r,-90) if ch=='j' else GeometryCollection())
    if ch=='l': return left(820)
    if ch=='m':
        mid=c
        return union(left(),right(),rect(mid-55,0,mid+55,580),top()).difference(
            union(Polygon([(l,580),(l+35,580),(l,545)]),Polygon([(r,580),(r-35,580),(r,545)])))
    if ch=='n': return union(left(),right(),top())
    if ch=='p': return union(left(h,-200),ring(l,r,0,h))
    if ch=='q': return union(right(h,-200),ring(l,r,0,h))
    if ch=='r': return union(left(),top(),right(h,400))
    if ch=='t': return union(rect(c-55,0,c+55,700),rect(l,470,r,580),rect(c-55,0,r,110,25))
    raise ValueError(f"Missing letter {ch}")


def make_digit(ch, advance):
    l,r=24,advance-24
    c=(l+r)//2
    h=780
    left=rect(l,0,l+110,h)
    right=rect(r-110,0,r,h)
    if ch=='0': return union(ring(l,r,0,h),rect(c-25,0,c+25,h))
    if ch=='1':
        return union(right,Polygon([(l,615),(l,725),(l+55,780),(r,780),(r,670),(l+55,670)]))
    if ch=='2':
        d=r-l-110
        cy=390
        return union(rect(l,670,r,780,35),rect(l,0,r,110,35),
                     path([(r-55,725),(r-55,cy+d//2),(l+55,cy-d//2),(l+55,55)]))
    if ch=='3': return union(right,rect(l,670,r,780,40),rect(l,335,r,445,20),rect(l,0,r,110,40))
    if ch=='4': return union(right,rect(l,290,r,400),rect(l,345,l+110,780,30))
    if ch=='5': return union(rect(l,335,l+110,780),rect(l,670,r,780,30),
                             rect(l,335,r,445),rect(r-110,55,r,390),rect(l,0,r,110,30))
    if ch=='6': return union(left,ring(l,r,0,445),rect(l,670,r,780,40))
    if ch=='7': return union(rect(l,670,r,780,30),
                            path([(r-55,725),(r-55,390+(r-l-110)//2),
                                  (l+55,390-(r-l-110)//2),(l+55,0)]))
    if ch=='8': return union(ring(l,r,335,780),ring(l,r,0,445))
    if ch=='9': return union(right,ring(l,r,335,780),rect(l,0,r,110,35))
    raise ValueError(ch)


def make_symbol(ch, advance):
    l,r=24,advance-24
    c=(l+r)//2
    dot=rect(c-55,0,c+55,110)
    comma=union(rect(l,0,l+110,110),Polygon([(l,0),(l+110,0),(l+110,-50),(l+30,-130),(l,-130)]))
    if ch==' ': return GeometryCollection()
    if ch=='.': return dot
    if ch==',': return comma
    if ch==':': return union(rect(c-55,110,c+55,220),rect(c-55,450,c+55,560))
    if ch==';': return union(comma,rect(l,450,l+110,560))
    if ch=='!': return union(dot,rect(c-55,220,c+55,780,20))
    if ch=='?': return union(dot,rect(l,670,r,780,40),rect(r-110,400,r,726,20),rect(c-55,220,c+55,510),rect(c-55,400,r,510))
    if ch=="'": return rect(l,560,r,780,25)
    if ch=='"': return union(rect(l,560,l+70,780,20),rect(r-70,560,r,780,20))
    if ch=='`': return Polygon([(l,780),(l+60,780),(r,780-(r-l-60)),(r,780-(r-l))])
    if ch=='-': return rect(l,335,r,445,20)
    if ch=='_': return rect(l,-160,r,-50)
    if ch=='=': return union(rect(l,225,r,335),rect(l,445,r,555))
    if ch=='+': return union(rect(l,335,r,445),rect(c-55,200,c+55,580))
    if ch in '/\\':
        a,b=l+55,r-55
        d=b-a
        shape=path([(a,0),(a,390-d//2),(b,390+d//2),(b,780)])
        return affinity.scale(shape,-1,1,origin=(c,0)) if ch=='\\' else shape
    if ch=='|': return rect(l,-120,r,820)
    if ch in '[]':
        shape=union(rect(l,-100,l+70,820),rect(l,710,r,820),rect(l,-100,r,10))
        return affinity.scale(shape,-1,1,origin=(c,0)) if ch==']' else shape
    if ch in '()':
        shape=Polygon([(r,820),(r,710),(l+110,710-(r-l-110)),(l+110,10+r-l-110),
                       (r,10),(r,-100),(r-70,-100),(l,-100+r-l-70),(l,820-(r-l-70)),(r-70,820)])
        return affinity.scale(shape,-1,1,origin=(c,0)) if ch==')' else shape
    if ch in '{}':
        # Narrow braces deliberately use 70-unit strokes to preserve the central notch.
        d=c+20-(l+35)
        shape=path([(r,765),(c+20,765),(c+20,390+d),(l+35,390),
                    (c+20,390-d),(c+20,-45),(r,-45)],70)
        return affinity.scale(shape,-1,1,origin=(c,0)) if ch=='}' else shape
    if ch in '<>':
        d=r-l
        shape=Polygon([(r,390+d),(r,390+d-156),(l+156,390),
                       (r,390-d+156),(r,390-d),(l,390)])
        return affinity.scale(shape,-1,1,origin=(c,0)) if ch=='>' else shape
    if ch=='^':
        d=c-l
        return Polygon([(l,650-d),(c,650),(r,650-d),(r,650-d-156),(c,494),(l,650-d-156)])
    if ch=='~':
        return path([(l,335),(l+55,390),(c-30,390),(c+30,330),(r-55,330),(r,385)],70).intersection(box(l,0,r,780))
    if ch=='#': return union(rect(l+40,80,l+110,700),rect(r-110,80,r-40,700),rect(l,230,r,340),rect(l,470,r,580))
    if ch=='*':
        span=(r-l)//2
        return union(rect(c-35,390-span,c+35,390+span),
                     path([(l+25,390-span+25),(r-25,390+span-25)],70),
                     path([(l+25,390+span-25),(r-25,390-span+25)],70))
    if ch=='%':
        return union(ring(l,l+220,480,780,30,60),ring(r-220,r,0,300,30,60),
                     path([(l+55,110),(r-55,110+r-l-110)],70))
    if ch=='$': return union(serpentine(l,r,780),rect(c-25,-80,c+25,820))
    if ch=='&':
        return union(ring(l,r-70,350,780),ring(l,r,0,460),
                     path([(l+55,550),(r-55,550-(r-l-110)),(r-55,0)]))
    if ch=='@':
        outer=ring(l,r,0,780)
        inner=ring(l+145,r-115,230,570,30,60)
        return union(outer.difference(box(r-110,110,r+10,280)),inner,rect(r-175,230,r-115,570))
    raise ValueError(f"Missing symbol {ch!r}")


def polygons(shape):
    if shape.is_empty: return []
    if isinstance(shape, Polygon): return [shape]
    if isinstance(shape, MultiPolygon): return list(shape.geoms)
    return [g for g in shape.geoms if isinstance(g,Polygon)]


def normalized(shape):
    result=[]
    for p in sorted(polygons(shape),key=lambda p:p.bounds):
        p=orient(p,sign=-1)  # TrueType outer clockwise, counter counterclockwise.
        for role,ring_ in [('outer',p.exterior)]+[('counter',q) for q in p.interiors]:
            points=[[int(round(x)),int(round(y))] for x,y in list(ring_.coords)[:-1]]
            # Remove redundant vertices, including duplicated closing points.
            clean=[]
            for pt in points:
                if not clean or pt!=clean[-1]: clean.append(pt)
            changed=True
            while changed and len(clean)>3:
                changed=False
                for i in range(len(clean)):
                    a,b,c=clean[i-1],clean[i],clean[(i+1)%len(clean)]
                    if (b[0]-a[0])*(c[1]-b[1]) == (b[1]-a[1])*(c[0]-b[0]):
                        clean.pop(i); changed=True; break
            result.append({'role':role,'points':clean})
    return result


def build():
    config=json.loads((ROOT/'docs/vantablack-gothic/system.json').read_text())
    records=[]
    missing=ring(24,436,0,780)
    records.append({'glyph_name':'.notdef','codepoint':None,'advance':460,'contours':normalized(missing)})
    for item in config['glyphs']:
        ch=item['character']; width=item['advance']
        if ch.isalpha(): shape=make_letter(ch,width)
        elif ch.isdigit(): shape=make_digit(ch,width)
        else: shape=make_symbol(ch,width)
        if not shape.is_empty and not shape.is_valid:
            raise ValueError(f'Invalid recipe for {ch!r}')
        # Give punctuation and alpha optical variants consistent final bearings.
        # No scaling: geometry remains axis/45-degree, and wider shapes require review.
        if not shape.is_empty:
            x0,_,x1,_=shape.bounds
            shape=affinity.translate(shape,xoff=24-x0)
            actual_width=int(round(x1-x0))+48
            if actual_width!=width:
                # Narrow marks/complex forms get their actual proportional advance.
                item['advance']=actual_width
                width=actual_width
        item['status']='alpha-outline'
        records.append({'glyph_name':'space' if ch==' ' else f'uni{ord(ch):04X}',
                        'codepoint':ord(ch),'advance':width,'contours':normalized(shape)})
    source={'family':'Vantablack Gothic','version':VERSION,'license':'MIT',
            'author':'Krishanth','status':'alpha','glyphs':records}
    src=ROOT/'sources/vantablack-gothic'; src.mkdir(parents=True,exist_ok=True)
    (src/'glyphs.json').write_text(json.dumps(source,indent=2)+'\n')
    config.update(status='alpha',outline_status='implemented-alpha',version=VERSION)
    (ROOT/'docs/vantablack-gothic/system.json').write_text(json.dumps(config,indent=2)+'\n')
    compile_source()


def compile_source():
    source=json.loads((ROOT/'sources/vantablack-gothic/glyphs.json').read_text())
    records=source['glyphs']
    order=[r['glyph_name'] for r in records]
    fb=FontBuilder(1000,isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({r['codepoint']:r['glyph_name'] for r in records if r['codepoint'] is not None})
    glyphs={}; metrics={}
    for record in records:
        pen=TTGlyphPen(None)
        for contour in record['contours']:
            pts=contour['points']; pen.moveTo(pts[0])
            for point in pts[1:]: pen.lineTo(point)
            pen.closePath()
        glyphs[record['glyph_name']]=pen.glyph()
        metrics[record['glyph_name']]=(record['advance'],24 if record['contours'] else 0)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=820,descent=-200,lineGap=0)
    license_text=(ROOT/'LICENSE').read_text()
    fb.setupNameTable({'familyName':'Vantablack Gothic','styleName':'Regular',
                      'fullName':'Vantablack Gothic Regular','psName':'VantablackGothic-Regular',
                      'uniqueFontIdentifier':'Krishanth:VantablackGothic-Regular:0.1.0',
                      'version':'Version 0.100; alpha 0.1.0','designer':'Krishanth',
                      'copyright':'Copyright (c) 2026 Krishanth',
                      'description':'Original proportional polygon display font. ASCII alpha; unhinted.',
                      'licenseDescription':license_text,
                      'licenseInfoURL':'https://github.com/krishanth7/afterbyte-mono/blob/main/LICENSE',
                      'vendorURL':'https://github.com/krishanth7/afterbyte-mono',
                      'typographicFamily':'Vantablack Gothic','typographicSubfamily':'Regular'})
    fb.setupOS2(version=4,usWeightClass=400,usWidthClass=2,fsType=0,
                fsSelection=0xC0,sTypoAscender=820,sTypoDescender=-200,sTypoLineGap=0,
                usWinAscent=820,usWinDescent=200,sCapHeight=780,sxHeight=580,
                achVendID='KRIS')
    fb.setupPost(isFixedPitch=0,underlinePosition=-160,underlineThickness=60)
    fb.font['head'].created=EPOCH; fb.font['head'].modified=EPOCH
    fb.font['head'].fontRevision=0.1
    # Candidate pair kerning is intentionally not shipped until visually measured.
    out=ROOT/'fonts/vantablack-gothic';out.mkdir(parents=True,exist_ok=True)
    fb.save(out/'VantablackGothic-Regular.ttf')
    fb.font.flavor='woff2'
    fb.save(out/'VantablackGothic-Regular.woff2')
    (out/'LICENSE.txt').write_text(license_text)
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('VantablackGothic-Regular.*'))}
    (out/'SHA256SUMS').write_text(''.join(f'{value}  {name}\n' for name,value in manifest.items()))
    print(f'Built {len(records)} glyphs: TTF, WOFF2, editable JSON, license, checksums.')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-source',action='store_true',help='Compile the edited glyphs.json without regenerating recipes.')
    args=parser.parse_args()
    compile_source() if args.from_source else build()
