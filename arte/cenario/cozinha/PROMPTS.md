# Cozinha da Fazenda: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C04.

Layout na escala do jogo, nesta pasta: `cozinha_layout.png` (2200 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `cozinha_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e a colagem `arte/conceito/colagem_cenarios/colagem_cozinha.png` (só o clima: o jogo é visto DE FRENTE) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário COZINHA DA FAZENDA do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É uma cozinha rústica e rosa: geladeira lilás, mesa com toalha xadrez e cadeiras de coração, panelas penduradas.

ESTILO: igual às peças 3D anexadas do quarto: brinquedo 3D estilizado, formas arredondadas e macias,
materiais foscos e simples, madeira clara cor de mel, cores pastel da fazenda (rosa, lilás, roxo, verde);
fofo, sem realismo fotográfico.

REFERÊNCIAS: o layout anexado mostra posição e tamanho de cada peça; os desenhos dele são RASCUNHOS, não
copie o estilo. A Catarina tem 300 px de altura no jogo: use-a como régua.

REGRAS PARA TODAS AS PEÇAS:
1. Uma peça por imagem, inteira, centralizada, sem cortar bordas.
2. Vista de frente, sem girar para o lado; luz suave de cima e um pouco da esquerda.
3. Fundo totalmente transparente (PNG). Se não der, magenta puro #FF00FF liso, sem magenta na peça.
4. Sem sombra no chão, sem texto, sem letras, sem números, sem moldura, sem personagens.
5. PEÇAS COM ESTADOS (ex.: fechada e aberta): todas as imagens do mesmo tamanho e com a base na MESMA
   posição, para o jogo trocar uma pela outra sem a peça "pular".
6. Proporção indicada em cada pedido (largura × altura, em pixels do jogo), no máximo 10% de diferença,
   e resolução de pelo menos o DOBRO desse tamanho.
7. Nada de personagens de filmes, desenhos ou marcas: tudo inventado.

Responda só "Entendido" e espere o primeiro pedido.
```

---

## Peças

Tamanhos em pixels do jogo. Para cada pedido, anexe também o PNG da peça em `2d/` como rascunho de forma.

| # | Peça | Tamanho | Estados | Pedido |
|---|---|---|---|---|
| 1 | Fundo da cozinha | 2200 × 900 | — | Parede rosa-pêssego com vigas, azulejinhos rosa e branco, armários de madeira embutidos atrás da bancada, prateleira com potes coloridos e uma plantinha, panelas de cobre penduradas e janela com cortina rosa. SEM geladeira, fogão, pia, mesa e porta. |
| 2 | Geladeira lilás | 238 × 430 | fechada · aberta | Geladeira retrô lilás com cantos bem arredondados e ímãs de coração. Aberta: prateleiras com frutas, leite, cenoura e maçã (para a Lumi), peixinho (gatos) e biscoito de coração (cães); a porta aberta aparece fina do lado direito. |
| 3 | Fogão com panela | 240 × 260 | normal · com vapor | Fogãozinho branco e rosa com forno e botões lilás, panela rosa em cima. Vapor: fiozinhos de vapor e um coração subindo. Sem chama. |
| 4 | Pia | 260 × 200 | — | Bancada de madeira com cuba branca e torneira prateada com registro de coração. Tampo PLANO. |
| 5 | Mesa com toalha xadrez | 420 × 200 | — | Mesa de madeira com toalha xadrez vermelho-rosado e branca. Tampo PLANO para pratos e comidinhas. |
| 6 | Cadeira de coração | 110 × 230 | — | Cadeira de madeira com coração vazado no encosto; o jogo usa quatro. |
| 7 | Pratos | 60 × 30 | sujo · limpo | Prato branco. Sujo: manchinhas de comida. Limpo: brilha. |
| 8 | Comidinhas de gente | xícara 40 × 36 · maçã 30 × 32 · banana 50 × 30 · leite 30 × 44 · sanduíche 50 × 34 | — | Só para a Catarina e a Carol (GDD, seção 9). |
| 9 | Tigelas dos bichos | 80 × 40 | vazia · cheia (cão, gato, Lumi) | Tigela rosa com biscoitos de coração, lilás com peixinho e cor de mel com cenoura e maçã. |
| 10 | Vaso de flores | 70 × 90 | — | Vaso rosa com flores amarelas, para enfeitar a mesa. |
| 11 | Porta e plaquinha | porta 170 × 350 · placa 70 × 60 | fechada · aberta | A mesma porta da sala; plaquinha com a casinha (volta para a sala). |

Gere primeiro a geladeira (os dois estados), a mesa e a cadeira.
Comida de gente só para a Catarina e a Carol; bichos só com o petisco deles. Fogão sem fogo.

---

## Entrega

Suba os arquivos em `arte/cenario/cozinha/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo da cozinha: `fundo.png`
- Geladeira lilás: `geladeira_fechada.png`, `geladeira_aberta.png`
- Fogão com panela: `fogao.png`, `fogao_aceso.png`
- Pia: `pia.png`
- Mesa com toalha xadrez: `mesa.png`
- Cadeira de coração: `cadeira.png`
- Pratos: `prato_sujo.png`, `prato_limpo.png`
- Comidinhas de gente: `xicara.png`, `maca.png`, `banana.png`, `copo_leite.png`, `sanduiche.png`
- Tigelas dos bichos: `tigela_cao_vazia.png`, `tigela_cao_cheia.png`, `tigela_gato_vazia.png`, `tigela_gato_cheia.png`, `tigela_lumi_vazia.png`, `tigela_lumi_cheia.png`
- Vaso de flores: `vaso_flores.png`
- Porta e plaquinha: `porta_fechada.png`, `porta_aberta.png`, `placa_casa.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
