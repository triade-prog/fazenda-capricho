"""Limpa uma peça 3D transparente enviada pela Carol e recorta justo no desenho.

Uso: python3 ferramentas/limpar_3d.py ORIGINAL.png SAIDA.png

- tira os pontinhos soltos em volta (fica só o que é grande perto da peça principal);
- tira a franja colorida (vermelho/amarelo/ciano) dos pixels meio transparentes da borda,
  pintando cada um com a cor do pixel firme mais próximo;
- recorta na caixa do desenho (sem margem sobrando).
Precisa de numpy, scipy e Pillow.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def limpar(im, minimo=0.02, corte=40, recortar=True):
    a = np.array(im.convert("RGBA"))
    alfa = a[..., 3].astype(float)
    alfa[alfa < corte] = 0
    mask = alfa > 0
    rot, n = ndimage.label(mask, structure=np.ones((3, 3)))
    if n:
        tam = ndimage.sum(mask, rot, range(1, n + 1))
        fica = np.zeros(n + 1, bool)
        fica[1:] = tam >= tam.max() * minimo  # pedaços pequenos demais são sujeira
        alfa[~fica[rot]] = 0
    firme = alfa >= 230
    if firme.any():
        _, (iy, ix) = ndimage.distance_transform_edt(~firme, return_indices=True)
        borda = (alfa > 0) & ~firme
        a[..., :3][borda] = a[..., :3][iy[borda], ix[borda]]
    a[..., 3] = alfa.astype(np.uint8)
    out = Image.fromarray(a)
    return out.crop(out.getbbox()) if recortar else out


if __name__ == "__main__":
    limpar(Image.open(sys.argv[1])).save(sys.argv[2])
