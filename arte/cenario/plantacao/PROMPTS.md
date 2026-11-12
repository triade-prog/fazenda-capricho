# Plantação da Fazenda — prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento completo do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C11.
Layout com a escala: `plantacao_layout_1.png` e `plantacao_layout_2.png` (nesta pasta).

Mesmo processo do quarto: **uma conversa só**, primeiro a mensagem de contexto, depois um pedido por
peça (ou por grupo de estados da mesma peça).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `plantacao_layout_1.png`, `plantacao_layout_2.png`, duas peças 3D do quarto para o estilo
(`arte/cenario/3d/pote_biscoitos.png` e `arte/cenario/3d/tapete.png`) e a colagem
`arte/conceito/colagem_cenarios/colagem_horta.png`.

```
Vou gerar, uma peça por vez, a PLANTAÇÃO do jogo infantil "Fazenda Capricho" (iPad, faz de conta no
estilo Avatar World): lavoura em quadradinhos, morangos e abóbora, jardim de flores, canteiro mágico e
pomar.

ESTILO: igual às peças 3D anexadas do quarto: brinquedo 3D estilizado, formas arredondadas e macias,
materiais foscos e simples, cores alegres com toque pastel (verde, rosa, lilás, madeira clara, terra
marrom-clara), fofo, sem realismo fotográfico.

REFERÊNCIAS: os desenhos do layout são RASCUNHOS de posição e tamanho; não copie o estilo deles.
A Catarina tem 300 px de altura no jogo e serve de régua.

REGRAS PARA TODAS AS PEÇAS:
1. Uma peça por imagem, inteira, centralizada, sem cortar bordas.
2. Vista de frente, sem girar para o lado; luz suave de cima e um pouco da esquerda.
3. Fundo totalmente transparente (PNG). Se não der, magenta puro #FF00FF liso, sem magenta na peça.
4. Sem sombra no chão, sem cenário em volta, sem texto, sem números, sem moldura, sem personagens.
5. PEÇAS COM ESTADOS (ex.: broto, planta, pronta): todas as imagens do mesmo tamanho, com a base da
   peça na MESMA posição, para o jogo trocar uma pela outra sem a peça "pular".
6. Proporção indicada em cada pedido (largura × altura, em pixels do jogo), no máximo 10% de diferença,
   e resolução de pelo menos o DOBRO desse tamanho.

Responda só "Entendido" e espere o primeiro pedido.
```

---

## Fase 1: bica, ferramentas, lavoura e macieira

| # | Peça | Tamanho no jogo | Estados (uma imagem cada) | Pedido |
|---|---|---|---|---|
| 1 | Bica d'água de madeira com torneirinha e baldinho | 110 × 190 | — | Bica de madeira clara com torneirinha e um balde pendurado; água pingando discreta. |
| 2 | Regador rosa | 80 × 55 | vazio · cheio (com gotinhas saindo) | Regador rosa com coração, bico comprido. |
| 3 | Enxadinha de brinquedo | 45 × 90 | — | Cabo de madeira clara, lâmina lilás arredondada, sem ponta. |
| 4 | Pacotinhos de sementes | 60 × 80 cada | cenoura · alface · tomate · morango · abóbora · girassol | Envelope de papel com o DESENHO da planta (sem letras). Mesmo formato nos seis. |
| 5 | Cesta de vime | 120 × 80 | vazia · cheia de legumes e frutas | Cesta com alça e paninho xadrez rosa. |
| 6 | Quadradinho de terra | 200 × 70 | terra dura · terra fofinha (arada) · terreno fechado (placa de madeira com cadeado dourado) | Canteiro baixo com borda de madeira, visto de frente. |
| 7 | Cenoura no quadradinho | 200 × 200 | semente · broto · folhas · pronta (folhas grandes e brilho) | O quadradinho fofinho da peça 6 com a planta em cada estágio; base no mesmo lugar. |
| 8 | Alface no quadradinho | 200 × 200 | semente · broto · folhas · pronta | Igual à peça 7. |
| 9 | Tomateiro no quadradinho, com estaca | 200 × 240 | semente · broto · planta verde · pronta (tomates vermelhos) | Igual à peça 7. |
| 10 | Colheita da fase 1 | cenoura 30 × 60 · alface 50 × 45 · tomate 30 × 30 | — | Cada legume solto, para segurar na mão. |
| 11 | Macieira | 230 × 500 | com maçãs · sem maçãs | Árvore arredondada, tronco grosso, copa fofa; maçãs vermelhas brilhantes. |
| 12 | Maçã | 30 × 32 | — | Maçã solta com folhinha. |

## Fase 2: morango, abóbora, jardim, canteiro mágico e pomar

| # | Peça | Tamanho no jogo | Estados | Pedido |
|---|---|---|---|---|
| 13 | Morangos no canteiro baixo | 160 × 110 | semente · broto · folhas · pronta | Canteiro baixo com borda de madeira. |
| 14 | Morango solto | 22 × 26 | — | |
| 15 | Abóbora | 60 × 50 · 110 × 90 · 160 × 150 | pequena · média · GIGANTE | Abóbora laranja fofa; a gigante com topo achatado para alguém sentar. |
| 16 | Girassol | 90 × 360 | caule com folhas · cabeça (imagem separada, para girar) | Mais alto que a Catarina. |
| 17 | Canteiro de flores coloridas | 250 × 90 | com flores · colhido (só folhas) | Margaridas brancas, tulipas rosa e flores em forma de coração. |
| 18 | Flores soltas e buquê | flor 25 × 55 · buquê 50 × 70 | margarida · tulipa · flor de coração · buquê com laço lilás | |
| 19 | Abelhinha fofa e borboleta | 30 × 25 · 35 × 30 | asas abertas · asas fechadas | Abelha redondinha, SEM ferrão aparente; borboleta lilás e rosa. |
| 20 | Flor arco-íris | 150 × 180 | rosa · lilás · azul · amarela | A mesma flor em quatro cores. |
| 21 | Pé de frutinhas mágicas | 160 × 260 | com frutinhas brilhantes · sem frutinhas | Arbusto rosa com frutinhas que parecem estrelinhas. |
| 22 | Arbusto de corações | 150 × 150 | — | Folhinhas em forma de coração. |
| 23 | Semente mágica dourada | 25 × 25 | — | Brilhante. |
| 24 | Laranjeira e laranja | 220 × 470 · 32 × 32 | com laranjas · sem laranjas | |
| 25 | Bananeira e cacho | 230 × 480 · 60 × 50 | com cacho · sem cacho | Folhas largas; banana solta 50 × 30. |
| 26 | Escadinha de pomar | 70 × 200 | — | Madeira clara, degraus largos. |
| 27 | Banca da colheita | 220 × 130 | — | Bancada de feirinha com toldo listrado rosa e branco (sem letreiro). |
| 28 | Carrinho de mão | 190 × 110 | — | Madeira com roda lilás. |
| 29 | Nuvem de chuva | 220 × 90 | parada · chovendo | Nuvem fofa e sorridente. |
| 30 | Espantalho fofo | 100 × 250 | — | Chapéu de cowboy, camisa xadrez, sorriso; nada assustador. |
| 31 | Minhoca amiga e matinho | 40 × 20 · 40 × 30 | — | Minhoca rosa sorridente; tufinho de mato com uma florzinha. |
| 32 | Fundo da Plantação | 3300 × 900 | — | Céu com sol, morros verdes, cerca branca e chão de terra clara. SEM nenhuma peça interativa. |

## Fase 3 (só se o "modo fazendinha" for aprovado)

| # | Peça | Tamanho no jogo | Estados | Pedido |
|---|---|---|---|---|
| 33 | Ferradurinha dourada (moeda do jogo) | 40 × 40 | — | Ferradura com coração, igual ao ícone da marca. |
| 34 | Estrelinha | 40 × 40 | — | Estrela amarela fofinha. |
| 35 | Balcão da lojinha de sementes | 300 × 220 | — | Para a Casinha de madeira; prateleira com pacotinhos. |
| 36 | Galinheiro | 260 × 240 | — | Casinha de madeira rosa com rampinha. |
| 37 | Ninho | 80 × 50 | vazio · com ovos | |
| 38 | Cocho e milho | 140 × 60 · 30 × 40 | vazio · cheio | |
| 39 | Balde de leite e novelo de lã | 60 × 70 · 45 × 40 | balde vazio · cheio | |

Galinhas, vaca e ovelha são **personagens**: devem ser gerados como folhas de pet, no mesmo processo
dos outros personagens (`docs/PROMPT_personagens.md`), depois da aprovação das criadoras.

---

## Entrega

Suba as imagens em `arte/cenario/plantacao/3d/`, com nomes simples: `bica.png`, `regador_vazio.png`,
`regador_cheio.png`, `cenoura_1.png` a `cenoura_4.png`, `macieira_com_macas.png` etc. Comece pela
**fase 1** e me avise: eu coloco no jogo e confiro antes da fase 2.
