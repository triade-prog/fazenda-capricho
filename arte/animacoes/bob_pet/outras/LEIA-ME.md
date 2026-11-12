# Bob — folha montada a partir de tiras

- idle: 6 quadros de /tmp/claude-0/-home-user-fazenda-capricho/22e56250-f7c7-597d-9a21-81e1312fb6c4/images/8.webp; altura original 334 px, escala 0.89x
- running-right: 8 quadros de /tmp/claude-0/-home-user-fazenda-capricho/22e56250-f7c7-597d-9a21-81e1312fb6c4/images/9.webp; altura original 242 px, escala 1.22x
- running-left: espelho de running-right

Ações que ainda faltam: waving, jumping, failed, waiting, running, review, look-row-9, look-row-10.

## Como acrescentar ações

1. Gere a tira com o prompt da ação em `prompts/` (ex.: `prompts/waving.md`, `prompts/jumping.md`), anexando
   `referencias/base.png`, `tiras/idle.webp` e o guia em `referencias/`.
2. Suba a imagem em `tiras/` com o nome da ação (`tiras/waving.png`, `tiras/jumping.png`).
3. A folha é remontada com todas as tiras:

       python3 ferramentas/montar_pet.py --nome bob --saida arte/animacoes/bob_pet \
           --linha idle:6:arte/animacoes/bob_pet/tiras/idle.webp \
           --linha running-right:8:arte/animacoes/bob_pet/tiras/running-right.webp \
           --espelhar running-left:running-right \
           --linha waving:4:arte/animacoes/bob_pet/tiras/waving.png \
           --linha jumping:5:arte/animacoes/bob_pet/tiras/jumping.png
       python3 ferramentas/pet_para_jogo.py arte/animacoes/bob_pet bob --sono 3
