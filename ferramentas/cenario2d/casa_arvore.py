"""Peças 2D provisórias da Casa na árvore (C07 pátio e C08 dentro).

Uso: python3 ferramentas/cenario2d/casa_arvore.py
Saída: arte/cenario/casa_arvore/2d/*.png (mesmos nomes da lista de entrega do PROMPTS.md).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, nuvem, salvar  # noqa: E402

P = {}

# ---------------------------------------------------------------- C07 pátio


def fundo_patio(w=2600, h=900, chao=600):
    rnd = random.Random(7)
    defs = (f'<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ceu"]}"/>'
            f'<stop offset="1" stop-color="{C["ceu_claro"]}"/></linearGradient>'
            f'<linearGradient id="grama" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ad884"/>'
            f'<stop offset="1" stop-color="#84c96f"/></linearGradient>')
    s = f'<rect width="{w}" height="{h}" fill="url(#ceu)" stroke="none"/>'
    for cx, cy, k in [(260, 120, 46), (900, 80, 36), (1500, 140, 50), (2100, 90, 40), (2450, 170, 30)]:
        s += nuvem(cx, cy, k)
    # morros
    s += path(f"M0,{chao-60} Q300,{chao-260} 700,{chao-80} T1500,{chao-120} T2300,{chao-90} T{w},{chao-200} "
              f"L{w},{chao} L0,{chao} Z", C["verde_claro"], 'stroke-width="3"')
    s += path(f"M0,{chao-10} Q500,{chao-170} 1100,{chao-30} T2100,{chao-60} T{w},{chao-40} L{w},{chao} L0,{chao} Z",
              "#a8dd8f", 'stroke-width="3"')
    # cerca branca
    y0 = chao - 70
    s += rr(0, y0 + 14, w, 12, 4, C["branco"]) + rr(0, y0 + 42, w, 12, 4, C["branco"])
    for x in range(10, w, 52):
        s += path(f"M{x},{chao+6} L{x},{y0+6} L{x+11},{y0-6} L{x+22},{y0+6} L{x+22},{chao+6} Z", C["branco"],
                  'stroke-width="2.5"')
    # grama
    s += f'<rect x="-5" y="{chao}" width="{w+10}" height="{h-chao+5}" fill="url(#grama)" stroke="{L}"/>'
    for _ in range(140):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(chao + 20, h - 10)
        s += path(f"M{x:.0f},{y:.0f} l-5,-12 M{x:.0f},{y:.0f} l0,-15 M{x:.0f},{y:.0f} l6,-12",
                  extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
    for _ in range(70):
        x, y = rnd.uniform(15, w - 15), rnd.uniform(chao + 25, h - 15)
        cor = rnd.choice([C["rosa"], C["branco"], C["lilas"], C["amarelo"]])
        s += flor(round(x), round(y), 5, cor)
    return svg(w, h, s, defs)


P["fundo_patio"] = fundo_patio()


def arvore_casinha():
    w, h = 1000, 600
    piso = h - 220          # topo do piso da varanda (y = 380)
    s = ""
    # copa (atrás de tudo)
    copa = [(500, 200, 195), (260, 250, 180), (740, 250, 180), (140, 330, 120), (860, 330, 120),
            (330, 150, 145), (670, 150, 145), (500, 120, 115)]
    for cx, cy, r in copa:
        s += circ(cx, cy, r, C["rosa_chiclete"], 'stroke-width="4"')
    for cx, cy, r in copa:
        s += circ(cx, cy, r - 4, C["rosa_chiclete"], 'stroke="none"')
    rnd = random.Random(3)
    for _ in range(40):
        x, y = rnd.uniform(60, 940), rnd.uniform(20, 430)
        if 250 < x < 750 and 40 < y < 400:
            continue
        s += flor(round(x), round(y), 7, C["rosa_claro"], C["rosa_forte"])
    # tronco com raízes
    s += path(f"M425,{piso+20} C430,{h-90} 400,{h-25} 350,{h-3} L650,{h-3} C600,{h-25} 570,{h-90} 575,{piso+20} Z",
              C["madeira_esc"], 'stroke-width="4"')
    s += path(f"M470,{piso+60} q10,60 -5,120 M530,{piso+50} q-8,70 8,140", extra='stroke-width="3" opacity="0.6"')
    # vigas sob a varanda
    s += path(f"M440,{piso+90} L300,{piso+22}", extra=f'stroke-width="16" stroke="{L}"')
    s += path(f"M440,{piso+90} L300,{piso+22}", extra=f'stroke-width="10" stroke="{C["madeira_esc"]}"')
    s += path(f"M560,{piso+90} L700,{piso+22}", extra=f'stroke-width="16" stroke="{L}"')
    s += path(f"M560,{piso+90} L700,{piso+22}", extra=f'stroke-width="10" stroke="{C["madeira_esc"]}"')
    # casinha 480 x 300 (paredes) com telhado
    hx, hw = 260, 480
    topo = piso - 305
    s += rr(hx, topo, hw, piso - topo, 6, C["creme"], 'stroke-width="4"')
    for i in range(1, 6):
        s += path(f"M{hx+4},{topo + i*52} L{hx+hw-4},{topo + i*52}", extra='stroke-width="1.5" opacity="0.25"')
    s += rr(hx, piso - 70, hw, 70, 0, C["rosa"], 'stroke-width="4"')            # barra rosa
    for x in range(hx + 30, hx + hw, 60):
        s += coracao(x, piso - 35, 9, C["rosa_forte"], 'stroke-width="2"')
    # parede lisa onde entra a porta (x 300..430): só a parede, sem porta
    # janelinha redonda
    s += circ(640, topo + 110, 52, C["madeira"], 'stroke-width="4"') + circ(640, topo + 110, 38, C["ceu"])
    s += path(f"M602,{topo+110} L678,{topo+110} M640,{topo+72} L640,{topo+148}", extra='stroke-width="5"')
    # telhado lilás
    s += path(f"M{hx-45},{topo+20} L500,{topo-68} L{hx+hw+45},{topo+20} Q500,{topo-10} {hx-45},{topo+20} Z",
              C["lilas"], 'stroke-width="4"')
    s += path(f"M{hx-45},{topo+20} L500,{topo-68} L{hx+hw+45},{topo+20}", extra='stroke-width="5"')
    s += coracao(500, topo - 18, 14, C["rosa_forte"])
    # piso da varanda (650 de largura)
    s += rr(175, piso, 650, 22, 6, C["madeira"], 'stroke-width="4"')
    for x in range(215, 825, 40):
        s += path(f"M{x},{piso+3} L{x},{piso+19}", extra='stroke-width="1.5" opacity="0.5"')
    return svg(w, h, s)


P["arvore_casinha"] = arvore_casinha()


def grade_varanda():
    w, h = 650, 60
    s = ""
    for x in range(10, w - 5, 32):
        s += rr(x, 6, 14, 52, 5, C["madeira_clara"], 'stroke-width="2.5"')
    s += rr(2, 4, w - 4, 12, 6, C["madeira"], 'stroke-width="3"')
    s += rr(2, 40, w - 4, 10, 5, C["madeira"], 'stroke-width="3"')
    for x in range(42, w, 128):
        s += coracao(x + 16, 29, 9, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["grade_varanda"] = grade_varanda()


def porta(aberta, de_dentro=False):
    w, h = 130, 300
    arco = f"M6,{h-2} L6,62 A59,59 0 0 1 124,62 L124,{h-2} Z"
    s = path(arco, C["madeira_esc"], 'stroke-width="4"')          # batente
    vao = f"M16,{h-2} L16,64 A49,49 0 0 1 114,64 L114,{h-2} Z"
    if not aberta:
        s += path(vao, C["roxo"])
        s += path(f"M28,{h-14} L28,72 A37,37 0 0 1 102,72 L102,{h-14} Z", "none", 'stroke-width="2" opacity="0.5"')
        s += coracao(65, 115, 16, C["rosa_forte"] if not de_dentro else C["lilas"])
        s += circ(98 if not de_dentro else 32, 175, 6, C["dourado"])
    else:
        if de_dentro:
            # lá fora: céu, copa rosa e a varanda
            s += path(vao, C["ceu"])
            s += circ(30, 120, 40, C["rosa_chiclete"], 'stroke="none"') + circ(110, 95, 45, C["rosa_chiclete"], 'stroke="none"')
            s += rr(16, h - 50, 98, 48, 0, C["madeira"], 'stroke="none"')
            s += path(vao, "none")
        else:
            s += path(vao, "#8a4f3a")
            s += path(f"M16,{h-2} L16,64 A49,49 0 0 1 114,64 L114,140 Q65,120 16,150 Z", "#b06a48", 'stroke="none"')
            s += circ(65, 95, 14, "#ffd98a", 'stroke="none" opacity="0.8"')
            s += path(vao, "none")
        # folha encostada para dentro
        s += path(f"M16,{h-2} L16,64 Q20,40 40,30 L40,{h-12} Z", C["roxo_esc"], 'stroke-width="3"')
    return svg(w, h, s)


P["porta_fechada"] = porta(False)
P["porta_aberta"] = porta(True)


def escada_madeira():
    w, h = 60, 220
    s = rr(4, 2, 12, h - 4, 5, C["madeira"]) + rr(w - 16, 2, 12, h - 4, 5, C["madeira"])
    for y in range(22, h - 8, 34):
        s += rr(10, y, w - 20, 11, 4, C["madeira_clara"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["escada_madeira"] = escada_madeira()


def escada_corda():
    w, h = 50, 220
    s = path(f"M10,2 C6,80 14,150 8,{h-4}", extra='stroke-width="7"')
    s += path(f"M10,2 C6,80 14,150 8,{h-4}", extra=f'stroke-width="3.5" stroke="{C["madeira_clara"]}"')
    s += path(f"M40,2 C44,80 36,150 43,{h-4}", extra='stroke-width="7"')
    s += path(f"M40,2 C44,80 36,150 43,{h-4}", extra=f'stroke-width="3.5" stroke="{C["madeira_clara"]}"')
    for i, y in enumerate(range(24, h - 10, 32)):
        t = (i - 2.5) * 1.2
        s += rr(4, y, 42, 9, 4, C["madeira"], f'stroke-width="2.5" transform="rotate({t:.1f} 25 {y+4})"')
    return svg(w, h, s)


P["escada_corda"] = escada_corda()


def escorregador(arco_iris):
    w, h = 470, 220
    curva = "M22,30 C170,30 250,120 330,175 S430,205 452,205"
    s = ""
    # apoios
    s += rr(300, 170, 14, 48, 4, C["madeira_esc"]) + rr(180, 85, 14, 133, 4, C["madeira_esc"])
    s += path(curva, extra='stroke-width="50"')
    if arco_iris:
        cores = ["#ff6f91", "#ffa45c", "#ffe066", "#7ddc8a", "#73c2fb", "#b48cf2"]
        for i, c in enumerate(cores):
            s += path(curva, extra=f'stroke-width="{44-7*i}" stroke="{c}"')
    else:
        s += path(curva, extra=f'stroke-width="44" stroke="{C["roxo"]}"')
        s += path(curva, extra=f'stroke-width="24" stroke="{C["rosa"]}"')
        s += path(curva, extra=f'stroke-width="6" stroke="{C["rosa_claro"]}"')
    # borda de cima
    s += rr(4, 6, 40, 48, 10, C["roxo_esc"] if not arco_iris else "#ff6f91")
    if arco_iris:
        for x, y, r in [(120, 20, 10), (250, 70, 12), (360, 150, 9), (430, 180, 11), (60, 70, 8)]:
            s += estrela(x, y, r, C["branco"], 4, 'stroke-width="2"')
    return svg(w, h, s)


P["escorregador_rosa"] = escorregador(False)
P["escorregador_arco_iris"] = escorregador(True)

P["brilho"] = svg(40, 40, estrela(20, 20, 18, C["branco"], 4, 'stroke-width="2"') +
                  estrela(20, 20, 8, C["rosa_chiclete"], 4, 'stroke="none"'))


def balanco_estrutura():
    w, h = 300, 380
    s = path(f"M30,{h-2} L50,24", extra='stroke-width="24"') + path(f"M30,{h-2} L50,24", extra=f'stroke-width="17" stroke="{C["madeira"]}"')
    s += path(f"M270,{h-2} L250,24", extra='stroke-width="24"') + path(f"M270,{h-2} L250,24", extra=f'stroke-width="17" stroke="{C["madeira"]}"')
    s += rr(14, 10, 272, 26, 10, C["madeira_esc"], 'stroke-width="3"')
    # flores enroladas
    for i in range(7):
        y = 60 + i * 45
        s += path(f"M{38+ (y/380)*-20 + 12},{y} q-14,12 0,24", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"')
        s += flor(44 - y * 0.05, y, 6, C["rosa"] if i % 2 else C["lilas"])
        s += flor(256 + y * 0.05, y + 20, 6, C["lilas"] if i % 2 else C["rosa"])
    s += path("M150,36 l0,0", extra='stroke-width="0"')
    return svg(w, h, s)


P["balanco_estrutura"] = balanco_estrutura()


def balanco_assento():
    w, h = 130, 260
    s = path(f"M22,2 L22,{h-28}", extra='stroke-width="6"') + path(f"M22,2 L22,{h-28}", extra=f'stroke-width="3" stroke="{C["madeira_clara"]}"')
    s += path(f"M108,2 L108,{h-28}", extra='stroke-width="6"') + path(f"M108,2 L108,{h-28}", extra=f'stroke-width="3" stroke="{C["madeira_clara"]}"')
    s += rr(6, h - 34, 118, 24, 9, C["rosa_chiclete"], 'stroke-width="3.5"')
    s += coracao(65, h - 22, 7, C["branco"], 'stroke-width="2"')
    s += circ(22, 6, 5, C["madeira_esc"]) + circ(108, 6, 5, C["madeira_esc"])
    return svg(w, h, s)


P["balanco_assento"] = balanco_assento()


def cacho(com):
    w, h = 70, 70
    s = path("M35,4 L35,22", extra='stroke-width="3"')
    for dx in (-16, 16):
        s += ell(35 + dx, 16, 13, 8, C["rosa"], f'transform="rotate({dx*1.5} {35+dx} 16)"')
    if com:
        for x, y in [(24, 34), (46, 34), (35, 44), (22, 54), (48, 54), (35, 60)]:
            s += circ(x, y, 9, C["rosa_forte"], 'stroke-width="2.5"') + circ(x - 3, y - 3, 2.5, C["branco"], 'stroke="none"')
        s += estrela(56, 22, 7, C["branco"], 4, 'stroke-width="1.5"')
    return svg(w, h, s)


P["cacho_com"] = cacho(True)
P["cacho_colhido"] = cacho(False)
P["frutinha"] = svg(30, 30, path("M15,3 L15,8", extra='stroke-width="2"') +
                    ell(20, 6, 6, 3.5, C["rosa"], 'stroke-width="1.5"') +
                    circ(15, 18, 10, C["rosa_forte"], 'stroke-width="2.5"') + circ(11, 14, 3, C["branco"], 'stroke="none"'))


def mesa_piquenique():
    w, h = 320, 130
    s = ""
    s += rr(30, 92, 260, 14, 6, C["madeira"]) + rr(40, 106, 12, 22, 3, C["madeira_esc"]) + rr(268, 106, 12, 22, 3, C["madeira_esc"])
    s += rr(70, 50, 14, 78, 4, C["madeira_esc"]) + rr(236, 50, 14, 78, 4, C["madeira_esc"])
    s += rr(10, 30, 300, 26, 8, C["madeira"])
    # toalha xadrez
    s += path("M40,28 L280,28 L272,62 L48,62 Z", C["rosa_claro"], 'stroke-width="3"')
    for x in range(52, 272, 22):
        s += rr(x, 30, 11, 30, 0, C["rosa"], 'stroke="none" opacity="0.8"')
    s += rr(44, 38, 232, 9, 0, C["rosa"], 'stroke="none" opacity="0.6"')
    s += path("M40,28 L280,28 L272,62 L48,62 Z", "none", 'stroke-width="3"')
    return svg(w, h, s)


P["mesa_piquenique"] = mesa_piquenique()


def cesto(cheio):
    w, h = 90, 70
    s = path("M14,30 Q45,-12 76,30", extra='stroke-width="7"') + path("M14,30 Q45,-12 76,30", extra=f'stroke-width="3.5" stroke="{C["mel"]}"')
    if cheio:
        for x, y in [(30, 30), (44, 26), (58, 30), (37, 22), (52, 21)]:
            s += circ(x, y, 7, C["rosa_forte"], 'stroke-width="2"')
    s += path("M8,30 L82,30 L74,66 L16,66 Z", C["mel"], 'stroke-width="3"')
    for y in (40, 50, 58):
        s += path(f"M{12 + (y-30)*0.2},{y} L{78 - (y-30)*0.2},{y}", extra='stroke-width="1.5" opacity="0.5"')
    s += path("M8,30 Q24,44 36,30 Z", C["rosa"], 'stroke-width="2"')
    return svg(w, h, s)


P["cesto_vazio"] = cesto(False)
P["cesto_cheio"] = cesto(True)


def bola():
    s = circ(30, 30, 27, C["amarelo"])
    s += path("M30,3 C15,15 15,45 30,57 C20,45 20,15 30,3 Z", C["rosa_chiclete"], 'stroke-width="2"')
    s += path("M3,30 C15,20 45,20 57,30 C45,42 15,42 3,30 Z", C["lilas"], 'stroke-width="2"')
    s += path("M30,3 C45,15 45,45 30,57", C["azul"], 'stroke-width="2" fill-opacity="0"')
    s += path("M30,3 A27,27 0 0 1 57,30 L30,30 Z", C["azul"], 'stroke-width="2"')
    s += circ(30, 30, 27, "none", 'stroke-width="3"') + circ(20, 18, 4, C["branco"], 'stroke="none" opacity="0.8"')
    return svg(60, 60, s)


P["bola"] = bola()


def placa(desenho):
    w, h = 120, 160
    s = rr(52, 50, 16, 108, 4, C["madeira_esc"])
    s += path("M8,14 L96,14 L114,46 L96,78 L8,78 Z", C["madeira"], 'stroke-width="3.5"')
    s += path("M60,46 L84,46 M76,38 L86,46 L76,54", extra='stroke-width="4"')    # setinha
    if desenho == "casa":
        s += path("M20,52 L20,38 L33,26 L46,38 L46,52 Z", C["rosa"], 'stroke-width="2.5"')
        s += rr(29, 42, 8, 10, 1, C["roxo"], 'stroke-width="2"')
    else:
        s += path("M16,56 L34,26 L52,56 Z", C["verde"], 'stroke-width="2.5"')
        s += path("M34,26 L34,56 M28,56 L34,44 L40,56", extra='stroke-width="2"')
    return svg(w, h, s)


P["placa_casa"] = placa("casa")
P["placa_cabana"] = placa("cabana")

# ---------------------------------------------------------------- C08 dentro


def fundo_dentro():
    w, h, chao = 1600, 900, 640
    s = rr(-5, -5, w + 10, h + 10, 0, C["creme"], 'stroke="none"')
    for x in range(0, w, 56):
        s += rr(x, 60, 56, chao - 60, 0, "#ffe9c7" if (x // 56) % 2 else C["creme"], 'stroke-width="1.5" stroke-opacity="0.45"')
    # teto inclinado
    s += path(f"M-5,-5 L{w+5},-5 L{w+5},90 L800,20 L-5,90 Z", C["madeira"], 'stroke-width="4"')
    s += path(f"M-5,90 L800,20 L{w+5},90", extra='stroke-width="10"')
    s += path(f"M-5,90 L800,20 L{w+5},90", extra=f'stroke-width="5" stroke="{C["madeira_esc"]}"')
    # luzinhas
    s += path(f"M0,70 Q200,110 400,60 T800,60 T1200,60 T{w},70", extra='stroke-width="2"')
    for i in range(1, 20):
        x = i * w / 20
        y = 70 + 22 * math.sin(i * 1.55)
        s += circ(f"{x:.0f}", f"{y + 10:.0f}", 9, C["amarelo"], 'stroke-width="2"')
    # janela redonda com folhas rosa
    cx, cy, r = 800, 270, 150
    s += circ(cx, cy, r + 18, C["madeira_esc"], 'stroke-width="4"') + circ(cx, cy, r, C["ceu"])
    s += f'<clipPath id="jan"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    s += f'<g clip-path="url(#jan)" stroke="none">'
    for fx, fy, fr in [(680, 180, 70), (900, 160, 80), (700, 400, 60), (930, 390, 75), (800, 130, 50)]:
        s += circ(fx, fy, fr, C["rosa_chiclete"])
    s += '</g>'
    s += path(f"M{cx-r},{cy} L{cx+r},{cy} M{cx},{cy-r} L{cx},{cy+r}", extra='stroke-width="8"')
    s += path(f"M{cx-r},{cy} L{cx+r},{cy} M{cx},{cy-r} L{cx},{cy+r}", extra=f'stroke-width="4" stroke="{C["madeira_esc"]}"')
    # rodapé e chão
    s += rr(-5, chao - 16, w + 10, 18, 0, C["madeira_esc"], 'stroke-width="3"')
    s += rr(-5, chao, w + 10, h - chao + 5, 0, "#e7bb87", 'stroke-width="3"')
    for y in range(chao + 40, h, 50):
        s += path(f"M0,{y} L{w},{y}", extra='stroke-width="1.5" opacity="0.35"')
    for i, y in enumerate(range(chao, h, 50)):
        for x in range(120 + (i % 2) * 150, w, 300):
            s += path(f"M{x},{y} L{x},{y+50}", extra='stroke-width="1.5" opacity="0.3"')
    return svg(w, h, s)


P["fundo_dentro"] = fundo_dentro()
P["porta_dentro_fechada"] = porta(False, True)
P["porta_dentro_aberta"] = porta(True, True)


def cama():
    w, h = 360, 150
    s = rr(4, 20, 28, 128, 8, C["madeira"]) + rr(w - 32, 50, 28, 98, 8, C["madeira"])
    s += rr(18, 80, w - 36, 52, 14, C["branco"])
    s += rr(18, 92, w - 36, 46, 14, C["rosa"])
    for x in range(60, w - 40, 55):
        s += coracao(x, 116, 8, C["rosa_forte"], 'stroke-width="2"')
    s += rr(36, 50, 72, 40, 18, C["branco"]) + rr(90, 56, 64, 36, 16, C["lilas_claro"]) + rr(48, 64, 50, 26, 12, C["rosa_claro"])
    s += coracao(18, 30, 10, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["cama"] = cama()


def cozinha(ligada):
    w, h = 220, 200
    s = rr(14, 6, 192, 12, 4, C["madeira"]) + rr(30, 18, 10, 18, 2, C["madeira_esc"]) + rr(180, 18, 10, 18, 2, C["madeira_esc"])
    for i, c in enumerate([C["rosa"], C["lilas"], C["amarelo"]]):
        s += rr(40 + i * 50, -2 + 0, 0, 0, 0, c)
    s += rr(6, 70, 208, 128, 10, C["rosa"])
    s += rr(2, 62, 216, 18, 6, C["branco"])
    # bocas
    for x in (60, 160):
        if ligada:
            s += ell(x, 70, 30, 7, "#ffb067", 'stroke="none" opacity="0.7"')
        s += ell(x, 70, 22, 5, "#ff9a3c" if ligada else C["cinza"], 'stroke-width="2.5"')
    # forninho
    s += rr(30, 96, 110, 82, 10, C["branco"]) + rr(42, 108, 86, 48, 8, "#ffd9a8" if ligada else "#e9d7ef")
    s += rr(52, 98, 66, 6, 3, C["rosa_forte"], 'stroke-width="2"')
    for i, y in enumerate((100, 130, 160)):
        s += circ(170, y + 6, 9, C["lilas"], 'stroke-width="2.5"')
    s += coracao(190, 182, 7, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["cozinha_desligada"] = cozinha(False)
P["cozinha_ligada"] = cozinha(True)
P["panelinha"] = svg(50, 35, rr(30, 12, 18, 6, 3, C["roxo"], 'stroke-width="2"') +
                     path("M4,10 L34,10 L31,32 L7,32 Z", C["rosa_chiclete"], 'stroke-width="2.5"') +
                     rr(2, 7, 34, 6, 3, C["rosa"], 'stroke-width="2"'))
P["bule"] = svg(50, 45, path("M36,22 Q48,14 46,6", extra='stroke-width="5"') +
                path("M36,22 Q48,14 46,6", extra=f'stroke-width="2.5" stroke="{C["branco"]}"') +
                path("M10,18 Q4,26 10,32", extra='stroke-width="3"') +
                ell(23, 28, 15, 14, C["branco"], 'stroke-width="2.5"') +
                circ(17, 25, 2.5, C["rosa_chiclete"], 'stroke="none"') + circ(27, 33, 2.5, C["lilas"], 'stroke="none"') +
                circ(29, 22, 2.5, C["rosa_chiclete"], 'stroke="none"') + ell(23, 14, 9, 3, C["rosa"], 'stroke-width="2"') +
                circ(23, 9, 3, C["rosa_forte"], 'stroke-width="1.5"'))


def xicara(cha):
    s = ell(12, 22, 11, 2.5, C["rosa"], 'stroke-width="1.5"')
    s += path("M4,11 L20,11 Q19,21 12,21 Q5,21 4,11 Z", C["branco"], 'stroke-width="1.8"')
    s += path("M20,13 q4,1 1,5", extra='stroke-width="1.8"')
    if cha:
        s += ell(12, 11.5, 7.5, 1.8, "#c98c56", 'stroke-width="1"')
        s += coracao(12, 4.5, 3, "none", 'stroke-width="1.3" stroke="#b9a7c9"')
    return svg(25, 25, s)


P["xicara_vazia"] = xicara(False)
P["xicara_cha"] = xicara(True)


def mesinha_cha():
    w, h = 180, 80
    s = rr(40, 30, 12, 48, 4, C["madeira_esc"]) + rr(128, 30, 12, 48, 4, C["madeira_esc"])
    s += ell(90, 22, 86, 16, C["madeira"])
    s += path("M8,22 Q12,42 30,40 Q44,48 60,40 Q76,48 90,40 Q104,48 120,40 Q136,48 150,40 Q168,42 172,22 Q90,40 8,22 Z",
              C["branco"], 'stroke-width="2.5"')
    s += ell(90, 20, 78, 12, C["branco"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["mesinha_cha"] = mesinha_cha()
P["cadeirinha"] = svg(60, 80, rr(8, 4, 44, 46, 10, C["madeira"]) + rr(16, 12, 28, 30, 8, C["madeira_clara"], 'stroke-width="2"') +
                      rr(8, 48, 8, 30, 3, C["madeira_esc"], 'stroke-width="2.5"') + rr(44, 48, 8, 30, 3, C["madeira_esc"], 'stroke-width="2.5"') +
                      rr(2, 44, 56, 14, 6, C["rosa"]) + coracao(30, 26, 6, C["rosa_forte"], 'stroke-width="1.5"'))


def bau(aberto):
    w, h = 160, 160
    s = ""
    if aberto:
        s += path("M10,92 L22,22 L150,22 L150,92 Z", C["madeira_esc"], 'stroke-width="3"')     # tampa levantada
        s += coracao(86, 56, 14, C["rosa_forte"])
        s += circ(48, 88, 18, C["amarelo"]) + rr(70, 64, 22, 36, 6, C["azul"]) + circ(110, 84, 16, C["rosa"])
        s += estrela(132, 70, 12, C["lilas"], 5, 'stroke-width="2"')
    s += rr(8, 92 if aberto else 92, 144, 66, 8, C["madeira"])
    if not aberto:
        s += path("M6,96 Q80,48 154,96 Z", C["madeira_esc"], 'stroke-width="3"')
        s += coracao(80, 80, 11, C["rosa_forte"], 'stroke-width="2.5"')
    s += rr(8, 108, 144, 8, 2, C["madeira_esc"], 'stroke-width="2"')
    s += rr(70, 100, 20, 22, 4, C["dourado"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["bau_fechado"] = bau(False)
P["bau_aberto"] = bau(True)


def unicornio():
    s = ell(45, 66, 26, 20, C["rosa_claro"])                                  # corpo sentado
    s += ell(28, 84, 9, 5, C["rosa"], 'stroke-width="2"') + ell(62, 84, 9, 5, C["rosa"], 'stroke-width="2"')
    s += path("M18,34 Q8,52 16,62 Q22,50 26,46 Z", C["lilas"], 'stroke-width="2.5"')   # crina
    s += ell(44, 36, 21, 18, C["rosa_claro"])
    s += path("M40,20 L46,2 L52,20 Z", C["amarelo"], 'stroke-width="2.5"')
    s += path("M30,22 L28,10 L38,18 Z", C["rosa_claro"], 'stroke-width="2.5"')
    s += path("M24,26 Q30,14 44,18 Q34,22 30,34 Z", C["lilas"], 'stroke-width="2.5"')
    s += circ(48, 36, 3, L, 'stroke="none"') + ell(58, 44, 6, 4, C["rosa"], 'stroke-width="2"')
    s += path("M70,64 Q86,56 82,76 Q76,70 70,72 Z", C["lilas"], 'stroke-width="2.5"')
    return svg(90, 90, s)


P["unicornio"] = unicornio()


def ursinho_heroi():
    s = path("M22,40 Q6,70 14,96 L66,96 Q74,70 58,40 Z", C["vermelho_rosa"], 'stroke-width="2.5"')      # capa
    s += ell(40, 70, 20, 22, "#c98c56")
    s += ell(24, 92, 9, 6, "#c98c56", 'stroke-width="2"') + ell(56, 92, 9, 6, "#c98c56", 'stroke-width="2"')
    s += ell(40, 72, 10, 12, "#efcfa4", 'stroke-width="2"') + estrela(40, 70, 7, C["amarelo"], 5, 'stroke-width="1.5"')
    s += circ(22, 18, 9, "#c98c56") + circ(58, 18, 9, "#c98c56")
    s += ell(40, 34, 22, 20, "#c98c56")
    s += path("M20,30 Q40,22 60,30 L58,38 Q40,32 22,38 Z", C["roxo"], 'stroke-width="2"')            # máscara
    s += circ(32, 33, 2.5, L, 'stroke="none"') + circ(48, 33, 2.5, L, 'stroke="none"')
    s += ell(40, 44, 7, 5, "#efcfa4", 'stroke-width="2"') + circ(40, 42, 2, L, 'stroke="none"')
    return svg(80, 100, s)


P["ursinho_heroi"] = ursinho_heroi()


def tapete():
    w, h = 300, 80
    s = ell(150, 40, 146, 37, C["lilas"]) + ell(150, 40, 126, 27, C["lilas_claro"], 'stroke-width="2"')
    for i in range(14):
        a = 2 * math.pi * i / 14
        s += coracao(150 + 137 * math.cos(a), 40 + 32 * math.sin(a), 5, C["rosa_forte"], 'stroke="none"')
    s += coracao(150, 40, 10, C["rosa"], 'stroke-width="2"')
    return svg(w, h, s)


P["tapete"] = tapete()


def passarinho(voando):
    s = path("M8,20 L1,15 L3,24 Z", C["azul"], 'stroke-width="1.8"')
    s += ell(19, 21, 12, 10, "#bfe3ff", 'stroke-width="2"')
    if voando:
        s += path("M14,18 Q10,2 24,6 Q22,14 20,18 Z", C["azul"], 'stroke-width="1.8"')
    else:
        s += ell(15, 23, 6, 4, C["azul"], 'stroke-width="1.8"')
        s += path("M16,31 l0,3 M22,31 l0,3", extra='stroke-width="1.8"')
    s += circ(26, 15, 8, "#bfe3ff", 'stroke-width="2"') + circ(28, 13, 1.8, L, 'stroke="none"')
    s += path("M33,15 L39,17 L33,19 Z", C["laranja"], 'stroke-width="1.5"')
    s += circ(29, 18, 1.8, C["rosa"], 'stroke="none"')
    return svg(40, 35, s)


P["passarinho_pousado"] = passarinho(False)
P["passarinho_voando"] = passarinho(True)


if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario/casa_arvore/2d")
    salvar(P, os.path.join(destino, "svg"), destino)
    print(len(P), "peças em", destino)
