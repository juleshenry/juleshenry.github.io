// Generates _includes/wasm-fft-vs-v8.svg from the intersekt research results.
// Usage: node scripts/wasm-fft-chart.mjs <path/to/intersekt/research/results>
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const dir = process.argv[2];
const tsv = (f) => {
  const [head, ...rows] = readFileSync(join(dir, f), 'utf8').trim().split('\n');
  const cols = head.split('\t');
  return rows.map((r) => Object.fromEntries(r.split('\t').map((v, i) => [cols[i], v])));
};
const final = tsv('final.tsv');
const old = tsv('old.tsv');

const series = [
  { name: 'V8 BigInt', color: '#3987e5', pts: final.map((r) => [+r.limbs32, +r.v8_us]) },
  { name: 'WASM FFT', color: '#d95926', pts: final.map((r) => [+r.limbs32, +r.fft_us]) },
  { name: 'WASM Karatsuba (rebuilt)', color: '#199e70', pts: final.map((r) => [+r.limbs32, +r.kara_us]) },
  { name: 'Wasmatsuba Karatsuba (fixed)', color: '#c98500', pts: old.map((r) => [+r.limbs32, +r.old_kara_us]) },
];

const W = 760, H = 480, L = 70, R = 190, T = 24, B = 56;
const x0 = Math.log10(8), x1 = Math.log10(1048576), y0 = -2, y1 = 7;
const sx = (v) => L + ((Math.log10(v) - x0) / (x1 - x0)) * (W - L - R);
const sy = (v) => H - B - ((Math.log10(v) - y0) / (y1 - y0)) * (H - T - B);
const f = (n) => n.toFixed(1);

const bits = (limbs) => {
  const b = limbs * 32;
  if (b >= 1 << 20) return `${+(b / (1 << 20)).toFixed(1)} Mbit`;
  if (b >= 1024) return `${+(b / 1024).toFixed(1)} kbit`;
  return `${b} bit`;
};
const time = (us) =>
  us >= 1e6 ? `${+(us / 1e6).toPrecision(3)} s`
  : us >= 1e3 ? `${+(us / 1e3).toPrecision(3)} ms`
  : us >= 1 ? `${+us.toPrecision(3)} µs`
  : `${+(us * 1e3).toPrecision(3)} ns`;

const out = [];
out.push(`<svg class="wasm-fft-chart" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="wfc-title wfc-desc" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-width:${W}px;display:block;margin:16px auto;font-family:inherit">`);
out.push(`<rect width="${W}" height="${H}" rx="8" fill="#121212"/>`);
out.push(`<title id="wfc-title">Multiply time vs operand size, log-log</title>`);
out.push(`<desc id="wfc-desc">V8 BigInt, WASM FFT, rebuilt WASM Karatsuba and the fixed Wasmatsuba Karatsuba, 8 to 1,048,576 32-bit limbs. WASM FFT crosses below V8 near 16 kbit and stays below.</desc>`);

// Grid + y axis (one line per decade)
const yLabels = ['10 ns', '100 ns', '1 µs', '10 µs', '100 µs', '1 ms', '10 ms', '100 ms', '1 s', '10 s'];
for (let e = y0; e <= y1; e++) {
  const y = sy(10 ** e);
  out.push(`<line x1="${L}" x2="${W - R}" y1="${f(y)}" y2="${f(y)}" stroke="#2a2a2a" stroke-width="1"/>`);
  out.push(`<text x="${L - 8}" y="${f(y + 4)}" text-anchor="end" font-size="11" fill="#c3c2b7">${yLabels[e - y0]}</text>`);
}
// x axis: every 8x in limbs
for (let limbs = 8; limbs <= 1048576; limbs *= 8) {
  const x = sx(limbs);
  out.push(`<line x1="${f(x)}" x2="${f(x)}" y1="${T}" y2="${H - B}" stroke="#2a2a2a" stroke-width="1"/>`);
  out.push(`<text x="${f(x)}" y="${H - B + 18}" text-anchor="middle" font-size="11" fill="#c3c2b7">${bits(limbs)}</text>`);
}
out.push(`<text x="${(L + W - R) / 2}" y="${H - 12}" text-anchor="middle" font-size="12" fill="#e0e0e0">Operand size (log scale)</text>`);
out.push(`<text transform="translate(16 ${(T + H - B) / 2}) rotate(-90)" text-anchor="middle" font-size="12" fill="#e0e0e0">Time per multiply (log scale)</text>`);

// Crossover marker: first size from which FFT stays below V8
const v8 = series[0].pts, fft = series[1].pts;
const cross = fft.findIndex((_, i) => fft.slice(i).every(([, t], j) => t < v8[i + j][1]));
const cx = sx(fft[cross][0]);
out.push(`<line x1="${f(cx)}" x2="${f(cx)}" y1="${T}" y2="${H - B}" stroke="#e0e0e0" stroke-width="1" stroke-dasharray="3 4" opacity="0.6"/>`);
out.push(`<text x="${f(cx + 6)}" y="${T + 14}" font-size="11" fill="#e0e0e0">FFT passes V8 at ${bits(fft[cross][0])}</text>`);

// Lines, points (native tooltips), direct labels at line ends
const ends = [];
for (const s of series) {
  const d = s.pts.map(([n, t], i) => `${i ? 'L' : 'M'}${f(sx(n))},${f(sy(t))}`).join('');
  out.push(`<path d="${d}" fill="none" stroke="${s.color}" stroke-width="2" stroke-linejoin="round"/>`);
  for (const [n, t] of s.pts) {
    out.push(`<circle cx="${f(sx(n))}" cy="${f(sy(t))}" r="2.5" fill="${s.color}"><title>${s.name}: ${time(t)} at ${bits(n)} (${n.toLocaleString('en-US')} limbs)</title></circle>`);
  }
  const [n, t] = s.pts.at(-1);
  if (n < 1048576) {
    // Series that stops early: label above-left of its last point, clear of the lines below
    out.push(`<text x="${f(sx(n) - 6)}" y="${f(sy(t) - 10)}" text-anchor="end" font-size="12" fill="#e0e0e0">${s.name}</text>`);
  } else ends.push({ s, x: sx(n), y: sy(t) });
}
// De-collide end labels vertically
ends.sort((a, b) => a.y - b.y);
for (let i = 1; i < ends.length; i++) ends[i].ly = Math.max(ends[i].y, (ends[i - 1].ly ?? ends[i - 1].y) + 16);
ends[0].ly = ends[0].y;
for (const e of ends) {
  out.push(`<circle cx="${f(e.x + 10)}" cy="${f(e.ly)}" r="4" fill="${e.s.color}"/>`);
  out.push(`<text x="${f(e.x + 18)}" y="${f(e.ly + 4)}" font-size="12" fill="#e0e0e0">${e.s.name}</text>`);
}
out.push('</svg>');

writeFileSync(new URL('../_includes/wasm-fft-vs-v8.svg', import.meta.url), out.join('\n') + '\n');
console.log(`crossover at ${fft[cross][0]} limbs (${bits(fft[cross][0])})`);
