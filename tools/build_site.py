#!/usr/bin/env python3
"""Stage the public specimen with commit-versioned assets and no build dependencies."""
import argparse
import re
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def build(output,version):
    if not re.fullmatch(r'[A-Za-z0-9._-]{1,64}',version):raise ValueError('Invalid asset version')
    output=Path(output).resolve()
    if output==ROOT or not output.is_relative_to(ROOT/'build'):raise ValueError('Output must be inside the project build directory')
    if output.exists():shutil.rmtree(output)
    output.mkdir(parents=True)
    for name in ('index.html','robots.txt','sitemap.xml','OFL.txt'):
        shutil.copyfile(ROOT/name,output/name)
    for folder in ('web','assets','fonts'):
        shutil.copytree(ROOT/folder,output/folder)
    target=output/'sources/afterbyte-mono';target.mkdir(parents=True)
    shutil.copyfile(ROOT/'sources/afterbyte-mono/coverage-v5.json',target/'coverage-v5.json')
    (output/'.nojekyll').touch()
    index=output/'index.html';text=index.read_text()
    for asset in ('web/app.mjs','web/theme.js','web/style.css','fonts/afterbyte-mono/AfterbyteMono-Regular.woff2'):
        text=text.replace('"'+asset+'"','"'+asset+'?v='+version+'"')
    index.write_text(text)
    app=output/'web/app.mjs';app.write_text(app.read_text().replace("'./coverage.mjs'","'./coverage.mjs?v="+version+"'").replace("'./letter-lab.mjs'","'./letter-lab.mjs?v="+version+"'").replace("'sources/afterbyte-mono/coverage-v5.json'","'sources/afterbyte-mono/coverage-v5.json?v="+version+"'"))
    css=output/'web/style.css';css.write_text(css.read_text().replace('AfterbyteMono-Regular.woff2"','AfterbyteMono-Regular.woff2?v='+version+'"'))
    print(f'Staged specimen in {output.relative_to(ROOT)}; asset version {version}.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'build/site');parser.add_argument('--version',default='local')
    args=parser.parse_args();build(args.output,args.version)
