# Cabana externa: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C12.

**Proposta:** a aparência e as brincadeiras da cabana ainda precisam da definição das criadoras. Ajuste a tabela antes de gerar.

Layout na escala do jogo, nesta pasta: `cabana_layout.png` (2200 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `cabana_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário CABANA EXTERNA do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É uma cabana de faz de conta no quintal, de madeira e tecido, para acampar e contar histórias, com almofadas, lanterna e bandeirinhas.

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
| 1 | Fundo do quintal | 2200 × 900 | — | Quintal com duas árvores grandes, céu claro, morros, cerca branca e um varal de bandeirinhas coloridas entre as árvores, grama com florzinhas. SEM a cabana e os objetos. |
| 2 | Cabana de tecido | 460 × 380 | fechada · aberta | Tenda triangular de madeira e tecido rosa-claro com listras, bandeirinha no topo e entrada de tecido lilás. Aberta: as abas presas para os lados, interior escuro e aconchegante (quem entra some, como no castelinho). |
| 3 | Saco de dormir e almofadas | 320 × 90 | — | Saco de dormir azul com estrelinhas e duas almofadas, rosa e lilás. Deitam até 3. |
| 4 | Lanterna | 60 × 100 | desligada · ligada | Lanterna de acampar verde com estrela; ligada, dentro da cabana fica 'de noite'. |
| 5 | Livro de figuras | 70 × 50 | fechado · aberto | Livro com estrela na capa; aberto mostra desenhos (sol, coração), sem letras. |
| 6 | Fogueira de mentirinha | 170 × 120 | normal · brilhando | Fogueira de FELTRO com costuras aparentes, lenha de brinquedo e pedrinhas em volta. Sem fogo de verdade; tocar faz brilhar. |
| 7 | Binóculo | 64 × 44 | — | Binóculo de brinquedo roxo e lilás com alça rosa. |
| 8 | Banco de tronco | 200 × 80 | — | Tronco deitado para sentar em volta da fogueira. |
| 9 | Passarinho | 40 × 35 | — | Passarinho azul-claro para olhar de binóculo. |

---

## Entrega

Suba os arquivos em `arte/cenario/cabana/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo do quintal: `fundo.png`
- Cabana de tecido: `cabana_fechada.png`, `cabana_aberta.png`
- Saco de dormir e almofadas: `saco_dormir.png`
- Lanterna: `lanterna_desligada.png`, `lanterna_ligada.png`
- Livro de figuras: `livro_fechado.png`, `livro_aberto.png`
- Fogueira de mentirinha: `fogueira.png`, `fogueira_brilho.png`
- Binóculo: `binoculo.png`
- Banco de tronco: `tronco_banco.png`
- Passarinho: `passarinho.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
