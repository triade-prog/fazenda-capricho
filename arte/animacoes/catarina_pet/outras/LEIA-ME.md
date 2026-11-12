# Catarina — folha montada a partir de tiras

- idle: 6 quadros de idle.png; altura original 628 px, escala 0.71x
- running-right: 8 quadros de running-right.png; altura original 425 px, escala 1.01x
- running-left: 8 quadros de running-left.png; altura original 429 px, escala 1.00x
- waving: 4 quadros de waving.png; altura original 684 px, escala 0.65x
- jumping: 5 quadros de jumping.png; altura original 578 px, escala 0.77x
- failed: 8 quadros de failed.png; altura original 534 px, escala 0.83x
- waiting: 6 quadros de waiting.png; altura original 582 px, escala 0.76x
- running: 6 quadros de running.png; altura original 634 px, escala 0.70x
- review: 6 quadros de review.png; altura original 606 px, escala 0.73x
- look-row-9: 8 quadros de look-row-9.png; altura original 605 px, escala 0.73x
- look-row-10: 8 quadros de look-row-10.png; altura original 562 px, escala 0.79x

Ações que ainda faltam: nenhuma.

Para montar de novo (da raiz do repositório):

```bash
python3 ferramentas/montar_pet.py --nome catarina \
    --saida arte/animacoes/catarina_pet \
    --resolucao 3 \
    --linha idle:6:arte/animacoes/catarina_pet/tiras/idle.png \
    --linha running-right:8:arte/animacoes/catarina_pet/tiras/running-right.png \
    --linha running-left:8:arte/animacoes/catarina_pet/tiras/running-left.png \
    --linha waving:4:arte/animacoes/catarina_pet/tiras/waving.png \
    --linha jumping:5:arte/animacoes/catarina_pet/tiras/jumping.png \
    --linha failed:8:arte/animacoes/catarina_pet/tiras/failed.png \
    --linha waiting:6:arte/animacoes/catarina_pet/tiras/waiting.png \
    --linha running:6:arte/animacoes/catarina_pet/tiras/running.png \
    --linha review:6:arte/animacoes/catarina_pet/tiras/review.png \
    --linha look-row-9:8:arte/animacoes/catarina_pet/tiras/look-row-9.png \
    --linha look-row-10:8:arte/animacoes/catarina_pet/tiras/look-row-10.png \
    --ajuste running-right:0.965 \
    --ajuste running-left:0.965
```

## Origem das tiras (entrega de 12/11/2026)

As tiras foram geradas uma por ação, com fundo transparente, e renomeadas para o padrão de pet:

| Arquivo em `tiras/` | Arquivo enviado |
|---|---|
| `idle.png` | Catarina em repouso tranquilo-1 (o 4º quadro, de olhos fechados, é o de dormir) |
| `running-right.png` | Catarina correndo para a direita-2 |
| `running-left.png` | Catarina correndo para a esquerda-4 |
| `waving.png` | Catarina acena em quatro poses-3 |
| `jumping.png` | Catarina em um salto divertido-1 |
| `jumping_alternativa.png` | Catarina em salto animado-2 (reserva, não usada) |
| `failed.png` | Catarina: surpresa e recuperação-3 |
| `waiting.png` | Catarina pede ajuda com carinho-2 |
| `running.png` | Catarina correndo em seis poses-1 |
| `review.png` | Catarina revisando em seis poses-2 |
| `look-row-9.png` | Catarina em oito direções-3 (de cima, pela direita, até quase embaixo) |
| `look-row-10.png` | Catarina em oito direções-1 (de baixo, pela esquerda, até quase em cima) |
| `../referencias/base.png` | Catarina, vaqueira mirim de rosa e roxo |

A folha 3x substitui a anterior (quadros de 192 × 208 ampliados), que ficava borrada no iPad. A escala da
corrida de lado foi reduzida em 3,5% (`--ajuste`) para a cabeça ficar do mesmo tamanho da pose parada.
Para levar ao jogo: `python3 ferramentas/pet_para_jogo.py arte/animacoes/catarina_pet catarina --colo 0.36 --sono 3`.
