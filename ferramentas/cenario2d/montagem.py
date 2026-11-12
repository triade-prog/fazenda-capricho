"""Monta uma prévia do cenário com as peças 2D e a Catarina (300 px) para conferir a escala.

Uso: python3 ferramentas/cenario2d/montagem.py <pasta_pecas> <saida.png> <largura> <altura> <pecas.json>
pecas.json: lista de [arquivo, x, y] em pixels do jogo (canto de cima à esquerda), na ordem de desenho.
Use "@catarina" como arquivo para colocar a Catarina com os pés em (x, y).
"""
import json
import sys
from PIL import Image

pasta, saida, W, H, lista = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
cat = Image.open("arte/personagens/catarina.png").convert("RGBA")
cat = cat.crop(cat.getbbox())
cat = cat.resize((round(cat.width * 300 / cat.height), 300), Image.LANCZOS)
tela = Image.new("RGBA", (W, H), (255, 255, 255, 255))
for nome, x, y in json.load(open(lista)):
    if nome == "@catarina":
        tela.alpha_composite(cat, (round(x - cat.width / 2), round(y - 300)))
        continue
    im = Image.open(f"{pasta}/{nome}.png").convert("RGBA")
    # as peças estão em 2x ou 4x: volta para o tamanho do jogo
    import re
    svgtxt = open(f"{pasta}/svg/{nome}.svg").read()
    w, h = map(int, re.search(r'width="(\d+)" height="(\d+)"', svgtxt).groups())
    im = im.resize((w, h), Image.LANCZOS)
    tela.alpha_composite(im, (round(x), round(y)))
tela.convert("RGB").save(saida)
