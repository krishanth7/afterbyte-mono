import { filterGlyphs, unsupported, pageSlice } from './coverage.mjs';

const $ = id => document.getElementById(id);
const root = document.documentElement;
const sample = $('sample');
const samples = {
  interface: 'Build something\nworth reading.',
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
  document.querySelector('meta[name="theme-color"]').content = dark ? '#1b2022' : '#ededeb';
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
  $('inspector-code').textContent = codePoint(row) + ' / ' + row.origin;
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

// Explicit user-triggered simulation. Nothing here reports real telemetry.
let transmitting = false, transmissionStep = 0;
const messages = [
  '> CONNECTION ESTABLISHED', '> SENDING: HELLO, TOMORROW.',
  '> LATIN / GREEK / CYRILLIC: READY', '> OTF / TTF / WOFF / WOFF2: READY',
  '> TRANSMISSION COMPLETE. MAKE IT YOURS.'
];
let transmissionTimer;
function finishTransmission() {
  transmitting = false;
  clearInterval(transmissionTimer);
  $('transmission-state').textContent = 'COMPLETE';
  $('transmit').textContent = 'Transmit again →';
}
$('transmit').addEventListener('click', () => {
  if (transmitting) {
    transmitting = false;
    clearInterval(transmissionTimer);
    $('transmission-state').textContent = 'STOPPED';
    $('transmit').textContent = 'Restart transmission →';
    return;
  }
  $('transmission-log').textContent = '';
  transmissionStep = 0;
  if (motionStopped()) {
    $('transmission-log').textContent = messages.join('\n');
    finishTransmission();
    return;
  }
  transmitting = true;
  $('transmission-state').textContent = 'TRANSMITTING';
  $('transmit').textContent = 'Stop transmission';
  transmissionTimer = setInterval(() => {
    if (document.hidden || motionStopped()) return;
    $('transmission-log').textContent += (transmissionStep ? '\n' : '') + messages[transmissionStep++];
    if (transmissionStep === messages.length) finishTransmission();
  }, 550);
});
function updateClock() {
  if (document.hidden || motionStopped()) return;
  const now = new Date();
  $('utc-clock').dateTime = now.toISOString();
  $('utc-clock').textContent = now.toISOString().slice(11, 19);
}
// One initial reading remains useful when motion is reduced or paused.
const initialTime = new Date();
$('utc-clock').dateTime = initialTime.toISOString();
$('utc-clock').textContent = initialTime.toISOString().slice(11, 19);
setInterval(updateClock, 1000);
$('frequency').addEventListener('input', () => {
  const value = Number($('frequency').value);
  $('frequency-value').textContent = value + ' MHz';
  $('channel').textContent = 'CHANNEL ' + String(value).padStart(3, '0') + ' / LOCKED';
  document.querySelector('.radar-sweep').style.animationDuration = (20 - value / 10) + 's';
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
  document.querySelectorAll('.wire-object,.radar').forEach(element => ambient.observe(element));
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

// A short, bounded title effect; its accessible name stays unchanged.
const titleParts = [...document.querySelectorAll('h1>span:not(.title-space)')];
const titleText = titleParts.map(part => part.textContent);
let titleFrame = 0;
function restoreTitle() { titleParts.forEach((part, index) => { part.textContent = titleText[index]; }); }
if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.querySelector('h1').addEventListener('pointerenter', () => {
    if (motionStopped()) return;
    cancelAnimationFrame(titleFrame);
    const started = performance.now();
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let previousStep = -1;
    function tick(now) {
      const elapsed = now - started;
      if (elapsed >= 650 || motionStopped()) { restoreTitle(); return; }
      const step = Math.floor(elapsed / 65);
      if (step !== previousStep) {
        titleParts.forEach((part, index) => {
          part.textContent = [...titleText[index]].map((char, position) => position < step ? char : alphabet[Math.floor(Math.random() * alphabet.length)]).join('');
        });
        previousStep = step;
      }
      titleFrame = requestAnimationFrame(tick);
    }
    titleFrame = requestAnimationFrame(tick);
  });
}
