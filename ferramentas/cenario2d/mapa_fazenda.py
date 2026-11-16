"""Mapa da fazenda ilustrado (visto de cima, como a imagem de referência de Carol, 15/11/2026).

Cada coisa do mapa é uma peça separada (PNG com fundo transparente), para trocar depois pela versão 3D
com o mesmo nome e o mesmo tamanho. As placas vêm SEM letras: o jogo escreve os nomes por cima.

Gera:
  arte/interface/mapa_fazenda/2d/*.png (+ svg/)       peças 2D
  arte/interface/mapa_fazenda/mapa_fazenda_layout.png  montagem com nomes e tamanhos
  arte/interface/mapa_fazenda/mapa_fazenda_previa.png  montagem como no jogo (com os textos)
  prototipo/assets/mapa/fazenda/*.png                  cópia para o jogo
  prototipo/dados/mapa_fazenda.json                    posições (o jogo lê daqui)
Uso: python3 ferramentas/cenario2d/mapa_fazenda.py
"""
import json
import math
import os
import random
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, flor, nuvem, salvar  # noqa: E402

raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = os.path.join(raiz, "arte/interface/mapa_fazenda")
d2 = os.path.join(base, "2d")
jogo = os.path.join(raiz, "prototipo/assets/mapa/fazenda")
FONTE = os.path.join(raiz, "prototipo/assets/fontes/Fredoka-SemiBold.ttf")

# Área do mapa: 1600 × 1200 (a tela do jogo). O fundo sobra 300 px de cada lado e 150 em cima e
# embaixo, para cobrir telas mais largas ou mais altas sem faixa vazia.
W, H = 1600, 1200
FX, FY = 300, 150
FW, FH = W + 2 * FX, H + 2 * FY

GRAMA, GRAMA_ESC, GRAMA_CLARA = "#9ed883", "#7fc56a", "#b9e6a0"
TERRA, TERRA_BORDA = "#f3dcb2", "#e2c08e"
ROSA_TELHA, ROXO_TELHA = "#ff9cc8", "#a874e0"
P = {}


def tam(nome):
    import re
    return tuple(map(int, re.search(r'width="(\d+)" height="(\d+)"', P[nome]).groups()))


# ---------------------------------------------------------------- miudezas

def tufo(x, y, k=1.0):
    return path(f"M{x},{y} l{-5*k:.1f},{-11*k:.1f} M{x},{y} l0,{-14*k:.1f} M{x},{y} l{6*k:.1f},{-11*k:.1f}",
                extra=f'stroke="{GRAMA_ESC}" stroke-width="2.5"')


def moita(cx, cy, r, cor=C["verde"], flores=None, rnd=None, n=4):
    s = ""
    bolas = [(cx - r * 0.9, cy, r * 0.75), (cx + r * 0.9, cy, r * 0.75), (cx, cy - r * 0.35, r)]
    for x, y, q in bolas:
        s += circ(round(x, 1), round(y, 1), round(q, 1), cor, 'stroke-width="3"')
    for x, y, q in bolas:
        s += circ(round(x, 1), round(y, 1), round(q - 3, 1), cor, 'stroke="none"')
    if flores:
        rnd = rnd or random.Random(int(cx * 7 + cy))
        for _ in range(n):
            s += flor(round(cx + rnd.uniform(-r * 1.2, r * 1.2)), round(cy + rnd.uniform(-r * 0.9, r * 0.2)),
                      max(4, r * 0.22), rnd.choice(flores), C["amarelo"])
    return s


def vaso_flores(cx, base_y, cor_vaso, flores):
    s = path(f"M{cx-17},{base_y-30} L{cx+17},{base_y-30} L{cx+12},{base_y} L{cx-12},{base_y} Z", cor_vaso, 'stroke-width="2.5"')
    s += moita(cx, base_y - 36, 13, C["verde"])
    for i, f in enumerate(flores):
        s += flor(cx - 12 + i * 12, base_y - 44 + (i % 2) * 6, 5, f)
    return s


def janela(x, y, w, h, moldura=C["branco"], luz="#fff2b8"):
    s = rr(x - 5, y - 5, w + 10, h + 10, 6, moldura, 'stroke-width="2.5"') + rr(x, y, w, h, 4, luz, 'stroke-width="2"')
    s += path(f"M{x+w/2},{y} L{x+w/2},{y+h} M{x},{y+h/2} L{x+w},{y+h/2}", extra='stroke-width="3"')
    return s


def telhado_escamas(pts, cor, cor_linha, y0, y1, passo=18):
    """Telhado (polígono pts) com fileiras de telhas desenhadas por cima."""
    pid = f"t{abs(hash((pts, cor))) % 99999}"
    s = f'<clipPath id="{pid}"><path d="{pts}"/></clipPath>'
    s += path(pts, cor, 'stroke-width="3.5"')
    s += f'<g clip-path="url(#{pid})">'
    y = y0 + passo
    i = 0
    while y < y1:
        off = (i % 2) * passo
        d = f"M-50,{y}"
        for x in range(-50 + off, 1400, passo * 2):
            d += f" q{passo},{passo*0.7:.0f} {passo*2},0"
        s += path(d, extra=f'stroke="{cor_linha}" stroke-width="2" opacity="0.55"')
        y += passo
        i += 1
    s += "</g>" + path(pts, extra='stroke-width="3.5"')
    return s


def cerca_trecho(w, h=62):
    s = rr(0, 16, w, 10, 4, C["branco"], 'stroke-width="2.5"') + rr(0, 38, w, 10, 4, C["branco"], 'stroke-width="2.5"')
    for x in range(8, w - 14, 46):
        s += path(f"M{x},{h-2} L{x},{10} L{x+9},{2} L{x+18},{10} L{x+18},{h-2} Z", C["branco"], 'stroke-width="2.5"')
    return s


# ---------------------------------------------------------------- fundo (grama, morros, caminhos)

CAMINHOS = [
    # da Entrada até a frente da Casa
    "M800,1290 C800,1120 790,980 740,870 C720,830 700,800 690,790",
    # para a Casa na Árvore (volta pela esquerda)
    "M745,880 C560,840 250,820 200,690 C160,590 170,540 205,505",
    # para a Cabana
    "M520,850 C430,880 360,920 330,960",
    # para o Estábulo (sobe pela direita da Casa)
    "M760,905 C1000,900 1080,780 1045,640 C1015,520 900,470 880,330",
    # para a Plantação
    "M1010,520 C1100,440 1170,400 1290,370",
    # para o Pet Care
    "M1052,700 C1100,700 1150,690 1200,690",
    # para a Casinha
    "M790,985 C900,950 1050,960 1230,1010",
]


def fundo():
    rnd = random.Random(15)
    defs = (f'<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ceu"]}"/>'
            f'<stop offset="1" stop-color="{C["ceu_claro"]}"/></linearGradient>')
    s = f'<rect width="{FW}" height="{FH}" fill="url(#ceu)" stroke="none"/>'
    for i in range(6):
        s += nuvem(round(FW * (i + 0.5) / 6 + rnd.uniform(-60, 60)), round(rnd.uniform(40, 110)), round(rnd.uniform(22, 34)))
    # morros lá longe
    s += path(f"M0,{FY+150} Q{FW*0.18},{FY-30} {FW*0.38},{FY+80} T{FW*0.7},{FY+40} T{FW},{FY+90} L{FW},{FY+300} L0,{FY+300} Z", "#c7ebb0")
    s += path(f"M0,{FY+190} Q{FW*0.3},{FY+60} {FW*0.55},{FY+150} T{FW},{FY+120} L{FW},{FY+300} L0,{FY+300} Z", GRAMA_CLARA)
    # gramado
    s += path(f"M-5,{FY+230} Q{FW*0.25},{FY+170} {FW*0.5},{FY+200} T{FW+5},{FY+190} L{FW+5},{FH+5} L-5,{FH+5} Z", GRAMA)
    for _ in range(46):
        x, y = rnd.uniform(0, FW), rnd.uniform(FY + 280, FH)
        s += ell(round(x), round(y), round(rnd.uniform(60, 140)), round(rnd.uniform(20, 40)), GRAMA_CLARA, 'stroke="none" opacity="0.55"')
    # caminhos de terra (borda + miolo)
    g = f'<g transform="translate({FX},{FY})" fill="none" stroke-linecap="round" stroke-linejoin="round">'
    for d in CAMINHOS:
        g += f'<path d="{d}" stroke="{TERRA_BORDA}" stroke-width="62"/>'
    for d in CAMINHOS:
        g += f'<path d="{d}" stroke="{TERRA}" stroke-width="50"/>'
    g += "</g>"
    s += g
    for _ in range(170):
        x, y = rnd.uniform(0, FW), rnd.uniform(FY + 260, FH - 10)
        s += tufo(round(x), round(y), rnd.uniform(0.7, 1.1))
    for _ in range(90):
        x, y = rnd.uniform(0, FW), rnd.uniform(FY + 270, FH - 10)
        s += flor(round(x), round(y), 4, rnd.choice([C["rosa"], C["branco"], C["lilas"], C["amarelo"]]))
    return svg(FW, FH, s, defs)


# ---------------------------------------------------------------- lugares

def casa():
    w, h = 660, 450
    s = ell(330, 432, 320, 18, "#86c46f", 'stroke="none" opacity="0.6"')
    # corpo
    s += rr(70, 210, 520, 200, 6, "#ffc6dc", 'stroke-width="3.5"')
    for y in range(226, 410, 18):
        s += path(f"M74,{y} L586,{y}", extra='stroke-width="1.2" opacity="0.18"')
    # alas e telhados
    s += telhado_escamas("M20,220 L150,120 L520,120 L640,220 Z", ROXO_TELHA, C["roxo_esc"], 120, 230)
    s += rr(10, 212, 640, 18, 8, C["lilas_claro"], 'stroke-width="3"')
    # frontão central (rosa) com telhado roxo
    s += path("M220,250 L330,120 L440,250 Z", "#ffb0d0", 'stroke-width="3.5"')
    s += path("M200,262 L330,98 L460,262", extra=f'stroke="{ROXO_TELHA}" stroke-width="22"') + path("M196,262 L330,90 L464,262", extra='stroke-width="3"')
    s += janela(304, 160, 52, 52)
    # águas-furtadas
    for cx in (130, 520):
        s += rr(cx - 34, 150, 68, 64, 4, "#ffc6dc", 'stroke-width="3"')
        s += path(f"M{cx-48},{158} L{cx},{118} L{cx+48},{158} Z", ROXO_TELHA, 'stroke-width="3"')
        s += janela(cx - 18, 166, 36, 38)
    # chaminé
    s += rr(450, 60, 48, 76, 4, "#f7a8c8", 'stroke-width="3"') + rr(442, 52, 64, 16, 4, "#f7a8c8", 'stroke-width="3"')
    for y in (80, 100, 120):
        s += path(f"M452,{y} L496,{y}", extra='stroke-width="1.5" opacity="0.3"')
    # varanda
    s += rr(70, 390, 520, 26, 5, C["madeira_clara"], 'stroke-width="3"')
    s += rr(60, 270, 540, 16, 6, C["branco"], 'stroke-width="3"')
    for x in (78, 200, 460, 582):
        s += rr(x - 7, 284, 14, 108, 4, C["branco"], 'stroke-width="2.5"')
    for x0, x1 in ((84, 192), (468, 576)):
        s += rr(x0, 352, x1 - x0, 8, 3, C["branco"], 'stroke-width="2"')
        for x in range(x0 + 8, x1, 14):
            s += rr(x, 360, 6, 30, 2, C["branco"], 'stroke-width="1.5"')
    # janelas grandes com floreira
    for x in (100, 480):
        s += janela(x, 296, 80, 56)
        s += rr(x - 6, 352, 92, 14, 4, C["madeira_esc"], 'stroke-width="2.5"')
        for k in range(5):
            s += flor(x + 4 + k * 18, 350, 6, C["rosa_chiclete"] if k % 2 else C["lilas"])
    # porta de coração
    s += path("M290,392 L290,320 A40,40 0 0 1 370,320 L370,392 Z", "#f27fb5", 'stroke-width="3.5"')
    s += coracao(330, 330, 13, "#ffd6e8", 'stroke-width="2.5"') + circ(358, 360, 4, C["dourado"], 'stroke-width="2"')
    # guirlanda de flores sobre a porta
    for i in range(11):
        a = math.pi * (1 - i / 10)
        s += flor(round(330 + 62 * math.cos(a)), round(322 - 62 * math.sin(a)), 7, C["rosa"] if i % 2 else C["rosa_chiclete"])
    # balanço na varanda
    s += path("M540,286 L540,345 M580,286 L580,345", extra='stroke-width="2"') + rr(530, 342, 60, 12, 5, C["rosa_chiclete"], 'stroke-width="2.5"')
    # degraus e vasos
    s += rr(278, 408, 104, 14, 3, C["cinza"], 'stroke-width="2.5"') + rr(266, 420, 128, 14, 3, C["cinza"], 'stroke-width="2.5"')
    s += vaso_flores(250, 430, C["lilas"], [C["rosa"], C["branco"], C["rosa_chiclete"]])
    s += vaso_flores(412, 430, C["lilas"], [C["rosa_chiclete"], C["branco"], C["rosa"]])
    s += moita(110, 425, 22, C["verde"], [C["rosa"], C["lilas"]], n=5)
    s += moita(560, 425, 22, C["verde"], [C["rosa"], C["lilas"]], n=5)
    return svg(w, h, s)


def casa_arvore():
    w, h = 520, 480
    rnd = random.Random(7)
    s = ell(260, 462, 200, 16, "#86c46f", 'stroke="none" opacity="0.6"')
    # tronco e galhos
    s += path("M200,470 C215,400 205,330 190,250 L330,250 C315,330 305,400 330,470 Z", C["madeira_esc"], 'stroke-width="3.5"')
    s += path("M240,440 C245,400 238,350 232,300 M285,430 C282,380 290,330 296,290", extra='stroke-width="2" opacity="0.4"')
    s += path("M160,470 C190,455 200,440 205,430 M360,470 C330,455 320,440 318,430", extra='stroke-width="3"')
    # copa rosa (bolas)
    copa = [(260, 120, 120), (130, 150, 95), (390, 150, 95), (76, 240, 70), (444, 240, 70), (180, 60, 75), (340, 60, 75)]
    for x, y, r in copa:
        s += circ(x, y, r, "#ffb3d6", 'stroke-width="3.5"')
    for x, y, r in copa:
        s += circ(x, y, r - 3.5, "#ffb3d6", 'stroke="none"')
    for _ in range(70):
        x, y = rnd.uniform(10, 510), rnd.uniform(0, 310)
        if any((x - a) ** 2 + (y - b) ** 2 < (r - 10) ** 2 for a, b, r in copa):
            s += flor(round(x), round(y), rnd.choice([6, 7, 8]), rnd.choice(["#ff8cc6", "#ffd6e8", "#ff9ccc"]), "#ff6fae")
    # casinha
    s += rr(130, 250, 240, 26, 4, C["madeira"], 'stroke-width="3"')  # plataforma
    s += rr(150, 170, 200, 82, 4, "#ffd0e3", 'stroke-width="3.5"')
    s += path("M130,180 L250,100 L370,180 Z", ROXO_TELHA, 'stroke-width="3.5"')
    s += coracao(250, 150, 12, C["branco"], 'stroke-width="2.5"')
    s += path("M200,252 L200,205 A30,30 0 0 1 260,205 L260,252 Z", "#ffe7a8", 'stroke-width="3"')
    for i in range(5):
        s += path(f"M{205+i*11},{200} l5,9 l5,-9", C["rosa_chiclete"] if i % 2 else C["amarelo"], 'stroke-width="1.5"')
    s += janela(290, 196, 40, 34)
    # cerquinha da plataforma
    s += rr(126, 276, 248, 8, 3, C["madeira_clara"], 'stroke-width="2"')
    for x in range(132, 372, 16):
        s += rr(x, 260, 6, 22, 2, C["madeira_clara"], 'stroke-width="1.5"')
    # escada
    s += path("M330,284 L360,430 M366,284 L396,430", extra='stroke-width="5"')
    for k in range(6):
        y = 300 + k * 22
        s += path(f"M{333+k*4.4:.0f},{y} L{369+k*4.4:.0f},{y}", extra='stroke-width="4"')
    # lanterna pendurada
    s += path("M430,240 L430,262", extra='stroke-width="2"') + rr(420, 262, 20, 28, 5, "#fff0a8", 'stroke-width="2.5"')
    s += moita(120, 450, 28, C["verde"], [C["rosa"], C["branco"]], n=6) + moita(420, 452, 22, C["verde"], [C["rosa"]])
    return svg(w, h, s)


def estabulo():
    w, h = 540, 280
    s = ell(270, 262, 260, 16, "#86c46f", 'stroke="none" opacity="0.6"')
    # cerca em volta (atrás)
    s += f'<g transform="translate(0,130)">{cerca_trecho(130, 66)}</g><g transform="translate(410,130)">{cerca_trecho(130, 66)}</g>'
    # celeiro
    s += rr(120, 100, 300, 150, 4, "#ffb6d5", 'stroke-width="3.5"')
    for x in range(132, 420, 22):
        s += path(f"M{x},104 L{x},248", extra='stroke-width="1.2" opacity="0.2"')
    s += telhado_escamas("M95,110 L140,40 L270,8 L400,40 L445,110 Z", ROXO_TELHA, C["roxo_esc"], 8, 120, 16)
    s += path("M95,110 L140,40 L270,8 L400,40 L445,110", extra=f'stroke="{C["lilas_claro"]}" stroke-width="9"') + path("M95,110 L140,40 L270,8 L400,40 L445,110", extra='stroke-width="2.5" fill="none"')
    s += circ(270, 64, 24, C["branco"], 'stroke-width="3"') + coracao(270, 66, 13, C["rosa_forte"], 'stroke-width="2"')
    # portão aberto com feno dentro
    s += rr(205, 120, 130, 130, 4, "#a8716f", 'stroke-width="3"')
    s += rr(215, 196, 110, 54, 8, C["amarelo"], 'stroke-width="2.5"')
    for x in range(222, 320, 14):
        s += path(f"M{x},{204} l6,30", extra='stroke-width="1.5" opacity="0.5"')
    s += rr(205, 200, 130, 50, 3, C["madeira"], 'stroke-width="3"') + path("M205,200 L335,250 M335,200 L205,250", extra='stroke-width="3"')
    s += rr(190, 112, 160, 14, 4, C["madeira_clara"], 'stroke-width="2.5"')
    # floreiras
    for x in (150, 360):
        s += janela(x, 140, 36, 36, C["branco"], "#fff2b8")
        s += rr(x - 6, 178, 48, 10, 3, C["madeira_esc"], 'stroke-width="2"')
        for k in range(3):
            s += flor(x + 4 + k * 14, 177, 6, C["rosa_chiclete"])
    # fardo de feno
    s += rr(70, 210, 70, 44, 6, C["amarelo"], 'stroke-width="3"') + path("M75,226 L135,226 M75,240 L135,240", extra='stroke-width="1.5" opacity="0.5"')
    return svg(w, h, s)


def horta():
    w, h = 380, 250
    rnd = random.Random(3)
    s = ell(190, 236, 180, 14, "#86c46f", 'stroke="none" opacity="0.6"')
    # arco de flores atrás
    s += path("M120,140 L120,40 C120,0 260,0 260,40 L260,140", extra=f'stroke="{C["madeira_esc"]}" stroke-width="10"')
    s += path("M120,140 L120,40 C120,0 260,0 260,40 L260,140", extra=f'stroke="{C["madeira"]}" stroke-width="5"')
    for i in range(13):
        t = i / 12
        x = 120 + 140 * t
        y = 40 - 34 * math.sin(math.pi * t) if 0 < t < 1 else 40
        s += circ(round(x), round(y), 9, C["verde"], 'stroke-width="2"') + flor(round(x), round(y), 5, C["rosa_chiclete"] if i % 2 else C["rosa"])
    # canteiros elevados
    def canteiro(x, y, w2, h2, plantas):
        c = rr(x, y, w2, h2, 6, C["madeira"], 'stroke-width="3"') + rr(x + 8, y + 6, w2 - 16, h2 * 0.45, 4, "#a0715a", 'stroke-width="2"')
        c += path(f"M{x},{y+h2*0.7:.0f} L{x+w2},{y+h2*0.7:.0f}", extra='stroke-width="1.5" opacity="0.4"')
        return c + plantas
    s += canteiro(40, 90, 150, 60, "".join(
        circ(60 + i * 26, 92, 8, C["verde_esc"], 'stroke-width="2"') + circ(60 + i * 26, 88, 6, C["vermelho_rosa"], 'stroke-width="2"') for i in range(6)))
    s += canteiro(200, 95, 150, 60, "".join(
        path(f"M{214+i*22},{100} l-4,-22 M{214+i*22},{100} l0,-26 M{214+i*22},{100} l5,-22", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') for i in range(6)))
    s += canteiro(20, 160, 160, 62, "".join(
        circ(44 + i * 28, 168, 13, C["verde_claro"], 'stroke-width="2.5"') + circ(44 + i * 28, 168, 6, C["verde"], 'stroke-width="1.5"') for i in range(5)))
    s += canteiro(190, 165, 150, 62, "".join(
        path(f"M{206+i*22},{176} l-5,10 l10,0 Z", C["laranja"], 'stroke-width="2"') + path(f"M{211+i*22},{172} l-5,-14 M{211+i*22},{172} l5,-14", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') for i in range(6)))
    # regador
    s += path("M330,215 L330,185 L364,185 L364,215 Z", C["rosa"], 'stroke-width="2.5"') + path("M330,195 L304,178", extra='stroke-width="5"')
    s += path("M338,186 C340,170 354,170 356,186", extra='stroke-width="2.5"') + coracao(347, 200, 6, C["branco"], 'stroke-width="1.5"')
    s += "".join(flor(round(rnd.uniform(20, 360)), round(rnd.uniform(230, 245)), 4, C["rosa"]) for _ in range(5))
    return svg(w, h, s)


def pet_care():
    w, h = 420, 300
    s = ell(210, 284, 200, 14, "#86c46f", 'stroke="none" opacity="0.6"')
    s += rr(40, 230, 340, 40, 8, C["madeira_clara"], 'stroke-width="3"')  # piso
    for x in range(60, 380, 28):
        s += path(f"M{x},232 L{x},268", extra='stroke-width="1.2" opacity="0.3"')
    for x in (62, 358):
        s += rr(x - 10, 100, 20, 140, 4, C["madeira"], 'stroke-width="3"')
    s += telhado_escamas("M0,112 L80,20 L340,20 L420,112 Z", ROSA_TELHA, C["rosa_forte"], 20, 120, 16)
    s += rr(-2, 106, 424, 14, 5, C["rosa_claro"], 'stroke-width="3"')
    s += circ(210, 66, 30, C["branco"], 'stroke-width="3"')
    for dx, dy in ((-13, -10), (-4, -16), (6, -16), (14, -10)):
        s += ell(210 + dx, 66 + dy, 5, 6, C["rosa_forte"], 'stroke-width="1.5"')
    s += ell(210, 74, 13, 10, C["rosa_forte"], 'stroke-width="1.5"')
    # banheira com bolhas
    s += path("M150,200 L270,200 L262,240 L158,240 Z", C["rosa"], 'stroke-width="3"') + rr(144, 192, 132, 12, 6, C["rosa_claro"], 'stroke-width="2.5"')
    for k in range(7):
        s += circ(162 + k * 16, 188 - (k % 2) * 6, 9, "#dff1ff", 'stroke-width="2"')
    s += path("M180,240 L172,256 M240,240 L248,256", extra='stroke-width="4"')
    s += coracao(210, 222, 7, C["branco"], 'stroke-width="1.5"')
    # prateleira com potes, toalhas, caminha e tigela
    s += rr(120, 140, 70, 8, 3, C["madeira_esc"], 'stroke-width="2"')
    s += rr(126, 120, 14, 20, 3, C["lilas"], 'stroke-width="2"') + rr(146, 116, 14, 24, 3, C["azul"], 'stroke-width="2"') + rr(166, 122, 14, 18, 3, C["rosa"], 'stroke-width="2"')
    s += path("M300,130 L350,130", extra='stroke-width="3"') + rr(306, 130, 16, 40, 3, C["rosa_chiclete"], 'stroke-width="2"') + rr(328, 130, 16, 34, 3, C["lilas"], 'stroke-width="2"')
    s += ell(340, 262, 46, 18, C["rosa_chiclete"], 'stroke-width="3"') + ell(340, 258, 32, 10, C["rosa_claro"], 'stroke-width="2"')
    s += ell(92, 258, 22, 9, C["lilas"], 'stroke-width="2.5"') + ell(92, 254, 14, 4, C["madeira_esc"], 'stroke-width="1.5"')
    s += vaso_flores(40, 270, C["rosa"], [C["rosa_chiclete"], C["branco"], C["rosa"]])
    return svg(w, h, s)


def cabana():
    w, h = 300, 230
    s = ell(150, 214, 140, 14, "#86c46f", 'stroke="none" opacity="0.6"')
    s += ell(170, 200, 70, 16, C["rosa_claro"], 'stroke-width="2.5"') + ell(170, 200, 46, 9, C["rosa"], 'stroke-width="1.5"')
    s += path("M40,200 L150,40 L270,200 Z", C["lilas"], 'stroke-width="3.5"')
    s += path("M150,40 L196,200 L270,200 Z", "#c4a2f0", 'stroke-width="3"')
    s += path("M150,40 L120,200 L196,200 Z", "#f6b4d8", 'stroke-width="3"')
    s += path("M150,40 L128,14 M150,40 L176,12", extra='stroke-width="5"')
    for k in range(7):
        x = 64 + k * 26
        s += circ(x, 92 + abs(k - 3) * 14, 5, "#fff3a0", 'stroke-width="1.5"')
    s += path("M64,140 Q150,66 238,140", extra='stroke-width="1.5"')
    s += rr(150, 170, 34, 14, 5, C["rosa_chiclete"], 'stroke-width="2"') + rr(150, 156, 26, 16, 5, C["amarelo"], 'stroke-width="2"')
    # lanterna e toco
    s += rr(36, 166, 52, 40, 8, C["madeira_esc"], 'stroke-width="3"') + ell(62, 166, 26, 7, C["madeira_clara"], 'stroke-width="2.5"')
    s += rr(50, 124, 24, 36, 6, "#fff0a8", 'stroke-width="2.5"') + rr(46, 118, 32, 8, 3, C["madeira_esc"], 'stroke-width="2"')
    s += ell(270, 206, 22, 12, C["cinza"], 'stroke-width="2.5"')
    return svg(w, h, s)


def entrada():
    w, h = 480, 280
    s = ell(240, 266, 230, 12, "#86c46f", 'stroke="none" opacity="0.6"')
    # pilares de pedra
    for x in (30, 380):
        s += rr(x, 170, 70, 96, 10, C["cinza"], 'stroke-width="3"')
        for y, o in ((190, 0), (212, 18), (234, 0)):
            s += path(f"M{x},{y} L{x+70},{y} M{x+20+o},{y-22} L{x+20+o},{y}", extra='stroke-width="1.5" opacity="0.45"')
    # postes e arco de madeira
    for x in (60, 410):
        s += rr(x - 4, 60, 18, 120, 5, C["madeira_esc"], 'stroke-width="3"')
    s += path("M60,80 C120,0 360,0 424,80", extra=f'stroke="{C["madeira_esc"]}" stroke-width="30"')
    s += path("M60,80 C120,0 360,0 424,80", extra=f'stroke="{C["madeira"]}" stroke-width="22"')
    for i in range(16):
        t = i / 15
        x = (1 - t) ** 3 * 60 + 3 * (1 - t) ** 2 * t * 120 + 3 * (1 - t) * t ** 2 * 360 + t ** 3 * 424
        y = (1 - t) ** 3 * 80 + 3 * (1 - t) ** 2 * t * 0 + 3 * (1 - t) * t ** 2 * 0 + t ** 3 * 80
        if i % 2 == 0:
            s += circ(round(x), round(y) - 2, 11, C["verde"], 'stroke-width="2"')
        s += flor(round(x), round(y) - 4, 7, C["rosa_chiclete"] if i % 3 else C["rosa"])
    # coração no topo
    s += rr(200, 12, 84, 62, 14, C["madeira_clara"], 'stroke-width="3"') + coracao(242, 44, 22, C["rosa_forte"], 'stroke-width="2.5"')
    # plaquinha pendurada (em branco; o jogo escreve "Entrada")
    s += path("M180,60 L170,100 M300,60 L310,100", extra='stroke-width="2.5"')
    # flores na base
    s += moita(60, 262, 26, C["verde"], [C["rosa"], C["lilas"], C["branco"]], n=6) + moita(420, 262, 26, C["verde"], [C["rosa"], C["lilas"], C["branco"]], n=6)
    return svg(w, h, s)


def casinha():
    w, h = 380, 280
    s = ell(190, 264, 180, 14, "#86c46f", 'stroke="none" opacity="0.6"')
    s += rr(60, 100, 260, 150, 4, "#ffd2e4", 'stroke-width="3.5"')
    for y in range(116, 250, 16):
        s += path(f"M64,{y} L316,{y}", extra='stroke-width="1.2" opacity="0.18"')
    s += telhado_escamas("M40,108 L90,30 L290,30 L340,108 Z", ROSA_TELHA, C["rosa_forte"], 30, 116, 15)
    # toldo listrado
    for i in range(9):
        x = 60 + i * 29
        s += path(f"M{x},110 L{x+29},110 L{x+29},140 Q{x+14.5},156 {x},140 Z", C["rosa_forte"] if i % 2 == 0 else C["branco"], 'stroke-width="2.5"')
    # balcão com vitrine
    s += rr(80, 150, 220, 60, 4, "#fff6e0", 'stroke-width="2.5"')
    s += rr(90, 160, 200, 8, 2, C["madeira_esc"], 'stroke-width="1.5"') + rr(90, 186, 200, 8, 2, C["madeira_esc"], 'stroke-width="1.5"')
    for k, cor in enumerate([C["lilas"], C["rosa"], C["amarelo"], C["azul"], C["rosa_chiclete"], C["verde"]]):
        s += rr(98 + k * 32, 168 + (k % 2) * 2, 18, 18 - (k % 2) * 2, 4, cor, 'stroke-width="1.5"')
    # ursinho de pelúcia (bicho de brinquedo, não personagem)
    s += circ(255, 176, 12, C["madeira"], 'stroke-width="2"') + circ(246, 166, 5, C["madeira"], 'stroke-width="1.5"') + circ(264, 166, 5, C["madeira"], 'stroke-width="1.5"')
    s += rr(70, 210, 240, 40, 4, "#ffb6d5", 'stroke-width="3"') + coracao(190, 230, 10, C["branco"], 'stroke-width="2"')
    # lampião e lousinha (em branco)
    s += path("M330,120 L330,140", extra='stroke-width="2"') + rr(322, 140, 16, 22, 4, "#fff0a8", 'stroke-width="2"')
    s += path("M310,262 L330,190 L350,262 M330,190 L330,262", extra='stroke-width="3"') + rr(312, 196, 36, 44, 4, "#5c4a55", 'stroke-width="2.5"')
    s += coracao(330, 218, 9, "none", 'stroke="#ffffff" stroke-width="2"')
    s += vaso_flores(46, 258, C["rosa"], [C["rosa_chiclete"], C["branco"], C["rosa"]])
    return svg(w, h, s)


# ---------------------------------------------------------------- decoração

def arvore(copa, flores=None, seed=1, w=200, h=210):
    rnd = random.Random(seed)
    s = ell(w / 2, h - 10, w * 0.32, 10, "#86c46f", 'stroke="none" opacity="0.6"')
    s += path(f"M{w/2-14},{h-12} C{w/2-10},{h-60} {w/2-12},{h-90} {w/2-10},{h*0.5} L{w/2+10},{h*0.5} C{w/2+12},{h-90} {w/2+10},{h-60} {w/2+14},{h-12} Z", C["madeira_esc"], 'stroke-width="3"')
    bl = [(w / 2, 62, 58), (w / 2 - 52, 92, 44), (w / 2 + 52, 92, 44), (w / 2, 112, 48)]
    for x, y, r in bl:
        s += circ(x, y, r, copa, 'stroke-width="3"')
    for x, y, r in bl:
        s += circ(x, y, r - 3, copa, 'stroke="none"')
    for _ in range(int(w / 9)):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(10, 150)
        if any((x - a) ** 2 + (y - b) ** 2 < (r - 9) ** 2 for a, b, r in bl):
            s += flor(round(x), round(y), 6, flores, C["rosa_forte"]) if flores else path(
                f"M{x:.0f},{y:.0f} q6,-6 12,0", extra=f'stroke="{GRAMA_ESC}" stroke-width="2"')
    return svg(w, h, s)


def pinheiro(w=130, h=210):
    s = ell(w / 2, h - 8, w * 0.35, 8, "#86c46f", 'stroke="none" opacity="0.6"')
    s += rr(w / 2 - 10, h - 40, 20, 34, 3, C["madeira_esc"], 'stroke-width="3"')
    for k, (y0, y1, a) in enumerate(((h - 40, h - 110, 62), (h - 90, h - 160, 50), (h - 140, 10, 38))):
        s += path(f"M{w/2-a},{y0} L{w/2},{y1} L{w/2+a},{y0} Q{w/2},{y0+12} {w/2-a},{y0} Z", "#6fb766", 'stroke-width="3"')
    return svg(w, h, s)


def lago():
    w, h = 200, 100
    s = path("M20,50 C20,10 180,8 186,46 C192,86 30,94 20,50 Z", C["agua"], 'stroke-width="3.5"')
    s += path("M50,40 C70,32 100,32 120,38", extra=f'stroke="{C["branco"]}" stroke-width="3" opacity="0.8"')
    for x, y in ((70, 60), (130, 52), (100, 72)):
        s += path(f"M{x},{y} m-14,0 a14,9 0 1 0 28,0 a14,9 0 1 0 -28,0", C["verde"], 'stroke-width="2"')
    s += flor(130, 50, 6, C["rosa"], C["amarelo"]) + flor(72, 58, 5, C["rosa_chiclete"], C["amarelo"])
    for x, y, r in ((12, 58, 12), (190, 42, 11), (176, 76, 13), (36, 82, 10), (110, 92, 12)):
        s += ell(x, y, r, r * 0.7, C["cinza"], 'stroke-width="2.5"')
    return svg(w, h, s)


def pedras():
    w, h = 90, 120
    s = ""
    for x, y, r in ((40, 18, 20), (52, 52, 22), (36, 86, 22), (54, 110, 18)):
        s += ell(x, y, r, r * 0.55, "#ece4ea", 'stroke-width="2.5"')
    return svg(w, h, s)


def flores():
    w, h = 120, 60
    return svg(w, h, moita(60, 44, 20, C["verde"], [C["rosa"], C["rosa_chiclete"], C["lilas"]], n=7))


def arbusto():
    w, h = 110, 70
    return svg(w, h, moita(55, 50, 24, C["verde"]))


# ---------------------------------------------------------------- interface (placas SEM letras)

def placa_titulo():
    w, h = 380, 200
    s = rr(20, 40, 340, 140, 36, C["madeira_esc"], 'stroke-width="4"') + rr(32, 50, 316, 120, 30, C["madeira"], 'stroke-width="2.5"')
    s += path("M50,80 C120,74 260,74 330,80 M46,130 C120,124 260,124 334,130", extra='stroke-width="1.5" opacity="0.3"')
    s += coracao(190, 30, 26, C["rosa_forte"], 'stroke-width="3"')
    for x, y in ((30, 150), (350, 150), (40, 60), (342, 58)):
        s += circ(x, y, 14, C["verde"], 'stroke-width="2"') + flor(x, y, 8, C["rosa"], C["amarelo"])
    return svg(w, h, s)


def placa_nome():
    w, h = 240, 64
    s = rr(4, 6, 232, 52, 26, "#e8b98f", 'stroke="none" opacity="0.7"')
    s += rr(4, 2, 232, 52, 26, "#fff2e2", 'stroke-width="3"')
    return svg(w, h, s)


def faixa_aviso():
    w, h = 700, 84
    s = rr(16, 10, 668, 64, 32, "#fff2e2", 'stroke-width="3.5"')
    for x, a in ((10, -1), (690, 1)):
        for k, dy in enumerate((-16, 0, 16)):
            s += path(f"M{x},{42+dy} l{a*-10},{dy*0.4:.0f}", extra=f'stroke="{C["rosa_forte"]}" stroke-width="4"')
    return svg(w, h, s)


def marcador():
    w, h = 130, 150
    s = path("M65,146 L44,110 L86,110 Z", C["rosa_forte"], 'stroke-width="3"')
    s += circ(65, 62, 58, C["rosa_forte"], 'stroke-width="3.5"') + circ(65, 62, 50, C["branco"], 'stroke-width="2.5"')
    return svg(w, h, s)


def botao_fechar():
    w, h = 110, 110
    s = circ(55, 58, 48, "#e9a9c6", 'stroke="none"') + circ(55, 53, 48, C["branco"], 'stroke-width="4"')
    s += path("M36,34 L74,72 M74,34 L36,72", extra=f'stroke="{C["rosa_forte"]}" stroke-width="13"')
    return svg(w, h, s)


# ---------------------------------------------------------------- montagem

P.update(fundo=fundo(), casa=casa(), casa_arvore=casa_arvore(), estabulo=estabulo(), horta=horta(), pet_care=pet_care(),
         cabana=cabana(), entrada=entrada(), casinha=casinha(),
         arvore=arvore(C["verde"], None, 2), arvore_rosa=arvore("#ffb3d6", "#ff8cc6", 5), pinheiro=pinheiro(),
         lago=lago(), pedras=pedras(), flores=flores(), arbusto=arbusto(), cerca=svg(300, 62, cerca_trecho(300, 62)),
         placa_titulo=placa_titulo(), placa_nome=placa_nome(), faixa_aviso=faixa_aviso(), marcador=marcador(),
         botao_fechar=botao_fechar())

# (peça, x, y) em pixels do mapa 1600 × 1200, na ordem de desenho (de trás para a frente)
DECOR = [
    ("arvore", 540, -40), ("arvore", 1060, -30), ("arvore_rosa", 1450, -10),
    ("cerca", 470, 120), ("cerca", 770, 120), ("cerca", 1170, 140), ("cerca", 1440, 150),
    ("arvore", 1470, 330), ("arvore", 1480, 640),
    ("pinheiro", -10, 520), ("pinheiro", 70, 600), ("pinheiro", -20, 700),
    ("arbusto", 380, 330), ("flores", 980, 380), ("flores", 1110, 340), ("flores", 250, 600),
    ("flores", 600, 1060), ("flores", 930, 1070), ("arbusto", 1060, 870), ("arbusto", 440, 1000),
    ("pedras", 690, 780), ("lago", 850, 730),
    ("cerca", -40, 1060), ("cerca", 250, 1040), ("cerca", 1010, 1050), ("cerca", 1310, 1060),
    ("flores", -10, 1140), ("flores", 1500, 1130),
]
# lugar -> peça, posição e nome (o nome vai numa placa_nome embaixo; destinos = cenários do jogo)
LUGARES = {
    "casa_arvore": dict(x=-10, y=40, rotulo="Casa na Árvore", placa=(200, 496),
                        destinos=[["casa_arvore", "Pátio"], ["casa_arvore_dentro", "Dentro"]]),
    "estabulo": dict(x=630, y=40, rotulo="Estábulo", placa=(960, 330), destinos=[["estabulo", ""]]),
    "horta": dict(x=1190, y=105, rotulo="Plantação", placa=(1350, 352), destinos=[["plantacao", ""]]),
    "casa": dict(x=300, y=330, rotulo="Casa", placa=(545, 795),
                 destinos=[["sede", "Varanda"], ["sala", "Sala"], ["cozinha", "Cozinha"],
                           ["quarto", "Quarto"], ["quarto_carol", "Quarto da mamãe"]]),
    "pet_care": dict(x=1090, y=395, rotulo="Pet Care", placa=(1282, 700), destinos=[["pet_care", ""]]),
    "cabana": dict(x=100, y=750, rotulo="Cabana", placa=(270, 1000), destinos=[["cabana", ""]]),
    "entrada": dict(x=560, y=830, rotulo="Entrada", placa=(800, 950), destinos=[["entrada", ""]]),
    "casinha": dict(x=1150, y=730, rotulo="Casinha", placa=(1320, 1010), destinos=[["casinha", ""]]),
}
# Peças 3D da Carol para o mapa (arte/interface/mapa_fazenda/novo3d/): entram no jogo no lugar da 2D.
NOVO3D = os.path.join(base, "novo3d")
if os.path.exists(os.path.join(NOVO3D, "casa_arvore.png")):  # casa na árvore inteira, com nuvem (15/11/2026)
    import re
    P["casa_arvore"] = re.sub(r'width="[^"]+" height="[^"]+"', 'width="640" height="480" preserveAspectRatio="none"',
                              P["casa_arvore"], count=1)
    LUGARES["casa_arvore"].update(x=-60, placa=(230, 496))
ORDEM = ["casa_arvore", "estabulo", "horta", "pet_care", "casa", "cabana", "casinha", "entrada"]
MARCA_X, MARCA_Y = 0.5, 0.22   # ponta do marcador "você está aqui": fração da peça do lugar
UI = dict(titulo=(10, 10), fechar=(1470, 20), faixa=(450, 1100),
          titulo_texto=["Fazenda", "Capricho"], faixa_texto="Toque em um lugar para brincar")

os.makedirs(d2, exist_ok=True)
salvar(P, os.path.join(d2, "svg"), d2)


def dados():
    d = {"tela": [W, H], "fundo": [-FX, -FY, FW, FH], "decoracao": [], "lugares": {}, "ordem": ORDEM, "ui": {}}
    for nome, x, y in DECOR:
        w, h = tam(nome)
        d["decoracao"].append([nome, x, y, w, h])
    for k, l in LUGARES.items():
        w, h = tam(k)
        d["lugares"][k] = {"rect": [l["x"], l["y"], w, h], "rotulo": l["rotulo"], "placa": list(l["placa"]), "destinos": l["destinos"]}
    tw, th = tam("placa_titulo")
    fw, fh = tam("faixa_aviso")
    d["ui"] = {"titulo": [UI["titulo"][0], UI["titulo"][1], tw, th], "titulo_texto": UI["titulo_texto"],
               "fechar": [UI["fechar"][0], UI["fechar"][1], 110, 110], "faixa": [UI["faixa"][0], UI["faixa"][1], fw, fh],
               "faixa_texto": UI["faixa_texto"], "marcador": list(tam("marcador")), "marcador_ponta": [MARCA_X, MARCA_Y], "placa_nome": list(tam("placa_nome"))}
    return d


D = dados()
with open(os.path.join(raiz, "prototipo/dados/mapa_fazenda.json"), "w", encoding="utf-8") as f:
    json.dump(D, f, ensure_ascii=False, indent=1)


def peca(nome, w, h):
    return Image.open(os.path.join(d2, nome + ".png")).convert("RGBA").resize((round(w), round(h)), Image.LANCZOS)


def texto_centro(dr, cx, cy, t, tamanho, cor="#a3336f", contorno=None):
    f = ImageFont.truetype(FONTE, tamanho)
    bb = dr.textbbox((0, 0), t, font=f)
    x, y = cx - (bb[2] + bb[0]) / 2, cy - (bb[3] + bb[1]) / 2
    if contorno:
        dr.text((x, y), t, font=f, fill=cor, stroke_width=contorno[0], stroke_fill=contorno[1])
    else:
        dr.text((x, y), t, font=f, fill=cor)


def montar(saida, rotulos):
    tela = Image.new("RGBA", (W, H), "white")
    tela.alpha_composite(peca("fundo", FW, FH).crop((FX, FY, FX + W, FY + H)))
    caixas = []

    def por(nome, x, y, w, h):
        im = peca(nome, w, h)
        tela.alpha_composite(im, (round(x), round(y))) if x >= 0 and y >= 0 else tela.paste(im, (round(x), round(y)), im)
        caixas.append((nome, x, y, w, h))
    for nome, x, y, w, h in D["decoracao"]:
        por(nome, x, y, w, h)
    for k in ORDEM:
        x, y, w, h = D["lugares"][k]["rect"]
        por(k, x, y, w, h)
    dr = ImageDraw.Draw(tela)
    pw, ph = D["ui"]["placa_nome"]
    for k in ORDEM:
        l = D["lugares"][k]
        f = ImageFont.truetype(FONTE, 34)
        larg = max(pw, dr.textlength(l["rotulo"], font=f) + 60)
        cx, cy = l["placa"]
        por("placa_nome", cx - larg / 2, cy - ph / 2, larg, ph)
        dr = ImageDraw.Draw(tela)
        if not rotulos:
            texto_centro(dr, cx, cy - 3, l["rotulo"], 34)
    x, y, w, h = D["ui"]["titulo"]
    por("placa_titulo", x, y, w, h)
    x, y, w, h = D["ui"]["faixa"]
    por("faixa_aviso", x, y, w, h)
    x, y, w, h = D["ui"]["fechar"]
    por("botao_fechar", x, y, w, h)
    mw, mh = D["ui"]["marcador"]
    lx, ly, lw, lh = D["lugares"]["casa"]["rect"]
    cx = lx + lw * MARCA_X
    my = ly + lh * MARCA_Y - mh
    por("marcador", cx - mw / 2, my, mw, mh)
    dr = ImageDraw.Draw(tela)
    if not rotulos:
        cat = Image.open(os.path.join(raiz, "arte/personagens/catarina.png")).convert("RGBA")
        cat = cat.crop(cat.getbbox())
        rosto = cat.crop((round(cat.width * 0.12), 0, round(cat.width * 0.88), round(cat.width * 0.76))).resize((100, 100), Image.LANCZOS)
        m = Image.new("L", (100, 100), 0)
        ImageDraw.Draw(m).ellipse((0, 0, 99, 99), fill=255)
        tela.paste(rosto, (round(cx - 50), round(my + 12)), Image.composite(rosto.getchannel("A"), m, m))
        x, y, w, h = D["ui"]["titulo"]
        branco = (255, 255, 255)
        texto_centro(dr, x + w / 2, y + 88, UI["titulo_texto"][0], 46, "#ffffff", (5, "#a3336f"))
        texto_centro(dr, x + w / 2, y + 138, UI["titulo_texto"][1], 50, "#ffc2df", (5, "#a3336f"))
        del branco
        x, y, w, h = D["ui"]["faixa"]
        texto_centro(dr, x + w / 2, y + h / 2 - 2, UI["faixa_texto"], 38)
    else:
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        except OSError:
            f = ImageFont.load_default()
        for nome, x, y, w, h in caixas:
            dr.rectangle((x, y, x + w, y + h), outline=(200, 40, 140), width=2)
        for nome, x, y, w, h in caixas:
            t = f"{nome} {round(w)}×{round(h)}"
            tw = dr.textlength(t, font=f)
            tx, ty = max(2, x + 3), max(2, y + 3)
            dr.rectangle((tx - 2, ty - 1, tx + tw + 3, ty + 18), fill=(255, 255, 255, 215))
            dr.text((tx, ty), t, fill=(150, 20, 100), font=f)
    tela.convert("RGB").save(saida)


montar(os.path.join(base, "mapa_fazenda_previa.png"), False)
montar(os.path.join(base, "mapa_fazenda_layout.png"), True)
os.makedirs(jogo, exist_ok=True)
_cat = Image.open(os.path.join(raiz, "arte/personagens/catarina.png")).convert("RGBA")
_cat = _cat.crop(_cat.getbbox())
_r = _cat.crop((round(_cat.width * 0.12), 0, round(_cat.width * 0.88), round(_cat.width * 0.76))).resize((200, 200), Image.LANCZOS)
_m = Image.new("L", (800, 800), 0)
ImageDraw.Draw(_m).ellipse((0, 0, 799, 799), fill=255)
_m = _m.resize((200, 200), Image.LANCZOS)
_fundo = Image.new("RGBA", (200, 200), "#ffe3ef")
_fundo.alpha_composite(_r)
_fundo.putalpha(_m)
_fundo.save(os.path.join(jogo, "_rosto_catarina.png"))
import pecas3d  # noqa: E402
for f in os.listdir(d2):
    if f.endswith(".png"):
        im3 = pecas3d.montar(f[:-4], NOVO3D, d2)
        if im3 is not None:
            im3.save(os.path.join(jogo, f))
        else:
            shutil.copyfile(os.path.join(d2, f), os.path.join(jogo, f))
print(len(P), "peças em", d2)
