// Abre a versão web do jogo (pasta docs/) no Chromium, no tamanho de um iPad deitado, e fotografa
// tudo o que a criança vê: a abertura, o quarto, o mapa, os balões de escolher cômodo, cada cenário
// de ponta a ponta (rolando para o lado), o modo Decorar e a lojinha da Plantação.
//
// Uso:  node ferramentas/analise_design/capturar.js [tamanho] [pasta_saida]
//   tamanho: air (1180x820, padrão), mini (1133x744), pro (1366x1024) ou LARGURAxALTURA
//   pasta_saida: padrão analise_design/capturas/<tamanho>/ (fotos ficam fora do git)
// Também grava tempos.json (quanto demorou para abrir) e console.txt (mensagens do jogo).
// Só lê o jogo: não muda nada. Precisa do Playwright (já vem no ambiente da nuvem).
const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('playwright');

const RAIZ = path.resolve(__dirname, '..', '..');
const DOCS = path.join(RAIZ, 'docs');
const DADOS = path.join(RAIZ, 'prototipo', 'dados');
const TAMANHOS = { air: [1180, 820], mini: [1133, 744], pro: [1366, 1024] };

const arg = process.argv[2] || 'air';
const [W, H] = TAMANHOS[arg] || arg.split('x').map(Number);
const SAIDA = process.argv[3] || path.join(RAIZ, 'analise_design', 'capturas', arg);
fs.mkdirSync(SAIDA, { recursive: true });

// Interface: desenhada em 1600 x 1200 e esticada (stretch canvas_items + expand) a partir do canto.
const S = Math.min(W / 1600, H / 1200);
const ui = (x, y) => [x * S, y * S];
// Mapa: quadro de 1600 x 1200 centralizado na tela.
const MX = (W - 1600 * S) / 2, MY = (H - 1200 * S) / 2;
const mapa = (x, y) => [MX + x * S, MY + y * S];
// Cenário: altura 900 preenche a tela.
const Z = H / 900;

const md = JSON.parse(fs.readFileSync(path.join(DADOS, 'mapa_fazenda.json'), 'utf8'));
const centro = (lugar) => { const r = md.lugares[lugar].rect; return [r[0] + r[2] / 2, r[1] + r[3] / 2]; };
// Figurinhas dos balões (em coordenadas do mapa), medidas nas capturas de 15/11/2026.
const BALAO = {
  casa: { sede: [221, 316], sala: [414, 316], cozinha: [610, 316], quarto: [803, 316], quarto_carol: [1014, 316] },
  casa_arvore: { casa_arvore: [164, 110], casa_arvore_dentro: [357, 110] },
};
const largura = (cena) => {
  const f = path.join(DADOS, 'cenarios', cena + '.json');
  return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')).largura || 2200 : 2200;
};

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.wasm': 'application/wasm', '.pck': 'application/octet-stream',
  '.png': 'image/png', '.json': 'application/json' };
const servidor = http.createServer((req, res) => {
  const f = path.join(DOCS, decodeURIComponent(req.url.split('?')[0]).replace(/^\/$/, '/index.html'));
  if (!f.startsWith(DOCS) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise((ok) => servidor.listen(0, ok));
  const url = `http://localhost:${servidor.address().port}/index.html`;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const consoleLog = [];
  page.on('console', (m) => consoleLog.push(m.text()));
  const foto = async (nome) => { await page.screenshot({ path: path.join(SAIDA, nome + '.png') }); console.log('foto', nome); };
  const toque = async ([x, y], espera = 1500) => {
    await page.mouse.move(x, y); await page.mouse.down(); await page.waitForTimeout(80); await page.mouse.up();
    await page.waitForTimeout(espera);
  };
  const arrasta = async (x0, x1, y) => {
    await page.mouse.move(x0, y); await page.mouse.down();
    for (let i = 1; i <= 12; i++) { await page.mouse.move(x0 + (x1 - x0) * i / 12, y); await page.waitForTimeout(16); }
    await page.mouse.up(); await page.waitForTimeout(1500);
  };
  const ferradura = ui(18 + 70, 18 + 70);
  // poltrona do Decorar: embaixo da ferradura, com o vão definido em decoracao.gd (antes de 16/11/2026: y = 172)
  const deco = fs.readFileSync(path.join(RAIZ, 'prototipo', 'scripts', 'decoracao.gd'), 'utf8');
  const vao = deco.match(/BOTAO_VAO := ([\d.]+)/);
  const poltrona = ui(18 + 70, (vao ? 18 + 140 + Number(vao[1]) : 172) + 70);

  // Abertura e tempo até o primeiro quadro do quarto.
  const t0 = Date.now();
  await page.goto(url);
  await page.waitForSelector('canvas');
  await page.waitForTimeout(2500); await foto('00_abertura');
  await page.waitForTimeout(30000); await foto('01_quarto');
  const tempos = { abrir_ms_aprox: Date.now() - t0, nota: 'Chromium sem placa de vídeo: no iPad é diferente; serve para comparar versões.' };

  const f = md.ui.fechar;
  const fecharMapa = mapa(f[0] + f[2] / 2, f[1] + f[3] / 2);
  await toque(ferradura); await foto('02_mapa'); await toque(fecharMapa);
  for (const lugar of Object.keys(BALAO)) {
    await toque(ferradura); await toque(mapa(...centro(lugar))); await foto(`03_balao_${lugar}`); await toque(fecharMapa);
  }

  // Cada cenário: chega pelo mapa, fotografa a chegada, vai até a ponta esquerda e anda até a direita.
  const destinos = [];
  for (const lugar of md.ordem) {
    for (const [cena] of md.lugares[lugar].destinos) {
      const balao = BALAO[lugar];
      destinos.push({ lugar, cena, toques: balao ? [mapa(...centro(lugar)), mapa(...balao[cena])] : [mapa(...centro(lugar))] });
    }
  }
  let n = 10;
  for (const d of destinos) {
    await toque(ferradura);
    for (const t of d.toques) await toque(t);
    await page.waitForTimeout(1500);
    await foto(`${n}_${d.cena}_chegada`);
    const passo = W * 0.7;
    const telas = Math.ceil((largura(d.cena) * Z) / passo) + 1;
    for (let i = 0; i < telas; i++) await arrasta(W * 0.15, W * 0.85, H * 0.06);
    for (let i = 0; i < telas; i++) {
      await foto(`${n}_${d.cena}_parte${i + 1}`);
      await arrasta(W * 0.85, W * 0.15, H * 0.06);
    }
    if (d.cena === 'sala') { await toque(poltrona); await foto(`${n}_${d.cena}_decorar`); await toque(poltrona); }
    if (d.cena === 'plantacao') {
      // a câmera está na ponta direita: a banca (2530..2790, 770..940) abre a lojinha
      const esq = largura('plantacao') - W / Z;
      await toque([(2660 - esq) * Z, 830 * Z]); await foto(`${n}_${d.cena}_lojinha`);
      await toque([W - 60 * S, 60 * S]);
    }
    n++;
  }
  fs.writeFileSync(path.join(SAIDA, 'tempos.json'), JSON.stringify(tempos, null, 2));
  fs.writeFileSync(path.join(SAIDA, 'console.txt'), consoleLog.join('\n'));
  await browser.close();
  servidor.close();
  console.log('pronto:', SAIDA);
})().catch((e) => { console.error(e); process.exit(1); });
