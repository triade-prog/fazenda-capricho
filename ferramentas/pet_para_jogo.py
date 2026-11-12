#!/usr/bin/env python3
"""Prepara uma folha de pet aprovada para o jogo.

Uso:
    python3 ferramentas/pet_para_jogo.py <pasta_do_pet> <nome_no_jogo>
    ex.: python3 ferramentas/pet_para_jogo.py arte/animacoes/catarina_pet catarina

Copia a folha para prototipo/assets/personagens/<nome>_pet.png e escreve <nome>_pet.json com a grade,
as ações (linha, quadros, duração, se repete), a linha do chão e a altura do personagem no quadro.
Depois basta chamar _add_pet("<nome>", "res://assets/personagens/<nome>_pet.json", altura, posição)
em prototipo/scripts/main.gd.
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

# duração de cada quadro (ms) por ação; ações de uma vez voltam para "idle" no fim
MS = {"idle": 170, "running-right": 85, "running-left": 85, "waving": 140, "jumping": 110, "failed": 120,
      "waiting": 170, "running": 150, "review": 150, "look-row-9": 160, "look-row-10": 160}
UMA_VEZ = {"waving", "jumping", "failed"}


def main():
    pasta, nome = Path(sys.argv[1]), sys.argv[2]
    req = json.load(open(pasta / "outras" / "pet_request.json", encoding="utf-8"))
    folha = pasta / "final" / "spritesheet-extended.png"
    at = req["atlas"]
    im = Image.open(folha).convert("RGBA")
    idle = im.crop((0, 0, at["cell_width"], at["cell_height"]))
    bb = idle.getchannel("A").point(lambda a: 255 if a >= 128 else 0).getbbox()
    rows = {r["state"]: {"row": r["row"], "frames": r["frames"], "ms": MS.get(r["state"], 150),
                         "loop": r["state"] not in UMA_VEZ} for r in req["rows"]}
    dados = {"_sobre": f"Folha de pet de {nome}, gerada por ferramentas/pet_para_jogo.py a partir de {pasta}.",
             "sheet": f"{nome}_pet.png", "columns": at["columns"], "rows_count": at["rows"],
             "cell_width": at["cell_width"], "cell_height": at["cell_height"],
             "ground_y": bb[3], "char_height": bb[3] - bb[1], "rows": rows}
    destino = Path("prototipo/assets/personagens")
    shutil.copyfile(folha, destino / f"{nome}_pet.png")
    json.dump(dados, open(destino / f"{nome}_pet.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"ok: {destino / (nome + '_pet.json')}  chão y={bb[3]}  altura={bb[3] - bb[1]} px no quadro")


if __name__ == "__main__":
    main()
