"""Monta as peças comuns 3D que vêm de mais de uma imagem da Carol (arte/cenario/comuns/novo3d/).

Uso: python3 ferramentas/cenario2d/comuns_3d.py
- grama: o gramado 3D (_grama_textura) num módulo que emenda dos lados, com florzinhas
  (_flor_rosa, _flor_branca, _flor_lilas, _flor_amarela) e tufinhos (_tufo) espalhados.
Os arquivos que começam com _ são só ingredientes (não entram no jogo sozinhos).
"""
import os
import random

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = os.path.join(RAIZ, "arte/cenario/comuns/novo3d")
K = 2  # o módulo 2D é 1100 × 300; a imagem sai com o dobro para ficar nítida


def abre(nome):
    return Image.open(os.path.join(N, nome + ".png")).convert("RGBA")


def grama(w=1100, h=300):
    W, H = w * K, h * K
    tex = abre("_grama_textura")
    tex = tex.crop((16, 16, tex.width - 16, tex.height - 16))
    alt = round(tex.width * H / (W + 200 * K))
    tex = tex.crop((0, 0, tex.width, min(alt, tex.height))).resize((W + 200 * K, H), Image.LANCZOS)
    base = tex.crop((0, 0, W, H))
    # emenda: o começo do módulo vem da continuação do fim, sumindo aos poucos
    # (assim o fim de um módulo emenda direitinho com o começo do próximo)
    faixa = 200 * K
    cont = tex.crop((W, 0, W + faixa, H))
    mascara = Image.linear_gradient("L").rotate(90, expand=True).point(lambda v: 255 - v).resize((faixa, H))  # 255 à esquerda
    base.paste(Image.composite(cont, base.crop((0, 0, faixa, H)), mascara), (0, 0))
    base = base.convert("RGBA")
    rnd = random.Random(11)
    flores = [abre(f"_flor_{c}") for c in ("rosa", "branca", "lilas", "amarela")]
    tufo = abre("_tufo")
    itens = []
    for _ in range(26):
        itens.append((tufo, rnd.uniform(20, 30) * K))
    for _ in range(34):
        itens.append((rnd.choice(flores), rnd.uniform(14, 22) * K))
    pos = []
    for im, larg in itens:
        larg = round(larg)
        alt = round(im.height * larg / im.width)
        for _ in range(40):
            x = rnd.uniform(25 * K, W - 25 * K - larg)
            y = rnd.uniform(18 * K, H - 10 * K - alt)
            if all(abs(x - px) > 40 * K or abs(y - py) > 30 * K for px, py in pos):
                break
        pos.append((x, y))
        pos_im = im.resize((larg, alt), Image.LANCZOS)
        base.alpha_composite(pos_im, (round(x), round(y)))
    base.convert("RGB").save(os.path.join(N, "grama.png"))


def pedra_caminho():
    """Pedra do caminho: a pedra 3D do pacote do Estábulo, achatada para ficar deitada no chão."""
    im = Image.open(os.path.join(RAIZ, "arte/objetos3d/estabulo_originais/pacote_R01/pedra.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    im.resize((im.width, round(im.width * 38 / 100)), Image.LANCZOS).save(os.path.join(N, "pedra_caminho.png"))


if __name__ == "__main__":
    pedra_caminho()
    grama()
    nomes = sorted(f[:-4] for f in os.listdir(N) if f.endswith(".png") and not f.startswith("_"))
    with open(os.path.join(N, "_enche.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(nomes) + "\n")
    print(nomes)
