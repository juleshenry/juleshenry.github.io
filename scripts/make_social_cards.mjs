// Renders a 1200×630 share card for each post into images/social/<post file name>.png,
// and one per series into images/social/series-<slug>.png (from _data/series.yml).
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

// The face in the card's footer, inlined so setContent needs no file access
const HEADSHOT = 'data:image/jpeg;base64,' + readFileSync(root + 'images/julian-headshot-square.jpg').toString('base64');
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

// Same as Jekyll's default slugify
const slugify = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '');

// Series landing pages: name, topic and blurb from _data/series.yml
const seriesCards = readFileSync(root + '_data/series.yml', 'utf8')
  .split(/^- /m)
  .slice(1)
  .map((entry) => {
    const field = (k) => {
      const m = entry.match(new RegExp(`^\\s*${k}:\\s*"?(.*?)"?\\s*$`, 'm'));
      return m ? m[1].replace(/\\"/g, '"') : '';
    };
    const series = field('name');
    return { kind: 'series', name: 'series-' + slugify(series), series, chapter: series, topic: field('topic'), blurb: field('blurb') };
  })
  .filter((c) => volumes[c.series]);

// The site's own card (home, Writing, Projects): name, tagline and bio from _config.yml,
// written to images/social-card.png
const config = readFileSync(root + '_config.yml', 'utf8');
const configField = (k) => (config.match(new RegExp(`^${k}:\\s*(.*)$`, 'm')) || [, ''])[1].trim();
const siteCard = { kind: 'site', name: '../social-card', chapter: configField('author'), topic: configField('tagline'), blurb: configField('bio') };

// Drop cards whose post is gone or became a redirect
mkdirSync(outDir, { recursive: true });
const cards = [...posts, ...seriesCards, siteCard];
const live = new Set(cards.map((p) => p.name + '.png'));
for (const f of readdirSync(outDir)) {
  if (f.endsWith('.png') && !live.has(f)) {
    unlinkSync(outDir + f);
    console.log('removed', f);
  }
}

const todo = cards.filter((p) => all || !existsSync(outDir + p.name + '.png'));
if (!todo.length) {
  console.log('All cards are up to date. Pass --all to render them again.');
  process.exit(0);
}

function cardHtml(p) {
  let kicker;
  let tiles = '';
  let desc = '';
  if (p.kind === 'site') {
    kicker = esc(p.topic);
    desc = `<p class="desc">${esc(p.blurb)}</p>`;
  } else if (p.kind === 'series') {
    const vols = NUMERALS.filter((n) => volumes[p.series].has(n));
    kicker = `${p.topic ? esc(p.topic) + ' <span class="dot">·</span> ' : ''}Series of ${vols.length}`;
    tiles = `<div class="tiles">${vols.map((n) => `<span class="tile">${n}</span>`).join('')}</div>`;
    if (p.blurb) desc = `<p class="desc">${esc(p.blurb)}</p>`;
  } else if (p.series) {
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=block">
<style>
  html, body { margin: 0; background: #fff; }
  .card { position: relative; box-sizing: border-box; width: 1200px; height: 630px; padding: 76px 88px 0 96px; overflow: hidden;
          font-family: 'Inter', system-ui, sans-serif; border-left: 12px solid #1d4ed8; }
  .kicker { margin: 0; font-size: 24px; font-weight: 700; line-height: 1.4; letter-spacing: .04em; text-transform: uppercase; color: #1d4ed8; }
  .dot { color: #1d4ed8; }
  h1 { margin: 18px 0 0; font-size: 80px; font-weight: 700; line-height: 1.08; letter-spacing: -.025em; color: #0f172a; }
  h1 sup { font-size: .55em; line-height: 0; }
  .desc { margin: 24px 0 0; max-width: 980px; font-size: 30px; line-height: 1.42; color: #334155;
          display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; }
  .tiles { position: absolute; left: 96px; bottom: 148px; display: flex; gap: 10px; }
  .tile { box-sizing: border-box; min-width: 72px; height: 52px; padding: 0 20px; display: flex; align-items: center; justify-content: center;
          border: 2px solid #cbd5e1; border-radius: 999px; font-size: 22px; font-weight: 700; color: #1f2937; }
  .tile.on { background: #1d4ed8; border-color: #1d4ed8; color: #fff; }
  .foot { position: absolute; left: 96px; right: 88px; bottom: 44px; display: flex; justify-content: space-between; align-items: center;
          padding-top: 24px; border-top: 2px solid #e5e7eb; font-size: 24px; color: #64748b; }
  .who { display: flex; align-items: center; gap: 18px; }
  .who img { width: 64px; height: 64px; border-radius: 50%; object-fit: cover; }
  .who b { font-size: 30px; font-weight: 700; color: #0f172a; }
</style></head><body>
<div class="card">
  <p class="kicker">${kicker}</p>
  <h1>${titleHtml(p.chapter)}</h1>
  ${desc}
  ${tiles}
  <div class="foot"><span class="who"><img src="${HEADSHOT}" alt=""><b>Julian Henry</b></span><span>juleshenry.github.io</span></div>
</div>
<script>
  // Shrink the title until it clears the tiles (or the footer), then trim the blurb
  document.fonts.ready.then(() => {
    const h1 = document.querySelector('h1');
    const desc = document.querySelector('.desc');
    const floor = (document.querySelector('.tiles') || document.querySelector('.foot')).getBoundingClientRect().top - 32;
    const bottom = () => (desc || h1).getBoundingClientRect().bottom;
    let size = 80;
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
