#!/usr/bin/env python3
"""Freeze selected OFL Noto source glyphs and explicit release coverage contracts."""
import hashlib
import json
import unicodedata as ud
import urllib.request
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'sources/upstream'
RAW=ROOT/'build/upstream/NotoSansMono.ttf'
PIN='097bc1b8c04c3224087c2ae95f7a923859b778cf'
EXPECTED='2cb2adb378a8f574213e23df697050b83c54c27df465a2015552740b2769a081'

def prepare():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True,exist_ok=True)
        url=f'https://raw.githubusercontent.com/google/fonts/{PIN}/ofl/notosansmono/NotoSansMono%5Bwdth%2Cwght%5D.ttf'
        RAW.write_bytes(urllib.request.urlopen(url,timeout=60).read())
    assert hashlib.sha256(RAW.read_bytes()).hexdigest()==EXPECTED
    font=TTFont(RAW)
    core={g['unicode'] for g in json.loads((ROOT/'sources/afterbyte-mono/vectors.json').read_text())['glyphs']}
    valid={n for n in font.getBestCmap() if ud.category(chr(n)) not in ('Cc','Cf','Cn','Co','Cs','Mn','Mc','Me','Zl','Zp')}
    blocks=[(0x20,0x24f),(0x370,0x52f),(0x2000,0x206f),(0x20a0,0x20cf),(0x2190,0x22ff),(0x2500,0x25ff)]
    braille=set(range(0x2800,0x2900))
    technical={0x220f,0x2211,0x222b}
    v4=core|{n for n in valid if any(a<=n<=b for a,b in blocks)}|braille|technical
    base=v4|{n for n in valid if (0x1e00<=n<=0x1fff or 0x2c60<=n<=0x2c7f or 0xa640<=n<=0xa69f) and n not in (0x1e9a,0x1e9b,0x1e9c)}
    math={n for n in range(0x1d400,0x1d49c) if ud.name(chr(n),'')}
    math|=set(range(0x1d7ce,0x1d7f6))|{0x210e,0x1d6c1}
    assert len(math)==197 and not base.intersection(math)
    v5=base|math
    assert len(v4)==1704 and len(v5)==2499 and v4<=v5
    donor=base-core-braille-technical
    # The mathematical italic h is generated from original h, not a donor glyph.
    for version,chars in [(4,v4),(5,v5)]:
        rows=[{'unicode':n,'name':ud.name(chr(n),'UNNAMED'),
               'origin':'afterbyte' if n in core else 'braille' if n in braille else 'mathematical-style' if n in math else 'technical' if n in technical else 'noto'} for n in sorted(chars)]
        contract={'version':f'{version}.0.0','glyph_count':len(chars)+1,'unicode_count':len(chars),
                  'unicode_database':ud.unidata_version,'glyphs':rows}
        (ROOT/f'sources/afterbyte-mono/coverage-v{version}.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
    font=instantiateVariableFont(font,{'wght':300,'wdth':100},inplace=True)
    options=subset.Options();options.layout_features=[];options.recalc_timestamp=False
    options.name_IDs=['*'];options.name_languages=['*'];options.notdef_outline=True
    sub=subset.Subsetter(options=options);sub.populate(unicodes=donor);sub.subset(font)
    font.recalcTimestamp=False;font['head'].created=font['head'].modified=3877286400
    path=UP/'NotoSansMono-ExpansionSource.ttf';font.save(path)
    info={'project':'Noto Sans Mono','upstream_version':'2.014','license':'OFL-1.1',
          'copyright':'Copyright 2022 The Noto Project Authors (https://github.com/notofonts/latin-greek-cyrillic)',
          'google_fonts_commit':PIN,'url':f'https://raw.githubusercontent.com/google/fonts/{PIN}/ofl/notosansmono/NotoSansMono%5Bwdth%2Cwght%5D.ttf',
          'download_sha256':EXPECTED,'subset_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'instance':{'wght':300,'wdth':100},'subset_unicode_count':len(donor),
          'changes':'Static Light instance; subset to the selected spacing characters; layout features dropped. Used as licensed glyph source, not shipped as an unmodified Noto font.'}
    (UP/'provenance.json').write_text(json.dumps(info,indent=2)+'\n')
    print(f'Frozen {len(donor)} licensed source mappings; v4={len(v4)+1}, v5={len(v5)+1} glyphs.')

if __name__=='__main__':prepare()
