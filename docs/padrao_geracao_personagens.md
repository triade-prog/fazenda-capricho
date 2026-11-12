# Padrão de geração de personagens — folhas de pet

Padrão definido a partir da **Nina v2** (`arte/animacoes/nina_pet_v2/`), gerada com a ferramenta de pets
do ChatGPT. Ela já está no protótipo: corre quando é arrastada, acena ao toque, pula ao ganhar biscoito,
fica triste quando não cabe num lugar e acompanha com o olhar o objeto que a criança arrasta.

> **Decisão pendente:** adotar o estilo `3d-toy` para todos os personagens depende do teste da Nina no
> iPad, ao lado dos personagens 2D (Catarina, Carol, Bob, Leo, Zoe e Lumi). Se for aprovado, os demais
> são gerados de novo neste padrão, na ordem da seção "Ordem de produção".

## O que pedir na geração

| Item | Valor |
|---|---|
| Ferramenta | pets do ChatGPT (mesmo processo da Nina v2) |
| Estilo | `3d-toy` (o mesmo da Nina) |
| Referência de identidade | a imagem oficial do personagem em `arte/personagens/` |
| Grade | 8 colunas × 11 linhas, mesmas ações e mesma ordem da Nina (tabela abaixo) |
| Quadro | **384 × 416 px** se a ferramenta permitir (o dobro da Nina, para ficar nítido no iPad); se não, 192 × 208 px |
| Fundo | transparente na folha final (o magenta é só da etapa de recorte) |
| Pés | na mesma linha do chão em todas as ações, menos no pulo e na corrida |

A escala entre os personagens **não** precisa vir na folha: o jogo aplica a tabela de escala do GDD
(Catarina 1,00; Carol 1,35; Lumi 1,30; Nina 0,62; Bob 0,57; Zoe 0,42; Leo 0,35). Cada personagem pode
ocupar o quadro inteiro, como a Nina.

## Como o jogo usa cada linha

| Linha | Ação na folha | No jogo |
|---|---|---|
| 0 | `idle` | parado no quarto (a respiração já vem desenhada) |
| 1 | `running-right` | sendo arrastado para a direita |
| 2 | `running-left` | sendo arrastado para a esquerda |
| 3 | `waving` | toque rápido no personagem |
| 4 | `jumping` | comer o biscoito, brincar com a pelúcia |
| 5 | `failed` | soltar num lugar onde não cabe (ex.: castelinho cheio) |
| 6 | `waiting` | escova e almofada (por enquanto) |
| 7 | `running` | reservado (no pet, "trabalhando") |
| 8 | `review` | reservado |
| 9–10 | `look-row-9`, `look-row-10` | olhar, em 16 direções, para o objeto que está sendo arrastado |

## Ações que o formato de pet não tem (pedir como linhas extras, se a ferramenta deixar)

| Ação | Para quê | Personagens |
|---|---|---|
| `sleeping` | deitado na cama | todos |
| `eating` | comer de verdade, no lugar do pulo | animais |
| `holding` | segurar pelúcia, escova ou biscoito na mão | Catarina, Carol |
| `sitting` | sentada na sela da Lumi | Catarina, Carol |
| `brushed` | reação ao ser escovado | animais |

Se a ferramenta não aceitar linhas extras, essas ações podem vir numa segunda folha no mesmo formato
(ex.: `catarina_extra`), com o mesmo tamanho de quadro e a mesma linha do chão.

## Cuidados que apareceram na Nina v2

- **Resolução:** com 150 px de altura, a Nina fica um pouco menos nítida que os personagens 2D na tela do
  iPad. Por isso, quadro maior quando der.
- **Sobra de magenta:** há um rastro lilás meio transparente perto da pata no aceno (`waving`) e alguns
  pixels nas linhas de olhar. Pedir uma limpeza mais forte do recorte, ou conferir de perto antes de aprovar.
- **Lumi (cavalo):** é largo e o quadro do pet é alto e estreito. O cavalo ficaria pequeno dentro do quadro;
  pedir a Lumi com o quadro mais largo, ou de frente/três quartos, para aproveitar o espaço.
- **Caminhos do computador:** os arquivos `pet_request.json`, prompts e scripts guardam caminhos da pasta
  de usuário. O repositório é público: antes de subir, trocar esses caminhos (ou subir só a folha final e
  o `pet_request.json` limpo).

## Entrega e conferência

Cada personagem em `arte/animacoes/<nome>_pet/`, com no mínimo:

- `final/spritesheet-extended.png` — a folha;
- `outras/pet_request.json` — a descrição das linhas.

Conferência automática:

```bash
python3 ferramentas/verificar_folha.py arte/animacoes/<nome>_pet/final/spritesheet-extended.png \
    --pet arte/animacoes/<nome>_pet/outras/pet_request.json
```

Depois de aprovada, a folha entra no jogo com uma linha em `prototipo/scripts/main.gd`
(`_add_pet("<nome>", ...)`) e um arquivo `.json` ao lado da imagem, como em
`prototipo/assets/personagens/nina_pet.json`.

## Ordem de produção

1. **Bob** — o personagem mais usado nas brincadeiras.
2. **Catarina** — com `holding` e `sitting`, que mudam mais a experiência.
3. **Zoe** e **Leo**.
4. **Carol**.
5. **Lumi** — com o cuidado do quadro largo.
