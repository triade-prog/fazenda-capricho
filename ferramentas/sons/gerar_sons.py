#!/usr/bin/env python3
"""Gera os sons provisórios do jogo (WAV mono 22 kHz) em prototipo/assets/sons/.

São sons sintetizados, curtinhos e suaves, para a criança ter retorno de cada ação já agora.
Quando houver sons gravados de verdade, é só pôr um WAV com o mesmo nome por cima.

Uso: python3 ferramentas/sons/gerar_sons.py
"""
import math
import os
import random
import struct
import wave

TAXA = 22050
SAIDA = os.path.join(os.path.dirname(__file__), "..", "..", "prototipo", "assets", "sons")


def env(i, n, ataque=0.01, solta=0.6):
    t = i / TAXA
    dur = n / TAXA
    a = min(1.0, t / ataque) if ataque > 0 else 1.0
    r = max(0.0, 1.0 - max(0.0, t - dur * (1 - solta)) / (dur * solta)) if solta > 0 else 1.0
    return a * r


def tom(f0, f1, dur, vol=0.5, forma="seno", vibrato=0.0, ataque=0.01, solta=0.6, ruido=0.0):
    n = int(TAXA * dur)
    out = []
    fase = 0.0
    for i in range(n):
        k = i / n
        f = f0 + (f1 - f0) * k
        if vibrato:
            f *= 1.0 + vibrato * math.sin(2 * math.pi * 7 * i / TAXA)
        fase += 2 * math.pi * f / TAXA
        if forma == "seno":
            v = math.sin(fase)
        elif forma == "suave":  # seno com um pouco de harmônico: mais "fofo"
            v = 0.8 * math.sin(fase) + 0.2 * math.sin(2 * fase)
        else:
            v = math.sin(fase)
        if ruido:
            v = v * (1 - ruido) + ruido * random.uniform(-1, 1)
        out.append(v * vol * env(i, n, ataque, solta))
    return out


def silencio(dur):
    return [0.0] * int(TAXA * dur)


def mistura(*partes):
    n = max(len(p) for p in partes)
    return [sum(p[i] for p in partes if i < len(p)) for i in range(n)]


def sopro(dur, vol=0.25):
    # ruído filtrado que sobe e desce (passagem de cenário)
    n = int(TAXA * dur)
    out, y = [], 0.0
    for i in range(n):
        k = i / n
        corte = 0.02 + 0.25 * math.sin(math.pi * k)
        y += corte * (random.uniform(-1, 1) - y)
        out.append(y * vol * 3 * math.sin(math.pi * k))
    return out


def grava(nome, amostras):
    os.makedirs(SAIDA, exist_ok=True)
    pico = max(1e-6, max(abs(v) for v in amostras))
    ganho = min(1.0, 0.85 / pico)
    with wave.open(os.path.join(SAIDA, nome + ".wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TAXA)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v * ganho)) * 32000)) for v in amostras))
    print("som", nome, f"{len(amostras) / TAXA:.2f}s")


random.seed(7)
grava("toque", tom(900, 650, 0.07, forma="suave", solta=0.8))
grava("pegar", tom(480, 900, 0.10, forma="suave"))
grava("soltar", tom(320, 170, 0.12, forma="suave", solta=0.8))
grava("nao", tom(330, 300, 0.12, forma="suave") + silencio(0.04) + tom(260, 230, 0.16, forma="suave"))
grava("moeda", tom(1320, 1320, 0.07, solta=0.5) + tom(1760, 1760, 0.22, solta=0.9))
grava("nivel", tom(784, 784, 0.10) + tom(988, 988, 0.10) + tom(1175, 1175, 0.10) + tom(1568, 1568, 0.35, solta=0.9))
grava("passagem", sopro(0.40))
grava("brilho", mistura(tom(1568, 2093, 0.25, vol=0.3, solta=0.9), silencio(0.06) + tom(2093, 2637, 0.2, vol=0.25)))
# bichinhos (provisório até ter gravação): cachorro, gato, cavalo e as pessoas
grava("cachorro", tom(520, 300, 0.11, forma="suave", ruido=0.25, ataque=0.005) + silencio(0.05)
      + tom(560, 320, 0.13, forma="suave", ruido=0.25, ataque=0.005))
grava("gato", tom(500, 760, 0.18, forma="suave", vibrato=0.01) + tom(760, 420, 0.30, forma="suave", vibrato=0.02))
grava("cavalo", tom(600, 1100, 0.15, forma="suave") + tom(1100, 500, 0.55, forma="suave", vibrato=0.06))
grava("pessoa", tom(660, 660, 0.09) + tom(880, 880, 0.16, solta=0.8))
