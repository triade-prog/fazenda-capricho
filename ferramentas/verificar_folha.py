#!/usr/bin/env python3
"""Confere uma folha de animação da Fazenda Capricho contra as regras do GDD (seção 7).

Uso:
    python3 ferramentas/verificar_folha.py FOLHA.png --altura 340 [--chao 480] [--colunas 4 --linhas 2]

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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folha")
    ap.add_argument("--altura", type=float, required=True, help="altura esperada do personagem no quadro, em px")
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
