"""Peças que se repetem em vários cenários (portas, plantas, janelas, parede)."""
import math
import random
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, nuvem


def porta_casa(aberta, cor=None, w=170, h=350, luz="#ffe3a8"):
    """Porta de madeira arredondada no alto (como a do quarto)."""
    cor = cor or C["madeira"]
    r = w / 2 - 6
    s = path(f"M2,{h-2} L2,{r+6} A{r+4},{r+4} 0 0 1 {w-2},{r+6} L{w-2},{h-2} Z", C["madeira_esc"], 'stroke-width="4"')
    vao = f"M14,{h-2} L14,{r+8} A{r-8},{r-8} 0 0 1 {w-14},{r+8} L{w-14},{h-2} Z"
    if not aberta:
        s += path(vao, cor)
        s += rr(32, r + 30, w - 64, 90, 8, "none", 'stroke-width="2.5" opacity="0.6"')
        s += rr(32, r + 140, w - 64, 110, 8, "none", 'stroke-width="2.5" opacity="0.6"')
        s += circ(w - 34, h * 0.55, 8, C["dourado"])
    else:
        s += path(vao, luz)
        s += path(f"M14,{h-2} L14,{r+8} Q16,{r-10} 44,{r-26} L44,{h-14} Z", cor, 'stroke-width="3"')
        s += rr(14, h - 40, w - 28, 38, 0, "#f3c98f", 'stroke="none" opacity="0.6"')
        s += path(vao, "none")
    return svg(w, h, s)


def plaquinha(desenho, w=70, h=60):
    s = path(f"M{w/2-12},4 L{w/2},0 L{w/2+12},4", extra='stroke-width="2"')
    s += rr(3, 6, w - 6, h - 9, 12, C["madeira_clara"], 'stroke-width="3"')
    cx, cy = w / 2, h / 2 + 3
    if desenho == "coracao":
        s += coracao(cx, cy, 13, C["rosa_forte"])
    elif desenho == "flor":
        s += flor(cx, cy, 8, C["lilas"], C["rosa_forte"])
    elif desenho == "panela":
        s += path(f"M{cx-15},{cy-6} L{cx+15},{cy-6} L{cx+12},{cy+12} L{cx-12},{cy+12} Z", C["rosa_chiclete"], 'stroke-width="2.5"')
        s += path(f"M{cx+15},{cy-3} l9,-3 M{cx-15},{cy-3} l-9,-3", extra='stroke-width="3"')
        s += path(f"M{cx-6},{cy-12} q2,-5 0,-8 M{cx+4},{cy-12} q2,-5 0,-8", extra='stroke-width="2"')
    elif desenho == "casa":
        s += path(f"M{cx-15},{cy+12} L{cx-15},{cy-2} L{cx},{cy-15} L{cx+15},{cy-2} L{cx+15},{cy+12} Z", C["rosa"], 'stroke-width="2.5"')
        s += rr(cx - 4, cy + 1, 8, 11, 1, C["roxo"], 'stroke-width="2"')
    elif desenho == "ferradura":
        s += path(f"M{cx-12},{cy+13} L{cx-14},{cy} A14,14 0 0 1 {cx+14},{cy} L{cx+12},{cy+13} L{cx+5},{cy+13} "
                  f"L{cx+6},{cy} A6,6 0 0 0 {cx-6},{cy} L{cx-5},{cy+13} Z", C["dourado"], 'stroke-width="2"')
        s += coracao(cx, cy + 1, 5, C["rosa_forte"], 'stroke-width="1.5"')
    elif desenho == "pata":
        s += ell(cx, cy + 5, 9, 7, C["rosa_forte"], 'stroke-width="2"')
        for dx, dy in [(-11, -5), (-4, -11), (4, -11), (11, -5)]:
            s += circ(cx + dx, cy + dy, 3.5, C["rosa_forte"], 'stroke-width="1.5"')
    return svg(w, h, s)


def planta_vaso(w=60, h=80, vaso=None, flores=None):
    vaso = vaso or C["rosa_chiclete"]
    s = ""
    for a in (-150, -120, -90, -60, -30):
        x2, y2 = w / 2 + (h * 0.45) * math.cos(math.radians(a)), h * 0.55 + (h * 0.45) * math.sin(math.radians(a))
        s += ell((w / 2 + x2) / 2, (h * 0.55 + y2) / 2, h * 0.24, h * 0.08, C["verde"],
                 f'stroke-width="2" transform="rotate({a} {(w/2 + x2)/2:.1f} {(h*0.55 + y2)/2:.1f})"')
    if flores:
        for x, y in [(w * 0.3, h * 0.25), (w * 0.7, h * 0.22), (w * 0.5, h * 0.12)]:
            s += flor(round(x, 1), round(y, 1), w * 0.08, flores)
    s += path(f"M{w*0.18},{h*0.55} L{w*0.82},{h*0.55} L{w*0.72},{h-2} L{w*0.28},{h-2} Z", vaso, 'stroke-width="2.5"')
    s += rr(w * 0.14, h * 0.52, w * 0.72, h * 0.09, 3, vaso, 'stroke-width="2.5"')
    return svg(w, h, s)


def planta_pendurada(cx, y0, comp=150, cor_vaso=None):
    cor_vaso = cor_vaso or C["madeira"]
    s = path(f"M{cx},{y0} L{cx-22},{y0+60} M{cx},{y0} L{cx+22},{y0+60}", extra='stroke-width="2"')
    for i in range(5):
        x = cx - 30 + i * 15
        yy = y0 + 70
        for k in range(4):
            s += ell(x + (k % 2) * 6 - 3, yy + 10 + k * (comp - 70) / 4, 9, 5, C["verde"], 'stroke-width="1.8"')
    s += path(f"M{cx-34},{y0+56} L{cx+34},{y0+56} L{cx+26},{y0+84} L{cx-26},{y0+84} Z", cor_vaso, 'stroke-width="2.5"')
    return s


def janela_paisagem(x, y, w, h, cortina=None):
    cortina = cortina or C["roxo"]
    s = rr(x - 10, y - 10, w + 20, h + 20, 6, C["madeira"], 'stroke-width="4"')
    s += rr(x, y, w, h, 2, C["ceu"])
    s += f'<clipPath id="j{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#j{x}{y})">'
    s += path(f"M{x},{y+h*0.7} Q{x+w*0.3},{y+h*0.45} {x+w*0.6},{y+h*0.68} T{x+w},{y+h*0.6} L{x+w},{y+h} L{x},{y+h} Z", C["verde"], 'stroke-width="2.5"')
    s += circ(x + w * 0.78, y + h * 0.25, h * 0.11, C["amarelo"], 'stroke-width="2"')
    s += circ(x + w * 0.25, y + h * 0.5, h * 0.12, C["rosa_chiclete"], 'stroke-width="2"') + rr(x + w * 0.25 - 3, y + h * 0.6, 6, h * 0.14, 2, C["madeira_esc"], 'stroke-width="1.5"')
    s += '</g>'
    s += path(f"M{x+w/2},{y} L{x+w/2},{y+h} M{x},{y+h/2} L{x+w},{y+h/2}", extra='stroke-width="6"')
    s += path(f"M{x+w/2},{y} L{x+w/2},{y+h} M{x},{y+h/2} L{x+w},{y+h/2}", extra=f'stroke-width="3" stroke="{C["madeira"]}"')
    s += path(f"M{x-14},{y-14} L{x+w*0.22},{y-14} Q{x+w*0.08},{y+h*0.5} {x+w*0.18},{y+h+12} L{x-14},{y+h+12} Z", cortina, 'stroke-width="3"')
    s += path(f"M{x+w+14},{y-14} L{x+w*0.78},{y-14} Q{x+w*0.92},{y+h*0.5} {x+w*0.82},{y+h+12} L{x+w+14},{y+h+12} Z", cortina, 'stroke-width="3"')
    s += rr(x - 24, y - 22, w + 48, 12, 5, C["madeira_esc"], 'stroke-width="2.5"')
    return s


def parede_interna(w, h, chao, cor_a, cor_b, piso="#e7bb87", listras=True, vigas=True):
    s = rr(-5, -5, w + 10, chao + 10, 0, cor_a, 'stroke="none"')
    if listras:
        for x in range(0, w, 80):
            s += rr(x, 0, 40, chao, 0, cor_b, 'stroke="none"')
    if vigas:
        s += rr(-5, -5, w + 10, 46, 0, C["madeira"], 'stroke-width="3"')
        for x in range(40, w, 340):
            s += rr(x, 30, 26, 26, 4, C["madeira_esc"], 'stroke-width="2.5"')
    s += rr(-5, chao - 22, w + 10, 24, 0, C["madeira_esc"], 'stroke-width="3"')
    s += rr(-5, chao, w + 10, h - chao + 5, 0, piso, 'stroke-width="3"')
    for y in range(chao + 45, h, 55):
        s += path(f"M0,{y} L{w},{y}", extra='stroke-width="1.5" opacity="0.3"')
    for i, y in enumerate(range(chao, h, 55)):
        for x in range(90 + (i % 2) * 170, w, 340):
            s += path(f"M{x},{y} L{x},{y+55}", extra='stroke-width="1.5" opacity="0.25"')
    return s


def grama_fundo(w, h, chao, rnd, cor="#8fd17a", n_flores=60, x0=0):
    s = rr(x0 - 5, chao, w - x0 + 10, h - chao + 5, 0, cor)
    for _ in range(int((w - x0) / 20)):
        x, y = rnd.uniform(x0 + 10, w - 10), rnd.uniform(chao + 20, h - 10)
        s += path(f"M{x:.0f},{y:.0f} l-5,-12 M{x:.0f},{y:.0f} l0,-15 M{x:.0f},{y:.0f} l6,-12", extra=f'stroke="{C["verde_esc"]}" stroke-width="2.5"')
    for _ in range(n_flores):
        x, y = rnd.uniform(x0 + 15, w - 15), rnd.uniform(chao + 25, h - 15)
        s += flor(round(x), round(y), 5, rnd.choice([C["rosa"], C["branco"], C["lilas"], C["amarelo"]]))
    return s


def ceu_morros(w, h, chao, rnd, nuvens=5):
    defs = (f'<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["ceu"]}"/>'
            f'<stop offset="1" stop-color="{C["ceu_claro"]}"/></linearGradient>')
    s = f'<rect width="{w}" height="{h}" fill="url(#ceu)" stroke="none"/>'
    for i in range(nuvens):
        s += nuvem(round(w * (i + 0.5) / nuvens + rnd.uniform(-80, 80)), round(rnd.uniform(60, 170)), round(rnd.uniform(28, 46)))
    s += path(f"M0,{chao-60} Q{w*0.15},{chao-250} {w*0.33},{chao-90} T{w*0.66},{chao-110} T{w},{chao-170} L{w},{chao} L0,{chao} Z", C["verde_claro"])
    s += path(f"M0,{chao-10} Q{w*0.25},{chao-150} {w*0.5},{chao-30} T{w},{chao-50} L{w},{chao} L0,{chao} Z", "#a8dd8f")
    return s, defs


def cerca(w, chao, x0=0, x1=None):
    x1 = x1 if x1 is not None else w
    y0 = chao - 70
    s = rr(x0, y0 + 14, x1 - x0, 12, 4, C["branco"]) + rr(x0, y0 + 42, x1 - x0, 12, 4, C["branco"])
    for x in range(x0 + 10, x1 - 10, 52):
        s += path(f"M{x},{chao+6} L{x},{y0+6} L{x+11},{y0-6} L{x+22},{y0+6} L{x+22},{chao+6} Z", C["branco"], 'stroke-width="2.5"')
    return s


def arvore_simples(w, h, copa=None, flores=None, seed=1):
    copa_cor = copa or C["verde"]
    cx = w / 2
    s = path(f"M{cx-w*0.09},{h*0.5} C{cx-w*0.08},{h-50} {cx-w*0.14},{h-12} {cx-w*0.2},{h-3} L{cx+w*0.2},{h-3} "
             f"C{cx+w*0.14},{h-12} {cx+w*0.08},{h-50} {cx+w*0.09},{h*0.5} Z", C["madeira_esc"], 'stroke-width="3.5"')
    r = w * 0.3
    bl = [(cx, r + 4, r), (cx - r * 0.9, r * 1.5, r * 0.75), (cx + r * 0.9, r * 1.5, r * 0.75), (cx, r * 1.8, r * 0.8)]
    for x, y, rr_ in bl:
        s += circ(round(x, 1), round(y, 1), round(rr_, 1), copa_cor, 'stroke-width="3.5"')
    for x, y, rr_ in bl:
        s += circ(round(x, 1), round(y, 1), round(rr_ - 3.5, 1), copa_cor, 'stroke="none"')
    if flores:
        rnd = random.Random(seed)
        for _ in range(int(w / 12)):
            x, y = cx + rnd.uniform(-r * 1.4, r * 1.4), rnd.uniform(r * 0.4, r * 2.3)
            if any((x - a) ** 2 + (y - b) ** 2 < (c - 12) ** 2 for a, b, c in bl):
                s += flor(round(x), round(y), max(5, w * 0.018), flores, C["rosa_forte"])
    return s
