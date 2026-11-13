"""Coloca um cenário 2D no protótipo: copia as peças para prototipo/assets/cenario/<cena>/ e escreve
prototipo/dados/cenarios/<cena>.json com a posição de cada peça (a mesma da prévia).

Uso: python3 ferramentas/cenario2d/para_jogo.py sala
O módulo do cenário precisa ter POS, P, W e JOGO (interativos, lugares, superficies).
Quando a peça 3D chegar com o mesmo nome, é só trocar o PNG em assets/cenario/<cena>/.
"""
import importlib
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import _tamanho  # noqa: E402
import placas  # noqa: E402
from PIL import Image  # noqa: E402

LIMITE = 4096

cena = sys.argv[1]
mod = importlib.import_module(cena)
raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
origem = os.path.join(raiz, "arte/cenario", getattr(mod, "PASTA", cena), "2d")
origem_placas = os.path.join(raiz, "arte/cenario", placas.PASTA, "2d")
P = dict(placas.P)
P.update(mod.P)
destino = os.path.join(raiz, "prototipo/assets/cenario", cena)
os.makedirs(destino, exist_ok=True)

inter = mod.JOGO["interativos"]
soltos = mod.JOGO.get("objetos", [])
pecas, usadas, objetos = [], set(), []
vistos = set()
for nome, x, y in list(mod.POS) + list(mod.JOGO.get("extras", [])):
    if nome.startswith("@") or nome in mod.JOGO.get("omitir", []):
        continue
    w, h = _tamanho(P[nome])
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
usadas.update(mod.JOGO.get("tambem", []))
faltam = {i for i in inter if inter[i]["estados"]} - vistos
assert not faltam, f"interativos sem posição na prévia: {faltam}"
for d in inter.values():
    if not d["estados"]:  # passagem sem imagem: x, y, w, h vêm do JOGO
        continue
    d["w"], d["h"] = _tamanho(P[d["estados"][0]])
for nome in sorted(usadas):
    pasta = origem if nome in mod.P else origem_placas
    de, para = os.path.join(pasta, nome + ".png"), os.path.join(destino, nome + ".png")
    im = Image.open(de)
    if im.width > LIMITE:  # iPads mais antigos não aceitam textura maior que 4096 px
        im.resize((LIMITE, round(im.height * LIMITE / im.width)), Image.LANCZOS).save(para)
    else:
        shutil.copyfile(de, para)
inter = {k: {a: b for a, b in d.items()} for k, d in inter.items()}
dados = {"id": cena, "largura": mod.W, "pecas": pecas, "interativos": inter, "objetos": objetos,
         "lugares": mod.JOGO["lugares"], "superficies": mod.JOGO["superficies"]}
os.makedirs(os.path.join(raiz, "prototipo/dados/cenarios"), exist_ok=True)
with open(os.path.join(raiz, "prototipo/dados/cenarios", cena + ".json"), "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=1)
print(f"{cena}: {len(usadas)} imagens em {destino}")
