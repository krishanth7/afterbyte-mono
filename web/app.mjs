import { filterGlyphs, unsupported, pageSlice } from './coverage.mjs';

const $ = id => document.getElementById(id);
const root = document.documentElement;
const sample = $('sample');
const samples = {
  interface: 'Consider every\ncharacter.',
  latin: 'ÀÁÂÃÄÅ ÆÇÈÉÊË Œ Ø ß\nŁąę ěŷ Ḃẞ — clarity, in detail.',
  greek: 'ΑΒΓΔΕΖΗΘ ΙΚΛΜΝΞΟΠ\nΡΣΤΥΦΧΨΩ αβγδελπ ἀὦ',
  cyrillic: 'АБВГДЕЁЖЗИЙКЛМН\nОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
  math: '∑ ∏ ∫ ∞ ≠ ≤ ≥ ± × ÷\n𝐀𝐁𝐂 𝑥𝑦𝑧 𝒂𝒃𝒄 𝟘𝟙𝟚',
  braille: '⠁ ⠃ ⠉ ⠙ ⠑ ⠋ ⠛ ⠓\n⠿ ⡿ ⢿ ⣀ ⣤ ⣶ ⣿'
};
const storage = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch { /* Private sessions still work. */ } }
};
const systemTheme = matchMedia('(prefers-color-scheme: dark)');
function syncTheme() {
  const dark = root.dataset.theme === 'dark';
  $('theme').setAttribute('aria-pressed', String(dark));
  $('theme').textContent = dark ? 'Light mode' : 'Dark mode';
  const preview = $('download-preview');
  if (preview) preview.href = 'assets/afterbyte-mono/website-preview-' + (dark ? 'dark' : 'light') + '.png';
  document.querySelector('meta[name="theme-color"]').content = dark ? '#10151e' : '#f7f8fa';
}
syncTheme();
let themeTimer;
$('theme').addEventListener('click', () => {
  root.classList.add('theme-changing');
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  storage.set('afterbyte-theme', root.dataset.theme);
  syncTheme();
  clearTimeout(themeTimer);
  themeTimer = setTimeout(() => root.classList.remove('theme-changing'), 500);
});
systemTheme.addEventListener('change', event => {
  if (!storage.get('afterbyte-theme')) {
    root.dataset.theme = event.matches ? 'dark' : 'light';
    syncTheme();
  }
});

// A single motion preference controls every ambient effect and live readout.
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let userPaused = storage.get('afterbyte-motion') === 'paused';
const motionStopped = () => userPaused || reducedMotion.matches;
function syncMotion() {
  root.classList.toggle('motion-paused', motionStopped());
  $('motion').setAttribute('aria-pressed', String(motionStopped()));
  $('motion').textContent = reducedMotion.matches ? 'Reduced motion' : userPaused ? 'Resume motion' : 'Pause motion';
  $('motion').disabled = reducedMotion.matches;
}
syncMotion();
reducedMotion.addEventListener('change', syncMotion);
$('motion').addEventListener('click', () => {
  userPaused = !userPaused;
  storage.set('afterbyte-motion', userPaused ? 'paused' : 'running');
  syncMotion();
});

// Native inputs preserve keyboard behavior, text selection, and mobile editing.
let rows = [], page = 0;
let selected = { unicode: 65, name: 'LATIN CAPITAL LETTER A', origin: 'afterbyte' };
const setPressed = (selector, predicate) => document.querySelectorAll(selector).forEach(button => {
  button.setAttribute('aria-pressed', String(predicate(button)));
});
function updateControls() {
  sample.style.fontSize = $('size').value + 'px';
  sample.style.letterSpacing = $('tracking').value + 'px';
  sample.style.lineHeight = $('leading').value;
  $('size-value').textContent = $('size').value + ' px';
  $('tracking-value').textContent = $('tracking').value + ' px';
  $('leading-value').textContent = Number($('leading').value).toFixed(2);
}
function reportText() {
  if (!rows.length) return;
  const missing = unsupported(sample.value, rows);
  $('text-status').textContent = missing.length
    ? 'Fallback needed for ' + missing.slice(0, 12).map(n => 'U+' + n.toString(16).toUpperCase()).join(', ') + (missing.length > 12 ? ' and more.' : '.')
    : 'All specimen characters are covered. Your text stays in this page.';
}
for (const id of ['size', 'tracking', 'leading']) $(id).addEventListener('input', updateControls);
document.querySelectorAll('[data-sample]').forEach(button => button.addEventListener('click', () => {
  sample.value = samples[button.dataset.sample];
  setPressed('[data-sample]', b => b === button);
  reportText();
}));
sample.addEventListener('input', () => {
  setPressed('[data-sample]', () => false);
  reportText();
});
document.querySelectorAll('[data-align]').forEach(button => button.addEventListener('click', () => {
  sample.style.textAlign = button.dataset.align;
  setPressed('[data-align]', b => b === button);
}));
function resetSpecimen() {
  sample.value = samples.interface;
  $('size').value = innerWidth < 701 ? 36 : 64;
  $('tracking').value = 0;
  $('leading').value = 1.4;
  sample.style.textAlign = 'left';
  setPressed('[data-align]', b => b.dataset.align === 'left');
  setPressed('[data-sample]', b => b.dataset.sample === 'interface');
  updateControls();
  reportText();
}
$('reset').addEventListener('click', resetSpecimen);
resetSpecimen();
document.fonts.load('24px "Afterbyte Mono"').then(faces => {
  $('font-status').textContent = faces.length && document.fonts.check('24px "Afterbyte Mono"')
    ? 'Afterbyte Mono loaded · v5.0.0' : 'Font unavailable — displaying a fallback.';
}).catch(() => { $('font-status').textContent = 'Font unavailable. Font downloads remain available.'; });

const codePoint = row => 'U+' + row.unicode.toString(16).toUpperCase().padStart(4, '0');
function inspect(row) {
  clearTimeout(insertTimer);
  $('insert-glyph').textContent = 'Add to tester +';
  selected = row;
  $('inspector-letter').textContent = String.fromCodePoint(row.unicode);
  $('inspector-name').textContent = row.name;
  $('inspector-code').textContent = codePoint(row) + ' / ADVANCE 650';
  $('insert-status').textContent = '';
  setPressed('.glyph', button => Number(button.dataset.unicode) === row.unicode);
}
function render() {
  const result = pageSlice(filterGlyphs(rows, $('query').value, $('group').value), page);
  page = result.index;
  const fragment = document.createDocumentFragment();
  for (const row of result.rows) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'glyph';
    button.dataset.unicode = String(row.unicode);
    button.setAttribute('aria-label', 'Inspect ' + row.name + ' (' + codePoint(row) + ')');
    button.setAttribute('aria-pressed', String(row.unicode === selected.unicode));
    button.title = codePoint(row) + ' · ' + row.name;
    const character = document.createElement('span');
    character.setAttribute('aria-hidden', 'true');
    character.textContent = String.fromCodePoint(row.unicode);
    const label = document.createElement('small');
    label.textContent = codePoint(row);
    button.append(character, label);
    button.addEventListener('click', () => inspect(row));
    fragment.append(button);
  }
  $('glyph-grid').replaceChildren(fragment);
  $('coverage-status').textContent = result.total
    ? result.total.toLocaleString() + (result.total === 1 ? ' matching character' : ' matching characters') + ' · select a character to inspect.'
    : 'No matching characters. Try another name, code point or group.';
  $('page-label').textContent = 'Page ' + (page + 1) + ' of ' + result.pages;
  $('previous').disabled = page === 0;
  $('next').disabled = page >= result.pages - 1;
}
for (const id of ['query', 'group']) $(id).addEventListener(id === 'query' ? 'input' : 'change', () => { page = 0; render(); });
$('previous').addEventListener('click', () => { page--; render(); });
$('next').addEventListener('click', () => { page++; render(); });
$('insert-glyph').addEventListener('click', () => {
  const char = String.fromCodePoint(selected.unicode);
  if (sample.value.length + char.length > sample.maxLength) {
    $('insert-status').textContent = 'The tester is full. Remove some text before adding a character.';
    return;
  }
  sample.value += char;
  setPressed('[data-sample]', () => false);
  reportText();
  $('insert-status').textContent = codePoint(selected) + ' added to the type tester.';
  $('insert-glyph').textContent = 'Added to tester ✓';
  clearTimeout(insertTimer);
  insertTimer = setTimeout(() => { $('insert-glyph').textContent = 'Add to tester +'; }, 1500);
});
let insertTimer;
fetch('sources/afterbyte-mono/coverage-v5.json').then(response => {
  if (!response.ok) throw Error('Coverage request failed');
  return response.json();
}).then(data => {
  if (data.unicode_count !== 2499 || data.glyphs.length !== 2499) throw Error('Invalid character index');
  rows = data.glyphs;
  render();
  reportText();
}).catch(() => {
  $('coverage-status').textContent = 'Character index unavailable. Use the full coverage list linked above.';
  $('previous').disabled = $('next').disabled = true;
});

async function copy(text, status, message) {
  try { await navigator.clipboard.writeText(text); $(status).textContent = message; }
  catch { $(status).textContent = 'Clipboard unavailable. Select and copy the text manually.'; }
}
$('copy-css').addEventListener('click', () => copy($('css-example').textContent, 'copy-status', 'CSS copied. Place the font file beside your stylesheet.'));
$('copy-link').addEventListener('click', () => copy(new URL('./', location.href).href, 'share-status', 'Site link copied. Your specimen text is not included.'));

// Transform-only ambient motion. No scroll hijacking or hidden page content.
if ('IntersectionObserver' in window) {
  const ambient = new IntersectionObserver(entries => {
    for (const entry of entries) entry.target.classList.toggle('offscreen', !entry.isIntersecting);
  }, { rootMargin: '100px' });
  document.querySelectorAll('.hero-diagram,.anatomy-art,.closing-graphic').forEach(element => ambient.observe(element));
  const reveals = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      entry.target.classList.add('reveal');
      reveals.unobserve(entry.target);
    }
  }, { threshold: .1 });
  document.querySelectorAll('.type-line,.section-head').forEach(element => reveals.observe(element));
}
let scrollQueued = false;
function progress() {
  const max = root.scrollHeight - innerHeight;
  document.querySelector('.reading-progress').style.transform = 'scaleX(' + (max > 0 ? Math.min(1, scrollY / max) : 0) + ')';
  scrollQueued = false;
}
addEventListener('scroll', () => {
  if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(progress); }
}, { passive: true });
addEventListener('resize', progress);
progress();


// Local application studies show the same typeface in three different contexts.
const previewNames={interface:'AFTERBYTE / INTERFACE STUDY',code:'AFTERBYTE / CODE STUDY',editorial:'AFTERBYTE / EDITORIAL STUDY'};
document.querySelectorAll('[data-preview]').forEach(button=>button.addEventListener('click',()=>{
  const name=button.dataset.preview;
  for(const key of Object.keys(previewNames)) $('preview-'+key).hidden=key!==name;
  setPressed('[data-preview]',b=>b===button);
  $('preview-title').textContent=previewNames[name];
}));
function groupState(){setPressed('[data-group]',button=>button.dataset.group===$('group').value);}
document.querySelectorAll('[data-group]').forEach(button=>button.addEventListener('click',()=>{
  $('group').value=button.dataset.group;
  $('query').value='';page=0;groupState();render();
}));
$('group').addEventListener('change',groupState);
groupState();
