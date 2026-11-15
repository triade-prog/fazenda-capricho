"""Plantas novas da fazendinha (níveis 7 e 10): milho e melancia, em 2D provisório.

Mesmo estilo e mesmas medidas das plantas da Plantação (plantacao.py): quadradinho de 200 px de
largura, estágios 1 a 4, pacotinho de sementes 60 x 80 e a colheita solta. Quando a arte 3D chegar,
é só trocar os PNGs (mesmos nomes e proporções).
Uso: python3 ferramentas/cenario2d/plantas_novas.py
Saída: arte/cenario/plantacao/2d/ e prototipo/assets/cenario/plantacao/
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, estrela, salvar  # noqa: E402
from plantacao import quadradinho, folha, TERRA  # noqa: E402

AMARELO_MILHO = "#ffd34d"
VERDE_MELANCIA = "#4fae5a"
P = {}


def espiga(x, y, k=1.0):
    """Espiga de milho em pé, com a base em (x, y)."""
    s = path(f"M{x-9*k},{y} Q{x-12*k},{y-26*k} {x},{y-40*k} Q{x+12*k},{y-26*k} {x+9*k},{y} Z", AMARELO_MILHO, 'stroke-width="2"')
    for yy in (y - 10 * k, y - 20 * k, y - 30 * k):
        s += path(f"M{x-7*k},{yy} L{x+7*k},{yy}", extra='stroke-width="1.2" opacity="0.5"')
    s += folha(x, y, 30 * k, -120, C["verde"], 2) + folha(x, y, 30 * k, -60, C["verde"], 2)
    return s


def melancia(cx, cy, r):
    s = ell(cx, cy, r, r * 0.78, VERDE_MELANCIA, 'stroke-width="2.5"')
    for dx in (-0.55, 0.0, 0.55):
        s += path(f"M{cx + dx * r},{cy - r * 0.72} Q{cx + dx * r * 1.3},{cy} {cx + dx * r},{cy + r * 0.72}",
                  extra=f'stroke="{C["verde_esc"]}" stroke-width="{max(2, r / 7):.1f}"')
    return s + ell(cx - r * 0.35, cy - r * 0.35, r * 0.18, r * 0.1, C["branco"], 'stroke="none" opacity="0.6"')


def milho_no_quadradinho(estagio, h=260):
    oy = h - 70
    base = oy + 24
    s = quadradinho("fofa", oy)
    for x in (55, 100, 145):
        if estagio == 1:
            s += ell(x, base + 4, 6, 4, AMARELO_MILHO, 'stroke-width="2"')
        elif estagio == 2:
            s += path(f"M{x},{base+6} L{x},{base-22}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"')
            s += folha(x, base - 18, 18, -150) + folha(x, base - 12, 18, -30)
        else:
            grande = estagio == 4
            top = 170 if grande else 110
            s += path(f"M{x},{base+4} L{x},{base-top}", extra=f'stroke="{C["verde_esc"]}" stroke-width="5"')
            for i, yy in enumerate(range(int(base - 20), int(base - top), -30)):
                s += folha(x, yy, 34, -165 if i % 2 else -15, C["verde"])
            s += path(f"M{x},{base-top} l-6,-14 M{x},{base-top} l6,-14 M{x},{base-top} l0,-16", extra=f'stroke="{C["mel"]}" stroke-width="3"')
            if grande:
                s += espiga(x + 14, base - 60, 0.9)
                s += estrela(x + 22, base - 120, 7, C["branco"], 4, 'stroke-width="1.5"')
    return svg(200, h, s)


def melancia_no_quadradinho(estagio, h=200):
    oy = h - 70
    base = oy + 24
    s = quadradinho("fofa", oy)
    if estagio == 1:
        for x in (55, 100, 145):
            s += ell(x, base + 4, 6, 4, "#3b3b3b", 'stroke-width="1.5"')
    elif estagio == 2:
        for x in (55, 100, 145):
            s += path(f"M{x},{base+6} L{x},{base-12}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"')
            s += folha(x, base - 10, 16, -150) + folha(x, base - 10, 16, -30)
    else:
        # rama rasteira com folhas e flores amarelas
        s += path(f"M20,{base} C60,{base-30} 140,{base+10} 182,{base-16}", extra=f'stroke="{C["verde_esc"]}" stroke-width="4"')
        for x in (36, 72, 108, 150, 176):
            s += folha(x, base - 6, 24, -120 if x % 2 else -60, C["verde"])
        if estagio == 3:
            for x in (60, 130):
                s += circ(x, base - 18, 6, C["amarelo"], 'stroke-width="1.5"') + melancia(x + 16, base + 2, 11)
        else:
            s += melancia(70, base - 10, 34) + melancia(140, base - 4, 26)
            s += estrela(170, base - 50, 7, C["branco"], 4, 'stroke-width="1.5"')
    return svg(200, h, s)


def pacote(desenho):
    s = path("M6,10 L54,10 L54,76 L6,76 Z", "#f6ead2", 'stroke-width="2.5"')
    s += path("M6,10 L12,4 L18,10 L24,4 L30,10 L36,4 L42,10 L48,4 L54,10", extra='stroke-width="2"')
    s += rr(12, 20, 36, 40, 6, C["branco"], 'stroke-width="2"') + desenho
    s += ell(30, 68, 4, 2.5, TERRA, 'stroke-width="1.5"')
    return svg(60, 80, s)


for e in range(1, 5):
    P[f"milho_{e}"] = milho_no_quadradinho(e)
    P[f"melancia_{e}"] = melancia_no_quadradinho(e)
P["sementes_milho"] = pacote(espiga(30, 56, 0.8))
P["sementes_melancia"] = pacote(melancia(30, 40, 14))
P["colheita_milho"] = svg(30, 60, espiga(15, 56, 1.05))
P["colheita_melancia"] = svg(70, 55, melancia(35, 29, 30))

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario/plantacao/2d")
    jogo = os.path.join(raiz, "prototipo/assets/cenario/plantacao")
    tmp = os.path.join(destino, "_novas")
    salvar(P, os.path.join(tmp, "svg"), tmp)
    for nome in P:
        shutil.copyfile(os.path.join(tmp, nome + ".png"), os.path.join(destino, nome + ".png"))
        shutil.copyfile(os.path.join(tmp, nome + ".png"), os.path.join(jogo, nome + ".png"))
    shutil.rmtree(tmp)
    print(len(P), "peças em", destino, "e", jogo)
