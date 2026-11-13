# Casinha de madeira: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C13.

**Proposta:** lojinha, consultório de bichos ou outra brincadeira ainda precisa da decisão das criadoras. As peças servem para as duas ideias.

Layout na escala do jogo, nesta pasta: `casinha_layout.png` (2200 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `casinha_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário CASINHA DE MADEIRA do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É uma casinha de brincar no chão, com janela-balcão, que vira lojinha ou consultório de bichinhos de faz de conta.

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
| 1 | Fundo do gramado | 2200 × 900 | — | Gramado com muitas flores, cerca branca, uma árvore florida, céu e morros. SEM a casinha. |
| 2 | Casinha de madeira | 560 × 480 | — | Casinha de brincar de madeira clara com telhado rosa, coração no frontão, porta lateral lilás e uma grande janela-balcão na frente com o vão TRANSPARENTE (a Catarina aparece por ele, com o interior atrás). SEM toldo, balcão e objetos. |
| 3 | Interior da casinha | 560 × 480 | — | Fundo de dentro da casinha (madeira mais escura e aconchegante). Fica ATRÁS de quem está dentro e aparece pela janela. |
| 4 | Balcão | 380 × 60 | — | Tábua de madeira com mãos-francesas, PLANA, na base da janela: apoia os itens para vender ou atender. |
| 5 | Toldo listrado | 440 × 130 | aberto · fechado | Toldo rosa e branco sobre a janela. Fechado: enrolado e curto. |
| 6 | Prateleira e potinhos | prateleira 300 × 130 · potinho 30 × 40 | rosa · lilás · amarelo | Prateleira de duas tábuas VAZIA e potinhos com tampa branca e coração. |
| 7 | Caixinha registradora | 90 × 80 | normal · plim | Caixa registradora de brinquedo rosa e lilás com botões e coração; plim: a gavetinha abre com estrelinhas. |
| 8 | Maleta de veterinário | 110 × 90 | fechada · aberta | Maleta branca de brinquedo com cruz rosa; aberta mostra o estetoscópio e um curativo. |
| 9 | Estetoscópio e coração | estetoscópio 70 × 60 · coração 40 × 36 | — | Estetoscópio de brinquedo lilás; coração batendo que aparece sobre o bicho. |
| 10 | Cadeirinha | 80 × 120 | — | Cadeirinha de madeira com assento rosa; senta 1. |
| 11 | Plaquinhas | 90 × 80 | consultório · lojinha | Placa com patinha (consultório de bichos) ou com cestinha (lojinha), sem letras. |

---

## Entrega

Suba os arquivos em `arte/cenario/casinha/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo do gramado: `fundo.png`
- Casinha de madeira: `casinha.png`
- Interior da casinha: `casinha_interior.png`
- Balcão: `balcao.png`
- Toldo listrado: `toldo_aberto.png`, `toldo_fechado.png`
- Prateleira e potinhos: `prateleira.png`, `potinho_rosa.png`, `potinho_lilas.png`, `potinho_amarelo.png`
- Caixinha registradora: `caixa_registradora.png`, `caixa_registradora_plim.png`
- Maleta de veterinário: `maleta_fechada.png`, `maleta_aberta.png`
- Estetoscópio e coração: `estetoscopio.png`, `coracao_batendo.png`
- Cadeirinha: `cadeirinha.png`
- Plaquinhas: `placa_pata.png`, `placa_cesta.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
