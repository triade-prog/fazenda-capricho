"""Plaquinhas de caminho (setas com desenho, sem letras) que ligam os cenários de fora.

Cada desenho existe apontando para a direita (_d) e para a esquerda (_e): seta_<desenho>_<d|e>.png,
120 × 160 px, em arte/cenario/placas/2d/. O para_jogo.py busca aqui as peças que o cenário não tem.
Uso: python3 ferramentas/cenario2d/placas.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, svg, rr, circ, ell, path, coracao, salvar  # noqa: E402

PASTA = "placas"
P = {}


def _desenho(d, cx, cy):
    if d == "casa":
        return (path(f"M{cx-13},{cy+14} L{cx-13},{cy} L{cx},{cy-12} L{cx+13},{cy} L{cx+13},{cy+14} Z", C["rosa"], 'stroke-width="2.5"') +
                rr(cx - 4, cy + 4, 8, 10, 1, C["roxo"], 'stroke-width="2"'))
    if d == "cabana":
        return (path(f"M{cx-18},{cy+14} L{cx},{cy-16} L{cx+18},{cy+14} Z", C["verde"], 'stroke-width="2.5"') +
                path(f"M{cx},{cy-16} L{cx},{cy+14} M{cx-6},{cy+14} L{cx},{cy+2} L{cx+6},{cy+14}", extra='stroke-width="2"'))
    if d == "arvore":
        return (rr(cx - 4, cy + 2, 8, 14, 2, C["madeira_esc"], 'stroke-width="2"') +
                circ(cx - 8, cy - 2, 9, C["rosa_chiclete"], 'stroke-width="2.2"') + circ(cx + 8, cy - 2, 9, C["rosa_chiclete"], 'stroke-width="2.2"') +
                circ(cx, cy - 9, 10, C["rosa_chiclete"], 'stroke-width="2.2"') + circ(cx, cy - 3, 7, C["rosa_chiclete"], 'stroke="none"'))
    if d == "ferradura":
        return (path(f"M{cx-12},{cy+14} L{cx-14},{cy} A14,14 0 0 1 {cx+14},{cy} L{cx+12},{cy+14} L{cx+5},{cy+14} "
                     f"L{cx+6},{cy} A6,6 0 0 0 {cx-6},{cy} L{cx-5},{cy+14} Z", C["dourado"], 'stroke-width="2"') +
                coracao(cx, cy + 1, 4, C["rosa_forte"], 'stroke-width="1.2"'))
    if d == "cenoura":
        return (path(f"M{cx-2},{cy-8} L{cx-8},{cy-17} M{cx},{cy-8} L{cx},{cy-19} M{cx+2},{cy-8} L{cx+8},{cy-17}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3.5"') +
                path(f"M{cx-9},{cy-8} L{cx+9},{cy-8} L{cx+1},{cy+16} L{cx-1},{cy+16} Z", C["laranja"], 'stroke-width="2.2"'))
    if d == "pata":
        s = ell(cx, cy + 6, 10, 8, C["rosa_forte"], 'stroke-width="2"')
        for dx, dy in [(-12, -4), (-5, -11), (5, -11), (12, -4)]:
            s += circ(cx + dx, cy + dy, 4, C["rosa_forte"], 'stroke-width="1.5"')
        return s
    if d == "portao":
        return (path(f"M{cx-16},{cy+14} L{cx-16},{cy-6} Q{cx},{cy-20} {cx+16},{cy-6} L{cx+16},{cy+14}", extra='stroke-width="5"') +
                path(f"M{cx-16},{cy+14} L{cx-16},{cy-6} Q{cx},{cy-20} {cx+16},{cy-6} L{cx+16},{cy+14}", extra=f'stroke="{C["madeira_clara"]}" stroke-width="2.5"') +
                rr(cx - 11, cy - 1, 22, 15, 2, C["madeira_clara"], 'stroke-width="2"') + coracao(cx, cy + 6, 4, C["rosa_forte"], 'stroke-width="1.2"'))
    if d == "cesta":
        return (path(f"M{cx-11},{cy} Q{cx},{cy-22} {cx+11},{cy}", extra='stroke-width="3"') +
                path(f"M{cx-15},{cy} L{cx+15},{cy} L{cx+11},{cy+15} L{cx-11},{cy+15} Z", C["madeira_clara"], 'stroke-width="2.2"') +
                circ(cx - 5, cy - 1, 4.5, C["rosa_forte"], 'stroke-width="1.5"') + circ(cx + 5, cy - 1, 4.5, C["amarelo"], 'stroke-width="1.5"'))
    raise ValueError(d)


def placa(desenho, esquerda):
    tabua = (path("M8,14 L96,14 L114,46 L96,78 L8,78 Z", C["madeira"], 'stroke-width="3.5"') +
             path("M66,46 L88,46 M80,38 L90,46 L80,54", extra='stroke-width="4"'))
    s = rr(52, 50, 16, 108, 4, C["madeira_esc"])
    if esquerda:
        s += f'<g transform="translate(120,0) scale(-1,1)">{tabua}</g>' + _desenho(desenho, 84, 45)
    else:
        s += tabua + _desenho(desenho, 36, 45)
    return svg(120, 160, s)


for _d in ["casa", "cabana", "arvore", "ferradura", "cenoura", "pata", "portao", "cesta"]:
    P[f"seta_{_d}_d"] = placa(_d, False)
    P[f"seta_{_d}_e"] = placa(_d, True)

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario/placas/2d")
    salvar(P, os.path.join(destino, "svg"), destino)
    print(len(P), "plaquinhas em", destino)
