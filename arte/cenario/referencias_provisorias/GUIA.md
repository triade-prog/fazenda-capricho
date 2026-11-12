# Fazenda Capricho — elementos do quarto para gerar em 3D

Esta pasta tem **cada elemento do quarto da Catarina separado**, exportado do protótipo, com fundo
transparente. Os desenhos atuais são **provisórios**: servem para mostrar **forma, tamanho, posição e
função** de cada peça. A arte final deve ser gerada em 3D no mesmo estilo da Nina v2.

Arquivos de referência de tamanho:

- `referencia_quarto_completo.png`: o quarto inteiro como está no jogo, com todos os personagens;
- `referencia_escala_anotada.png`: a mesma imagem, com o tamanho de cada elemento marcado.

## Regras para todos os elementos

1. **Estilo igual ao da Nina v2**: brinquedo 3D estilizado (`3d-toy`), formas arredondadas e macias,
   materiais simples, cores pastel da fazenda (rosa, lilás, roxo, madeira clara, verde), sem realismo.
2. **Vista de frente**, sem girar o objeto, como no jogo: a câmera olha de frente para a parede do quarto.
   A luz vem de cima e um pouco da esquerda, a mesma em todos os elementos.
3. **Fundo transparente** (ou magenta #FF00FF puro para recortar, como na Nina, sem magenta no objeto).
4. **Sem sombra no chão**: o jogo desenha as sombras.
5. **Um elemento por imagem**, inteiro, sem cortar bordas, sem texto e sem moldura.
6. **Proporções da tabela abaixo**: a largura e a altura podem variar até ±10%. Mais do que isso
   desencaixa os personagens (deitar, entrar no castelinho, escorregar).
7. **Resolução**: pelo menos **2 vezes** o tamanho em pixels do jogo. Os PNGs desta pasta já estão em 2x.

## Os elementos

Tamanhos em pixels do jogo. A Catarina tem **300 px** de altura. O chão do quarto fica na altura y = 600.

| Arquivo de referência | Elemento | Tamanho no jogo | O que precisa ser respeitado |
|---|---|---|---|
| `beliche.png` | Beliche rosa com cabeceira de coração | 464 × 462 (1,54× Catarina) | Colchão de cima **plano**, a 330 px do chão, com pelo menos 420 px de comprimento: é onde os personagens deitam (cabem 3). Embaixo, vão livre de 270 px de altura para o castelinho. |
| `castelo_frente_porta_fechada.png` e `castelo_frente_porta_aberta.png` | Frente do castelinho de ursinhos (embaixo do beliche) | 420 × 266 (0,89×) | **A porta roxa em camada separada**, em dois estados: fechada e aberta. A abertura da porta tem **92 × 176 px**, com o centro a 220 px da borda esquerda do castelinho: quem entra aparece por ela. Almofadas de urso na parede. |
| `castelo_interior.png` | Fundo de dentro do castelinho | 420 × 270 | Fica **atrás** dos personagens; aparece pela porta aberta. Mais escuro que a frente. |
| `escada.png` | Escada de madeira | 46 × 312 (1,04×) | Vai do chão até a altura do colchão, encostada no lado esquerdo do beliche. |
| `escorregador.png` | Escorregador lilás | 308 × 348 (1,16×) | Começa na ponta direita do colchão (a 300 px do chão) e termina no chão, 270 px para a direita, numa curva parecida. O personagem desliza **por cima** dele. |
| `tapete.png` | Tapete oval lilás com coraçõezinhos | 680 × 190 | Visto de cima em perspectiva, como um oval achatado no chão. |
| `janela.png` | Janela com cortinas roxas e vista da fazenda | 340 × 288 (0,96×) | Decorativa. Vista: céu, sol, morrinhos verdes, florzinhas e árvore rosa. |
| `porta.png` | Porta de madeira com coração | 170 × 350 (1,17×) | Decorativa por enquanto; no futuro leva para fora do quarto. |
| `quadro_ferradura.png` | Quadro da ferradura com coração | 182 × 162 (0,54×) | Pode usar o ícone da ferradura da marca. |
| `mesinha.png` | Mesinha de madeira | 230 × 96 (0,32×) | Tampo **plano**: o pote e os objetos ficam em cima. |
| `pote_biscoitos.png` | Pote de vidro com biscoitos de coração | 92 × 103 (0,34×) | Tocar no pote dá um biscoito: precisa ser fácil de reconhecer. |
| `varal_coracoes.png` | Varal de coraçõezinhos | faixa de 2200 de largura | **Repete na horizontal** sem emenda aparente. |
| `parede.png` | Parede listrada rosa com rodapé | 2200 × 600 | Textura que **repete na horizontal** (o quarto é mais largo que a tela). |
| `piso.png` | Piso de madeira clara | 2200 × 300 | Textura que **repete na horizontal**, em perspectiva leve. |

## Objetos que os personagens seguram

Imagens em 4x. Os tamanhos abaixo são no jogo.

| Arquivo | Objeto | Tamanho no jogo | Observação |
|---|---|---|---|
| `objeto_biscoito.png` | Biscoito de coração para os bichos | ~52 px de largura | Petisco de **animal**, não doce de gente. |
| `objeto_pelucia.png` | Ursinho de pelúcia | ~80 × 100 | Ursinho original, **sem personagem de marca**. |
| `objeto_escova.png` | Escova de pelo | ~90 × 45 | Cabo rosa e cerdas claras; precisa caber na mão da Catarina. |
| `objeto_almofada.png` | Almofada de ursinho | ~84 × 60 | Formato de cara de urso. |

## Texto para pedir cada elemento (trocar o que está entre colchetes)

> Gere **um** elemento de cenário para o jogo infantil Fazenda Capricho, no **mesmo estilo da Nina v2**:
> brinquedo 3D estilizado, formas arredondadas, materiais simples, cores pastel, sem realismo.
> Elemento: **[nome e descrição da tabela]**. Use a imagem anexada **só como referência de forma,
> proporção e posição**, não de estilo. Vista de frente, sem perspectiva lateral, luz de cima e da
> esquerda. Fundo transparente (ou magenta #FF00FF puro, sem magenta no objeto), sem sombra no chão,
> sem texto, sem moldura, objeto inteiro e centralizado. Proporção **[largura × altura da tabela]**,
> em resolução de pelo menos **[2x o tamanho]** px. **[O que precisa ser respeitado, da tabela]**.

Anexe sempre: o PNG do elemento + `referencia_escala_anotada.png` + a folha da Nina (para o estilo).

## Ordem sugerida

1. **Beliche + castelinho (com a porta em separado) + escada + escorregador**: é a peça central das
   brincadeiras e as quatro precisam encaixar entre si. Gere juntas e confira o encaixe.
2. Objetos que os personagens seguram (biscoito, pelúcia, escova, almofada).
3. Mesinha e pote.
4. Janela, porta e quadro.
5. Parede, piso, varal e tapete.

Quando cada grupo ficar pronto, suba em `arte/cenario/3d/` no GitHub. Eu coloco no jogo, confiro se
os personagens ainda deitam, entram e escorregam no lugar certo, e mando as capturas para aprovação.
