#!/usr/bin/env python3
"""Monta uma folha de pet a partir de TIRAS de animação geradas em fundo magenta (ex.: no ChatGPT).

Uso:
    python3 ferramentas/montar_pet.py --nome bob --saida arte/animacoes/bob_pet \\
        --linha idle:6:bob_idle.webp --linha running-right:8:bob_correndo.webp \\
        --espelhar running-left:running-right --base bob_base.png

Para cada tira: tira o fundo magenta (com borda suave e limpeza do reflexo magenta), separa os quadros
(fatias de largura igual), deixa o personagem com a MESMA altura em todas as ações (padrão: 296 px no
quadro 2x), alinha os pés na mesma linha do chão e monta:

    final/spritesheet-extended@2x.png   grade 8 x 11, quadros 384 x 416 (a que o jogo usa)
    final/spritesheet-extended.png      a mesma, reduzida para 192 x 208 (formato de pet)
    outras/pet_request.json             só com as ações entregues
    referencias/base.png                a pose base, se informada

Ações que faltam ficam de fora: o jogo usa as reações feitas por código até elas chegarem.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ORDEM = ["idle", "running-right", "running-left", "waving", "jumping", "failed", "waiting", "running",
         "review", "look-row-9", "look-row-10"]
CW, CH = 384, 416          # quadro 2x
CHAO = 404                 # linha do chão no quadro 2x (202 no 1x)
MAGENTA = np.array([250.0, 12.0, 250.0])


def sem_magenta(img: Image.Image) -> Image.Image:
    """Fundo magenta -> transparente, com borda suave e remoção do reflexo magenta na borda.
    Se a tira já vier com fundo transparente, só limpa a borda."""
    if img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info:
        rgba = img.convert("RGBA")
        if rgba.getchannel("A").getextrema()[0] < 10:
            alfa = rgba.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
            rgba.putalpha(alfa)
            return rgba
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    d = np.sqrt(((rgb - MAGENTA) ** 2).sum(axis=2))
    a = np.clip((d - 70.0) / (150.0 - 70.0), 0.0, 1.0)
    # reflexo magenta: vermelho e azul acima do verde, nas bordas (alfa parcial)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    spill = np.clip(np.minimum(r, b) - g, 0, None)
    borda = (a < 0.999)
    fator = np.where(borda, 0.9, 0.0)
    rgb[..., 0] = r - spill * fator
    rgb[..., 2] = b - spill * fator
    rgba = np.dstack([np.clip(rgb, 0, 255), a * 255.0]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    # some com fiapos soltos e afina 1 px de halo
    alfa = out.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    out.putalpha(alfa)
    return out


def quadros(tira: Image.Image, n: int):
    w, h = tira.size
    fw = w / n
    out = []
    for i in range(n):
        q = tira.crop((round(i * fw), 0, round((i + 1) * fw), h))
        bb = q.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox()
        out.append((q, bb))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nome", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--linha", action="append", default=[], help="ação:quadros:arquivo")
    ap.add_argument("--espelhar", action="append", default=[], help="ação_nova:ação_origem")
    ap.add_argument("--base")
    ap.add_argument("--altura", type=int, default=296, help="altura do personagem no quadro 2x")
    a = ap.parse_args()

    saida = Path(a.saida)
    for sub in ("final", "outras", "referencias"):
        (saida / sub).mkdir(parents=True, exist_ok=True)
    linhas = {}
    relatorio = []
    for spec in a.linha:
        estado, n, arq = spec.split(":", 2)
        tira = sem_magenta(Image.open(arq))
        qs = quadros(tira, int(n))
        alt = max(bb[3] - bb[1] for _, bb in qs)
        chao = max(bb[3] for _, bb in qs)
        esc = a.altura / alt
        celulas = []
        for q, bb in qs:
            g = q.resize((round(q.width * esc), round(q.height * esc)), Image.LANCZOS)
            if esc > 1.0:
                g = g.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=1))
            cel = Image.new("RGBA", (CW, CH))
            # centro da fatia -> centro do quadro; linha do chão da ação -> CHAO
            x = round(CW / 2 - g.width / 2)
            y = round(CHAO - chao * esc)
            cel.alpha_composite(g, (x, max(0, y)) if y >= 0 else (x, 0))
            if y < 0:
                cel = Image.new("RGBA", (CW, CH))
                cel.alpha_composite(g.crop((0, -y, g.width, g.height)), (x, 0))
            celulas.append(cel)
        linhas[estado] = celulas
        relatorio.append(f"{estado}: {n} quadros de {arq}; altura original {alt} px, escala {esc:.2f}x")
    for spec in a.espelhar:
        novo, origem = spec.split(":")
        linhas[novo] = [c.transpose(Image.FLIP_LEFT_RIGHT) for c in linhas[origem]]
        relatorio.append(f"{novo}: espelho de {origem}")

    folha2 = Image.new("RGBA", (CW * 8, CH * 11))
    rows = []
    for i, estado in enumerate(ORDEM):
        if estado not in linhas:
            continue
        for c, cel in enumerate(linhas[estado][:8]):
            folha2.alpha_composite(cel, (c * CW, i * CH))
        rows.append({"state": estado, "row": i, "frames": len(linhas[estado][:8])})
    folha2.save(saida / "final" / "spritesheet-extended@2x.png", optimize=True)
    folha2.resize((CW * 4, CH * 11 // 2), Image.LANCZOS).save(saida / "final" / "spritesheet-extended.png",
                                                               optimize=True)
    req = {"pet_id": a.nome, "display_name": a.nome.capitalize(),
           "atlas": {"columns": 8, "rows": 11, "cell_width": 192, "cell_height": 208, "width": 1536, "height": 2288},
           "rows": rows, "montado_por": "ferramentas/montar_pet.py",
           "faltam": [e for e in ORDEM if e not in linhas]}
    json.dump(req, open(saida / "outras" / "pet_request.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    if a.base:
        Image.open(a.base).save(saida / "referencias" / "base.png")
    (saida / "outras" / "LEIA-ME.md").write_text(
        f"# {a.nome.capitalize()} — folha montada a partir de tiras\n\n"
        + "\n".join(f"- {l}" for l in relatorio)
        + f"\n\nAções que ainda faltam: {', '.join(req['faltam']) or 'nenhuma'}.\n", encoding="utf-8")
    print("\n".join(relatorio))
    print(f"ok: {saida}/final/spritesheet-extended@2x.png  ({len(rows)} ações)")


if __name__ == "__main__":
    main()
