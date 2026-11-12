# Plantação — peças 2D provisórias (fases 1 e 2)

Desenhos 2D chapados, no estilo das peças provisórias do quarto, para montar o cenário no jogo agora.
Depois serão trocados pelas peças 3D (pasta `../3d/`) **com os mesmos nomes e tamanhos**.

- Tamanhos iguais aos da tabela do `../PROMPTS.md`, em 2x (peças de até 100 px em 4x).
- A fase 3 (galinheiro e curral) ainda não foi desenhada: espera a aprovação dos novos bichos.
- `previa.png` mostra as peças montadas com a Catarina (300 px) para conferir a escala.
- `svg/` guarda o desenho vetorial de cada peça. Para refazer: `python3 ferramentas/cenario2d/plantacao.py`.

Nomes (os estados vão no fim do nome):

| Peça | Arquivos |
|---|---|
| Bica, regador, enxadinha | `bica`, `regador_vazio`, `regador_cheio`, `enxada` |
| Pacotinhos de sementes | `sementes_cenoura`, `_alface`, `_tomate`, `_morango`, `_abobora`, `_girassol` |
| Cesta | `cesta_vazia`, `cesta_cheia` |
| Quadradinho de terra | `terra_dura`, `terra_fofa`, `terra_fechada` |
| Cenoura, alface, tomate no quadradinho | `cenoura_1` a `cenoura_4`, `alface_1` a `_4`, `tomate_1` a `_4` (1 semente, 2 broto, 3 folhas, 4 pronta) |
| Colheita | `colheita_cenoura`, `colheita_alface`, `colheita_tomate` |
| Macieira e maçã | `macieira_com_macas`, `macieira_sem_macas`, `maca` |
| Fazendinha | `banca`, `ferradurinha`, `estrelinha`, `quadro_pedidos`, `contador` |
| Morango | `morango_1` a `morango_4`, `morango` |
| Abóbora | `abobora_pequena`, `abobora_media`, `abobora_gigante` |
| Girassol | `girassol_caule`, `girassol_cabeca` |
| Jardim | `canteiro_flores`, `canteiro_colhido`, `flor_margarida`, `flor_tulipa`, `flor_coracao`, `buque` |
| Bichinhos | `abelha_aberta`, `abelha_fechada`, `borboleta_aberta`, `borboleta_fechada`, `minhoca`, `matinho` |
| Canteiro mágico | `flor_arco_iris_rosa`, `_lilas`, `_azul`, `_amarela`, `frutinhas_magicas_com`, `frutinhas_magicas_sem`, `arbusto_coracoes`, `semente_magica` |
| Pomar | `laranjeira_com`, `laranjeira_sem`, `laranja`, `bananeira_com`, `bananeira_sem`, `cacho_banana`, `banana`, `escadinha`, `carrinho` |
| Outros | `nuvem_parada`, `nuvem_chovendo`, `espantalho`, `fundo` |
