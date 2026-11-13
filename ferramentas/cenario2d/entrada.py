"""C01 Entrada da Fazenda: peças 2D provisórias, layout e prompts 3D.

Uso: python3 ferramentas/cenario2d/entrada.py
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


def pilar(x, topo, base, w=80):
    rnd = random.Random(x)
    s = rr(x, topo, w, base - topo, 8, "#e3d7ca", 'stroke-width="3.5"')
    for y in range(topo + 14, base - 10, 34):
        for k in range(2):
            s += ell(x + 20 + k * 40 + (y // 34 % 2) * 6, y + 10, 18, 12, rnd.choice(["#d6c9b9", "#ece2d6", "#cbbcab"]), 'stroke-width="2"')
    s += rr(x - 8, topo - 16, w + 16, 22, 6, "#cbbcab", 'stroke-width="3"')
    return s


def fundo():
    rnd = random.Random(51)
    s, defs = ceu_morros(W, H, CHAO, rnd)
    # celeiro rosa e casinhas ao longe
    s += path("M1650,470 L1650,400 L1720,350 L1790,400 L1790,470 Z", C["vermelho_rosa"], 'stroke-width="3"')
    s += path("M1690,470 L1690,425 L1750,425 L1750,470 M1690,425 L1750,470 M1750,425 L1690,470", C["branco"], 'stroke-width="2.5"')
    s += path("M1840,480 L1840,440 L1880,412 L1920,440 L1920,480 Z", C["rosa"], 'stroke-width="2.5"')
    s += path("M380,486 L380,446 L420,418 L460,446 L460,486 Z", C["lilas"], 'stroke-width="2.5"')
    s += f'<g transform="translate(60,250)">{arvore_simples(240, 300, C["verde"], C["rosa"], 6)}</g>'
    s += f'<g transform="translate(1960,240)">{arvore_simples(220, 300, C["verde"], C["rosa"], 7)}</g>'
    s += cerca(W, CHAO, 0, 740) + cerca(W, CHAO, 1460, W)
    s += grama_fundo(W, H, CHAO, rnd)
    # estrada de terra
    s += path(f"M900,{CHAO} L1300,{CHAO} L1520,{H+5} L680,{H+5} Z", "#dcb98d", 'stroke-width="3"')
    for _ in range(40):
        x, y = rnd.uniform(800, 1400), rnd.uniform(CHAO + 20, H - 10)
        s += ell(round(x), round(y), rnd.uniform(4, 8), 3, "#c9a376", 'stroke="none"')
    s += pilar(740, 300, CHAO + 10) + pilar(1380, 300, CHAO + 10)
    return svg(W, H, s, defs)


P["fundo"] = fundo()


def portao(aberto):
    w, h = 560, 280
    s = ""
    def folha(x0, x1):
        f = rr(x0, 30, x1 - x0, 240, 10, C["madeira"], 'stroke-width="4"')
        f += rr(x0, 30, x1 - x0, 26, 8, C["madeira_esc"], 'stroke-width="3"') + rr(x0, 244, x1 - x0, 26, 8, C["madeira_esc"], 'stroke-width="3"')
        f += path(f"M{x0+14},64 L{x1-14},236 M{x0+14},236 L{x1-14},64", extra='stroke-width="20"')
        f += path(f"M{x0+14},64 L{x1-14},236 M{x0+14},236 L{x1-14},64", extra=f'stroke-width="14" stroke="{C["madeira_esc"]}"')
        cx = (x0 + x1) / 2
        f += circ(cx, 150, 36, C["madeira"], 'stroke-width="3.5"') + coracao(cx, 152, 22, C["rosa_forte"])
        return f
    if not aberto:
        s += folha(4, 278) + folha(282, 556)
        s += rr(270, 120, 20, 50, 4, C["dourado"], 'stroke-width="2.5"')
    else:
        # folhas abertas para trás: estreitas junto aos pilares
        for x0, x1 in ((4, 74), (486, 556)):
            s += rr(x0, 30, x1 - x0, 240, 8, C["madeira"], 'stroke-width="4"')
            s += rr(x0, 30, x1 - x0, 26, 6, C["madeira_esc"], 'stroke-width="3"') + rr(x0, 244, x1 - x0, 26, 6, C["madeira_esc"], 'stroke-width="3"')
            s += coracao((x0 + x1) / 2, 152, 12, C["rosa_forte"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["portao_fechado"] = portao(False)
P["portao_aberto"] = portao(True)


def arco_portal():
    w, h = 820, 220
    s = path("M10,150 Q410,60 810,150 L810,180 Q410,92 10,180 Z", C["madeira"], 'stroke-width="4"')
    for x in range(20, 810, 30):
        y = 150 - 90 * math.sin(math.pi * x / 820) * 0.62 - 6
        s += circ(x, round(y), 16, C["verde"], 'stroke-width="2.5"')
    for x in range(26, 800, 44):
        y = 150 - 90 * math.sin(math.pi * x / 820) * 0.62 - 10
        s += flor(x, round(y), 9, C["rosa_chiclete"] if x % 3 else C["lilas"], C["amarelo"])
    # tabuleta vazia para a logo (a logo é peça separada)
    s += rr(250, 10, 320, 150, 26, C["madeira_clara"], 'stroke-width="4"') + rr(264, 24, 292, 122, 18, "#fff4e2", 'stroke-width="2"')
    s += path("M300,10 L300,0 M520,10 L520,0", extra='stroke-width="4"')
    return svg(w, h, s)


P["arco_portal"] = arco_portal()


def lanterna(acesa):
    w, h = 60, 110
    s = ""
    if acesa:
        s += circ(30, 62, 32, "#ffe08a", 'stroke="none" opacity="0.6"')
    s += rr(26, 2, 8, 14, 2, L, 'stroke="none"') + rr(14, 16, 32, 8, 3, C["madeira_esc"], 'stroke-width="2.5"')
    s += path("M16,24 L44,24 L48,92 L12,92 Z", "#fff1b3" if acesa else "#dde6ee", 'stroke-width="2.5"')
    s += ell(30, 60, 6, 11, C["laranja"] if acesa else C["cinza"], 'stroke-width="2"') + rr(8, 92, 44, 14, 4, C["madeira_esc"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["lanterna_apagada"] = lanterna(False)
P["lanterna_acesa"] = lanterna(True)


def moinho_torre():
    w, h = 200, 380
    s = path(f"M60,{h-2} L88,30 L112,30 L140,{h-2}", extra='stroke-width="9"') + path(f"M60,{h-2} L88,30 L112,30 L140,{h-2}", extra=f'stroke-width="5" stroke="{C["madeira"]}"')
    for y in range(80, h, 70):
        t = (y - 30) / (h - 32)
        xa, xb = 88 - 28 * t, 112 + 28 * t
        s += path(f"M{xa:.0f},{y} L{xb:.0f},{y}", extra='stroke-width="7"') + path(f"M{xa:.0f},{y} L{xb:.0f},{y}", extra=f'stroke-width="3.5" stroke="{C["madeira"]}"')
    s += path("M100,30 L150,20 L156,40 L100,40 Z", C["rosa"], 'stroke-width="2.5"')     # leme
    s += rr(84, 20, 32, 24, 5, C["madeira_esc"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["moinho_torre"] = moinho_torre()


def moinho_helice():
    w = h = 240
    s = ""
    for i in range(8):
        a = math.radians(i * 45)
        x1, y1 = 120 + 108 * math.cos(a), 120 + 108 * math.sin(a)
        nx, ny = -math.sin(a) * 14, math.cos(a) * 14
        s += path(f"M120,120 L{x1+nx:.1f},{y1+ny:.1f} L{x1-nx:.1f},{y1-ny:.1f} Z", C["rosa"] if i % 2 else C["branco"], 'stroke-width="2.5"')
    s += circ(120, 120, 14, C["madeira_esc"], 'stroke-width="2.5"') + coracao(120, 121, 6, C["rosa_forte"], 'stroke-width="1.5"')
    return svg(w, h, s)


P["moinho_helice"] = moinho_helice()


def correio(aberto):
    w, h = 110, 170
    s = rr(48, 70, 14, 98, 4, C["madeira_esc"])
    s += path("M10,80 L10,40 Q10,10 55,10 Q100,10 100,40 L100,80 Z", C["rosa_chiclete"], 'stroke-width="3"')
    if aberto:
        s += path("M10,80 L100,80 L104,92 L6,92 Z", C["rosa"], 'stroke-width="2.5"')
        s += ell(55, 44, 34, 24, "#7d4f63", 'stroke-width="2.5"')
        s += rr(36, 36, 38, 22, 3, C["branco"], 'stroke-width="2"') + coracao(55, 46, 5, C["rosa_forte"], 'stroke-width="1.2"')
    else:
        s += rr(10, 76, 90, 10, 3, C["rosa"], 'stroke-width="2.5"') + coracao(55, 46, 12, C["branco"], 'stroke-width="2.5"')
    s += rr(98, 26, 8, 36, 2, C["dourado"], 'stroke-width="2"') + rr(98, 22, 20, 14, 2, C["dourado"], 'stroke-width="2"')
    return svg(w + 12, h, s)


P["correio_fechado"] = correio(False)
P["correio_aberto"] = correio(True)
P["cartinha"] = svg(50, 36, rr(3, 4, 44, 28, 3, C["branco"], 'stroke-width="2.2"') + path("M3,4 L25,20 L47,4", extra='stroke-width="2"') +
                    coracao(25, 22, 5, C["rosa_forte"], 'stroke-width="1.2"'))


def floreira(com):
    w, h = 220, 110
    s = ""
    if com:
        for i, x in enumerate(range(30, 200, 28)):
            s += path(f"M{x},{60} L{x},{30 + (i % 2) * 10}", extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
            s += flor(x, 30 + (i % 2) * 10, 10, [C["rosa_chiclete"], C["lilas"], C["amarelo"], C["branco"]][i % 4], C["rosa_forte"] if i % 4 == 2 else C["amarelo"])
    for x in range(26, 200, 24):
        s += ell(x, 62, 14, 6, C["verde"], f'stroke-width="2" transform="rotate({-30 if x % 48 else 30} {x} 62)"')
    s += path("M10,62 L210,62 L196,108 L24,108 Z", C["madeira"], 'stroke-width="3.5"') + rr(4, 56, 212, 14, 6, C["madeira_esc"], 'stroke-width="3"')
    return svg(w, h, s)


P["floreira"] = floreira(True)
P["floreira_colhida"] = floreira(False)
P["flor"] = svg(25, 55, path("M12.5,18 L12.5,53", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') + flor(12.5, 13, 6.5, C["rosa_chiclete"]))
P["banco"] = svg(260, 110, rr(14, 6, 232, 44, 10, C["madeira"], 'stroke-width="3.5"') + rr(6, 52, 248, 22, 8, C["madeira"], 'stroke-width="3.5"') +
                 rr(24, 74, 16, 34, 4, C["madeira_esc"]) + rr(220, 74, 16, 34, 4, C["madeira_esc"]) + coracao(130, 28, 10, C["rosa_forte"], 'stroke-width="2"'))

POS = [("fundo", 0, 0),
       ("moinho_torre", 420, 220), ("moinho_helice", 400, 120),
       ("portao_aberto", 820, 330), ("arco_portal", 690, 140),
       ("lanterna_acesa", 750, 330), ("lanterna_acesa", 1390, 330),
       ("floreira", 520, 560), ("floreira_colhida", 1490, 560),
       ("correio_aberto", 1660, 450), ("cartinha", 1800, 560),
       ("banco", 220, 540), ("flor", 1530, 760), ("@catarina", 1080, 860), ("@catarina", 1880, 820)]

TABELA = [
    ("Fundo da Entrada", "2200 × 900", None, "Céu claro, morros, ao longe um celeiro ROSA e casinhas em tons rosados, árvores floridas, cerca branca, estrada de terra subindo para o portal e os dois pilares de pedra do portal. SEM portão, arco, logo, moinho, lanternas, caixa de correio, floreiras e banco. SEM cactos.", ["fundo"]),
    ("Portão de duas folhas", "560 × 280", "fechado · aberto", "Duas folhas de madeira em 'X' com um coração rosa em cada, entre os pilares. Aberto: as folhas giradas para trás, estreitas junto aos pilares.", ["portao_fechado", "portao_aberto"]),
    ("Arco do portal", "820 × 220", None, "Viga de madeira em arco coberta de folhas e flores rosa e lilás, com uma tabuleta clara VAZIA no centro: a logo da Fazenda Capricho é peça separada (folha de pulso da R01), não pinte letras.", ["arco_portal"]),
    ("Lanterna do portal", "60 × 110", "apagada · acesa", "Lanterna de fazenda pendurada no pilar; acesa, luz quente.", ["lanterna_apagada", "lanterna_acesa"]),
    ("Moinho", "torre 200 × 380 · hélice 240 × 240", None, "Torre de madeira treliçada e, numa imagem separada, a hélice de pás rosa e brancas com coração no centro, para o jogo girar.", ["moinho_torre", "moinho_helice"]),
    ("Caixa de correio", "122 × 170", "fechada · aberta", "Caixinha rosa arredondada num poste, com bandeirinha dourada e coração. Aberta: aparece uma cartinha.", ["correio_fechado", "correio_aberto"]),
    ("Cartinha", "50 × 36", None, "Envelope branco com coração (o desenho de dentro é feito pelo jogo).", ["cartinha"]),
    ("Floreira", "220 × 110", "com flores · colhida", "Jardineira de madeira com flores rosa, lilás, amarelas e brancas.", ["floreira", "floreira_colhida"]),
    ("Flor solta", "25 × 55", None, "Flor rosa com caule, para dar a um personagem.", ["flor"]),
    ("Banco", "260 × 110", None, "Banco de madeira com coração no encosto; sentam 2.", ["banco"]),
]

# Como o cenário entra no protótipo (ver para_jogo.py). O portão leva à Sede.
JOGO = {
    "interativos": {
        "portao": {"estados": ["portao_fechado", "portao_aberto"], "x": 820, "y": 330, "leva": "sede", "chegada": 1100, "estado": 0},
        "lanterna_esq": {"estados": ["lanterna_apagada", "lanterna_acesa"], "x": 750, "y": 330},
        "lanterna_dir": {"estados": ["lanterna_apagada", "lanterna_acesa"], "x": 1390, "y": 330},
        "floreira_esq": {"estados": ["floreira_colhida", "floreira"], "x": 520, "y": 560},
        "floreira_dir": {"estados": ["floreira_colhida", "floreira"], "x": 1490, "y": 560},
        "correio": {"estados": ["correio_fechado", "correio_aberto"], "x": 1660, "y": 450},
    },
    "objetos": ["cartinha", "flor"],
    "lugares": [],
    "superficies": [],
}

if __name__ == "__main__":
    pr, le = textos("entrada", "Entrada da Fazenda", "C01",
                    "É a chegada: portal de madeira com a placa da Fazenda Capricho, flores e lanternas; ao fundo, a fazenda.",
                    " e o conceito `arte/conceito/cenarios_R01/01_entrada_fazenda.png` (só o clima, sem cactos)",
                    "2200 × 900, chão a partir de y = 600", TABELA,
                    aviso="\n**Pendência:** a Entrada pode ser só a ilustração do mapa. As peças servem para os dois usos.\n",
                    ordem="\nGere primeiro o portão (os dois estados) e o arco, que encaixam nos pilares do fundo.\n")
    gerar_cenario("entrada", P, W, H, POS, "C01 Entrada da Fazenda · Catarina = 300 px · chão a partir de y = 600 · tela 2200 × 900", pr, le)
