"""Base comum para desenhar as peças 2D provisórias dos cenários (SVG -> PNG).

Estilo igual às peças provisórias do quarto: desenho chapado, contorno marrom-arroxeado,
cores pastel. Tudo em pixels do jogo; o PNG sai em 2x (ou 4x nas peças pequenas).
"""
import math
import os
import subprocess

L = "#5b3a4f"          # contorno
SW = 3                 # espessura do contorno

C = dict(
    rosa="#ffb6d5", rosa_claro="#ffd6e8", rosa_forte="#ff6fae", rosa_chiclete="#ff8cc6",
    lilas="#d4b8f5", lilas_claro="#ece0ff", roxo="#a874e0", roxo_esc="#7d4fc0",
    madeira="#e6b47e", madeira_esc="#c98c56", madeira_clara="#f3d3a8", mel="#e9a95c",
    creme="#fff3dc", branco="#ffffff", verde="#93d47c", verde_esc="#6dbb5c",
    verde_claro="#bfe8a6", ceu="#bfe3fb", ceu_claro="#e6f5ff", amarelo="#ffd75e",
    azul="#8fc9f5", laranja="#ffb067", vermelho_rosa="#ef6f8c", dourado="#f2c14e",
    cinza="#d9d2dc", agua="#aee0fa",
)


def svg(w, h, corpo, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>'
            f'<g stroke="{L}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{corpo}</g></svg>')


def rr(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'


def circ(cx, cy, r, fill, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {extra}/>'


def ell(cx, cy, rx, ry, fill, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def coracao(cx, cy, s, fill, extra=""):
    """Coração com largura ~2s, centrado em (cx, cy)."""
    d = (f"M{cx},{cy + s * 0.9} C{cx - s * 1.2},{cy + s * 0.1} {cx - s * 1.05},{cy - s * 0.95} {cx},{cy - s * 0.35} "
         f"C{cx + s * 1.05},{cy - s * 0.95} {cx + s * 1.2},{cy + s * 0.1} {cx},{cy + s * 0.9} Z")
    return path(d, fill, extra)


def estrela(cx, cy, r, fill, pontas=4, extra=""):
    pts = []
    for i in range(pontas * 2):
        a = math.pi * i / pontas - math.pi / 2
        rad = r if i % 2 == 0 else r * 0.38
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" {extra}/>'


def flor(cx, cy, r, petala, miolo=None, n=5):
    miolo = miolo or C["amarelo"]
    s = ""
    for i in range(n):
        a = 2 * math.pi * i / n
        s += circ(f"{cx + r * math.cos(a):.1f}", f"{cy + r * math.sin(a):.1f}", r * 0.75, petala,
                  'stroke-width="2"')
    return s + circ(cx, cy, r * 0.55, miolo, 'stroke-width="2"')


def nuvem(cx, cy, s):
    return (f'<g stroke="none" fill="#ffffff" opacity="0.95">'
            + circ(cx - s, cy, s * 0.7, "#fff") + circ(cx, cy - s * 0.35, s, "#fff")
            + circ(cx + s, cy, s * 0.75, "#fff") + rr(cx - s * 1.6, cy, s * 3.3, s * 0.65, s * 0.3, "#fff")
            + '</g>')


def salvar(pecas, pasta_svg, pasta_png):
    """pecas: dict nome -> svg. Grava os SVGs e gera os PNGs."""
    os.makedirs(pasta_svg, exist_ok=True)
    for nome, s in pecas.items():
        with open(os.path.join(pasta_svg, nome + ".svg"), "w", encoding="utf-8") as f:
            f.write(s)
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["node", os.path.join(raiz, "svg_para_png.js"), pasta_svg, pasta_png], check=True)
