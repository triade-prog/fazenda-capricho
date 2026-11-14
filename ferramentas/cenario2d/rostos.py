"""Rostinhos redondos de quem faz pedidos na Plantação, recortados da arte dos personagens.

Uso: python3 ferramentas/cenario2d/rostos.py
Saída: prototipo/assets/cenario/plantacao/rosto_<quem>.png (120 x 120).
Se a arte de um personagem mudar, ajuste o recorte (x, y, lado) aqui e rode de novo.
"""
import os
from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECORTES = {"catarina": (66, 0, 252), "carol": (150, 25, 235), "lumi": (630, 0, 320)}
FUNDO = {"catarina": "#ffd9ea", "carol": "#e6d8ff", "lumi": "#fff0c2"}
T = 120

for quem, (x, y, lado) in RECORTES.items():
    im = Image.open(os.path.join(RAIZ, "prototipo/assets/personagens", quem + ".png")).convert("RGBA")
    rosto = im.crop((x, y, x + lado, y + lado)).resize((T * 4, T * 4), Image.LANCZOS)
    base = Image.new("RGBA", (T * 4, T * 4), FUNDO[quem])
    base.alpha_composite(rosto)
    masc = Image.new("L", (T * 4, T * 4), 0)
    ImageDraw.Draw(masc).ellipse([8, 8, T * 4 - 8, T * 4 - 8], fill=255)
    base.putalpha(masc)
    ImageDraw.Draw(base).ellipse([8, 8, T * 4 - 8, T * 4 - 8], outline="#5c3a4a", width=14)
    base.resize((T, T), Image.LANCZOS).save(os.path.join(RAIZ, "prototipo/assets/cenario/plantacao", f"rosto_{quem}.png"))
    print("rosto_" + quem)
