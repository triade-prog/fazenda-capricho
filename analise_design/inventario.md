# Inventário de design dos cenários

Gerado por `ferramentas/analise_design/inventario.py`. Medidas em unidades do cenário (altura 900) e, entre parênteses, em pontos do iPad Air deitado (1180 x 820).

**Resumo:** Pode estar flutuando: 7, Margem transparente embaixo: 0, Sem sombra no chão: 17, Fora da área: 14, Pequeno para o dedo: 42, Coberto por botão: 0, Famílias com tamanhos diferentes: 10.

## cabana

Largura 2200 (1.7 telas), 23 peças, 5 de tocar, 1 de pegar, 1 lugares, 0 superfícies.

- **Fora da área** (1): `cerca` em (2080, 518) tamanho 416x92
- **Pequeno para o dedo** (2): `lanterna` (tocar) 60x100, 55x91 pt; `livro` (tocar) 70x50, 64x46 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2200 | 900 |
| 1 | grama | 0 | 600 | 1100 | 300 |
| 2 | grama | 1100 | 600 | 1100 | 300 |
| 3 | arvore_flores | 45 | 120 | 409 | 500 |
| 4 | arvore_flores | 1774 | 140 | 393 | 480 |
| 5 | cerca | 0 | 518 | 416 | 92 |
| 6 | cerca | 416 | 518 | 416 | 92 |
| 7 | cerca | 832 | 518 | 416 | 92 |
| 8 | cerca | 1248 | 518 | 416 | 92 |
| 9 | cerca | 1664 | 518 | 416 | 92 |
| 10 | cerca | 2080 | 518 | 416 | 92 |
| 11 | varal_bandeirinhas | 240 | 240 | 1730 | 180 |
| 12 | @cabana | 820 | 230 | 460 | 380 |
| 13 | saco_dormir | 890 | 500 | 320 | 90 |
| 14 | @lanterna | 1020 | 420 | 60 | 100 |
| 15 | @fogueira | 1400 | 560 | 170 | 120 |
| 16 | chama | 1450 | 580 | 70 | 70 |
| 17 | tronco_banco | 1560 | 600 | 200 | 80 |
| 18 | tronco_banco | 1180 | 690 | 200 | 80 |
| 19 | @livro | 640 | 690 | 70 | 50 |
| 20 | livro_fechado | 560 | 700 | 70 | 50 |
| 21 | passarinho | 1880 | 300 | 40 | 35 |
| 22 | @seta_arvore | 200 | 470 | 120 | 160 |

</details>

## casa_arvore

Largura 2600 (2.0 telas), 44 peças, 9 de tocar, 2 de pegar, 0 lugares, 1 superfícies.

- **Sem sombra no chão** (2): `pilar`; `pilar`
- **Fora da área** (2): `cerca` em (2496, 518) tamanho 416x92; `grama` em (2200, 600) tamanho 1100x300
- **Pequeno para o dedo** (1): `frutinha` 28x36, com a folga 51x58 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo_patio | 0 | 0 | 2600 | 900 |
| 1 | cerca | 0 | 518 | 416 | 92 |
| 2 | cerca | 416 | 518 | 416 | 92 |
| 3 | cerca | 832 | 518 | 416 | 92 |
| 4 | cerca | 1248 | 518 | 416 | 92 |
| 5 | cerca | 1664 | 518 | 416 | 92 |
| 6 | cerca | 2080 | 518 | 416 | 92 |
| 7 | cerca | 2496 | 518 | 416 | 92 |
| 8 | grama | 0 | 600 | 1100 | 300 |
| 9 | grama | 1100 | 600 | 1100 | 300 |
| 10 | grama | 2200 | 600 | 1100 | 300 |
| 11 | arbusto | 200 | 515 | 300 | 99 |
| 12 | arbusto | 2130 | 515 | 300 | 99 |
| 13 | copa | 495 | 20 | 905 | 448 |
| 14 | @cacho_1 | 560 | 170 | 70 | 70 |
| 15 | @cacho_2 | 1310 | 200 | 70 | 70 |
| 16 | @cacho_3 | 545 | 330 | 70 | 70 |
| 17 | tronco | 779 | 380 | 324 | 225 |
| 18 | tufo | 915 | 572 | 56 | 48 |
| 19 | viga_esq | 745 | 410 | 144 | 74 |
| 20 | viga_dir | 995 | 412 | 144 | 47 |
| 21 | parede_casinha | 745 | 179 | 410 | 201 |
| 22 | janela_casinha | 1018 | 213 | 90 | 92 |
| 23 | @porta | 798 | 180 | 103 | 200 |
| 24 | oitao | 750 | 121 | 400 | 67 |
| 25 | telhado | 715 | 95 | 470 | 99 |
| 26 | grade_varanda | 735 | 322 | 650 | 60 |
| 27 | piso_varanda | 622 | 376 | 668 | 50 |
| 28 | escada_madeira | 640 | 335 | 78 | 270 |
| 29 | escada_corda | 1105 | 360 | 71 | 245 |
| 30 | pilar | 1300 | 425 | 23 | 180 |
| 31 | pilar | 1385 | 425 | 23 | 180 |
| 32 | @escorregador | 1268 | 392 | 480 | 185 |
| 33 | balanco_estrutura | 1870 | 230 | 281 | 380 |
| 34 | trepadeira | 1872 | 295 | 49 | 300 |
| 35 | trepadeira | 2100 | 295 | 49 | 300 |
| 36 | balanco_assento | 1945 | 255 | 130 | 295 |
| 37 | mesa_piquenique | 2200 | 650 | 320 | 130 |
| 38 | toalha | 2195 | 650 | 310 | 45 |
| 39 | banco_piquenique | 2185 | 712 | 330 | 65 |
| 40 | @cesto | 2290 | 752 | 90 | 88 |
| 41 | @seta_sede | 40 | 520 | 136 | 160 |
| 42 | @seta_cabana | 2460 | 470 | 108 | 160 |
| 43 | @seta_casinha | 2040 | 640 | 120 | 160 |

</details>

## casa_arvore_dentro

Largura 1600 (1.2 telas), 13 peças, 4 de tocar, 5 de pegar, 1 lugares, 2 superfícies.

- **Sem sombra no chão** (1): `cama`
- **Pequeno para o dedo** (3): `panelinha` 56x30, com a folga 77x53 pt; `xicara_cha` 24x27, com a folga 47x50 pt; `passarinho` (tocar) 44x34, 40x31 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo_dentro | 0 | 0 | 1600 | 900 |
| 1 | luzinhas | -4 | 40 | 1608 | 66 |
| 2 | janela_redonda | 628 | 98 | 344 | 344 |
| 3 | @passarinho | 830 | 100 | 44 | 34 |
| 4 | @porta | 1440 | 340 | 130 | 300 |
| 5 | cama | 60 | 550 | 360 | 150 |
| 6 | @fogaozinho | 470 | 460 | 220 | 200 |
| 7 | tapete | 520 | 790 | 300 | 80 |
| 8 | cadeirinha | 840 | 620 | 60 | 80 |
| 9 | mesinha_cha | 780 | 680 | 180 | 80 |
| 10 | cadeirinha_dir | 720 | 720 | 60 | 80 |
| 11 | cadeirinha_esq | 960 | 720 | 60 | 80 |
| 12 | @bau | 1040 | 500 | 160 | 160 |

</details>

## casinha

Largura 2200 (1.7 telas), 20 peças, 4 de tocar, 4 de pegar, 0 lugares, 2 superfícies.

- **Sem sombra no chão** (2): `casinha_interior`; `casinha`
- **Fora da área** (1): `cerca` em (2080, 518) tamanho 416x92
- **Pequeno para o dedo** (3): `potinho_rosa` 30x40, com a folga 53x62 pt; `potinho_lilas` 30x40, com a folga 53x62 pt; `potinho_amarelo` 30x40, com a folga 53x62 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2200 | 900 |
| 1 | grama | 0 | 600 | 1100 | 300 |
| 2 | grama | 1100 | 600 | 1100 | 300 |
| 3 | arvore_flores | 1802 | 160 | 376 | 460 |
| 4 | cerca | 0 | 518 | 416 | 92 |
| 5 | cerca | 416 | 518 | 416 | 92 |
| 6 | cerca | 832 | 518 | 416 | 92 |
| 7 | cerca | 1248 | 518 | 416 | 92 |
| 8 | cerca | 1664 | 518 | 416 | 92 |
| 9 | cerca | 2080 | 518 | 416 | 92 |
| 10 | casinha_interior | 780 | 130 | 560 | 480 |
| 11 | prateleira | 910 | 300 | 300 | 130 |
| 12 | @maleta | 1120 | 268 | 110 | 90 |
| 13 | casinha | 780 | 130 | 560 | 480 |
| 14 | @toldo | 840 | 222 | 440 | 130 |
| 15 | balcao | 870 | 480 | 380 | 60 |
| 16 | @caixa | 920 | 410 | 90 | 80 |
| 17 | placa_pata | 1015 | 150 | 90 | 80 |
| 18 | cadeirinha | 1400 | 480 | 80 | 120 |
| 19 | @seta_arvore | 200 | 470 | 120 | 160 |

</details>

## cozinha

Largura 2200 (1.7 telas), 31 peças, 8 de tocar, 7 de pegar, 0 lugares, 4 superfícies.

- **Pode estar flutuando** (5): `maca` (de pegar) pé em (365, 300), sem superfície embaixo; `banana` (de pegar) pé em (445, 300), sem superfície embaixo; `copo_leite` (de pegar) pé em (365, 400), sem superfície embaixo; `queijo` (de pegar) pé em (450, 400), sem superfície embaixo; `cenoura` (de pegar) pé em (410, 490), sem superfície embaixo
- **Sem sombra no chão** (2): `fogao`; `pia`
- **Pequeno para o dedo** (10): `xicara` 40x36, com a folga 62x58 pt; `sanduiche` 50x34, com a folga 71x56 pt; `maca` 30x32, com a folga 53x55 pt; `copo_leite` 34x44, com a folga 56x66 pt; `queijo` 44x32, com a folga 66x55 pt; `cenoura` 52x26, com a folga 73x49 pt; `prato_pia` (tocar) 60x30, 55x27 pt; `tigela_cao` (tocar) 80x40, 73x36 pt; `tigela_gato` (tocar) 80x40, 73x36 pt; `tigela_lumi` (tocar) 80x40, 73x36 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2200 | 900 |
| 1 | piso | 0 | 578 | 2200 | 324 |
| 2 | janela | 1156 | 128 | 278 | 214 |
| 3 | azulejos | 540 | 320 | 320 | 120 |
| 4 | azulejos | 860 | 320 | 320 | 120 |
| 5 | azulejos | 1180 | 320 | 320 | 120 |
| 6 | armario | 555 | 420 | 160 | 184 |
| 7 | armario | 705 | 420 | 160 | 184 |
| 8 | armario | 855 | 420 | 160 | 184 |
| 9 | armario | 1005 | 420 | 160 | 184 |
| 10 | armario | 1155 | 420 | 160 | 184 |
| 11 | armario | 1305 | 420 | 160 | 184 |
| 12 | prateleira | 552 | 40 | 556 | 104 |
| 13 | panelas | 552 | 192 | 556 | 112 |
| 14 | @porta_sala | 60 | 250 | 170 | 350 |
| 15 | placa_casa | 110 | 180 | 70 | 60 |
| 16 | @geladeira | 300 | 170 | 238 | 430 |
| 17 | @fogao | 600 | 340 | 240 | 260 |
| 18 | vapor | 665 | 234 | 110 | 146 |
| 19 | @torneira | 1318 | 404 | 80 | 70 |
| 20 | pia | 1200 | 400 | 260 | 200 |
| 21 | @prato_pia | 1240 | 420 | 60 | 30 |
| 22 | vaso_flores | 1000 | 350 | 70 | 90 |
| 23 | cadeira | 1455 | 470 | 160 | 230 |
| 24 | mesa | 1560 | 500 | 420 | 200 |
| 25 | cadeira | 1965 | 470 | 160 | 230 |
| 26 | prato_limpo | 1640 | 528 | 60 | 30 |
| 27 | vaso_flores | 1910 | 468 | 70 | 90 |
| 28 | @tigela_cao | 700 | 760 | 80 | 40 |
| 29 | @tigela_gato | 800 | 760 | 80 | 40 |
| 30 | @tigela_lumi | 900 | 760 | 80 | 40 |

</details>

## entrada

Largura 2200 (1.7 telas), 25 peças, 6 de tocar, 2 de pegar, 0 lugares, 0 superfícies.

- **Fora da área** (1): `cerca` em (1876, 518) tamanho 416x92
- **Pequeno para o dedo** (4): `cartinha` 50x36, com a folga 71x58 pt; `flor` 25x55, com a folga 48x76 pt; `lanterna_esq` (tocar) 60x110, 55x100 pt; `lanterna_dir` (tocar) 60x110, 55x100 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2200 | 900 |
| 1 | celeiro_longe | 1644 | 344 | 152 | 132 |
| 2 | casinha_longe | 1836 | 408 | 88 | 76 |
| 3 | casinha_longe | 376 | 414 | 88 | 76 |
| 4 | arvore_flores | 57 | 250 | 246 | 300 |
| 5 | arvore_flores | 1947 | 240 | 246 | 300 |
| 6 | cerca | 0 | 518 | 416 | 92 |
| 7 | cerca | 416 | 518 | 416 | 92 |
| 8 | cerca | 1460 | 518 | 416 | 92 |
| 9 | cerca | 1876 | 518 | 416 | 92 |
| 10 | grama | 0 | 600 | 1100 | 300 |
| 11 | grama | 1100 | 600 | 1100 | 300 |
| 12 | estrada | 676 | 596 | 848 | 308 |
| 13 | pilar | 728 | 280 | 104 | 330 |
| 14 | pilar | 1368 | 280 | 104 | 330 |
| 15 | moinho_torre | 420 | 220 | 200 | 380 |
| 16 | moinho_helice | 400 | 120 | 240 | 240 |
| 17 | @portao | 820 | 330 | 560 | 280 |
| 18 | arco_portal | 690 | 140 | 820 | 220 |
| 19 | @lanterna_esq | 750 | 330 | 60 | 110 |
| 20 | @lanterna_dir | 1390 | 330 | 60 | 110 |
| 21 | @floreira_esq | 520 | 560 | 220 | 110 |
| 22 | @floreira_dir | 1490 | 560 | 220 | 110 |
| 23 | @correio | 1660 | 450 | 122 | 170 |
| 24 | banco | 220 | 540 | 260 | 110 |

</details>

## estabulo

Largura 4300 (3.3 telas), 83 peças, 13 de tocar, 13 de pegar, 0 lugares, 3 superfícies.

- **Sem sombra no chão** (2): `caixote_frutas`; `lanterna_jardim`
- **Fora da área** (2): `cerca` em (4088, 518) tamanho 416x92; `pedra` em (2440, 850) tamanho 110x60
- **Pequeno para o dedo** (5): `feno` 70x36, com a folga 89x58 pt; `cenoura` 36x54, com a folga 58x75 pt; `margarida` 30x60, com a folga 53x80 pt; `margarida` 30x60, com a folga 53x80 pt; `lanterna` (tocar) 52x110, 47x100 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 4300 | 900 |
| 1 | arvore | 2900 | 60 | 480 | 540 |
| 2 | arvore | 180 | 60 | 480 | 540 |
| 3 | cerca | 2840 | 518 | 416 | 92 |
| 4 | cerca | 3256 | 518 | 416 | 92 |
| 5 | cerca | 3672 | 518 | 416 | 92 |
| 6 | cerca | 4088 | 518 | 416 | 92 |
| 7 | cerca | 0 | 518 | 416 | 92 |
| 8 | cerca | 416 | 518 | 416 | 92 |
| 9 | cerca | 832 | 518 | 416 | 92 |
| 10 | pedra_caminho | 310 | 849 | 100 | 38 |
| 11 | pedra_caminho | 405 | 796 | 100 | 38 |
| 12 | pedra_caminho | 510 | 749 | 100 | 38 |
| 13 | pedra_caminho | 625 | 709 | 100 | 38 |
| 14 | pedra_caminho | 745 | 676 | 100 | 38 |
| 15 | pedra_caminho | 855 | 649 | 100 | 38 |
| 16 | pedra_caminho | 2650 | 631 | 100 | 38 |
| 17 | pedra_caminho | 2695 | 681 | 100 | 38 |
| 18 | pedra_caminho | 2750 | 733 | 100 | 38 |
| 19 | pedra_caminho | 2820 | 781 | 100 | 38 |
| 20 | pedra_caminho | 2910 | 831 | 100 | 38 |
| 21 | pedra_caminho | 3010 | 859 | 100 | 38 |
| 22 | parede_estabulo | 992 | 106 | 1512 | 500 |
| 23 | telhado_estabulo | 990 | 30 | 1556 | 177 |
| 24 | flor_pendurada_lilas | 1058 | 168 | 44 | 80 |
| 25 | flor_pendurada_rosa | 1178 | 168 | 44 | 80 |
| 26 | flor_pendurada_lilas | 1298 | 168 | 44 | 80 |
| 27 | flor_pendurada_rosa | 1418 | 168 | 44 | 80 |
| 28 | flor_pendurada_lilas | 1538 | 168 | 44 | 80 |
| 29 | flor_pendurada_rosa | 1658 | 168 | 44 | 80 |
| 30 | flor_pendurada_lilas | 1778 | 168 | 44 | 80 |
| 31 | flor_pendurada_rosa | 1898 | 168 | 44 | 80 |
| 32 | flor_pendurada_lilas | 2018 | 168 | 44 | 80 |
| 33 | flor_pendurada_rosa | 2138 | 168 | 44 | 80 |
| 34 | flor_pendurada_lilas | 2258 | 168 | 44 | 80 |
| 35 | flor_pendurada_rosa | 2378 | 168 | 44 | 80 |
| 36 | cesto_pendurado | 1080 | 200 | 180 | 250 |
| 37 | ferradura | 1330 | 250 | 115 | 120 |
| 38 | suporte_manta | 1500 | 260 | 140 | 120 |
| 39 | prateleira_banho | 1870 | 330 | 280 | 44 |
| 40 | ganchos | 1895 | 380 | 230 | 45 |
| 41 | pente_pendurado | 1915 | 410 | 32 | 118 |
| 42 | escova_pendurada | 1982 | 410 | 50 | 125 |
| 43 | espelho | 2050 | 410 | 70 | 120 |
| 44 | @ducha | 2170 | 190 | 240 | 430 |
| 45 | @lanterna | 2395 | 150 | 52 | 110 |
| 46 | trepadeira_flores | 2440 | 180 | 70 | 420 |
| 47 | @cocho | 1050 | 450 | 300 | 210 |
| 48 | @banheira | 1830 | 500 | 340 | 190 |
| 49 | @balde | 2250 | 590 | 110 | 136 |
| 50 | tapete_coracao | 1760 | 712 | 300 | 100 |
| 51 | caixote_frutas | 1030 | 650 | 260 | 170 |
| 52 | tigela_racao | 1430 | 770 | 160 | 70 |
| 53 | tigela_agua | 1610 | 770 | 160 | 70 |
| 54 | fardo | 2060 | 720 | 210 | 136 |
| 55 | fardo | 2275 | 730 | 210 | 136 |
| 56 | @porteira | 2540 | 420 | 300 | 200 |
| 57 | banco_tronco | 3560 | 520 | 200 | 80 |
| 58 | @moita_1 | 3830 | 510 | 200 | 90 |
| 59 | @moita_2 | 4040 | 590 | 200 | 90 |
| 60 | @laguinho | 3090 | 610 | 820 | 260 |
| 61 | cascata | 3700 | 540 | 240 | 160 |
| 62 | vitoria_regia | 3330 | 740 | 120 | 50 |
| 63 | vitoria_regia_flor | 3410 | 720 | 170 | 96 |
| 64 | touceira | 3060 | 600 | 110 | 110 |
| 65 | touceira | 3460 | 540 | 110 | 110 |
| 66 | touceira | 3930 | 650 | 110 | 110 |
| 67 | flores_lago | 2960 | 690 | 230 | 110 |
| 68 | flores_lago | 3230 | 540 | 230 | 110 |
| 69 | lanterna_jardim | 3135 | 610 | 90 | 170 |
| 70 | @moita_3 | 3850 | 750 | 200 | 90 |
| 71 | pedra | 4150 | 820 | 110 | 60 |
| 72 | pedra | 2440 | 850 | 110 | 60 |
| 73 | flores_lago | 480 | 548 | 230 | 110 |
| 74 | touceira | 750 | 560 | 110 | 110 |
| 75 | moita_flores | 40 | 700 | 200 | 90 |
| 76 | pedra | 670 | 830 | 110 | 60 |
| 77 | flores_lago | 180 | 790 | 230 | 110 |
| 78 | touceira | 300 | 640 | 110 | 110 |
| 79 | pedra | 100 | 610 | 110 | 60 |
| 80 | @seta_sede | 40 | 462 | 120 | 160 |
| 81 | @seta_plantacao | 3380 | 462 | 120 | 160 |
| 82 | @seta_pet_care | 4160 | 462 | 120 | 160 |

</details>

## pet_care

Largura 2600 (2.0 telas), 29 peças, 7 de tocar, 7 de pegar, 0 lugares, 2 superfícies.

- **Sem sombra no chão** (1): `pergola`
- **Fora da área** (2): `grama` em (2200, 600) tamanho 1100x300; `cerca` em (2496, 518) tamanho 416x92
- **Pequeno para o dedo** (7): `osso` 56x26, com a folga 77x49 pt; `bolinha` 30x30, com a folga 53x53 pt; `biscoito` 40x36, com a folga 62x58 pt; `peixinho` 44x26, com a folga 66x49 pt; `tigela_cao` (tocar) 80x40, 73x36 pt; `tigela_gato` (tocar) 80x40, 73x36 pt; `tigela_agua` (tocar) 80x40, 73x36 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2600 | 900 |
| 1 | grama | 0 | 600 | 1100 | 300 |
| 2 | grama | 1100 | 600 | 1100 | 300 |
| 3 | grama | 2200 | 600 | 1100 | 300 |
| 4 | arvore_flores | 70 | 170 | 360 | 440 |
| 5 | arvore_flores | 2198 | 190 | 344 | 420 |
| 6 | cerca | 0 | 518 | 416 | 92 |
| 7 | cerca | 416 | 518 | 416 | 92 |
| 8 | cerca | 832 | 518 | 416 | 92 |
| 9 | cerca | 1248 | 518 | 416 | 92 |
| 10 | cerca | 1664 | 518 | 416 | 92 |
| 11 | cerca | 2080 | 518 | 416 | 92 |
| 12 | cerca | 2496 | 518 | 416 | 92 |
| 13 | pergola | 636 | 120 | 928 | 492 |
| 14 | piso_pedrinhas | 626 | 626 | 948 | 148 |
| 15 | placa_pata | 1060 | 60 | 90 | 80 |
| 16 | @chuveirinho | 760 | 290 | 140 | 320 |
| 17 | @banheira | 840 | 440 | 300 | 170 |
| 18 | bolha | 980 | 380 | 30 | 30 |
| 19 | bolha | 1030 | 350 | 30 | 30 |
| 20 | prateleira | 1230 | 300 | 220 | 140 |
| 21 | gancho_toalha | 1380 | 250 | 60 | 40 |
| 22 | @tigela_cao | 1560 | 640 | 80 | 40 |
| 23 | @tigela_gato | 1660 | 640 | 80 | 40 |
| 24 | @tigela_agua | 1760 | 640 | 80 | 40 |
| 25 | @cercadinho | 1900 | 520 | 420 | 180 |
| 26 | vaso_flores | 620 | 520 | 70 | 90 |
| 27 | vaso_flores | 1530 | 520 | 70 | 90 |
| 28 | @seta_estabulo | 380 | 470 | 120 | 160 |

</details>

## plantacao

Largura 3300 (2.5 telas), 30 peças, 12 de tocar, 1 de pegar, 0 lugares, 0 superfícies.

- **Sem sombra no chão** (2): `canteiro_flores`; `banca`
- **Fora da área** (2): `cerca` em (2912, 518) tamanho 416x92; `banca` em (2530, 770) tamanho 260x170
- **Pequeno para o dedo** (3): `maca` 30x32, com a folga 53x55 pt; `borboleta` (tocar) 35x30, 32x27 pt; `abelha` (tocar) 30x25, 27x23 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 3300 | 900 |
| 1 | sol | 2636 | 56 | 128 | 128 |
| 2 | cerca | 0 | 518 | 416 | 92 |
| 3 | cerca | 416 | 518 | 416 | 92 |
| 4 | cerca | 832 | 518 | 416 | 92 |
| 5 | cerca | 1248 | 518 | 416 | 92 |
| 6 | cerca | 1664 | 518 | 416 | 92 |
| 7 | cerca | 2080 | 518 | 416 | 92 |
| 8 | cerca | 2496 | 518 | 416 | 92 |
| 9 | cerca | 2912 | 518 | 416 | 92 |
| 10 | @nuvem | 560 | 150 | 220 | 90 |
| 11 | bica | 30 | 570 | 110 | 190 |
| 12 | espantalho | 1150 | 390 | 100 | 250 |
| 13 | carrinho | 420 | 790 | 190 | 110 |
| 14 | @cesta | 680 | 810 | 120 | 80 |
| 15 | @canteiro_flores | 1890 | 700 | 250 | 90 |
| 16 | @borboleta | 1960 | 560 | 35 | 30 |
| 17 | @abelha | 2050 | 600 | 30 | 25 |
| 18 | @flor_arco_iris | 2180 | 640 | 150 | 180 |
| 19 | @frutinhas_magicas | 2350 | 530 | 160 | 260 |
| 20 | arbusto_coracoes | 2160 | 450 | 150 | 150 |
| 21 | @macieira | 2540 | 140 | 230 | 500 |
| 22 | @laranjeira | 2800 | 170 | 220 | 470 |
| 23 | @bananeira | 3040 | 140 | 230 | 480 |
| 24 | escadinha | 2740 | 610 | 70 | 200 |
| 25 | banca | 2530 | 770 | 260 | 170 |
| 26 | minhoca | 3000 | 860 | 40 | 20 |
| 27 | matinho | 3150 | 850 | 40 | 30 |
| 28 | @seta_sede | 1430 | 440 | 120 | 160 |
| 29 | @seta_estabulo | 1560 | 440 | 120 | 160 |

</details>

## quarto_carol

Largura 2200 (1.7 telas), 21 peças, 8 de tocar, 5 de pegar, 1 lugares, 2 superfícies.

- **Pode estar flutuando** (2): `laco` (de pegar) pé em (785, 516), sem superfície embaixo; `livrinho` (de pegar) pé em (1555, 516), sem superfície embaixo
- **Pequeno para o dedo** (2): `laco` 50x30, com a folga 71x53 pt; `livrinho` 40x32, com a folga 62x55 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2200 | 900 |
| 1 | piso | 0 | 578 | 2200 | 324 |
| 2 | janela | 1476 | 108 | 320 | 246 |
| 3 | quadro_coracao | 516 | 146 | 118 | 138 |
| 4 | quadro_flor | 656 | 176 | 98 | 98 |
| 5 | quadro_ferradura | 1956 | 156 | 128 | 108 |
| 6 | @porta_sala | 50 | 250 | 170 | 350 |
| 7 | placa_casa | 100 | 180 | 70 | 60 |
| 8 | @guarda_roupa | 260 | 200 | 300 | 420 |
| 9 | planta | 600 | 490 | 90 | 130 |
| 10 | @gaveta_esq | 720 | 470 | 130 | 150 |
| 11 | @abajur_esq | 745 | 372 | 80 | 110 |
| 12 | porta_retrato_coracao | 830 | 410 | 60 | 66 |
| 13 | cama | 860 | 290 | 620 | 330 |
| 14 | @cobertor | 890 | 505 | 560 | 110 |
| 15 | @gaveta_dir | 1490 | 470 | 130 | 150 |
| 16 | @abajur_dir | 1515 | 372 | 80 | 110 |
| 17 | porta_retrato_paisagem | 1590 | 410 | 60 | 66 |
| 18 | @penteadeira | 1790 | 260 | 260 | 360 |
| 19 | banquinho | 1870 | 560 | 100 | 100 |
| 20 | tapete | 900 | 720 | 520 | 120 |

</details>

## sala

Largura 2200 (1.7 telas), 27 peças, 7 de tocar, 8 de pegar, 1 lugares, 5 superfícies.

- **Sem sombra no chão** (1): `lareira`

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 2200 | 900 |
| 1 | piso | 0 | 578 | 2200 | 324 |
| 2 | janela | 1326 | 88 | 314 | 242 |
| 3 | planta_pendurada | 1220 | 36 | 80 | 172 |
| 4 | planta_pendurada | 1660 | 36 | 86 | 184 |
| 5 | quadro_fazenda | 274 | 114 | 212 | 152 |
| 6 | @porta_frente | 40 | 250 | 170 | 350 |
| 7 | placa_casa | 95 | 180 | 70 | 60 |
| 8 | estante | 250 | 270 | 300 | 330 |
| 9 | porta_retrato | 440 | 330 | 50 | 50 |
| 10 | plantinha | 470 | 420 | 50 | 60 |
| 11 | @porta_cozinha | 600 | 250 | 170 | 350 |
| 12 | placa_panela | 650 | 180 | 70 | 60 |
| 13 | lareira | 800 | 180 | 420 | 420 |
| 14 | @fogo | 940 | 508 | 140 | 90 |
| 15 | vaso_flores | 830 | 330 | 50 | 70 |
| 16 | vaso_flores | 1110 | 330 | 50 | 70 |
| 17 | sofa | 1240 | 410 | 460 | 200 |
| 18 | @abajur | 1715 | 412 | 90 | 200 |
| 19 | @porta_catarina | 1820 | 250 | 170 | 350 |
| 20 | placa_coracao | 1870 | 180 | 70 | 60 |
| 21 | @porta_carol | 2010 | 250 | 170 | 350 |
| 22 | placa_flor | 2060 | 180 | 70 | 60 |
| 23 | tapete | 900 | 700 | 600 | 150 |
| 24 | mesa_centro | 1070 | 660 | 260 | 100 |
| 25 | vaso_flores | 1170 | 600 | 50 | 70 |
| 26 | @cesto | 520 | 690 | 140 | 110 |

</details>

## sede

Largura 3000 (2.3 telas), 36 peças, 10 de tocar, 2 de pegar, 2 lugares, 1 superfícies.

- **Sem sombra no chão** (4): `rede`; `cadeira_deck`; `cadeira_deck`; `vaso_1`
- **Fora da área** (3): `grama` em (2200, 604) tamanho 1100x300; `arvore_flores` em (2772, 300) tamanho 246x300; `cerca` em (2830, 518) tamanho 416x92
- **Pequeno para o dedo** (2): `lanterna_esq` (tocar) 60x100, 55x91 pt; `lanterna_dir` (tocar) 60x100, 55x91 pt

<details><summary>Todas as peças (ordem de desenho)</summary>

| # | peça | x | y | larg. | alt. |
|---|---|---|---|---|---|
| 0 | fundo | 0 | 0 | 3000 | 900 |
| 1 | grama | 0 | 604 | 1100 | 300 |
| 2 | grama | 1100 | 604 | 1100 | 300 |
| 3 | grama | 2200 | 604 | 1100 | 300 |
| 4 | arvore_flores | 40 | 160 | 360 | 440 |
| 5 | arvore_flores | 2772 | 300 | 246 | 300 |
| 6 | cerca | 0 | 518 | 416 | 92 |
| 7 | cerca | 2830 | 518 | 416 | 92 |
| 8 | casa_fachada | 340 | 0 | 1440 | 608 |
| 9 | janela_casa | 466 | 238 | 218 | 232 |
| 10 | janela_casa | 1406 | 238 | 218 | 232 |
| 11 | deck | 1780 | 136 | 1090 | 472 |
| 12 | pedra_caminho | 1010 | 621 | 100 | 38 |
| 13 | pedra_caminho | 1032 | 659 | 100 | 38 |
| 14 | pedra_caminho | 974 | 697 | 100 | 38 |
| 15 | pedra_caminho | 996 | 735 | 100 | 38 |
| 16 | pedra_caminho | 938 | 773 | 100 | 38 |
| 17 | pedra_caminho | 960 | 811 | 100 | 38 |
| 18 | pedra_caminho | 902 | 849 | 100 | 38 |
| 19 | @porta_sala | 965 | 240 | 190 | 360 |
| 20 | banco_varanda | 620 | 425 | 360 | 150 |
| 21 | vaso_3 | 540 | 418 | 110 | 160 |
| 22 | vaso_2 | 1210 | 418 | 110 | 160 |
| 23 | @lanterna_dir | 1160 | 240 | 60 | 100 |
| 24 | @lanterna_esq | 860 | 240 | 60 | 100 |
| 25 | @luzinhas_1 | 1830 | 190 | 740 | 80 |
| 26 | @luzinhas_2 | 2090 | 186 | 740 | 80 |
| 27 | rede | 1845 | 290 | 460 | 300 |
| 28 | cadeira_deck | 2340 | 362 | 100 | 200 |
| 29 | cadeira_deck | 2690 | 362 | 100 | 200 |
| 30 | mesa_deck | 2420 | 410 | 300 | 150 |
| 31 | vaso_1 | 1700 | 590 | 110 | 160 |
| 32 | @seta_entrada | 1150 | 640 | 120 | 160 |
| 33 | @seta_arvore | 30 | 640 | 120 | 160 |
| 34 | @seta_estabulo | 2700 | 640 | 120 | 160 |
| 35 | @seta_plantacao | 2850 | 640 | 120 | 160 |

</details>

## Mesma peça, tamanhos diferentes

- **banquinho/cadeira**: 5 tamanhos. banquinho 100x100 (quarto_carol), cadeira 160x230 (cozinha), cadeira_deck 100x200 (sede), cadeirinha 60x80 (casa_arvore_dentro), cadeirinha 80x120 (casinha), cadeirinha_dir 60x80 (casa_arvore_dentro), cadeirinha_esq 60x80 (casa_arvore_dentro)
- **lanterna**: 4 tamanhos. lanterna 52x110 (estabulo), lanterna 60x100 (cabana), lanterna_dir 60x100 (sede), lanterna_dir 60x110 (entrada), lanterna_esq 60x100 (sede), lanterna_esq 60x110 (entrada), lanterna_jardim 90x170 (estabulo)
- **mesa**: 5 tamanhos. mesa 420x200 (cozinha), mesa_centro 260x100 (sala), mesa_deck 300x150 (sede), mesa_piquenique 320x130 (casa_arvore), mesinha_cha 180x80 (casa_arvore_dentro)
- **moita**: 6 tamanhos. arbusto 300x99 (casa_arvore), arbusto_coracoes 150x150 (plantacao), matinho 40x30 (plantacao), moita_1 200x90 (estabulo), moita_2 200x90 (estabulo), moita_3 200x90 (estabulo), moita_flores 200x90 (estabulo), touceira 110x110 (estabulo), tufo 56x48 (casa_arvore)
- **pedra**: 2 tamanhos. pedra 110x60 (estabulo), pedra_caminho 100x38 (estabulo), pedra_caminho 100x38 (sede)
- **porta**: 4 tamanhos. porta 103x200 (casa_arvore), porta 130x300 (casa_arvore_dentro), porta_carol 170x350 (sala), porta_catarina 170x350 (sala), porta_cozinha 170x350 (sala), porta_frente 170x350 (sala), porta_sala 170x350 (cozinha), porta_sala 170x350 (quarto_carol), porta_sala 190x360 (sede)
- **porta-retrato**: 2 tamanhos. porta_retrato 50x50 (sala), porta_retrato_coracao 60x66 (quarto_carol), porta_retrato_paisagem 60x66 (quarto_carol)
- **tigela**: 2 tamanhos. tigela_agua 160x70 (estabulo), tigela_agua 80x40 (pet_care), tigela_cao 80x40 (cozinha), tigela_cao 80x40 (pet_care), tigela_gato 80x40 (cozinha), tigela_gato 80x40 (pet_care), tigela_lumi 80x40 (cozinha), tigela_racao 160x70 (estabulo)
- **vaso**: 5 tamanhos. planta 90x130 (quarto_carol), plantinha 50x60 (sala), vaso_1 110x160 (sede), vaso_2 110x160 (sede), vaso_3 110x160 (sede), vaso_flores 50x70 (sala), vaso_flores 70x90 (cozinha), vaso_flores 70x90 (pet_care)
- **árvore**: 10 tamanhos. arvore 480x540 (estabulo), arvore_flores 246x300 (entrada), arvore_flores 246x300 (sede), arvore_flores 344x420 (pet_care), arvore_flores 360x440 (pet_care), arvore_flores 360x440 (sede), arvore_flores 376x460 (casinha), arvore_flores 393x480 (cabana), arvore_flores 409x500 (cabana), bananeira 230x480 (plantacao), laranjeira 220x470 (plantacao), macieira 230x500 (plantacao)
