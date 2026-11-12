# Prompts para gerar o cenário 3D (copiar e colar)

Use **uma conversa só** para todo o cenário, para o estilo ficar igual em todas as peças.
Primeiro envie a **mensagem 1 (contexto)** e depois **uma mensagem por elemento**, sempre com o arquivo
indicado.

---

## Mensagem 1: contexto (enviar uma vez, no começo)

**Anexar:** `referencia_escala_anotada.png`, `referencia_quarto_completo.png` e a folha da Nina
(`arte/animacoes/nina_pet_v2/final/spritesheet-extended.png`).

```
Vou gerar, uma peça por vez, o cenário do quarto da Catarina para o jogo infantil "Fazenda Capricho"
(iPad, brincadeira de faz de conta no estilo Avatar World).

ESTILO: o mesmo da folha da Nina anexada: brinquedo 3D estilizado ("3d-toy"), formas arredondadas e
macias, materiais simples e foscos, cores pastel (rosa, lilás, roxo, madeira clara, verde-claro),
fofo e aconchegante, sem realismo fotográfico.

REFERÊNCIAS: as imagens do quarto anexadas são um protótipo PROVISÓRIO em desenho plano. Use-as SÓ
para forma, proporção, tamanho e posição de cada peça. NÃO copie o estilo plano nem os contornos.
A imagem anotada mostra o tamanho de cada peça em relação à Catarina (300 px de altura no jogo).

REGRAS PARA TODAS AS PEÇAS:
1. Uma peça por imagem, inteira, centralizada, sem cortar bordas.
2. Vista de frente (câmera olhando de frente para a parede do quarto), sem girar a peça para o lado.
3. Luz suave de cima e um pouco da esquerda, igual em todas as peças.
4. Fundo totalmente transparente (PNG). Se não for possível, fundo magenta puro #FF00FF liso, e nada
   magenta ou lilás muito saturado na peça.
5. Sem sombra no chão, sem cenário em volta, sem texto, sem moldura, sem personagens.
6. Manter a proporção (largura × altura) que eu passar em cada pedido, com no máximo 10% de diferença.
7. Resolução alta: no mínimo o dobro do tamanho em pixels indicado.

Responda só "Entendido" e espere o primeiro pedido.
```

---

## Grupo 1: beliche, castelinho, escada e escorregador (gerar nesta ordem)

### 1.1 Beliche
**Anexar:** `beliche.png`
```
Peça 1: BELICHE rosa com cabeceira em forma de coração, só a cama de cima (embaixo fica um vão vazio,
onde vai o castelinho, que é outra peça). Proporção 464 × 462 (quase quadrada). Colchão de cima branco
com coraçõezinhos rosa e travesseiro branco à esquerda. O topo do colchão precisa ser RETO e PLANO,
ocupando quase toda a largura, porque os personagens deitam ali. Quatro colunas rosa até o chão; o vão
embaixo da cama deve ficar vazio e transparente, com altura de cerca de 58% da altura total.
Resolução mínima 928 × 924 px.
```

### 1.2 Castelinho, frente com a porta FECHADA
**Anexar:** `castelo_frente_porta_fechada.png`
```
Peça 2: FRENTE DO CASTELINHO DE URSINHOS que fica embaixo do beliche. Parede rosa-clara com ameias
pequenas no alto, duas almofadas em forma de rosto de urso marrom (uma de cada lado) e uma PORTA ROXA
em arco, com coração lilás e maçaneta amarela, perto do centro. Proporção 420 × 266 (larga e baixa).
A porta tem 92 × 176 (estreita e alta, cerca de 22% da largura e 66% da altura da peça), apoiada no chão.
Resolução mínima 840 × 532 px.
```

### 1.3 Castelinho, frente com a porta ABERTA (mesma peça, só a porta muda)
**Anexar:** `castelo_frente_porta_aberta.png`
```
Peça 3: a MESMA frente do castelinho da peça 2, idêntica em tudo, mas com a porta roxa ABERTA: a folha
da porta girada para o lado direito, e o vão da porta TOTALMENTE TRANSPARENTE (é por ali que se vê quem
entrou). Mesmo tamanho e mesma posição da peça 2, para trocar uma pela outra sem mexer.
```

### 1.4 Interior do castelinho
**Anexar:** `castelo_interior.png`
```
Peça 4: FUNDO DE DENTRO DO CASTELINHO, a parede que aparece pela porta aberta, atrás dos personagens.
Retângulo 420 × 270, rosa mais escuro e aconchegante, com dois corações em relevo suave e luz mais fraca
que a frente. Resolução mínima 840 × 540 px.
```

### 1.5 Escada
**Anexar:** `escada.png`
```
Peça 5: ESCADA DE MADEIRA clara, estreita e alta, proporção 46 × 312 (bem fina), com 7 degraus
arredondados. Ela fica encostada no lado esquerdo do beliche, do chão até a altura do colchão.
Resolução mínima 92 × 624 px.
```

### 1.6 Escorregador
**Anexar:** `escorregador.png`
```
Peça 6: ESCORREGADOR lilás com borda rosa, visto de lado como na referência: começa no alto à esquerda
(na altura do colchão do beliche) e desce numa curva suave até o chão, à direita, terminando com uma
pontinha arredondada. Proporção 308 × 348. A rampa precisa ser lisa e contínua, porque o personagem
desliza por cima dela. Resolução mínima 616 × 696 px.
```

Depois do grupo 1: suba as 6 imagens em `arte/cenario/3d/` com os mesmos nomes dos arquivos de
referência (`beliche.png`, `castelo_frente_porta_fechada.png` etc.) e me avise. Eu confiro o encaixe no
jogo antes de seguir para os próximos grupos.

---

## Grupo 2: objetos que os personagens seguram

### 2.1 Biscoito de coração
**Anexar:** `objeto_biscoito.png`
```
Objeto: BISCOITO DE CORAÇÃO para cães e gatos (petisco de animal, não doce de gente), dourado com
pontinhos rosa. Pequeno e fácil de reconhecer. Proporção quase quadrada. Resolução mínima 256 × 256 px.
```

### 2.2 Ursinho de pelúcia
**Anexar:** `objeto_pelucia.png`
```
Objeto: URSINHO DE PELÚCIA marrom e fofinho, sentado, com um coração rosa na barriga. Ursinho original,
sem nenhum personagem de marca. Proporção 80 × 100. Resolução mínima 320 × 400 px.
```

### 2.3 Escova
**Anexar:** `objeto_escova.png`
```
Objeto: ESCOVA DE PELO para animais, horizontal, com cabo rosa (coração branco no cabo) e cabeça roxa
com cerdas claras viradas para baixo. Precisa caber na mão de uma criança. Proporção 90 × 45.
Resolução mínima 360 × 180 px.
```

### 2.4 Almofada de ursinho
**Anexar:** `objeto_almofada.png`
```
Objeto: ALMOFADA rosa em forma de rosto de urso, com orelhinhas, olhos e focinho, macia e fofa.
Proporção 84 × 60. Resolução mínima 336 × 240 px.
```

---

## Grupo 3: mesinha e pote

### 3.1 Mesinha
**Anexar:** `mesinha.png`
```
Peça: MESINHA DE MADEIRA clara, baixa e larga, proporção 230 × 96, com tampo RETO e PLANO (objetos ficam
em cima) e duas pernas. Resolução mínima 460 × 192 px.
```

### 3.2 Pote de biscoitos
**Anexar:** `pote_biscoitos.png`
```
Peça: POTE DE VIDRO com tampa rosa e puxador lilás, cheio de biscoitos de coração dourados à mostra.
Proporção 92 × 103. Precisa ser fácil de reconhecer, porque a criança toca nele para ganhar um biscoito.
Resolução mínima 184 × 206 px.
```

---

## Grupo 4: janela, porta e quadro

### 4.1 Janela
**Anexar:** `janela.png`
```
Peça: JANELA com moldura branca, cortinas roxas dos dois lados e varão de madeira no alto. Pelo vidro,
a vista da fazenda: céu azul-claro, sol amarelo, morrinhos verdes com florzinhas rosa e uma árvore rosa.
Proporção 340 × 288. Resolução mínima 680 × 576 px.
```

### 4.2 Porta
**Anexar:** `porta.png`
```
Peça: PORTA DE MADEIRA clara com o alto em arco, coração rosa no alto, dois painéis e maçaneta amarela.
Proporção 170 × 350 (estreita e alta). Resolução mínima 340 × 700 px.
```

### 4.3 Quadro
**Anexar:** `quadro_ferradura.png` e o ícone da ferradura da marca
```
Peça: QUADRO com moldura de madeira e, dentro, a ferradura dourada com coração rosa (igual ao ícone da
marca anexado). Proporção 182 × 162. Resolução mínima 364 × 324 px.
```

---

## Grupo 5: parede, piso, varal e tapete

### 5.1 Parede
**Anexar:** `parede.png`
```
Peça: PAREDE do quarto, listras verticais em dois tons de rosa-claro e rodapé rosa embaixo, como uma
TEXTURA QUE REPETE NA HORIZONTAL sem emenda aparente (a borda esquerda continua na direita).
Proporção 2200 × 600; pode ser entregue um pedaço de 1100 × 600 que repete. Sem janela, porta ou móveis.
```

### 5.2 Piso
**Anexar:** `piso.png`
```
Peça: PISO de tábuas de madeira clara, visto em perspectiva leve (tábuas horizontais, as de trás um
pouco mais finas), como TEXTURA QUE REPETE NA HORIZONTAL sem emenda. Proporção 2200 × 300; pode ser um
pedaço de 1100 × 300 que repete.
```

### 5.3 Varal de coraçõezinhos
**Anexar:** `varal_coracoes.png`
```
Peça: VARAL com cordinha ondulada e coraçõezinhos rosa e lilás pendurados, alternando cores, em faixa
horizontal que REPETE sem emenda. Fundo transparente. Faixa de 1100 × 60 (repete).
```

### 5.4 Tapete
**Anexar:** `tapete.png`
```
Peça: TAPETE OVAL lilás, com uma faixa mais clara por dentro e coraçõezinhos brancos, visto deitado no
chão em perspectiva (oval bem achatado). Proporção 680 × 190. Resolução mínima 1360 × 380 px.
```
