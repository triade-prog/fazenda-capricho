// Converte SVGs em PNG com fundo transparente usando o Chromium do Playwright.
// Uso: node ferramentas/svg_para_png.js <pasta_svg> <pasta_png> [escala_padrao=2]
// Peças pequenas (os dois lados <= 100 px) saem em 4x, como os objetos do quarto.
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [src, dst, esc = '2'] = process.argv.slice(2);
  fs.mkdirSync(dst, { recursive: true });
  const browser = await chromium.launch();
  const ctxs = {};
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.svg')).sort()) {
    const svg = fs.readFileSync(path.join(src, f), 'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    const w = +m[1], h = +m[2];
    const s = (w <= 100 && h <= 100) ? 4 : +esc;
    if (!ctxs[s]) ctxs[s] = await browser.newContext({ deviceScaleFactor: s });
    const page = await ctxs[s].newPage();
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await page.screenshot({ path: path.join(dst, f.replace('.svg', '.png')), omitBackground: true,
                            clip: { x: 0, y: 0, width: w, height: h } });
    await page.close();
  }
  await browser.close();
})();
