# Casa na árvore (pátio e dentro): prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seções C07 (pátio) e C08 (dentro).

Layouts na escala do jogo, nesta pasta:

| Arquivo | Mostra |
|---|---|
| `fora_layout_1.png` | Árvore, casinha, varanda, escadas e começo do escorregador |
| `fora_layout_2.png` | Escorregador, balanço, mesa de piquenique e trilha |
| `dentro_layout.png` | O cômodo da casinha |

Mesmo processo do quarto e do estábulo: **uma conversa só**. Envie primeiro a mensagem de contexto e
depois um pedido por peça. Comece pelo pátio (C07, prioridade P0) e deixe o lado de dentro (C08, P1) para depois.

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar estes arquivos:**

- os três layouts da tabela acima;
- duas peças 3D do quarto para o estilo: `arte/cenario/3d/escorregador.png` e `arte/cenario/3d/beliche.png`;
- o conceito `arte/conceito/cenarios_R01/04_casa_arvore_patio.png`;
- a imagem oficial da Catarina: `arte/personagens/catarina.png`.

```
Vou gerar, uma peça por vez, a CASA NA ÁRVORE do jogo infantil "Fazenda Capricho" (iPad, faz de conta no estilo
Avatar World): o pátio de brincadeiras em volta da árvore e o cômodo de dentro da casinha. É o esconderijo da
Catarina, a menina da imagem anexada.

ESTILO: igual às peças 3D anexadas do quarto: brinquedo 3D estilizado, formas arredondadas e macias, materiais
foscos e simples, madeira clara cor de mel. A árvore é ROSA (copa rosa-chiclete com flores), a casinha é colorida
(paredes creme e rosa, telhado lilás), e há toques de roxo, lilás e arco-íris; fofo e mágico, sem realismo
fotográfico.

REFERÊNCIAS: o conceito anexado mostra o clima, mas a árvore dele é verde e marrom, e a nossa é ROSA. Os desenhos
do layout são RASCUNHOS de posição e tamanho; não copie o estilo deles. A Catarina tem 300 px de altura no jogo:
use-a como régua. Ela precisa passar pela porta da casinha (130 × 300) e ficar de pé na varanda.

REGRAS PARA TODAS AS PEÇAS:
1. Uma peça por imagem, inteira, centralizada, sem cortar bordas.
2. Vista de frente, sem girar para o lado; luz suave de cima e um pouco da esquerda.
3. Fundo totalmente transparente (PNG). Se não der, magenta puro #FF00FF liso, sem magenta na peça.
4. Sem sombra no chão, sem texto, sem letras, sem números, sem moldura, sem personagens, sem bonecas.
5. PEÇAS COM ESTADOS (ex.: porta fechada e aberta): todas as imagens do mesmo tamanho e com a base na MESMA
   posição, para o jogo trocar uma pela outra sem a peça "pular".
6. Proporção indicada em cada pedido (largura × altura, em pixels do jogo), no máximo 10% de diferença,
   e resolução de pelo menos o DOBRO desse tamanho.
7. Nada de personagens de filmes, desenhos ou marcas: tudo inventado.

Responda só "Entendido" e espere o primeiro pedido.
```

---

## Peças

Os tamanhos estão em pixels do jogo. Peça os estados de uma mesma peça numa só mensagem: "gere as duas
versões, do mesmo tamanho e na mesma posição".

### C07 — Pátio da casa na árvore (2600 × 900, chão a partir de y = 600)

Gere primeiro as peças 2 a 7: elas encaixam umas nas outras na varanda.

| # | Peça | Tamanho | Estados | Pedido |
|---|---|---|---|---|
| 1 | Fundo do pátio | 2600 × 900 | — | Panorama largo: céu claro, morros verdes, cerca branca e grama com florzinhas. SEM a árvore e sem nenhuma peça interativa (sem escadas, balanço, mesa ou placas). Pode ser entregue em duas metades de 1300 × 900. |
| 2 | Árvore rosa com a casinha | 1000 × 600 | — | Árvore grande de copa ROSA bem redonda e fofa, tronco largo. No alto, a casinha de madeira colorida (480 × 300, telhado lilás, janelinha redonda) sobre o piso da varanda. O piso fica a **220 px da base da imagem** e ocupa uma faixa de 650 px de largura. No lugar da porta, só a parede lisa: a porta é a peça 4. SEM grade, escadas, escorregador ou frutinhas. |
| 3 | Grade da varanda | 650 × 60 | — | Grade baixa de madeira clara com coraçõezinhos, VAZADA (entre as ripas, transparente). Fica na frente de quem está de pé na varanda. |
| 4 | Porta da casinha | 130 × 300 | fechada · aberta | Porta arredondada no alto, roxa com coração. Aberta: folha encostada para dentro e o interior quentinho aparecendo. |
| 5 | Escada de madeira | 60 × 220 | — | Escada de mão reta, degraus largos, da grama até a varanda. |
| 6 | Escada de corda | 50 × 220 | — | Escada de corda com degraus de madeira, pendurada da varanda; um pouco solta embaixo. |
| 7 | Escorregador mágico | 470 × 220 | rosa/roxo · arco-íris | Curvo, com a ponta alta no canto de cima à ESQUERDA (encaixa na varanda) e a saída no chão à direita. Arco-íris: mesmo formato, com as cores do arco-íris e brilho, para quando alguém desce. |
| 8 | Brilho | 40 × 40 | — | Estrelinha de brilho branca e rosa, para o efeito do escorregador e das frutinhas. |
| 9 | Balanço: estrutura | 300 × 380 | — | Duas colunas de madeira e uma trave em cima, com flores enroladas; SEM assento. |
| 10 | Balanço: assento | 130 × 260 | — | Assento de madeira rosa com as duas cordas até a trave (o jogo balança essa peça). |
| 11 | Cacho de frutinhas mágicas | 70 × 70 | com frutinhas · colhido | Cacho de frutinhas redondas rosa-brilhante com estrelinha; colhido: só as folhinhas rosa. Fica na copa. |
| 12 | Frutinha mágica | 30 × 30 | — | Uma frutinha solta, para colher, guardar no cesto e comer. |
| 13 | Mesa de piquenique | 320 × 130 | — | Mesa de madeira com dois bancos, vista de frente, com toalhinha xadrez rosa. |
| 14 | Cesto de piquenique | 90 × 70 | vazio · com frutinhas | Cesto de vime com tampa aberta e paninho rosa. |
| 15 | Bola colorida | 60 × 60 | — | Bola de brinquedo com gomos rosa, lilás, amarelo e azul. |
| 16 | Placas da trilha | 120 × 160 | para a casa · para a cabana | Placa de madeira num poste. SEM letras: uma com uma setinha e o desenho de uma casa, a outra com uma setinha e o desenho de uma cabana. |

### C08 — Dentro da casa na árvore (1600 × 900, chão a partir de y = 640)

| # | Peça | Tamanho | Estados | Pedido |
|---|---|---|---|---|
| 17 | Fundo do cômodo | 1600 × 900 | — | Cômodo pequeno de madeira clara: tábuas nas paredes, teto inclinado, janela redonda grande no centro com folhas rosa lá fora, cordão de luzinhas amarelas e chão de madeira. SEM porta, móveis ou brinquedos. |
| 18 | Porta, vista de dentro | 130 × 300 | fechada · aberta | A mesma porta roxa vista por dentro. Aberta: aparece a varanda e a copa rosa. |
| 19 | Cama com travesseiros | 360 × 150 | — | Cama baixa e fofa, colcha rosa com corações, vários travesseiros; para deitar duas. |
| 20 | Cozinha de brinquedo | 220 × 200 | desligada · ligada | Fogãozinho com bancada e prateleira, rosa e branco. Ligada: as bocas com luz laranja suave de brinquedo, sem fogo de verdade. |
| 21 | Panelinha | 50 × 35 | — | Panelinha de brinquedo com cabo. |
| 22 | Bule | 50 × 45 | — | Bule de chá com bolinhas. |
| 23 | Xícara | 25 × 25 | vazia · com chá | Xícara com pires; com chá: um fio de vapor em forma de coração. |
| 24 | Mesinha de chá | 180 × 80 | — | Mesinha redonda baixa com toalha de renda. |
| 25 | Cadeirinha | 60 × 80 | — | Cadeirinha de madeira com almofada rosa; o jogo usa três. |
| 26 | Baú de brinquedos | 160 × 160 | fechado · aberto | Baú de madeira com coração na tampa. Fechado, ocupa a parte de baixo do quadro. Aberto: a tampa levantada para trás e brinquedos aparecendo. As duas imagens com a base no mesmo lugar. |
| 27 | Mini unicórnio de pelúcia | 90 × 90 | — | Unicórnio rosa de pelúcia, sentado, crina lilás. |
| 28 | Ursinho herói | 80 × 100 | — | Ursinho de pelúcia com capa e máscara de herói INVENTADO: sem símbolo, cores ou roupa de herói existente. |
| 29 | Tapete redondo | 300 × 80 | — | Tapete oval visto de cima e de leve, lilás com borda de corações. |
| 30 | Passarinho | 40 × 35 | pousado · voando | Passarinho azul-claro redondinho, que aparece na janela. |

O ursinho comum reaproveita a pelúcia do quarto (`arte/cenario/3d/objeto_pelucia.png`): não precisa gerar outro.

---

## Entrega

Suba os arquivos em `arte/cenario/casa_arvore/3d/` com estes nomes.

**Pátio (C07):**

- `fundo_patio.png` (ou `fundo_patio_1.png` e `fundo_patio_2.png`)
- `arvore_casinha.png`, `grade_varanda.png`
- `porta_fechada.png`, `porta_aberta.png`
- `escada_madeira.png`, `escada_corda.png`
- `escorregador_rosa.png`, `escorregador_arco_iris.png`, `brilho.png`
- `balanco_estrutura.png`, `balanco_assento.png`
- `cacho_com.png`, `cacho_colhido.png`, `frutinha.png`
- `mesa_piquenique.png`, `cesto_vazio.png`, `cesto_cheio.png`, `bola.png`
- `placa_casa.png`, `placa_cabana.png`

**Dentro (C08):**

- `fundo_dentro.png`
- `porta_dentro_fechada.png`, `porta_dentro_aberta.png`
- `cama.png`
- `cozinha_desligada.png`, `cozinha_ligada.png`
- `panelinha.png`, `bule.png`, `xicara_vazia.png`, `xicara_cha.png`
- `mesinha_cha.png`, `cadeirinha.png`
- `bau_fechado.png`, `bau_aberto.png`
- `unicornio.png`, `ursinho_heroi.png`, `tapete.png`
- `passarinho_pousado.png`, `passarinho_voando.png`

Avise quando subir. Eu monto o cenário no jogo e confiro:

- se a Catarina passa pela porta e fica de pé na varanda atrás da grade;
- se as escadas e o escorregador encaixam na varanda;
- se o balanço e a mesa cabem os personagens.
