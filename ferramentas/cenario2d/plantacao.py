"""Peças 2D provisórias da Plantação (fases 1 e 2 do PROMPTS.md; a fase 3 espera a aprovação dos bichos).

Uso: python3 ferramentas/cenario2d/plantacao.py
Saída: arte/cenario/plantacao/2d/*.png
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, nuvem, salvar  # noqa: E402

P = {}
TERRA, TERRA_FOFA, TERRA_ESC = "#c99a6b", "#a8784f", "#8d6342"


def margarida(cx, cy, r):
    s = ""
    for i in range(8):
        a = 2 * math.pi * i / 8
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        s += ell(round(x, 1), round(y, 1), r * 0.62, r * 0.32, C["branco"],
                 f'stroke-width="1.6" transform="rotate({math.degrees(a):.0f} {x:.1f} {y:.1f})"')
    return s + circ(cx, cy, r * 0.45, C["amarelo"], 'stroke-width="1.6"')


def tulipa(cx, cy, r, cor=None):
    cor = cor or C["rosa_chiclete"]
    return path(f"M{cx-r},{cy-r*0.6} L{cx-r*0.5},{cy-r*0.1} L{cx},{cy-r*0.8} L{cx+r*0.5},{cy-r*0.1} L{cx+r},{cy-r*0.6} "
                f"Q{cx+r},{cy+r} {cx},{cy+r} Q{cx-r},{cy+r} {cx-r},{cy-r*0.6} Z", cor, 'stroke-width="2"')


def folha(x, y, comp, ang, cor=None, sw=2):
    cor = cor or C["verde"]
    return ell(x + comp / 2, y, comp / 2, comp / 5, cor, f'stroke-width="{sw}" transform="rotate({ang} {x} {y})"')


# ---------------------------------------------------------------- fase 1

P["bica"] = svg(110, 190,
                rr(10, 20, 30, 168, 6, C["madeira"]) + rr(4, 10, 100, 20, 7, C["madeira_esc"]) +
                path("M40,60 L76,60 L76,74", extra='stroke-width="10"') + path("M40,60 L76,60 L76,74", extra=f'stroke-width="5" stroke="{C["cinza"]}"') +
                circ(58, 52, 8, C["rosa_forte"], 'stroke-width="2.5"') +
                path("M76,84 q-3,8 0,11 q3,-3 0,-11 Z", C["agua"], 'stroke-width="1.5"') +
                path("M54,120 Q78,96 102,120", extra='stroke-width="3"') +
                path("M50,120 L106,120 L100,170 L56,170 Z", C["madeira"], 'stroke-width="2.5"') +
                rr(51, 130, 54, 6, 2, C["dourado"], 'stroke-width="1.5"') + ell(78, 120, 28, 5, C["agua"], 'stroke-width="2"') +
                flor(24, 120, 6, C["rosa"]))


def regador(cheio):
    s = path("M52,22 L76,8 L78,14 L58,30 Z", C["rosa_chiclete"], 'stroke-width="2.5"')
    s += ell(77, 10, 3, 5, C["rosa"], 'stroke-width="2"')
    s += path("M14,18 Q8,32 14,42", extra='stroke-width="5"') + path("M14,18 Q8,32 14,42", extra=f'stroke-width="2.5" stroke="{C["rosa"]}"')
    s += rr(14, 18, 42, 34, 9, C["rosa"], 'stroke-width="2.5"') + ell(35, 18, 21, 4, C["rosa_chiclete"], 'stroke-width="2"')
    s += path("M24,18 Q35,4 46,18", extra='stroke-width="3.5"')
    s += coracao(35, 35, 7, C["rosa_forte"], 'stroke-width="1.5"')
    if cheio:
        for x, y in [(74, 22), (69, 32), (78, 34), (73, 44)]:
            s += path(f"M{x},{y} q-2,4 0,6 q2,-2 0,-6 Z", C["agua"], 'stroke-width="1.2"')
    return svg(80, 55, s)


P["regador_vazio"] = regador(False)
P["regador_cheio"] = regador(True)
P["enxada"] = svg(45, 90, rr(19, 6, 8, 82, 4, C["madeira_clara"], 'stroke-width="2.5"') +
                  path("M6,8 Q22,-2 40,8 L36,24 Q22,18 10,24 Z", C["lilas"], 'stroke-width="2.5"') +
                  rr(18, 10, 10, 8, 2, C["madeira_esc"], 'stroke-width="2"'))


def desenho_planta(tipo, cx, cy, k=1.0):
    if tipo == "cenoura":
        return (path(f"M{cx-8*k},{cy-8*k} L{cx+8*k},{cy-8*k} L{cx},{cy+16*k} Z", C["laranja"], 'stroke-width="2"') +
                folha(cx, cy - 8 * k, 10 * k, -110, C["verde"], 1.5) + folha(cx, cy - 8 * k, 10 * k, -70, C["verde"], 1.5))
    if tipo == "alface":
        return circ(cx, cy, 12 * k, C["verde"], 'stroke-width="2"') + circ(cx, cy, 7 * k, C["verde_claro"], 'stroke-width="1.5"')
    if tipo == "tomate":
        return circ(cx, cy, 11 * k, "#ef5a5a", 'stroke-width="2"') + estrela(cx, cy - 10 * k, 5 * k, C["verde_esc"], 5, 'stroke-width="1"')
    if tipo == "morango":
        return (path(f"M{cx-10*k},{cy-6*k} Q{cx},{cy-12*k} {cx+10*k},{cy-6*k} Q{cx+8*k},{cy+10*k} {cx},{cy+14*k} "
                     f"Q{cx-8*k},{cy+10*k} {cx-10*k},{cy-6*k} Z", "#f0506e", 'stroke-width="2"') +
                estrela(cx, cy - 8 * k, 6 * k, C["verde_esc"], 5, 'stroke-width="1"'))
    if tipo == "abobora":
        return (ell(cx, cy + 2 * k, 14 * k, 11 * k, C["laranja"], 'stroke-width="2"') +
                ell(cx, cy + 2 * k, 5 * k, 11 * k, C["laranja"], 'stroke-width="1.5"') + rr(cx - 2 * k, cy - 13 * k, 4 * k, 6 * k, 1, C["verde_esc"], 'stroke-width="1.5"'))
    # girassol
    s = ""
    for i in range(10):
        a = 2 * math.pi * i / 10
        s += circ(round(cx + 10 * k * math.cos(a), 1), round(cy + 10 * k * math.sin(a), 1), 5 * k, C["amarelo"], 'stroke-width="1.5"')
    return s + circ(cx, cy, 7 * k, "#8a5a3c", 'stroke-width="1.5"')


def pacote(tipo):
    s = path("M6,10 L54,10 L54,76 L6,76 Z", "#f6ead2", 'stroke-width="2.5"')
    s += path("M6,10 L12,4 L18,10 L24,4 L30,10 L36,4 L42,10 L48,4 L54,10", extra='stroke-width="2"')
    s += rr(12, 20, 36, 40, 6, C["branco"], 'stroke-width="2"') + desenho_planta(tipo, 30, 40, 1.15)
    s += ell(30, 68, 4, 2.5, TERRA, 'stroke-width="1.5"')
    return svg(60, 80, s)


for t in ("cenoura", "alface", "tomate", "morango", "abobora", "girassol"):
    P[f"sementes_{t}"] = pacote(t)


def cesta(cheia, w=120, h=80):
    s = path(f"M18,40 Q60,-12 102,40", extra='stroke-width="8"') + path("M18,40 Q60,-12 102,40", extra=f'stroke-width="4" stroke="{C["mel"]}"')
    if cheia:
        s += desenho_planta("cenoura", 34, 34, 1.3) + desenho_planta("tomate", 56, 36, 1.2) + desenho_planta("alface", 78, 34, 1.3)
        s += circ(96, 38, 9, "#ef5a5a", 'stroke-width="2"') + desenho_planta("morango", 46, 40, 0.9)
    s += path("M8,40 L112,40 L102,78 L18,78 Z", C["mel"], 'stroke-width="3"')
    for y in (50, 60, 70):
        s += path(f"M{10 + (y-40)*0.25},{y} L{110 - (y-40)*0.25},{y}", extra='stroke-width="1.5" opacity="0.5"')
    s += path("M8,40 L30,40 L26,56 Z", C["rosa"], 'stroke-width="2"') + path("M14,40 l3,8 M22,40 l2,8", extra=f'stroke="{C["branco"]}" stroke-width="2"')
    return svg(w, h, s)


P["cesta_vazia"] = cesta(False)
P["cesta_cheia"] = cesta(True)


def quadradinho(estado, oy=0):
    """Canteiro 200 x 70 com o topo em oy."""
    cor = {"dura": TERRA, "fofa": TERRA_FOFA, "fechada": "#bfae9e"}[estado]
    s = path(f"M14,{oy+14} L186,{oy+14} L196,{oy+60} L4,{oy+60} Z", cor, 'stroke-width="3"')
    if estado == "fofa":
        for y in (oy + 26, oy + 40, oy + 52):
            s += path(f"M{16},{y} q14,-6 28,0 t28,0 t28,0 t28,0 t28,0 t28,0", extra=f'stroke="{TERRA_ESC}" stroke-width="2.5"')
    elif estado == "dura":
        for x, y in [(40, oy + 30), (90, oy + 44), (140, oy + 28), (160, oy + 50), (60, oy + 50)]:
            s += path(f"M{x},{y} l8,4 l6,-3", extra=f'stroke="{TERRA_ESC}" stroke-width="2"')
    s += rr(0, oy + 56, 200, 13, 4, C["madeira"], 'stroke-width="2.5"') + rr(8, oy + 8, 184, 9, 4, C["madeira_clara"], 'stroke-width="2"')
    if estado == "fechada":
        s += rr(64, oy + 16, 72, 38, 6, C["madeira"], 'stroke-width="2.5"')
        s += path(f"M92,{oy+32} L92,{oy+24} A8,8 0 0 1 108,{oy+24} L108,{oy+32}", extra='stroke-width="3"')
        s += rr(88, oy + 30, 24, 20, 4, C["dourado"], 'stroke-width="2.5"') + circ(100, oy + 39, 3, L, 'stroke="none"')
    return s


for e in ("dura", "fofa", "fechada"):
    P[f"terra_{e}"] = svg(200, 70, quadradinho(e))


def planta_no_quadradinho(tipo, estagio, h=200):
    oy = h - 70
    base = oy + 24     # onde a planta nasce
    s = ""
    xs = (55, 100, 145)
    if tipo == "tomate" and estagio >= 2:
        s += rr(96, base - 170 if h == 240 else base - 130, 8, 170 if h == 240 else 130, 3, C["madeira_clara"], 'stroke-width="2"')
    s += quadradinho("fofa", oy)
    for x in xs:
        if estagio == 1:
            s += ell(x, base + 4, 6, 4, "#e9d29a", 'stroke-width="2"')
        elif estagio == 2:
            s += path(f"M{x},{base+6} L{x},{base-16}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"')
            s += folha(x, base - 14, 14, -150) + folha(x, base - 14, 14, -30)
        else:
            grande = estagio == 4
            if tipo == "cenoura":
                if grande:
                    s += path(f"M{x-12},{base} L{x+12},{base} L{x},{base+18} Z", C["laranja"], 'stroke-width="2"')
                for a in (-130, -105, -80, -55):
                    s += folha(x, base, 34 if grande else 24, a, C["verde"] if grande else C["verde_claro"])
            elif tipo == "alface":
                r = 26 if grande else 17
                s += ell(x, base - r * 0.5, r, r * 0.8, C["verde"], 'stroke-width="2.5"')
                s += ell(x, base - r * 0.55, r * 0.6, r * 0.5, C["verde_claro"], 'stroke-width="2"')
            elif tipo == "tomate":
                top = 120 if h == 240 else 90
                s += path(f"M{x},{base+4} C{x-6},{base-top/2} {x+8},{base-top/2} {x},{base-top}", extra=f'stroke="{C["verde_esc"]}" stroke-width="4"')
                for i, yy in enumerate(range(int(base - 20), int(base - top), -26)):
                    s += folha(x, yy, 22, -160 if i % 2 else -20)
                if grande:
                    for dx, yy in [(-12, base - 40), (12, base - 70), (-10, base - 98)]:
                        s += circ(x + dx, yy, 10, "#ef5a5a", 'stroke-width="2"') + circ(x + dx - 3, yy - 3, 2.5, C["branco"], 'stroke="none"')
            elif tipo == "morango":
                for a in (-140, -90, -40):
                    s += folha(x, base, 24 if grande else 18, a)
                if grande:
                    s += desenho_planta("morango", x - 12, base + 2, 0.8) + desenho_planta("morango", x + 12, base, 0.8)
            if grande:
                s += estrela(x + 18, base - 40, 7, C["branco"], 4, 'stroke-width="1.5"')
    return svg(200, h, s)


for tipo, h in (("cenoura", 200), ("alface", 200), ("tomate", 240)):
    for e in range(1, 5):
        P[f"{tipo}_{e}"] = planta_no_quadradinho(tipo, e, h)

P["colheita_cenoura"] = svg(30, 60, path("M8,22 L22,22 L16,58 L14,58 Z", C["laranja"], 'stroke-width="2"') +
                            path("M11,30 l5,0 M12,40 l5,0", extra='stroke-width="1.5"') +
                            folha(15, 22, 18, -115) + folha(15, 22, 18, -65) + folha(15, 22, 20, -90))
P["colheita_alface"] = svg(50, 45, ell(25, 26, 22, 17, C["verde"], 'stroke-width="2.5"') + ell(25, 24, 14, 11, C["verde_claro"], 'stroke-width="2"') +
                           ell(25, 23, 7, 6, "#e3f5cf", 'stroke-width="1.5"'))
P["colheita_tomate"] = svg(30, 30, circ(15, 17, 12, "#ef5a5a", 'stroke-width="2"') + estrela(15, 6, 6, C["verde_esc"], 5, 'stroke-width="1.2"') +
                           circ(10, 13, 2.5, C["branco"], 'stroke="none"'))


def arvore_fruta(w, h, fruta, com, copa_cor=None, frutas_cor="#ef4d4d"):
    copa_cor = copa_cor or C["verde"]
    cx = w / 2
    tronco_top = h * 0.42
    s = path(f"M{cx-24},{tronco_top} C{cx-22},{h-60} {cx-34},{h-16} {cx-48},{h-3} L{cx+48},{h-3} C{cx+34},{h-16} {cx+22},{h-60} {cx+24},{tronco_top} Z",
             C["madeira_esc"], 'stroke-width="3.5"')
    r = w * 0.42
    copa = [(cx, r + 6, r), (cx - r * 0.55, r * 1.6, r * 0.62), (cx + r * 0.55, r * 1.6, r * 0.62), (cx, r * 1.75, r * 0.7)]
    for x, y, rr_ in copa:
        s += circ(round(x, 1), round(y, 1), round(rr_, 1), copa_cor, 'stroke-width="3.5"')
    for x, y, rr_ in copa:
        s += circ(round(x, 1), round(y, 1), round(rr_ - 3.5, 1), copa_cor, 'stroke="none"')
    if com:
        rnd = random.Random(w + h)
        pts = [(cx + rnd.uniform(-r * 0.9, r * 0.9), rnd.uniform(r * 0.4, r * 2.1)) for _ in range(30)]
        pts = [p for p in pts if any((p[0] - x) ** 2 + (p[1] - y) ** 2 < (rr_ - 16) ** 2 for x, y, rr_ in copa)][:9]
        for x, y in pts:
            if fruta == "maca":
                s += circ(round(x), round(y), 11, frutas_cor, 'stroke-width="2"') + circ(round(x) - 4, round(y) - 4, 2.5, C["branco"], 'stroke="none"')
            else:
                s += circ(round(x), round(y), 11, C["laranja"], 'stroke-width="2"') + ell(round(x) + 3, round(y) - 11, 4, 2, C["verde_esc"], 'stroke-width="1.2"')
    return svg(w, h, s)


P["macieira_com_macas"] = arvore_fruta(230, 500, "maca", True)
P["macieira_sem_macas"] = arvore_fruta(230, 500, "maca", False)
P["maca"] = svg(30, 32, path("M15,8 Q4,2 3,16 Q4,30 15,29 Q26,30 27,16 Q26,2 15,8 Z", "#ef4d4d", 'stroke-width="2"') +
                path("M15,8 L16,2", extra='stroke-width="2"') + folha(16, 4, 9, -20, C["verde"], 1.5) + circ(9, 13, 2.5, C["branco"], 'stroke="none"'))


def banca():
    w, h = 260, 170
    s = rr(20, 40, 12, 128, 3, C["madeira_esc"]) + rr(228, 40, 12, 128, 3, C["madeira_esc"])
    s += rr(40, 60, 180, 10, 3, C["madeira"], 'stroke-width="2.5"')                 # prateleira
    for i, t in enumerate(("cenoura", "alface", "tomate", "morango", "abobora", "girassol")):
        x = 54 + i * 29
        s += rr(x - 11, 34, 22, 26, 3, "#f6ead2", 'stroke-width="2"') + desenho_planta(t, x, 46, 0.55)
    s += rr(6, 110, 248, 58, 8, C["madeira"], 'stroke-width="3"') + rr(6, 104, 248, 14, 5, C["madeira_clara"], 'stroke-width="2.5"')
    s += coracao(130, 140, 12, C["rosa_forte"])
    # toldo listrado
    for i in range(8):
        cor = C["rosa_chiclete"] if i % 2 == 0 else C["branco"]
        x = 4 + i * 31.5
        s += path(f"M{x},4 L{x+31.5},4 L{x+31.5},26 Q{x+15.75},38 {x},26 Z", cor, 'stroke-width="2.5"')
    return svg(w, h, s)


P["banca"] = banca()
P["ferradurinha"] = svg(40, 40, path("M8,37 L5,20 A15,15 0 0 1 35,20 L32,37 L24,37 L26,21 A6,6 0 0 0 14,21 L16,37 Z", C["dourado"], 'stroke-width="2"') +
                        coracao(20, 22, 5, C["rosa_forte"], 'stroke-width="1.5"'))
P["estrelinha"] = svg(40, 40, estrela(20, 21, 17, C["amarelo"], 5, 'stroke-width="2.5"') +
                      circ(15, 20, 1.6, L, 'stroke="none"') + circ(25, 20, 1.6, L, 'stroke="none"') + path("M17,25 q3,3 6,0", extra='stroke-width="1.5"'))


def quadro_pedidos():
    w, h = 140, 160
    s = rr(60, 120, 20, 38, 3, C["madeira_esc"]) + rr(6, 6, 128, 118, 10, C["madeira"], 'stroke-width="3.5"') + rr(16, 16, 108, 98, 6, "#f3dcb4", 'stroke-width="2"')
    for (x, y, t, a) in [(22, 26, "cenoura", -4), (74, 24, "tomate", 5), (24, 70, "morango", 3), (76, 70, "alface", -5)]:
        s += f'<g transform="rotate({a} {x+21} {y+18})">' + rr(x, y, 42, 38, 2, C["branco"], 'stroke-width="2"') + desenho_planta(t, x + 21, y + 21, 0.8) + '</g>'
        s += rr(x + 16, y - 6, 10, 12, 2, C["rosa_chiclete"], 'stroke-width="1.5"')
    return svg(w, h, s)


P["quadro_pedidos"] = quadro_pedidos()
P["contador"] = svg(300, 70, rr(4, 6, 292, 58, 29, C["madeira_clara"], 'stroke-width="3.5"') + rr(12, 13, 276, 44, 22, "#fbe9cc", 'stroke-width="1.5"') +
                    path("M30,52 L27,34 A15,15 0 0 1 57,34 L54,52 L47,52 L49,35 A6,6 0 0 0 37,35 L39,52 Z", C["dourado"], 'stroke-width="2"') +
                    coracao(42, 37, 5, C["rosa_forte"], 'stroke-width="1.2"') + estrela(178, 35, 17, C["amarelo"], 5, 'stroke-width="2.2"') +
                    path("M150,12 L150,58", extra='stroke-width="2" opacity="0.4"'))

# ---------------------------------------------------------------- fase 2


def morango_canteiro(estagio):
    w, h = 160, 110
    s = ""
    oy = 60
    for x in (40, 80, 120):
        base = oy + 8
        if estagio in (0, 1):
            s += ""
        elif estagio == 2:
            s += path(f"M{x},{base} L{x},{base-14}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') + folha(x, base - 12, 12, -150) + folha(x, base - 12, 12, -30)
        else:
            big = estagio == 4
            for a in (-150, -115, -65, -30):
                s += folha(x, base - 4, 26 if big else 20, a)
            if big:
                s += desenho_planta("morango", x - 12, base - 4, 0.8) + desenho_planta("morango", x + 13, base - 8, 0.8)
    s += path(f"M10,{oy} L150,{oy} L156,{h-12} L4,{h-12} Z", TERRA_FOFA, 'stroke-width="3"')
    if estagio == 1:
        for x in (40, 80, 120):
            s += ell(x, oy + 18, 5, 3.5, "#e9d29a", 'stroke-width="2"')
    s += rr(0, h - 16, 160, 13, 4, C["madeira"], 'stroke-width="2.5"')
    if estagio == 4:
        s += estrela(140, 30, 7, C["branco"], 4, 'stroke-width="1.5"')
    return svg(w, h, s)


for e in range(0, 5):   # 0 = canteiro vazio, esperando a semente (jogo da fazendinha)
    P[f"morango_{e}"] = morango_canteiro(e)
P["morango"] = svg(22, 26, desenho_planta("morango", 11, 12, 0.85))


def abobora(w, h, gigante=False):
    cx, cy = w / 2, h * 0.58
    rx, ry = w * 0.46, h * 0.4
    s = ""
    for k in (0.95, 0.6, 0.25):
        pass
    s += ell(cx - rx * 0.45, cy, rx * 0.55, ry, C["laranja"], 'stroke-width="2.5"')
    s += ell(cx + rx * 0.45, cy, rx * 0.55, ry, C["laranja"], 'stroke-width="2.5"')
    s += ell(cx, cy, rx * 0.5, ry * 1.02, "#ffbd7a", 'stroke-width="2.5"')
    if gigante:
        s += ell(cx, cy - ry * 0.85, rx * 0.65, ry * 0.18, "#ffbd7a", 'stroke-width="2.5"')   # topo achatado
    s += rr(cx - w * 0.04, cy - ry - h * 0.14, w * 0.08, h * 0.17, 3, C["verde_esc"], 'stroke-width="2"')
    s += path(f"M{cx+w*0.03},{cy-ry-h*0.06} q{w*0.12},{-h*0.08} {w*0.2},{0}", extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
    return svg(w, h, s)


P["abobora_pequena"] = abobora(60, 50)
P["abobora_media"] = abobora(110, 90)
P["abobora_gigante"] = abobora(160, 150, True)


def covinha(broto):
    """Montinho de terra onde se planta a abóbora e o girassol (160 x 80, base embaixo)."""
    s = ell(80, 62, 74, 16, TERRA_ESC, 'stroke-width="3"') + ell(80, 56, 60, 15, TERRA_FOFA, 'stroke-width="3"')
    if broto:
        s += path("M80,54 L80,26", extra=f'stroke="{C["verde_esc"]}" stroke-width="4"') + folha(80, 30, 22, -150) + folha(80, 30, 22, -30)
    else:
        s += ell(80, 54, 9, 5, "#8a6a4a", 'stroke-width="2"')
    return svg(160, 80, s)


P["covinha"] = covinha(False)
P["covinha_broto"] = covinha(True)
P["cadeado"] = svg(50, 56, path("M14,28 L14,18 A11,11 0 0 1 36,18 L36,28", extra='stroke-width="5"') +
                   rr(6, 24, 38, 28, 7, C["dourado"], 'stroke-width="3"') + circ(25, 37, 4.5, L, 'stroke="none"'))
P["girassol_caule"] = svg(90, 360, path("M45,358 C40,260 52,160 45,40", extra='stroke-width="11"') +
                          path("M45,358 C40,260 52,160 45,40", extra=f'stroke-width="7" stroke="{C["verde_esc"]}"') +
                          folha(44, 280, 40, -160) + folha(46, 220, 40, -20) + folha(44, 150, 34, -165) + folha(46, 100, 30, -15))
P["girassol_cabeca"] = svg(90, 90, "".join(
    ell(round(45 + 30 * math.cos(2 * math.pi * i / 14), 1), round(45 + 30 * math.sin(2 * math.pi * i / 14), 1), 13, 7, C["amarelo"],
        f'stroke-width="2" transform="rotate({360 * i / 14:.0f} {45 + 30 * math.cos(2 * math.pi * i / 14):.1f} {45 + 30 * math.sin(2 * math.pi * i / 14):.1f})"')
    for i in range(14)) + circ(45, 45, 21, "#8a5a3c", 'stroke-width="2.5"') +
    circ(38, 42, 2.5, L, 'stroke="none"') + circ(52, 42, 2.5, L, 'stroke="none"') + path("M38,51 q7,6 14,0", extra='stroke-width="2.5"'))


def flor_coracao(cx, cy, r):
    s = ""
    for i in range(5):
        a = 2 * math.pi * i / 5 - math.pi / 2
        s += coracao(round(cx + r * math.cos(a), 1), round(cy + r * math.sin(a), 1), r * 0.6, C["rosa_chiclete"], 'stroke-width="1.5"')
    return s + circ(cx, cy, r * 0.5, C["amarelo"], 'stroke-width="1.5"')


def canteiro_flores(com):
    w, h = 250, 90
    s = ""
    for x in range(26, 240, 34):
        s += folha(x, 62, 22, -120) + folha(x, 62, 22, -60)
    if com:
        for i, x in enumerate(range(26, 240, 34)):
            y = 30 + (i % 2) * 10
            s += path(f"M{x},{y} L{x},62", extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
            s += [margarida(x, y, 9), tulipa(x, y, 9), flor_coracao(x, y, 8)][i % 3]
    s += path("M8,58 L242,58 L246,78 L4,78 Z", TERRA_FOFA, 'stroke-width="3"') + rr(0, 74, 250, 14, 5, C["madeira"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["canteiro_flores"] = canteiro_flores(True)
P["canteiro_colhido"] = canteiro_flores(False)
caule = lambda x, y1, y2: path(f"M{x},{y1} L{x},{y2}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"')
P["flor_margarida"] = svg(25, 55, caule(12.5, 18, 53) + folha(12.5, 38, 10, -30, C["verde"], 1.5) + margarida(12.5, 12, 7))
P["flor_tulipa"] = svg(25, 55, caule(12.5, 18, 53) + folha(12.5, 40, 10, -150, C["verde"], 1.5) + tulipa(12.5, 13, 8))
P["flor_coracao"] = svg(25, 55, caule(12.5, 18, 53) + folha(12.5, 38, 10, -30, C["verde"], 1.5) + flor_coracao(12.5, 13, 6.5))
P["buque"] = svg(50, 70, path("M25,66 L14,34 M25,66 L25,30 M25,66 L36,34", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') +
                 path("M14,44 L36,44 L28,66 L22,66 Z", C["rosa_claro"], 'stroke-width="2"') +
                 margarida(13, 22, 8) + tulipa(37, 22, 8) + flor_coracao(25, 14, 7) +
                 path("M25,50 q-12,-6 -10,4 q4,4 10,-4 q12,-6 10,4 q-4,4 -10,-4 M25,50 l-6,12 M25,50 l6,12", C["lilas"], 'stroke-width="2"'))


def abelha(aberta):
    s = ""
    if aberta:
        s += ell(11, 6, 6, 5, C["branco"], 'stroke-width="1.5" fill-opacity="0.9"') + ell(19, 6, 6, 5, C["branco"], 'stroke-width="1.5" fill-opacity="0.9"')
    else:
        s += ell(15, 6, 4, 5, C["branco"], 'stroke-width="1.5" fill-opacity="0.9"')
    s += ell(15, 15, 11, 8, C["amarelo"], 'stroke-width="2"')
    s += path("M12,8 L12,22 M18,8 L18,22", extra='stroke-width="2.5"')
    s += circ(23, 14, 1.4, L, 'stroke="none"') + circ(24, 17, 1.3, C["rosa"], 'stroke="none"')
    return svg(30, 25, s)


def borboleta(aberta):
    s = ""
    if aberta:
        s += ell(10, 11, 9, 8, C["lilas"], 'stroke-width="2"') + ell(25, 11, 9, 8, C["lilas"], 'stroke-width="2"')
        s += ell(11, 21, 6, 5, C["rosa"], 'stroke-width="2"') + ell(24, 21, 6, 5, C["rosa"], 'stroke-width="2"')
        s += circ(10, 11, 3, C["rosa_forte"], 'stroke="none"') + circ(25, 11, 3, C["rosa_forte"], 'stroke="none"')
    else:
        s += ell(15, 12, 5, 10, C["lilas"], 'stroke-width="2"') + ell(16, 20, 4, 6, C["rosa"], 'stroke-width="2"')
    s += ell(17.5, 16, 2.5, 9, L, 'stroke="none"') + path("M17,7 q-3,-5 -5,-5 M18,7 q3,-5 5,-5", extra='stroke-width="1.5"')
    return svg(35, 30, s)


P["abelha_aberta"] = abelha(True)
P["abelha_fechada"] = abelha(False)
P["borboleta_aberta"] = borboleta(True)
P["borboleta_fechada"] = borboleta(False)


def flor_arco_iris(cor, miolo):
    w, h = 150, 180
    s = path("M75,178 C70,140 80,110 75,80", extra='stroke-width="9"') + path("M75,178 C70,140 80,110 75,80", extra=f'stroke-width="5" stroke="{C["verde_esc"]}"')
    s += folha(74, 150, 36, -160) + folha(76, 128, 36, -20)
    for i in range(7):
        a = 2 * math.pi * i / 7 - math.pi / 2
        x, y = 75 + 36 * math.cos(a), 62 + 36 * math.sin(a)
        s += ell(round(x, 1), round(y, 1), 24, 17, cor, f'stroke-width="2.5" transform="rotate({math.degrees(a):.0f} {x:.1f} {y:.1f})"')
    for i, c in enumerate(["#ff6f91", "#ffa45c", "#ffe066", "#7ddc8a", "#73c2fb", "#b48cf2"]):
        s += circ(75, 62, 26 - i * 4, c, 'stroke-width="1.5"' if i == 0 else 'stroke="none"')
    s += estrela(110, 22, 8, C["branco"], 4, 'stroke-width="1.5"')
    return svg(w, h, s)


for nome, cor in (("rosa", C["rosa"]), ("lilas", C["lilas"]), ("azul", C["azul"]), ("amarela", C["amarelo"])):
    P[f"flor_arco_iris_{nome}"] = flor_arco_iris(cor, None)


def pe_frutinhas(com):
    w, h = 160, 260
    s = path("M80,258 L80,150 M80,200 L50,160 M80,190 L112,150", extra=f'stroke="{C["madeira_esc"]}" stroke-width="9"')
    blobs = [(80, 90, 60), (40, 130, 38), (120, 130, 38), (80, 150, 44), (55, 60, 34), (105, 60, 34)]
    for x, y, r in blobs:
        s += circ(x, y, r, C["rosa"], 'stroke-width="3"')
    for x, y, r in blobs:
        s += circ(x, y, r - 3, C["rosa"], 'stroke="none"')
    if com:
        for x, y in [(50, 70), (100, 50), (80, 100), (40, 130), (118, 120), (70, 150), (110, 160), (78, 40)]:
            s += estrela(x, y, 11, C["rosa_forte"], 5, 'stroke-width="2"') + circ(x - 2, y - 2, 2, C["branco"], 'stroke="none"')
    return svg(w, h, s)


P["frutinhas_magicas_com"] = pe_frutinhas(True)
P["frutinhas_magicas_sem"] = pe_frutinhas(False)


def arbusto_coracoes():
    s = rr(70, 120, 10, 28, 3, C["madeira_esc"])
    rnd = random.Random(4)
    for i in range(30):
        a, d = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 55) ** 0.95
        s += coracao(round(75 + d * math.cos(a) * 1.15, 1), round(72 + d * math.sin(a), 1), 15,
                     rnd.choice([C["verde"], C["verde_esc"], "#a6e08f"]), 'stroke-width="2"')
    return svg(150, 150, s)


P["arbusto_coracoes"] = arbusto_coracoes()
P["semente_magica"] = svg(25, 25, ell(12.5, 13, 7, 9, C["dourado"], 'stroke-width="2"') + circ(10, 10, 2, C["branco"], 'stroke="none"') +
                          estrela(20, 5, 4, C["branco"], 4, 'stroke-width="1"'))
P["laranjeira_com"] = arvore_fruta(220, 470, "laranja", True, C["verde_esc"])
P["laranjeira_sem"] = arvore_fruta(220, 470, "laranja", False, C["verde_esc"])
P["laranja"] = svg(32, 32, circ(16, 17, 13, C["laranja"], 'stroke-width="2"') + folha(16, 4, 10, -20, C["verde"], 1.5) + circ(11, 12, 2.5, C["branco"], 'stroke="none"'))


def bananeira(com):
    w, h = 230, 480
    s = path(f"M100,{h-3} C104,330 108,250 112,170 L124,170 C128,250 132,330 136,{h-3} Z", "#b9c97a", 'stroke-width="3.5"')
    for y in range(200, h, 40):
        s += path(f"M104,{y} q14,6 30,0", extra='stroke-width="1.5" opacity="0.5"')
    for a, comp in [(-150, 120), (-120, 130), (-60, 130), (-30, 120), (-90, 110), (-175, 95), (-5, 95)]:
        x2 = 118 + comp * math.cos(math.radians(a))
        y2 = 175 + comp * math.sin(math.radians(a))
        mx, my = 118 + comp * 0.5 * math.cos(math.radians(a)), 175 + comp * 0.5 * math.sin(math.radians(a))
        nx, ny = -math.sin(math.radians(a)) * 26, math.cos(math.radians(a)) * 26
        s += path(f"M118,175 Q{mx+nx:.0f},{my+ny:.0f} {x2:.0f},{y2:.0f} Q{mx-nx:.0f},{my-ny:.0f} 118,175 Z", C["verde"], 'stroke-width="3"')
        s += path(f"M118,175 L{x2:.0f},{y2:.0f}", extra='stroke-width="1.5" opacity="0.5"')
    if com:
        s += cacho_banana_svg(96, 190)
    return svg(w, h, s)


def cacho_banana_svg(x, y):
    s = path(f"M{x+30},{y} L{x+30},{y+12}", extra='stroke-width="4"')
    for i, (dx, dy) in enumerate([(4, 14), (18, 12), (32, 14), (10, 28), (26, 28)]):
        s += path(f"M{x+dx},{y+dy} q-6,14 4,24 q10,4 14,-2 q-10,-4 -8,-22 Z", C["amarelo"], 'stroke-width="2"')
    return s


P["bananeira_com"] = bananeira(True)
P["bananeira_sem"] = bananeira(False)
P["cacho_banana"] = svg(60, 50, cacho_banana_svg(0, -4).replace("M30,-4", "M30,0"))
P["banana"] = svg(50, 30, path("M4,8 Q10,26 30,26 Q44,24 47,14 Q40,18 30,18 Q14,18 8,6 Z", C["amarelo"], 'stroke-width="2"') +
                  rr(2, 4, 7, 6, 2, "#8a6a3a", 'stroke-width="1.5"'))
P["escadinha"] = svg(70, 200, path("M14,198 L26,4", extra='stroke-width="12"') + path("M14,198 L26,4", extra=f'stroke-width="7" stroke="{C["madeira_clara"]}"') +
                     path("M56,198 L44,4", extra='stroke-width="12"') + path("M56,198 L44,4", extra=f'stroke-width="7" stroke="{C["madeira_clara"]}"') +
                     "".join(rr(20 - i * 1.6 + 0, 30 + i * 36, 30 + i * 3.2, 10, 3, C["madeira"], 'stroke-width="2.5"') for i in range(5)))
P["carrinho"] = svg(190, 110, path("M150,40 L186,22", extra='stroke-width="7"') + path("M150,40 L186,22", extra=f'stroke-width="4" stroke="{C["madeira_clara"]}"') +
                    path("M8,24 L160,24 L140,72 L30,72 Z", C["madeira"], 'stroke-width="3"') + path("M14,40 L154,40 M22,56 L146,56", extra='stroke-width="1.5" opacity="0.5"') +
                    path("M120,72 L132,104", extra='stroke-width="6"') + circ(52, 84, 22, C["lilas"], 'stroke-width="3"') + circ(52, 84, 7, C["roxo"], 'stroke-width="2"'))


def nuvem_chuva(chovendo):
    w, h = 220, 90
    s = ""
    if chovendo:
        for x in range(50, 180, 22):
            s += path(f"M{x},64 q-3,8 0,12 q3,-4 0,-12 Z", C["agua"], 'stroke-width="1.5"')
            s += path(f"M{x+11},76 q-3,7 0,10 q3,-3 0,-10 Z", C["agua"], 'stroke-width="1.5"')
    nuv = [(70, 40, 30), (110, 30, 36), (150, 40, 30), (40, 50, 20), (180, 50, 20)]
    for x, y, r in nuv:
        s += circ(x, y, r, "#f4f8ff", 'stroke-width="3"')
    s += rr(32, 42, 160, 26, 13, "#f4f8ff", 'stroke-width="3"')
    for x, y, r in nuv:
        s += circ(x, y, r - 3, "#f4f8ff", 'stroke="none"')
    s += rr(35, 44, 154, 21, 10, "#f4f8ff", 'stroke="none"')
    s += circ(98, 44, 3, L, 'stroke="none"') + circ(124, 44, 3, L, 'stroke="none"') + path("M102,52 q9,8 18,0", extra='stroke-width="2.5"')
    s += circ(88, 52, 5, C["rosa"], 'stroke="none"') + circ(134, 52, 5, C["rosa"], 'stroke="none"')
    return svg(w, h, s)


P["nuvem_parada"] = nuvem_chuva(False)
P["nuvem_chovendo"] = nuvem_chuva(True)


def espantalho():
    w, h = 100, 250
    s = rr(45, 70, 10, 178, 3, C["madeira_esc"]) + rr(6, 100, 88, 9, 3, C["madeira_esc"])
    s += path("M24,96 L76,96 L82,170 L18,170 Z", "#ef7a9a", 'stroke-width="3"')
    for x in (34, 50, 66):
        s += path(f"M{x},98 L{x+2},168", extra=f'stroke="{C["branco"]}" stroke-width="3" opacity="0.8"')
    s += path("M24,120 L80,120 M22,145 L80,145", extra=f'stroke="{C["branco"]}" stroke-width="3" opacity="0.8"')
    s += path("M24,96 L76,96 L82,170 L18,170 Z", "none", 'stroke-width="3"')
    s += path("M8,98 L24,98 L24,116 L8,116 Z M92,98 L76,98 L76,116 L92,116 Z", "#ef7a9a", 'stroke-width="2.5"')
    s += path("M4,108 l-2,8 M4,108 l3,9 M96,108 l2,8 M96,108 l-3,9", extra=f'stroke="{C["amarelo"]}" stroke-width="2.5"')
    s += circ(50, 66, 25, "#f6dcb0", 'stroke-width="3"')
    s += circ(41, 64, 3, L, 'stroke="none"') + circ(59, 64, 3, L, 'stroke="none"') + path("M40,74 q10,9 20,0", extra='stroke-width="2.5"')
    s += circ(34, 72, 4.5, C["rosa"], 'stroke="none"') + circ(66, 72, 4.5, C["rosa"], 'stroke="none"')
    s += ell(50, 44, 42, 8, C["mel"], 'stroke-width="3"') + path("M30,44 Q30,14 50,14 Q70,14 70,44 Z", C["mel"], 'stroke-width="3"')
    s += rr(30, 34, 40, 7, 2, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["espantalho"] = espantalho()
P["minhoca"] = svg(40, 20, path("M4,16 Q10,4 16,14 Q22,22 28,10", extra='stroke-width="9"') +
                   path("M4,16 Q10,4 16,14 Q22,22 28,10", extra=f'stroke-width="5.5" stroke="{C["rosa_chiclete"]}"') +
                   circ(31, 9, 6, C["rosa_chiclete"], 'stroke-width="2"') + circ(32, 8, 1.3, L, 'stroke="none"') + path("M31,12 q2,1 4,-1", extra='stroke-width="1.2"'))
P["matinho"] = svg(40, 30, "".join(folha(20, 28, 18, a, C["verde"], 1.5) for a in (-160, -125, -90, -55, -20)) + flor(27, 9, 3.5, C["rosa"]))


def fundo():
    w, h, chao = 3300, 900, 600
    rnd = random.Random(21)
    defs = (f'<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ceu"]}"/>'
            f'<stop offset="1" stop-color="{C["ceu_claro"]}"/></linearGradient>')
    s = f'<rect width="{w}" height="{h}" fill="url(#ceu)" stroke="none"/>'
    s += circ(2700, 120, 60, C["amarelo"], 'stroke-width="3"')
    for cx, cy, k in [(300, 110, 40), (1100, 80, 34), (1800, 140, 44), (2300, 70, 32), (3100, 130, 38)]:
        s += nuvem(cx, cy, k)
    s += path(f"M0,{chao-50} Q500,{chao-260} 1100,{chao-90} T2200,{chao-110} T{w},{chao-180} L{w},{chao} L0,{chao} Z", C["verde_claro"])
    s += path(f"M0,{chao-10} Q700,{chao-160} 1500,{chao-30} T{w},{chao-50} L{w},{chao} L0,{chao} Z", "#a8dd8f")
    y0 = chao - 70
    s += rr(0, y0 + 14, w, 12, 4, C["branco"]) + rr(0, y0 + 42, w, 12, 4, C["branco"])
    for x in range(10, w, 52):
        s += path(f"M{x},{chao+6} L{x},{y0+6} L{x+11},{y0-6} L{x+22},{y0+6} L{x+22},{chao+6} Z", C["branco"], 'stroke-width="2.5"')
    s += rr(-5, chao, w + 10, h - chao + 5, 0, "#dcb98d")
    for _ in range(120):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(chao + 15, h - 8)
        s += ell(round(x), round(y), rnd.uniform(4, 9), 3, "#c9a376", 'stroke="none"')
    for _ in range(60):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(chao + 15, h - 10)
        s += path(f"M{x:.0f},{y:.0f} l-4,-10 M{x:.0f},{y:.0f} l0,-12 M{x:.0f},{y:.0f} l5,-10", extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
    return svg(w, h, s, defs)


P["fundo"] = fundo()

# Posição das peças na prévia e no jogo (canto de cima à esquerda, em pixels do jogo).
W, H, CHAO = 3300, 900, 600
POS = [("fundo", 0, 0), ("nuvem_chovendo", 560, 150), ("bica", 30, 570), ("regador_cheio", 170, 820), ("enxada", 270, 790),
       ("sementes_cenoura", 170, 640), ("sementes_tomate", 235, 640), ("cenoura_4", 380, 500), ("alface_3", 590, 500), ("tomate_4", 800, 460),
       ("terra_fofa", 1010, 630), ("terra_dura", 380, 740), ("morango_2", 590, 740), ("terra_fechada", 800, 740), ("terra_fechada", 1010, 740),
       ("espantalho", 1150, 390), ("carrinho", 420, 790), ("cesta_cheia", 680, 810), ("abobora_gigante", 1270, 630), ("morango_4", 1270, 790),
       ("@catarina", 1550, 860), ("girassol_caule", 1690, 280), ("girassol_cabeca", 1690, 250), ("girassol_caule", 1790, 300), ("girassol_cabeca", 1790, 270),
       ("canteiro_flores", 1890, 700), ("borboleta_aberta", 1960, 560), ("abelha_aberta", 2050, 600), ("flor_arco_iris_rosa", 2180, 640), ("frutinhas_magicas_com", 2350, 530),
       ("arbusto_coracoes", 2160, 450), ("macieira_com_macas", 2540, 140), ("laranjeira_com", 2800, 170), ("bananeira_com", 3040, 140), ("escadinha", 2740, 610),
       ("banca", 2530, 770), ("maca", 2700, 860), ("minhoca", 3000, 860), ("matinho", 3150, 850), ("quadro_pedidos", 3130, 620)]


def _c(nome, x, y, estados):
    return {"estados": estados, "x": x, "y": y}


# Como o cenário entra no protótipo (ver para_jogo.py). Os quadradinhos de terra, as ferramentas e as
# sementes são do jogo da fazendinha (prototipo/scripts/fazendinha.gd + dados/fazendinha.json): por isso
# saem da lista de peças ("omitir") e as imagens de todos os estágios vão junto ("tambem").
JOGO = {
    "interativos": {
        "nuvem": _c("nuvem", 560, 150, ["nuvem_parada", "nuvem_chovendo"]),
        "cesta": _c("cesta", 680, 810, ["cesta_vazia", "cesta_cheia"]),
        "canteiro_flores": _c("canteiro_flores", 1890, 700, ["canteiro_colhido", "canteiro_flores"]),
        "borboleta": _c("borboleta", 1960, 560, ["borboleta_fechada", "borboleta_aberta"]),
        "abelha": _c("abelha", 2050, 600, ["abelha_fechada", "abelha_aberta"]),
        "flor_arco_iris": _c("flor_arco_iris", 2180, 640, ["flor_arco_iris_rosa", "flor_arco_iris_lilas", "flor_arco_iris_azul", "flor_arco_iris_amarela"]),
        "frutinhas_magicas": _c("frutinhas_magicas", 2350, 530, ["frutinhas_magicas_sem", "frutinhas_magicas_com"]),
        "macieira": _c("macieira", 2540, 140, ["macieira_sem_macas", "macieira_com_macas"]),
        "laranjeira": _c("laranjeira", 2800, 170, ["laranjeira_sem", "laranjeira_com"]),
        "bananeira": _c("bananeira", 3040, 140, ["bananeira_sem", "bananeira_com"]),
        "seta_sede": {"estados": ["seta_casa_e"], "x": 1430, "y": 440, "leva": "sede", "chegada": 1490},
        "seta_estabulo": {"estados": ["seta_ferradura_d"], "x": 1560, "y": 440, "leva": "estabulo", "chegada": 1620},
    },
    "extras": [("seta_casa_e", 1430, 440), ("seta_ferradura_d", 1560, 440)],
    "omitir": ["cenoura_4", "alface_3", "tomate_4", "terra_fofa", "terra_dura", "terra_fechada",
                "sementes_cenoura", "sementes_tomate", "regador_cheio", "enxada",
                "morango_2", "morango_4", "abobora_gigante", "girassol_caule", "girassol_cabeca"],
    "tambem": ["terra_dura", "terra_fofa", "terra_fechada", "regador_vazio", "regador_cheio", "enxada",
               "sementes_cenoura", "sementes_alface", "sementes_tomate",
               "cenoura_1", "cenoura_2", "cenoura_3", "cenoura_4", "alface_1", "alface_2", "alface_3", "alface_4",
               "tomate_1", "tomate_2", "tomate_3", "tomate_4",
               "colheita_cenoura", "colheita_alface", "colheita_tomate", "morango", "maca", "laranja", "banana",
               "ferradurinha", "estrelinha", "contador",
               "sementes_morango", "sementes_abobora", "sementes_girassol",
               "morango_0", "morango_1", "morango_2", "morango_3", "morango_4",
               "covinha", "covinha_broto", "cadeado", "abobora_pequena", "abobora_media", "abobora_gigante",
               "girassol_caule", "girassol_cabeca", "flor_margarida", "flor_tulipa", "flor_coracao"],
    "objetos": ["maca"],
    "lugares": [],
    "superficies": [],
}

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario/plantacao/2d")
    salvar(P, os.path.join(destino, "svg"), destino)
    print(len(P), "peças em", destino)
