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

import {letterVariants} from '../web/coverage.mjs';
test('a exposes its real lowercase, capital, bold and italic Unicode forms',()=>{
 const variants=letterVariants(rows,'a');
 assert.deepEqual(variants.map(v=>v.row.unicode),[97,65,0x1d41a,0x1d44e,0x1d482,0x1d400,0x1d434,0x1d468]);
 assert.equal(variants[0].label,'Lowercase');
 assert.equal(variants[1].label,'Capital');
 assert.deepEqual(letterVariants(rows,'𝐀').map(v=>v.row.unicode),variants.map(v=>v.row.unicode));
});
test('variants handle the italic h alias and avoid inventing unsupported styles',()=>{
 assert.ok(letterVariants(rows,'h').some(v=>v.row.unicode===0x210e&&v.label==='Italic lowercase'));
 assert.equal(letterVariants(rows,'ℎ').length,8);
 assert.deepEqual(letterVariants(rows,'Ω').map(v=>v.row.unicode),[0x3c9,0x3a9]);
 assert.deepEqual(letterVariants(rows,'unknown'),[]);
});

import {keyboardLayout,keyOutput} from '../web/keyboard-layout.mjs';
test('ANSI keyboard has 104 unique nonoverlapping keys, including all function and numpad keys',()=>{
 assert.equal(keyboardLayout.length,104);assert.equal(new Set(keyboardLayout.map(k=>k.code)).size,104);
 for(let i=1;i<=12;i++)assert.ok(keyboardLayout.some(k=>k.code==='F'+i));
 assert.equal(keyboardLayout.filter(k=>k.code.startsWith('Numpad')||k.code==='NumLock').length,17);
 for(const [i,a] of keyboardLayout.entries())for(const b of keyboardLayout.slice(i+1)){
   assert.ok(!(a.x<b.x+b.w-.13&&a.x+a.w-.13>b.x&&a.y<b.y+b.h-.13&&a.y+a.h-.13>b.y),'Overlapping keys '+a.code+' and '+b.code);
 }
 const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
 assert.equal([...html.matchAll(/data-code="/g)].length,104);
 assert.equal([...html.matchAll(/data-link-code="/g)].length,104);
});
test('keyboard resolves Caps XOR Shift, shifted punctuation and Num Lock navigation',()=>{
 const key=code=>keyboardLayout.find(k=>k.code===code);
 assert.equal(keyOutput(key('KeyA')), 'a');
 assert.equal(keyOutput(key('KeyA'),{caps:true}), 'A');
 assert.equal(keyOutput(key('KeyA'),{shift:true}), 'A');
 assert.equal(keyOutput(key('KeyA'),{caps:true,shift:true}), 'a');
 assert.equal(keyOutput(key('Digit2'),{shift:true}), '@');
 assert.equal(keyOutput(key('Numpad7'),{num:false}), 'Home');
 assert.equal(keyOutput(key('Numpad7'),{num:true}), '7');
 assert.equal(keyOutput(key('Space')), ' ');
 assert.equal(keyOutput(key('NumpadEnter')), '\n');
});
