# Prompt para gerar os personagens (copiar e colar na IA)

Use com uma IA que **acesse o repositório** e tenha a **ferramenta de pets do ChatGPT** (a mesma que gerou a
Nina v2, por exemplo o Codex com o plugin de pets). Cole o **prompt principal** e depois o **bloco do
personagem** da vez. **Um personagem por vez**, começando pelo Bob.

---

## Prompt principal

```
Você vai gerar os personagens do jogo infantil "Fazenda Capricho" (iPad, brincadeira de faz de conta
no estilo Avatar World), usando EXATAMENTE a mesma técnica da Nina v2, que já está pronta e aprovada.

REPOSITÓRIO: https://github.com/triade-prog/fazenda-capricho  (branch claude/brave-mendel-g0wd4g)

1) ANTES DE GERAR, LEIA E ANALISE:
   - arte/animacoes/nina_pet_v2/outras/pet_request.json  → formato da folha (grade, ações, ordem)
   - arte/animacoes/nina_pet_v2/prompts/                 → prompts usados em cada linha (base,
     rows/ e row-retries/); reutilize a mesma estrutura, trocando só a identidade do personagem
   - arte/animacoes/nina_pet_v2/final/spritesheet-extended.png → resultado esperado (estilo,
     enquadramento, tamanho do personagem no quadro, linha do chão)
   - arte/animacoes/nina_pet_v2/referencias/layout-guides/ → guias de espaçamento das linhas
   - docs/padrao_geracao_personagens.md                  → regras do projeto
   - arte/cenario/3d/                                    → cenário 3D já aprovado: os personagens
     precisam combinar com essas cores, materiais e luz
   - arte/personagens/<personagem>.png                   → imagem OFICIAL do personagem (identidade)
   Antes de gerar, me responda em poucas linhas o que entendeu do processo da Nina.

2) REGRAS DA FOLHA (iguais às da Nina, não mude nada):
   - estilo "3d-toy": brinquedo 3D estilizado, formas arredondadas, materiais simples, sem realismo;
   - grade 8 colunas × 11 linhas, quadros de 192 × 208 px, folha de 1536 × 2288 px;
   - as mesmas 11 ações, na mesma ordem e com o mesmo número de quadros:
     idle (6), running-right (8), running-left (8), waving (4), jumping (5), failed (8),
     waiting (6), running (6), review (6), look-row-9 (8), look-row-10 (8);
   - o personagem ocupa o quadro como a Nina (cerca de 150 px de altura). NÃO reduza nem aumente
     por causa da altura real: o jogo aplica a escala sozinho;
   - pés na mesma linha do chão (y ≈ 202) em todas as ações, menos no pulo e na corrida;
   - corpo centralizado no quadro (x ≈ 96) em todas as ações;
   - fundo transparente na folha final, sem nenhum resto de magenta/lilás do recorte (atenção
     especial ao aceno, onde a Nina ficou com um rastro lilás perto da pata);
   - sem sombra, sem cenário, sem texto, sem objetos extras.

3) IDENTIDADE: siga a imagem oficial e a descrição do bloco do personagem. Preserve roupa, cores,
   acessórios e proporções do rosto. Não invente acessórios.

4) ENTREGA NO REPOSITÓRIO (na branch acima), numa pasta nova arte/animacoes/<nome>_pet/ com:
   - final/spritesheet-extended.png      (a folha)
   - final/spritesheet-extended@2x.png   (A MESMA folha montada a partir das imagens grandes, ANTES de
     reduzir: quadros de 384 × 416 px, folha de 3072 × 4576 px, personagem com ~300 px de altura,
     mesma grade, mesma ordem e mesma linha do chão proporcional. É ela que fica nítida no iPad.)
   - outras/pet_request.json             (mesmo formato do da Nina)
   - prompts/                            (os prompts usados)
   ALTERNATIVA MAIS SIMPLES (a que deu melhor resultado, na Catarina): suba só as TIRAS grandes, uma
   imagem por ação com fundo transparente e os quadros lado a lado, em arte/animacoes/<nome>_pet/tiras/
   (idle.png, running-right.png, running-left.png, waving.png, jumping.png, failed.png, waiting.png,
   running.png, review.png, look-row-9.png, look-row-10.png) e a pose base em referencias/base.png.
   A folha em alta resolução é montada depois com ferramentas/montar_pet.py --resolucao 3.
   NÃO inclua as etapas intermediárias com fundo magenta e NÃO deixe caminhos do computador
   (como /Users/...) em nenhum arquivo: o repositório é público.
   Mensagem do commit: "Personagem <Nome>: folha de pet 3D (padrão Nina v2)".

5) CONFERÊNCIA OBRIGATÓRIA antes de subir (das duas folhas):
   python3 ferramentas/verificar_folha.py arte/animacoes/<nome>_pet/final/spritesheet-extended.png \
       --pet arte/animacoes/<nome>_pet/outras/pet_request.json
   Só suba se o resultado for APROVADA. Avisos de "sobra do fundo magenta" acima de 10 pixels numa
   linha: refaça o recorte daquela linha. Me mostre o resultado da conferência.

6) Gere SÓ o personagem pedido no bloco abaixo e pare. Eu coloco no jogo e aprovo no iPad antes
   do próximo.
```

---

## Blocos dos personagens (colar depois do prompt principal, um de cada vez)

### 1. Bob

```
PERSONAGEM: Bob — pasta arte/animacoes/bob_pet/ — imagem oficial arte/personagens/bob.png
Cachorro de pelo dourado e orelhas longas e caídas; chapéu de cowboy marrom com ferradura dourada;
coleira marrom grande com medalha de coração; roupa verde de fazenda (camisa e short verdes);
SEM chifres. Fica de lado, em quatro patas, como na imagem oficial.
Personalidade: brincalhão e bagunceiro; late "au, au" e espirra "atchim".
No "failed" ele abaixa as orelhas; no "waving" levanta uma pata da frente.
```

### 2. Catarina

```
PERSONAGEM: Catarina — pasta arte/animacoes/catarina_pet/ — imagem oficial arte/personagens/catarina.png
Menina (filha), de pé, de frente. Óculos rosa; cabelo castanho muito comprido em duas tranças com
laços rosa; chapéu de cowboy bege com fita rosa; camisa xadrez rosa, lenço rosa e colete roxo com
estrela dourada; calça roxa; botas marrons de cowboy.
Personalidade: alegre, curiosa, carinhosa com os bichos.
No "waving" acena com a mão; no "running" corre como criança; no "failed" faz carinha de "ops".
```

### 3. Zoe

```
PERSONAGEM: Zoe — pasta arte/animacoes/zoe_pet/ — imagem oficial arte/personagens/gatinha-rosa.png
Gata rosa fofinha, sentada; flor branca na orelha; bandana xadrez lilás com florzinha; coração claro
no peito. Personalidade: quietinha e tranquila; movimentos suaves e delicados.
```

### 4. Leo

```
PERSONAGEM: Leo — pasta arte/animacoes/leo_pet/ — imagem oficial arte/personagens/gatinha-azul.png
Gato azul com listras azul-escuras; chapéu de cowboy pequeno; bandana roxa com estrela.
Personalidade: bagunceiro e brincalhão, pede comida dizendo "dá, dá"; movimentos rápidos e animados.
```

### 5. Carol

```
PERSONAGEM: Carol — pasta arte/animacoes/carol_pet/ — imagem oficial arte/personagens/carol.png
Mulher adulta (mãe), de pé, de frente. Cabelo castanho-escuro liso na altura dos ombros, SEM chapéu;
camisa rosa de botões com mangas dobradas; cinto marrom com fivela dourada; calça jeans azul; botas
marrons. Personalidade: calma, carinhosa, sorridente.
```

### 6. Lumi (por último)

```
PERSONAGEM: Lumi — pasta arte/animacoes/lumi_pet/ — imagem oficial arte/personagens/cavalo-rosa.png
Cavalo (pônei) rosa, de lado; crina e cauda rosa-escuro com mechas lilás; flores brancas na crina;
laço lilás na cauda; sela lilás com arco-íris e estribo dourado. Personalidade: calmo e amistoso;
relincha "ehêhêhê" e gosta de girar.
ATENÇÃO: o cavalo é largo e o quadro é alto e estreito. Antes de gerar, me diga se a ferramenta
permite um quadro mais largo para ele; se não permitir, gere de lado ocupando a largura do quadro,
e me mostre a linha "idle" antes de gerar o resto.
```

---

## Antes de começar: uma decisão

Na imagem conceitual do quarto 3D, a Nina aparece com **colete** laranja. Na folha que está no jogo,
ela usa o **traje de astronauta completo**. Os outros personagens devem seguir o mesmo nível de
detalhe da folha da Nina, que é a referência técnica. Se você preferir a Nina de colete, gere uma
**Nina v3** antes do Bob, com o mesmo bloco abaixo:

```
PERSONAGEM: Nina — pasta arte/animacoes/nina_pet_v3/ — imagem oficial arte/personagens/nina.png
Husky cinza e branca, olhos castanhos, sentada; colete laranja de astronauta com detalhes cinza
(como na imagem conceitual do quarto). Personalidade: curiosa, companheira e engraçada.
```
