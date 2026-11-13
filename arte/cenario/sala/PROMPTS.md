# Sala da Família: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C03.

Layout na escala do jogo, nesta pasta: `sala_layout.png` (2200 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `sala_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e a colagem `arte/conceito/colagem_cenarios/colagem_sala.png` (só o clima: o jogo é visto DE FRENTE, sem teto) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário SALA DA FAMÍLIA do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É o coração da casa: sofá lilás, lareira de pedra com coração e mesa de centro; dela saem as portas para os quartos, a cozinha e a frente da casa.

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
| 1 | Fundo da sala | 2200 × 900 | — | Parede rosa-clara com listras suaves e vigas de madeira no alto, janela com cortina rosa e vista da fazenda, três plantas penduradas, quadro de um celeiro rosa, rodapé e piso de madeira clara. SEM lareira, portas ou móveis. |
| 2 | Lareira de pedra | 420 × 420 | — | Lareira de pedras arredondadas creme com prateleira de madeira e um coração rosa grande no alto. Boca da lareira escura e VAZIA (o fogo é a peça 3). |
| 3 | Fogo da lareira | 140 × 90 | baixo · alto | Foguinho de brinquedo, laranja e amarelo, que encaixa na boca da lareira. Alto: chamas maiores e estrelinhas. |
| 4 | Sofá lilás | 460 × 200 | — | Sofá fofo de três lugares, lilás com encosto acolchoado e pés de madeira. Assento plano a 110 px do chão do sofá, onde sentam 3 ou deita 1. |
| 5 | Almofada de coração | 70 × 60 | rosa · lilás | Almofada em forma de coração com costura aparente. |
| 6 | Mesa de centro | 260 × 100 | — | Mesa redonda baixa de madeira, tampo PLANO para apoiar objetos. |
| 7 | Vaso de flores | 50 × 70 | — | Vaso rosa com flores amarelas. |
| 8 | Tapete redondo | 600 × 150 | — | Tapete de palha trançada visto de cima e de leve, oval. |
| 9 | Abajur | 90 × 200 | apagado · aceso | Abajur de pé de madeira com cúpula rosa-clara e coração. Aceso: cúpula clara e brilho quente em volta. |
| 10 | Estante | 300 × 330 | — | Estante de madeira com três prateleiras VAZIAS (os objetos são peças separadas). |
| 11 | Objetos da estante | livro 40 × 50 · porta-retrato 50 × 50 · plantinha 50 × 60 | livro rosa · livro azul | Livros de figura com estrelinha na capa (sem letras), porta-retrato lilás com paisagem, vasinho com planta. |
| 12 | Cesto de brinquedos | 140 × 110 | — | Cesto de vime com coração; aparecem uma bola amarela e um ursinho. |
| 13 | Porta da casa | 170 × 350 | fechada · aberta | A mesma porta de madeira do quarto (arredondada no alto). Aberta: folha encostada e luz quente do outro cômodo. Serve para as 4 portas. |
| 14 | Plaquinhas das portas | 70 × 60 | coração · flor · panela · casinha | Plaquinha de madeira pendurada acima de cada porta, SEM letras: coração (quarto da Catarina), flor (quarto da Carol), panelinha (cozinha) e casinha (porta da frente). |

Gere primeiro a lareira com o fogo, o sofá e a porta: são as peças das brincadeiras principais.
A lareira é decorativa: o fogo só crepita, não aceita objetos nem personagens.

---

## Entrega

Suba os arquivos em `arte/cenario/sala/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo da sala: `fundo.png`
- Lareira de pedra: `lareira.png`
- Fogo da lareira: `fogo_baixo.png`, `fogo_alto.png`
- Sofá lilás: `sofa.png`
- Almofada de coração: `almofada_rosa.png`, `almofada_lilas.png`
- Mesa de centro: `mesa_centro.png`
- Vaso de flores: `vaso_flores.png`
- Tapete redondo: `tapete.png`
- Abajur: `abajur_apagado.png`, `abajur_aceso.png`
- Estante: `estante.png`
- Objetos da estante: `livro_rosa.png`, `livro_azul.png`, `porta_retrato.png`, `plantinha.png`
- Cesto de brinquedos: `cesto_brinquedos.png`
- Porta da casa: `porta_fechada.png`, `porta_aberta.png`
- Plaquinhas das portas: `placa_coracao.png`, `placa_flor.png`, `placa_panela.png`, `placa_casa.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
