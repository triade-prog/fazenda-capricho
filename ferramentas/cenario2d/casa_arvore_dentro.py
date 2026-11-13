"""C08 Dentro da casa na árvore: como o interior entra no protótipo (as peças são as de casa_arvore.py)."""
from casa_arvore import P, POS_DENTRO as POS  # noqa: F401

PASTA = "casa_arvore"
W, H, CHAO = 1600, 900, 600

JOGO = {
    "interativos": {
        "porta": {"estados": ["porta_dentro_fechada", "porta_dentro_aberta"], "x": 1440, "y": 340, "leva": "casa_arvore", "chegada": 1400, "estado": 0},
        "bau": {"estados": ["bau_fechado", "bau_aberto"], "x": 1040, "y": 500},
        "fogaozinho": {"estados": ["cozinha_desligada", "cozinha_ligada"], "x": 470, "y": 460},
        "passarinho": {"estados": ["passarinho_pousado", "passarinho_voando"], "x": 830, "y": 100},
    },
    "objetos": ["panelinha", "bule", "xicara_cha", "unicornio", "ursinho_heroi"],
    "lugares": [{"id": "cama_arvore", "area": [70, 520, 340, 170], "spots": [[240, 640]], "pose": "deitar"}],
    "superficies": [[475, 685, 460], [790, 950, 690]],
}
