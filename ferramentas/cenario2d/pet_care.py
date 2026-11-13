"""C10 Pet Care (área dos animais): peças 2D provisórias, layout e prompts 3D.

Uso: python3 ferramentas/cenario2d/pet_care.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import plaquinha, planta_vaso, ceu_morros, cerca, grama_fundo, arvore_simples  # noqa: E402

W, H, CHAO = 2600, 900, 600
P = {}


def pata(cx, cy, k, cor):
    s = ell(cx, cy + 5 * k, 9 * k, 7 * k, cor, 'stroke-width="2"')
    for dx, dy in [(-11, -5), (-4, -11), (4, -11), (11, -5)]:
        s += circ(cx + dx * k, cy + dy * k, 3.5 * k, cor, 'stroke-width="1.5"')
    return s


def fundo():
    rnd = random.Random(31)
    s, defs = ceu_morros(W, H, CHAO, rnd)
    s += f'<g transform="translate(60,170)">{arvore_simples(380, 440, C["verde"], C["rosa"], 2)}</g>'
    s += f'<g transform="translate(2200,190)">{arvore_simples(340, 420, C["verde_esc"], C["branco"], 3)}</g>'
    s += cerca(W, CHAO)
    # pérgola de madeira com flores (fundo)
    x0, x1, top = 700, 1500, 170
    for x in (x0, x0 + 260, x1 - 260, x1):
        s += rr(x - 14, top, 28, CHAO - top + 8, 5, C["madeira"], 'stroke-width="3.5"')
    s += rr(x0 - 60, top - 26, x1 - x0 + 120, 30, 8, C["madeira_esc"], 'stroke-width="3.5"')
    for x in range(x0 - 40, x1 + 60, 60):
        s += rr(x, top - 46, 18, 28, 4, C["madeira"], 'stroke-width="2.5"')
    for x in range(x0 - 50, x1 + 60, 36):
        s += circ(x, top - 20 + (x % 3) * 6, 16, C["verde"], 'stroke-width="2.5"')
    for x in range(x0 - 40, x1 + 60, 46):
        s += flor(x, top - 26 + (x % 4) * 5, 8, C["rosa"] if x % 2 else C["rosa_chiclete"], C["amarelo"])
    for x in (x0, x1):
        for y in range(top + 30, CHAO - 40, 70):
            s += flor(x + (8 if y % 140 else -8), y, 7, C["rosa"], C["amarelo"])
    # piso de pedrinhas sob a pérgola
    s += grama_fundo(W, H, CHAO, rnd)
    s += ell(1100, 700, 470, 70, "#e9e0d6", 'stroke-width="3"')
    for _ in range(40):
        x, y = rnd.uniform(700, 1500), rnd.uniform(660, 745)
        if ((x - 1100) / 450) ** 2 + ((y - 700) / 62) ** 2 < 1:
            s += ell(round(x), round(y), rnd.uniform(14, 24), rnd.uniform(7, 10), rnd.choice(["#d8cfc5", "#f3ece4"]), 'stroke-width="1.5"')
    return svg(W, H, s, defs)


P["fundo"] = fundo()


def banheira(estado):
    w, h = 300, 170
    s = ""
    if estado == "espuma":
        for x, y, r in [(50, 46, 26), (90, 32, 30), (140, 26, 32), (190, 32, 30), (235, 44, 26), (115, 50, 22), (170, 52, 22)]:
            s += circ(x, y, r, C["branco"], 'stroke-width="2.5"')
        for x, y, r in [(70, 12, 8), (210, 8, 10), (260, 20, 6)]:
            s += circ(x, y, r, "#eef7ff", 'stroke-width="2"')
    s += path("M14,56 L286,56 Q284,150 230,158 L70,158 Q16,150 14,56 Z", C["branco"], 'stroke-width="4"')
    if estado in ("agua", "espuma"):
        s += ell(150, 60, 132, 12, C["agua"], 'stroke-width="2.5"')
    else:
        s += ell(150, 60, 132, 12, "#e3eef5", 'stroke-width="2.5"')
    s += rr(6, 48, 288, 18, 9, C["rosa_claro"], 'stroke-width="3"')
    s += pata(150, 106, 2.2, C["rosa_chiclete"])
    s += rr(64, 156, 24, 12, 5, C["madeira_esc"]) + rr(212, 156, 24, 12, 5, C["madeira_esc"])
    return svg(w, h, s)


P["banheira_vazia"] = banheira("vazia")
P["banheira_agua"] = banheira("agua")
P["banheira_espuma"] = banheira("espuma")


def chuveirinho(ligado):
    w, h = 140, 320
    s = rr(14, 30, 16, 288, 5, C["cinza"], 'stroke-width="3"') + path("M22,32 Q22,6 60,10 L92,18", extra='stroke-width="10"')
    s += path("M22,32 Q22,6 60,10 L92,18", extra=f'stroke-width="5" stroke="{C["cinza"]}"')
    s += path("M78,18 L118,18 L112,36 L84,36 Z", C["cinza"], 'stroke-width="3"')
    if ligado:
        for i, x in enumerate(range(88, 116, 6)):
            s += path(f"M{x},40 q{-8 + i*4},70 {-14 + i*8},150", extra=f'stroke="{C["agua"]}" stroke-width="5" opacity="0.9"')
        for x, y in [(86, 120), (112, 150), (96, 180)]:
            s += circ(x, y, 5, C["agua"], 'stroke-width="1.5"')
    s += circ(22, 200, 12, C["rosa_forte"], 'stroke-width="2.5"') + coracao(22, 201, 6, C["branco"], 'stroke="none"')
    s += rr(4, 306, 36, 12, 4, C["cinza"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["chuveirinho_desligado"] = chuveirinho(False)
P["chuveirinho_ligado"] = chuveirinho(True)
P["xampu"] = svg(40, 60, rr(6, 18, 28, 40, 9, C["rosa"], 'stroke-width="2.5"') + rr(14, 8, 12, 12, 3, C["lilas"], 'stroke-width="2"') +
                 path("M20,8 L20,3 L30,3", extra='stroke-width="2.5"') + pata(20, 36, 0.9, C["rosa_forte"]))
P["toalha"] = svg(100, 60, path("M4,12 Q50,2 96,12 L94,54 Q50,46 6,54 Z", C["azul"], 'stroke-width="2.5"') +
                  path("M6,44 Q50,36 94,44 L94,54 Q50,46 6,54 Z", C["branco"], 'stroke-width="2"') + pata(50, 24, 0.8, C["branco"]))
P["bolha"] = svg(30, 30, circ(15, 15, 12, "#f4fbff", 'stroke-width="2" fill-opacity="0.9"') + ell(11, 10, 3.5, 2, C["rosa"], 'stroke="none"'))


def tigela(tipo, cheia):
    w, h = 80, 40
    cor = C["rosa_chiclete"] if tipo == "cao" else C["lilas"]
    s = ""
    if cheia:
        if tipo == "agua":
            s += ell(40, 14, 30, 6, C["agua"], 'stroke-width="2"')
        else:
            for x in range(20, 64, 9):
                s += circ(x, 13 - (x % 2) * 2, 5, "#c98c56", 'stroke-width="1.5"')
    s += path("M6,14 L74,14 L64,36 L16,36 Z", cor if tipo != "agua" else C["azul"], 'stroke-width="2.5"')
    s += ell(40, 14, 34, 5, "none", 'stroke-width="2.5"')
    s += pata(40, 24, 0.55, C["branco"])
    return svg(w, h, s)


for t in ("cao", "gato", "agua"):
    P[f"tigela_{t}_vazia"] = tigela(t, False)
    P[f"tigela_{t}_cheia"] = tigela(t, True)
P["biscoito"] = svg(40, 36, coracao(20, 18, 16, "#e6b47e", 'stroke-width="2.5"') + circ(15, 15, 2, "#c98c56", 'stroke="none"') +
                    circ(25, 15, 2, "#c98c56", 'stroke="none"') + circ(20, 22, 2, "#c98c56", 'stroke="none"'))
P["peixinho"] = svg(44, 26, ell(18, 13, 15, 9, C["azul"], 'stroke-width="2.2"') + path("M32,13 L42,4 L42,22 Z", C["azul"], 'stroke-width="2.2"') +
                    circ(10, 11, 2, L, 'stroke="none"') + path("M16,7 q4,6 0,12", extra='stroke-width="1.5"'))
P["bolinha"] = svg(30, 30, circ(15, 15, 12, C["amarelo"], 'stroke-width="2.2"') + path("M5,11 Q15,17 25,11 M5,19 Q15,13 25,19", extra=f'stroke="{C["branco"]}" stroke-width="2"'))
P["osso"] = svg(56, 26, path("M12,8 a6,6 0 1 1 4,-2 L40,6 a6,6 0 1 1 4,2 a6,6 0 1 1 -4,10 L16,18 a6,6 0 1 1 -4,-10 Z", C["branco"], 'stroke-width="2.2"'))
P["varinha_pena"] = svg(40, 120, path("M8,116 L30,30", extra='stroke-width="5"') + path("M8,116 L30,30", extra=f'stroke-width="2.5" stroke="{C["madeira_clara"]}"') +
                        path("M30,30 q-8,-20 0,-28 q8,8 0,28 Z", C["rosa_chiclete"], 'stroke-width="2"') + path("M30,30 q4,-18 10,-20 q2,12 -10,20 Z", C["lilas"], 'stroke-width="2"') +
                        path("M30,30 q-14,-8 -18,-18 q12,0 18,18 Z", C["amarelo"], 'stroke-width="2"'))


def cercadinho():
    w, h = 420, 180
    s = ell(210, 140, 200, 34, C["rosa_claro"], 'stroke-width="3"')                          # caminha
    s += ell(210, 136, 170, 24, "#fff0f6", 'stroke-width="2"')
    for i, x in enumerate(range(16, 410, 30)):
        s += rr(x, 30, 14, 128 + (8 if 4 < i < 9 else 0), 6, C["branco"], 'stroke-width="2.5"')
    s += rr(6, 44, 408, 14, 6, C["branco"], 'stroke-width="3"') + rr(6, 120, 408, 14, 6, C["branco"], 'stroke-width="3"')
    s += coracao(210, 26, 14, C["rosa_forte"], 'stroke-width="2.5"')
    for x in (60, 360):
        s += flor(x, 44, 8, C["lilas"], C["amarelo"])
    return svg(w, h, s)


P["cercadinho"] = cercadinho()


def prateleira():
    w, h = 220, 140
    s = rr(10, 4, 14, 134, 4, C["madeira_esc"]) + rr(196, 4, 14, 134, 4, C["madeira_esc"])
    s += rr(0, 60, 220, 14, 4, C["madeira"], 'stroke-width="3"') + rr(0, 120, 220, 14, 4, C["madeira"], 'stroke-width="3"')
    return svg(w, h, s)


P["prateleira"] = prateleira()
P["gancho_toalha"] = svg(60, 40, rr(4, 8, 52, 12, 5, C["madeira"], 'stroke-width="2.5"') + path("M20,20 q0,14 8,14 M40,20 q0,14 8,14", extra='stroke-width="3"'))
P["placa_pata"] = plaquinha("pata", 90, 80)
P["vaso_flores"] = planta_vaso(70, 90, C["rosa_chiclete"], C["rosa"])

POS = [("fundo", 0, 0), ("placa_pata", 1060, 60),
       ("chuveirinho_ligado", 760, 290), ("banheira_espuma", 840, 440), ("bolha", 980, 380), ("bolha", 1030, 350),
       ("prateleira", 1230, 300), ("xampu", 1250, 320), ("toalha", 1300, 324), ("gancho_toalha", 1380, 250), ("osso", 1250, 395), ("bolinha", 1330, 386), ("varinha_pena", 1400, 300),
       ("tigela_cao_cheia", 1560, 640), ("tigela_gato_cheia", 1660, 640), ("tigela_agua_cheia", 1760, 640),
       ("biscoito", 1600, 600), ("peixinho", 1700, 606),
       ("cercadinho", 1900, 520), ("vaso_flores", 620, 520), ("vaso_flores", 1530, 520),
       ("@catarina", 1150, 860), ("@catarina", 500, 820)]

TABELA = [
    ("Fundo do Pet Care", "2600 × 900", None, "Céu claro, morros verdes, duas árvores floridas, cerca branca, grama com florzinhas e, no centro, uma pérgola de madeira coberta de flores rosa com piso de pedrinhas claras. SEM banheira, chuveiro, tigelas ou cercadinho.", ["fundo"]),
    ("Banheira com patinha", "300 × 170", "vazia · com água · com espuma", "Banheira branca com pezinhos, borda rosa e uma patinha rosa na frente. Espuma: montinho de bolhas brancas por cima. Os bichos entram nela.", ["banheira_vazia", "banheira_agua", "banheira_espuma"]),
    ("Chuveirinho", "140 × 320", "desligado · ligado", "Coluna de chuveiro prateada de brinquedo com registro rosa de coração. Ligado: água azul-clara caindo em fios fofos, sem respingo no chão.", ["chuveirinho_desligado", "chuveirinho_ligado"]),
    ("Xampu", "40 × 60", None, "Frasquinho rosa com tampa lilás e patinha.", ["xampu"]),
    ("Toalha", "100 × 60", None, "Toalha azul-clara com barra branca e patinha.", ["toalha"]),
    ("Bolha de sabão", "30 × 30", None, "Bolha branca com reflexo rosa (efeito).", ["bolha"]),
    ("Tigelas", "80 × 40", "vazia · cheia (cão, gato, água)", "Tigela rosa (ração de cachorro), lilás (ração de gato) e azul (água), com patinha.", ["tigela_cao_vazia", "tigela_cao_cheia", "tigela_gato_vazia", "tigela_gato_cheia", "tigela_agua_vazia", "tigela_agua_cheia"]),
    ("Petiscos", "biscoito 40 × 36 · peixinho 44 × 26", None, "Biscoito de coração (cães) e peixinho azul de petisco (gatos).", ["biscoito", "peixinho"]),
    ("Brinquedos", "bolinha 30 × 30 · osso 56 × 26 · varinha 40 × 120", None, "Bolinha amarela, osso de brinquedo branco e varinha com penas coloridas (o Leo pula atrás).", ["bolinha", "osso", "varinha_pena"]),
    ("Cercadinho", "420 × 180", None, "Cercadinho branco baixo com coração e flores, com uma caminha rosa redonda dentro: lugar seguro para o bicho se acalmar e cochilar.", ["cercadinho"]),
    ("Prateleira e gancho", "prateleira 220 × 140 · gancho 60 × 40", None, "Prateleira de madeira com duas tábuas VAZIAS (xampu e brinquedos são peças separadas) e gancho para a toalha.", ["prateleira", "gancho_toalha"]),
    ("Placa e vaso", "placa 90 × 80 · vaso 70 × 90", None, "Plaquinha de madeira com patinha (sem letras) e vaso de flores rosa.", ["placa_pata", "vaso_flores"]),
]

# Como o cenário entra no protótipo (ver para_jogo.py).
JOGO = {
    "interativos": {
        "chuveirinho": {"estados": ["chuveirinho_desligado", "chuveirinho_ligado"], "x": 760, "y": 290},
        "banheira": {"estados": ["banheira_vazia", "banheira_agua", "banheira_espuma"], "x": 840, "y": 440},
        "tigela_cao": {"estados": ["tigela_cao_vazia", "tigela_cao_cheia"], "x": 1560, "y": 640},
        "tigela_gato": {"estados": ["tigela_gato_vazia", "tigela_gato_cheia"], "x": 1660, "y": 640},
        "tigela_agua": {"estados": ["tigela_agua_vazia", "tigela_agua_cheia"], "x": 1760, "y": 640},
        "seta_estabulo": {"estados": ["seta_ferradura_e"], "x": 380, "y": 470, "leva": "estabulo", "chegada": 440},
    },
    "extras": [("seta_ferradura_e", 380, 470)],
    "objetos": ["xampu", "toalha", "osso", "bolinha", "varinha_pena", "biscoito", "peixinho"],
    "lugares": [],
    "superficies": [[1235, 1445, 382], [1235, 1445, 421]],
}

if __name__ == "__main__":
    pr, le = textos("pet_care", "Pet Care", "C10",
                    "É o cantinho ao ar livre para cuidar dos bichos: banho de espuma, toalha, comidinha, brinquedos e um cercadinho para acalmar.",
                    " e a colagem `arte/conceito/colagem_cenarios/colagem_pet_care.png` (só o clima)",
                    "2600 × 900, chão a partir de y = 600", TABELA,
                    aviso="\n**Sem casinha de cachorro:** a colagem tem uma, mas o GDD diz que o Bob dorme com a família. Ela fica de fora até as criadoras decidirem.\n",
                    ordem="\nGere primeiro a banheira com os três estados e o chuveirinho: são o centro da brincadeira.\n")
    gerar_cenario("pet_care", P, W, H, POS, "C10 Pet Care · Catarina = 300 px · chão a partir de y = 600 · tela 2600 × 900", pr, le)
