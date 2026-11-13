# Pet Care: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C10.

**Sem casinha de cachorro:** a colagem tem uma, mas o GDD diz que o Bob dorme com a família. Ela fica de fora até as criadoras decidirem.

Layout na escala do jogo, nesta pasta: `pet_care_layout.png` (2600 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `pet_care_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e a colagem `arte/conceito/colagem_cenarios/colagem_pet_care.png` (só o clima) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário PET CARE do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É o cantinho ao ar livre para cuidar dos bichos: banho de espuma, toalha, comidinha, brinquedos e um cercadinho para acalmar.

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
| 1 | Fundo do Pet Care | 2600 × 900 | — | Céu claro, morros verdes, duas árvores floridas, cerca branca, grama com florzinhas e, no centro, uma pérgola de madeira coberta de flores rosa com piso de pedrinhas claras. SEM banheira, chuveiro, tigelas ou cercadinho. |
| 2 | Banheira com patinha | 300 × 170 | vazia · com água · com espuma | Banheira branca com pezinhos, borda rosa e uma patinha rosa na frente. Espuma: montinho de bolhas brancas por cima. Os bichos entram nela. |
| 3 | Chuveirinho | 140 × 320 | desligado · ligado | Coluna de chuveiro prateada de brinquedo com registro rosa de coração. Ligado: água azul-clara caindo em fios fofos, sem respingo no chão. |
| 4 | Xampu | 40 × 60 | — | Frasquinho rosa com tampa lilás e patinha. |
| 5 | Toalha | 100 × 60 | — | Toalha azul-clara com barra branca e patinha. |
| 6 | Bolha de sabão | 30 × 30 | — | Bolha branca com reflexo rosa (efeito). |
| 7 | Tigelas | 80 × 40 | vazia · cheia (cão, gato, água) | Tigela rosa (ração de cachorro), lilás (ração de gato) e azul (água), com patinha. |
| 8 | Petiscos | biscoito 40 × 36 · peixinho 44 × 26 | — | Biscoito de coração (cães) e peixinho azul de petisco (gatos). |
| 9 | Brinquedos | bolinha 30 × 30 · osso 56 × 26 · varinha 40 × 120 | — | Bolinha amarela, osso de brinquedo branco e varinha com penas coloridas (o Leo pula atrás). |
| 10 | Cercadinho | 420 × 180 | — | Cercadinho branco baixo com coração e flores, com uma caminha rosa redonda dentro: lugar seguro para o bicho se acalmar e cochilar. |
| 11 | Prateleira e gancho | prateleira 220 × 140 · gancho 60 × 40 | — | Prateleira de madeira com duas tábuas VAZIAS (xampu e brinquedos são peças separadas) e gancho para a toalha. |
| 12 | Placa e vaso | placa 90 × 80 · vaso 70 × 90 | — | Plaquinha de madeira com patinha (sem letras) e vaso de flores rosa. |

Gere primeiro a banheira com os três estados e o chuveirinho: são o centro da brincadeira.

---

## Entrega

Suba os arquivos em `arte/cenario/pet_care/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo do Pet Care: `fundo.png`
- Banheira com patinha: `banheira_vazia.png`, `banheira_agua.png`, `banheira_espuma.png`
- Chuveirinho: `chuveirinho_desligado.png`, `chuveirinho_ligado.png`
- Xampu: `xampu.png`
- Toalha: `toalha.png`
- Bolha de sabão: `bolha.png`
- Tigelas: `tigela_cao_vazia.png`, `tigela_cao_cheia.png`, `tigela_gato_vazia.png`, `tigela_gato_cheia.png`, `tigela_agua_vazia.png`, `tigela_agua_cheia.png`
- Petiscos: `biscoito.png`, `peixinho.png`
- Brinquedos: `bolinha.png`, `osso.png`, `varinha_pena.png`
- Cercadinho: `cercadinho.png`
- Prateleira e gancho: `prateleira.png`, `gancho_toalha.png`
- Placa e vaso: `placa_pata.png`, `vaso_flores.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
