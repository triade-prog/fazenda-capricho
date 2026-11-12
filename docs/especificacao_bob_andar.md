# Especificação — folha `bob_andar` (R02)

Primeira folha de **ação** da Fazenda Capricho, pedida na "Direção de produção" da entrega R01.
Ela vai substituir o "Bob deslizando" do protótipo por um Bob que anda de verdade quando a criança o
arrasta pelo quarto no iPad.

## O que é

Ciclo de caminhada **no lugar** do Bob, de perfil, olhando para a **direita**. O jogo desloca o Bob
pelo quarto e espelha a folha quando ele anda para a esquerda; a folha não deve "andar" dentro do quadro.

## Formato (igual ao aprovado na R01)

| Item | Valor |
|---|---|
| Arquivo | `personagens/bob_andar_8f.png` + quadros soltos em `frames/bob_andar/` |
| Grade | 4 colunas × 2 linhas = 8 quadros, da esquerda para a direita, de cima para baixo |
| Quadro | 512 × 512 px, PNG RGBA, fundo transparente, sem legenda, moldura ou sombra |
| Ritmo | 12 quadros por segundo (**83 ms** por quadro), em loop |
| `manifest.json` | nova entrada `bob_andar`, no mesmo modelo da R01, com `frame_duration_ms: 83` |

## Escala e posição (o ponto que a R01 precisa corrigir)

| Item | Valor |
|---|---|
| Altura do Bob | **340 px** do chão ao topo do chapéu, em **todos** os quadros (tabela de escala do GDD: Bob = 0,57 × Catarina) |
| Linha do chão | **y = 480 px**, fixa: as patas que estão apoiadas tocam exatamente essa linha em todos os quadros |
| Centro | corpo centralizado em **x ≈ 256 px**; pode oscilar no máximo ±6 px |
| Margem | pelo menos 16 px de transparência entre o desenho e as bordas do quadro |

Na R01, a base do Bob subia e descia entre 473 e 478 px e a altura ficava em cerca de 314 px. No jogo,
isso faz o Bob parecer flutuar sobre a sombra.

## Movimento (8 quadros)

1. Contato: pata dianteira direita à frente, traseira esquerda atrás.
2. Baixa: corpo desce ~4 px (o **corpo**, não as patas apoiadas).
3. Passagem: patas se cruzam.
4. Alta: corpo sobe ~4 px.
5–8. Os mesmos quatro, com as patas do outro lado.

- Orelhas e rabo acompanham com um leve atraso (dão vida ao ciclo).
- Chapéu, coleira e roupa verde **iguais** à arte aprovada; o chapéu pode balançar até 3°.
- Expressão alegre, boca aberta como na arte original.

## Como a entrega é conferida

```bash
python3 ferramentas/verificar_folha.py personagens/bob_andar_8f.png --altura 340 --chao 480
```

A folha é aprovada quando o verificador responde **APROVADA**. Depois disso, ela entra no protótipo
e é testada no iPad (arrastar o Bob pelo quarto).

## Próximas folhas, em ordem de prioridade

1. `bob_andar` (esta)
2. `bob_comer` e `bob_abanar` (biscoito e carinho)
3. `catarina_andar` e `catarina_sentada` (para montar na Lumi; hoje ela aparece em pé na sela)
4. `lumi_andar` e `lumi_girar`
5. Partes separadas da Catarina (corpo, braços, cabeça) para segurar objetos e trocar roupas
