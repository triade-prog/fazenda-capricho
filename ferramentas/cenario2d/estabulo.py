"""Peças 2D provisórias do Estábulo florido + pasto.

Uso: python3 ferramentas/cenario2d/estabulo.py
Saída: arte/cenario/estabulo/2d/*.png (mesmos nomes da lista de entrega do PROMPTS.md).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from moveis import Soltos  # noqa: E402
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, nuvem, salvar  # noqa: E402

P = {}
S = Soltos(P)
DX = 1000   # largura do jardim da esquerda: o estábulo fica no meio do cenário (referência de 15/11/2026, noite)


def quadro(peca, w, h):
    """Mesmo desenho 2D num quadro com a proporção da peça 3D nova."""
    import re
    return re.sub(r'width="[^"]+" height="[^"]+"', f'width="{w}" height="{h}" preserveAspectRatio="none"', peca, count=1)


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
    S.limpar()
    s = f'<rect width="{w}" height="{h}" fill="url(#ceu)" stroke="none"/>'
    for cx, cy, k in [(1800, 110, 44), (2400, 70, 36), (3000, 140, 46), (600, 60, 30)]:
        s += nuvem(cx, cy, k)
    # pasto: morros, cerca, grama
    s += path(f"M{div-40},{chao-40} Q2000,{chao-260} 2500,{chao-120} T{w},{chao-170} L{w},{chao} L{div-40},{chao} Z",
              C["verde_claro"])
    s += path(f"M{div-40},{chao-10} Q2300,{chao-150} 2900,{chao-40} T{w},{chao-60} L{w},{chao} L{div-40},{chao} Z", "#a8dd8f")
    S.cerca(chao, 1840, w)          # a cerca começa depois da porteira: aberta, ela dá para o jardim
    S.cerca(chao, -DX, 0)           # jardim da esquerda (x negativo: tudo anda DX para a direita no fim)
    for x, y in [(-640, 868), (-545, 815), (-440, 768), (-325, 728), (-205, 695), (-95, 668)]:
        S.comum("pedra_caminho", x - 50, y - 19)
    # o chão (palha e grama) é o do fundo 3D; caminho de pedras saindo da porteira para o jardim
    for x, y in [(1700, 650), (1745, 700), (1800, 752), (1870, 800), (1960, 850), (2060, 878)]:
        S.comum("pedra_caminho", x - 50, y - 19)
    # estábulo: parede de tábuas cor de mel, telhado e flores penduradas (peças)
    pa = rr(-5, 110, div + 5, chao - 110, 0, C["mel"], 'stroke-width="4"')
    for x in range(0, div, 50):
        pa += rr(x, 110, 50, chao - 110, 0, "#e3a257" if (x // 50) % 2 else C["mel"], 'stroke-width="1.5" stroke-opacity="0.5"')
    for x in (20, 740, 1460):
        pa += rr(x, 120, 30, chao - 120, 4, C["madeira_esc"])
    pa += rr(-5, 150, div + 5, 22, 3, C["madeira_esc"])           # viga
    S.add("parede_estabulo", pa, -8, 106, div + 12, chao - 100)
    S.add("telhado_estabulo", path(f"M-5,135 L750,55 L{div+40},135 L{div+40},165 L750,85 L-5,165 Z", C["vermelho_rosa"], 'stroke-width="4"'),
          -10, 30, div + 56, 177)
    for i, x in enumerate(range(80, div - 40, 120)):
        nome = "flor_pendurada_" + ("rosa" if i % 2 else "lilas")
        fp = path(f"M{x},172 L{x},{196 + (i % 2) * 14}", extra='stroke-width="2"') + flor(x, 206 + (i % 2) * 14, 10, C["rosa"] if i % 2 else C["lilas"], C["rosa_forte"])
        S.add(nome, fp, x - 22, 168, 44, 64, [(x - 22, 168)])
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
    """Cocho alto de madeira com pés (como na imagem de referência da Carol)."""
    w, h = 300, 210
    s = rr(20, 90, 22, 118, 5, C["madeira_esc"]) + rr(258, 90, 22, 118, 5, C["madeira_esc"])
    s += path("M30,190 L270,110 M30,110 L270,190", extra=f'stroke-width="10" stroke="{C["madeira_esc"]}"')
    if conteudo == "feno":
        for i in range(22):
            x = 14 + i * 12
            s += path(f"M{x},64 q8,-34 16,0", "#f0d27a", 'stroke-width="2.5"')
    elif conteudo == "cenouras":
        for x, a in [(50, -30), (90, 20), (130, -15), (170, 25), (210, -20), (250, 10)]:
            s += path(f"M{x-24},58 L{x+22},50 L{x-20},70 Z", C["laranja"], f'stroke-width="2.5" transform="rotate({a/3} {x} 60)"')
            s += path(f"M{x-24},62 l-12,-12 M{x-24},62 l-14,2", extra=f'stroke="{C["verde_esc"]}" stroke-width="4"')
    s += rr(4, 56, 292, 64, 8, C["madeira"], 'stroke-width="3.5"')
    s += path("M10,78 L290,78 M10,98 L290,98", extra='stroke-width="1.5" opacity="0.5"')
    s += coracao(150, 88, 16, C["rosa_forte"], 'stroke-width="2.5"')
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


P["balde_vazio"] = balde(False).replace('width="90" height="90"', 'width="125" height="125" preserveAspectRatio="none"', 1)
P["balde_agua"] = balde(True).replace('width="90" height="90"', 'width="125" height="125" preserveAspectRatio="none"', 1)


def fardo():
    w, h = 170, 110  # quadro final 210 × 136 (mais perto da referência)
    s = rr(4, 8, 162, 98, 18, "#f2d77e", 'stroke-width="3.5"')
    rnd = random.Random(2)
    for _ in range(40):
        x, y = rnd.uniform(16, 154), rnd.uniform(18, 96)
        s += path(f"M{x:.0f},{y:.0f} l{rnd.uniform(-14,14):.0f},{rnd.uniform(-4,4):.0f}", extra='stroke="#c99c3a" stroke-width="2"')
    s += rr(44, 6, 10, 102, 3, C["vermelho_rosa"], 'stroke-width="2"') + rr(116, 6, 10, 102, 3, C["vermelho_rosa"], 'stroke-width="2"')
    return svg(w, h, s)


P["fardo"] = fardo().replace('width="170" height="110"', 'width="210" height="136" preserveAspectRatio="none"', 1)
P["feno"] = svg(60, 40, path("M4,38 Q8,14 22,16 Q28,4 40,12 Q54,10 56,38 Z", "#f2d77e", 'stroke-width="2.5"') +
                path("M14,30 l10,-8 M26,32 l6,-14 M38,30 l8,-12 M44,34 l-6,-8", extra='stroke="#c99c3a" stroke-width="2"'))


def ducha(ligada):
    """Ducha de cano prateado: cano em pé à direita, curva no alto e o chuveiro virado para a esquerda (como na referência)."""
    w, h = 300, 430
    cano = "M250,428 L250,70 Q250,30 210,30 L120,30 Q96,30 96,54"
    s = path(cano, extra='stroke-width="18"') + path(cano, extra=f'stroke-width="12" stroke="{C["cinza"]}"')
    s += path("M60,54 L132,54 L124,84 L68,84 Z", C["cinza"], 'stroke-width="3"')
    s += rr(236, 400, 28, 28, 6, C["cinza"], 'stroke-width="3"')
    if ligada:
        for i, x in enumerate(range(72, 128, 9)):
            s += path(f"M{x},88 q{-4 + i*1.5},150 {-12 + i*5},330", extra=f'stroke="{C["agua"]}" stroke-width="5" opacity="0.9"')
        for x, y in [(80, 170), (116, 240), (70, 320), (124, 380)]:
            s += circ(x, y, 6, C["agua"], 'stroke-width="2"')
    s += circ(250, 260, 18, C["rosa_forte"], 'stroke-width="3"') + coracao(250, 261, 8, C["branco"], 'stroke="none"')
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


# ---------------------------------------------------------------- peças novas (referência de 15/11/2026)


def cesto_pendurado():
    w, h = 200, 240
    s = path("M100,4 L36,110 M100,4 L164,110", extra='stroke-width="3"') + circ(100, 8, 6, C["madeira_esc"], 'stroke-width="2"')
    for x, y in [(30, 150), (56, 186), (150, 160), (170, 200), (100, 210)]:
        s += path(f"M{x},110 Q{x-6},{y-30} {x},{y}", extra=f'stroke="{C["verde_esc"]}" stroke-width="4"')
        s += ell(x, y, 8, 5, C["verde"], 'stroke-width="1.5"')
    s += path("M24,110 L176,110 L160,160 Q100,176 40,160 Z", C["rosa"], 'stroke-width="3"')
    s += path("M30,124 L170,124", extra='stroke-width="2" opacity="0.5"')
    for x, y, c in [(52, 96, C["rosa"]), (84, 84, C["lilas"]), (116, 82, C["rosa"]), (148, 94, C["lilas"]), (100, 100, C["branco"])]:
        s += ell(x, y + 10, 18, 10, C["verde"], 'stroke-width="2"') + flor(x, y, 10, c, C["amarelo"])
    return svg(w, h, s)


P["cesto_pendurado"] = cesto_pendurado()
P["prateleira_banho"] = svg(280, 50, rr(4, 4, 272, 16, 5, C["madeira"], 'stroke-width="3"') +
                            path("M30,20 L30,44 L56,20 M250,20 L250,44 L224,20", C["madeira_esc"], 'stroke-width="3"'))
P["shampoo"] = svg(50, 80, rr(8, 26, 34, 52, 10, C["rosa_claro"]) + rr(18, 12, 14, 16, 3, C["branco"], 'stroke-width="2"') +
                   path("M25,12 L25,4 L38,4", extra='stroke-width="3"') + coracao(25, 52, 8, C["rosa_forte"], 'stroke-width="1.5"'))
P["pote_creme"] = svg(64, 46, rr(4, 4, 56, 14, 6, C["rosa"], 'stroke-width="2.5"') + rr(6, 16, 52, 28, 8, C["branco"], 'stroke-width="2.5"') +
                      coracao(32, 30, 6, C["rosa_forte"], 'stroke-width="1.5"'))
P["vaso_flores"] = svg(90, 90, "".join(ell(x, 44, 12, 7, C["verde"], 'stroke-width="2"') for x in (22, 68)) +
                       "".join(flor(x, y, 10, c, C["amarelo"]) for x, y, c in [(26, 26, C["rosa"]), (46, 16, C["rosa_chiclete"]), (66, 28, C["rosa"]), (46, 36, C["lilas"])]) +
                       path("M18,50 L72,50 L64,88 L26,88 Z", C["rosa_chiclete"], 'stroke-width="3"'))
P["ganchos"] = svg(230, 40, rr(4, 6, 222, 22, 6, C["madeira"], 'stroke-width="3"') +
                   "".join(circ(x, 30, 6, C["dourado"], 'stroke-width="2"') for x in (40, 115, 190)))
P["pente_pendurado"] = svg(40, 110, circ(20, 8, 6, "none", 'stroke-width="3"') + rr(8, 14, 24, 94, 6, C["rosa_chiclete"], 'stroke-width="2.5"') +
                           "".join(path(f"M8,{y} L-2,{y}", extra='stroke-width="0"') for y in ()) +
                           "".join(rr(20, y, 16, 3, 1, C["rosa"], 'stroke-width="1"') for y in range(20, 104, 8)))
P["escova_pendurada"] = svg(56, 120, circ(28, 8, 6, "none", 'stroke-width="3"') + rr(22, 14, 12, 50, 5, C["rosa_forte"], 'stroke-width="2.5"') +
                            ell(28, 88, 24, 30, C["rosa"], 'stroke-width="2.5"') +
                            "".join(circ(x, y, 3, C["branco"], 'stroke-width="1"') for x in (18, 28, 38) for y in (76, 88, 100)))
P["espelho"] = svg(70, 120, circ(35, 8, 6, "none", 'stroke-width="3"') + rr(29, 80, 12, 36, 5, C["rosa_forte"], 'stroke-width="2.5"') +
                   circ(35, 50, 32, C["rosa_chiclete"], 'stroke-width="3"') + circ(35, 50, 24, C["azul"], 'stroke-width="2"') +
                   path("M24,40 Q34,30 44,36", extra=f'stroke="{C["branco"]}" stroke-width="3"'))


def banheira(espuma):
    w, h = 340, 190
    s = ""
    if espuma:
        for x, y, r in [(60, 46, 26), (100, 34, 32), (150, 40, 30), (200, 30, 34), (250, 40, 30), (286, 50, 24), (130, 56, 22), (220, 56, 24)]:
            s += circ(x, y + 14, r, C["branco"], 'stroke-width="2.5"')
    s += path("M18,64 L322,64 L300,184 L40,184 Z", C["madeira"], 'stroke-width="3.5"')
    for x in range(70, 300, 50):
        s += path(f"M{x},66 L{x + (x - 170) * 0.07},182", extra='stroke-width="1.5" opacity="0.45"')
    s += rr(16, 58, 308, 14, 6, C["madeira_esc"], 'stroke-width="3"')
    s += rr(26, 96, 288, 10, 3, C["cinza"], 'stroke-width="2"') + rr(34, 156, 272, 10, 3, C["cinza"], 'stroke-width="2"')
    if not espuma:
        s += ell(170, 66, 146, 8, C["agua"], 'stroke-width="2"')
    s += coracao(170, 130, 18, C["rosa_forte"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["banheira_agua"] = banheira(False)
P["banheira_espuma"] = banheira(True)


def tigela(racao):
    w, h = 160, 70
    s = ell(80, 20, 70, 14, "#c98c56" if racao else C["agua"], 'stroke-width="3"')
    if racao:
        for x, y in [(50, 16), (66, 12), (82, 18), (98, 12), (112, 18), (74, 22), (90, 24)]:
            s += circ(x, y, 6, "#9c6236", 'stroke-width="1.5"')
    s += path("M10,20 Q80,40 150,20 L140,64 Q80,74 20,64 Z", C["rosa_chiclete"], 'stroke-width="3"')
    s += coracao(80, 48, 9, C["branco"], 'stroke-width="2"')
    return svg(w, h, s)


P["tigela_racao"] = tigela(True)
P["tigela_agua"] = tigela(False)
P["escova_pelo"] = svg(110, 56, rr(6, 6, 98, 26, 10, C["rosa_chiclete"], 'stroke-width="2.5"') + coracao(55, 18, 6, C["branco"], 'stroke-width="1.5"') +
                       "".join(rr(x, 30, 5, 22, 2, C["lilas"], 'stroke-width="1.2"') for x in range(14, 98, 8)))
P["tapete_coracao"] = svg(300, 100, ell(150, 50, 144, 44, C["rosa_claro"], 'stroke-width="3"') + ell(150, 50, 126, 34, "none", 'stroke-width="2" stroke-dasharray="6 6"') +
                          coracao(150, 50, 26, C["rosa_forte"], 'stroke-width="2.5"'))


def caixote_frutas():
    w, h = 260, 170
    s = ""
    for x, y in [(50, 50), (84, 40), (64, 70), (110, 60)]:
        s += circ(x, y, 22, "#ff5f6d", 'stroke-width="2.5"') + path(f"M{x},{y-22} l3,-10", extra='stroke-width="2.5"')
    for x, a in [(150, -20), (180, -10), (205, 5), (232, 15)]:
        s += path(f"M{x-12},76 L{x},18 L{x+12},76 Z", C["laranja"], f'stroke-width="2.5" transform="rotate({a} {x} 76)"')
        s += path(f"M{x},18 l-10,-16 M{x},18 l0,-18 M{x},18 l10,-16", extra=f'stroke="{C["verde_esc"]}" stroke-width="4" transform="rotate({a} {x} 76)"')
    s += rr(6, 70, 248, 96, 8, C["madeira"], 'stroke-width="3.5"')
    s += path("M10,102 L250,102 M10,134 L250,134", extra='stroke-width="2" opacity="0.5"')
    s += coracao(140, 118, 18, C["rosa_forte"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["caixote_frutas"] = caixote_frutas()


def trepadeira_flores():
    w, h = 70, 420
    s = path("M35,4 Q10,60 35,110 T35,210 T35,310 T35,416", extra=f'stroke="{C["verde_esc"]}" stroke-width="5"')
    for i, y in enumerate(range(30, 410, 42)):
        x = 35 + (18 if i % 2 else -18)
        s += ell(x, y + 14, 10, 6, C["verde"], 'stroke-width="2"') + flor(x, y, 10, C["rosa"] if i % 3 else C["rosa_chiclete"], C["amarelo"])
    return svg(w, h, s)


P["trepadeira_flores"] = trepadeira_flores()


def pedra(cx, cy, rx, ry, cor="#d8c3a6"):
    return ell(cx, cy, rx, ry, cor, 'stroke-width="2.5"') + ell(cx - rx * 0.25, cy - ry * 0.35, rx * 0.4, ry * 0.25, "#efe2cf", 'stroke="none"')


def laguinho(ondas):
    """Lago em forma de feijão com pedras marrons arredondadas em volta (cascata e vitórias-régias à parte)."""
    w, h = 820, 260
    borda = "M70,150 C60,70 200,40 330,62 C430,78 470,40 600,44 C740,48 790,120 760,170 C730,230 560,236 400,226 C240,236 90,224 70,150 Z"
    rnd = random.Random(8)
    s = ""
    pts = [(60, 150), (80, 96), (140, 64), (220, 50), (300, 60), (380, 70), (450, 52), (530, 40), (610, 40), (690, 60), (750, 100), (780, 150),
           (750, 200), (680, 228), (600, 238), (520, 236), (440, 232), (360, 236), (280, 238), (200, 232), (130, 216), (80, 190)]
    for x, y in pts:
        s += pedra(x, y, rnd.uniform(34, 48), rnd.uniform(20, 28), rnd.choice(["#d9b48a", "#cfa57a", "#e2c29c"]))
    s += path(borda, C["agua"], 'stroke-width="3"')
    s += ell(300, 100, 90, 10, C["branco"], 'stroke="none" opacity="0.6"')
    if ondas:
        for rx, ry in [(40, 10), (80, 20), (120, 30)]:
            s += ell(440, 150, rx, ry, "none", f'stroke="{C["branco"]}" stroke-width="3"')
    return svg(w, h, s)


P["laguinho_parado"] = laguinho(False)
P["laguinho_ondas"] = laguinho(True)
P["cascata"] = svg(230, 180, pedra(60, 70, 56, 40, "#d9b48a") + pedra(176, 64, 50, 44, "#cfa57a") + pedra(40, 140, 36, 26, "#e2c29c") + pedra(196, 140, 32, 28, "#d9b48a") +
                   path("M80,46 L150,46 L162,170 L74,170 Z", C["agua"], 'stroke-width="3"') +
                   "".join(path(f"M{x},50 Q{x+4},110 {x+2},168", extra=f'stroke="{C["branco"]}" stroke-width="3"') for x in (92, 112, 132, 148)))
P["vitoria_regia"] = svg(120, 50, path("M60,25 L112,20 A54,20 0 1 1 112,30 Z", C["verde"], 'stroke-width="2.5"'))
P["vitoria_regia_flor"] = svg(170, 96, path("M85,70 L160,64 A78,24 0 1 1 160,76 Z", C["verde"], 'stroke-width="2.5"') +
                              "".join(ell(85 + dx, 46, 12, 26, C["rosa"], f'stroke-width="2" transform="rotate({dx*1.6} {85+dx} 66)"') for dx in (-24, -12, 0, 12, 24)) +
                              circ(85, 54, 8, C["amarelo"], 'stroke-width="2"'))


def lanterna_jardim():
    w, h = 120, 160
    s = circ(60, 84, 50, "#ffe08a", 'stroke="none" opacity="0.45"')
    s += path("M14,30 L60,4 L106,30 Z", "#8a5a3c", 'stroke-width="3"') + rr(24, 30, 72, 10, 3, "#8a5a3c", 'stroke-width="2.5"')
    s += rr(28, 40, 64, 90, 6, "#fff1b3", 'stroke-width="3"')
    s += path("M60,40 L60,130 M28,84 L92,84", extra='stroke="#8a5a3c" stroke-width="5"')
    s += rr(18, 130, 84, 26, 6, "#8a5a3c", 'stroke-width="3"')
    return svg(w, h, s)


P["lanterna_jardim"] = lanterna_jardim()


def flores_lago():
    w, h = 230, 110
    s = "".join(ell(x, 82, 40, 26, C["verde_esc"], 'stroke-width="2.5"') for x in (50, 115, 180))
    for x, y, c in [(40, 60, C["rosa"]), (76, 44, C["branco"]), (110, 58, C["rosa_chiclete"]), (146, 42, C["rosa"]), (186, 60, C["branco"]),
                    (60, 84, C["rosa_chiclete"]), (130, 84, C["branco"]), (170, 86, C["rosa"])]:
        s += flor(x, y, 12, c, C["amarelo"])
    return svg(w, h, s)


P["flores_lago"] = flores_lago()
P["touceira"] = svg(110, 110, "".join(path(f"M55,108 Q{55 + dx * 0.4},60 {55 + dx},{10 + abs(dx) * 0.6}", C["verde"], 'stroke-width="2.5"') +
                                      path(f"M55,108 Q{55 + dx * 0.4},60 {55 + dx},{10 + abs(dx) * 0.6} Q{55 + dx * 0.7},70 {62},108 Z", C["verde"], 'stroke-width="2.5"')
                                      for dx in (-44, -22, 0, 22, 44)))
P["pedra"] = svg(110, 60, pedra(55, 34, 50, 24, "#cfc6cf"))

# quadros na proporção das peças 3D da Carol (15/11/2026)
for _n, _w, _h in [("cesto_pendurado", 180, 250), ("ferradura", 115, 120), ("ganchos", 230, 45), ("lanterna_apagada", 52, 110),
                   ("lanterna_acesa", 52, 110), ("lanterna_jardim", 90, 170), ("pente_pendurado", 32, 118),
                   ("prateleira_banho", 280, 44), ("escova_pendurada", 50, 125),
                   ("balde_vazio", 110, 136), ("balde_agua", 110, 136), ("ducha_ligada", 240, 430), ("ducha_desligada", 240, 430),
                   ("feno", 70, 36), ("shampoo", 40, 85),
                   ("vaso_flores", 66, 92), ("flor_pendurada_rosa", 44, 80), ("flor_pendurada_lilas", 44, 80), ("cascata", 240, 160)]:
    P[_n] = quadro(P[_n], _w, _h)

P["maca"] = svg(44, 42, path("M22,12 l2,-9", extra='stroke-width="3"') + circ(22, 25, 15, "#ff5f6d", 'stroke-width="2.5"') +
                ell(31, 8, 7, 4, C["verde"], 'stroke-width="1.5"'))
P["cenoura"] = svg(36, 54, path("M18,16 l-9,-13 M18,16 l0,-15 M18,16 l9,-13", extra=f'stroke="{C["verde_esc"]}" stroke-width="5"') +
                   path("M6,18 L30,18 L18,52 Z", C["laranja"], 'stroke-width="2.5"'))

# Posição das peças na prévia e no jogo (canto de cima à esquerda, em pixels do jogo).
# As posições abaixo são do arranjo antigo (estábulo colado à esquerda); no fim tudo anda DX para a direita.
W, H, CHAO = 3300 + DX, 900, 600
POS = [("fundo", 0, 0),
       # estábulo (parede)
       ("cesto_pendurado", 80, 200), ("ferradura", 330, 250), ("suporte_manta", 500, 260),
       ("prateleira_banho", 870, 330), ("shampoo", 910, 250), ("pote_creme", 980, 284), ("vaso_flores", 1078, 238),
       ("ganchos", 895, 380), ("pente_pendurado", 915, 410), ("escova_pendurada", 982, 410), ("espelho", 1050, 410),
       ("ducha_ligada", 1170, 190), ("lanterna_acesa", 1395, 150), ("trepadeira_flores", 1440, 180),
       # estábulo (chão)
       ("cocho_feno", 50, 450), ("banheira_espuma", 830, 500), ("toalha", 1060, 560), ("shampoo", 820, 610),
       ("balde_agua", 1250, 590), ("tapete_coracao", 760, 712), ("caixote_frutas", 30, 650), ("escova_pelo", 260, 790),
       ("tigela_racao", 430, 770), ("tigela_agua", 610, 770), ("fardo", 1060, 720), ("fardo", 1275, 730), ("feno", 640, 640),
       ("pente", 300, 860), ("maca", 300, 668), ("cenoura", 345, 690), ("maca", 520, 800),
       # jardim
       ("arvore", 1900, 60), ("porteira_fechada", 1540, 420), ("banco_tronco", 2560, 520),
       ("moita_flores", 2830, 510), ("moita_colhida", 3040, 590),
       ("laguinho_ondas", 2090, 610), ("cascata", 2700, 540), ("vitoria_regia", 2330, 740), ("vitoria_regia_flor", 2410, 720),
       ("touceira", 2060, 600), ("touceira", 2460, 540), ("touceira", 2930, 650), ("flores_lago", 1960, 690), ("flores_lago", 2230, 540),
       ("lanterna_jardim", 2135, 610), ("moita_flores", 2850, 750), ("pedra", 3150, 820), ("pedra", 1440, 850),
       ("margarida", 1750, 760), ("@catarina", 1800, 880), ("@catarina", 640, 860),
       # jardim da esquerda
       ("flores_lago", -520, 548), ("touceira", -250, 560), ("moita_flores", -960, 700), ("pedra", -330, 830),
       ("flores_lago", -820, 790), ("touceira", -700, 640), ("margarida", -480, 700), ("pedra", -900, 610)]
POS[1:1] = S.pos
POS.remove(("arvore", 1900, 60))
POS[1:1] = [("arvore", 1900, 60), ("arvore", -820, 60)]   # árvores atrás da cerca, uma de cada lado
POS = [p if p[0] == "fundo" else (p[0], p[1] + DX) + tuple(p[2:]) for p in POS]

# Como o cenário entra no protótipo (ver para_jogo.py).
JOGO = {
    "interativos": {
        "cocho": {"estados": ["cocho_vazio", "cocho_feno", "cocho_cenouras"], "x": 50, "y": 450},
        "banheira": {"estados": ["banheira_agua", "banheira_espuma"], "x": 830, "y": 500},
        "balde": {"estados": ["balde_vazio", "balde_agua"], "x": 1250, "y": 590},
        "ducha": {"estados": ["ducha_desligada", "ducha_ligada"], "x": 1170, "y": 190},
        "lanterna": {"estados": ["lanterna_apagada", "lanterna_acesa"], "x": 1395, "y": 150},
        "porteira": {"estados": ["porteira_fechada", "porteira_aberta"], "x": 1540, "y": 420},
        "laguinho": {"estados": ["laguinho_parado", "laguinho_ondas"], "x": 2090, "y": 610},
        "moita_1": {"estados": ["moita_colhida", "moita_flores"], "x": 2830, "y": 510},
        "moita_2": {"estados": ["moita_colhida", "moita_flores"], "x": 3040, "y": 590},
        "moita_3": {"estados": ["moita_colhida", "moita_flores"], "x": 2850, "y": 750},
        "seta_sede": {"estados": ["seta_casa_e"], "x": -960, "y": 462, "leva": "sede", "chegada": -840},
        "seta_plantacao": {"estados": ["seta_cenoura_d"], "x": 2380, "y": 462, "leva": "plantacao", "chegada": 2440},
        "seta_pet_care": {"estados": ["seta_pata_d"], "x": 3160, "y": 462, "leva": "pet_care", "chegada": 3180},
    },
    "extras": [("seta_casa_e", -960, 462), ("seta_cenoura_d", 2380, 462), ("seta_pata_d", 3160, 462)],
    "objetos": ["maca", "cenoura", "pente", "feno", "margarida", "shampoo", "pote_creme", "vaso_flores", "toalha", "escova_pelo"],
    "lugares": [],
    "superficies": [[880, 1140, 334], [1070, 1260, 726], [1285, 1475, 736]],
}
for _it in JOGO["interativos"].values():
    _it["x"] += DX
    if "chegada" in _it:
        _it["chegada"] += DX
JOGO["extras"] = [(n, x + DX, y) for n, x, y in JOGO["extras"]]
JOGO["superficies"] = [[a + DX, b + DX, y] for a, b, y in JOGO["superficies"]]
P["fundo"] = quadro(P["fundo"], W, H)

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario/estabulo/2d")
    salvar(P, os.path.join(destino, "svg"), destino)
    print(len(P), "peças em", destino)
