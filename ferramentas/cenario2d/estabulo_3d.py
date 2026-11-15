"""Monta as peças 3D do Estábulo que não vieram prontas (arte/cenario/estabulo/novo3d/).

Uso: python3 ferramentas/cenario2d/estabulo_3d.py   (depois: para_jogo.py estabulo)
- limpa as peças da Carol (originais em arte/objetos3d/estabulo_originais/); estados da mesma peça são
  recortados juntos, para não pularem quando trocam;
- lanterna_acesa: a lanterna dourada que a Carol mandou (apagada) com a chama e o vidro iluminado;
- parede_estabulo: a parede 3D esticada para a largura do estábulo; telhado_estabulo: a viga rosa;
- fundo: o céu, os morros, a palha e a grama da imagem da Carol, alargado para os 3300 px do cenário.
Originais da Carol, sem mexer: arte/objetos3d/estabulo_originais/.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "ferramentas"))
from limpar_3d import limpar  # noqa: E402

N = os.path.join(RAIZ, "arte/cenario/estabulo/novo3d")
ORIG = os.path.join(RAIZ, "arte/objetos3d/estabulo_originais")


SOZINHAS = ["lanterna_jardim", "cesto_pendurado", "pente_pendurado", "espelho", "pente", "escova_pendurada", "escova_pelo",
            "suporte_manta", "ganchos", "ferradura", "prateleira_banho", "tapete_coracao", "toalha", "tigela_racao", "tigela_agua",
            "pote_creme", "shampoo", "caixote_frutas", "fardo", "feno", "arvore",
            "vaso_flores", "trepadeira_flores", "cascata", "vitoria_regia"]
JUNTAS = [["lanterna_apagada"], ["ducha_ligada", "ducha_desligada"], ["balde_vazio", "balde_agua"],
          ["banheira_espuma", "banheira_agua"], ["cocho_vazio", "cocho_feno", "cocho_cenouras"],
          ["porteira_fechada", "porteira_aberta"], ["laguinho_parado", "laguinho_ondas"],
          ["flor_pendurada_rosa", "flor_pendurada_lilas"]]


def importar():
    for n in SOZINHAS:
        limpar(Image.open(os.path.join(ORIG, n + ".png"))).save(os.path.join(N, n + ".png"))
    for grupo in JUNTAS:
        ims = [limpar(Image.open(os.path.join(ORIG, n + ".png")), recortar=False) for n in grupo]
        caixas = [im.getbbox() for im in ims]
        caixa = (min(c[0] for c in caixas), min(c[1] for c in caixas), max(c[2] for c in caixas), max(c[3] for c in caixas))
        for n, im in zip(grupo, ims):
            im.crop(caixa).save(os.path.join(N, n + ".png"))


def vitoria_regia():
    """A folha veio vista de cima; achatada para parecer deitada na água."""
    im = Image.open(os.path.join(N, "vitoria_regia.png"))
    im.resize((im.width, round(im.height * 0.55)), Image.LANCZOS).save(os.path.join(N, "vitoria_regia.png"))


def parede_telhado():
    parede = limpar(Image.open(os.path.join(ORIG, "_parede.png")))
    parede.resize((round(parede.height * 1512 / 500), parede.height), Image.LANCZOS).save(os.path.join(N, "parede_estabulo.png"))
    limpar(Image.open(os.path.join(ORIG, "_telhado.png"))).save(os.path.join(N, "telhado_estabulo.png"))


def fundo(W=3300, H=900, chao=600):
    im = Image.open(os.path.join(ORIG, "_fundo.png")).convert("RGB")
    k = chao / 585                                     # a linha do horizonte da imagem fica no chão do jogo
    im = im.resize((round(im.width * k * H / 900), round(im.height * k)), Image.LANCZOS)
    im = im.crop((0, im.height - H, im.width, im.height))
    w = im.width
    palha, divisa, grama = round(w * 0.42), round(w * 0.42), round(w * 0.62)
    tela = Image.new("RGB", (W, H))
    tela.paste(im.crop((0, 0, palha, H)).resize((1460, H), Image.LANCZOS), (0, 0))   # palha do estábulo
    meio = im.crop((divisa, 0, w, H))
    tela.paste(meio, (1460, 0))
    x = 1460 + meio.width
    resto = im.crop((grama, 0, w, H))
    espelho = True
    while x < W:
        pedaco = resto.transpose(Image.FLIP_LEFT_RIGHT) if espelho else resto
        tela.paste(pedaco, (x, 0))
        x += pedaco.width
        espelho = not espelho
    tela.save(os.path.join(N, "fundo.png"))


def lanterna_acesa():
    im = Image.open(os.path.join(ORIG, "lanterna_apagada.png")).convert("RGBA")
    a = np.array(im).astype(float)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    vidro = (al > 0) & (np.abs(r - b) < 30) & (r > 170)            # vidro claro, quase sem cor
    w, h = im.size
    cx, cy = w * 0.508, h * 0.66                                    # vela
    yy, xx = np.mgrid[0:h, 0:w]
    luz = np.clip(1 - np.hypot((xx - cx) / (w * 0.42), (yy - cy) / (h * 0.42)), 0, 1)
    k = (vidro * (0.35 + 0.55 * luz))[..., None]
    a[..., :3] = a[..., :3] * (1 - k) + np.array([255, 214, 120]) * k
    out = Image.fromarray(a.astype(np.uint8))
    # chama em cima do pavio
    chama = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(chama)
    fx, fy = w * 0.508, h * 0.674
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([fx - 90, fy - 190, fx + 90, fy + 20], fill=(255, 214, 120, 110))
    out.alpha_composite(halo.filter(ImageFilter.GaussianBlur(40)))
    d.polygon([(fx, fy - 130), (fx + 26, fy - 40), (fx + 22, fy - 10), (fx, fy), (fx - 22, fy - 10), (fx - 26, fy - 40)], fill=(255, 170, 40, 255))
    d.ellipse([fx - 12, fy - 60, fx + 12, fy - 8], fill=(255, 245, 200, 255))
    chama = chama.filter(ImageFilter.GaussianBlur(3))
    out.alpha_composite(chama)
    limpar(out).save(os.path.join(N, "lanterna_acesa.png"))


if __name__ == "__main__":
    importar()
    vitoria_regia()
    parede_telhado()
    fundo()
    lanterna_acesa()
    nomes = sorted(f[:-4] for f in os.listdir(N) if f.endswith(".png"))
    with open(os.path.join(N, "_enche.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(nomes) + "\n")
    print(len(nomes), "peças 3D em", N)
