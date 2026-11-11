import{test}from'node:test';import assert from'node:assert/strict';import{readFileSync}from'node:fs';import{filterGlyphs,groupOf,unsupported,pageSlice}from'../web/coverage.mjs';
const data=JSON.parse(readFileSync(new URL('../sources/afterbyte-mono/coverage-v5.json',import.meta.url)));const rows=data.glyphs;
test('coverage browser accounts for all 2499 mappings in disjoint groups',()=>{const counts={};for(const r of rows){const key=groupOf(r);counts[key]=(counts[key]||0)+1}assert.deepEqual(counts,{ascii:95,latin:716,greek:354,cyrillic:377,symbols:504,math:197,braille:256});assert.equal(rows.length,2499)});
test('search handles supplementary code points and Greek characters',()=>{assert.equal(filterGlyphs(rows,'U+1D400')[0].unicode,0x1d400);assert.equal(filterGlyphs(rows,'0x03A9')[0].unicode,0x3a9);assert.equal(filterGlyphs(rows,'Ω')[0].unicode,0x3a9);assert.ok(filterGlyphs(rows,'CYRILLIC').length>300);assert.equal(filterGlyphs(rows,'U+1D400','greek').length,0)});
test('fallback warning handles astral characters, combining marks and line breaks',()=>{assert.deepEqual(unsupported('Hello Ω Ж\n𝐀',rows),[]);assert.deepEqual(unsupported('a\u0301',rows),[0x301]);assert.deepEqual(unsupported('😀😀',rows),[0x1f600])});
test('pagination covers every glyph once and handles empty results',()=>{const seen=[];for(let p=0;p<35;p++)seen.push(...pageSlice(rows,p).rows.map(r=>r.unicode));assert.equal(seen.length,2499);assert.equal(new Set(seen).size,2499);assert.equal(pageSlice([],99).index,0);assert.equal(pageSlice(rows,999).index,34)});

test('public page has unique IDs, valid section anchors and resolvable local assets',()=>{
  const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(ids.length,new Set(ids).size,'Duplicate element ID');
  for(const match of html.matchAll(/href="#([^"]+)"/g))assert.ok(ids.includes(match[1]),'Missing anchor '+match[1]);
  for(const match of html.matchAll(/(?:src|href)="([^"#]+)"/g)){
    if(/^(https?:|data:)/.test(match[1]))continue;
    assert.doesNotThrow(()=>readFileSync(new URL('../'+match[1],import.meta.url)),match[1]);
  }
});
test('all static page text and script symbols belong to the font repertoire',()=>{
  const known=new Set(rows.map(r=>r.unicode));
  const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
  const body=html.slice(html.indexOf('<body>')).replace(/<[^>]*>/g,'').replace(/&(?:amp|lt|gt|quot|apos);/g,'');
  const app=readFileSync(new URL('../web/app.mjs',import.meta.url),'utf8');
  for(const character of body+app){const point=character.codePointAt(0);if(point>127&&!/\s/.test(character))assert.ok(known.has(point),'Unsupported static character '+character);}
});
