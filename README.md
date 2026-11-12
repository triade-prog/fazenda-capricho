# Fazenda Capricho

Jogo de faz de conta com interação inspirada em Avatar World: a criança movimenta personagens e animais,
manipula objetos, explora ambientes e cria suas próprias histórias, sem missões obrigatórias.

- `docs/Fazenda_Capricho_GDD_Revisao4.docx` — documento de visão e design (GDD), Revisão 4.
- `docs/Fazenda_Capricho_Cenarios.docx` — lista e desenvolvimento dos 13 cenários, incluindo a Plantação com a proposta "fazendinha" inspirada no Mini Fazenda (mapa em `docs/mapa_cenarios.png`).
- `docs/PROMPT_personagens.md` — prompt pronto para a IA gerar os personagens no padrão da Nina, um de cada vez.
- `docs/padrao_geracao_personagens.md` — padrão para gerar os personagens como folhas de pet (a partir da Nina v2).
- `arte/animacoes/R01/` — entrega R01 de folhas de animação (espera/pulso) e marca.
- `arte/animacoes/nina_pet_v2/` — Nina gerada como pet do ChatGPT (estilo 3D): folha final, etapas, prompts e referências.
- `ferramentas/montar_pet.py` — monta a folha de pet a partir de tiras geradas em fundo magenta (ex.: ChatGPT); `ferramentas/pet_para_jogo.py` coloca a folha no jogo.
- `ferramentas/verificar_folha.py` — confere se uma folha de animação segue as regras do GDD.
- `prototipo/` — protótipo de interação P-0 em Godot 4.4 (quarto da Catarina), feito para iPad deitado. Veja `prototipo/README.md`.
- **Versão web para iPad:** <https://triade-prog.github.io/fazenda-capricho/> (GitHub Pages, servida da pasta `docs/`).
- `arte/conceito/colagem_cenarios/` — colagem "Novos Cenários do Jogo" e cada cenário recortado.
- `arte/conceito/cenarios_R01/` — estudos visuais dos cenários (só referência estética, não são peças do jogo).
- `arte/cenario/3d/` — arte 3D final do cenário e dos objetos (originais); as versões do jogo ficam em `prototipo/assets/cenario/`.
- `arte/cenario/estabulo/` — layout e prompts das peças do Estábulo florido + pasto (próximo cenário).
- `arte/cenario/plantacao/` — layout e prompts das peças da Plantação (horta, pomar, jardim, canteiro mágico).
- `arte/cenario/referencias_provisorias/` — cada elemento do quarto e cada objeto em PNG separado, com tamanhos o guia `GUIA.md` e os prompts prontos em `PROMPTS.md` para gerar a arte 3D.
- `arte/personagens/` — imagens oficiais dos personagens (versão final; prevalecem sobre o texto do GDD).

| Arquivo | Personagem |
|---|---|
| `catarina.png` | Catarina (filha) |
| `carol.png` | Carol (mãe) |
| `bob.png` | Bob, cachorro cowboy |
| `gatinha-rosa.png` | Zoe, gata rosa |
| `gatinha-azul.png` | Leo, gato azul |
| `cavalo-rosa.png` | Lumi, cavalo rosa |
| `nina.png` | Nina, husky astronauta |
