"""Mapa da fazenda: botão da ferradura e figurinhas dos lugares (recortes das prévias 2D).

Gera arte/interface/mapa/*.png e copia para prototipo/assets/mapa/.
Quando a arte 3D chegar, é só trocar os PNGs (mesmos nomes; figurinhas 400 × 300).
Uso: python3 ferramentas/cenario2d/mapa.py [foto_do_quarto.png]
"""
import os
import shutil
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, L, svg, circ, path, coracao, salvar  # noqa: E402

raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dest = os.path.join(raiz, "arte/interface/mapa")
jogo = os.path.join(raiz, "prototipo/assets/mapa")
os.makedirs(dest, exist_ok=True)
os.makedirs(jogo, exist_ok=True)

# cena -> (prévia, x0, y0) do recorte de 800 × 600 em pixels do jogo
RECORTES = {
    "sala": ("sala/2d/previa.png", 860, 150),
    "cozinha": ("cozinha/2d/previa.png", 260, 130),
    "quarto_carol": ("quarto_carol/2d/previa.png", 760, 180),
    "sede": ("sede/2d/previa.png", 660, 60),
    "entrada": ("entrada/2d/previa.png", 700, 120),
    "estabulo": ("estabulo/2d/previa.png", 1000, 120),
    "plantacao": ("plantacao/2d/previa.png", 330, 280),
    "pet_care": ("pet_care/2d/previa.png", 640, 100),
    "casa_arvore": ("casa_arvore/2d/previa_fora.png", 470, 0),
    "casa_arvore_dentro": ("casa_arvore/2d/previa_dentro.png", 380, 260),
    "cabana": ("cabana/2d/previa.png", 640, 160),
    "casinha": ("casinha/2d/previa.png", 660, 80),
}
TW, TH, R, B = 400, 300, 44, 10


def figurinha(im):
    im = im.convert("RGB").resize((TW, TH), Image.LANCZOS)
    mask = Image.new("L", (TW * 2, TH * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, TW * 2 - 1, TH * 2 - 1), R * 2, fill=255)
    mask = mask.resize((TW, TH), Image.LANCZOS)
    out = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    borda = Image.new("RGBA", (TW * 2, TH * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(borda)
    d.rounded_rectangle((B, B, TW * 2 - 1 - B, TH * 2 - 1 - B), R * 2 - B, outline="#ffffff", width=B * 2)
    d.rounded_rectangle((0, 0, TW * 2 - 1, TH * 2 - 1), R * 2, outline=L, width=B)
    out.alpha_composite(borda.resize((TW, TH), Image.LANCZOS))
    return out


for cena, (arq, x0, y0) in RECORTES.items():
    im = Image.open(os.path.join(raiz, "arte/cenario", arq))
    figurinha(im.crop((x0, y0, x0 + 800, y0 + 600))).save(os.path.join(dest, cena + ".png"))
if len(sys.argv) > 1:  # o quarto da Catarina não tem prévia 2D: usa uma foto do jogo
    im = Image.open(sys.argv[1])
    w = round(im.height * 4 / 3)
    x0 = (im.width - w) // 2
    figurinha(im.crop((x0, 0, x0 + w, im.height))).save(os.path.join(dest, "quarto.png"))


def ferradura(cx, cy, k):
    return (path(f"M{cx-24*k},{cy+30*k} L{cx-30*k},{cy-2*k} A{30*k},{30*k} 0 0 1 {cx+30*k},{cy-2*k} L{cx+24*k},{cy+30*k} L{cx+9*k},{cy+30*k} "
                 f"L{cx+13*k},{cy-2*k} A{13*k},{13*k} 0 0 0 {cx-13*k},{cy-2*k} L{cx-9*k},{cy+30*k} Z", C["dourado"], 'stroke-width="4"') +
            coracao(cx, cy + 4 * k, 8 * k, C["rosa_forte"], 'stroke-width="2.5"'))


P = {
    "botao_mapa": svg(140, 140, circ(70, 74, 60, "#e9a9c6", 'stroke="none"') + circ(70, 68, 60, C["rosa_claro"], 'stroke-width="5"') +
                      circ(70, 68, 49, "#fff5fa", 'stroke-width="2.5"') + ferradura(70, 66, 1.0)),
    "botao_fechar": svg(110, 110, circ(55, 58, 46, "#e9a9c6", 'stroke="none"') + circ(55, 53, 46, C["branco"], 'stroke-width="5"') +
                        path("M38,36 L72,70 M72,36 L38,70", extra=f'stroke="{C["rosa_forte"]}" stroke-width="11"')),
    "aqui": svg(90, 90, coracao(45, 44, 34, C["rosa_forte"], 'stroke-width="5"') + coracao(45, 44, 18, C["branco"], 'stroke="none"')),
}
salvar(P, os.path.join(dest, "svg"), dest)
for f in os.listdir(dest):
    if f.endswith(".png"):
        shutil.copyfile(os.path.join(dest, f), os.path.join(jogo, f))
print(sorted(f for f in os.listdir(jogo) if f.endswith(".png")))
