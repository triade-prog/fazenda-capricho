# Entrada da Fazenda: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C01.

**Pendência:** a Entrada pode ser só a ilustração do mapa. As peças servem para os dois usos.

Layout na escala do jogo, nesta pasta: `entrada_layout.png` (2200 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `entrada_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e o conceito `arte/conceito/cenarios_R01/01_entrada_fazenda.png` (só o clima, sem cactos) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário ENTRADA DA FAZENDA do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É a chegada: portal de madeira com a placa da Fazenda Capricho, flores e lanternas; ao fundo, a fazenda.

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
| 1 | Fundo da Entrada | 2200 × 900 | — | Céu claro, morros, ao longe um celeiro ROSA e casinhas em tons rosados, árvores floridas, cerca branca, estrada de terra subindo para o portal e os dois pilares de pedra do portal. SEM portão, arco, logo, moinho, lanternas, caixa de correio, floreiras e banco. SEM cactos. |
| 2 | Portão de duas folhas | 560 × 280 | fechado · aberto | Duas folhas de madeira em 'X' com um coração rosa em cada, entre os pilares. Aberto: as folhas giradas para trás, estreitas junto aos pilares. |
| 3 | Arco do portal | 820 × 220 | — | Viga de madeira em arco coberta de folhas e flores rosa e lilás, com uma tabuleta clara VAZIA no centro: a logo da Fazenda Capricho é peça separada (folha de pulso da R01), não pinte letras. |
| 4 | Lanterna do portal | 60 × 110 | apagada · acesa | Lanterna de fazenda pendurada no pilar; acesa, luz quente. |
| 5 | Moinho | torre 200 × 380 · hélice 240 × 240 | — | Torre de madeira treliçada e, numa imagem separada, a hélice de pás rosa e brancas com coração no centro, para o jogo girar. |
| 6 | Caixa de correio | 122 × 170 | fechada · aberta | Caixinha rosa arredondada num poste, com bandeirinha dourada e coração. Aberta: aparece uma cartinha. |
| 7 | Cartinha | 50 × 36 | — | Envelope branco com coração (o desenho de dentro é feito pelo jogo). |
| 8 | Floreira | 220 × 110 | com flores · colhida | Jardineira de madeira com flores rosa, lilás, amarelas e brancas. |
| 9 | Flor solta | 25 × 55 | — | Flor rosa com caule, para dar a um personagem. |
| 10 | Banco | 260 × 110 | — | Banco de madeira com coração no encosto; sentam 2. |

Gere primeiro o portão (os dois estados) e o arco, que encaixam nos pilares do fundo.

---

## Entrega

Suba os arquivos em `arte/cenario/entrada/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo da Entrada: `fundo.png`
- Portão de duas folhas: `portao_fechado.png`, `portao_aberto.png`
- Arco do portal: `arco_portal.png`
- Lanterna do portal: `lanterna_apagada.png`, `lanterna_acesa.png`
- Moinho: `moinho_torre.png`, `moinho_helice.png`
- Caixa de correio: `correio_fechado.png`, `correio_aberto.png`
- Cartinha: `cartinha.png`
- Floreira: `floreira.png`, `floreira_colhida.png`
- Flor solta: `flor.png`
- Banco: `banco.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
