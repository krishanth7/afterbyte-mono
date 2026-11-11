export function groupOf(row){const n=row.unicode;if(n<128)return'ascii';if(n<=0x24f||n>=0x1e00&&n<=0x1eff||n>=0x2c60&&n<=0x2c7f)return'latin';if(n>=0x370&&n<=0x3ff||n>=0x1f00&&n<=0x1fff)return'greek';if(n>=0x400&&n<=0x52f||n>=0xa640&&n<=0xa69f)return'cyrillic';if(n>=0x2800&&n<=0x28ff)return'braille';if(row.origin==='mathematical-style')return'math';return'symbols'}
export function filterGlyphs(rows,query='',group='all'){const raw=query.trim(),q=raw.toUpperCase(),single=[...raw].length===1;const cp=/^(?:U\+|0X)([0-9A-F]{1,6})$/.exec(q);return rows.filter(r=>(group==='all'||groupOf(r)===group)&&(!q||(cp?r.unicode===parseInt(cp[1],16):single?r.unicode===raw.codePointAt(0):r.name.toUpperCase().includes(q))))}
export function unsupported(text,rows){const known=new Set(rows.map(r=>r.unicode));return [...new Set([...text].map(c=>c.codePointAt(0)))].filter(n=>n!==10&&n!==13&&n!==9&&!known.has(n))}
export function pageSlice(rows,page,size=72){const pages=Math.max(1,Math.ceil(rows.length/size));const index=Math.max(0,Math.min(page,pages-1));return{rows:rows.slice(index*size,(index+1)*size),index,pages,total:rows.length}}

// Return real encoded forms present in this font, never synthetic CSS weights.
export function letterVariants(rows, value){
  const input=typeof value==='string'?value:String.fromCodePoint(value.unicode);
  if([...input].length!==1)return[];
  const exact=rows.find(row=>row.unicode===input.codePointAt(0));
  const name=exact?.name||'';
  const ascii=input.codePointAt(0)===0x210e?'H':/^[a-z]$/i.test(input)?input.toUpperCase():/(?:CAPITAL|SMALL) ([A-Z])$/.exec(name)?.[1];
  if(ascii){
    const definitions=[
      ['Lowercase','LATIN SMALL LETTER '+ascii],['Capital','LATIN CAPITAL LETTER '+ascii],
      ['Bold lowercase','MATHEMATICAL BOLD SMALL '+ascii],['Italic lowercase','MATHEMATICAL ITALIC SMALL '+ascii],
      ['Bold italic lowercase','MATHEMATICAL BOLD ITALIC SMALL '+ascii],['Bold capital','MATHEMATICAL BOLD CAPITAL '+ascii],
      ['Italic capital','MATHEMATICAL ITALIC CAPITAL '+ascii],['Bold italic capital','MATHEMATICAL BOLD ITALIC CAPITAL '+ascii]
    ];
    return definitions.flatMap(([label,target])=>{const row=rows.find(item=>item.name===target)||(target==='MATHEMATICAL ITALIC SMALL H'?rows.find(item=>item.unicode===0x210e):undefined);return row?[{label,row}]:[]});
  }
  const values=[...new Set([input.toLowerCase(),input.toUpperCase()])].filter(char=>[...char].length===1);
  return values.flatMap(char=>{const row=rows.find(item=>item.unicode===char.codePointAt(0));return row?[{label:char===char.toUpperCase()?'Capital':'Lowercase',row}]:[]});
}
