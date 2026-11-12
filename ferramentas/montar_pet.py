#!/usr/bin/env python3
"""Monta uma folha de pet a partir de TIRAS de animação geradas em fundo magenta (ex.: no ChatGPT).

Uso:
    python3 ferramentas/montar_pet.py --nome bob --saida arte/animacoes/bob_pet \\
        --linha idle:6:bob_idle.webp --linha running-right:8:bob_correndo.webp \\
        --espelhar running-left:running-right --base bob_base.png

Para cada tira: tira o fundo magenta (com borda suave e limpeza do reflexo magenta), separa os quadros
(fatias de largura igual), deixa o personagem com a MESMA altura em todas as ações (padrão: 296 px no
quadro 2x), alinha os pés na mesma linha do chão e monta:

    final/spritesheet-extended@3x.png   com --resolucao 3: quadros 576 x 624 (o jogo prefere esta)
    final/spritesheet-extended@2x.png   grade 8 x 11, quadros 384 x 416
    final/spritesheet-extended.png      a mesma, reduzida para 192 x 208 (formato de pet)
    outras/pet_request.json             só com as ações entregues
    referencias/base.png                a pose base, se informada

Ações que faltam ficam de fora: o jogo usa as reações feitas por código até elas chegarem.

Use --resolucao 3 quando as tiras forem grandes (personagem com 450 px de altura ou mais na tira): no iPad o
personagem aparece com uns 550 pixels reais de altura, e a folha 3x fica bem mais nítida que a 2x.
"""
import sys
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ORDEM = ["idle", "running-right", "running-left", "waving", "jumping", "failed", "waiting", "running",
         "review", "look-row-9", "look-row-10"]
CW1, CH1, CHAO1 = 192, 208, 202   # quadro 1x e linha do chão (formato de pet)
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


def cortes(tira: Image.Image, n: int):
    """Onde cortar a tira em n quadros: perto de cada divisão igual, na coluna mais vazia
    (assim um braço ou uma trança que passa da divisão não é cortado)."""
    w, _ = tira.size
    fw = w / n
    col = np.asarray(tira.getchannel("A")).astype(np.int64).sum(axis=0)
    xs = [0]
    for i in range(1, n):
        c = round(i * fw)
        r = round(fw * 0.2)
        trecho = col[c - r:c + r]
        menor = trecho.min()
        candidatos = np.where(trecho == menor)[0]
        # entre colunas igualmente vazias, a mais perto da divisão igual
        xs.append(c - r + int(candidatos[np.argmin(np.abs(candidatos - r))]))
    xs.append(w)
    return xs


def quadros(tira: Image.Image, n: int):
    w, h = tira.size
    xs = cortes(tira, n)
    out = []
    for i in range(n):
        q = tira.crop((xs[i], 0, xs[i + 1], h))
        bb = q.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox()
        centro = (i + 0.5) * w / n - xs[i]      # centro da vaga igual, em coordenadas do quadro
        out.append((q, bb, centro))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nome", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--linha", action="append", default=[], help="ação:quadros:arquivo")
    ap.add_argument("--espelhar", action="append", default=[], help="ação_nova:ação_origem")
    ap.add_argument("--base")
    ap.add_argument("--altura", type=int, default=296, help="altura do personagem no quadro 2x")
    ap.add_argument("--resolucao", type=int, default=2, choices=(2, 3),
                    help="tamanho da folha principal: 2 (quadros 384 x 416) ou 3 (576 x 624)")
    ap.add_argument("--ajuste", action="append", default=[],
                    help="ação:fator — corrige a escala de uma ação (ex.: running-right:0.95 se a pose "
                         "correndo é naturalmente mais baixa que a pose parada)")
    a = ap.parse_args()
    ajustes = {e: float(f) for e, f in (s.split(":") for s in a.ajuste)}
    R = a.resolucao
    CW, CH, CHAO = CW1 * R, CH1 * R, CHAO1 * R
    altura = a.altura * R / 2

    saida = Path(a.saida)
    for sub in ("final", "outras", "referencias"):
        (saida / sub).mkdir(parents=True, exist_ok=True)
    linhas = {}
    relatorio = []
    for spec in a.linha:
        estado, n, arq = spec.split(":", 2)
        tira = sem_magenta(Image.open(arq))
        qs = quadros(tira, int(n))
        alt = max(bb[3] - bb[1] for _, bb, _ in qs)
        chao = max(bb[3] for _, bb, _ in qs)
        esc = altura / alt * ajustes.get(estado, 1.0)
        celulas = []
        for q, bb, centro in qs:
            g = q.resize((round(q.width * esc), round(q.height * esc)), Image.LANCZOS)
            if esc > 1.0:
                g = g.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=1))
            cel = Image.new("RGBA", (CW, CH))
            # centro da vaga -> centro do quadro; linha do chão da ação -> CHAO
            x = round(CW / 2 - centro * esc)
            y = round(CHAO - chao * esc)
            cel.alpha_composite(g, (x, max(0, y)) if y >= 0 else (x, 0))
            if y < 0:
                cel = Image.new("RGBA", (CW, CH))
                cel.alpha_composite(g.crop((0, -y, g.width, g.height)), (x, 0))
            celulas.append(cel)
        linhas[estado] = celulas
        relatorio.append(f"{estado}: {n} quadros de {Path(arq).name}; altura original {alt} px, escala {esc:.2f}x")
    for spec in a.espelhar:
        novo, origem = spec.split(":")
        linhas[novo] = [c.transpose(Image.FLIP_LEFT_RIGHT) for c in linhas[origem]]
        relatorio.append(f"{novo}: espelho de {origem}")

    folha = Image.new("RGBA", (CW * 8, CH * 11))
    rows = []
    for i, estado in enumerate(ORDEM):
        if estado not in linhas:
            continue
        for c, cel in enumerate(linhas[estado][:8]):
            folha.alpha_composite(cel, (c * CW, i * CH))
        rows.append({"state": estado, "row": i, "frames": len(linhas[estado][:8])})
    folha.save(saida / "final" / f"spritesheet-extended@{R}x.png", optimize=True)
    if R != 2:
        folha.resize((CW1 * 2 * 8, CH1 * 2 * 11), Image.LANCZOS).save(
            saida / "final" / "spritesheet-extended@2x.png", optimize=True)
    elif (saida / "final" / "spritesheet-extended@3x.png").exists():
        (saida / "final" / "spritesheet-extended@3x.png").unlink()   # sobra de uma montagem 3x anterior
    folha.resize((CW1 * 8, CH1 * 11), Image.LANCZOS).save(saida / "final" / "spritesheet-extended.png",
                                                           optimize=True)
    req = {"pet_id": a.nome, "display_name": a.nome.capitalize(),
           "atlas": {"columns": 8, "rows": 11, "cell_width": 192, "cell_height": 208, "width": 1536, "height": 2288},
           "rows": rows, "montado_por": "ferramentas/montar_pet.py", "resolucao": R,
           "faltam": [e for e in ORDEM if e not in linhas]}
    json.dump(req, open(saida / "outras" / "pet_request.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    base = saida / "referencias" / "base.png"
    if a.base and Path(a.base).resolve() != base.resolve():
        Image.open(a.base).save(base)
    comando = "python3 ferramentas/montar_pet.py " + " \\\n    ".join(
        f"{x} {y}" if x.startswith("--") else x for x, y in zip(sys.argv[1::2], sys.argv[2::2]))
    (saida / "outras" / "LEIA-ME.md").write_text(
        f"# {a.nome.capitalize()} — folha montada a partir de tiras\n\n"
        + "\n".join(f"- {l}" for l in relatorio)
        + f"\n\nAções que ainda faltam: {', '.join(req['faltam']) or 'nenhuma'}.\n"
        + f"\nPara montar de novo (da raiz do repositório):\n\n```bash\n{comando}\n```\n", encoding="utf-8")
    print("\n".join(relatorio))
    print(f"ok: {saida}/final/spritesheet-extended@{R}x.png  ({len(rows)} ações)")


if __name__ == "__main__":
    main()
