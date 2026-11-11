#!/usr/bin/env python3
"""Validate versioned coverage, licensed provenance, all containers and rendering."""
import argparse,hashlib,io,json,unicodedata as ud
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from PIL import ImageFont
import uharfbuzz as hb
ROOT=Path(__file__).resolve().parents[1]

def validate(version=5,directory=None):
    directory=Path(directory) if directory else ROOT/'fonts/afterbyte-mono'
    contract=json.loads((ROOT/f'sources/afterbyte-mono/coverage-v{version}.json').read_text())
    chars={g['unicode'] for g in contract['glyphs']};expected={4:(1705,1704),5:(2500,2499)}[version]
    assert (contract['glyph_count'],len(chars))==expected
    assert all(ud.category(chr(c)) not in ('Co','Cs','Cn','Cc','Cf','Mn','Mc','Me') for c in chars)
    license=(ROOT/'OFL.txt').read_text()
    assert (ROOT/'LICENSE').read_text()==license==(directory/'LICENSE.txt').read_text()
    assert 'The Noto Project Authors' in license
    fonts={ext:TTFont(directory/f'AfterbyteMono-Regular.{ext}',checkChecksums=2) for ext in ('ttf','otf','woff','woff2')}
    t=fonts['ttf'];cmap=t.getBestCmap();assert set(cmap)==chars and len(set(cmap.values()))==len(chars)
    assert len(t.getGlyphOrder())==expected[0] and t.getGlyphOrder()[0]=='.notdef'
    core=TTFont(ROOT/'build/core/AfterbyteMono-Regular.ttf')
    assert set(core.getBestCmap())<=chars
    for c,name in core.getBestCmap().items():
        a=core['glyf'][name].getCoordinates(core['glyf']);b=t['glyf'][cmap[c]].getCoordinates(t['glyf'])
        assert list(a[0])==list(b[0]) and list(a[1])==list(b[1]),f'Original glyph changed U+{c:04X}'
    assert set(range(0x2800,0x2900))<=chars
    for c in range(0x2800,0x2900):assert t['glyf'][cmap[c]].numberOfContours==(c-0x2800).bit_count()
    if version==5:
        v4=json.loads((ROOT/'sources/afterbyte-mono/coverage-v4.json').read_text())
        assert {g['unicode'] for g in v4['glyphs']}<=chars
        for c,base in [(0x1d400,'A'),(0x1d434,'A'),(0x1d7ce,'0'),(0x1d7d8,'0')]:
            a=t['glyf'][cmap[c]].getCoordinates(t['glyf']);b=t['glyf'][cmap[ord(base)]].getCoordinates(t['glyf'])
            assert list(a[0])!=list(b[0]),f'Undifferentiated math style U+{c:04X}'
    signatures={'ttf':b'\x00\x01\x00\x00','otf':b'OTTO','woff':b'wOFF','woff2':b'wOF2'}
    for ext,font in fonts.items():
        assert (directory/f'AfterbyteMono-Regular.{ext}').read_bytes()[:4]==signatures[ext]
        assert len(font.getGlyphOrder())==expected[0] and font.getBestCmap()==cmap
        assert font['name'].getDebugName(5)==f'Version {version}.000'
        assert font['name'].getDebugName(13)==license and font['name'].getDebugName(14)=='https://openfontlicense.org'
        assert all(a==650 for a,b in font['hmtx'].metrics.values()) and font['post'].isFixedPitch
        assert (font['hhea'].ascent,font['hhea'].descent)==(1280,-450)
        gs=font.getGlyphSet();ref=t.getGlyphSet()
        for c,name in cmap.items():
            p=BoundsPen(gs);gs[name].draw(p);q=BoundsPen(ref);ref[name].draw(q)
            if p.bounds is not None:
                assert q.bounds is not None and max(abs(a-b) for a,b in zip(p.bounds,q.bounds))<1.1,(ext,c)
                assert 0<=p.bounds[0]<p.bounds[2]<=650 and -450<=p.bounds[1]<p.bounds[3]<=1280
            else:assert ud.category(chr(c))=='Zs' or c==0x2800,('Unexpected blank glyph',ext,hex(c))
            if ext in ('woff','woff2'):
                a=t['glyf'][name].getCoordinates(t['glyf']);b=font['glyf'][name].getCoordinates(font['glyf'])
                assert list(a[0])==list(b[0]) and list(a[1])==list(b[1])
        font.flavor=None;buf=io.BytesIO();font.save(buf);data=buf.getvalue();hf=hb.Font(hb.Face(data))
        # Shape each assigned code point independently: no script or bidi mixing artifacts.
        for c in sorted(chars):
            b=hb.Buffer();b.add_str(chr(c));b.guess_segment_properties();hb.shape(hf,b)
            assert len(b.glyph_infos)==1 and b.glyph_infos[0].codepoint!=0 and b.glyph_positions[0].x_advance==650,(ext,c)
        for size in (12,24,48):
            face=ImageFont.truetype(io.BytesIO(data),size)
            for c in chars:
                assert abs(face.getlength(chr(c))-size*.65)<.03,(ext,c,size)
                if ud.category(chr(c))!='Zs' and c!=0x2800:assert face.getmask(chr(c)).getbbox() is not None,(ext,c,size)
    for row in (directory/'SHA256SUMS').read_text().splitlines():
        digest,name=row.split();assert hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest
    print(f'PASS v{version}: {expected[0]} glyphs / {expected[1]} mappings; retained original outlines; complete Braille bits; four formats; licenses; bounds; shaping every character; 3-size raster checks; checksums.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--version',type=int,choices=[4,5],default=5);p.add_argument('--directory',type=Path)
    args=p.parse_args();validate(args.version,args.directory)
