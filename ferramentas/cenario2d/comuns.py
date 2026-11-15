"""Peças que se repetem em vários cenários: feitas UMA vez e reaproveitadas (pedido de Carol, 15/11/2026).

Ficam em arte/cenario/comuns/2d/ (e a versão 3D em arte/cenario/comuns/png3d/). Os cenários usam
pelo nome; o tamanho em cada lugar pode mudar com a escala (4º valor no POS: (nome, x, y, escala)).
Uso: python3 ferramentas/cenario2d/comuns.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, svg, rr, path, ell, salvar  # noqa: E402
from moveis import CERCA_W, cerca, arvore_simples, janela_paisagem, planta_pendurada, grama_fundo  # noqa: E402

PASTA = "comuns"
CHAO = 600
P = {}
TABELA = []


def _peca(nome, corpo, w, h, titulo, pedido, defs=""):
    P[nome] = svg(w, h, corpo, defs)
    TABELA.append((titulo, f"{w} × {h}", None, pedido, [nome]))


_peca("cerca", cerca(CERCA_W, 82), CERCA_W, 92, "Cerca branca (módulo)",
      "Pedaço de cerca de madeira branca com 8 estacas pontudas e duas travessas. Os módulos ficam lado a lado, "
      "então as pontas das travessas precisam encaixar com o próximo.")
_peca("arvore_flores", arvore_simples(360, 440, C["verde"], C["rosa"], 4), 360, 440,
      "Árvore com florzinhas", "Árvore de copa verde bem redonda, cheia de florzinhas rosa, tronco marrom. A mesma árvore aparece "
      "em vários cenários, em tamanhos diferentes.")
_peca("janela", '<g transform="translate(24,22)">' + janela_paisagem(0, 0, 230, 180, C["rosa_chiclete"]) + "</g>", 278, 214,
      "Janela com cortinas", "Janela de madeira com cruz no meio, cortinas rosa dos lados e varão em cima; lá fora um morro verde, "
      "sol e uma arvorezinha rosa. Usada em todos os cômodos.")
_peca("planta_pendurada", planta_pendurada(40, 4, 150), 80, 172, "Planta pendurada",
      "Vasinho de madeira pendurado no teto por cordinhas, com folhinhas verdes caindo.")
_peca("pedra_caminho", ell(50, 19, 46, 15, "#e9e0d6", 'stroke-width="2.5"'), 100, 38, "Pedra do caminho",
      "Pedra lisa e achatada, bege clarinho, vista de cima e um pouco de frente (caminho de pedras no gramado).")


def _piso():
    w, h = 2200, 324
    s = rr(-5, 0, w + 10, 24, 0, C["madeira_esc"], 'stroke-width="3"') + rr(-5, 22, w + 10, h - 22 + 5, 0, "#e7bb87", 'stroke-width="3"')
    for y in range(22 + 45, h, 55):
        s += path(f"M0,{y} L{w},{y}", extra='stroke-width="1.5" opacity="0.3"')
    for i, y in enumerate(range(22, h, 55)):
        for x in range(90 + (i % 2) * 170, w, 340):
            s += path(f"M{x},{y} L{x},{y+55}", extra='stroke-width="1.5" opacity="0.25"')
    return s


_peca("piso", _piso(), 2200, 324, "Chão de tábuas com rodapé",
      "Chão de tábuas de madeira clara, visto de frente e um pouco de cima, com rodapé marrom na parte de cima. "
      "É o chão de todos os cômodos da casa (sala, cozinha, quarto).")
_peca("grama", grama_fundo(1100, 300, 0, random.Random(5), n_flores=40), 1100, 300, "Gramado (módulo)",
      "Pedaço de gramado verde com tufinhos e florzinhas miúdas. Os módulos ficam lado a lado, então as bordas "
      "da esquerda e da direita precisam emendar.")

if __name__ == "__main__":
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    destino = os.path.join(raiz, "arte/cenario", PASTA, "2d")
    salvar(P, os.path.join(destino, "svg"), destino)
    print(len(P), "peças comuns em", destino)
