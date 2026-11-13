# Quarto da Carol: prompts para gerar as peças 3D (copiar e colar)

Desenvolvimento do cenário: `docs/Fazenda_Capricho_Cenarios.docx`, seção C06.

**Proposta:** cores, cama e objetos ainda precisam da aprovação das criadoras (pendência do GDD). Ajuste a tabela antes de gerar.

Layout na escala do jogo, nesta pasta: `quarto_carol_layout.png` (2200 × 900, chão a partir de y = 600). As peças 2D provisórias,
com os mesmos nomes e tamanhos, estão em `2d/` e já servem de rascunho de forma para cada pedido.

Mesmo processo do quarto, do estábulo e da casa na árvore: **uma conversa só**. Envie primeiro a mensagem
de contexto e depois um pedido por peça (os estados da mesma peça juntos, numa mensagem só).

---

## Mensagem 1: contexto (enviar uma vez)

**Anexar:** `quarto_carol_layout.png`, duas peças 3D do quarto para o estilo (`arte/cenario/3d/beliche.png` e
`arte/cenario/3d/mesinha.png`) e a imagem oficial da Catarina (`arte/personagens/catarina.png`).

```
Vou gerar, uma peça por vez, o cenário QUARTO DA CAROL do jogo infantil "Fazenda Capricho" (iPad, faz de
conta no estilo Avatar World). É o quarto da mãe, a Carol: calmo, rosa-claro e lilás com madeira, com cama de casal de cabeceira de coração, onde a Catarina dorme com a mãe quando quiser.

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
| 1 | Fundo do quarto | 2200 × 900 | — | Parede rosa-clara com listras lilás bem suaves, vigas de madeira no alto, janela com cortina lilás e vista da fazenda, três quadrinhos da família (coração, flor e ferradura), rodapé e piso de madeira. SEM porta e sem móveis. |
| 2 | Cama de casal | 620 × 330 | — | Cabeceira acolchoada rosa em forma de coração sobre moldura de madeira. Colchão PLANO e branco, a cerca de 130 px do chão, com pelo menos 560 px de comprimento: deitam 3 (Carol, Catarina e Bob). Sem cobertor (é a peça 3). |
| 3 | Cobertor | 560 × 110 | cobrindo · dobrado | Cobertor lilás com coraçõezinhos e barra branca. Cobrindo: estendido sobre o colchão. Dobrado: só no pé da cama. |
| 4 | Travesseiro | 130 × 60 | — | Travesseiro rosa-claro fofinho com coração. |
| 5 | Criado-mudo | 130 × 150 | — | Mesinha de cabeceira de madeira com duas gavetas, tampo PLANO. |
| 6 | Abajur de mesa | 80 × 110 | apagado · aceso | Abajur lilás com cúpula clara e coração. Apagado deixa o quarto na hora de dormir. |
| 7 | Guarda-roupa | 300 × 420 | fechado · aberto | Guarda-roupa de madeira com portas rosa-claro e corações. Aberto: cabide com quatro vestidos/blusas coloridos e sapatos embaixo. |
| 8 | Penteadeira com espelho | 260 × 360 | normal · brilho | Espelho oval lilás com coração em cima, tampo de madeira e gavetas. Brilho: o espelho reluz com estrelinhas. |
| 9 | Banquinho | 100 × 100 | — | Banquinho redondo com assento rosa, para sentar 1 na penteadeira. |
| 10 | Escova de cabelo | 80 × 40 | — | Escova rosa e lilás com coração; na Catarina, as tranças brilham. |
| 11 | Tapete | 520 × 120 | — | Tapete oval lilás e rosa com florzinhas, visto de cima e de leve. |
| 12 | Porta-retratos | 60 × 66 | coração · paisagem | Moldurinha dourada com um coração ou uma paisagem (sem pessoas). |
| 13 | Planta | 90 × 130 | — | Planta de folhas largas num vaso lilás. |
| 14 | Porta e plaquinha | porta 170 × 350 · placa 70 × 60 | fechada · aberta | A mesma porta das outras salas, num tom de madeira mais rosado; plaquinha com a casinha (volta para a sala). |

Gere primeiro a cama com o cobertor e os travesseiros: é onde a Carol, a Catarina e o Bob deitam juntos.

---

## Entrega

Suba os arquivos em `arte/cenario/quarto_carol/3d/` com estes nomes (os mesmos da pasta `2d/`):

- Fundo do quarto: `fundo.png`
- Cama de casal: `cama.png`
- Cobertor: `cobertor_coberto.png`, `cobertor_dobrado.png`
- Travesseiro: `travesseiro.png`
- Criado-mudo: `criado_mudo.png`
- Abajur de mesa: `abajur_apagado.png`, `abajur_aceso.png`
- Guarda-roupa: `guarda_roupa_fechado.png`, `guarda_roupa_aberto.png`
- Penteadeira com espelho: `penteadeira.png`, `penteadeira_brilho.png`
- Banquinho: `banquinho.png`
- Escova de cabelo: `escova_cabelo.png`
- Tapete: `tapete.png`
- Porta-retratos: `porta_retrato_coracao.png`, `porta_retrato_paisagem.png`
- Planta: `planta.png`
- Porta e plaquinha: `porta_fechada.png`, `porta_aberta.png`, `placa_casa.png`

Avise quando subir: eu troco as peças 2D pelas 3D no jogo e confiro o encaixe com os personagens.
