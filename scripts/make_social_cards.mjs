// Renders a 1200×630 share card for each post into images/social/<post file name>.png.
// _includes/meta.html uses the card when it exists and falls back to the site card.
// Usage: node scripts/make_social_cards.mjs [--all]
//   Without --all, only posts that have no card yet are rendered.
// Needs Playwright (npm i -g playwright) and Google Chrome, or Playwright's own
// Chromium (npx playwright install chromium).
import { readFileSync, readdirSync, existsSync, mkdirSync, unlinkSync } from 'node:fs';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';

const root = new URL('..', import.meta.url).pathname;
const postsDir = root + '_posts/';
const outDir = root + 'images/social/';
const all = process.argv.includes('--all');

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require('playwright');
} catch {
  playwright = createRequire(execSync('npm root -g').toString().trim() + '/')('playwright');
}

const NUMERALS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
const LABELS = ['Undergraduate Thesis'];
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function frontMatter(text) {
  const fm = {};
  const block = text.split(/^---\s*$/m)[1] || '';
  for (const line of block.split('\n')) {
    const m = line.match(/^([A-Za-z_]+):\s*(.*)$/);
    if (!m) continue;
    let v = m[2].trim();
    if (/^".*"$/.test(v)) v = v.slice(1, -1).replace(/\\"/g, '"');
    else if (/^'.*'$/.test(v)) v = v.slice(1, -1).replace(/''/g, "'");
    fm[m[1]] = v;
  }
  return fm;
}

// Same split as _includes/series-info.html
function parseTitle(title) {
  const plain = title.replace('Back-of-the-Envelope:', '').trim();
  const at = plain.indexOf(', Vol. ');
  if (at >= 0) {
    const series = plain.slice(0, at);
    const tail = plain.slice(at + ', Vol. '.length);
    const num = tail.split(':')[0].trim();
    return { series, num, chapter: tail.slice(tail.indexOf(':') + 1).trim(), label: '' };
  }
  for (const label of LABELS) {
    if (plain.startsWith(label + ':')) {
      return { series: '', num: '', chapter: plain.slice(label.length + 1).trim(), label };
    }
  }
  return { series: '', num: '', chapter: plain, label: '' };
}

// Curly quotes, as kramdown typesets them on the site
const smart = (s) =>
  s
    .replace(/([\p{L}\p{N}.,!?])'/gu, '$1\u2019')
    .replace(/'/g, '\u2018')
    .replace(/(^|[\s(])"/g, '$1\u201c')
    .replace(/"/g, '\u201d');
const esc = (s) => smart(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// "e^γ" in a chapter title reads better as a superscript
const titleHtml = (s) => esc(s).replace(/\^(\S)/g, '<sup>$1</sup>');

const posts = readdirSync(postsDir)
  .filter((f) => f.endsWith('.md'))
  .map((file) => {
    const fm = frontMatter(readFileSync(postsDir + file, 'utf8'));
    return { file, name: file.replace(/\.md$/, ''), fm, ...parseTitle(fm.title || '') };
  })
  .filter((p) => !p.fm.redirect_to && p.fm.title);

const volumes = {};
for (const p of posts) {
  if (p.series) (volumes[p.series] ||= new Set()).add(p.num);
}

// Drop cards whose post is gone or became a redirect
mkdirSync(outDir, { recursive: true });
const live = new Set(posts.map((p) => p.name + '.png'));
for (const f of readdirSync(outDir)) {
  if (f.endsWith('.png') && !live.has(f)) {
    unlinkSync(outDir + f);
    console.log('removed', f);
  }
}

const todo = posts.filter((p) => all || !existsSync(outDir + p.name + '.png'));
if (!todo.length) {
  console.log('All cards are up to date. Pass --all to render them again.');
  process.exit(0);
}

function cardHtml(p) {
  let kicker;
  let tiles = '';
  let desc = '';
  if (p.series) {
    kicker = `${esc(p.series)} <span class="dot">·</span> Vol. ${p.num}`;
    const vols = NUMERALS.filter((n) => volumes[p.series].has(n));
    tiles = `<div class="tiles">${vols
      .map((n) => `<span class="tile${n === p.num ? ' on' : ''}">${n}</span>`)
      .join('')}</div>`;
  } else {
    const [y, m] = String(p.fm.date).split('-');
    kicker = esc(p.label || `${MONTHS[+m - 1]} ${y}`);
    if (p.fm.description) desc = `<p class="desc">${esc(p.fm.description)}</p>`;
  }
  return `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=block">
<style>
  html, body { margin: 0; background: #000; }
  .card { position: relative; box-sizing: border-box; width: 1200px; height: 630px; padding: 80px 88px 0; overflow: hidden; }
  .kicker { margin: 0; font: 500 22px/1.4 'JetBrains Mono', monospace; letter-spacing: .09em; text-transform: uppercase; color: #4da3ff; }
  .dot { color: #4da3ff; }
  h1 { margin: 20px 0 0; font: 600 84px/1.06 'Source Serif 4', serif; font-optical-sizing: auto; letter-spacing: -.02em; color: #fff; }
  h1 sup { font-size: .55em; line-height: 0; }
  .desc { margin: 24px 0 0; max-width: 960px; font: 400 30px/1.42 'Source Serif 4', serif; color: #dcdde0;
          display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; }
  .tiles { position: absolute; left: 88px; bottom: 130px; display: flex; gap: 10px; }
  .tile { box-sizing: border-box; min-width: 70px; height: 70px; padding: 0 14px; display: flex; align-items: center; justify-content: center;
          border: 2px solid #3b3d43; font: 700 24px 'JetBrains Mono', monospace; letter-spacing: .06em; color: #fff; }
  .tile.on { background: #4da3ff; border-color: #4da3ff; color: #000; }
  .foot { position: absolute; left: 88px; right: 88px; bottom: 56px; display: flex; justify-content: space-between; align-items: baseline;
          font: 500 24px 'JetBrains Mono', monospace; color: #9c9ea6; }
  .foot b { font: 600 30px 'Source Serif 4', serif; color: #fff; }
</style></head><body>
<div class="card">
  <p class="kicker">${kicker}</p>
  <h1>${titleHtml(p.chapter)}</h1>
  ${desc}
  ${tiles}
  <div class="foot"><b>Julian Henry</b><span>juleshenry.github.io</span></div>
</div>
<script>
  // Shrink the title until it clears the tiles (or the footer), then trim the blurb
  document.fonts.ready.then(() => {
    const h1 = document.querySelector('h1');
    const desc = document.querySelector('.desc');
    const floor = (document.querySelector('.tiles') || document.querySelector('.foot')).getBoundingClientRect().top - 36;
    const bottom = () => (desc || h1).getBoundingClientRect().bottom;
    let size = 84;
    while (bottom() > floor && size > 52) h1.style.fontSize = (size -= 2) + 'px';
    for (let lines = 2; desc && bottom() > floor && lines > 0; lines--) desc.style.webkitLineClamp = lines;
    if (desc && bottom() > floor) desc.remove();
    document.body.dataset.ready = '1';
  });
</script>
</body></html>`;
}

let browser;
try {
  browser = await playwright.chromium.launch({ channel: 'chrome' });
} catch {
  browser = await playwright.chromium.launch();
}
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
for (const p of todo) {
  await page.setContent(cardHtml(p), { waitUntil: 'networkidle' });
  await page.waitForSelector('body[data-ready]');
  await page.locator('.card').screenshot({ path: outDir + p.name + '.png' });
  console.log('rendered', p.name);
}
await browser.close();
