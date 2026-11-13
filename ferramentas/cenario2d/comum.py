"""Base comum para desenhar as peças 2D provisórias dos cenários (SVG -> PNG).

Estilo igual às peças provisórias do quarto: desenho chapado, contorno marrom-arroxeado,
cores pastel. Tudo em pixels do jogo; o PNG sai em 2x (ou 4x nas peças pequenas).
"""
import math
import os
import subprocess

L = "#5b3a4f"          # contorno
SW = 3                 # espessura do contorno

C = dict(
    rosa="#ffb6d5", rosa_claro="#ffd6e8", rosa_forte="#ff6fae", rosa_chiclete="#ff8cc6",
    lilas="#d4b8f5", lilas_claro="#ece0ff", roxo="#a874e0", roxo_esc="#7d4fc0",
    madeira="#e6b47e", madeira_esc="#c98c56", madeira_clara="#f3d3a8", mel="#e9a95c",
    creme="#fff3dc", branco="#ffffff", verde="#93d47c", verde_esc="#6dbb5c",
    verde_claro="#bfe8a6", ceu="#bfe3fb", ceu_claro="#e6f5ff", amarelo="#ffd75e",
    azul="#8fc9f5", laranja="#ffb067", vermelho_rosa="#ef6f8c", dourado="#f2c14e",
    cinza="#d9d2dc", agua="#aee0fa",
)


def svg(w, h, corpo, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>'
            f'<g stroke="{L}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{corpo}</g></svg>')


def rr(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'


def circ(cx, cy, r, fill, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {extra}/>'


def ell(cx, cy, rx, ry, fill, extra=""):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def coracao(cx, cy, s, fill, extra=""):
    """Coração com largura ~2s, centrado em (cx, cy)."""
    d = (f"M{cx},{cy + s * 0.9} C{cx - s * 1.2},{cy + s * 0.1} {cx - s * 1.05},{cy - s * 0.95} {cx},{cy - s * 0.35} "
         f"C{cx + s * 1.05},{cy - s * 0.95} {cx + s * 1.2},{cy + s * 0.1} {cx},{cy + s * 0.9} Z")
    return path(d, fill, extra)


def estrela(cx, cy, r, fill, pontas=4, extra=""):
    pts = []
    for i in range(pontas * 2):
        a = math.pi * i / pontas - math.pi / 2
        rad = r if i % 2 == 0 else r * 0.38
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" {extra}/>'


def flor(cx, cy, r, petala, miolo=None, n=5):
    miolo = miolo or C["amarelo"]
    s = ""
    for i in range(n):
        a = 2 * math.pi * i / n
        s += circ(f"{cx + r * math.cos(a):.1f}", f"{cy + r * math.sin(a):.1f}", r * 0.75, petala,
                  'stroke-width="2"')
    return s + circ(cx, cy, r * 0.55, miolo, 'stroke-width="2"')


def nuvem(cx, cy, s):
    return (f'<g stroke="none" fill="#ffffff" opacity="0.95">'
            + circ(cx - s, cy, s * 0.7, "#fff") + circ(cx, cy - s * 0.35, s, "#fff")
            + circ(cx + s, cy, s * 0.75, "#fff") + rr(cx - s * 1.6, cy, s * 3.3, s * 0.65, s * 0.3, "#fff")
            + '</g>')


def salvar(pecas, pasta_svg, pasta_png):
    """pecas: dict nome -> svg. Grava os SVGs e gera os PNGs."""
    os.makedirs(pasta_svg, exist_ok=True)
    for nome, s in pecas.items():
        with open(os.path.join(pasta_svg, nome + ".svg"), "w", encoding="utf-8") as f:
            f.write(s)
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["node", os.path.join(raiz, "svg_para_png.js"), pasta_svg, pasta_png], check=True)


# ---------------------------------------------------------------- cenário completo

def _tamanho(svgtxt):
    import re
    return tuple(map(int, re.search(r'width="(\d+)" height="(\d+)"', svgtxt).groups()))


def montar(pasta, pecas, W, H, pos, saida, rotulos=False, legenda=""):
    """Monta a prévia do cenário. pos: lista de (nome, x, y); '@catarina' com os pés em (x, y)."""
    from PIL import Image, ImageDraw, ImageFont
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cat = Image.open(os.path.join(raiz, "arte/personagens/catarina.png")).convert("RGBA")
    cat = cat.crop(cat.getbbox())
    cat = cat.resize((round(cat.width * 300 / cat.height), 300), Image.LANCZOS)
    tela = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    caixas = []
    for nome, x, y in pos:
        if nome == "@catarina":
            tela.alpha_composite(cat, (round(x - cat.width / 2), round(y - 300)))
            continue
        w, h = _tamanho(pecas[nome])
        im = Image.open(os.path.join(pasta, nome + ".png")).convert("RGBA").resize((w, h), Image.LANCZOS)
        tela.alpha_composite(im, (round(x), round(y)))
        if not nome.startswith("fundo"):
            caixas.append((nome, x, y, w, h))
    if rotulos:
        d = ImageDraw.Draw(tela)
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
            fl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        except OSError:
            f = fl = ImageFont.load_default()
        for nome, x, y, w, h in caixas:
            d.rectangle((x, y, x + w, y + h), outline=(200, 40, 140), width=2)
        for nome, x, y, w, h in caixas:
            t = f"{nome} {w}×{h}"
            tw = d.textlength(t, font=f)
            tx, ty = x + 3, y + 3
            d.rectangle((tx - 2, ty - 1, tx + tw + 3, ty + 20), fill=(255, 255, 255, 215))
            d.text((tx, ty), t, fill=(150, 20, 100), font=f)
        if legenda:
            d.rectangle((0, H - 34, W, H), fill=(255, 255, 255, 225))
            d.text((12, H - 30), legenda, fill=(60, 30, 60), font=fl)
    tela.convert("RGB").save(saida)


def gerar_cenario(nome_pasta, pecas, W, H, pos, legenda, prompts_md, leia_me):
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    base = os.path.join(raiz, "arte/cenario", nome_pasta)
    d2 = os.path.join(base, "2d")
    salvar(pecas, os.path.join(d2, "svg"), d2)
    montar(d2, pecas, W, H, pos, os.path.join(d2, "previa.png"))
    montar(d2, pecas, W, H, pos, os.path.join(base, f"{nome_pasta}_layout.png"), True, legenda)
    with open(os.path.join(base, "PROMPTS.md"), "w", encoding="utf-8") as f:
        f.write(prompts_md)
    with open(os.path.join(d2, "LEIA-ME.md"), "w", encoding="utf-8") as f:
        f.write(leia_me)
    print(len(pecas), "peças em", d2)


REGRAS = """REGRAS PARA TODAS AS PEÇAS:
1. Uma peça por imagem, inteira, centralizada, sem cortar bordas.
2. Vista de frente, sem girar para o lado; luz suave de cima e um pouco da esquerda.
3. Fundo totalmente transparente (PNG). Se não der, magenta puro #FF00FF liso, sem magenta na peça.
4. Sem sombra no chão, sem texto, sem letras, sem números, sem moldura, sem personagens.
5. PEÇAS COM ESTADOS (ex.: fechada e aberta): todas as imagens do mesmo tamanho e com a base na MESMA
   posição, para o jogo trocar uma pela outra sem a peça "pular".
6. Proporção indicada em cada pedido (largura × altura, em pixels do jogo), no máximo 10% de diferença,
   e resolução de pelo menos o DOBRO desse tamanho.
7. Nada de personagens de filmes, desenhos ou marcas: tudo inventado."""


def textos(pasta, titulo, secao, fantasia, conceito, tela, tabela, aviso="", ordem=""):
    """tabela: lista de (peça, tamanho, estados, pedido, arquivos)."""
    linhas = "\n".join(f"| {i} | {p} | {t} | {e or '—'} | {d} |" for i, (p, t, e, d, _) in enumerate(tabela, 1))
    arquivos = "\n".join(f"- {p}: " + ", ".join(f"`{a}.png`" for a in arqs) for p, _, _, _, arqs in tabela)
    prompts = f"""# {titulo}: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção {secao}.
{aviso}
Layout na escala do jogo, nesta pasta: `{pasta}_layout.png` ({tela}). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `{pasta}_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`){conceito} e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário {titulo.upper()} do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). {fantasia}

ESTILO: igual às peças 3D anexadas do quarto: brinquedo 3D estilizado, formas arredondadas e macias,
materiais foscos e simples, madeira clara cor de mel, cores pastel da fazenda (rosa, lilás, roxo, verde);
fofo, sem realismo fotográfico.

REFERÊNCIAS: o layout anexado mostra posição e tamanho de cada peça; os desenhos dele são RASCUNHOS, não
copie o estilo. A Catarina tem 300 px de altura no jogo: use-a como régua.

{REGRAS}

Responda só "Entendido" e espere o primeiro pedido.
```

---

## Peças

Tamanhos em pixels do jogo. Para cada pedido, anexe também o PNG da peça em `2d/` como rascunho de forma.

| # | Peça | Tamanho | Estados | Pedido |
|---|---|---|---|---|
{linhas}
{ordem}
---

## Entrega

Suba os arquivos em `arte/cenario/{pasta}/3d/` com estes nomes (os mesmos da pasta `2d/`):

{arquivos}

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
"""
    leia = f"""# {titulo} — peças 2D provisórias

Desenhos 2D chapados, no estilo das peças provisórias do quarto, para montar o cenário no jogo agora.
Depois serão trocados pelas peças 3D (pasta `../3d/`), **com os mesmos nomes e tamanhos**: a troca é só
substituir o arquivo.

- Tamanhos da tabela do `../PROMPTS.md`, em 2x (peças de até 100 px em 4x).
- `previa.png`: as peças montadas com a Catarina (300 px). `../{pasta}_layout.png`: a mesma montagem com o
  nome e o tamanho de cada peça.
- `svg/`: o desenho vetorial de cada peça. Para refazer: `python3 ferramentas/cenario2d/{pasta}.py`.
"""
    return prompts, leia
