"""Recorta uma folha de peças 3D (grade de quadros) em PNGs transparentes, todos do mesmo tamanho.

Uso: python3 ferramentas/recortar_folha.py FOLHA.png PASTA_SAIDA COLUNAS LINHAS QUANTOS FUNDO [nomes...]
  FUNDO: "transparente" (limpa sujeirinhas soltas), "branco" ou "verde" (tira a cor do fundo).
Cada quadro fica só com o maior pedaço (a peça) e todos saem com a mesma tela, apoiados embaixo e
centrados, para trocar um pelo outro sem a peça pular. Precisa de numpy, scipy e Pillow.
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def tirar_fundo(rgba, fundo):
    a = rgba[..., 3].astype(float)
    r, g, b = (rgba[..., i].astype(float) for i in range(3))
    if fundo == "branco":
        dist = np.sqrt((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2)
        a = np.minimum(a, np.clip((dist - 14) / 26, 0, 1) * 255)
    elif fundo == "verde":
        verde = g - np.maximum(r, b)
        a = np.minimum(a, np.clip(1 - (verde - 20) / 60, 0, 1) * 255)
        g = np.minimum(g, np.maximum(r, b) + 8)  # tira o reflexo verde da borda
        rgba[..., 1] = g.astype(np.uint8)
    rgba[..., 3] = a.astype(np.uint8)
    return rgba


def so_a_peca(rgba):
    mask = rgba[..., 3] > 40
    rot, n = ndimage.label(mask)
    if n == 0:
        return rgba
    tam = ndimage.sum(mask, rot, range(1, n + 1))
    maior = rot == (int(np.argmax(tam)) + 1)
    maior = ndimage.binary_fill_holes(maior)
    maior = ndimage.binary_dilation(maior, iterations=3)
    rgba[..., 3] = (rgba[..., 3] * maior).astype(np.uint8)
    return rgba


def main():
    folha, saida, cols, lins, quantos, fundo = sys.argv[1:7]
    cols, lins, quantos = int(cols), int(lins), int(quantos)
    nomes = sys.argv[7:] or [str(i) for i in range(quantos)]
    im = np.array(Image.open(folha).convert("RGBA"))
    h, w = im.shape[:2]
    quadros = []
    for i in range(quantos):
        c, l = i % cols, i // cols
        q = im[round(l * h / lins):round((l + 1) * h / lins), round(c * w / cols):round((c + 1) * w / cols)].copy()
        q[:4], q[-4:], q[:, :4], q[:, -4:] = 0, 0, 0, 0  # linhas da grade
        quadros.append(Image.fromarray(so_a_peca(tirar_fundo(q, fundo))))
    caixas = [q.getbbox() for q in quadros]
    largura = max(c[2] - c[0] for c in caixas) + 16
    altura = max(c[3] - c[1] for c in caixas) + 16
    os.makedirs(saida, exist_ok=True)
    for nome, q, c in zip(nomes, quadros, caixas):
        p = q.crop(c)
        tela = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        tela.paste(p, ((largura - p.width) // 2, altura - 8 - p.height), p)
        tela.save(os.path.join(saida, nome + ".png"))
    print(len(quadros), "quadros", largura, "x", altura, "em", saida)


if __name__ == "__main__":
    main()
