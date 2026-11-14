"""Botões do modo Decorar (arrumar móveis e enfeites dos cenários), no mesmo estilo do botão do mapa.

- botao_decorar: poltrona com uma mãozinha de arrastar (liga o modo Decorar);
- botao_pronto: certinho verde (sai do modo e guarda a arrumação).
Sem letras (regra do GDD). Gera arte/interface/decorar/*.png e copia para prototipo/assets/decorar/.
Uso: python3 ferramentas/cenario2d/botoes_decorar.py
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from comum import C, svg, circ, rr, path, coracao, salvar  # noqa: E402

raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dest = os.path.join(raiz, "arte/interface/decorar")
jogo = os.path.join(raiz, "prototipo/assets/decorar")
os.makedirs(dest, exist_ok=True)
os.makedirs(jogo, exist_ok=True)


def base(fundo):
    return (circ(70, 74, 60, "#e9a9c6", 'stroke="none"') + circ(70, 68, 60, C["rosa_claro"], 'stroke-width="5"') +
            circ(70, 68, 49, fundo, 'stroke-width="2.5"'))


def poltrona():
    return (rr(36, 54, 68, 38, 14, C["lilas"]) +              # encosto
            rr(30, 70, 18, 30, 8, C["roxo"]) + rr(92, 70, 18, 30, 8, C["roxo"]) +   # braços
            rr(44, 76, 52, 18, 7, C["lilas_claro"]) +          # assento
            path("M42,98 L40,106 M98,98 L100,106", extra='stroke-width="5"') +
            coracao(70, 66, 7, C["rosa_forte"], 'stroke-width="2"') +
            # setinhas de mover (esquerda e direita)
            path("M52,38 L88,38 M58,31 L50,38 L58,45 M82,31 L90,38 L82,45",
                 extra=f'stroke="{C["rosa_forte"]}" stroke-width="5"'))


P = {
    "botao_decorar": svg(140, 140, base("#fff5fa") + poltrona()),
    "botao_pronto": svg(140, 140, base("#effbe9") +
                        path("M44,70 L62,88 L98,50", extra=f'stroke="{C["verde_esc"]}" stroke-width="14"') +
                        path("M44,70 L62,88 L98,50", extra=f'stroke="{C["verde"]}" stroke-width="7"')),
}
salvar(P, os.path.join(dest, "svg"), dest)
for f in os.listdir(dest):
    if f.endswith(".png"):
        shutil.copyfile(os.path.join(dest, f), os.path.join(jogo, f))
print(sorted(f for f in os.listdir(jogo) if f.endswith(".png")))
