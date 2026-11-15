"""Monta, a partir das peças 3D que a Carol mandou (arte/cenario/casa_arvore/novo3d/), as que o jogo
precisa e que vêm de mais de uma peça ou de um estado que não veio pronto.

Uso: python3 ferramentas/cenario2d/casa_arvore_3d.py   (depois: para_jogo.py casa_arvore)
- porta_aberta: a porta 3D com o vão escuro no lugar da folha;
- cacho_colhido: as folhinhas na mesma tela do cacho_com (para não pular ao colher);
- cesto_cheio: o cesto 3D com as bolinhas rosa dentro;
- balanco_assento: as duas cordas e a prancha numa peça só (é ela que balança);
- fundo_patio: o céu, os morros e as nuvens 3D.
As peças originais limpas estão em novo3d/ (ferramentas/limpar_3d.py); as que a Carol mandou, sem
mexer, em arte/objetos3d/casa_arvore_originais/.
"""
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = os.path.join(RAIZ, "arte/cenario/casa_arvore/novo3d")
ORIG = os.path.join(RAIZ, "arte/objetos3d/casa_arvore_originais")


def abre(nome, pasta=N):
    return Image.open(os.path.join(pasta, nome + ".png")).convert("RGBA")


def porta_aberta():
    im = abre("porta_fechada")
    a = np.array(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    moldura = (al > 0) & (r > 150) & (g > 90) & (b < 120) & (r > b + 80)   # madeira laranja
    dentro = ndimage.binary_fill_holes(moldura) & ~moldura
    dentro = ndimage.binary_opening(dentro, iterations=3)
    dentro = ndimage.binary_fill_holes(dentro)
    h = a.shape[0]
    t = np.linspace(0, 1, h)[:, None]
    cor = np.stack([110 + 40 * t, 62 + 28 * t, 48 + 18 * t], -1) * np.ones((1, a.shape[1], 1))
    a[..., :3][dentro] = cor[dentro].astype(int)
    a[..., 3][dentro] = 255
    out = Image.fromarray(a.astype(np.uint8))
    # luzinha amarela lá dentro
    ys, xs = np.where(dentro)
    cx, cy = xs.mean(), ys.min() + (ys.max() - ys.min()) * 0.3
    luz = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=(255, 217, 138, 150))
    luz.putalpha(Image.fromarray((np.array(luz.getchannel("A")) * dentro).astype(np.uint8)))
    out.alpha_composite(luz)
    out.save(os.path.join(N, "porta_aberta.png"))


def cachos():
    com = abre("cacho_com")
    folhas = abre("cacho_colhido")
    if folhas.size == com.size:  # já montado antes
        return
    k = com.width * 0.98 / folhas.width
    folhas = folhas.resize((round(folhas.width * k), round(folhas.height * k)), Image.LANCZOS)
    tela = Image.new("RGBA", com.size, (0, 0, 0, 0))
    tela.alpha_composite(folhas, ((com.width - folhas.width) // 2, 0))
    tela.save(os.path.join(N, "cacho_colhido.png"))


def cesto_cheio():
    cesto = abre("cesto_vazio")
    bol = abre("bolinhas")
    w, h = cesto.size
    k = w * 0.58 / bol.width
    bol = bol.resize((round(bol.width * k), round(bol.height * k)), Image.LANCZOS)
    borda = int(h * 0.56)  # a borda de cima do cesto
    tela = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tela.alpha_composite(cesto)
    tela.alpha_composite(bol, ((w - bol.width) // 2, borda - int(bol.height * 0.78)))
    frente = cesto.crop((0, borda, w, h))
    tela.alpha_composite(frente, (0, borda))
    tela.save(os.path.join(N, "cesto_cheio.png"))


def balanco_assento():
    corda, prancha = abre("balanco_corda"), abre("balanco_prancha")
    w = 600
    k = w / prancha.width
    prancha = prancha.resize((w, round(prancha.height * k)), Image.LANCZOS)
    h = 1360
    comp = h - prancha.height // 2
    kc = comp / corda.height
    corda = corda.resize((max(1, round(corda.width * kc)), comp), Image.LANCZOS)
    tela = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for x in (int(w * 0.16), int(w * 0.84)):
        tela.alpha_composite(corda, (x - corda.width // 2, 0))
    tela.alpha_composite(prancha, (0, h - prancha.height))
    tela.save(os.path.join(N, "balanco_assento.png"))


def fundo_patio(w=2600, h=900, chao=600):
    ceu = abre("ceu")
    ceu = ceu.crop((12, 12, ceu.width - 12, ceu.height - 12)).convert("RGB").resize((w, h), Image.LANCZOS)
    tela = ceu.convert("RGBA")
    morro = abre("morro")
    for x, larg in [(-200, 1500), (1150, 1650)]:
        m = morro.resize((larg, round(morro.height * larg / morro.width)), Image.LANCZOS)
        tela.alpha_composite(m, (x, chao + 20 - m.height))
    nuvem = abre("nuvem")
    for x, y, larg in [(180, 70, 230), (880, 40, 170), (1500, 110, 250), (2120, 55, 190), (2430, 160, 130)]:
        n = nuvem.resize((larg, round(nuvem.height * larg / nuvem.width)), Image.LANCZOS)
        tela.alpha_composite(n, (x, y))
    tela.convert("RGB").save(os.path.join(N, "fundo_patio.png"))


if __name__ == "__main__":
    porta_aberta()
    cachos()
    cesto_cheio()
    balanco_assento()
    fundo_patio()
    nomes = sorted(f[:-4] for f in os.listdir(N) if f.endswith(".png"))
    with open(os.path.join(N, "_enche.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(nomes) + "\n")
    print(len(nomes), "peças 3D em", N)
