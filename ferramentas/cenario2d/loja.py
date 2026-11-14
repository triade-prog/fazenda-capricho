"""Lojinha de enfeites da fazenda: enfeites que a criança compra com ferradurinhas e o botão da lojinha.

Gera arte/interface/loja/*.png e copia para prototipo/assets/loja/. Peças 2D provisórias: quando a
arte 3D chegar, é só trocar os PNGs (mesmos nomes e proporções). Preços e níveis ficam em
prototipo/dados/fazendinha.json ("loja").
Uso: python3 ferramentas/cenario2d/loja.py
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, salvar  # noqa: E402

raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dest = os.path.join(raiz, "arte/interface/loja")
jogo = os.path.join(raiz, "prototipo/assets/loja")
os.makedirs(dest, exist_ok=True)
os.makedirs(jogo, exist_ok=True)
P = {}

# vaso com flor
P["vaso_flor"] = svg(70, 100, path("M35,62 L35,30", extra=f'stroke="{C["verde_esc"]}" stroke-width="5"') +
                     path("M35,50 q-16,-4 -18,-16 q14,0 18,16 Z", C["verde"], 'stroke-width="2"') +
                     flor(35, 22, 12, C["rosa_chiclete"], C["amarelo"]) +
                     path("M12,60 L58,60 L52,96 L18,96 Z", C["lilas"], 'stroke-width="3"') + rr(8, 54, 54, 12, 5, C["lilas"], 'stroke-width="3"') +
                     coracao(35, 80, 7, C["branco"], 'stroke-width="1.8"'))
# pedra de caminho
P["pedra_caminho"] = svg(100, 44, ell(50, 24, 46, 17, "#d6c9b9", 'stroke-width="3"') + ell(40, 19, 20, 6, "#e8ded2", 'stroke="none"') +
                         coracao(66, 26, 6, "#c4b5a3", 'stroke-width="1.5"'))
# cerquinha branca
s = ""
for x in (8, 40, 72, 104):
    s += path(f"M{x},90 L{x},24 L{x+10},12 L{x+20},24 L{x+20},90 Z", C["branco"], 'stroke-width="3"')
s += rr(2, 36, 128, 12, 5, C["branco"], 'stroke-width="3"') + rr(2, 66, 128, 12, 5, C["branco"], 'stroke-width="3"') + coracao(66, 42, 6, C["rosa_forte"], 'stroke-width="1.5"')
P["cerquinha"] = svg(132, 94, s)
# catavento
s = rr(36, 44, 8, 100, 3, C["madeira"], 'stroke-width="2.5"')
for i, c in enumerate([C["rosa_chiclete"], C["amarelo"], C["azul"], C["lilas"]]):
    s += f'<g transform="rotate({i*90} 40 40)">' + path("M40,40 L40,6 Q64,10 62,34 Z", c, 'stroke-width="2.5"') + '</g>'
s += circ(40, 40, 7, C["branco"], 'stroke-width="2.5"')
P["catavento"] = svg(80, 146, s)
# casinha de passarinho num poste
s = rr(41, 70, 10, 96, 3, C["madeira_esc"]) + rr(18, 34, 56, 46, 6, C["creme"], 'stroke-width="3"')
s += path("M10,38 L46,8 L82,38 Z", C["rosa_chiclete"], 'stroke-width="3"') + circ(46, 54, 10, "#6b4630", 'stroke-width="2.5"') + rr(42, 68, 8, 12, 2, C["madeira"], 'stroke-width="2"')
s += coracao(46, 26, 5, C["branco"], 'stroke-width="1.5"')
P["casinha_passarinho"] = svg(92, 168, s)
# lanterna de jardim
s = rr(26, 50, 8, 80, 3, L) + ell(30, 132, 18, 6, C["cinza"], 'stroke-width="2.5"')
s += circ(30, 30, 26, "#fff0b8", 'stroke="none" opacity="0.6"') + rr(16, 14, 28, 36, 6, "#ffe9a3", 'stroke-width="3"') + rr(12, 8, 36, 10, 4, C["lilas"], 'stroke-width="2.5"')
s += coracao(30, 32, 6, C["rosa_forte"], 'stroke-width="1.5"')
P["lanterna_jardim"] = svg(60, 140, s)
# banquinho de jardim
s = rr(16, 40, 12, 44, 3, C["madeira_esc"]) + rr(112, 40, 12, 44, 3, C["madeira_esc"])
s += rr(6, 28, 128, 16, 6, C["madeira"], 'stroke-width="3"') + rr(14, 4, 112, 12, 5, C["madeira"], 'stroke-width="3"') + rr(22, 14, 8, 16, 2, C["madeira_esc"]) + rr(110, 14, 8, 16, 2, C["madeira_esc"])
s += coracao(70, 10, 5, C["rosa_forte"], 'stroke-width="1.5"')
P["banquinho_jardim"] = svg(140, 86, s)
# cogumelo
P["cogumelo"] = svg(70, 70, rr(26, 36, 18, 30, 8, C["creme"], 'stroke-width="2.8"') + path("M6,40 Q8,6 35,6 Q62,6 64,40 Z", C["vermelho_rosa"], 'stroke-width="3"') +
                    circ(22, 24, 5, C["branco"], 'stroke="none"') + circ(40, 16, 6, C["branco"], 'stroke="none"') + circ(52, 30, 4, C["branco"], 'stroke="none"'))
# arco de flores
s = path("M24,250 L24,110 Q24,22 110,22 Q196,22 196,110 L196,250", extra=f'stroke="{L}" stroke-width="22"')
s += path("M24,250 L24,110 Q24,22 110,22 Q196,22 196,110 L196,250", extra=f'stroke="{C["verde"]}" stroke-width="15"')
for i, (x, y) in enumerate([(24, 210), (24, 150), (34, 86), (70, 40), (110, 22), (150, 40), (186, 86), (196, 150), (196, 210)]):
    s += flor(x, y, 11, [C["rosa_chiclete"], C["lilas"], C["amarelo"]][i % 3], C["branco"])
P["arco_flores"] = svg(220, 256, s)
# botão da lojinha (cestinha de compras) e etiqueta de preço
P["botao_loja"] = svg(120, 120, circ(60, 60, 54, C["rosa_claro"], 'stroke-width="5"') + circ(60, 60, 44, C["branco"], 'stroke-width="2"') +
                      path("M40,56 Q60,22 80,56", extra='stroke-width="5"') + path("M32,56 L88,56 L80,88 L40,88 Z", C["mel"], 'stroke-width="3.5"') +
                      path("M36,68 L84,68 M38,78 L82,78", extra='stroke-width="1.6" opacity="0.5"') + coracao(60, 72, 8, C["rosa_forte"], 'stroke-width="2"'))
P["ferradurinha"] = svg(60, 60, path("M14,52 L10,26 A20,20 0 0 1 50,26 L46,52 L37,52 L40,27 A10,10 0 0 0 20,27 L23,52 Z", C["dourado"], 'stroke-width="3"') +
                        coracao(30, 30, 5, C["rosa_forte"], 'stroke-width="1.5"'))
P["cadeado"] = svg(50, 56, path("M14,26 L14,18 A11,11 0 0 1 36,18 L36,26", extra='stroke-width="7"') + path("M14,26 L14,18 A11,11 0 0 1 36,18 L36,26", extra=f'stroke="{C["dourado"]}" stroke-width="3.5"') +
                   rr(6, 24, 38, 28, 7, C["dourado"], 'stroke-width="3"') + coracao(25, 38, 6, C["rosa_forte"], 'stroke-width="1.5"'))

salvar(P, os.path.join(dest, "svg"), dest)
for f in os.listdir(dest):
    if f.endswith(".png"):
        shutil.copyfile(os.path.join(dest, f), os.path.join(jogo, f))
print(sorted(f for f in os.listdir(jogo) if f.endswith(".png")))
