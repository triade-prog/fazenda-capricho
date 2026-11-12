# Estábulo florido + pasto — prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C09.
Layout com a escala: `estabulo_layout_1.png` (estábulo) e `estabulo_layout_2.png` (pasto), nesta pasta.

Mesmo processo do quarto: **uma conversa só**, primeiro a mensagem de contexto, depois um pedido por peça.

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `estabulo_layout_1.png`, `estabulo_layout_2.png`, duas peças 3D do quarto para o estilo
(`arte/cenario/3d/beliche.png` e `arte/cenario/3d/pote_biscoitos.png`) e a imagem oficial da Lumi
(`arte/personagens/cavalo-rosa.png`).

```
Vou gerar, uma peça por vez, o ESTÁBULO FLORIDO e o PASTO do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É onde mora a Lumi, a pônei rosa da imagem anexada: as peças precisam combinar
com ela e caber em volta dela.

ESTILO: igual às peças 3D anexadas do quarto: brinquedo 3D estilizado, formas arredondadas e macias,
materiais foscos e simples, madeira clara cor de mel, telhado vermelho-rosado, muitas flores rosa, lilás e
brancas, verde do pasto suave; fofo e aconchegante, sem realismo fotográfico.

REFERÊNCIAS: os desenhos do layout são RASCUNHOS de posição e tamanho; não copie o estilo deles.
A Lumi tem 390 px de altura e 573 px de comprimento no jogo; a Catarina, 300 px. Use as duas como régua.

REGRAS PARA TODAS AS PEÇAS:
1. Uma peça por imagem, inteira, centralizada, sem cortar bordas.
2. Vista de frente, sem girar para o lado; luz suave de cima e um pouco da esquerda.
3. Fundo totalmente transparente (PNG). Se não der, magenta puro #FF00FF liso, sem magenta na peça.
4. Sem sombra no chão, sem texto, sem números, sem moldura, sem personagens.
5. PEÇAS COM ESTADOS (ex.: porta fechada e aberta): todas as imagens do mesmo tamanho e com a base na MESMA
   posição, para o jogo trocar uma pela outra sem a peça "pular".
6. Proporção indicada em cada pedido (largura × altura, em pixels do jogo), no máximo 10% de diferença,
   e resolução de pelo menos o DOBRO desse tamanho.

Responda só "Entendido" e espere o primeiro pedido.
```

---

## Peças

Tamanhos em pixels do jogo. Peça os estados de uma peça na mesma mensagem ("gere as duas versões, do mesmo
tamanho e na mesma posição").

### Fundo

| # | Peça | Tamanho | Pedido |
|---|---|---|---|
| 1 | Fundo do estábulo e do pasto | 3300 × 900 | Panorama largo. À esquerda (até 1500 px), o estábulo de madeira visto por dentro, como uma casa de bonecas aberta na frente: parede de tábuas cor de mel, vigas, telhado vermelho-rosado no alto com flores penduradas e chão de palha. À direita, o pasto: morros verdes, céu claro, cerca branca e grama com florzinhas. SEM nenhuma peça interativa (sem porta, cocho, árvore grande ou banco). Pode ser entregue em duas metades de 1650 × 900. |

### Estábulo

| # | Peça | Tamanho | Estados | Pedido |
|---|---|---|---|---|
| 2 | Meia-porta da baia | 300 × 170 | fechada · aberta (folha girada para o lado, 80 × 170) | Porta baixa de madeira em "X", com coração rosa; a Lumi fica atrás dela. |
| 3 | Cocho de madeira | 220 × 100 | vazio · com feno · com cenouras | Comedouro baixo e comprido. |
| 4 | Balde | 90 × 90 | vazio · com água | Balde de madeira com aro dourado. |
| 5 | Fardo de feno | 170 × 110 | — | Fardo retangular fofinho, para sentar. |
| 6 | Punhado de feno | 60 × 40 | — | Montinho solto, para levar ao cocho. |
| 7 | Ducha do cavalo | 300 × 430 | desligada · ligada (água caindo) | Estrutura de madeira com chuveiro alto e torneira; água azul-clara fofa, sem respingo no chão. |
| 8 | Piso de banho | 260 × 60 | — | Estrado de madeira com ralinho em forma de coração. |
| 9 | Espuma de banho | 60 × 60 · 40 × 40 · 25 × 25 | — | Três tamanhos de bolhas de sabão, brancas com reflexo rosa. |
| 10 | Toalha | no gancho 90 × 60 · solta 100 × 60 | — | Toalha rosa com borda lilás. |
| 11 | Pente de crina | 70 × 45 | — | Pente largo rosa com coração; combina com a escova que já existe. |
| 12 | Suporte com manta e cabresto | 140 × 120 | — | Decorativo, pendurado na parede (a sela já faz parte da Lumi). |
| 13 | Ferradura decorativa | 120 × 110 | — | Ferradura dourada com coração, igual à da marca. |
| 14 | Lanterna | 60 × 100 | apagada · acesa | Lanterna de fazenda com luz quente. |

### Pasto

| # | Peça | Tamanho | Estados | Pedido |
|---|---|---|---|---|
| 15 | Porteira | 300 × 200 | fechada · aberta | Porteira de madeira branca com flores, que encaixa na cerca. |
| 16 | Árvore grande | 480 × 540 | — | Árvore de copa redonda com flores rosa; tronco largo para sentar à sombra. |
| 17 | Bebedouro / laguinho | 300 × 110 | parado · com ondinhas | Laguinho raso de pedras arredondadas, onde a Lumi bebe água. |
| 18 | Banco de tronco | 200 × 80 | — | Tronco deitado, para sentar dois. |
| 19 | Moita de flores | 200 × 90 | com flores · colhida (só folhas) | Margaridas brancas (as mesmas da crina da Lumi), flores rosa e lilás. |
| 20 | Margarida solta | 30 × 60 | — | Para colher e pôr na crina da Lumi. |

Cenoura, maçã, borboleta e abelhinha já estão nos prompts da Plantação (`arte/cenario/plantacao/PROMPTS.md`)
e servem aqui também.

---

## Entrega

Suba em `arte/cenario/estabulo/3d/` com nomes simples: `fundo.png` (ou `fundo_1.png` e `fundo_2.png`),
`meia_porta_fechada.png`, `meia_porta_aberta.png`, `cocho_vazio.png`, `cocho_feno.png`, `cocho_cenouras.png`,
`balde_vazio.png`, `balde_agua.png`, `fardo.png`, `feno.png`, `ducha_desligada.png`, `ducha_ligada.png`,
`piso_banho.png`, `espuma_1.png` a `espuma_3.png`, `toalha_gancho.png`, `toalha.png`, `pente.png`,
`suporte_manta.png`, `ferradura.png`, `lanterna_apagada.png`, `lanterna_acesa.png`, `porteira_fechada.png`,
`porteira_aberta.png`, `arvore.png`, `laguinho_parado.png`, `laguinho_ondas.png`, `banco_tronco.png`,
`moita_flores.png`, `moita_colhida.png`, `margarida.png`. Avise quando subir: eu monto o cenário no jogo e
confiro se a Lumi cabe na baia, se o banho funciona e se a porteira abre no lugar certo.
