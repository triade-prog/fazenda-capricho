"""C12 Cabana externa (proposta para as criadoras): peças 2D provisórias, layout e prompts 3D.

Uso: python3 ferramentas/cenario2d/cabana.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import ceu_morros, cerca, grama_fundo, arvore_simples  # noqa: E402

W, H, CHAO = 2200, 900, 600
P = {}


def fundo():
    rnd = random.Random(61)
    s, defs = ceu_morros(W, H, CHAO, rnd)
    s += f'<g transform="translate(40,120)">{arvore_simples(420, 500, C["verde"], C["rosa"], 8)}</g>'
    s += f'<g transform="translate(1780,140)">{arvore_simples(380, 480, C["verde_esc"], C["branco"], 9)}</g>'
    s += cerca(W, CHAO)
    # varal de bandeirinhas entre as árvores
    s += path("M250,250 Q1100,380 1960,250", extra='stroke-width="3"')
    cores = [C["rosa_chiclete"], C["lilas"], C["amarelo"], C["azul"], C["verde"]]
    for i in range(26):
        t = (i + 0.5) / 26
        x = 250 + t * 1710
        y = 250 + 4 * 130 * t * (1 - t) * 1.0
        s += path(f"M{x-16:.0f},{y:.0f} L{x+16:.0f},{y+3:.0f} L{x:.0f},{y+40:.0f} Z", cores[i % 5], 'stroke-width="2.5"')
    s += grama_fundo(W, H, CHAO, rnd)
    return svg(W, H, s, defs)


P["fundo"] = fundo()


def cabana(aberta):
    w, h = 460, 380
    s = rr(224, 0, 12, 40, 3, C["madeira_esc"]) + path("M236,6 L280,18 L236,30 Z", C["rosa_chiclete"], 'stroke-width="2.5"')
    s += path(f"M230,30 L20,{h-6} L440,{h-6} Z", C["rosa_claro"], 'stroke-width="4"')
    for k in range(1, 6):
        x = 20 + k * 70
        s += path(f"M230,30 L{x},{h-6}", extra=f'stroke="{C["rosa"]}" stroke-width="10" opacity="0.6"')
    s += path(f"M230,30 L20,{h-6} L440,{h-6} Z", "none", 'stroke-width="4"')
    if aberta:
        s += path(f"M230,110 L120,{h-6} L340,{h-6} Z", "#6b4a63", 'stroke-width="3"')
        s += path(f"M230,110 Q160,220 100,{h-6} L120,{h-6} Z", C["lilas"], 'stroke-width="3"')
        s += path(f"M230,110 Q300,220 360,{h-6} L340,{h-6} Z", C["lilas"], 'stroke-width="3"')
        s += circ(230, 250, 30, "#ffe7a3", 'stroke="none" opacity="0.5"')
    else:
        s += path(f"M230,110 L120,{h-6} L340,{h-6} Z", C["lilas"], 'stroke-width="3"')
        s += path(f"M230,110 L230,{h-6}", extra='stroke-width="2.5"')
        s += coracao(230, 250, 18, C["rosa_forte"], 'stroke-width="2.5"')
    s += rr(14, h - 14, 432, 12, 5, C["madeira"], 'stroke-width="3"')
    return svg(w, h, s)


P["cabana_fechada"] = cabana(False)
P["cabana_aberta"] = cabana(True)


def almofadas():
    w, h = 320, 90
    s = rr(10, 40, 300, 46, 20, C["azul"], 'stroke-width="3"') + rr(10, 40, 90, 46, 20, "#cfe6fb", 'stroke-width="3"')
    for x in range(130, 300, 50):
        s += estrela(x, 63, 8, C["amarelo"], 5, 'stroke-width="1.5"')
    s += rr(150, 6, 80, 46, 20, C["rosa"], 'stroke-width="3"') + rr(214, 14, 70, 40, 18, C["lilas"], 'stroke-width="3"')
    return svg(w, h, s)


P["saco_dormir"] = almofadas()


def lanterna(ligada):
    w, h = 60, 100
    s = ""
    if ligada:
        s += circ(30, 56, 30, "#ffe08a", 'stroke="none" opacity="0.6"')
    s += path("M18,16 Q30,0 42,16", extra='stroke-width="3"') + rr(14, 16, 32, 8, 3, C["verde_esc"], 'stroke-width="2.5"')
    s += path("M16,24 L44,24 L48,84 L12,84 Z", "#fff1b3" if ligada else "#dde6ee", 'stroke-width="2.5"')
    s += estrela(30, 54, 9, C["laranja"] if ligada else C["cinza"], 5, 'stroke-width="2"') + rr(8, 84, 44, 12, 4, C["verde_esc"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["lanterna_desligada"] = lanterna(False)
P["lanterna_ligada"] = lanterna(True)


def livro(aberto):
    w, h = 70, 50
    if not aberto:
        s = rr(14, 6, 42, 40, 4, C["rosa_chiclete"], 'stroke-width="2.5"') + estrela(35, 26, 9, C["amarelo"], 5, 'stroke-width="1.5"')
    else:
        s = path("M35,10 Q18,2 4,8 L4,44 Q18,38 35,46 Z", C["branco"], 'stroke-width="2.5"') + path("M35,10 Q52,2 66,8 L66,44 Q52,38 35,46 Z", C["branco"], 'stroke-width="2.5"')
        s += circ(18, 24, 6, C["amarelo"], 'stroke-width="1.5"') + path("M8,38 Q18,30 30,38", extra=f'stroke="{C["verde_esc"]}" stroke-width="2"')
        s += coracao(52, 26, 7, C["rosa_forte"], 'stroke-width="1.5"')
    return svg(w, h, s)


P["livro_fechado"] = livro(False)
P["livro_aberto"] = livro(True)


def fogueira(brilho):
    w, h = 170, 120
    s = ""
    if brilho:
        s += ell(85, 60, 80, 56, "#ffe7a3", 'stroke="none" opacity="0.5"')
        s += estrela(30, 20, 7, C["amarelo"], 4, 'stroke-width="1.5"') + estrela(145, 28, 6, C["amarelo"], 4, 'stroke-width="1.5"')
    for i in range(7):
        a = math.pi * i / 6
        s += ell(85 + 64 * math.cos(a + math.pi), 100 + 8 * math.sin(a), 15, 9, "#d6c9b9", 'stroke-width="2"')
    s += path("M40,100 L130,84 M40,84 L130,100", extra='stroke-width="16"') + path("M40,100 L130,84 M40,84 L130,100", extra=f'stroke-width="11" stroke="{C["madeira_esc"]}"')
    # chamas de feltro (tecido)
    for dx, hh, c in [(-20, 50, "#ff9a3c"), (20, 50, "#ff9a3c"), (0, 70, "#ff7b54"), (0, 40, C["amarelo"])]:
        x = 85 + dx
        s += path(f"M{x-18},88 Q{x-20},{88-hh*0.5} {x},{88-hh} Q{x+20},{88-hh*0.5} {x+18},88 Z", c, 'stroke-width="2.5" stroke-dasharray="5 3"' if c != C["amarelo"] else 'stroke-width="2.5"')
    return svg(w, h, s)


P["fogueira"] = fogueira(False)
P["fogueira_brilho"] = fogueira(True)
P["binoculo"] = svg(64, 44, circ(18, 26, 14, C["roxo"], 'stroke-width="2.5"') + circ(46, 26, 14, C["roxo"], 'stroke-width="2.5"') +
                    circ(18, 26, 8, C["ceu"], 'stroke-width="2"') + circ(46, 26, 8, C["ceu"], 'stroke-width="2"') + rr(26, 10, 12, 14, 3, C["lilas"], 'stroke-width="2"') +
                    path("M8,14 Q32,-4 56,14", extra=f'stroke="{C["rosa_chiclete"]}" stroke-width="2.5"'))
P["tronco_banco"] = svg(200, 80, rr(8, 14, 170, 60, 30, C["madeira_esc"], 'stroke-width="3.5"') + ell(176, 44, 20, 30, C["madeira_clara"], 'stroke-width="3.5"') +
                        ell(176, 44, 11, 18, "none", 'stroke-width="2"'))
P["passarinho"] = svg(40, 35, path("M8,20 L1,15 L3,24 Z", C["azul"], 'stroke-width="1.8"') + ell(19, 21, 12, 10, "#bfe3ff", 'stroke-width="2"') +
                      ell(15, 23, 6, 4, C["azul"], 'stroke-width="1.8"') + circ(26, 15, 8, "#bfe3ff", 'stroke-width="2"') + circ(28, 13, 1.8, L, 'stroke="none"') +
                      path("M33,15 L39,17 L33,19 Z", C["laranja"], 'stroke-width="1.5"'))

POS = [("fundo", 0, 0), ("cabana_aberta", 820, 230), ("saco_dormir", 890, 500), ("lanterna_ligada", 1020, 420),
       ("fogueira_brilho", 1400, 560), ("tronco_banco", 1560, 600), ("tronco_banco", 1180, 690),
       ("livro_aberto", 640, 690), ("livro_fechado", 560, 700), ("binoculo", 1700, 560), ("passarinho", 1880, 300),
       ("@catarina", 700, 860), ("@catarina", 1640, 880)]

TABELA = [
    ("Fundo do quintal", "2200 × 900", None, "Quintal com duas árvores grandes, céu claro, morros, cerca branca e um varal de bandeirinhas coloridas entre as árvores, grama com florzinhas. SEM a cabana e os objetos.", ["fundo"]),
    ("Cabana de tecido", "460 × 380", "fechada · aberta", "Tenda triangular de madeira e tecido rosa-claro com listras, bandeirinha no topo e entrada de tecido lilás. Aberta: as abas presas para os lados, interior escuro e aconchegante (quem entra some, como no castelinho).", ["cabana_fechada", "cabana_aberta"]),
    ("Saco de dormir e almofadas", "320 × 90", None, "Saco de dormir azul com estrelinhas e duas almofadas, rosa e lilás. Deitam até 3.", ["saco_dormir"]),
    ("Lanterna", "60 × 100", "desligada · ligada", "Lanterna de acampar verde com estrela; ligada, dentro da cabana fica 'de noite'.", ["lanterna_desligada", "lanterna_ligada"]),
    ("Livro de figuras", "70 × 50", "fechado · aberto", "Livro com estrela na capa; aberto mostra desenhos (sol, coração), sem letras.", ["livro_fechado", "livro_aberto"]),
    ("Fogueira de mentirinha", "170 × 120", "normal · brilhando", "Fogueira de FELTRO com costuras aparentes, lenha de brinquedo e pedrinhas em volta. Sem fogo de verdade; tocar faz brilhar.", ["fogueira", "fogueira_brilho"]),
    ("Binóculo", "64 × 44", None, "Binóculo de brinquedo roxo e lilás com alça rosa.", ["binoculo"]),
    ("Banco de tronco", "200 × 80", None, "Tronco deitado para sentar em volta da fogueira.", ["tronco_banco"]),
    ("Passarinho", "40 × 35", None, "Passarinho azul-claro para olhar de binóculo.", ["passarinho"]),
]

if __name__ == "__main__":
    pr, le = textos("cabana", "Cabana externa", "C12",
                    "É uma cabana de faz de conta no quintal, de madeira e tecido, para acampar e contar histórias, com almofadas, lanterna e bandeirinhas.",
                    "", "2200 × 900, chão a partir de y = 600", TABELA,
                    aviso="\n**Proposta:** a aparência e as brincadeiras da cabana ainda precisam da definição das criadoras. Ajuste a tabela antes de gerar.\n")
    gerar_cenario("cabana", P, W, H, POS, "C12 Cabana externa (proposta) · Catarina = 300 px · chão a partir de y = 600 · tela 2200 × 900", pr, le)
