"""Põe o selo 3D da ferradura (arte/objetos3d/avulsas/selo_ferradura.png) onde a Carol pediu (15/11/2026):

- placas de ida para o Estábulo (seta_ferradura_d / _e): a placa 3D de madeira com o selo pregado no lugar do desenho;
- ícone do Estábulo no mapa: o selo no lugar do coração redondo do telhado.
Uso: python3 ferramentas/cenario2d/selo_ferradura_3d.py   (depois: para_jogo.py nos cenários e mapa_fazenda.py)
"""
import os

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SELO = Image.open(os.path.join(RAIZ, "arte/objetos3d/avulsas/selo_ferradura.png")).convert("RGBA")


def selo(d):
    k = d / max(SELO.size)
    return SELO.resize((round(SELO.width * k), round(SELO.height * k)), Image.LANCZOS)


def enche(pasta, nomes):
    arq = os.path.join(pasta, "_enche.txt")
    atual = open(arq, encoding="utf-8").read().split() if os.path.exists(arq) else []
    with open(arq, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(set(atual) | set(nomes))) + "\n")


def placas():
    pasta = os.path.join(RAIZ, "arte/cenario/placas/novo3d")
    base = Image.open(os.path.join(pasta, "seta_cesta_d.png")).convert("RGBA")
    cx, cy, d = 222, 338, 330          # onde fica o cesto na placa da cesta
    s = selo(d)
    for lado in ("d", "e"):
        im = base if lado == "d" else ImageOps.mirror(base)
        x = cx if lado == "d" else im.width - cx
        im = im.copy()
        im.alpha_composite(s, (round(x - s.width / 2), round(cy - s.height / 2)))
        im.save(os.path.join(pasta, f"seta_ferradura_{lado}.png"))
    enche(pasta, ["seta_ferradura_d", "seta_ferradura_e"])


def mapa():
    pasta = os.path.join(RAIZ, "arte/interface/mapa_fazenda/novo3d")
    im = Image.open(os.path.join(RAIZ, "arte/interface/mapa_fazenda/2d/estabulo.png")).convert("RGBA")
    k = im.width / 540                 # o 2D sai em 2x
    s = selo(round(66 * k))
    im.alpha_composite(s, (round(270 * k - s.width / 2), round(64 * k - s.height / 2)))
    im.save(os.path.join(pasta, "estabulo.png"))
    enche(pasta, ["estabulo"])


if __name__ == "__main__":
    placas()
    mapa()
