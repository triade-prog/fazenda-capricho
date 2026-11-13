"""Peças 2D provisórias do Estábulo florido + pasto.

Uso: python3 ferramentas/cenario2d/estabulo.py
Saída: arte/cenario/estabulo/2d/*.png (mesmos nomes da lista de entrega do PROMPTS.md).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, nuvem, salvar  # noqa: E402

P = {}


def margarida(cx, cy, r):
    s = ""
    for i in range(8):
        a = 2 * math.pi * i / 8
        s += ell(round(cx + r * math.cos(a), 1), round(cy + r * math.sin(a), 1), r * 0.62, r * 0.32, C["branco"],
                 f'stroke-width="1.8" transform="rotate({math.degrees(a):.0f} {cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f})"')
    return s + circ(cx, cy, r * 0.45, C["amarelo"], 'stroke-width="1.8"')


def fundo():
    w, h, chao, div = 3300, 900, 600, 1500
    rnd = random.Random(11)
    defs = (f'<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ceu"]}"/>'
            f'<stop offset="1" stop-color="{C["ceu_claro"]}"/></linearGradient>')
    s = f'<rect width="{w}" height="{h}" fill="url(#ceu)" stroke="none"/>'
    for cx, cy, k in [(1800, 110, 44), (2400, 70, 36), (3000, 140, 46), (600, 60, 30)]:
        s += nuvem(cx, cy, k)
    # pasto: morros, cerca, grama
    s += path(f"M{div-40},{chao-40} Q2000,{chao-260} 2500,{chao-120} T{w},{chao-170} L{w},{chao} L{div-40},{chao} Z",
              C["verde_claro"])
    s += path(f"M{div-40},{chao-10} Q2300,{chao-150} 2900,{chao-40} T{w},{chao-60} L{w},{chao} L{div-40},{chao} Z", "#a8dd8f")
    y0 = chao - 70
    s += rr(div, y0 + 14, w - div, 12, 4, C["branco"]) + rr(div, y0 + 42, w - div, 12, 4, C["branco"])
    for x in range(div + 10, w, 52):
        s += path(f"M{x},{chao+6} L{x},{y0+6} L{x+11},{y0-6} L{x+22},{y0+6} L{x+22},{chao+6} Z", C["branco"], 'stroke-width="2.5"')
    s += rr(div - 20, chao, w - div + 30, h - chao + 5, 0, "#8fd17a")
    for _ in range(90):
        x, y = rnd.uniform(div + 20, w - 10), rnd.uniform(chao + 20, h - 10)
        s += path(f"M{x:.0f},{y:.0f} l-5,-12 M{x:.0f},{y:.0f} l0,-15 M{x:.0f},{y:.0f} l6,-12",
                  extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
    for _ in range(45):
        x, y = rnd.uniform(div + 20, w - 15), rnd.uniform(chao + 25, h - 15)
        s += flor(round(x), round(y), 5, rnd.choice([C["rosa"], C["branco"], C["lilas"], C["amarelo"]]))
    # estábulo: parede de tábuas cor de mel
    s += rr(-5, 110, div + 5, chao - 110, 0, C["mel"], 'stroke-width="4"')
    for x in range(0, div, 50):
        s += rr(x, 110, 50, chao - 110, 0, "#e3a257" if (x // 50) % 2 else C["mel"], 'stroke-width="1.5" stroke-opacity="0.5"')
    for x in (20, 740, 1460):
        s += rr(x, 120, 30, chao - 120, 4, C["madeira_esc"])
    s += rr(-5, 150, div + 5, 22, 3, C["madeira_esc"])           # viga
    # telhado vermelho-rosado
    s += path(f"M-5,135 L750,55 L{div+40},135 L{div+40},165 L750,85 L-5,165 Z", C["vermelho_rosa"], 'stroke-width="4"')
    # flores penduradas
    for i, x in enumerate(range(80, div - 40, 120)):
        s += path(f"M{x},172 L{x},{196 + (i % 2) * 14}", extra='stroke-width="2"')
        s += flor(x, 206 + (i % 2) * 14, 10, C["rosa"] if i % 2 else C["lilas"], C["rosa_forte"])
    # chão de palha
    s += rr(-5, chao, div + 5, h - chao + 5, 0, "#f0d27a")
    for _ in range(260):
        x, y = rnd.uniform(5, div - 10), rnd.uniform(chao + 10, h - 6)
        a = rnd.uniform(-0.5, 0.5)
        s += path(f"M{x:.0f},{y:.0f} l{30*math.cos(a):.0f},{30*math.sin(a):.0f}",
                  extra=f'stroke="{rnd.choice(["#d9b44f", "#c99c3a", "#f7e29b"])}" stroke-width="2.5"')
    s += path(f"M{div},{110} L{div},{h}", extra='stroke-width="4"')
    return svg(w, h, s, defs)


P["fundo"] = fundo()


def meia_porta(aberta):
    w, h = 300, 170
    s = rr(0, 0, 18, h, 4, C["madeira_esc"])                             # batente fixo
    if not aberta:
        s += rr(14, 10, 282, 156, 8, C["madeira"], 'stroke-width="4"')
        s += rr(14, 10, 282, 22, 6, C["madeira_esc"]) + rr(14, 144, 282, 22, 6, C["madeira_esc"])
        s += path("M30,36 L278,140 M30,140 L278,36", extra='stroke-width="18"')
        s += path("M30,36 L278,140 M30,140 L278,36", extra=f'stroke-width="12" stroke="{C["madeira_esc"]}"')
        s += circ(155, 88, 30, C["madeira"]) + coracao(155, 90, 18, C["rosa_forte"])
    else:
        s += rr(14, 10, 66, 156, 8, C["madeira"], 'stroke-width="4"')
        s += rr(14, 10, 66, 22, 6, C["madeira_esc"]) + rr(14, 144, 66, 22, 6, C["madeira_esc"])
        s += path("M24,40 L70,136 M24,136 L70,40", extra=f'stroke-width="10" stroke="{C["madeira_esc"]}"')
    return svg(w, h, s)


P["meia_porta_fechada"] = meia_porta(False)
P["meia_porta_aberta"] = meia_porta(True)


def cocho(conteudo):
    w, h = 220, 100
    s = rr(20, 70, 16, 28, 3, C["madeira_esc"]) + rr(184, 70, 16, 28, 3, C["madeira_esc"])
    if conteudo == "feno":
        for i in range(16):
            x = 18 + i * 12
            s += path(f"M{x},44 q8,-22 16,0", "#f0d27a", 'stroke-width="2.5"')
    elif conteudo == "cenouras":
        for x, a in [(40, -30), (70, 20), (100, -15), (130, 25), (160, -20), (182, 10)]:
            s += path(f"M{x-20},40 L{x+18},34 L{x-16},50 Z", C["laranja"], f'stroke-width="2.5" transform="rotate({a/3} {x} 42)"')
            s += path(f"M{x-20},44 l-10,-10 M{x-20},44 l-12,2", extra=f'stroke="{C["verde_esc"]}" stroke-width="4"')
    s += path("M6,36 L214,36 L198,82 L22,82 Z", C["madeira"], 'stroke-width="3.5"')
    s += path("M14,52 L206,52 M18,67 L202,67", extra='stroke-width="1.5" opacity="0.5"')
    s += coracao(110, 60, 9, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["cocho_vazio"] = cocho(None)
P["cocho_feno"] = cocho("feno")
P["cocho_cenouras"] = cocho("cenouras")


def balde(agua):
    s = path("M14,26 Q45,-14 76,26", extra='stroke-width="4"')
    s += path("M10,26 L80,26 L72,86 L18,86 Z", C["madeira"], 'stroke-width="3"')
    for x in (30, 45, 60):
        s += path(f"M{x - (x-45)*0.1},28 L{x - (x-45)*0.25},84", extra='stroke-width="1.5" opacity="0.4"')
    s += rr(11, 38, 68, 7, 3, C["dourado"], 'stroke-width="2"') + rr(15, 70, 60, 7, 3, C["dourado"], 'stroke-width="2"')
    if agua:
        s += ell(45, 26, 34, 7, C["agua"], 'stroke-width="2.5"') + path("M32,25 q6,-3 12,0", extra=f'stroke="{C["branco"]}" stroke-width="2"')
    else:
        s += ell(45, 26, 34, 7, C["madeira_esc"], 'stroke-width="2.5"')
    return svg(90, 90, s)


P["balde_vazio"] = balde(False)
P["balde_agua"] = balde(True)


def fardo():
    w, h = 170, 110
    s = rr(4, 8, 162, 98, 18, "#f2d77e", 'stroke-width="3.5"')
    rnd = random.Random(2)
    for _ in range(40):
        x, y = rnd.uniform(16, 154), rnd.uniform(18, 96)
        s += path(f"M{x:.0f},{y:.0f} l{rnd.uniform(-14,14):.0f},{rnd.uniform(-4,4):.0f}", extra='stroke="#c99c3a" stroke-width="2"')
    s += rr(44, 6, 10, 102, 3, C["vermelho_rosa"], 'stroke-width="2"') + rr(116, 6, 10, 102, 3, C["vermelho_rosa"], 'stroke-width="2"')
    return svg(w, h, s)


P["fardo"] = fardo()
P["feno"] = svg(60, 40, path("M4,38 Q8,14 22,16 Q28,4 40,12 Q54,10 56,38 Z", "#f2d77e", 'stroke-width="2.5"') +
                path("M14,30 l10,-8 M26,32 l6,-14 M38,30 l8,-12 M44,34 l-6,-8", extra='stroke="#c99c3a" stroke-width="2"'))


def ducha(ligada):
    w, h = 300, 430
    s = rr(20, 20, 24, 408, 6, C["madeira"]) + rr(20, 20, 200, 24, 8, C["madeira"])
    s += path("M210,44 L210,70", extra='stroke-width="8"') + path("M210,44 L210,70", extra=f'stroke-width="4" stroke="{C["cinza"]}"')
    s += path("M180,70 L240,70 L232,92 L188,92 Z", C["cinza"], 'stroke-width="3"')
    if ligada:
        for i, x in enumerate(range(192, 232, 8)):
            s += path(f"M{x},96 q{-6 + i*3},150 {-20 + i*10},320", extra=f'stroke="{C["agua"]}" stroke-width="7" opacity="0.9"')
        for x, y in [(190, 160), (226, 240), (176, 320), (240, 360)]:
            s += circ(x, y, 7, C["agua"], 'stroke-width="2"')
    s += path("M44,260 L70,260", extra='stroke-width="8"') + path("M44,260 L70,260", extra=f'stroke-width="4" stroke="{C["cinza"]}"')
    s += circ(72, 250, 12, C["rosa_forte"], 'stroke-width="2.5"') + coracao(72, 251, 6, C["branco"], 'stroke="none"')
    s += flor(32, 110, 8, C["rosa"]) + flor(30, 200, 7, C["lilas"]) + flor(120, 32, 8, C["rosa"])
    return svg(w, h, s)


P["ducha_desligada"] = ducha(False)
P["ducha_ligada"] = ducha(True)


def piso_banho():
    w, h = 260, 60
    s = path("M10,8 L250,8 L258,54 L2,54 Z", C["madeira"], 'stroke-width="3"')
    for y in (20, 32, 44):
        s += path(f"M{8 - (y-8)*0.1},{y} L{252 + (y-8)*0.1},{y}", extra='stroke-width="1.8" opacity="0.6"')
    s += coracao(130, 30, 11, "#9bb3c7", 'stroke-width="2.5"')
    for dx in (-4, 0, 4):
        s += circ(130 + dx, 30, 1.2, L, 'stroke="none"')
    return svg(w, h, s)


P["piso_banho"] = piso_banho()
for i, t in enumerate((60, 40, 25), 1):
    r = t / 2 - 2
    P[f"espuma_{i}"] = svg(t, t, circ(t / 2, t / 2, r, C["branco"], 'stroke-width="2" fill-opacity="0.92"') +
                           ell(t / 2 - r * 0.35, t / 2 - r * 0.35, r * 0.3, r * 0.18, C["rosa"], 'stroke="none"') +
                           path(f"M{t/2 + r*0.2},{t/2 + r*0.6} q{r*0.4},-{r*0.1} {r*0.55},-{r*0.5}", extra=f'stroke="{C["lilas"]}" stroke-width="1.5"'))
P["toalha_gancho"] = svg(90, 60, circ(45, 6, 5, C["madeira_esc"], 'stroke-width="2"') +
                         path("M14,14 L76,14 L80,56 L10,56 Z", C["rosa"], 'stroke-width="2.5"') +
                         rr(10, 46, 70, 10, 2, C["lilas"], 'stroke-width="2"') + path("M14,14 Q45,24 76,14", extra='stroke-width="2"') +
                         coracao(45, 32, 6, C["rosa_forte"], 'stroke-width="1.5"'))
P["toalha"] = svg(100, 60, path("M4,12 Q50,2 96,12 L94,54 Q50,46 6,54 Z", C["rosa"], 'stroke-width="2.5"') +
                  path("M6,44 Q50,36 94,44 L94,54 Q50,46 6,54 Z", C["lilas"], 'stroke-width="2"') +
                  coracao(50, 26, 7, C["rosa_forte"], 'stroke-width="1.5"'))


def pente():
    s = rr(4, 4, 62, 18, 8, C["rosa_chiclete"], 'stroke-width="2.5"')
    for x in range(9, 64, 6):
        s += rr(x, 20, 3.5, 22, 1.5, C["rosa"], 'stroke-width="1.5"')
    s += coracao(35, 13, 5, C["branco"], 'stroke-width="1.5"')
    return svg(70, 45, s)


P["pente"] = pente()


def suporte_manta():
    w, h = 140, 120
    s = rr(10, 6, 120, 14, 5, C["madeira_esc"]) + circ(30, 13, 3, L, 'stroke="none"') + circ(110, 13, 3, L, 'stroke="none"')
    s += path("M24,20 L116,20 L112,92 Q70,104 28,92 Z", C["lilas"], 'stroke-width="2.5"')
    s += path("M28,82 Q70,94 112,82", extra=f'stroke="{C["rosa_forte"]}" stroke-width="4"')
    for x in range(36, 110, 16):
        s += path(f"M{x},{92 + (3 if x % 2 else 0)} l0,10", extra=f'stroke="{C["rosa_forte"]}" stroke-width="2.5"')
    s += coracao(70, 50, 12, C["rosa"], 'stroke-width="2"')
    s += path("M100,20 Q130,40 118,74 Q104,90 96,70", extra='stroke-width="7"')
    s += path("M100,20 Q130,40 118,74 Q104,90 96,70", extra=f'stroke="{C["rosa_chiclete"]}" stroke-width="4"')
    s += rr(110, 52, 14, 14, 3, C["dourado"], 'stroke-width="2"')
    return svg(w, h, s)


P["suporte_manta"] = suporte_manta()


def ferradura():
    w, h = 120, 110
    s = path("M22,104 L14,58 A46,46 0 0 1 106,58 L98,104 L74,104 L80,60 A20,20 0 0 0 40,60 L46,104 Z", C["dourado"], 'stroke-width="3.5"')
    for x, y in [(20, 80), (18, 56), (100, 80), (102, 56), (30, 30), (90, 30)]:
        s += circ(x, y, 3, "#c99a2e", 'stroke="none"')
    s += coracao(60, 64, 14, C["rosa_forte"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["ferradura"] = ferradura()


def lanterna(acesa):
    w, h = 60, 100
    s = ""
    if acesa:
        s += circ(30, 58, 30, "#ffe08a", 'stroke="none" opacity="0.55"')
    s += path("M18,16 Q30,0 42,16", extra='stroke-width="3"')
    s += rr(14, 16, 32, 8, 3, C["madeira_esc"], 'stroke-width="2.5"')
    s += path("M16,24 L44,24 L48,84 L12,84 Z", "#fff1b3" if acesa else "#dde6ee", 'stroke-width="2.5"')
    s += path("M30,24 L30,84", extra='stroke-width="2" opacity="0.5"')
    s += ell(30, 60, 6, 10, C["laranja"] if acesa else C["cinza"], 'stroke-width="2"')
    s += rr(8, 84, 44, 12, 4, C["madeira_esc"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["lanterna_apagada"] = lanterna(False)
P["lanterna_acesa"] = lanterna(True)


def porteira(aberta):
    w, h = 300, 200
    s = rr(2, 10, 26, 188, 6, C["branco"]) + rr(272, 10, 26, 188, 6, C["branco"])
    if not aberta:
        s += rr(26, 40, 248, 18, 6, C["branco"]) + rr(26, 100, 248, 18, 6, C["branco"]) + rr(26, 160, 248, 18, 6, C["branco"])
        s += path("M34,170 L266,48", extra='stroke-width="18"') + path("M34,170 L266,48", extra=f'stroke-width="12" stroke="{C["branco"]}"')
        for x in range(60, 260, 40):
            s += rr(x, 36, 14, 146, 5, C["branco"], 'stroke-width="2.5"')
        for x, y in [(60, 40), (150, 100), (240, 160), (110, 160), (200, 40)]:
            s += flor(x, y, 8, C["rosa"] if x % 20 else C["lilas"])
    else:
        # folha aberta, vista de lado junto ao poste
        s += rr(26, 30, 44, 156, 6, C["branco"])
        for y in (40, 100, 160):
            s += rr(26, y, 44, 16, 5, C["branco"], 'stroke-width="2.5"')
        s += flor(48, 48, 8, C["rosa"]) + flor(48, 168, 8, C["lilas"])
    return svg(w, h, s)


P["porteira_fechada"] = porteira(False)
P["porteira_aberta"] = porteira(True)


def arvore():
    w, h = 480, 540
    s = path(f"M190,300 C196,420 180,500 140,{h-3} L340,{h-3} C300,500 284,420 290,300 Z", C["madeira_esc"], 'stroke-width="4"')
    s += path("M230,360 q8,60 -4,140 M262,350 q-6,70 6,150", extra='stroke-width="3" opacity="0.5"')
    copa = [(240, 190, 170), (110, 230, 105), (370, 230, 105), (160, 110, 110), (320, 110, 110), (240, 290, 120)]
    for cx, cy, r in copa:
        s += circ(cx, cy, r, C["verde"], 'stroke-width="4"')
    for cx, cy, r in copa:
        s += circ(cx, cy, r - 4, C["verde"], 'stroke="none"')
    rnd = random.Random(5)
    for gx in range(30, 460, 62):
        for gy in range(30, 400, 62):
            x, y = gx + rnd.uniform(-18, 18), gy + rnd.uniform(-18, 18)
            if any((x - cx) ** 2 + (y - cy) ** 2 < (r - 18) ** 2 for cx, cy, r in copa) and rnd.random() < 0.7:
                s += flor(round(x), round(y), 9, C["rosa"], C["rosa_forte"])
    return svg(w, h, s)


P["arvore"] = arvore()


def laguinho(ondas):
    w, h = 300, 110
    s = ""
    rnd = random.Random(8)
    for i in range(16):
        a = 2 * math.pi * i / 16
        s += ell(150 + 138 * math.cos(a), 56 + 44 * math.sin(a), 18, 13, rnd.choice(["#d8d2dc", "#c9c1cf", "#e6e0ea"]), 'stroke-width="2.5"')
    s += ell(150, 56, 124, 36, C["agua"], 'stroke-width="3"')
    s += ell(110, 46, 30, 6, C["branco"], 'stroke="none" opacity="0.6"')
    if ondas:
        for rx, ry in [(26, 8), (48, 14), (72, 21)]:
            s += ell(170, 62, rx, ry, "none", f'stroke="{C["branco"]}" stroke-width="3"')
    return svg(w, h, s)


P["laguinho_parado"] = laguinho(False)
P["laguinho_ondas"] = laguinho(True)


def banco_tronco():
    w, h = 200, 80
    s = rr(8, 14, 170, 60, 30, C["madeira_esc"], 'stroke-width="3.5"')
    s += path("M40,30 q40,-6 90,4 M50,56 q50,6 100,-2", extra='stroke-width="2" opacity="0.5"')
    s += ell(176, 44, 20, 30, C["madeira_clara"], 'stroke-width="3.5"') + ell(176, 44, 11, 18, "none", 'stroke-width="2"')
    s += ell(176, 44, 4, 7, "none", 'stroke-width="2"')
    s += path("M70,16 q4,-12 14,-10", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') + ell(88, 6, 7, 4, C["verde"], 'stroke-width="2"')
    return svg(w, h, s)


P["banco_tronco"] = banco_tronco()


def moita(com):
    w, h = 200, 90
    s = ""
    for cx, cy, r in [(40, 60, 34), (100, 50, 44), (160, 60, 34), (70, 66, 26), (132, 66, 26)]:
        s += circ(cx, cy, r, C["verde_esc"], 'stroke-width="3"')
    for cx, cy, r in [(40, 60, 31), (100, 50, 41), (160, 60, 31), (70, 66, 23), (132, 66, 23)]:
        s += circ(cx, cy, r, C["verde_esc"], 'stroke="none"')
    s += rr(10, 76, 180, 14, 7, C["verde_esc"], 'stroke="none"')
    if com:
        for x, y in [(40, 40), (90, 22), (120, 40), (160, 44), (66, 58)]:
            s += margarida(x, y, 10)
        for x, y, c in [(110, 66, C["rosa"]), (150, 70, C["lilas"]), (30, 72, C["rosa"]), (76, 36, C["lilas"])]:
            s += flor(x, y, 6, c)
    else:
        for x, y in [(50, 50), (110, 36), (150, 58), (84, 70)]:
            s += ell(x, y, 8, 4, C["verde"], 'stroke-width="1.5"')
    return svg(w, h, s)


P["moita_flores"] = moita(True)
P["moita_colhida"] = moita(False)
P["margarida"] = svg(30, 60, path("M15,30 Q12,45 15,58", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') +
                     ell(9, 46, 5, 2.5, C["verde"], 'stroke-width="1.5" transform="rotate(-30 9 46)"') + margarida(15, 16, 9))

# Posição das peças na prévia e no jogo (canto de cima à esquerda, em pixels do jogo).
W, H, CHAO = 3300, 900, 600
POS = [("fundo", 0, 0), ("suporte_manta", 840, 300), ("ferradura", 1000, 290), ("toalha_gancho", 1100, 270), ("ducha_ligada", 1180, 190),
       ("lanterna_acesa", 1330, 200), ("piso_banho", 1200, 780), ("meia_porta_fechada", 380, 530), ("cocho_cenouras", 820, 600), ("balde_agua", 1060, 610),
       ("fardo", 850, 770), ("fardo", 1040, 770), ("feno", 700, 720), ("pente", 40, 830), ("arvore", 1950, 100),
       ("porteira_fechada", 1560, 500), ("laguinho_ondas", 2500, 750), ("banco_tronco", 2600, 620), ("moita_flores", 2850, 690), ("moita_colhida", 3060, 690),
       ("moita_flores", 2250, 820), ("margarida", 2200, 850), ("@catarina", 2180, 880), ("@catarina", 640, 860)]

# Como o cenário entra no protótipo (ver para_jogo.py).
JOGO = {
    "interativos": {
        "meia_porta": {"estados": ["meia_porta_fechada", "meia_porta_aberta"], "x": 380, "y": 530},
        "cocho": {"estados": ["cocho_vazio", "cocho_feno", "cocho_cenouras"], "x": 820, "y": 600},
        "balde": {"estados": ["balde_vazio", "balde_agua"], "x": 1060, "y": 610},
        "ducha": {"estados": ["ducha_desligada", "ducha_ligada"], "x": 1180, "y": 190},
        "lanterna": {"estados": ["lanterna_apagada", "lanterna_acesa"], "x": 1330, "y": 200},
        "porteira": {"estados": ["porteira_fechada", "porteira_aberta"], "x": 1560, "y": 500},
        "laguinho": {"estados": ["laguinho_parado", "laguinho_ondas"], "x": 2500, "y": 750},
        "moita_1": {"estados": ["moita_colhida", "moita_flores"], "x": 2850, "y": 690},
        "moita_2": {"estados": ["moita_colhida", "moita_flores"], "x": 3060, "y": 690},
        "moita_3": {"estados": ["moita_colhida", "moita_flores"], "x": 2250, "y": 820},
        "seta_sede": {"estados": ["seta_casa_e"], "x": 1880, "y": 470, "leva": "sede", "chegada": 1960},
        "seta_plantacao": {"estados": ["seta_cenoura_d"], "x": 2380, "y": 470, "leva": "plantacao", "chegada": 2440},
        "seta_pet_care": {"estados": ["seta_pata_d"], "x": 3160, "y": 470, "leva": "pet_care", "chegada": 3180},
    },
    "extras": [("seta_casa_e", 1880, 470), ("seta_cenoura_d", 2380, 470), ("seta_pata_d", 3160, 470)],
    "objetos": ["pente", "feno", "margarida"],
    "lugares": [],
    "superficies": [[860, 1010, 775], [1050, 1200, 775]],
}

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario/estabulo/2d")
    salvar(P, os.path.join(destino, "svg"), destino)
    print(len(P), "peças em", destino)
