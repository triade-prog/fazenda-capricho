# Sede da Fazenda: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C02.

Layout na escala do jogo, nesta pasta: `sede_layout.png` (3000 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `sede_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e o conceito `arte/conceito/cenarios_R01/02_casa_principal.png` (só o clima: a nossa casa é ROSA, não creme com telha) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário SEDE DA FAZENDA do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É a casa grande e ROSA da família, com varanda florida e um deck com rede para descansar ao ar livre.

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
| 1 | Fundo da Sede | 3000 × 900 | — | Fachada da casa grande ROSA com telhado lilás, coração no frontão, duas janelas lilás com floreiras, varanda de madeira com colunas floridas; à direita, o deck de madeira com pergolado florido e gradinha (de DIA). Árvores, morros, céu, cerca e caminho de pedras. SEM porta, rede, banco, mesa, vasos e luzinhas. |
| 2 | Porta da frente | 190 × 360 | fechada · aberta | Porta roxa arredondada no alto com moldura de madeira. Aberta: luz quente da sala. Leva para a Sala. |
| 3 | Rede | 460 × 300 | — | Rede rosa com franjas, presa entre dois postes de madeira. Cabem 1 ou 2 deitados; o jogo faz a rede balançar. |
| 4 | Banco da varanda | 360 × 150 | — | Banco de madeira com quatro almofadas rosa e lilás. Assento PLANO: sentam 3. |
| 5 | Mesa e cadeira do deck | mesa 300 × 150 · cadeira 100 × 200 | — | Mesa de madeira com tampo PLANO e cadeira de ripas; o jogo usa quatro cadeiras. |
| 6 | Vaso de flores | 110 × 160 | brotinho · flores · flores brilhando | Vaso de madeira; ao regar, as flores crescem e brilham. |
| 7 | Regador | 80 × 55 | vazio · cheio | O mesmo regador rosa da Plantação. |
| 8 | Varal de luzinhas | 740 × 80 | apagado · aceso | Fio com lampadinhas amarelas penduradas sob o pergolado do deck. |
| 9 | Lanterna da varanda | 60 × 100 | apagada · acesa | Lanterna roxa com coração; acesa, luz quente. |
| 10 | Bola | 60 × 60 | — | Bola com gomos coloridos; o Bob e a Nina brincam. |

Gere primeiro a porta, a rede e o banco da varanda. Uma rede só. Deck de dia.

---

## Entrega

Suba os arquivos em `arte/cenario/sede/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo da Sede: `fundo.png`
- Porta da frente: `porta_frente_fechada.png`, `porta_frente_aberta.png`
- Rede: `rede.png`
- Banco da varanda: `banco_varanda.png`
- Mesa e cadeira do deck: `mesa_deck.png`, `cadeira_deck.png`
- Vaso de flores: `vaso_1.png`, `vaso_2.png`, `vaso_3.png`
- Regador: `regador_vazio.png`, `regador_cheio.png`
- Varal de luzinhas: `luzinhas_apagadas.png`, `luzinhas_acesas.png`
- Lanterna da varanda: `lanterna_apagada.png`, `lanterna_acesa.png`
- Bola: `bola.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
