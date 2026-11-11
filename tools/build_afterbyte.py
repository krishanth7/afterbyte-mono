#!/usr/bin/env python3
"""OFL-1.1 compiler: original core, licensed Noto expansion, Braille and math."""
import argparse, copy, hashlib, json, math, unicodedata as ud
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.roundingPen import RoundingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.ttLib.tables.O_S_2f_2 import Panose
import build_core
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_VERSION=4

def name_for(c):return 'space' if c==32 else f'uni{c:04X}' if c<=65535 else f'u{c:05X}'

def copy_glyph(glyph,gs,transform=(1,0,0,1,0,0)):
    source=DecomposingRecordingPen(gs);glyph.draw(source)
    pen=TTGlyphPen(None);source.replay(TransformPen(RoundingPen(pen),transform));return pen.glyph()

def harmonize(glyph,gs):
    p=BoundsPen(gs);glyph.draw(p)
    if p.bounds is None:return copy_glyph(glyph,gs)
    x0,y0,x1,y1=p.bounds;sx=min(650/600,618/(x1-x0)) if x1>x0 else 1
    return copy_glyph(glyph,gs,(sx,0,0,700/714,325-(x0+x1)*sx/2,0))

def braille(c):
    pen=TTGlyphPen(None)
    positions=[(215,650),(215,450),(215,250),(435,650),(435,450),(435,250),(215,50),(435,50)]
    for bit,(x,y) in enumerate(positions):
        if not ((c-0x2800)>>bit)&1:continue
        pts=[(round(x+42*math.cos(-i*math.tau/24)),round(y+42*math.sin(-i*math.tau/24))) for i in range(24)]
        pen.moveTo(pts[0])
        for pt in pts[1:]:pen.lineTo(pt)
        pen.closePath()
    return pen.glyph()

def math_glyph(c,core,donor,recipes):
    base=ud.normalize('NFKD',chr(c))[-1];bold='BOLD' in ud.name(chr(c));italic='ITALIC' in ud.name(chr(c)) or c==0x210e
    if base=='∇':recipes[base]={'paths':[[['M',78,668],['L',325,32],['L',572,668],['Z']]],'solids':[],'stroke':64}
    if base not in recipes:return harmonize(donor.getGlyphSet()[donor.getBestCmap()[ord(base)]],donor.getGlyphSet())
    shape=build_core.shape_for(recipes[base])
    if 'DOUBLE-STRUCK' in ud.name(chr(c)):shape=shape.boundary.buffer(10,quad_segs=8)
    elif bold:shape=shape.buffer(13,quad_segs=8)
    p=TTGlyphPen(None)
    for contour in build_core.contours_for(shape):
        p.moveTo(contour[0])
        for pt in contour[1:]:p.lineTo(pt)
        p.closePath()
    glyph=p.glyph();record=DecomposingRecordingPen(core.getGlyphSet());glyph.draw(record,core['glyf'])
    pen=BoundsPen(None);record.replay(pen);x0,y0,x1,y1=pen.bounds
    shear=.18 if italic else 0;xs=[x+shear*y for x in (x0,x1) for y in (y0,y1)]
    sx=min(1,610/(max(xs)-min(xs)));dx=325-(max(xs)+min(xs))*sx/2
    p=TTGlyphPen(None);record.replay(TransformPen(RoundingPen(p),(sx,0,shear*sx,1,dx,0)));return p.glyph()

def technical(c):
    paths={
        0x2211:[['M',570,700],['L',100,700],['L',350,350],['L',100,0],['L',570,0]],
        0x222b:[['M',500,725],['C',365,820,290,710,290,570],['L',290,130],['C',290,-30,200,-85,100,0]],
    }
    record={'paths':[paths[c]] if c in paths else [[['M',70,700],['L',580,700]],[['M',145,700],['L',145,0]],[['M',505,700],['L',505,0]]],'solids':[],'stroke':64}
    pen=TTGlyphPen(None)
    for contour in build_core.contours_for(build_core.shape_for(record)):
        pen.moveTo(contour[0])
        for point in contour[1:]:pen.lineTo(point)
        pen.closePath()
    return pen.glyph()

def build(version=DEFAULT_VERSION,out=None):
    build_core.build();core=TTFont(ROOT/'build/core/AfterbyteMono-Regular.ttf')
    path=ROOT/'sources/upstream/NotoSansMono-ExpansionSource.ttf'
    provenance=json.loads((ROOT/'sources/upstream/provenance.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==provenance['subset_sha256']
    donor=TTFont(path);dgs=donor.getGlyphSet()
    contract=json.loads((ROOT/f'sources/afterbyte-mono/coverage-v{version}.json').read_text())
    recipes={g['character']:g for g in json.loads((ROOT/'sources/afterbyte-mono/vectors.json').read_text())['glyphs']}
    glyphs={'.notdef':copy.deepcopy(core['glyf']['.notdef'])};cmap={};metrics={'.notdef':(650,78)};order=['.notdef'];ys=[]
    for r in contract['glyphs']:
        c=r['unicode'];name=name_for(c);origin=r['origin']
        if origin=='afterbyte':glyph=copy.deepcopy(core['glyf'][core.getBestCmap()[c]])
        elif origin=='noto':glyph=harmonize(dgs[donor.getBestCmap()[c]],dgs)
        elif origin=='braille':glyph=braille(c)
        elif origin=='technical':glyph=technical(c)
        else:glyph=math_glyph(c,core,donor,recipes)
        glyph.recalcBounds(None);lsb=glyph.xMin if glyph.numberOfContours else 0
        if glyph.numberOfContours:
            assert 0<=glyph.xMin<glyph.xMax<=650,(c,glyph.xMin,glyph.xMax)
            ys.append((glyph.yMin,glyph.yMax))
        glyphs[name]=glyph;metrics[name]=(650,lsb);cmap[c]=name;order.append(name)
    assert len(order)==contract['glyph_count'] and len(cmap)==contract['unicode_count']
    ymin=min(y[0] for y in ys);ymax=max(y[1] for y in ys);assert -450<=ymin and ymax<=1280,(ymin,ymax)
    fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1280,descent=-450,lineGap=0)
    license_text=(ROOT/'OFL.txt').read_text()
    fb.setupNameTable({'familyName':'Afterbyte Mono','styleName':'Regular','typographicFamily':'Afterbyte Mono','typographicSubfamily':'Regular',
        'fullName':'Afterbyte Mono Regular','psName':'AfterbyteMono-Regular','uniqueFontIdentifier':f'Krishanth:AfterbyteMono-Regular:{version}.0.0',
        'version':f'Version {version}.000','designer':'Krishanth; The Noto Project Authors (selected expansion glyphs)',
        'copyright':'Copyright (c) 2026 Krishanth. Copyright 2022 The Noto Project Authors.',
        'description':f'Afterbyte Mono {version}.0.0. Original Afterbyte core; licensed Noto multilingual expansion; algorithmic Braille and mathematical styles. {len(order)} glyphs, {len(cmap)} Unicode mappings.',
        'licenseDescription':license_text,'licenseInfoURL':'https://openfontlicense.org','vendorURL':'https://github.com/krishanth7/afterbyte-mono'})
    panose=Panose();panose.bFamilyType=2;panose.bProportion=9
    fb.setupOS2(version=4,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0xc0,sTypoAscender=1280,sTypoDescender=-450,
        sTypoLineGap=0,usWinAscent=1280,usWinDescent=450,sCapHeight=700,sxHeight=500,panose=panose,achVendID='KRIS')
    fb.setupPost(isFixedPitch=1,underlinePosition=-160,underlineThickness=45)
    fb.font['gasp']=newTable('gasp');fb.font['gasp'].gaspRange={65535:2}
    fb.font['head'].created=fb.font['head'].modified=3877286400;fb.font['head'].fontRevision=float(version)
    out=Path(out) if out else ROOT/'fonts/afterbyte-mono';out.mkdir(parents=True,exist_ok=True)
    fb.save(out/'AfterbyteMono-Regular.ttf')
    otf=FontBuilder(1000,isTTF=False);otf.setupGlyphOrder(order);otf.setupCharacterMap(cmap)
    strings={};gs=fb.font.getGlyphSet()
    for name in order:
        pen=T2CharStringPen(650,None);gs[name].draw(ReverseContourPen(pen));strings[name]=pen.getCharString()
    otf.setupCFF('AfterbyteMono-Regular',{'FullName':'Afterbyte Mono Regular','FamilyName':'Afterbyte Mono','Weight':'Regular',
        'version':f'{version}.000','isFixedPitch':True,'Notice':'Copyright 2026 Krishanth; Copyright 2022 The Noto Project Authors. SIL Open Font License 1.1.'},strings,{})
    for tag in ('head','hhea','hmtx','name','OS/2'):otf.font[tag]=copy.deepcopy(fb.font[tag])
    otf.setupPost(isFixedPitch=1,underlinePosition=-160,underlineThickness=45);otf.save(out/'AfterbyteMono-Regular.otf')
    for ext in ('woff','woff2'):fb.font.flavor=ext;fb.save(out/f'AfterbyteMono-Regular.{ext}')
    (out/'LICENSE.txt').write_text(license_text)
    (out/'coverage.txt').write_text(f'Afterbyte Mono Regular / {version}.0.0\n{len(order)} glyphs: {len(cmap)} Unicode mappings + .notdef.\n650-unit fixed advance; spacing characters only.\n\n'+''.join(f'U+{r["unicode"]:04X} {chr(r["unicode"])} {r["name"]} [{r["origin"]}]\n' for r in contract['glyphs']))
    summary={'version':f'{version}.0.0','glyph_count':len(order),'unicode_count':len(cmap),'added_since_v3':len(cmap)-196,
             'actual_ink_bounds':[ymin,ymax],'typographic_bounds':[-450,1280],
             'origin_counts':{s:sum(r['origin']==s for r in contract['glyphs']) for s in ('afterbyte','noto','technical','braille','mathematical-style')}}
    (out/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'afterbyte-mono.css').write_text(f'/* Afterbyte Mono {version}.0.0. OFL-1.1; see LICENSE.txt. */\n@font-face {{\n  font-family: "Afterbyte Mono";\n  src: url("./AfterbyteMono-Regular.woff2") format("woff2"), url("./AfterbyteMono-Regular.woff") format("woff"), url("./AfterbyteMono-Regular.ttf") format("truetype"), url("./AfterbyteMono-Regular.otf") format("opentype");\n  font-weight: 400; font-style: normal; font-display: swap;\n}}\n')
    (out/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(out.glob('AfterbyteMono-Regular.*'))))
    print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--version',type=int,choices=[4,5],default=DEFAULT_VERSION);p.add_argument('--output',type=Path)
    args=p.parse_args();build(args.version,args.output)
