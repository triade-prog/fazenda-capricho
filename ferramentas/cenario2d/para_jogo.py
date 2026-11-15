"""Coloca um cenário 2D no protótipo: copia as peças para prototipo/assets/cenario/<cena>/ e escreve
prototipo/dados/cenarios/<cena>.json com a posição de cada peça (a mesma da prévia).

Uso: python3 ferramentas/cenario2d/para_jogo.py sala
O módulo do cenário precisa ter POS, P, W e JOGO (interativos, lugares, superficies).
As peças 3D transparentes de arte/cenario/<pasta>/png3d/ entram no lugar das 2D de mesmo nome (pecas3d.py).
"""
import importlib
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import _tamanho  # noqa: E402
import comuns  # noqa: E402
import pecas3d  # noqa: E402

# 15/11/2026: Carol decidiu refazer toda a arte 3D do zero. As peças 3D novas ficam em
# arte/cenario/<pasta>/novo3d/; as antigas (png3d/) não entram mais no jogo.
USAR_3D = True
PASTA_3D = "novo3d"
import placas  # noqa: E402
import vida  # noqa: E402
from PIL import Image  # noqa: E402

LIMITE = 4096

cena = sys.argv[1]
mod = importlib.import_module(cena)
raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
origem = os.path.join(raiz, "arte/cenario", getattr(mod, "PASTA", cena), "2d")
origem_placas = os.path.join(raiz, "arte/cenario", placas.PASTA, "2d")
origem_comuns = os.path.join(raiz, "arte/cenario", comuns.PASTA, "2d")
P = dict(placas.P)
P.update(mod.P)
destino = os.path.join(raiz, "prototipo/assets/cenario", cena)
os.makedirs(destino, exist_ok=True)

vida.juntar(cena, mod.JOGO)
inter = mod.JOGO["interativos"]
soltos = mod.JOGO.get("objetos", [])
pecas, usadas, objetos = [], set(), []
vistos = set()
for nome, x, y, *esc in list(mod.POS) + list(mod.JOGO.get("extras", [])):
    if nome.startswith("@") or nome in mod.JOGO.get("omitir", []):
        continue
    w, h = _tamanho(P[nome])
    if esc:  # peça comum em outro tamanho (4º valor do POS)
        w, h = round(w * esc[0]), round(h * esc[0])
    alvo = next((i for i, d in inter.items() if nome in d["estados"] and d["x"] == x and d["y"] == y), None)
    if nome in soltos:  # objeto que dá para pegar: posição = centro da base
        objetos.append({"tipo": nome, "x": x + w / 2, "y": y + h, "w": w, "h": h})
        usadas.add(nome)
    elif alvo:
        pecas.append(["@" + alvo, x, y, w, h])
        inter[alvo].setdefault("estado", inter[alvo]["estados"].index(nome))
        vistos.add(alvo)
        usadas.update(inter[alvo]["estados"])
    else:
        pecas.append([nome, x, y, w, h])
        usadas.add(nome)
# objetos guardados dentro de um móvel que abre (geladeira): {id do interativo: [[peça, x, y], ...]}
for onde, lista in mod.JOGO.get("dentro", {}).items():
    for nome, x, y in lista:
        w, h = _tamanho(P[nome])
        objetos.append({"tipo": nome, "x": x, "y": y, "w": w, "h": h, "dentro": onde})
        usadas.add(nome)
usadas.update(mod.JOGO.get("tambem", []))
faltam = {i for i in inter if inter[i]["estados"]} - vistos
assert not faltam, f"interativos sem posição na prévia: {faltam}"
for d in inter.values():
    if not d["estados"]:  # passagem sem imagem: x, y, w, h vêm do JOGO
        continue
    d["w"], d["h"] = _tamanho(P[d["estados"][0]])
for nome in sorted(usadas):
    pasta = origem_comuns if nome in comuns.P else origem if nome in mod.P else origem_placas
    de, para = os.path.join(pasta, nome + ".png"), os.path.join(destino, nome + ".png")
    im = pecas3d.montar(nome, os.path.join(os.path.dirname(pasta), PASTA_3D), pasta) if USAR_3D else None
    if im is not None:  # peça 3D encaixada no quadro da peça 2D
        if im.width > LIMITE:
            im = im.resize((LIMITE, round(im.height * LIMITE / im.width)), Image.LANCZOS)
        im.save(para)
        continue
    im = Image.open(de)
    if im.width > LIMITE:  # iPads mais antigos não aceitam textura maior que 4096 px
        im.resize((LIMITE, round(im.height * LIMITE / im.width)), Image.LANCZOS).save(para)
    else:
        shutil.copyfile(de, para)
inter = {k: {a: b for a, b in d.items()} for k, d in inter.items()}


def pecas3d_cabe(nome):
    """Peça tirada do fundo que ainda cabe no modo Decorar (até 700 × 560, como no jogo)."""
    w, h = _tamanho(P[nome])
    return w <= 700 and h <= 560


dados = {"id": cena, "largura": mod.W, "pecas": pecas, "interativos": inter, "objetos": objetos,
         "lugares": mod.JOGO["lugares"], "superficies": mod.JOGO["superficies"],
         "animacoes": mod.JOGO.get("animacoes", {}), "moveis": mod.JOGO.get("moveis", []),
         "so_se": mod.JOGO.get("so_se", {}), "passagens": mod.JOGO.get("passagens", {}),
         "fundos": sorted({p[0] for p in getattr(mod, "S", None).pos if not pecas3d_cabe(p[0])} if hasattr(mod, "S") else [])}
os.makedirs(os.path.join(raiz, "prototipo/dados/cenarios"), exist_ok=True)
with open(os.path.join(raiz, "prototipo/dados/cenarios", cena + ".json"), "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=1)
print(f"{cena}: {len(usadas)} imagens em {destino}")
