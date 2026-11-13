"""C02 Sede da Fazenda (fachada, varanda e deck): peças 2D provisórias, layout e prompts 3D.

Uso: python3 ferramentas/cenario2d/sede.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import porta_casa, ceu_morros, grama_fundo, arvore_simples, cerca  # noqa: E402

W, H, CHAO = 3000, 900, 600
P = {}


def janela_lilas(x, y, w=150, h=170):
    s = rr(x - 8, y - 8, w + 16, h + 16, 10, C["madeira"], 'stroke-width="3.5"') + rr(x, y, w, h, 6, "#dff1ff", 'stroke-width="2.5"')
    s += path(f"M{x+w/2},{y} L{x+w/2},{y+h} M{x},{y+h/2} L{x+w},{y+h/2}", extra='stroke-width="5"')
    s += rr(x - 30, y - 6, 26, h + 12, 4, C["lilas"], 'stroke-width="3"') + rr(x + w + 4, y - 6, 26, h + 12, 4, C["lilas"], 'stroke-width="3"')
    s += rr(x - 14, y + h + 8, w + 28, 26, 6, C["madeira_esc"], 'stroke-width="3"')
    for k in range(5):
        s += flor(x + 6 + k * (w - 12) / 4, y + h + 8, 9, C["rosa_chiclete"] if k % 2 else C["lilas"])
    return s


def fundo():
    rnd = random.Random(41)
    s, defs = ceu_morros(W, H, CHAO, rnd)
    s += f'<g transform="translate(40,160)">{arvore_simples(360, 440, C["verde"], C["rosa"], 4)}</g>'
    s += f'<g transform="translate(2790,300)">{arvore_simples(210, 300, C["verde"], C["rosa"], 5)}</g>'
    s += cerca(W, CHAO, 0, 400) + cerca(W, CHAO, 2830, W)
    # casa rosa (fachada) de x 420 a 1700
    x0, x1, base, topo = 420, 1700, CHAO, 170
    s += rr(x0, topo, x1 - x0, base - topo, 6, "#ffc6dc", 'stroke-width="4"')
    for y in range(topo + 40, base, 40):
        s += path(f"M{x0+4},{y} L{x1-4},{y}", extra='stroke-width="1.5" opacity="0.2"')
    s += path(f"M{x0-70},{topo+10} L{(x0+x1)/2},{topo-150} L{x1+70},{topo+10} Z", C["roxo"], 'stroke-width="4"')
    s += path(f"M{x0-70},{topo+10} L{(x0+x1)/2},{topo-150} L{x1+70},{topo+10}", extra=f'stroke-width="12" stroke="{C["madeira_esc"]}"')
    s += circ((x0 + x1) / 2, topo - 50, 36, C["madeira"], 'stroke-width="3.5"') + coracao((x0 + x1) / 2, topo - 48, 18, C["rosa_forte"])
    s += rr(1480, topo - 160, 70, 120, 4, C["vermelho_rosa"], 'stroke-width="3.5"')   # chaminé
    s += janela_lilas(500, 250) + janela_lilas(1440, 250)
    # varanda: piso, telhadinho e colunas
    s += rr(x0 + 120, base - 30, 1040, 34, 6, C["madeira"], 'stroke-width="3.5"')
    s += rr(x0 + 100, 205, 1080, 26, 8, C["madeira_esc"], 'stroke-width="3.5"')
    for x in (x0 + 140, x0 + 560, x0 + 720, x0 + 1140):
        s += rr(x - 12, 230, 24, base - 260, 5, C["madeira"], 'stroke-width="3"')
        s += flor(x, 260, 9, C["rosa"], C["amarelo"]) + flor(x + 4, 330, 8, C["lilas"], C["amarelo"])
    # deck à direita (de dia)
    dx0, dx1 = 1820, 2830
    s += rr(dx0, base - 50, dx1 - dx0, 54, 6, C["mel"], 'stroke-width="3.5"')
    for x in range(dx0 + 40, dx1, 50):
        s += path(f"M{x},{base-46} L{x},{base}", extra='stroke-width="1.5" opacity="0.4"')
    for x in (dx0 + 30, dx1 - 30):
        s += rr(x - 14, 180, 28, base - 230, 5, C["madeira"], 'stroke-width="3"')
    s += rr(dx0 - 20, 160, dx1 - dx0 + 40, 26, 8, C["madeira_esc"], 'stroke-width="3.5"')
    for x in range(dx0, dx1, 34):
        s += circ(x, 160 + (x % 3) * 5, 14, C["verde"], 'stroke-width="2.5"')
    for x in range(dx0 + 10, dx1, 44):
        s += flor(x, 156 + (x % 4) * 4, 8, C["rosa_chiclete"], C["amarelo"])
    # grade baixa do deck (fundo)
    s += rr(dx0, base - 120, dx1 - dx0, 12, 4, C["madeira"], 'stroke-width="2.5"')
    for x in range(dx0 + 10, dx1, 36):
        s += rr(x, base - 116, 10, 66, 3, C["madeira_clara"], 'stroke-width="2"')
    # grama e caminho de pedras
    s += grama_fundo(W, H, CHAO + 4, rnd)
    for i in range(7):
        x, y = 1060 - i * 18 + (i % 2) * 40, 640 + i * 38
        s += ell(x, y, 46, 15, "#e9e0d6", 'stroke-width="2.5"')
    return svg(W, H, s, defs)


P["fundo"] = fundo()
P["porta_frente_fechada"] = porta_casa(False, C["roxo"], 190, 360)
P["porta_frente_aberta"] = porta_casa(True, C["roxo"], 190, 360)


def rede(deitada):
    w, h = 460, 300
    s = rr(10, 20, 24, 278, 6, C["madeira"]) + rr(426, 20, 24, 278, 6, C["madeira"])
    s += path("M34,60 L80,120 M426,60 L380,120", extra='stroke-width="3"')
    s += path("M80,120 Q230,280 380,120 L380,128 Q230,210 80,128 Z", C["rosa_chiclete"], 'stroke-width="3.5"')
    for x in range(110, 360, 40):
        s += path(f"M{x},{128 + (x-80)*0.5 if x < 230 else 128 + (380-x)*0.5} l0,18", extra=f'stroke="{C["rosa_forte"]}" stroke-width="3"')
    s += path("M80,124 Q230,232 380,124", extra=f'stroke="{C["branco"]}" stroke-width="3" opacity="0.7"')
    s += rr(0, 290, 44, 10, 3, C["madeira_esc"]) + rr(416, 290, 44, 10, 3, C["madeira_esc"])
    return svg(w, h, s)


P["rede"] = rede(False)


def banco():
    w, h = 360, 150
    s = rr(20, 6, 320, 70, 14, C["madeira"], 'stroke-width="3.5"') + rr(10, 76, 340, 24, 8, C["madeira"], 'stroke-width="3.5"')
    for x in (40, 110, 180, 250):
        s += rr(x + 20, 18, 46, 44, 14, C["rosa"] if x % 20 else C["lilas_claro"], 'stroke-width="2.5"')
    s += rr(28, 100, 18, 48, 4, C["madeira_esc"]) + rr(314, 100, 18, 48, 4, C["madeira_esc"])
    return svg(w, h, s)


P["banco_varanda"] = banco()


def mesa_deck():
    w, h = 300, 150
    s = rr(40, 50, 18, 98, 4, C["madeira_esc"]) + rr(242, 50, 18, 98, 4, C["madeira_esc"])
    s += rr(6, 30, 288, 24, 8, C["madeira"], 'stroke-width="3.5"')
    return svg(w, h, s)


P["mesa_deck"] = mesa_deck()
P["cadeira_deck"] = svg(100, 200, rr(14, 6, 72, 104, 14, C["madeira"], 'stroke-width="3.5"') +
                        "".join(rr(24 + k * 18, 18, 10, 84, 4, C["madeira_clara"], 'stroke-width="2"') for k in range(3)) +
                        rr(6, 104, 88, 22, 8, C["madeira"], 'stroke-width="3.5"') + rr(14, 126, 12, 72, 4, C["madeira_esc"]) + rr(74, 126, 12, 72, 4, C["madeira_esc"]))


def vaso(estagio):
    w, h = 110, 160
    s = ""
    alt = {1: 30, 2: 60, 3: 80}[estagio]
    for dx in (-26, 0, 26):
        s += path(f"M{55+dx},100 L{55+dx},{100-alt}", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"')
        if estagio >= 2:
            r = 10 if estagio == 2 else 14
            s += flor(55 + dx, 100 - alt, r, C["rosa_chiclete"] if dx else C["lilas"], C["amarelo"])
        else:
            s += ell(55 + dx + 6, 100 - alt + 4, 8, 4, C["verde"], 'stroke-width="1.5"')
    if estagio == 3:
        s += estrela(18, 18, 9, C["branco"], 4, 'stroke-width="1.5"') + estrela(96, 30, 7, C["branco"], 4, 'stroke-width="1.5"')
    s += path("M14,96 L96,96 L84,158 L26,158 Z", C["madeira"], 'stroke-width="3"') + rr(8, 90, 94, 14, 5, C["madeira_esc"], 'stroke-width="3"')
    return svg(w, h, s)


P["vaso_1"] = vaso(1)
P["vaso_2"] = vaso(2)
P["vaso_3"] = vaso(3)


def regador(cheio):
    s = path("M52,22 L76,8 L78,14 L58,30 Z", C["rosa_chiclete"], 'stroke-width="2.5"') + ell(77, 10, 3, 5, C["rosa"], 'stroke-width="2"')
    s += rr(14, 18, 42, 34, 9, C["rosa"], 'stroke-width="2.5"') + path("M24,18 Q35,4 46,18", extra='stroke-width="3.5"')
    s += coracao(35, 35, 7, C["rosa_forte"], 'stroke-width="1.5"')
    if cheio:
        for x, y in [(74, 22), (69, 32), (78, 34)]:
            s += path(f"M{x},{y} q-2,4 0,6 q2,-2 0,-6 Z", C["agua"], 'stroke-width="1.2"')
    return svg(80, 55, s)


P["regador_vazio"] = regador(False)
P["regador_cheio"] = regador(True)


def varal_luzes(aceso):
    w, h = 740, 80
    s = path("M4,10 Q185,60 370,14 T736,10", extra='stroke-width="2.5"')
    for i in range(1, 15):
        x = i * 740 / 15
        import math
        y = 26 + 16 * math.sin(i * 0.85)
        if aceso:
            s += circ(round(x), round(y + 14), 16, "#fff1a8", 'stroke="none" opacity="0.6"')
        s += ell(round(x), round(y + 14), 8, 11, C["amarelo"] if aceso else "#e9e2d0", 'stroke-width="2"')
        s += rr(round(x) - 4, round(y), 8, 6, 2, C["cinza"], 'stroke-width="1.5"')
    return svg(w, h, s)


P["luzinhas_apagadas"] = varal_luzes(False)
P["luzinhas_acesas"] = varal_luzes(True)


def lanterna(acesa):
    w, h = 60, 100
    s = ""
    if acesa:
        s += circ(30, 58, 30, "#ffe08a", 'stroke="none" opacity="0.55"')
    s += path("M18,16 Q30,0 42,16", extra='stroke-width="3"') + rr(14, 16, 32, 8, 3, C["roxo"], 'stroke-width="2.5"')
    s += path("M16,24 L44,24 L48,84 L12,84 Z", "#fff1b3" if acesa else "#dde6ee", 'stroke-width="2.5"')
    s += coracao(30, 56, 8, C["laranja"] if acesa else C["cinza"], 'stroke-width="2"') + rr(8, 84, 44, 12, 4, C["roxo"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["lanterna_apagada"] = lanterna(False)
P["lanterna_acesa"] = lanterna(True)
P["bola"] = svg(60, 60, circ(30, 30, 27, C["amarelo"]) + path("M30,3 C15,15 15,45 30,57 C20,45 20,15 30,3 Z", C["rosa_chiclete"], 'stroke-width="2"') +
                path("M3,30 C15,20 45,20 57,30 C45,42 15,42 3,30 Z", C["lilas"], 'stroke-width="2"') + circ(30, 30, 27, "none", 'stroke-width="3"'))

POS = [("fundo", 0, 0),
       ("porta_frente_aberta", 965, 240),
       ("banco_varanda", 620, 425), ("vaso_3", 540, 418), ("vaso_2", 1210, 418),
       ("lanterna_acesa", 1160, 240), ("lanterna_apagada", 860, 240),
       ("luzinhas_acesas", 1830, 190), ("luzinhas_acesas", 2090, 186),
       ("rede", 1845, 290), ("cadeira_deck", 2340, 362), ("cadeira_deck", 2690, 362), ("mesa_deck", 2420, 410),
       ("vaso_1", 1700, 590), ("regador_cheio", 1640, 720), ("bola", 1450, 760),
       ("@catarina", 760, 570), ("@catarina", 1300, 860)]

TABELA = [
    ("Fundo da Sede", "3000 × 900", None, "Fachada da casa grande ROSA com telhado lilás, coração no frontão, duas janelas lilás com floreiras, varanda de madeira com colunas floridas; à direita, o deck de madeira com pergolado florido e gradinha (de DIA). Árvores, morros, céu, cerca e caminho de pedras. SEM porta, rede, banco, mesa, vasos e luzinhas.", ["fundo"]),
    ("Porta da frente", "190 × 360", "fechada · aberta", "Porta roxa arredondada no alto com moldura de madeira. Aberta: luz quente da sala. Leva para a Sala.", ["porta_frente_fechada", "porta_frente_aberta"]),
    ("Rede", "460 × 300", None, "Rede rosa com franjas, presa entre dois postes de madeira. Cabem 1 ou 2 deitados; o jogo faz a rede balançar.", ["rede"]),
    ("Banco da varanda", "360 × 150", None, "Banco de madeira com quatro almofadas rosa e lilás. Assento PLANO: sentam 3.", ["banco_varanda"]),
    ("Mesa e cadeira do deck", "mesa 300 × 150 · cadeira 100 × 200", None, "Mesa de madeira com tampo PLANO e cadeira de ripas; o jogo usa quatro cadeiras.", ["mesa_deck", "cadeira_deck"]),
    ("Vaso de flores", "110 × 160", "brotinho · flores · flores brilhando", "Vaso de madeira; ao regar, as flores crescem e brilham.", ["vaso_1", "vaso_2", "vaso_3"]),
    ("Regador", "80 × 55", "vazio · cheio", "O mesmo regador rosa da Plantação.", ["regador_vazio", "regador_cheio"]),
    ("Varal de luzinhas", "740 × 80", "apagado · aceso", "Fio com lampadinhas amarelas penduradas sob o pergolado do deck.", ["luzinhas_apagadas", "luzinhas_acesas"]),
    ("Lanterna da varanda", "60 × 100", "apagada · acesa", "Lanterna roxa com coração; acesa, luz quente.", ["lanterna_apagada", "lanterna_acesa"]),
    ("Bola", "60 × 60", None, "Bola com gomos coloridos; o Bob e a Nina brincam.", ["bola"]),
]

if __name__ == "__main__":
    pr, le = textos("sede", "Sede da Fazenda", "C02",
                    "É a casa grande e ROSA da família, com varanda florida e um deck com rede para descansar ao ar livre.",
                    " e o conceito `arte/conceito/cenarios_R01/02_casa_principal.png` (só o clima: a nossa casa é ROSA, não creme com telha)",
                    "3000 × 900, chão a partir de y = 600", TABELA,
                    ordem="\nGere primeiro a porta, a rede e o banco da varanda. Uma rede só. Deck de dia.\n")
    gerar_cenario("sede", P, W, H, POS, "C02 Sede: fachada, varanda e deck · Catarina = 300 px · chão a partir de y = 600 · tela 3000 × 900", pr, le)
