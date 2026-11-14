"""C04 Cozinha da Fazenda: peças 2D provisórias, layout e prompts 3D.

Uso: python3 ferramentas/cenario2d/cozinha.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import porta_casa, plaquinha, planta_vaso, janela_paisagem, parede_interna  # noqa: E402

W, H, CHAO = 2200, 900, 600
P = {}
XADREZ = C["vermelho_rosa"]


def fundo():
    s = parede_interna(W, H, CHAO, "#ffe9e2", "#ffe0ea", listras=False)
    # azulejinhos atrás da bancada
    for x in range(560, 1460, 40):
        for y in range(330, 440, 40):
            s += rr(x, y, 40, 40, 0, "#fff6f9" if (x // 40 + y // 40) % 2 else "#ffe1ec", 'stroke-width="1" stroke-opacity="0.4"')
    # armários de madeira (fundo, sem interação)
    s += rr(560, 440, 900, 160, 6, C["madeira"], 'stroke-width="3.5"')
    for x in range(570, 1450, 150):
        s += rr(x, 456, 136, 132, 6, C["madeira_clara"], 'stroke-width="2.5"') + circ(x + 120, 520, 5, C["dourado"], 'stroke-width="2"')
    s += rr(550, 424, 920, 22, 6, C["branco"], 'stroke-width="3"')
    # prateleira com potes e panelas penduradas
    s += rr(560, 120, 540, 16, 5, C["madeira"], 'stroke-width="3"')
    for i, (x, c) in enumerate([(590, C["rosa"]), (650, C["lilas"]), (710, C["azul"]), (770, C["rosa_chiclete"])]):
        s += rr(x, 72, 46, 48, 10, c, 'stroke-width="2.5"') + rr(x + 4, 64, 38, 10, 4, C["branco"], 'stroke-width="2"')
    s += planta_vaso_inline(860, 50)
    s += path("M560,200 L1100,200", extra='stroke-width="6"') + path("M560,200 L1100,200", extra=f'stroke-width="3" stroke="{C["madeira_esc"]}"')
    for x, r in [(620, 34), (720, 28), (810, 32), (910, 26), (1000, 30)]:
        s += path(f"M{x},200 L{x},{214}", extra='stroke-width="2.5"')
        s += path(f"M{x},{214} L{x},{230}", extra='stroke-width="6"') + circ(x, 230 + r, r, "#d99a64", 'stroke-width="3"') + circ(x, 230 + r, r - 8, "#c98454", 'stroke="none"')
    s += janela_paisagem(1180, 150, 230, 180, C["rosa_chiclete"])
    return svg(W, H, s)


def planta_vaso_inline(x, y):
    s = ""
    for a in (-150, -110, -70, -30):
        import math
        s += ell(x + 30 + 22 * math.cos(math.radians(a)), y + 40 + 22 * math.sin(math.radians(a)), 18, 7, C["verde"], f'stroke-width="2" transform="rotate({a} {x + 30 + 22 * math.cos(math.radians(a)):.1f} {y + 40 + 22 * math.sin(math.radians(a)):.1f})"')
    return s + path(f"M{x+10},{y+40} L{x+50},{y+40} L{x+44},{y+70} L{x+16},{y+70} Z", C["madeira"], 'stroke-width="2.5"')


P["fundo"] = fundo()


def geladeira(aberta):
    w, h = 230, 430
    s = rr(10, 10, 210, 410, 30, C["lilas"], 'stroke-width="4"')
    if not aberta:
        s += path("M14,150 L216,150", extra='stroke-width="3"')
        s += rr(176, 60, 12, 60, 6, C["branco"], 'stroke-width="2.5"') + rr(176, 190, 12, 90, 6, C["branco"], 'stroke-width="2.5"')
        s += coracao(80, 80, 18, C["amarelo"], 'stroke-width="2.5"') + coracao(90, 250, 14, C["rosa_chiclete"], 'stroke-width="2.5"')
    else:
        s += rr(24, 24, 182, 382, 22, "#f2f7ff", 'stroke-width="3"')
        for y in (130, 230, 320):
            s += rr(30, y, 170, 8, 3, "#cfe3f5", 'stroke-width="2"')
        # prateleiras vazias: as comidinhas são objetos soltos do jogo (JOGO["dentro"])
        s += path("M206,20 L236,6 L236,426 L206,412 Z", C["lilas"], 'stroke-width="3"')
    s += rr(30, 412, 30, 16, 4, C["roxo"]) + rr(170, 412, 30, 16, 4, C["roxo"])
    return svg(w + 8, h, s)


P["geladeira_fechada"] = geladeira(False)
P["geladeira_aberta"] = geladeira(True)


def mesa():
    w, h = 420, 200
    s = rr(50, 80, 22, 118, 5, C["madeira_esc"]) + rr(348, 80, 22, 118, 5, C["madeira_esc"])
    s += rr(10, 60, 400, 24, 8, C["madeira"], 'stroke-width="3.5"')
    s += path("M20,56 L400,56 L392,150 L28,150 Z", C["branco"], 'stroke-width="3"')
    for x in range(30, 392, 30):
        s += rr(x, 58, 15, 90, 0, XADREZ, 'stroke="none" opacity="0.55"')
    for y in range(70, 150, 30):
        s += rr(24, y, 372, 15, 0, XADREZ, 'stroke="none" opacity="0.35"')
    s += path("M20,56 L400,56 L392,150 L28,150 Z", "none", 'stroke-width="3"')
    s += rr(14, 46, 392, 16, 6, C["branco"], 'stroke-width="3"')
    return svg(w, h, s)


P["mesa"] = mesa()
P["cadeira"] = svg(110, 230, rr(14, 6, 82, 120, 16, C["madeira"], 'stroke-width="3.5"') + coracao(55, 60, 20, C["madeira_esc"], 'stroke-width="3"') +
                   rr(6, 120, 98, 24, 8, C["madeira"], 'stroke-width="3.5"') + rr(14, 144, 14, 84, 4, C["madeira_esc"]) + rr(82, 144, 14, 84, 4, C["madeira_esc"]))


def fogao(vapor):
    w, h = 240, 260
    s = rr(10, 90, 220, 168, 12, C["branco"], 'stroke-width="4"') + rr(4, 80, 232, 22, 8, C["rosa"], 'stroke-width="3.5"')
    s += rr(36, 130, 168, 90, 10, "#f3e5ee", 'stroke-width="3"') + rr(56, 120, 128, 8, 3, C["rosa_forte"], 'stroke-width="2"')
    for x in (60, 100, 140, 180):
        s += circ(x, 240, 8, C["lilas"], 'stroke-width="2.5"')
    # panela
    s += path("M70,40 L170,40 L162,82 L78,82 Z", C["rosa_chiclete"], 'stroke-width="3"') + rr(64, 32, 112, 12, 5, C["rosa"], 'stroke-width="2.5"')
    s += path("M170,46 L196,40 M70,46 L44,40", extra='stroke-width="5"')
    if vapor:
        for x in (96, 144):
            s += path(f"M{x},28 q-10,-10 0,-18 q10,-8 0,-18", extra=f'stroke="#c9bcd6" stroke-width="3"')
        s += coracao(120, 10, 8, C["rosa"], 'stroke-width="2"')
    return svg(w, h, s)


P["fogao"] = fogao(False)
P["fogao_vapor"] = fogao(True)


def pia():
    w, h = 260, 200
    s = rr(10, 60, 240, 138, 8, C["madeira"], 'stroke-width="3.5"')
    s += rr(28, 80, 96, 104, 6, C["madeira_clara"], 'stroke-width="2.5"') + rr(136, 80, 96, 104, 6, C["madeira_clara"], 'stroke-width="2.5"')
    s += rr(2, 46, 256, 20, 6, C["branco"], 'stroke-width="3"') + ell(130, 52, 70, 8, "#d9e9f5", 'stroke-width="2.5"')
    s += path("M130,46 L130,14 Q130,4 150,6 L158,8", extra='stroke-width="8"') + path("M130,46 L130,14 Q130,4 150,6 L158,8", extra=f'stroke-width="4" stroke="{C["cinza"]}"')
    s += circ(112, 30, 7, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["pia"] = pia()


def prato(sujo):
    s = ell(30, 16, 28, 12, C["branco"], 'stroke-width="2.5"') + ell(30, 15, 17, 6, "#f3f3f3", 'stroke-width="1.5"')
    if sujo:
        s += ell(24, 15, 6, 3, "#d79a5f", 'stroke="none"') + ell(36, 13, 4, 2, "#e28585", 'stroke="none"')
    else:
        s += estrela(46, 8, 5, C["branco"], 4, 'stroke-width="1.2"')
    return svg(60, 30, s)


P["prato_limpo"] = prato(False)
P["prato_sujo"] = prato(True)
P["xicara"] = svg(40, 36, ell(18, 32, 16, 3.5, C["rosa"], 'stroke-width="2"') + path("M6,12 L30,12 Q29,30 18,30 Q7,30 6,12 Z", C["branco"], 'stroke-width="2.2"') +
                  path("M30,15 q7,2 2,9", extra='stroke-width="2.2"') + coracao(18, 20, 4, C["rosa_forte"], 'stroke-width="1.2"'))
P["maca"] = svg(30, 32, path("M15,8 Q4,2 3,16 Q4,30 15,29 Q26,30 27,16 Q26,2 15,8 Z", "#ef4d4d", 'stroke-width="2"') + path("M15,8 L16,2", extra='stroke-width="2"') +
                circ(9, 13, 2.5, C["branco"], 'stroke="none"'))
P["banana"] = svg(50, 30, path("M4,8 Q10,26 30,26 Q44,24 47,14 Q40,18 30,18 Q14,18 8,6 Z", C["amarelo"], 'stroke-width="2"') + rr(2, 4, 7, 6, 2, "#8a6a3a", 'stroke-width="1.5"'))
P["copo_leite"] = svg(30, 44, path("M5,4 L25,4 L22,42 L8,42 Z", C["branco"], 'stroke-width="2.2"') + path("M6,14 L24,14", extra='stroke-width="1.5" opacity="0.5"'))
P["queijo"] = svg(44, 32, path("M4,28 L40,28 L40,14 L4,22 Z", "#ffd45c", 'stroke-width="2.2"') + path("M4,22 L40,14 L30,6 Z", "#ffe08a", 'stroke-width="2.2"') +
                  circ(16, 24, 3, "#f0b93a", 'stroke="none"') + circ(30, 22, 2.5, "#f0b93a", 'stroke="none"'))
P["cenoura"] = svg(52, 26, path("M14,6 Q40,6 49,13 Q40,21 14,20 Q8,13 14,6 Z", C["laranja"], 'stroke-width="2.2"') + path("M14,9 L4,3 M13,13 L2,13 M14,17 L4,23", extra=f'stroke="{C["verde"]}" stroke-width="3.5"') +
                   path("M24,8 L24,12 M33,9 L33,12", extra='stroke-width="1.4" opacity="0.5"'))
P["sanduiche"] = svg(50, 34, path("M4,22 Q25,4 46,22 Z", "#f3c98f", 'stroke-width="2.2"') + rr(4, 20, 42, 5, 2, C["verde"], 'stroke-width="1.5"') +
                     rr(4, 24, 42, 4, 2, "#ef7a7a", 'stroke-width="1.5"') + rr(4, 27, 42, 6, 3, "#f3c98f", 'stroke-width="2"'))


def tigela_bicho(cor, cheia, comida):
    w, h = 80, 40
    s = ""
    if cheia:
        if comida == "biscoito":
            for x in (26, 40, 54):
                s += coracao(x, 12, 6, "#e6b47e", 'stroke-width="1.5"')
        elif comida == "peixe":
            s += ell(38, 12, 12, 6, C["azul"], 'stroke-width="1.5"') + path("M49,12 L57,6 L57,18 Z", C["azul"], 'stroke-width="1.5"')
        else:
            s += path("M18,14 L58,8 L22,20 Z", C["laranja"], 'stroke-width="1.5"') + circ(56, 12, 7, "#ef4d4d", 'stroke-width="1.5"')
    s += path("M6,16 L74,16 L64,38 L16,38 Z", cor, 'stroke-width="2.5"') + ell(40, 16, 34, 5, "none", 'stroke-width="2.5"')
    return svg(w, h, s)


for nome, cor, com in (("cao", C["rosa_chiclete"], "biscoito"), ("gato", C["lilas"], "peixe"), ("lumi", C["mel"], "cenoura")):
    P[f"tigela_{nome}_vazia"] = tigela_bicho(cor, False, com)
    P[f"tigela_{nome}_cheia"] = tigela_bicho(cor, True, com)
P["vaso_flores"] = planta_vaso(70, 90, C["rosa"], C["amarelo"])
P["porta_fechada"] = porta_casa(False)
P["porta_aberta"] = porta_casa(True)
P["placa_casa"] = plaquinha("casa")

POS = [("fundo", 0, 0), ("porta_aberta", 60, 250), ("placa_casa", 110, 180),
       ("geladeira_fechada", 300, 170),
       ("fogao_vapor", 600, 340), ("pia", 1200, 400), ("prato_sujo", 1240, 420),
       ("xicara", 940, 400), ("vaso_flores", 1000, 350),
       ("cadeira", 1480, 470), ("mesa", 1560, 500), ("cadeira", 1990, 470),
       ("prato_limpo", 1640, 528), ("sanduiche", 1700, 520), ("vaso_flores", 1910, 468),
       ("tigela_cao_cheia", 700, 760), ("tigela_gato_cheia", 800, 760), ("tigela_lumi_cheia", 900, 760),
       ("@catarina", 1100, 860), ("@catarina", 1650, 790)]

TABELA = [
    ("Fundo da cozinha", "2200 × 900", None, "Parede rosa-pêssego com vigas, azulejinhos rosa e branco, armários de madeira embutidos atrás da bancada, prateleira com potes coloridos e uma plantinha, panelas de cobre penduradas e janela com cortina rosa. SEM geladeira, fogão, pia, mesa e porta.", ["fundo"]),
    ("Geladeira lilás", "238 × 430", "fechada · aberta", "Geladeira retrô lilás com cantos bem arredondados e ímãs de coração. Aberta: prateleiras com frutas, leite, cenoura e maçã (para a Lumi), peixinho (gatos) e biscoito de coração (cães); a porta aberta aparece fina do lado direito.", ["geladeira_fechada", "geladeira_aberta"]),
    ("Fogão com panela", "240 × 260", "normal · com vapor", "Fogãozinho branco e rosa com forno e botões lilás, panela rosa em cima. Vapor: fiozinhos de vapor e um coração subindo. Sem chama.", ["fogao", "fogao_vapor"]),
    ("Pia", "260 × 200", None, "Bancada de madeira com cuba branca e torneira prateada com registro de coração. Tampo PLANO.", ["pia"]),
    ("Mesa com toalha xadrez", "420 × 200", None, "Mesa de madeira com toalha xadrez vermelho-rosado e branca. Tampo PLANO para pratos e comidinhas.", ["mesa"]),
    ("Cadeira de coração", "110 × 230", None, "Cadeira de madeira com coração vazado no encosto; o jogo usa quatro.", ["cadeira"]),
    ("Pratos", "60 × 30", "sujo · limpo", "Prato branco. Sujo: manchinhas de comida. Limpo: brilha.", ["prato_sujo", "prato_limpo"]),
    ("Comidinhas de gente", "xícara 40 × 36 · maçã 30 × 32 · banana 50 × 30 · leite 30 × 44 · sanduíche 50 × 34", None, "Só para a Catarina e a Carol (GDD, seção 9).", ["xicara", "maca", "banana", "copo_leite", "sanduiche"]),
    ("Tigelas dos bichos", "80 × 40", "vazia · cheia (cão, gato, Lumi)", "Tigela rosa com biscoitos de coração, lilás com peixinho e cor de mel com cenoura e maçã.", ["tigela_cao_vazia", "tigela_cao_cheia", "tigela_gato_vazia", "tigela_gato_cheia", "tigela_lumi_vazia", "tigela_lumi_cheia"]),
    ("Vaso de flores", "70 × 90", None, "Vaso rosa com flores amarelas, para enfeitar a mesa.", ["vaso_flores"]),
    ("Porta e plaquinha", "porta 170 × 350 · placa 70 × 60", "fechada · aberta", "A mesma porta da sala; plaquinha com a casinha (volta para a sala).", ["porta_fechada", "porta_aberta", "placa_casa"]),
]

# Como o cenário entra no protótipo (ver para_jogo.py). "objetos" são peças que dá para pegar.
JOGO = {
    "interativos": {
        "porta_sala": {"estados": ["porta_fechada", "porta_aberta"], "x": 60, "y": 250, "leva": "sala", "chegada": 145, "estado": 0},
        "geladeira": {"estados": ["geladeira_fechada", "geladeira_aberta"], "x": 300, "y": 170, "repoe": True,
                      "prateleiras": [[334, 498, 300], [334, 498, 400], [334, 498, 490], [334, 498, 574]]},
        "fogao": {"estados": ["fogao", "fogao_vapor"], "x": 600, "y": 340},
        "prato_pia": {"estados": ["prato_sujo", "prato_limpo"], "x": 1240, "y": 420},
        "tigela_cao": {"estados": ["tigela_cao_vazia", "tigela_cao_cheia"], "x": 700, "y": 760},
        "tigela_gato": {"estados": ["tigela_gato_vazia", "tigela_gato_cheia"], "x": 800, "y": 760},
        "tigela_lumi": {"estados": ["tigela_lumi_vazia", "tigela_lumi_cheia"], "x": 900, "y": 760},
    },
    "objetos": ["xicara", "sanduiche"],
    # comidinhas guardadas na geladeira (aparecem quando ela abre): [peça, x do meio, y da base]
    "dentro": {"geladeira": [["maca", 365, 300], ["banana", 445, 300], ["copo_leite", 365, 400], ["queijo", 450, 400], ["cenoura", 410, 490]]},
    "moveis": ["cadeira"],
    "lugares": [],
    "superficies": [[850, 1190, 438], [1590, 1960, 556]],
}

if __name__ == "__main__":
    pr, le = textos("cozinha", "Cozinha da Fazenda", "C04",
                    "É uma cozinha rústica e rosa: geladeira lilás, mesa com toalha xadrez e cadeiras de coração, panelas penduradas.",
                    " e a colagem `arte/conceito/colagem_cenarios/colagem_cozinha.png` (só o clima: o jogo é visto DE FRENTE)",
                    "2200 × 900, chão a partir de y = 600", TABELA,
                    ordem="\nGere primeiro a geladeira (os dois estados), a mesa e a cadeira.\nComida de gente só para a Catarina e a Carol; bichos só com o petisco deles. Fogão sem fogo.\n")
    gerar_cenario("cozinha", P, W, H, POS, "C04 Cozinha da Fazenda · Catarina = 300 px · chão a partir de y = 600 · tela 2200 × 900", pr, le)
