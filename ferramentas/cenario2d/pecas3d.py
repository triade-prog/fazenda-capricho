"""Troca as peças 2D provisórias pelas peças 3D transparentes (arte/cenario/<pasta>/png3d/).

Cada peça 3D é encaixada no mesmo quadro da peça 2D de mesmo nome: a imagem final tem o tamanho
da peça 2D e o desenho ocupa o lugar que o desenho 2D ocupava (centrado, apoiado embaixo). Assim
posições, toques, lugares de sentar e o modo Decorar continuam iguais.

Peças que são estados uma da outra (porta_aberta / porta_fechada, fogo_alto / fogo_baixo ...) usam a
mesma régua, para não pularem quando trocam. Se faltar o 3D de um dos estados, o par todo fica 2D
(é só não deixar o arquivo em png3d/).
"""
import os

from PIL import Image

ESTICA = 0.12      # quanto o desenho pode esticar para preencher melhor o quadro (12%)
EM_CIMA = ("luzinhas", "gancho", "toalha_gancho", "varal", "lustre")  # penduradas: alinham pelo alto


def _enche(pasta3d):
    arq = os.path.join(pasta3d, "_enche.txt")
    return open(arq, encoding="utf-8").read().split() if os.path.exists(arq) else []


def _sombra(pasta3d):
    arq = os.path.join(pasta3d, "_sombra.txt")
    return open(arq, encoding="utf-8").read().split() if os.path.exists(arq) else []


def _com_sombra(final, caixa):
    """Sombra macia embaixo da peça (apoiada no chão), dentro do próprio quadro."""
    from PIL import ImageDraw, ImageFilter
    x0, y0, x1, y1 = caixa
    w, h = x1 - x0, y1 - y0
    sh = max(4, h * 0.10)
    sombra = Image.new("RGBA", final.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse([x0 + w * 0.02, y1 - sh * 0.9, x1 - w * 0.02, y1 + sh * 0.6], fill=(70, 60, 30, 110))
    sombra = sombra.filter(ImageFilter.GaussianBlur(max(2, sh * 0.25)))
    sombra.alpha_composite(final)
    return sombra


def _prefixo(nome):
    return nome.rsplit("_", 1)[0] if "_" in nome else nome


def _uniao(caixas):
    caixas = [c for c in caixas if c]
    return (min(c[0] for c in caixas), min(c[1] for c in caixas),
            max(c[2] for c in caixas), max(c[3] for c in caixas))


def _grupo(nome, pasta3d, pasta2d):
    """Nomes que dividem a régua com `nome`: mesmo prefixo e mesmo tamanho de tela no 3D e no 2D."""
    im3 = Image.open(os.path.join(pasta3d, nome + ".png"))
    im2 = Image.open(os.path.join(pasta2d, nome + ".png"))
    g = []
    for f in sorted(os.listdir(pasta3d)):
        n = f[:-4]
        if not f.endswith(".png") or _prefixo(n) != _prefixo(nome):
            continue
        p2 = os.path.join(pasta2d, f)
        if not os.path.exists(p2):
            continue
        if Image.open(os.path.join(pasta3d, f)).size == im3.size and Image.open(p2).size == im2.size:
            g.append(n)
    return g or [nome]


def montar(nome, pasta3d, pasta2d):
    """Imagem final da peça, ou None se não houver versão 3D."""
    p3 = os.path.join(pasta3d, nome + ".png")
    if not os.path.exists(p3):
        return None
    grupo = _grupo(nome, pasta3d, pasta2d)
    base = Image.open(os.path.join(pasta2d, nome + ".png")).convert("RGBA")
    alvo = _uniao([Image.open(os.path.join(pasta2d, n + ".png")).convert("RGBA").getbbox() for n in grupo])
    if nome in _enche(pasta3d):  # peça avulsa (arte/objetos3d/): ocupa o quadro inteiro, não só o desenho 2D
        alvo = (0, 0) + base.size
    fonte = _uniao([Image.open(os.path.join(pasta3d, n + ".png")).convert("RGBA").getbbox() for n in grupo])
    aw, ah = alvo[2] - alvo[0], alvo[3] - alvo[1]
    fw, fh = fonte[2] - fonte[0], fonte[3] - fonte[1]
    sx, sy = aw / fw, ah / fh
    s = min(sx, sy)
    sx, sy = min(sx, s * (1 + ESTICA)), min(sy, s * (1 + ESTICA))
    im = Image.open(p3).convert("RGBA")
    caixa = im.getbbox()
    peca = im.crop(caixa)
    w, h = max(1, round(peca.width * sx)), max(1, round(peca.height * sy))
    peca = peca.resize((w, h), Image.LANCZOS)
    # posição do desenho dentro da régua do grupo, levada para o quadro 2D
    ox = alvo[0] + (aw - fw * sx) / 2 + (caixa[0] - fonte[0]) * sx
    if any(nome.startswith(k) for k in EM_CIMA):
        oy = alvo[1] + (caixa[1] - fonte[1]) * sy
    else:
        oy = alvo[3] - fh * sy + (caixa[1] - fonte[1]) * sy
    final = Image.new("RGBA", base.size, (0, 0, 0, 0))
    final.paste(peca, (round(ox), round(oy)), peca)
    if nome in _sombra(pasta3d):
        final = _com_sombra(final, final.getbbox())
    return final
