"""C06 Quarto da Carol (proposta para validar com as criadoras): peças 2D, layout e prompts 3D.

Uso: python3 ferramentas/cenario2d/quarto_carol.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import porta_casa, plaquinha, planta_vaso, janela_paisagem, parede_interna  # noqa: E402

W, H, CHAO = 2200, 900, 600
P = {}


def fundo():
    s = parede_interna(W, H, CHAO, "#fbe6f0", "#f4e4fb", listras=True, vigas=True)
    s += janela_paisagem(1500, 130, 280, 200, C["lilas"])
    # quadros da família (só desenhos: corações, flor, ferradura)
    for x, y, w, h, des in [(520, 150, 110, 130, "coracao"), (660, 180, 90, 90, "flor"), (1960, 160, 120, 100, "ferradura")]:
        s += rr(x, y, w, h, 6, C["madeira"], 'stroke-width="3.5"') + rr(x + 10, y + 10, w - 20, h - 20, 3, C["creme"], 'stroke-width="2"')
        cx, cy = x + w / 2, y + h / 2
        if des == "coracao":
            s += coracao(cx, cy, 22, C["rosa_chiclete"])
        elif des == "flor":
            s += flor(cx, cy, 12, C["lilas"], C["rosa_forte"])
        else:
            s += path(f"M{cx-18},{cy+22} L{cx-21},{cy} A21,21 0 0 1 {cx+21},{cy} L{cx+18},{cy+22} L{cx+8},{cy+22} L{cx+9},{cy} A9,9 0 0 0 {cx-9},{cy} L{cx-8},{cy+22} Z", C["dourado"], 'stroke-width="2.5"')
    return svg(W, H, s)


P["fundo"] = fundo()


def cama():
    w, h = 620, 330
    s = rr(10, 20, 600, 230, 24, C["madeira"], 'stroke-width="4"')              # cabeceira
    s += path("M310,214 C150,170 120,40 230,30 C280,26 300,60 310,80 C320,60 340,26 390,30 C500,40 470,170 310,214 Z", C["rosa"], 'stroke-width="4"')
    for x, y in [(240, 80), (380, 80), (310, 140), (260, 130), (360, 130)]:
        s += circ(x, y, 3, C["rosa_forte"], 'stroke="none"')
    s += rr(20, 196, 580, 74, 20, C["branco"], 'stroke-width="3.5"')            # colchão (plano)
    s += rr(70, 172, 130, 50, 22, C["branco"], 'stroke-width="3"') + rr(420, 172, 130, 50, 22, C["branco"], 'stroke-width="3"')
    s += rr(6, 250, 608, 50, 12, C["madeira_esc"], 'stroke-width="3.5"')
    s += rr(24, 296, 26, 32, 5, C["madeira_esc"]) + rr(570, 296, 26, 32, 5, C["madeira_esc"])
    return svg(w, h, s)


P["cama"] = cama()


def cobertor(cobrindo):
    w, h = 560, 110
    if cobrindo:
        s = path("M6,30 Q280,-10 554,30 L548,104 Q280,90 12,104 Z", C["lilas"], 'stroke-width="3.5"')
        s += path("M6,30 Q280,-10 554,30 L552,48 Q280,10 8,48 Z", C["branco"], 'stroke-width="2.5"')
    else:
        s = path("M330,60 Q440,40 554,52 L548,104 Q440,96 336,104 Z", C["lilas"], 'stroke-width="3.5"')
        s += path("M330,60 Q440,40 554,52 L552,66 Q440,54 332,74 Z", C["branco"], 'stroke-width="2.5"')
    for x in range(60 if cobrindo else 380, 540, 70):
        s += coracao(x, 74, 9, C["rosa"], 'stroke-width="2"')
    return svg(w, h, s)


P["cobertor_coberto"] = cobertor(True)
P["cobertor_dobrado"] = cobertor(False)
P["travesseiro"] = svg(130, 60, rr(4, 6, 122, 48, 22, C["rosa_claro"], 'stroke-width="3"') + coracao(65, 30, 9, C["rosa"], 'stroke-width="2"'))


def criado_mudo(aberto=False):
    w, h = 130, 150
    s = rr(10, 20, 110, 110, 8, C["madeira"], 'stroke-width="3.5"') + rr(4, 10, 122, 16, 6, C["madeira_clara"], 'stroke-width="3"')
    if aberto:  # gaveta de cima puxada: aparece o fundo escuro e a frente desce um pouco
        s += rr(18, 36, 94, 16, 3, "#6b4630", 'stroke-width="2.5"') + rr(16, 46, 98, 34, 5, C["madeira_clara"], 'stroke-width="2.8"')
        s += circ(65, 63, 4, C["dourado"], 'stroke-width="2"') + rr(22, 84, 86, 34, 5, C["madeira_clara"], 'stroke-width="2.5"') + circ(65, 101, 4, C["dourado"], 'stroke-width="2"')
        s += rr(18, 128, 14, 20, 3, C["madeira_esc"]) + rr(98, 128, 14, 20, 3, C["madeira_esc"])
        return svg(w, h, s)
    s += rr(22, 40, 86, 34, 5, C["madeira_clara"], 'stroke-width="2.5"') + rr(22, 84, 86, 34, 5, C["madeira_clara"], 'stroke-width="2.5"')
    s += circ(65, 57, 4, C["dourado"], 'stroke-width="2"') + circ(65, 101, 4, C["dourado"], 'stroke-width="2"')
    s += rr(18, 128, 14, 20, 3, C["madeira_esc"]) + rr(98, 128, 14, 20, 3, C["madeira_esc"])
    return svg(w, h, s)


P["criado_mudo"] = criado_mudo()
P["criado_mudo_aberto"] = criado_mudo(True)
P["laco"] = svg(50, 30, path("M25,15 L6,4 Q2,15 6,26 Z", C["rosa_forte"], 'stroke-width="2.2"') + path("M25,15 L44,4 Q48,15 44,26 Z", C["rosa_forte"], 'stroke-width="2.2"') + circ(25, 15, 6, C["rosa_chiclete"], 'stroke-width="2"'))
P["livrinho"] = svg(40, 32, rr(4, 4, 32, 26, 4, C["lilas"], 'stroke-width="2.3"') + rr(31, 6, 4, 22, 2, C["branco"], 'stroke-width="1.2"') + estrela(18, 17, 6, C["amarelo"], 5, 'stroke-width="1.3"'))


def abajur_mesa(aceso):
    w, h = 80, 110
    s = ""
    if aceso:
        s += circ(40, 40, 38, "#ffe7a3", 'stroke="none" opacity="0.6"')
    s += ell(40, 100, 22, 8, C["lilas"], 'stroke-width="2.5"') + rr(36, 56, 8, 44, 3, C["lilas"], 'stroke-width="2"')
    s += path("M14,60 L66,60 L56,16 L24,16 Z", "#fff2c4" if aceso else C["rosa_claro"], 'stroke-width="3"')
    s += coracao(40, 38, 7, C["rosa_forte"], 'stroke-width="1.8"')
    return svg(w, h, s)


P["abajur_apagado"] = abajur_mesa(False)
P["abajur_aceso"] = abajur_mesa(True)


def guarda_roupa(aberto):
    w, h = 300, 420
    s = rr(10, 20, 280, 380, 10, C["madeira"], 'stroke-width="4"')
    s += path("M4,26 Q150,-6 296,26 L296,36 L4,36 Z", C["madeira_esc"], 'stroke-width="3"')
    s += rr(20, 396, 30, 22, 4, C["madeira_esc"]) + rr(250, 396, 30, 22, 4, C["madeira_esc"])
    if not aberto:
        s += rr(24, 46, 124, 340, 8, C["rosa_claro"], 'stroke-width="3"') + rr(152, 46, 124, 340, 8, C["rosa_claro"], 'stroke-width="3"')
        s += coracao(86, 120, 16, C["rosa"], 'stroke-width="2.5"') + coracao(214, 120, 16, C["rosa"], 'stroke-width="2.5"')
        s += circ(136, 220, 6, C["dourado"]) + circ(164, 220, 6, C["dourado"])
    else:
        s += rr(24, 46, 252, 340, 6, "#8d6178", 'stroke-width="3"')
        s += path("M34,80 L266,80", extra='stroke-width="5"')
        for x, c in [(70, C["rosa_chiclete"]), (120, C["lilas"]), (170, C["azul"]), (220, C["amarelo"])]:
            s += path(f"M{x},80 l0,10", extra='stroke-width="2.5"')
            s += path(f"M{x-24},96 L{x+24},96 L{x+30},210 L{x-30},210 Z", c, 'stroke-width="2.5"')
        s += rr(34, 300, 232, 12, 3, C["madeira"], 'stroke-width="2.5"')
        for x in (60, 110, 160, 210):
            s += ell(x + 10, 296, 18, 8, C["madeira_esc"], 'stroke-width="2"')
        # portas abertas para os lados (finas)
        s += path("M24,46 L-2,30 L-2,400 L24,386 Z", C["rosa_claro"], 'stroke-width="3"')
        s += path("M276,46 L302,30 L302,400 L276,386 Z", C["rosa_claro"], 'stroke-width="3"')
    return svg(w, h, s)


P["guarda_roupa_fechado"] = guarda_roupa(False)
P["guarda_roupa_aberto"] = guarda_roupa(True)


def penteadeira(brilho):
    w, h = 260, 360
    s = ""
    if brilho:
        s += ell(130, 110, 100, 110, "#fff4c9", 'stroke="none" opacity="0.6"')
    s += ell(130, 110, 80, 96, C["lilas"], 'stroke-width="4"') + ell(130, 110, 64, 80, "#e7f4ff", 'stroke-width="3"')
    s += path("M96,70 q14,-16 30,-6", extra=f'stroke="{C["branco"]}" stroke-width="5"')
    if brilho:
        for x, y, r in [(90, 80, 10), (170, 140, 12), (150, 60, 8)]:
            s += estrela(x, y, r, C["branco"], 4, 'stroke-width="1.5"')
    s += coracao(130, 18, 12, C["rosa_forte"], 'stroke-width="2.5"')
    s += rr(10, 200, 240, 24, 8, C["madeira_clara"], 'stroke-width="3.5"')   # tampo
    s += rr(20, 224, 220, 70, 8, C["madeira"], 'stroke-width="3.5"')
    s += rr(36, 236, 84, 44, 5, C["madeira_clara"], 'stroke-width="2.5"') + rr(140, 236, 84, 44, 5, C["madeira_clara"], 'stroke-width="2.5"')
    s += rr(28, 294, 14, 64, 4, C["madeira_esc"]) + rr(218, 294, 14, 64, 4, C["madeira_esc"])
    return svg(w, h, s)


P["penteadeira"] = penteadeira(False)
P["penteadeira_brilho"] = penteadeira(True)
P["banquinho"] = svg(100, 100, ell(50, 28, 44, 20, C["rosa"], 'stroke-width="3"') + rr(6, 26, 88, 16, 8, C["rosa"], 'stroke-width="3"') +
                     rr(18, 40, 10, 58, 3, C["madeira_esc"], 'stroke-width="2.5"') + rr(72, 40, 10, 58, 3, C["madeira_esc"], 'stroke-width="2.5"') +
                     coracao(50, 26, 7, C["rosa_forte"], 'stroke-width="1.8"'))
P["escova_cabelo"] = svg(80, 40, rr(4, 14, 44, 14, 7, C["lilas"], 'stroke-width="2.5"') + ell(60, 21, 16, 17, C["rosa_chiclete"], 'stroke-width="2.5"') +
                         ell(60, 21, 10, 11, C["branco"], 'stroke-width="1.5"') + coracao(24, 21, 4, C["branco"], 'stroke-width="1.2"'))


def tapete():
    w, h = 520, 120
    s = ell(260, 60, 256, 56, C["lilas_claro"], 'stroke-width="3.5"') + ell(260, 60, 220, 44, C["rosa_claro"], 'stroke-width="2.5"')
    for x in range(80, 460, 60):
        s += flor(x, 60, 7, C["lilas"], C["amarelo"])
    return svg(w, h, s)


P["tapete"] = tapete()


def porta_retrato(desenho):
    s = rr(4, 4, 52, 56, 6, C["dourado"], 'stroke-width="2.5"') + rr(11, 11, 38, 42, 3, C["ceu"], 'stroke-width="2"')
    if desenho == "coracao":
        s += coracao(30, 32, 10, C["rosa_forte"], 'stroke-width="2"')
    else:
        s += path("M11,50 Q30,34 49,46 L49,53 L11,53 Z", C["verde"], 'stroke-width="1.5"') + circ(38, 22, 5, C["amarelo"], 'stroke-width="1.5"')
    s += path("M22,60 L18,64 M38,60 L42,64", extra='stroke-width="2"')
    return svg(60, 66, s)


P["porta_retrato_coracao"] = porta_retrato("coracao")
P["porta_retrato_paisagem"] = porta_retrato("paisagem")
P["planta"] = planta_vaso(90, 130, C["lilas"])
P["porta_fechada"] = porta_casa(False, "#e9c3a0")
P["porta_aberta"] = porta_casa(True, "#e9c3a0")
P["placa_casa"] = plaquinha("casa")

POS = [("fundo", 0, 0), ("porta_fechada", 50, 250), ("placa_casa", 100, 180),
       ("guarda_roupa_fechado", 260, 200), ("planta", 600, 490),
       ("criado_mudo", 720, 470), ("abajur_aceso", 745, 372), ("porta_retrato_coracao", 830, 410),
       ("cama", 860, 290), ("travesseiro", 920, 455), ("travesseiro", 1290, 455), ("cobertor_dobrado", 890, 505),
       ("criado_mudo", 1490, 470), ("abajur_apagado", 1515, 372), ("porta_retrato_paisagem", 1590, 410),
       ("penteadeira", 1790, 260), ("escova_cabelo", 1830, 430), ("banquinho", 1870, 560),
       ("tapete", 900, 720), ("@catarina", 1100, 520), ("@catarina", 1640, 860)]

TABELA = [
    ("Fundo do quarto", "2200 × 900", None, "Parede rosa-clara com listras lilás bem suaves, vigas de madeira no alto, janela com cortina lilás e vista da fazenda, três quadrinhos da família (coração, flor e ferradura), rodapé e piso de madeira. SEM porta e sem móveis.", ["fundo"]),
    ("Cama de casal", "620 × 330", None, "Cabeceira acolchoada rosa em forma de coração sobre moldura de madeira. Colchão PLANO e branco, a cerca de 130 px do chão, com pelo menos 560 px de comprimento: deitam 3 (Carol, Catarina e Bob). Sem cobertor (é a peça 3).", ["cama"]),
    ("Cobertor", "560 × 110", "cobrindo · dobrado", "Cobertor lilás com coraçõezinhos e barra branca. Cobrindo: estendido sobre o colchão. Dobrado: só no pé da cama.", ["cobertor_coberto", "cobertor_dobrado"]),
    ("Travesseiro", "130 × 60", None, "Travesseiro rosa-claro fofinho com coração.", ["travesseiro"]),
    ("Criado-mudo", "130 × 150", None, "Mesinha de cabeceira de madeira com duas gavetas, tampo PLANO.", ["criado_mudo"]),
    ("Abajur de mesa", "80 × 110", "apagado · aceso", "Abajur lilás com cúpula clara e coração. Apagado deixa o quarto na hora de dormir.", ["abajur_apagado", "abajur_aceso"]),
    ("Guarda-roupa", "300 × 420", "fechado · aberto", "Guarda-roupa de madeira com portas rosa-claro e corações. Aberto: cabide com quatro vestidos/blusas coloridos e sapatos embaixo.", ["guarda_roupa_fechado", "guarda_roupa_aberto"]),
    ("Penteadeira com espelho", "260 × 360", "normal · brilho", "Espelho oval lilás com coração em cima, tampo de madeira e gavetas. Brilho: o espelho reluz com estrelinhas.", ["penteadeira", "penteadeira_brilho"]),
    ("Banquinho", "100 × 100", None, "Banquinho redondo com assento rosa, para sentar 1 na penteadeira.", ["banquinho"]),
    ("Escova de cabelo", "80 × 40", None, "Escova rosa e lilás com coração; na Catarina, as tranças brilham.", ["escova_cabelo"]),
    ("Tapete", "520 × 120", None, "Tapete oval lilás e rosa com florzinhas, visto de cima e de leve.", ["tapete"]),
    ("Porta-retratos", "60 × 66", "coração · paisagem", "Moldurinha dourada com um coração ou uma paisagem (sem pessoas).", ["porta_retrato_coracao", "porta_retrato_paisagem"]),
    ("Planta", "90 × 130", None, "Planta de folhas largas num vaso lilás.", ["planta"]),
    ("Porta e plaquinha", "porta 170 × 350 · placa 70 × 60", "fechada · aberta", "A mesma porta das outras salas, num tom de madeira mais rosado; plaquinha com a casinha (volta para a sala).", ["porta_fechada", "porta_aberta", "placa_casa"]),
]

# Como o cenário entra no protótipo (ver para_jogo.py).
JOGO = {
    "interativos": {
        "porta_sala": {"estados": ["porta_fechada", "porta_aberta"], "x": 50, "y": 250, "leva": "sala", "chegada": 135},
        "gaveta_esq": {"estados": ["criado_mudo", "criado_mudo_aberto"], "x": 720, "y": 470, "prateleiras": [[742, 828, 516]]},
        "gaveta_dir": {"estados": ["criado_mudo", "criado_mudo_aberto"], "x": 1490, "y": 470, "prateleiras": [[1512, 1598, 516]]},
        "guarda_roupa": {"estados": ["guarda_roupa_fechado", "guarda_roupa_aberto"], "x": 260, "y": 200},
        "abajur_esq": {"estados": ["abajur_apagado", "abajur_aceso"], "x": 745, "y": 372},
        "abajur_dir": {"estados": ["abajur_apagado", "abajur_aceso"], "x": 1515, "y": 372},
        "penteadeira": {"estados": ["penteadeira", "penteadeira_brilho"], "x": 1790, "y": 260},
        "cobertor": {"estados": ["cobertor_dobrado", "cobertor_coberto"], "x": 890, "y": 505},
    },
    "objetos": ["escova_cabelo"],
    "lugares": [{"id": "cama_carol", "area": [880, 330, 580, 170], "spots": [[1170, 520], [1050, 524]], "pose": "deitar"}],
    # surpresas guardadas nas gavetas dos criados-mudos
    "dentro": {"gaveta_esq": [["laco", 785, 516]], "gaveta_dir": [["livrinho", 1555, 516]]},
    "superficies": [[1800, 2040, 470], [880, 1460, 515]],
}

if __name__ == "__main__":
    pr, le = textos("quarto_carol", "Quarto da Carol", "C06",
                    "É o quarto da mãe, a Carol: calmo, rosa-claro e lilás com madeira, com cama de casal de cabeceira de coração, onde a Catarina dorme com a mãe quando quiser.",
                    "", "2200 × 900, chão a partir de y = 600", TABELA,
                    aviso="\n**Proposta:** cores, cama e objetos ainda precisam da aprovação das criadoras (pendência do GDD). Ajuste a tabela antes de gerar.\n",
                    ordem="\nGere primeiro a cama com o cobertor e os travesseiros: é onde a Carol, a Catarina e o Bob deitam juntos.\n")
    gerar_cenario("quarto_carol", P, W, H, POS, "C06 Quarto da Carol (proposta) · Catarina = 300 px · chão a partir de y = 600 · tela 2200 × 900", pr, le)
