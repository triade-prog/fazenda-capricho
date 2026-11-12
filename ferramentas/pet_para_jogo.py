#!/usr/bin/env python3
"""Prepara uma folha de pet aprovada para o jogo.

Uso:
    python3 ferramentas/pet_para_jogo.py <pasta_do_pet> <nome_no_jogo> [--escala 2] [--colo 0.5] [--sono 3]
    ex.: python3 ferramentas/pet_para_jogo.py arte/animacoes/catarina_pet catarina

- Separa a folha em uma imagem por ação (prototipo/assets/personagens/<nome>_pet/<ação>.png): o jogo carrega
  só as ações em uso, o que poupa memória no iPad quando houver muitos personagens.
- Amplia cada ação (--escala, padrão 2) com filtro Lanczos e um leve reforço de nitidez: fica bem mais nítido
  no iPad do que deixar a placa de vídeo ampliar. Use --escala 1 quando a folha já vier em alta resolução.
- Escreve <nome>_pet.json com as ações (quadros, duração, se repete), a linha do chão, a altura do personagem,
  o ponto do colo (onde segura objetos, em fração da altura) e o quadro de olhos fechados usado para dormir.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageFilter

MS = {"idle": 170, "running-right": 85, "running-left": 85, "waving": 140, "jumping": 110, "failed": 120,
      "waiting": 170, "running": 150, "review": 150, "look-row-9": 160, "look-row-10": 160}
UMA_VEZ = {"waving", "jumping", "failed"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("nome")
    ap.add_argument("--escala", type=float, default=2.0)
    ap.add_argument("--colo", type=float, default=0.5, help="altura do colo (fração da altura, a partir dos pés)")
    ap.add_argument("--sono", type=int, default=3, help="quadro da linha idle com olhos fechados")
    a = ap.parse_args()
    pasta, nome, k = Path(a.pasta), a.nome, a.escala
    req = json.load(open(pasta / "outras" / "pet_request.json", encoding="utf-8"))
    at = req["atlas"]
    cw, ch = at["cell_width"], at["cell_height"]
    folha = Image.open(pasta / "final" / "spritesheet-extended.png").convert("RGBA")
    alta = pasta / "final" / "spritesheet-extended@2x.png"
    if alta.exists():
        # versão em alta resolução entregue pela IA: usa direto, sem ampliar
        folha_alta = Image.open(alta).convert("RGBA")
        f = folha_alta.width / folha.width
        print(f"usando {alta.name} ({f:g}x), sem ampliar")
        folha, cw, ch, k = folha_alta, round(cw * f), round(ch * f), 1.0
    idle = folha.crop((0, 0, cw, ch))
    bb = idle.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox()
    destino = Path("prototipo/assets/personagens")
    pasta_acoes = destino / f"{nome}_pet"
    pasta_acoes.mkdir(parents=True, exist_ok=True)
    rows = {}
    for r in req["rows"]:
        tira = folha.crop((0, r["row"] * ch, r["frames"] * cw, (r["row"] + 1) * ch))
        if k != 1:
            tira = tira.resize((round(tira.width * k), round(tira.height * k)), Image.LANCZOS)
            tira = tira.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=1))
        tira.save(pasta_acoes / f"{r['state']}.png", optimize=True)
        rows[r["state"]] = {"sheet": f"{nome}_pet/{r['state']}.png", "frames": r["frames"],
                            "ms": MS.get(r["state"], 150), "loop": r["state"] not in UMA_VEZ}
    dados = {"_sobre": f"Folha de pet de {nome}, gerada por ferramentas/pet_para_jogo.py a partir de {pasta}.",
             "cell_width": round(cw * k), "cell_height": round(ch * k),
             "ground_y": round(bb[3] * k), "char_height": round((bb[3] - bb[1]) * k),
             "colo": a.colo, "sleep": {"state": "idle", "frame": a.sono}, "rows": rows}
    json.dump(dados, open(destino / f"{nome}_pet.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"ok: {destino / (nome + '_pet.json')}  {len(rows)} ações  quadro {round(cw * k)}x{round(ch * k)}  "
          f"personagem {round((bb[3] - bb[1]) * k)} px")


if __name__ == "__main__":
    main()
