# Fazenda Capricho — PNGs individuais com transparência

Entrega: 380 itens do catálogo original + 1 extra identificado separadamente, distribuídos em 14 grupos.

## Como usar
1. Extraia o ZIP mantendo a estrutura de pastas.
2. Abra catalogo.html para buscar e visualizar os PNGs sobre fundo escuro quadriculado.
3. Em cada cenário, use objetos/ e interface/ para selecionar as peças. fundos/ contém as composições de fundo. previas/ contém referências prontas com personagens e não deve ser usada como objeto arrastável. extras/ está fora do catálogo original.
4. Consulte manifesto.json ou inventario.csv para dimensões, origem, recorte e observações de cada arquivo.

## Características dos arquivos
- PNG RGBA com transparência verdadeira, conferida nos 381 arquivos.
- Nomes sem acentos ou espaços; peças separadas por cenário e função.
- Margem transparente de 8 px nos recortes, sem nomes impressos nas peças.
- Principais pares de estado compartilham dimensões de tela e alinhamento pela base, sem redimensionar a arte original. Ainda é necessário conferir escala e encaixe visual na integração.
- As duas nuvens compartilham a mesma tela e o mesmo desenho de nuvem, nas mesmas coordenadas.
- O solo endurecido e as duas nuvens foram produzidos como correções complementares. A maioria das peças foi extraída das pranchas existentes com Python.
- As dimensões nativas dos recortes foram preservadas. Peças pequenas não foram ampliadas artificialmente. Há itens com uma dimensão menor que 64 px; objetos grandes no jogo poderão exigir nova geração em maior resolução.

## Limites da entrega
Os arquivos são sprites estáticos com visual 3D. As pranchas não contêm malhas 3D, animações, camadas escondidas atrás de objetos ou uma escala física comum. Nenhuma interação, hitbox ou posicionamento no jogo foi alterado. O pacote foi preparado para envio ao repositório GitHub. Não houve teste no iPad nesta etapa.

Algumas inconsistências visuais já estavam nas pranchas. Estão identificadas em PENDENCIAS.md e no inventário; os PNGs correspondentes foram preservados para revisão, sem afirmar que esses estados estejam corretos para produção. As bolhas mantêm o interior pintado da referência; o fundo ao redor está transparente.

## Organização dos lotes
- Lote 1 — pastas 01 a 06: quarto das meninas, sala, cozinha, sede, entrada e quarto da Carol.
- Lote 2 — pastas 07 a 10: estábulo, plantação, Pet Care e casa na árvore.
- Lote 3 — pastas 11 a 14: cabana, casinha, placas e mapa/botões.

Cada cenário inclui CONTATO.jpg para revisão rápida. O quadro_sementes_extra é uma peça que apareceu na geração da prancha e foi separado dos 380 IDs originais. Os nomes dos pacotes de sementes foram corrigidos conforme a espécie efetivamente desenhada.
