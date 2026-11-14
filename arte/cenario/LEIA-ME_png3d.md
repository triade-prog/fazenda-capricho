# Peças 3D transparentes (png3d/)

Em 14/11/2026 chegou o pacote "Fazenda_Capricho_PNG_Transparente_14_Grupos" (381 PNGs; original completo em `png_3d_transparentes_r01/`). As peças de
objetos/ e interface/ foram copiadas para `arte/cenario/<cenário>/png3d/` (placas em `placas/png3d/`).

- `ferramentas/cenario2d/para_jogo.py <cena>` usa a peça 3D quando existe e encaixa no quadro da peça
  2D de mesmo nome (`pecas3d.py`), sem mudar posições, toques nem o modo Decorar.
- Ficaram de fora: fundos e prévias (pequenos demais), o quarto das meninas (o jogo já tem arte
  maior) e as 19 peças do PENDENCIAS.md do pacote, junto com o par delas (ex.: se morango_4 está em
  revisão, morango_0..3 também ficam 2D, para as fases combinarem).
- Para trocar uma peça: coloque o PNG novo em png3d/ com o mesmo nome e rode o para_jogo.py do cenário.
