"""C03 Sala da Família: peças 2D provisórias, layout e prompts das peças 3D.

Uso: python3 ferramentas/cenario2d/sala.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, gerar_cenario, textos  # noqa: E402
from moveis import porta_casa, plaquinha, planta_vaso, planta_pendurada, janela_paisagem, parede_interna  # noqa: E402

W, H, CHAO = 2200, 900, 600
P = {}


def fundo():
    s = parede_interna(W, H, CHAO, "#ffe4ee", "#ffd9e8")
    s += janela_paisagem(1350, 110, 260, 190, C["rosa_chiclete"])
    s += planta_pendurada(1260, 40, 150) + planta_pendurada(1700, 40, 160)
    # quadro da fazenda (acima da estante)
    s += f'<g transform="translate(-1600,0)">'
    s += rr(1880, 120, 200, 140, 6, C["madeira"], 'stroke-width="4"') + rr(1894, 134, 172, 112, 2, C["ceu"])
    s += path("M1894,220 Q1960,190 2066,215 L2066,246 L1894,246 Z", C["verde"], 'stroke-width="2"')
    s += path("M1950,215 L1950,180 L1975,160 L2000,180 L2000,215 Z", C["vermelho_rosa"], 'stroke-width="2.5"')
    s += path("M1964,215 L1964,195 L1986,195 L1986,215", extra='stroke-width="2"')
    s += '</g>'
    return svg(W, H, s)


P["fundo"] = fundo()


def lareira():
    w, h = 420, 420
    rnd = random.Random(9)
    s = path(f"M60,{h-2} L80,40 L340,40 L360,{h-2} Z", "#d9cbbd", 'stroke-width="4"')
    for _ in range(46):
        x, y = rnd.uniform(90, 330), rnd.uniform(52, h - 20)
        s += ell(round(x), round(y), rnd.uniform(14, 22), rnd.uniform(9, 13), rnd.choice(["#cbbcab", "#e3d7ca", "#bfae9c"]), 'stroke-width="2"')
    s += rr(20, 200, 380, 30, 8, C["madeira"], 'stroke-width="3.5"')          # prateleira
    s += circ(210, 120, 44, C["rosa_claro"], 'stroke-width="4"') + coracao(210, 122, 26, C["rosa_chiclete"])
    s += path(f"M110,{h-2} L110,320 A100,90 0 0 1 310,320 L310,{h-2} Z", "#d9cbbd", 'stroke-width="4"')
    s += path(f"M128,{h-2} L128,322 A82,74 0 0 1 292,322 L292,{h-2} Z", "#5e3f45", 'stroke-width="3"')
    s += rr(130, h - 30, 160, 16, 6, C["madeira_esc"], 'stroke-width="2.5"')
    s += rr(40, h - 18, 340, 16, 4, "#cbbcab", 'stroke-width="3"')
    return svg(w, h, s)


P["lareira"] = lareira()


def fogo(alto):
    w, h = 140, 90
    k = 1.0 if alto else 0.65
    s = ""
    for dx, hh, c in [(-34, 60, "#ff9a3c"), (34, 60, "#ff9a3c"), (0, 84, "#ff7b54"), (-14, 52, C["amarelo"]), (16, 48, C["amarelo"])]:
        x = 70 + dx
        s += path(f"M{x-22},{h-6} Q{x-24},{h-6-hh*k*0.5} {x},{h-6-hh*k} Q{x+24},{h-6-hh*k*0.5} {x+22},{h-6} Z", c, 'stroke-width="2.5"')
    if alto:
        s += estrela(28, 18, 6, C["amarelo"], 4, 'stroke-width="1.5"') + estrela(112, 26, 5, C["amarelo"], 4, 'stroke-width="1.5"')
    return svg(w, h, s)


P["fogo_baixo"] = fogo(False)
P["fogo_alto"] = fogo(True)


def sofa():
    w, h = 460, 200
    s = rr(20, 20, 420, 120, 40, C["lilas"], 'stroke-width="4"')            # encosto
    s += rr(36, 34, 190, 96, 30, "#e2cff9", 'stroke-width="2.5"') + rr(234, 34, 190, 96, 30, "#e2cff9", 'stroke-width="2.5"')
    s += rr(44, 112, 372, 56, 22, C["lilas"], 'stroke-width="3.5"')           # assento
    s += path("M230,116 L230,164", extra='stroke-width="2.5" opacity="0.6"')
    s += rr(2, 80, 70, 100, 30, C["roxo"], 'stroke-width="4"') + rr(388, 80, 70, 100, 30, C["roxo"], 'stroke-width="4"')
    s += rr(40, 168, 16, 30, 4, C["madeira_esc"]) + rr(404, 168, 16, 30, 4, C["madeira_esc"])
    return svg(w, h, s)


P["sofa"] = sofa()


def almofada(cor):
    s = coracao(35, 30, 27, cor, 'stroke-width="3"') + coracao(35, 30, 15, "none", 'stroke-width="2" opacity="0.5" stroke-dasharray="4 4"')
    return svg(70, 60, s)


P["almofada_rosa"] = almofada(C["rosa"])
P["almofada_lilas"] = almofada(C["lilas_claro"])


def mesa_centro():
    w, h = 260, 100
    s = rr(40, 34, 22, 64, 6, C["madeira_esc"]) + rr(198, 34, 22, 64, 6, C["madeira_esc"])
    s += ell(130, 26, 126, 22, C["madeira"], 'stroke-width="3.5"') + rr(4, 26, 252, 18, 9, C["madeira"], 'stroke-width="3.5"')
    s += ell(130, 24, 124, 20, C["madeira_clara"], 'stroke-width="2.5"')
    return svg(w, h, s)


P["mesa_centro"] = mesa_centro()
P["vaso_flores"] = planta_vaso(50, 70, C["rosa_chiclete"], C["amarelo"])


def tapete():
    w, h = 600, 150
    s = ell(300, 75, 296, 70, "#e8cf9f", 'stroke-width="3.5"')
    for k in (0.82, 0.62, 0.42, 0.22):
        s += ell(300, 75, 296 * k, 70 * k, "none", 'stroke-width="2" opacity="0.45"')
    return svg(w, h, s)


P["tapete"] = tapete()


def abajur(aceso):
    w, h = 90, 200
    s = ""
    if aceso:
        s += circ(45, 60, 46, "#ffe7a3", 'stroke="none" opacity="0.6"')
    s += rr(40, 80, 10, 100, 3, C["madeira_esc"], 'stroke-width="2.5"')
    s += ell(45, 186, 30, 10, C["madeira"], 'stroke-width="3"')
    s += path("M18,82 L72,82 L62,24 L28,24 Z", "#fff2c4" if aceso else C["rosa_claro"], 'stroke-width="3"')
    s += coracao(45, 54, 8, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["abajur_apagado"] = abajur(False)
P["abajur_aceso"] = abajur(True)


def estante():
    w, h = 300, 330
    s = rr(4, 4, 292, 322, 8, C["madeira"], 'stroke-width="4"') + rr(18, 18, 264, 296, 4, C["madeira_esc"], 'stroke-width="2.5"')
    for y in (110, 210):
        s += rr(14, y, 272, 14, 3, C["madeira"], 'stroke-width="2.5"')
    s += rr(10, 300, 280, 26, 4, C["madeira"], 'stroke-width="3"')
    return svg(w, h, s)


P["estante"] = estante()


def livro(cor):
    s = rr(6, 4, 28, 42, 4, cor, 'stroke-width="2.5"') + rr(30, 6, 5, 38, 2, C["branco"], 'stroke-width="1.5"')
    s += estrela(20, 25, 7, C["amarelo"], 5, 'stroke-width="1.5"')
    return svg(40, 50, s)


P["livro_rosa"] = livro(C["rosa_chiclete"])
P["livro_azul"] = livro(C["azul"])
P["porta_retrato"] = svg(50, 50, rr(4, 4, 42, 40, 5, C["lilas"], 'stroke-width="2.5"') + rr(10, 10, 30, 28, 2, C["ceu"], 'stroke-width="2"') +
                         path("M10,34 Q25,22 40,32 L40,38 L10,38 Z", C["verde"], 'stroke-width="1.5"') + coracao(25, 22, 5, C["rosa_forte"], 'stroke-width="1.5"') +
                         path("M18,44 L14,48 M32,44 L36,48", extra='stroke-width="2"'))
P["plantinha"] = planta_vaso(50, 60, C["lilas"])


def cesto_brinquedos():
    w, h = 140, 110
    s = circ(48, 40, 18, C["amarelo"], 'stroke-width="2.5"') + circ(42, 34, 4, C["branco"], 'stroke="none"')
    s += circ(84, 30, 13, "#c98c56", 'stroke-width="2.5"') + circ(73, 20, 6, "#c98c56", 'stroke-width="2"') + circ(95, 20, 6, "#c98c56", 'stroke-width="2"')
    s += circ(80, 30, 1.8, L, 'stroke="none"') + circ(88, 30, 1.8, L, 'stroke="none"')
    s += path("M6,46 L134,46 L122,108 L18,108 Z", C["mel"], 'stroke-width="3"')
    for y in (60, 76, 92):
        s += path(f"M{8 + (y-46)*0.18},{y} L{132 - (y-46)*0.18},{y}", extra='stroke-width="1.6" opacity="0.5"')
    s += rr(2, 40, 136, 14, 6, C["mel"], 'stroke-width="3"') + coracao(70, 82, 9, C["rosa_forte"], 'stroke-width="2"')
    return svg(w, h, s)


P["cesto_brinquedos"] = cesto_brinquedos()
P["porta_fechada"] = porta_casa(False)
P["porta_aberta"] = porta_casa(True)
for d in ("coracao", "flor", "panela", "casa"):
    P[f"placa_{d}"] = plaquinha(d)

POS = [("fundo", 0, 0),
       ("porta_aberta", 40, 250), ("placa_casa", 95, 180),
       ("estante", 250, 270), ("livro_rosa", 280, 330), ("livro_azul", 322, 330), ("porta_retrato", 440, 330), ("plantinha", 470, 420),
       ("livro_rosa", 300, 430),
       ("porta_fechada", 600, 250), ("placa_panela", 650, 180),
       ("lareira", 800, 180), ("fogo_alto", 940, 508), ("vaso_flores", 830, 330), ("vaso_flores", 1110, 330),
       ("sofa", 1240, 410), ("almofada_rosa", 1290, 450), ("almofada_lilas", 1600, 450),
       ("abajur_aceso", 1715, 412),
       ("porta_fechada", 1820, 250), ("placa_coracao", 1870, 180),
       ("porta_fechada", 2010, 250), ("placa_flor", 2060, 180),
       ("tapete", 900, 700), ("mesa_centro", 1070, 660), ("vaso_flores", 1170, 600),
       ("cesto_brinquedos", 520, 690), ("@catarina", 700, 860), ("@catarina", 1460, 600)]

TABELA = [
    ("Fundo da sala", "2200 × 900", None, "Parede rosa-clara com listras suaves e vigas de madeira no alto, janela com cortina rosa e vista da fazenda, três plantas penduradas, quadro de um celeiro rosa, rodapé e piso de madeira clara. SEM lareira, portas ou móveis.", ["fundo"]),
    ("Lareira de pedra", "420 × 420", None, "Lareira de pedras arredondadas creme com prateleira de madeira e um coração rosa grande no alto. Boca da lareira escura e VAZIA (o fogo é a peça 3).", ["lareira"]),
    ("Fogo da lareira", "140 × 90", "baixo · alto", "Foguinho de brinquedo, laranja e amarelo, que encaixa na boca da lareira. Alto: chamas maiores e estrelinhas.", ["fogo_baixo", "fogo_alto"]),
    ("Sofá lilás", "460 × 200", None, "Sofá fofo de três lugares, lilás com encosto acolchoado e pés de madeira. Assento plano a 110 px do chão do sofá, onde sentam 3 ou deita 1.", ["sofa"]),
    ("Almofada de coração", "70 × 60", "rosa · lilás", "Almofada em forma de coração com costura aparente.", ["almofada_rosa", "almofada_lilas"]),
    ("Mesa de centro", "260 × 100", None, "Mesa redonda baixa de madeira, tampo PLANO para apoiar objetos.", ["mesa_centro"]),
    ("Vaso de flores", "50 × 70", None, "Vaso rosa com flores amarelas.", ["vaso_flores"]),
    ("Tapete redondo", "600 × 150", None, "Tapete de palha trançada visto de cima e de leve, oval.", ["tapete"]),
    ("Abajur", "90 × 200", "apagado · aceso", "Abajur de pé de madeira com cúpula rosa-clara e coração. Aceso: cúpula clara e brilho quente em volta.", ["abajur_apagado", "abajur_aceso"]),
    ("Estante", "300 × 330", None, "Estante de madeira com três prateleiras VAZIAS (os objetos são peças separadas).", ["estante"]),
    ("Objetos da estante", "livro 40 × 50 · porta-retrato 50 × 50 · plantinha 50 × 60", "livro rosa · livro azul", "Livros de figura com estrelinha na capa (sem letras), porta-retrato lilás com paisagem, vasinho com planta.", ["livro_rosa", "livro_azul", "porta_retrato", "plantinha"]),
    ("Cesto de brinquedos", "140 × 110", None, "Cesto de vime com coração; aparecem uma bola amarela e um ursinho.", ["cesto_brinquedos"]),
    ("Porta da casa", "170 × 350", "fechada · aberta", "A mesma porta de madeira do quarto (arredondada no alto). Aberta: folha encostada e luz quente do outro cômodo. Serve para as 4 portas.", ["porta_fechada", "porta_aberta"]),
    ("Plaquinhas das portas", "70 × 60", "coração · flor · panela · casinha", "Plaquinha de madeira pendurada acima de cada porta, SEM letras: coração (quarto da Catarina), flor (quarto da Carol), panelinha (cozinha) e casinha (porta da frente).", ["placa_coracao", "placa_flor", "placa_panela", "placa_casa"]),
]

if __name__ == "__main__":
    pr, le = textos("sala", "Sala da Família", "C03",
                    "É o coração da casa: sofá lilás, lareira de pedra com coração e mesa de centro; dela saem as portas para os quartos, a cozinha e a frente da casa.",
                    " e a colagem `arte/conceito/colagem_cenarios/colagem_sala.png` (só o clima: o jogo é visto DE FRENTE, sem teto)",
                    "2200 × 900, chão a partir de y = 600", TABELA,
                    ordem="\nGere primeiro a lareira com o fogo, o sofá e a porta: são as peças das brincadeiras principais.\n"
                          "A lareira é decorativa: o fogo só crepita, não aceita objetos nem personagens.\n")
    gerar_cenario("sala", P, W, H, POS, "C03 Sala da Família · Catarina = 300 px · chão a partir de y = 600 · tela 2200 × 900", pr, le)

# ---------------------------------------------------------------- no jogo (ferramentas/cenario2d/para_jogo.py)
# Peças que mudam de estado com um toque, lugares onde os personagens se encaixam e superfícies.
JOGO = {
    "interativos": {
        "porta_frente": {"estados": ["porta_fechada", "porta_aberta"], "x": 40, "y": 250, "leva": "sede", "chegada": 125, "estado": 0},
        "porta_cozinha": {"estados": ["porta_fechada", "porta_aberta"], "x": 600, "y": 250, "leva": "cozinha", "chegada": 685},
        "porta_catarina": {"estados": ["porta_fechada", "porta_aberta"], "x": 1820, "y": 250, "leva": "quarto", "chegada": 1905},
        "porta_carol": {"estados": ["porta_fechada", "porta_aberta"], "x": 2010, "y": 250, "leva": "quarto_carol", "chegada": 2095},
        "abajur": {"estados": ["abajur_apagado", "abajur_aceso"], "x": 1715, "y": 412},
        "fogo": {"estados": ["fogo_baixo", "fogo_alto"], "x": 940, "y": 508},
    },
    # sofá: deitam até 3 (pose "deitar", como no beliche)
    "animacoes": {"@fogo": {"tipo": "fogo"}},
    "lugares": [{"id": "sofa", "area": [1250, 330, 440, 220], "spots": [[1520, 528], [1600, 530], [1360, 530]], "pose": "deitar"}],
    # superfícies onde os objetos se apoiam: [x inicial, x final, altura]
    "superficies": [[1076, 1324, 682], [266, 534, 382], [266, 534, 482], [266, 534, 572]],
}
