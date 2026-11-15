#!/usr/bin/env python3
"""Inventário de design dos cenários da Fazenda Capricho.

Lê prototipo/dados/cenarios/*.json e as imagens de prototipo/assets/cenario/<cenário>/ e escreve,
peça por peça, onde cada coisa está e o que pode estar errado:

- peça que parece flutuar (o pé não encosta no chão, numa superfície nem em outra peça);
- margem transparente embaixo da imagem (a peça "pisa" mais alto do que o retângulo diz);
- a mesma peça com tamanhos diferentes em cenários diferentes (vaso, lanterna, banquinho...);
- peça fora da área do cenário;
- coisa de pegar ou tocar menor que um dedo de criança no iPad;
- botões fixos da tela (ferradura, Decorar) cobrindo peças que dá para tocar.

Uso:  python3 ferramentas/analise_design/inventario.py [saida.md]
Sem argumento, escreve em analise_design/inventario.md (pasta ignorada pelo jogo).
Só lê arquivos: não muda nada no jogo.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

try:
    from PIL import Image
except ImportError:  # sem Pillow: pula a parte das margens transparentes
    Image = None

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DADOS = os.path.join(RAIZ, "prototipo", "dados", "cenarios")
ASSETS = os.path.join(RAIZ, "prototipo", "assets", "cenario")

# Tela de referência: iPad Air deitado (1180 x 820 pontos). O cenário tem 900 de altura,
# então 1 unidade do cenário = 820/900 pontos. A interface (CanvasLayer) é desenhada em 1600 x 1200
# e esticada para caber: 1 unidade da interface = min(1180/1600, 820/1200) pontos.
TELA = (1180, 820)
ALTURA_CENARIO = 900.0
PT_CENARIO = TELA[1] / ALTURA_CENARIO
PT_UI = min(TELA[0] / 1600.0, TELA[1] / 1200.0)

# Alvo mínimo de toque para criança pequena (em pontos). A Apple pede 44 pt para adultos;
# para 3 a 7 anos usamos 60 pt como mínimo e 75 pt como ideal.
TOQUE_MIN = 60.0
TOQUE_BOM = 75.0
FOLGA_PEGAR = 14.0  # toy.gd: hit() aceita o toque até 14 unidades fora do desenho (dos dois lados)
HORIZONTE_PADRAO = 560.0  # cenários ao ar livre: abaixo disso é chão (o chão está pintado no fundo)

# Botões fixos da tela (em unidades da interface, 1600 x 1200): x, y, largura, altura.
BOTOES = {
    "ferradura (mapa)": (18, 18, 140, 140),
    "poltrona (Decorar)": (18, 172, 140, 140),
}

# Nomes de peças que ficam na parede, no céu ou penduradas: não precisam tocar o chão.
NAO_PISA = re.compile(
    r"fundo|piso|parede|janela|quadro|pendurad|placa|seta|nuvem|sol\b|^sol$|telhado|oitao|toldo|"
    r"luzinha|varal|bandeir|ganch|prateleira|cortina|espelho|relogio|lustre|trepadeira|"
    r"abelha|borboleta|passarinho|bolha|vapor|chama|fogo$|cacho|moinho_helice|viga|"
    r"azulejo|flor_pendurada|escova_pendurada|pente_pendurado|cesto_pendurado|gancho|"
    r"arco_portal|longe|copa|escada_corda|torneira|chuveirinho|ducha|luzes|grade|estrada|grama|"
    r"lanterna_esq|lanterna_dir|janela_|porta"
)

# Famílias de peças que deviam ter o mesmo tamanho em todos os cenários.
FAMILIAS = {
    "vaso": re.compile(r"^(vaso|plantinha|planta$|vaso_flores)"),
    "lanterna": re.compile(r"^lanterna"),
    "banquinho/cadeira": re.compile(r"^(banquinho|cadeira|cadeirinha)"),
    "porta": re.compile(r"^porta($|_(?!retrato))"),
    "porta-retrato": re.compile(r"^porta_retrato"),
    "pedra": re.compile(r"^pedra"),
    "tigela": re.compile(r"^tigela"),
    "mesa": re.compile(r"^(mesa|mesinha)"),
    "árvore": re.compile(r"^(arvore|macieira|laranjeira|bananeira)"),
    "moita": re.compile(r"^(moita|arbusto|touceira|tufo|matinho)"),
}

_margem_cache = {}


def margem_baixo(cena, nome):
    """Fração da altura da imagem que é transparente embaixo (0 = o desenho encosta na borda)."""
    if Image is None:
        return None
    path = os.path.join(ASSETS, cena, nome + ".png")
    if not os.path.exists(path):
        return None
    if path not in _margem_cache:
        im = Image.open(path)
        if im.mode != "RGBA":
            _margem_cache[path] = 0.0
        else:
            a = im.getchannel("A").point(lambda v: 255 if v > 40 else 0)
            box = a.getbbox()
            _margem_cache[path] = 0.0 if not box else (im.height - box[3]) / im.height
    return _margem_cache[path]


def tem_sombra(cena, nome):
    """True se a faixa de baixo da imagem tem pixels meio transparentes e escuros (sombra pintada)."""
    if Image is None:
        return None
    path = os.path.join(ASSETS, cena, nome + ".png")
    if not os.path.exists(path):
        return None
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    faixa = im.crop((0, int(h * 0.85), w, h)).resize((max(1, w // 8), max(1, int(h * 0.15) // 8)))
    n = 0
    tot = 0
    px = faixa.tobytes()
    for k in range(0, len(px), 4):
        r, g, b, a = px[k], px[k + 1], px[k + 2], px[k + 3]
        if a > 0:
            tot += 1
            if 20 < a < 200 and (r + g + b) / 3 < 140:
                n += 1
    return tot > 0 and n / tot > 0.08


def apoios(d, pecas):
    """Alturas onde uma peça pode pousar: chão (topo do piso), superfícies e o topo de outras peças."""
    chao = []
    for nome, x, y, w, h in pecas:
        if nome.lstrip("@") in ("piso", "piso_varanda", "piso_pedrinhas", "grama", "deck"):
            chao.append((x, x + w, y, h))
    sup = [(s[0], s[1], s[2]) for s in d.get("superficies", [])]
    horizonte = min([c[2] for c in chao] + [HORIZONTE_PADRAO])
    return chao, sup, horizonte


def pisa_em_algo(p, i, pecas, chao, sup, horizonte, tol=14):
    nome, x, y, w, h = p
    base = y + h
    if base >= horizonte - tol and not chao:
        return "chão"
    cx0, cx1 = x + w * 0.25, x + w * 0.75
    for x0, x1, y0, hh in chao:  # pé dentro da faixa do chão
        if cx1 > x0 and cx0 < x1 and y0 - tol <= base <= y0 + hh + tol:
            return "chão"
    for x0, x1, sy in sup:
        if cx1 > x0 and cx0 < x1 and abs(base - sy) <= tol:
            return "superfície"
    for j, q in enumerate(pecas):
        if j == i:
            continue
        qn, qx, qy, qw, qh = q
        if qn.lstrip("@") in ("fundo", "fundo_patio", "fundo_dentro"):
            continue
        if cx1 > qx and cx0 < qx + qw and qy - tol <= base <= qy + qh:
            return "em cima de " + qn.lstrip("@")
    if base >= ALTURA_CENARIO - tol:
        return "borda de baixo"
    return None


def cobre(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def main():
    saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "analise_design", "inventario.md")
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    linhas = ["# Inventário de design dos cenários", "",
              "Gerado por `ferramentas/analise_design/inventario.py`. Medidas em unidades do cenário "
              "(altura 900) e, entre parênteses, em pontos do iPad Air deitado (1180 x 820).", ""]
    familias = defaultdict(list)
    resumo = defaultdict(int)

    for path in sorted(glob.glob(os.path.join(DADOS, "*.json"))):
        cena = os.path.splitext(os.path.basename(path))[0]
        d = json.load(open(path, encoding="utf-8"))
        largura = float(d.get("largura", 2200))
        pecas = [list(p[:5]) for p in d["pecas"]]
        chao, sup, horizonte = apoios(d, pecas)
        flutua, margem, fora, pequenos, sem_sombra, cobertos = [], [], [], [], [], []

        for i, p in enumerate(pecas):
            nome, x, y, w, h = p
            base_nome = nome.lstrip("@")
            for fam, rx in FAMILIAS.items():
                if rx.search(base_nome):
                    familias[fam].append((cena, base_nome, w, h))
            if x < -5 or y < -5 or x + w > largura + 5 or y + h > ALTURA_CENARIO + 5:
                fora.append(f"`{base_nome}` em ({x}, {y}) tamanho {w}x{h}")
            if NAO_PISA.search(base_nome) or w * h > largura * ALTURA_CENARIO * 0.25:
                continue
            onde = pisa_em_algo(p, i, pecas, chao, sup, horizonte)
            if onde is None:
                flutua.append(f"`{base_nome}` pé em y={y + h} (x {x}–{x + w})")
            m = margem_baixo(cena, base_nome)
            if m is not None and m > 0.06:
                margem.append(f"`{base_nome}`: {m:.0%} vazio embaixo (sobe {m * h:.0f} unidades)")
            s = tem_sombra(cena, base_nome)
            if s is False and onde in ("chão", "borda de baixo") and h > 60 and not base_nome.startswith("cerca"):
                sem_sombra.append(f"`{base_nome}`")

        # coisas de pegar: o pé (y) tem que estar no chão ou numa superfície
        for o in d.get("objetos", []):
            ox, oy = o["x"], o["y"]
            no_chao = oy >= horizonte - 14
            na_sup = any(x0 - 10 <= ox <= x1 + 10 and abs(oy - sy) <= 14 for x0, x1, sy in sup)
            if not (no_chao or na_sup):
                flutua.append(f"`{o['tipo']}` (de pegar) pé em ({ox:.0f}, {oy:.0f}), sem superfície embaixo")
        for o in d.get("objetos", []):
            w, h = o["w"] + 2 * FOLGA_PEGAR, o["h"] + 2 * FOLGA_PEGAR
            if min(w, h) * PT_CENARIO < TOQUE_MIN:
                pequenos.append(f"`{o['tipo']}` {o['w']}x{o['h']}, com a folga {w * PT_CENARIO:.0f}x{h * PT_CENARIO:.0f} pt")
        for iid, it in d.get("interativos", {}).items():
            w, h = it["w"], it["h"]
            if min(w, h) * PT_CENARIO < TOQUE_MIN:
                pequenos.append(f"`{iid}` (tocar) {w}x{h}, {w * PT_CENARIO:.0f}x{h * PT_CENARIO:.0f} pt")

        # botões fixos cobrindo coisas de tocar quando a câmera está no começo do cenário (x = 0)
        for bnome, (bx, by, bw, bh) in BOTOES.items():
            r_tela = (bx * PT_UI, by * PT_UI, bw * PT_UI, bh * PT_UI)
            r_cen = tuple(v / PT_CENARIO for v in r_tela)
            for iid, it in d.get("interativos", {}).items():
                if cobre(r_cen, (it["x"], it["y"], it["w"], it["h"])):
                    cobertos.append(f"{bnome} cobre `{iid}` com a câmera no começo do cenário")
            for o in d.get("objetos", []):
                if cobre(r_cen, (o["x"] - o["w"] / 2, o["y"] - o["h"], o["w"], o["h"])):
                    cobertos.append(f"{bnome} cobre `{o['tipo']}` com a câmera no começo do cenário")

        linhas.append(f"## {cena}")
        linhas.append("")
        linhas.append(f"Largura {largura:.0f} ({largura / ALTURA_CENARIO * TELA[1] / TELA[0]:.1f} telas), "
                      f"{len(pecas)} peças, {len(d.get('interativos', {}))} de tocar, "
                      f"{len(d.get('objetos', []))} de pegar, {len(d.get('lugares', []))} lugares, "
                      f"{len(d.get('superficies', []))} superfícies.")
        linhas.append("")
        for titulo, lista in [("Pode estar flutuando", flutua), ("Margem transparente embaixo", margem),
                              ("Sem sombra no chão", sem_sombra), ("Fora da área", fora),
                              ("Pequeno para o dedo", pequenos), ("Coberto por botão", cobertos)]:
            resumo[titulo] += len(lista)
            if lista:
                linhas.append(f"- **{titulo}** ({len(lista)}): " + "; ".join(lista))
        linhas.append("")
        linhas.append("<details><summary>Todas as peças (ordem de desenho)</summary>")
        linhas.append("")
        linhas.append("| # | peça | x | y | larg. | alt. |")
        linhas.append("|---|---|---|---|---|---|")
        for i, (nome, x, y, w, h) in enumerate(pecas):
            linhas.append(f"| {i} | {nome} | {x} | {y} | {w} | {h} |")
        linhas.append("")
        linhas.append("</details>")
        linhas.append("")

    linhas.append("## Mesma peça, tamanhos diferentes")
    linhas.append("")
    for fam, itens in sorted(familias.items()):
        tamanhos = sorted({(w, h) for _, _, w, h in itens})
        if len(tamanhos) > 1:
            resumo["Famílias com tamanhos diferentes"] += 1
            det = ", ".join(sorted({f"{n} {w}x{h} ({c})" for c, n, w, h in itens}))
            linhas.append(f"- **{fam}**: {len(tamanhos)} tamanhos. {det}")
    linhas.append("")
    linhas.insert(4, "**Resumo:** " + ", ".join(f"{k}: {v}" for k, v in resumo.items()) + ".\n")
    open(saida, "w", encoding="utf-8").write("\n".join(linhas))
    print("escrito em", saida)
    for k, v in resumo.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
