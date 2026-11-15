"""Itens novos da loja e botões do baú, em 2D provisório (15/11/2026).

Cada item tem o tamanho da ficha em prototipo/dados/itens.json (régua do jogo: Catarina com 300 px).
Quando a arte 3D chegar, é só trocar os PNGs (mesmos nomes e proporções).
Uso: python3 ferramentas/cenario2d/itens.py
Saída: arte/interface/itens/*.png, copiados para prototipo/assets/itens/.
"""
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, rr, circ, ell, path, coracao, estrela, flor, salvar  # noqa: E402

raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dest = os.path.join(raiz, "arte/interface/itens")
jogo = os.path.join(raiz, "prototipo/assets/itens")
os.makedirs(dest, exist_ok=True)
os.makedirs(jogo, exist_ok=True)
P = {}
PEDRA, PEDRA_ESC = "#d6c9b9", "#b8a893"
VERM = "#ef6f6f"


def folha(x, y, comp, ang, cor=None, sw=2):
    a = math.radians(ang)
    x2, y2 = x + comp * math.cos(a), y + comp * math.sin(a)
    px, py = -math.sin(a) * comp * 0.3, math.cos(a) * comp * 0.3
    mx, my = (x + x2) / 2, (y + y2) / 2
    return path(f"M{x:.1f},{y:.1f} Q{mx+px:.1f},{my+py:.1f} {x2:.1f},{y2:.1f} Q{mx-px:.1f},{my-py:.1f} {x:.1f},{y:.1f} Z",
                cor or C["verde"], f'stroke-width="{sw}"')


# ---------------------------------------------------------------- quintal

# banco de tronco (200 x 80): tronco deitado com dois tocos
s = rr(20, 40, 30, 38, 6, C["madeira_esc"], 'stroke-width="3"') + rr(150, 40, 30, 38, 6, C["madeira_esc"], 'stroke-width="3"')
s += rr(4, 14, 192, 34, 16, C["madeira"], 'stroke-width="3"') + ell(18, 31, 12, 16, C["madeira_clara"], 'stroke-width="2.5"')
s += ell(18, 31, 5, 7, "none", 'stroke-width="1.5"') + path("M50,24 L120,24 M70,36 L160,36", extra='stroke-width="1.5" opacity="0.4"')
s += coracao(110, 30, 6, C["rosa_forte"], 'stroke-width="1.5"')
P["banco_tronco"] = svg(200, 80, s)

# bebedouro de passarinho (110 x 150): bacia de pedra num pé
s = path("M42,60 L68,60 L74,140 L36,140 Z", PEDRA, 'stroke-width="3"') + ell(55, 142, 34, 7, PEDRA_ESC, 'stroke-width="2.5"')
s += path("M6,44 Q55,82 104,44 Z", PEDRA, 'stroke-width="3"') + ell(55, 44, 49, 10, C["agua"], 'stroke-width="3"')
s += ell(42, 42, 10, 3, C["branco"], 'stroke="none" opacity="0.7"') + coracao(55, 100, 7, C["rosa_forte"], 'stroke-width="1.5"')
P["bebedouro"] = svg(110, 150, s)

# carrinho de flores (170 x 120)
s = rr(8, 50, 130, 44, 8, C["azul"], 'stroke-width="3"') + path("M138,58 L166,40", extra='stroke-width="6"') + path("M138,58 L166,40", extra=f'stroke="{C["madeira"]}" stroke-width="3"')
for i, x in enumerate((26, 50, 74, 98, 122)):
    s += folha(x, 50, 18, -120, C["verde"]) + flor(x, 34 - (i % 2) * 8, 11, [C["rosa_chiclete"], C["amarelo"], C["lilas"]][i % 3], C["branco"])
s += circ(36, 100, 16, C["madeira"], 'stroke-width="3"') + circ(36, 100, 5, C["madeira_esc"], 'stroke-width="2"')
s += circ(112, 100, 16, C["madeira"], 'stroke-width="3"') + circ(112, 100, 5, C["madeira_esc"], 'stroke-width="2"')
P["carrinho_flores"] = svg(170, 120, s)

# balanço de pneu (150 x 260): galho em cima, corda e pneu
s = rr(4, 6, 142, 20, 9, C["madeira_esc"], 'stroke-width="3"') + folha(30, 10, 22, -150) + folha(124, 10, 22, -30)
s += path("M75,24 L75,170", extra='stroke-width="5"') + path("M75,24 L75,170", extra=f'stroke="{C["mel"]}" stroke-width="2.5"')
s += ell(75, 214, 52, 40, "#5a5560", 'stroke-width="3"') + ell(75, 214, 26, 18, C["verde_claro"], 'stroke-width="3"')
s += path("M40,206 q8,-8 16,0 M94,206 q8,-8 16,0", extra=f'stroke="{C["cinza"]}" stroke-width="2"')
P["balanco_pneu"] = svg(150, 260, s)

# fonte de passarinho (160 x 170): dois pratos com água
s = path("M64,90 L96,90 L104,160 L56,160 Z", PEDRA, 'stroke-width="3"') + ell(80, 162, 50, 7, PEDRA_ESC, 'stroke-width="2.5"')
s += path("M8,82 Q80,124 152,82 Z", PEDRA, 'stroke-width="3"') + ell(80, 82, 72, 13, C["agua"], 'stroke-width="3"')
s += path("M70,36 L90,36 L88,80 L72,80 Z", PEDRA, 'stroke-width="2.5"') + path("M40,32 Q80,58 120,32 Z", PEDRA, 'stroke-width="3"')
s += ell(80, 32, 40, 8, C["agua"], 'stroke-width="2.5"') + path("M80,26 Q80,6 80,4 M80,8 Q70,14 64,24 M80,8 Q90,14 96,24", extra=f'stroke="{C["azul"]}" stroke-width="3"')
P["fonte_passarinho"] = svg(160, 170, s)

# rede de jardim (300 x 170): dois postes e a rede listrada
s = rr(12, 20, 16, 148, 5, C["madeira_esc"], 'stroke-width="3"') + rr(272, 20, 16, 148, 5, C["madeira_esc"], 'stroke-width="3"')
s += path("M26,40 Q150,150 274,40 L274,58 Q150,170 26,58 Z", C["rosa_claro"], 'stroke-width="3"')
for k, cor in ((0.33, C["lilas"]), (0.66, C["amarelo"])):
    s += path(f"M26,{40 + 18 * k} Q150,{150 + 20 * k} 274,{40 + 18 * k}", extra=f'stroke="{cor}" stroke-width="5"')
s += coracao(150, 118, 8, C["rosa_forte"], 'stroke-width="1.5"')
P["rede_jardim"] = svg(300, 170, s)

# ---------------------------------------------------------------- casa

# almofada de chão (90 x 50)
P["almofada_chao"] = svg(90, 50, path("M6,30 Q4,8 45,8 Q86,8 84,30 Q86,46 45,46 Q4,46 6,30 Z", C["lilas"], 'stroke-width="3"') +
                         path("M20,20 Q45,30 70,20", extra='stroke-width="1.5" opacity="0.4"') + coracao(45, 28, 8, C["rosa_forte"], 'stroke-width="1.5"'))

# tapete redondo (240 x 70)
P["tapete_redondo"] = svg(240, 70, ell(120, 38, 114, 28, C["rosa_claro"], 'stroke-width="3"') + ell(120, 38, 84, 19, C["creme"], 'stroke-width="2"') +
                          ell(120, 38, 50, 11, C["lilas_claro"], 'stroke-width="2"') + coracao(120, 38, 7, C["rosa_forte"], 'stroke-width="1.5"'))

# quadro de flor (100 x 110), de parede
s = rr(6, 6, 88, 98, 8, C["madeira"], 'stroke-width="3"') + rr(16, 16, 68, 78, 4, C["ceu_claro"], 'stroke-width="2"')
s += path("M50,90 L50,52", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') + folha(50, 74, 14, -150) + flor(50, 44, 13, C["rosa_chiclete"], C["amarelo"])
P["quadro_flor"] = svg(100, 110, s)

# abajur de chão (70 x 190)
s = ell(35, 184, 26, 6, C["madeira_esc"], 'stroke-width="2.5"') + rr(31, 60, 8, 124, 3, C["madeira"], 'stroke-width="2.5"')
s += circ(35, 40, 30, "#fff0b8", 'stroke="none" opacity="0.5"') + path("M14,62 L22,14 L48,14 L56,62 Z", C["rosa_claro"], 'stroke-width="3"')
s += coracao(35, 40, 7, C["rosa_forte"], 'stroke-width="1.5"')
P["abajur_chao"] = svg(70, 190, s)

# banquinho de casa (90 x 90)
s = rr(14, 40, 10, 48, 3, C["madeira_esc"], 'stroke-width="2.5"') + rr(66, 40, 10, 48, 3, C["madeira_esc"], 'stroke-width="2.5"')
s += rr(4, 26, 82, 20, 8, C["lilas"], 'stroke-width="3"') + rr(10, 60, 70, 8, 3, C["madeira"], 'stroke-width="2"') + coracao(45, 36, 5, C["branco"], 'stroke-width="1.5"')
P["banquinho_casa"] = svg(90, 90, s)

# poltrona (200 x 190)
s = rr(26, 160, 14, 28, 4, C["madeira_esc"], 'stroke-width="2.5"') + rr(160, 160, 14, 28, 4, C["madeira_esc"], 'stroke-width="2.5"')
s += rr(30, 10, 140, 120, 40, C["rosa"], 'stroke-width="3"') + rr(34, 104, 132, 46, 16, C["rosa_claro"], 'stroke-width="3"')
s += rr(4, 70, 40, 92, 18, C["rosa"], 'stroke-width="3"') + rr(156, 70, 40, 92, 18, C["rosa"], 'stroke-width="3"')
s += coracao(100, 60, 12, C["rosa_forte"], 'stroke-width="2"')
P["poltrona"] = svg(200, 190, s)

# estante baixa (200 x 150) com livros e vaso
s = rr(6, 30, 188, 116, 8, C["madeira"], 'stroke-width="3"') + rr(16, 40, 168, 44, 4, C["madeira_clara"], 'stroke-width="2"') + rr(16, 92, 168, 44, 4, C["madeira_clara"], 'stroke-width="2"')
for i, (x, cor) in enumerate([(24, C["azul"]), (40, C["rosa_chiclete"]), (56, C["amarelo"]), (72, C["lilas"])]):
    s += rr(x, 50 + (i % 2) * 4, 14, 34 - (i % 2) * 4, 3, cor, 'stroke-width="2"')
s += circ(140, 116, 16, C["verde"], 'stroke-width="2.5"') + rr(118, 100, 10, 36, 3, C["rosa"], 'stroke-width="2"')
s += path("M140,30 L140,10", extra=f'stroke="{C["verde_esc"]}" stroke-width="3"') + rr(128, 18, 24, 14, 4, C["creme"], 'stroke-width="2"') + flor(140, 8, 8, C["rosa_chiclete"], C["amarelo"])
P["estante_baixa"] = svg(200, 150, s)

# mesa de chá com duas cadeirinhas (260 x 130)
s = ""
for x in (8, 222):
    s += rr(x, 24, 30, 60, 10, C["lilas"], 'stroke-width="3"') + rr(x - 2, 78, 34, 14, 6, C["lilas"], 'stroke-width="3"')
    s += rr(x + 2, 90, 6, 38, 2, C["madeira_esc"], 'stroke-width="2"') + rr(x + 22, 90, 6, 38, 2, C["madeira_esc"], 'stroke-width="2"')
s += rr(76, 80, 10, 48, 3, C["madeira_esc"], 'stroke-width="2.5"') + rr(174, 80, 10, 48, 3, C["madeira_esc"], 'stroke-width="2.5"')
s += rr(60, 66, 140, 18, 8, C["madeira"], 'stroke-width="3"') + path("M64,72 L196,72", extra=f'stroke="{C["rosa_claro"]}" stroke-width="6"')
s += path("M110,64 L110,46 Q130,36 150,46 L150,64 Z", C["branco"], 'stroke-width="2.5"') + path("M150,50 q10,0 8,10", extra='stroke-width="2.5"')
s += coracao(130, 54, 5, C["rosa_forte"], 'stroke-width="1.2"')
P["mesa_cha"] = svg(260, 130, s)

# relógio de parede (100 x 130)
s = path("M50,4 L94,40 L6,40 Z", C["madeira"], 'stroke-width="3"') + rr(12, 36, 76, 90, 10, C["madeira"], 'stroke-width="3"')
s += circ(50, 72, 28, C["creme"], 'stroke-width="2.5"') + path("M50,72 L50,54 M50,72 L64,78", extra='stroke-width="3"')
s += circ(50, 72, 3, L, 'stroke="none"') + path("M50,100 L50,116", extra='stroke-width="2"') + circ(50, 118, 6, C["dourado"], 'stroke-width="2"')
P["relogio_parede"] = svg(100, 130, s)

# tapete grande de flores (420 x 110)
s = rr(6, 20, 408, 84, 30, C["verde_claro"], 'stroke-width="3"') + rr(26, 34, 368, 56, 22, C["creme"], 'stroke-width="2"')
for i, x in enumerate(range(60, 380, 52)):
    s += flor(x, 62, 12, [C["rosa_chiclete"], C["amarelo"], C["lilas"]][i % 3], C["branco"])
P["tapete_flores"] = svg(420, 110, s)

# ---------------------------------------------------------------- bichinhos

# tigela de água (80 x 40)
P["tigela_agua_pet"] = svg(80, 40, path("M6,12 L74,12 L64,36 L16,36 Z", C["azul"], 'stroke-width="3"') + ell(40, 12, 34, 6, C["agua"], 'stroke-width="2.5"') +
                           coracao(40, 25, 5, C["branco"], 'stroke-width="1.2"'))

# caminha (170 x 80)
s = path("M6,40 Q4,10 30,10 L140,10 Q166,10 164,40 L164,64 Q164,76 150,76 L20,76 Q6,76 6,64 Z", C["rosa"], 'stroke-width="3"')
s += rr(22, 30, 126, 36, 16, C["creme"], 'stroke-width="2.5"') + coracao(85, 22, 6, C["rosa_forte"], 'stroke-width="1.5"')
s += path("M40,48 q8,-8 16,0 M114,48 q8,-8 16,0", extra='stroke-width="1.5" opacity="0.4"')
P["caminha"] = svg(170, 80, s)

# arranhador de gato (110 x 200)
s = rr(6, 182, 98, 16, 6, C["lilas"], 'stroke-width="3"') + rr(42, 50, 26, 134, 6, C["mel"], 'stroke-width="3"')
for y in range(62, 180, 12):
    s += path(f"M42,{y} L68,{y+6}", extra='stroke-width="1.5" opacity="0.5"')
s += rr(8, 26, 94, 26, 10, C["lilas"], 'stroke-width="3"') + circ(30, 76, 9, C["rosa_chiclete"], 'stroke-width="2"') + path("M30,52 L30,67", extra='stroke-width="2"')
P["arranhador"] = svg(110, 200, s)

# casinha de cachorro (220 x 200)
s = rr(20, 70, 180, 126, 8, C["madeira"], 'stroke-width="3"') + path("M8,82 L110,10 L212,82 Z", VERM, 'stroke-width="3"')
s += path("M74,196 L74,130 Q110,96 146,130 L146,196 Z", "#6b4630", 'stroke-width="3"') + rr(80, 54, 60, 18, 6, C["creme"], 'stroke-width="2.5"')
s += path("M100,63 a5,5 0 1 0 10,0 a5,5 0 1 0 -10,0 M114,58 a4,4 0 1 0 8,0 a4,4 0 1 0 -8,0", C["madeira_esc"], 'stroke-width="1"')
P["casinha_cachorro"] = svg(220, 200, s)

# parquinho de gato (200 x 260): duas plataformas em postes
s = rr(10, 240, 180, 18, 6, C["lilas"], 'stroke-width="3"') + rr(46, 70, 20, 172, 5, C["mel"], 'stroke-width="3"') + rr(134, 150, 20, 92, 5, C["mel"], 'stroke-width="3"')
s += rr(12, 58, 90, 22, 8, C["rosa"], 'stroke-width="3"') + rr(100, 136, 90, 22, 8, C["rosa"], 'stroke-width="3"')
s += rr(40, 20, 50, 40, 18, C["lilas_claro"], 'stroke-width="3"') + ell(65, 44, 14, 10, "#6b4630", 'stroke-width="2"') + circ(160, 190, 10, C["amarelo"], 'stroke-width="2"')
P["parquinho_gato"] = svg(200, 260, s)

# manta e escovinha da Lumi num cavalete (150 x 130)
s = path("M20,128 L40,40 M130,128 L110,40", extra='stroke-width="8"') + path("M20,128 L40,40 M130,128 L110,40", extra=f'stroke="{C["madeira"]}" stroke-width="5"')
s += rr(26, 34, 98, 12, 4, C["madeira_esc"], 'stroke-width="2.5"') + path("M30,40 L120,40 L114,104 Q75,114 36,104 Z", C["rosa_chiclete"], 'stroke-width="3"')
s += path("M38,90 Q75,98 112,90", extra=f'stroke="{C["amarelo"]}" stroke-width="4"') + estrela(75, 70, 12, C["amarelo"], 5, 'stroke-width="2"')
s += rr(96, 4, 40, 16, 6, C["lilas"], 'stroke-width="2.5"') + path("M100,20 l0,8 M108,20 l0,8 M116,20 l0,8 M124,20 l0,8 M132,20 l0,8", extra='stroke-width="2"')
P["manta_lumi"] = svg(150, 130, s)

# ---------------------------------------------------------------- construções

# poço (200 x 230)
s = rr(36, 30, 14, 140, 4, C["madeira_esc"], 'stroke-width="3"') + rr(150, 30, 14, 140, 4, C["madeira_esc"], 'stroke-width="3"')
s += path("M20,40 L100,4 L180,40 Z", VERM, 'stroke-width="3"') + rr(46, 60, 108, 10, 4, C["madeira"], 'stroke-width="2.5"')
s += path("M100,70 L100,110", extra='stroke-width="2.5"') + rr(88, 108, 24, 22, 4, C["madeira"], 'stroke-width="2.5"')
s += path("M10,150 Q100,170 190,150 L190,224 L10,224 Z", PEDRA, 'stroke-width="3"') + ell(100, 150, 90, 16, "#6b8fa8", 'stroke-width="3"')
for x, y in ((40, 186), (100, 196), (160, 186), (70, 212), (130, 212)):
    s += rr(x - 18, y - 9, 36, 18, 6, PEDRA_ESC, 'stroke-width="2"')
P["poco"] = svg(200, 230, s)

# galinheiro (320 x 260)
s = rr(30, 100, 260, 154, 8, C["creme"], 'stroke-width="3"') + path("M12,112 L160,24 L308,112 Z", VERM, 'stroke-width="3"')
for x in range(46, 290, 22):
    s += path(f"M{x},104 L{x},250", extra='stroke-width="1.2" opacity="0.25"')
s += path("M130,254 L130,180 Q160,150 190,180 L190,254 Z", "#6b4630", 'stroke-width="3"') + path("M136,254 L184,214", extra=f'stroke="{C["madeira"]}" stroke-width="6"')
s += rr(54, 140, 50, 40, 6, C["ceu_claro"], 'stroke-width="2.5"') + rr(216, 140, 50, 40, 6, C["ceu_claro"], 'stroke-width="2.5"')
# galinha (sem rosto de personagem: bichinho de enfeite)
s += ell(240, 234, 24, 18, C["branco"], 'stroke-width="2.5"') + circ(258, 216, 10, C["branco"], 'stroke-width="2.5"') + path("M266,216 l8,3 l-8,3 Z", C["laranja"], 'stroke-width="1.5"')
s += path("M254,206 q4,-8 8,0 q4,-8 6,2", C["vermelho_rosa"], 'stroke-width="1.5"') + circ(260, 214, 1.8, L, 'stroke="none"')
s += ell(80, 248, 12, 7, C["creme"], 'stroke-width="2"') + ell(98, 250, 11, 7, C["creme"], 'stroke-width="2"')
s += coracao(160, 70, 10, C["branco"], 'stroke-width="2"')
P["galinheiro"] = svg(320, 260, s)

# colmeia (120 x 170): caixas empilhadas num pé
s = rr(26, 140, 12, 28, 3, C["madeira_esc"], 'stroke-width="2.5"') + rr(82, 140, 12, 28, 3, C["madeira_esc"], 'stroke-width="2.5"')
for k, y in enumerate((96, 62, 28)):
    s += rr(14, y, 92, 38, 6, [C["amarelo"], C["mel"], C["amarelo"]][k], 'stroke-width="3"')
s += path("M8,30 L60,8 L112,30 Z", C["rosa_chiclete"], 'stroke-width="3"') + rr(46, 124, 28, 8, 3, "#6b4630", 'stroke-width="2"')
for x, y in ((18, 20), (104, 60), (96, 14)):
    s += ell(x, y, 6, 5, C["amarelo"], 'stroke-width="1.5"') + path(f"M{x-2},{y-4} l0,8 M{x+2},{y-4} l0,8", extra='stroke-width="1.2"')
P["colmeia"] = svg(120, 170, s)

# estufa de flores (380 x 300)
s = rr(20, 110, 340, 186, 10, C["ceu_claro"], 'stroke-width="3" fill-opacity="0.9"') + path("M10,120 Q190,-20 370,120 Z", C["ceu_claro"], 'stroke-width="3"')
for x in range(70, 340, 50):
    s += path(f"M{x},110 L{x},294", extra='stroke-width="2" opacity="0.6"')
s += path("M40,120 Q190,10 340,120", extra='stroke-width="2" opacity="0.6"') + path("M160,296 L160,200 L220,200 L220,296", C["branco"], 'stroke-width="3"')
for i, x in enumerate(range(44, 340, 34)):
    if 150 < x < 230:
        continue
    s += folha(x, 270, 20, -110) + flor(x, 248 - (i % 2) * 14, 10, [C["rosa_chiclete"], C["amarelo"], C["lilas"]][i % 3], C["branco"])
s += rr(20, 270, 340, 26, 6, C["madeira"], 'stroke-width="3"')
P["estufa"] = svg(380, 300, s)

# coreto de flores (420 x 380)
s = ell(210, 352, 196, 24, C["madeira_clara"], 'stroke-width="3"') + rr(24, 320, 372, 34, 10, C["madeira"], 'stroke-width="3"')
for x in (54, 132, 210, 288, 366):
    s += rr(x - 9, 130, 18, 192, 5, C["branco"], 'stroke-width="3"')
s += path("M24,300 L396,300", extra='stroke-width="6"') + path("M24,300 L396,300", extra=f'stroke="{C["branco"]}" stroke-width="3"')
s += path("M8,140 L210,30 L412,140 Z", C["rosa_chiclete"], 'stroke-width="3"') + rr(4, 132, 412, 18, 8, C["rosa"], 'stroke-width="3"')
s += circ(210, 26, 12, C["dourado"], 'stroke-width="2.5"')
for i, x in enumerate(range(20, 410, 30)):
    s += flor(x, 156, 9, [C["rosa_chiclete"], C["amarelo"], C["lilas"]][i % 3], C["branco"])
P["coreto"] = svg(420, 380, s)

# ---------------------------------------------------------------- botões do baú e da loja

def bau(aberto):
    s = rr(10, 50, 100, 60, 10, C["madeira"], 'stroke-width="4"') + rr(10, 72, 100, 10, 2, C["madeira_esc"], 'stroke-width="2.5"')
    if aberto:
        s += path("M14,50 L22,14 L98,14 L106,50 Z", C["madeira_clara"], 'stroke-width="4"') + estrela(60, 36, 10, C["amarelo"], 4, 'stroke-width="2"')
    else:
        s += path("M10,52 Q10,22 60,22 Q110,22 110,52 Z", C["madeira"], 'stroke-width="4"')
    s += path("M44,96 L42,82 A10,10 0 0 1 78,82 L76,96 L70,96 L71,84 A5,5 0 0 0 49,84 L50,96 Z", C["dourado"], 'stroke-width="2.5"')
    return s


P["botao_bau"] = svg(120, 120, circ(60, 60, 56, C["rosa_claro"], 'stroke-width="5"') + f'<g transform="translate(10 6) scale(0.84)">{bau(False)}</g>')
P["botao_bau_aberto"] = svg(120, 120, circ(60, 60, 56, C["amarelo"], 'stroke-width="5"') + f'<g transform="translate(10 6) scale(0.84)">{bau(True)}</g>')
P["balao_guardar"] = svg(110, 120, path("M55,116 L42,94 L14,94 Q4,94 4,84 L4,14 Q4,4 14,4 L96,4 Q106,4 106,14 L106,84 Q106,94 96,94 L68,94 Z", C["branco"], 'stroke-width="4"') +
                         f'<g transform="translate(10 8) scale(0.75)">{bau(False)}</g>')
P["seta_dir"] = svg(80, 80, circ(40, 40, 36, C["branco"], 'stroke-width="4"') + path("M32,22 L54,40 L32,58", extra='stroke-width="8"'))
P["seta_esq"] = svg(80, 80, circ(40, 40, 36, C["branco"], 'stroke-width="4"') + path("M48,22 L26,40 L48,58", extra='stroke-width="8"'))
# abas da loja (sem letras): árvore, poltrona, patinha, casinha
P["aba_quintal"] = svg(90, 90, rr(40, 50, 10, 34, 3, C["madeira_esc"], 'stroke-width="2.5"') + circ(45, 36, 28, C["verde"], 'stroke-width="3"') +
                       circ(36, 30, 4, C["rosa_chiclete"], 'stroke-width="1.5"') + circ(56, 42, 4, C["rosa_chiclete"], 'stroke-width="1.5"'))
P["aba_casa"] = svg(90, 90, rr(20, 22, 50, 46, 16, C["rosa"], 'stroke-width="3"') + rr(22, 56, 46, 18, 7, C["rosa_claro"], 'stroke-width="3"') +
                    rr(8, 44, 18, 36, 8, C["rosa"], 'stroke-width="3"') + rr(64, 44, 18, 36, 8, C["rosa"], 'stroke-width="3"'))
P["aba_bichinhos"] = svg(90, 90, ell(45, 58, 18, 15, C["madeira"], 'stroke-width="3"') + circ(24, 36, 8, C["madeira"], 'stroke-width="3"') +
                         circ(38, 24, 8, C["madeira"], 'stroke-width="3"') + circ(54, 24, 8, C["madeira"], 'stroke-width="3"') + circ(66, 36, 8, C["madeira"], 'stroke-width="3"'))
P["aba_construcoes"] = svg(90, 90, rr(18, 40, 54, 44, 4, C["creme"], 'stroke-width="3"') + path("M10,44 L45,12 L80,44 Z", VERM, 'stroke-width="3"') +
                           rr(37, 58, 16, 26, 3, C["madeira"], 'stroke-width="2.5"'))
P["selo_novo"] = svg(60, 60, estrela(30, 30, 26, C["amarelo"], 5, 'stroke-width="3"') + circ(30, 32, 6, C["branco"], 'stroke="none"'))
# passarinho visitante (bebedouro, fonte, casinha de passarinho)
P["passarinho_visita"] = svg(50, 40, ell(24, 24, 15, 11, C["azul"], 'stroke-width="2.5"') + circ(36, 15, 8, C["azul"], 'stroke-width="2.5"') +
                             path("M43,15 l7,2 l-7,3 Z", C["laranja"], 'stroke-width="1.5"') + circ(38, 13, 1.8, L, 'stroke="none"') +
                             path("M14,22 q8,-8 16,2", C["ceu_claro"], 'stroke-width="2"') + path("M9,26 l-7,-3 l2,7 Z", C["azul"], 'stroke-width="1.5"'))

if __name__ == "__main__":
    salvar(P, os.path.join(dest, "svg"), dest)
    for f in os.listdir(dest):
        if f.endswith(".png"):
            shutil.copyfile(os.path.join(dest, f), os.path.join(jogo, f))
    print(len(P), "imagens em", jogo)
