#!/usr/bin/env python3
"""Prepara uma folha de pet aprovada para o jogo.

Uso:
    python3 ferramentas/pet_para_jogo.py <pasta_do_pet> <nome_no_jogo> [--escala 2] [--colo 0.5] [--sono 3]
    ex.: python3 ferramentas/pet_para_jogo.py arte/animacoes/catarina_pet catarina

- Separa a folha em uma imagem por ação (prototipo/assets/personagens/<nome>_pet/<ação>.png): o jogo carrega
  só as ações em uso, o que poupa memória no iPad quando houver muitos personagens.
- Usa a folha de maior resolução que existir (@3x, depois @2x). Só com a folha 1x ela amplia cada ação
  (--escala, padrão 2) com filtro Lanczos e um leve reforço de nitidez.
- Corta as sobras transparentes em volta do personagem (a mesma janela em todos os quadros, centrada): a imagem
  de cada ação fica menor, gasta menos memória e cabe no limite de textura do Safari (4096 px).
- Escreve <nome>_pet.json com as ações (quadros, duração, se repete), a linha do chão, a altura do personagem,
  o ponto do colo (onde segura objetos, em fração da altura) e o quadro de olhos fechados usado para dormir.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageFilter

LIMITE_TEXTURA = 4096   # largura máxima segura de uma textura no Safari do iPad
FOLGA = 6               # px de folga em volta do recorte

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
    for alta in (pasta / "final" / "spritesheet-extended@3x.png", pasta / "final" / "spritesheet-extended@2x.png"):
        if alta.exists():
            # versão em alta resolução: usa direto, sem ampliar
            folha_alta = Image.open(alta).convert("RGBA")
            f = folha_alta.width / folha.width
            print(f"usando {alta.name} ({f:g}x), sem ampliar")
            folha, cw, ch, k = folha_alta, round(cw * f), round(ch * f), 1.0
            break
    if k != 1:
        folha = folha.resize((round(folha.width * k), round(folha.height * k)), Image.LANCZOS)
        folha = folha.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=1))
        cw, ch = round(cw * k), round(ch * k)
    idle = folha.crop((0, 0, cw, ch))
    bb = idle.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox()
    # janela de recorte: a mesma para todos os quadros, centrada no meio do quadro (o jogo ancora ali)
    x0, y0, x1, y1 = cw, ch, 0, 0
    for r in req["rows"]:
        for c in range(r["frames"]):
            q = folha.crop((c * cw, r["row"] * ch, (c + 1) * cw, (r["row"] + 1) * ch)).getchannel("A").getbbox()
            if q:
                x0, y0, x1, y1 = min(x0, q[0]), min(y0, q[1]), max(x1, q[2]), max(y1, q[3])
    meia = min(cw // 2, max(cw // 2 - x0, x1 - cw // 2) + FOLGA)
    jx0, jx1 = cw // 2 - meia, cw // 2 + meia
    jy0, jy1 = max(0, y0 - FOLGA), min(ch, max(y1, bb[3]) + FOLGA)
    jw, jh = jx1 - jx0, jy1 - jy0
    destino = Path("prototipo/assets/personagens")
    pasta_acoes = destino / f"{nome}_pet"
    pasta_acoes.mkdir(parents=True, exist_ok=True)
    rows = {}
    for velho in pasta_acoes.glob("*.png"):
        velho.unlink()     # ações de uma folha anterior que não existem mais
    for r in req["rows"]:
        tira = Image.new("RGBA", (jw * r["frames"], jh))
        for c in range(r["frames"]):
            q = folha.crop((c * cw + jx0, r["row"] * ch + jy0, c * cw + jx1, r["row"] * ch + jy1))
            tira.alpha_composite(q, (c * jw, 0))
        if tira.width > LIMITE_TEXTURA:
            print(f"AVISO: {r['state']} tem {tira.width} px de largura (limite seguro {LIMITE_TEXTURA})")
        tira.save(pasta_acoes / f"{r['state']}.png", optimize=True)
        rows[r["state"]] = {"sheet": f"{nome}_pet/{r['state']}.png", "frames": r["frames"],
                            "ms": MS.get(r["state"], 150), "loop": r["state"] not in UMA_VEZ}
    dados = {"_sobre": f"Folha de pet de {nome}, gerada por ferramentas/pet_para_jogo.py a partir de {pasta}.",
             "cell_width": jw, "cell_height": jh,
             "ground_y": bb[3] - jy0, "char_height": bb[3] - bb[1],
             "colo": a.colo, "sleep": {"state": "idle", "frame": a.sono}, "rows": rows}
    json.dump(dados, open(destino / f"{nome}_pet.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"ok: {destino / (nome + '_pet.json')}  {len(rows)} ações  quadro {jw}x{jh} (de {cw}x{ch})  "
          f"personagem {bb[3] - bb[1]} px")


if __name__ == "__main__":
    main()
