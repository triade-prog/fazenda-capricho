# Análise de design e frontend — 15/11/2026

Primeira análise do agente `analista-design-frontend` (versão do jogo: commit 8f706cb, estábulo no meio
do cenário). Versão completa, com tabelas por tema: <https://claude.ai/artifact/7Rxt1DGoMciMFg3dEhrFid>.
Inventário peça por peça: `analise_design/inventario.md`.

## Resumo

Bom: mapa a 1 ou 2 toques de qualquer cenário; botões fixos grandes (~96 pt) e iguais em todo lugar;
cadeado + cinza no que ainda não abriu.

Corrigir primeiro:
1. **Alta — memória:** `cenario.gd` guarda as imagens de todo cenário visitado (~670 MB de cenários + 130 MB
   de personagens + 87 MB do mapa na placa de vídeo). Soltar `_tex` ao sair do cenário e ligar a compressão
   de textura para celular. Confirmar no iPad visitando os 13 cenários.
2. **Alta — toque:** 42 coisas abaixo de 60 pt (abelha 27x23, borboleta 32x27, passarinho 40x31, xícara 47x50,
   tigelas 73x36, lanternas 47–55 pt de largura). Folga de pegar 14 → 30 em `toy.gd`; área mínima 70x70
   para `interativos`.
3. **Alta — botões:** ferradura e poltrona do Decorar a 10 pt uma da outra; poltrona some no quarto; X da
   lojinha em cima do contador.
4. **Alta — som:** o jogo não tem nenhum som; avisos são só texto ("Faltam ferradurinhas").
5. **Alta — estilo:** 3 cenários 3D (Quarto, Estábulo, Casa na árvore) e 9 planos + mapa plano; mapa não bate
   com as fachadas (Casa 2 andares x 1; Estábulo rosa x madeira) e chama a Plantação de "Horta".

Média: 17 peças de chão sem sombra; 10 famílias de peça com tamanhos diferentes (vaso 50x70 x 70x90, tigela de
água 80x40 x 160x70, porta 103x200 x 170x350); móveis de boneca na casa na árvore; chão vazio na Sala/Cozinha;
lojinha fecha ao tocar no fundo; personagens não viajam pelo mapa (decisão da Carol); service worker não
registrado (sem cache offline); `main.gd` com 1.476 linhas e véu de passagem repetido.
Baixa: banca da Plantação cortada embaixo (y até 940); cerca passando da borda em 8 cenários.
