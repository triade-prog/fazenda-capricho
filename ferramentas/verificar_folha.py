#!/usr/bin/env python3
"""Confere uma folha de animação da Fazenda Capricho contra as regras do GDD (seção 7).

Uso:
    python3 ferramentas/verificar_folha.py FOLHA.png --pet pet_request.json [--altura 150]
    python3 ferramentas/verificar_folha.py FOLHA.png --altura 340 [--chao 480] [--colunas 4 --linhas 2]

O modo --pet confere uma folha no formato de pet do ChatGPT (padrão do projeto): uma linha por ação,
com o número de quadros de cada linha lido do pet_request.json.

Confere: tamanho divisível pela grade, fundo transparente, bordas dos quadros vazias (sem legendas
ou molduras), linha do chão fixa em todos os quadros, altura do personagem dentro de ±3% e
deslocamento horizontal do corpo (para ciclos "no lugar").
"""
import argparse
import sys

from PIL import Image

ALPHA = 128  # pixel considerado parte do desenho


def bbox_alpha(img):
    a = img.getchannel("A").point(lambda v: 255 if v >= ALPHA else 0)
    return a.getbbox()


# altura mínima (px) para o personagem ficar nítido no iPad na escala da tabela do GDD
MINIMO_NITIDO = 280

# ações em que os pés saem do chão de propósito
MOVIMENTO_LIVRE = {"jumping", "running-right", "running-left"}


def magenta(px):
    """Sobra do fundo de recorte #FF00FF: tom entre roxo e magenta (280°–320°), bem saturado.
    Rosa de língua e orelha (tom acima de 330°) não conta."""
    import colorsys

    r, g, b, a = px
    if a < 40:
        return False
    h, sat, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return 0.78 <= h <= 0.89 and sat > 0.3 and v > 0.55


def sobra_na_borda(q):
    """Conta pixels com tom de magenta só na BORDA do desenho (semitransparentes ou encostados no fundo).
    Roupas roxas ou lilás no meio do personagem não contam: sobra de recorte aparece na borda."""
    from PIL import ImageFilter

    a = q.getchannel("A")
    fundo = a.point(lambda v: 255 if v < 128 else 0).filter(ImageFilter.MaxFilter(3))
    n = 0
    dados = q.load()
    borda = fundo.load()
    w, h = q.size
    for y in range(h):
        for x in range(w):
            px = dados[x, y]
            if px[3] >= 40 and (px[3] < 250 or borda[x, y]) and magenta(px):
                n += 1
    return n


def verificar_pet(sheet, request_path, altura):
    import json

    req = json.load(open(request_path, encoding="utf-8"))
    at = req["atlas"]
    cw, ch = at["cell_width"], at["cell_height"]
    falhas, avisos = [], []
    k = sheet.size[0] / at["width"]  # 2 para a versão @2x
    if k >= 1 and abs(sheet.size[1] - at["height"] * k) < 1 and k == round(k):
        cw, ch = cw * int(k), ch * int(k)
        if k > 1:
            print(f"Versão em alta resolução: {int(k)}x a grade do pet_request.json")
    else:
        falhas.append(f"tamanho {sheet.size} diferente do combinado {at['width']}x{at['height']} (ou 2x)")
        k = 1
    usados = {}
    ref_altura = None
    for r in req["rows"]:
        usados[r["row"]] = r["frames"]
        chao, alt, resid = [], [], 0
        for c in range(r["frames"]):
            q = sheet.crop((c * cw, r["row"] * ch, (c + 1) * cw, (r["row"] + 1) * ch))
            bb = bbox_alpha(q)
            if bb is None:
                falhas.append(f"{r['state']} quadro {c}: vazio")
                continue
            chao.append(bb[3])
            alt.append(bb[3] - bb[1])
            resid += sobra_na_borda(q)
        if not alt:
            continue
        if r["state"] == "idle":
            ref_altura = max(alt)
        livre = r["state"] in MOVIMENTO_LIVRE
        print(f"  {r['state']:14s} {r['frames']} quadros  chão {min(chao)}–{max(chao)}  altura {min(alt)}–{max(alt)}"
              f"  sobra magenta {resid}")
        if not livre and max(chao) - min(chao) > 2 * k:
            falhas.append(f"{r['state']}: linha do chão varia {min(chao)}–{max(chao)} px")
        if resid > 0:
            avisos.append(f"{r['state']}: {resid} pixels com sobra do fundo magenta (conferir de perto)")
    for row in range(at["rows"]):
        for c in range(usados.get(row, 0), at["columns"]):
            q = sheet.crop((c * cw, row * ch, (c + 1) * cw, (row + 1) * ch))
            if bbox_alpha(q) is not None:
                falhas.append(f"linha {row} quadro {c}: deveria estar vazio")
    alvo = altura or ref_altura
    if altura and ref_altura and abs(ref_altura - altura) / altura > 0.03:
        falhas.append(f"altura na espera {ref_altura} px, esperada {altura:.0f} px (±3%)")
    if ref_altura and ref_altura < MINIMO_NITIDO:
        avisos.append(f"o personagem tem {ref_altura} px de altura: no iPad (tela 2x) ele aparece ampliado e fica "
                      f"menos nítido; para nitidez, gerar com pelo menos {MINIMO_NITIDO} px (quadro ~2x maior)")
    return falhas, avisos


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folha")
    ap.add_argument("--altura", type=float, default=None, help="altura esperada do personagem no quadro, em px")
    ap.add_argument("--pet", default=None, help="pet_request.json da folha (formato de pet do ChatGPT)")
    ap.add_argument("--chao", type=int, default=None, help="linha do chão esperada (y), em px; padrão: não confere")
    ap.add_argument("--colunas", type=int, default=4)
    ap.add_argument("--linhas", type=int, default=2)
    ap.add_argument("--tolerancia-chao", type=int, default=1)
    args = ap.parse_args()

    falhas = []
    sheet = Image.open(args.folha)
    print(f"Folha: {args.folha}  {sheet.size[0]}x{sheet.size[1]}  modo {sheet.mode}")
    if sheet.mode != "RGBA":
        falhas.append("a folha não tem canal de transparência (precisa ser PNG RGBA)")
        sheet = sheet.convert("RGBA")
    if args.pet:
        falhas, avisos = verificar_pet(sheet, args.pet, args.altura)
        for a in avisos:
            print("Aviso: " + a)
        if falhas:
            print("\nREPROVADA:")
            for f in falhas:
                print("  - " + f)
            sys.exit(1)
        print("\nAPROVADA")
        return
    if args.altura is None:
        ap.error("--altura é obrigatório fora do modo --pet")
    w, h = sheet.size
    if w % args.colunas or h % args.linhas:
        falhas.append(f"tamanho {w}x{h} não divide em {args.colunas}x{args.linhas} quadros iguais")
    fw, fh = w // args.colunas, h // args.linhas
    print(f"Quadros: {args.colunas}x{args.linhas} de {fw}x{fh}")

    chao, alturas, centros = [], [], []
    for i in range(args.colunas * args.linhas):
        x, y = (i % args.colunas) * fw, (i // args.colunas) * fh
        q = sheet.crop((x, y, x + fw, y + fh))
        bb = bbox_alpha(q)
        if bb is None:
            falhas.append(f"quadro {i}: vazio")
            continue
        if bb[0] == 0 or bb[1] == 0 or bb[2] == fw or bb[3] == fh:
            falhas.append(f"quadro {i}: o desenho encosta na borda do quadro (corte, moldura ou legenda?)")
        cantos = [q.getpixel(c)[3] for c in ((0, 0), (fw - 1, 0), (0, fh - 1), (fw - 1, fh - 1))]
        if max(cantos) > 0:
            falhas.append(f"quadro {i}: fundo não é transparente nos cantos")
        chao.append(bb[3])
        alturas.append(bb[3] - bb[1])
        centros.append((bb[0] + bb[2]) / 2)
        print(f"  quadro {i}: chão y={bb[3]:4d}  altura={bb[3] - bb[1]:4d}  centro x={(bb[0] + bb[2]) / 2:6.1f}")

    if chao:
        if max(chao) - min(chao) > args.tolerancia_chao:
            falhas.append(f"linha do chão varia {min(chao)}–{max(chao)} px: os pés devem ficar fixos no chão")
        if args.chao is not None and any(abs(c - args.chao) > args.tolerancia_chao for c in chao):
            falhas.append(f"linha do chão diferente da combinada ({args.chao} px)")
        media = sum(alturas) / len(alturas)
        if abs(media - args.altura) / args.altura > 0.03:
            falhas.append(f"altura média {media:.0f} px, esperada {args.altura:.0f} px (±3%)")
        print(f"Deslocamento horizontal do corpo: {max(centros) - min(centros):.0f} px")

    if falhas:
        print("\nREPROVADA:")
        for f in falhas:
            print("  - " + f)
        sys.exit(1)
    print("\nAPROVADA")


if __name__ == "__main__":
    main()
