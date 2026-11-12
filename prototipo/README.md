# Fazenda Capricho — Protótipo de interação P-0

Primeiro protótipo jogável, previsto na seção 8 do GDD (Revisão 2). Ele testa **apenas a base do
brinquedo**: arrastar, segurar, posicionar e combinar personagens e objetos no quarto da Catarina.

- **Motor:** Godot 4.4 (renderizador *Compatibility*, que roda em celular, computador e web).
- **Arte:** Catarina e Bob usam as imagens oficiais (`assets/personagens/`). O quarto e os objetos são
  **desenhos provisórios feitos por código**, para testar a interação antes de produzir a arte final.

## Como abrir

1. Instale o [Godot 4.4](https://godotengine.org/download) (versão padrão, não a .NET).
2. No Godot, clique em **Importar** e escolha o arquivo `prototipo/project.godot`.
3. Pressione **F5** (ou o botão ▶) para rodar.

O mouse funciona como um dedo: clicar = tocar, clicar e arrastar = pegar.

## O que dá para fazer

| Ação | Como |
|---|---|
| Pegar e mover qualquer coisa | Tocar e arrastar a Catarina, o Bob ou um objeto |
| Colocar um objeto na mão da Catarina | Soltar o objeto sobre ela (se a mão estiver ocupada, ela troca) |
| Pegar um objeto do chão com a Catarina | Soltar a Catarina sobre o objeto |
| Dar biscoito ao Bob | Soltar o biscoito no Bob, **ou** levar a Catarina segurando o biscoito até ele, **ou** levar o Bob até o biscoito |
| Escovar o Bob | Escova sobre o Bob (ou pela mão da Catarina) |
| Brincar com o Bob | Pelúcia sobre o Bob |
| Bob tirar um cochilo | Almofada sobre o Bob |
| Deitar no beliche | Soltar a Catarina (ou o Bob) em cima da cama; os dois cabem juntos |
| Subir a escada | Soltar a Catarina na escada: ela sobe e deita na cama |
| Descer o escorregador | Soltar a Catarina no alto do escorregador |
| Entrar no castelinho | Soltar a Catarina ou o Bob na porta do castelinho |
| Abrir/fechar a portinha roxa | Tocar na porta (com a porta fechada, quem está dentro fica escondido) |
| Ganhar biscoitos | Tocar no pote de biscoitos na mesinha (até 3 no quarto) |
| Reações rápidas | Tocar no Bob ("Au, au!" ou "Atchim!"), na Catarina, nos objetos |

Enquanto algo está sendo arrastado, o lugar ou o personagem que vai receber o soltar **brilha**,
para a criança saber o que vai acontecer antes de soltar.

## Onde mexer

| Arquivo | Papel |
|---|---|
| `dados/interacoes.json` | **Tabela de brincadeiras.** Combinações objeto + alvo e reações ao toque. Nova brincadeira = nova linha, sem programar. |
| `scripts/main.gd` | Entrada por toque/mouse, regras de soltar, lugares interativos e reações. |
| `scripts/toy.gd` | Tudo que pode ser pego: pose, mão, cabeça, toque generoso, animação de respirar. |
| `scripts/slot.gd` | Lugares de encaixe (cama, castelinho, escorregador, escada). |
| `scripts/room.gd`, `castle_front.gd`, `item_art.gd` | Desenhos provisórios do quarto, do castelinho e dos objetos. |

Para adicionar um personagem (ex.: Nina, Carol), basta uma chamada a `_add_character()` em
`main.gd` com a imagem, a altura e a posição da mão/cabeça, e linhas novas em `interacoes.json`.

## Roteiro de teste (critério de aceite do P-0)

- [ ] Arrastar Catarina e Bob pelo quarto com mouse **e** com toque (celular/tablet).
- [ ] Colocar pelúcia, escova e biscoito na mão da Catarina; trocar o que ela segura.
- [ ] Deitar a Catarina no beliche (com e sem o Bob junto).
- [ ] Descer o escorregador e subir a escada.
- [ ] Abrir e fechar a portinha roxa com alguém dentro do castelinho.
- [ ] Dar petisco ao Bob dos três jeitos (direto, pela mão da Catarina, levando o Bob).
- [ ] Observar uma criança brincando por 10 minutos, sem explicar nada: o que ela tenta fazer e não consegue?

## Limitações conhecidas (esperadas nesta fase)

- Personagens são imagens únicas: "abanar o rabo", "piscar" e "andar" são simulados com o corpo
  inteiro (balançar, pular, amassar). As animações reais dependem da arte em partes separadas (GDD, seção 7).
- Sem sons, sem salvamento e sem troca de ambiente.
- O protótipo ainda não foi exportado para Android/iOS/web; isso será feito depois da validação no computador.
