"""C13 Casinha de madeira (proposta para as criadoras: lojinha ou consultório de bichos).

Uso: python3 ferramentas/cenario2d/casinha.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import ceu_morros, cerca, grama_fundo, arvore_simples, plaquinha  # noqa: E402

W, H, CHAO = 2200, 900, 600
P = {}


def fundo():
    rnd = random.Random(71)
    s, defs = ceu_morros(W, H, CHAO, rnd)
    s += f'<g transform="translate(1820,160)">{arvore_simples(340, 460, C["verde"], C["rosa"], 10)}</g>'
    s += cerca(W, CHAO)
    s += grama_fundo(W, H, CHAO, rnd, n_flores=90)
    return svg(W, H, s, defs)


P["fundo"] = fundo()


def casinha():
    w, h = 560, 480
    # parede da frente com o vão da janela VAZADO (transparente): quem está dentro aparece por ele
    s = path("M48,120 L512,120 Q520,120 520,128 L520,476 L40,476 L40,128 Q40,120 48,120 Z M110,190 L110,360 L450,360 L450,190 Z",
             C["madeira_clara"], 'stroke-width="4" fill-rule="evenodd"')
    for y in range(150, 476, 32):
        if 190 < y < 360:
            s += path(f"M44,{y} L108,{y} M452,{y} L516,{y}", extra='stroke-width="1.5" opacity="0.35"')
        else:
            s += path(f"M44,{y} L516,{y}", extra='stroke-width="1.5" opacity="0.35"')
    s += path("M10,130 L280,10 L550,130 Z", C["rosa_chiclete"], 'stroke-width="4"')
    s += path("M10,130 L280,10 L550,130", extra=f'stroke-width="12" stroke="{C["madeira_esc"]}"')
    s += circ(280, 80, 26, C["branco"], 'stroke-width="3"') + coracao(280, 82, 13, C["rosa_forte"])
    # janela-balcão (vão) — o balcão é a peça "balcao"
    s += rr(110, 190, 340, 170, 6, "none", 'stroke-width="6"')
    # porta lateral
    s += rr(462, 300, 50, 176, 6, C["lilas"], 'stroke-width="3"') + circ(472, 390, 4, C["dourado"], 'stroke-width="1.5"')
    s += rr(36, 466, 488, 12, 4, C["madeira_esc"], 'stroke-width="3"')
    for x in (70, 420):
        s += flor(x, 470, 10, C["rosa"], C["amarelo"])
    return svg(w, h, s)


P["casinha"] = casinha()


def casinha_interior():
    w, h = 560, 480
    s = rr(60, 150, 440, 320, 4, "#9a6e7c", 'stroke-width="3"')
    for x in range(80, 500, 40):
        s += path(f"M{x},152 L{x},468", extra='stroke-width="1.5" opacity="0.3"')
    s += rr(60, 400, 440, 70, 0, "#7d5563", 'stroke-width="3"')
    return svg(w, h, s)


P["casinha_interior"] = casinha_interior()


def prateleira_fundo():
    w, h = 300, 130
    s = rr(10, 50, 280, 12, 4, C["madeira"], 'stroke-width="2.5"') + rr(10, 116, 280, 12, 4, C["madeira"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["prateleira"] = prateleira_fundo()


def potinho(cor):
    return svg(30, 40, rr(5, 12, 20, 26, 6, cor, 'stroke-width="2.2"') + rr(3, 6, 24, 9, 3, C["branco"], 'stroke-width="2"') + coracao(15, 25, 4, C["branco"], 'stroke-width="1.2"'))


P["potinho_rosa"] = potinho(C["rosa_chiclete"])
P["potinho_lilas"] = potinho(C["lilas"])
P["potinho_amarelo"] = potinho(C["amarelo"])
P["balcao"] = svg(380, 60, rr(4, 4, 372, 24, 8, C["madeira"], 'stroke-width="3.5"') + rr(30, 28, 320, 28, 0, "none", 'stroke="none"') +
                  path("M40,28 L60,56 M340,28 L320,56", extra='stroke-width="6"'))


def toldo(aberto):
    w, h = 440, 130
    s = rr(0, 2, 440, 14, 5, C["madeira_esc"], 'stroke-width="3"')
    n = 8
    alt = 110 if aberto else 40
    for i in range(n):
        x = 6 + i * 53.5
        cor = C["rosa_chiclete"] if i % 2 == 0 else C["branco"]
        s += path(f"M{x},14 L{x+53.5},14 L{x+53.5},{alt} Q{x+26.75},{alt+16} {x},{alt} Z", cor, 'stroke-width="2.5"')
    return svg(w, h, s)


P["toldo_aberto"] = toldo(True)
P["toldo_fechado"] = toldo(False)


def caixa_registradora(plim):
    w, h = 90, 80
    s = ""
    if plim:
        s += estrela(14, 14, 8, C["amarelo"], 4, 'stroke-width="1.5"') + estrela(78, 10, 6, C["amarelo"], 4, 'stroke-width="1.5"')
        s += rr(22, 50, 46, 14, 3, C["madeira_clara"], 'stroke-width="2"')
    s += path("M10,40 L80,40 L84,74 L6,74 Z", C["rosa"], 'stroke-width="2.5"') + rr(24, 14, 42, 26, 5, C["lilas"], 'stroke-width="2.5"')
    s += rr(30, 20, 30, 12, 2, "#dff4e5", 'stroke-width="1.5"')
    for x in (22, 36, 50, 64):
        s += circ(x + 2, 52, 4, C["branco"], 'stroke-width="1.5"')
    s += coracao(45, 66, 4, C["rosa_forte"], 'stroke-width="1.2"')
    return svg(w, h, s)


P["caixa_registradora"] = caixa_registradora(False)
P["caixa_registradora_plim"] = caixa_registradora(True)


def maleta(aberta):
    w, h = 110, 90
    s = path("M38,22 L38,10 L72,10 L72,22", extra='stroke-width="5"')
    if aberta:
        s += path("M8,40 L102,40 L94,8 L16,8 Z", "#f6f0f4", 'stroke-width="2.5"')
        s += path("M40,30 q-10,-14 6,-16 q18,0 8,18", extra=f'stroke="{C["azul"]}" stroke-width="3"') + rr(68, 18, 22, 10, 3, C["amarelo"], 'stroke-width="1.5"')
    s += rr(8, 30 if aberta else 20, 94, 58 if aberta else 68, 10, C["branco"], 'stroke-width="3"')
    s += rr(44, 48, 22, 22, 2, C["rosa_forte"], 'stroke="none"') + rr(49, 43, 12, 32, 2, C["rosa_forte"], 'stroke="none"')
    s += rr(38, 38, 34, 4, 2, "none", 'stroke="none"')
    return svg(w, h, s)


P["maleta_fechada"] = maleta(False)
P["maleta_aberta"] = maleta(True)
P["estetoscopio"] = svg(70, 60, path("M14,6 Q4,40 30,42 Q56,40 46,6", extra=f'stroke="{C["lilas"]}" stroke-width="5"') +
                        path("M30,42 L30,48 Q30,56 42,54", extra='stroke-width="3"') + circ(48, 52, 7, C["cinza"], 'stroke-width="2.5"') +
                        circ(14, 6, 4, C["roxo"], 'stroke-width="1.5"') + circ(46, 6, 4, C["roxo"], 'stroke-width="1.5"'))
P["coracao_batendo"] = svg(40, 36, coracao(20, 18, 16, C["rosa_forte"], 'stroke-width="2.5"') + path("M6,18 L14,18 L17,12 L21,24 L24,18 L34,18", extra=f'stroke="{C["branco"]}" stroke-width="2"'))
P["cadeirinha"] = svg(80, 120, rr(12, 6, 56, 60, 12, C["madeira"], 'stroke-width="3"') + coracao(40, 34, 10, C["rosa"], 'stroke-width="2"') +
                      rr(6, 62, 68, 16, 6, C["rosa"], 'stroke-width="3"') + rr(12, 78, 9, 40, 3, C["madeira_esc"], 'stroke-width="2"') + rr(59, 78, 9, 40, 3, C["madeira_esc"], 'stroke-width="2"'))
P["placa_pata"] = plaquinha("pata", 90, 80)
P["placa_cesta"] = svg(90, 80, path("M33,4 L45,0 L57,4", extra='stroke-width="2"') + rr(3, 6, 84, 70, 12, C["madeira_clara"], 'stroke-width="3"') +
                       path("M28,36 Q45,14 62,36", extra='stroke-width="3"') + path("M24,36 L66,36 L60,62 L30,62 Z", C["mel"], 'stroke-width="2.5"'))

POS = [("fundo", 0, 0), ("casinha_interior", 780, 130), ("prateleira", 910, 300), ("potinho_rosa", 940, 310), ("potinho_lilas", 990, 310), ("potinho_amarelo", 1040, 310),
       ("maleta_aberta", 1120, 268), ("@catarina", 1060, 600), ("casinha", 780, 130),
       ("toldo_aberto", 840, 222), ("balcao", 870, 480), ("caixa_registradora_plim", 920, 410),
       ("estetoscopio", 1060, 430), ("placa_pata", 1015, 150), ("cadeirinha", 1400, 480),
       ("@catarina", 1560, 860)]

TABELA = [
    ("Fundo do gramado", "2200 × 900", None, "Gramado com muitas flores, cerca branca, uma árvore florida, céu e morros. SEM a casinha.", ["fundo"]),
    ("Casinha de madeira", "560 × 480", None, "Casinha de brincar de madeira clara com telhado rosa, coração no frontão, porta lateral lilás e uma grande janela-balcão na frente com o vão TRANSPARENTE (a Catarina aparece por ele, com o interior atrás). SEM toldo, balcão e objetos.", ["casinha"]),
    ("Interior da casinha", "560 × 480", None, "Fundo de dentro da casinha (madeira mais escura e aconchegante). Fica ATRÁS de quem está dentro e aparece pela janela.", ["casinha_interior"]),
    ("Balcão", "380 × 60", None, "Tábua de madeira com mãos-francesas, PLANA, na base da janela: apoia os itens para vender ou atender.", ["balcao"]),
    ("Toldo listrado", "440 × 130", "aberto · fechado", "Toldo rosa e branco sobre a janela. Fechado: enrolado e curto.", ["toldo_aberto", "toldo_fechado"]),
    ("Prateleira e potinhos", "prateleira 300 × 130 · potinho 30 × 40", "rosa · lilás · amarelo", "Prateleira de duas tábuas VAZIA e potinhos com tampa branca e coração.", ["prateleira", "potinho_rosa", "potinho_lilas", "potinho_amarelo"]),
    ("Caixinha registradora", "90 × 80", "normal · plim", "Caixa registradora de brinquedo rosa e lilás com botões e coração; plim: a gavetinha abre com estrelinhas.", ["caixa_registradora", "caixa_registradora_plim"]),
    ("Maleta de veterinário", "110 × 90", "fechada · aberta", "Maleta branca de brinquedo com cruz rosa; aberta mostra o estetoscópio e um curativo.", ["maleta_fechada", "maleta_aberta"]),
    ("Estetoscópio e coração", "estetoscópio 70 × 60 · coração 40 × 36", None, "Estetoscópio de brinquedo lilás; coração batendo que aparece sobre o bicho.", ["estetoscopio", "coracao_batendo"]),
    ("Cadeirinha", "80 × 120", None, "Cadeirinha de madeira com assento rosa; senta 1.", ["cadeirinha"]),
    ("Plaquinhas", "90 × 80", "consultório · lojinha", "Placa com patinha (consultório de bichos) ou com cestinha (lojinha), sem letras.", ["placa_pata", "placa_cesta"]),
]

if __name__ == "__main__":
    pr, le = textos("casinha", "Casinha de madeira", "C13",
                    "É uma casinha de brincar no chão, com janela-balcão, que vira lojinha ou consultório de bichinhos de faz de conta.",
                    "", "2200 × 900, chão a partir de y = 600", TABELA,
                    aviso="\n**Proposta:** lojinha, consultório de bichos ou outra brincadeira ainda precisa da decisão das criadoras. As peças servem para as duas ideias.\n")
    gerar_cenario("casinha", P, W, H, POS, "C13 Casinha de madeira (proposta) · Catarina = 300 px · chão a partir de y = 600 · tela 2200 × 900", pr, le)
