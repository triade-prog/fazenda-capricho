class_name Decoracao
extends CanvasLayer
## Modo Decorar: a criança arruma os móveis e enfeites de cada cenário do jeito dela.
##
##   - o botão da poltrona (embaixo da ferradura) liga o modo; as peças que mudam de lugar ganham
##     um contorno tracejado e os personagens ficam quietos (o toque é só das peças);
##   - tocar e arrastar uma peça leva a peça para qualquer lugar do cenário; o que está em cima dela
##     vai junto (vaso na mesa, fogo na lareira, quem está sentado no sofá, comidinha na mesa);
##   - arrastar num espaço vazio rola o cenário, e levar a peça até a borda da tela também rola;
##   - o certinho verde sai do modo. A arrumação fica guardada no aparelho (user://decoracao.json)
##     a cada peça solta e volta igual quando o jogo abre de novo.
## O quarto da Catarina é desenhado por código (room.gd) e por isso ainda não entra no modo Decorar.
##
## Baú (15/11/2026): no modo Decorar aparecem o baú e a loja, embaixo. Arrastar uma peça até o baú
## (ou tocar nela e depois no balãozinho do baú) guarda a peça; abrir o baú e arrastar um cartão para
## o cenário coloca de novo. Um baú só para a fazenda inteira; o mesmo item pode estar várias vezes
## (o cartão mostra quantos). O que não combina com o cenário aberto (de casa no quintal, de quintal
## em casa) fica apagadinho. Itens de chão só param no chão ou em cima de outra peça; de parede, só na
## parede. Regras das peças em dados/moveis.json; ficha dos itens da loja em dados/itens.json.

static var arquivo := "user://decoracao.json"

const BOTAO_TAM := Vector2(140, 140)
const BOTAO_VAO := 40.0            # espaço entre um botão e o outro na coluna da esquerda (~27 pontos no iPad)
const BOTAO_POS := Vector2(18, 18 + 140 + BOTAO_VAO)   # embaixo da ferradura do mapa (18, 18)
const ALTURA := 900.0              # altura dos cenários (main.H)
const BORDA := 110.0               # faixa da borda da tela que rola o cenário (BORDA)
const ROLAGEM := 650.0             # velocidade dessa rolagem (ROLAGEM)

var main: Node2D
var botao: TextureButton
var ligado := false
var _tex_decorar: Texture2D
var _tex_pronto: Texture2D
var _cen: Cenario = null           # cenário da peça que está sendo levada
var _grupo: Array = []             # a peça tocada e o que está em cima dela
var _pega := Vector2.ZERO          # onde o dedo pegou, em relação ao canto da peça
var _antes := Vector2.ZERO         # posição da peça ao ser pega (para a balançadinha ao soltar)
var _novo := false                 # a peça levada acabou de sair do baú
var _gaveta_era := false           # a gaveta estava aberta antes de pegar a peça (some enquanto leva)

# baú
var bau := {}                      # item -> quantos estão guardados
var uid_prox := 1                  # próximo número fixo de peça nova
var botao_bau: TextureButton
var botao_loja: TextureButton
var selo_loja: TextureRect
var gaveta: Control                # cartões do baú, embaixo da tela
var seta_esq: TextureButton
var seta_dir: TextureButton
var balao: TextureButton           # balãozinho "guardar no baú" em cima de uma peça tocada
var _balao_i := -1
var _balao_t := 0.0
var _pagina := 0
var _cartas: Array = []            # [item, Rect2 na tela da gaveta, pode colocar]
var _tex_bau: Texture2D
var _tex_bau_aberto: Texture2D

const CARTA := Vector2(150, 160)
const GAVETA_ALT := 196.0


func _init() -> void:
	layer = 6


func _ready() -> void:
	_tex_decorar = load("res://assets/decorar/botao_decorar.png")
	_tex_pronto = load("res://assets/decorar/botao_pronto.png")
	botao = TextureButton.new()
	botao.name = "BotaoDecorar"
	botao.texture_normal = _tex_decorar
	botao.ignore_texture_size = true
	botao.stretch_mode = TextureButton.STRETCH_SCALE
	botao.custom_minimum_size = BOTAO_TAM
	botao.size = BOTAO_TAM
	botao.position = BOTAO_POS
	botao.pivot_offset = BOTAO_TAM / 2.0
	botao.button_down.connect(func() -> void: botao.scale = Vector2(0.92, 0.92))
	botao.button_up.connect(func() -> void: botao.scale = Vector2.ONE)
	botao.pressed.connect(alternar)
	add_child(botao)
	_tex_bau = Itens.icone("botao_bau")
	_tex_bau_aberto = Itens.icone("botao_bau_aberto")
	botao_loja = _botao(load("res://assets/loja/botao_loja.png"), BOTAO_TAM, func() -> void: abrir_loja())
	selo_loja = TextureRect.new()
	selo_loja.texture = Itens.icone("selo_novo")
	selo_loja.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	selo_loja.size = Vector2(48, 48)
	selo_loja.position = Vector2(BOTAO_TAM.x - 44, -4)
	selo_loja.mouse_filter = Control.MOUSE_FILTER_IGNORE
	selo_loja.visible = false
	botao_loja.add_child(selo_loja)
	gaveta = Control.new()
	gaveta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	gaveta.visible = false
	gaveta.draw.connect(_desenha_gaveta)
	add_child(gaveta)
	botao_bau = _botao(_tex_bau, BOTAO_TAM, func() -> void: abrir_bau(not gaveta.visible))
	seta_esq = _botao(Itens.icone("seta_esq"), Vector2(72, 72), func() -> void: _virar(-1))
	seta_dir = _botao(Itens.icone("seta_dir"), Vector2(72, 72), func() -> void: _virar(1))
	balao = _botao(Itens.icone("balao_guardar"), Vector2(100, 110), func() -> void: _guardar_balao())
	for b in [botao_bau, seta_esq, seta_dir, balao]:
		b.visible = false


func _botao(tex: Texture2D, tam: Vector2, acao: Callable) -> TextureButton:
	var b := TextureButton.new()
	b.texture_normal = tex
	b.ignore_texture_size = true
	b.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	b.size = tam
	b.pivot_offset = tam / 2.0
	b.button_down.connect(func() -> void:
		b.scale = Vector2(0.92, 0.92)
		Sons.tocar("toque"))
	b.button_up.connect(func() -> void: b.scale = Vector2.ONE)
	b.pressed.connect(acao)
	add_child(b)
	return b


## O toque foi num botão desta camada (decorar, loja, baú, setas, balão, gaveta)?
func ui_em(sp: Vector2) -> bool:
	for b in [botao, botao_loja, botao_bau, seta_esq, seta_dir, balao]:
		if b.visible and (b as Control).get_global_rect().has_point(sp):
			return true
	return false


## Ponto da tela em cima da gaveta aberta ou do botão do baú (soltar ali guarda a peça).
func sobre_bau(sp: Vector2) -> bool:
	return botao_bau.visible and botao_bau.get_global_rect().grow(30.0).has_point(sp)


## Liga cada cenário ao modo Decorar e põe as peças onde a criança deixou da última vez.
func preparar(m: Node2D) -> void:
	main = m
	for id in main.cenarios:
		var c = main.cenarios[id]
		if c is Cenario:
			(c as Cenario).preparar_deco()
			(c as Cenario).peca_movida.connect(_peca_movida.bind(c))
	_carregar()
	_migrar_enfeites()


func pode() -> bool:
	return main != null and main.cena != "quarto" and main.cenarios.get(main.cena) is Cenario


func alternar() -> void:
	if not ligado and not pode():
		# quarto da Catarina: ainda não dá para decorar; o botão balança dizendo "aqui não"
		Sons.tocar("nao")
		var tw := botao.create_tween()
		for k in 4:
			tw.tween_property(botao, "rotation", 0.18 if k % 2 == 0 else -0.18, 0.06)
		tw.tween_property(botao, "rotation", 0.0, 0.06)
		return
	Sons.tocar("toque")
	if ligado:
		desligar()
	else:
		ligar()


func ligar() -> void:
	if not pode():
		return
	ligado = true
	botao.texture_normal = _tex_pronto
	botao_bau.visible = true
	_cenario().decorando = true
	_cenario().queue_redraw()
	main._log("modo Decorar ligado")


func desligar() -> void:
	if _cen:
		soltar()
	ligado = false
	botao.texture_normal = _tex_decorar
	abrir_bau(false)
	_esconder_balao()
	botao_bau.visible = false
	for id in main.cenarios:
		if main.cenarios[id] is Cenario and (main.cenarios[id] as Cenario).decorando:
			(main.cenarios[id] as Cenario).decorando = false
			(main.cenarios[id] as Cenario).queue_redraw()
	_salvar()
	main._log("modo Decorar desligado")


func arrastando() -> bool:
	return _cen != null


func _cenario() -> Cenario:
	return main.cenarios[main.cena] as Cenario


# ---------------------------------------------------------------- tocar, levar e soltar

## Toque no cenário com o modo ligado: true se pegou uma peça.
func pegar(p: Vector2) -> bool:
	var c := _cenario()
	var i := c.peca_deco_em(p)
	_esconder_balao()
	if i < 0:
		return false
	_novo = false
	_esconder_gaveta()
	_cen = c
	_grupo = [i]
	var k := 0
	while k < _grupo.size():   # o que está em cima do que está em cima também vai
		for j in c.carga(int(_grupo[k])):
			if not j in _grupo:
				_grupo.append(j)
		k += 1
	var r := c._rect_peca(i)
	_pega = p - r.position
	_antes = r.position
	c.deco_ativa = i
	c.queue_redraw()
	return true


## O dedo andou: a peça (e o que está nela) vai junto, sem sair do cenário.
func levar(p: Vector2) -> void:
	if _cen == null:
		return
	var i := int(_grupo[0])
	var r := _cen._rect_peca(i)
	var alvo := p - _pega
	alvo.x = clampf(alvo.x, 0.0, _cen.largura - r.size.x)
	alvo.y = clampf(alvo.y, 20.0, ALTURA - r.size.y)
	_mover_grupo(_cen, _grupo, alvo - r.position)


## Enquanto a criança leva uma peça, a gaveta do baú sai da frente (o chão fica livre);
## para guardar, é só levar até o botão do baú. Ao soltar, ela volta.
func _esconder_gaveta() -> void:
	_gaveta_era = gaveta.visible
	gaveta.visible = false


func soltar() -> void:
	if _cen == null:
		return
	var c := _cen
	var i := int(_grupo[0])
	var r := c._rect_peca(i)
	# a gaveta volta, menos quando um item novo acabou de ir para o cenário (assim ele fica à vista
	# e dá para mexer; o botão do baú abre de novo)
	if _gaveta_era and not (_novo and _lugar_certo(c, i) and not sobre_bau(main.last_screen)):
		gaveta.visible = true
		gaveta.queue_redraw()
	_gaveta_era = false
	c.deco_ativa = -1
	c.queue_redraw()
	# solto em cima do baú: vai para o baú
	if sobre_bau(main.last_screen) and c.pode_guardar(i):
		_cen = null
		guardar(c, _grupo)
		_grupo = []
		return
	# lugar que não dá (item de chão no ar, quadro no chão): volta sozinho, sem bronca
	if not _lugar_certo(c, i):
		if _novo:
			_cen = null
			guardar(c, [i], false)
			main._log("o item voltou para o baú (lugar que não dá)")
		else:
			_mover_grupo(c, _grupo, _antes - r.position)
			c.sacudir(i)
			_cen = null
			main._log("a peça voltou (lugar que não dá)")
		_grupo = []
		return
	if _novo or r.position.distance_to(_antes) > 2.0:
		c.reordenar(_grupo)
		main._sparkle(Vector2(r.get_center().x, r.end.y - 10.0), 4)
		main._log("decorou: %s foi para (%d, %d)" % [c.chave_peca(i), r.position.x, r.position.y])
		_cen = null
		_salvar()
	else:
		c.sacudir(i)  # só tocou: dá uma balançadinha
		_cen = null
		if c.pode_guardar(i):
			_mostrar_balao(c, i)
	_novo = false
	_grupo = []


## Item de chão no chão (ou em cima de outra peça); item de parede na parede. Só vale para os itens
## do baú e as peças de parede: as outras peças continuam podendo ir para onde já iam.
func _lugar_certo(c: Cenario, i: int) -> bool:
	var parede := c.eh_parede(i)
	if not parede and not c.itens.has(i):
		return true
	var pe := c._rect_peca(i).end.y
	var chao := Itens.chao(c.id)
	if parede:
		return pe <= chao + 10.0
	if pe >= chao - 10.0:
		return true
	# em cima de outra peça só vale se ela tem tampo (mesa, prateleira, banca): copa de árvore não
	var ap := c._achar_apoio(i, _grupo)
	return ap >= 0 and not c.superficies_da(ap).is_empty()


## Enquanto leva uma peça perto da borda da tela, o cenário rola junto (como ao arrastar um personagem).
func _process(delta: float) -> void:
	if main == null:
		return
	# sempre no mesmo lugar (no quarto também, onde só balança): botão que some parece quebrado
	var loja_aberta: bool = main.fazenda != null and main.fazenda.loja != null and main.fazenda.loja.aberta()
	botao.visible = not (main.mapa and main.mapa.aberto()) and not loja_aberta
	if main.mapa and main.mapa.botao:
		main.mapa.botao.visible = not loja_aberta and not main.mapa.aberto()  # loja aberta: só o X dela
	_arruma_ui()
	if balao.visible:
		_balao_t -= delta
		if _balao_t <= 0.0 or _balao_i < 0:
			_esconder_balao()
		else:
			_pos_balao()
	if ligado and not pode():
		desligar()
	if ligado and pode() and not _cenario().decorando:
		# mudou de cenário com o modo ligado (pelo mapa): o contorno passa para o cenário novo
		for id in main.cenarios:
			if main.cenarios[id] is Cenario:
				(main.cenarios[id] as Cenario).decorando = id == main.cena
				(main.cenarios[id] as Cenario).queue_redraw()
	if _cen == null:
		return
	var vis: Vector2 = main.get_viewport().get_visible_rect().size
	var dir := 0.0
	if main.last_screen.x < BORDA:
		dir = -1.0
	elif main.last_screen.x > vis.x - BORDA:
		dir = 1.0
	if dir != 0.0:
		var antes: float = main.cam.position.x
		main.camera_to(main.cam.position.x + dir * ROLAGEM * delta)
		if main.cam.position.x != antes:
			levar(main.screen_to_world(main.last_screen))


## Leva as peças do grupo d pixels, com as coisas soltas que estão apoiadas nelas.
func _mover_grupo(c: Cenario, grupo: Array, d: Vector2) -> void:
	if d.length() < 0.01:
		return
	var juntos := _apoiados(c, grupo)
	for i in grupo:
		c.deslocar(int(i), d)
	for t in juntos:
		(t as Toy).global_position += d


## Objetos e personagens soltos (fora de lugar e de mão) em pé numa superfície das peças do grupo,
## e o que está guardado dentro delas.
func _apoiados(c: Cenario, grupo: Array) -> Array:
	var sups: Array[Vector3] = []
	var guardam := []                  # móveis que guardam coisas dentro (cesto, gaveta, geladeira)
	for i in grupo:
		sups.append_array(c.superficies_da(int(i)))
		var nome := str(c.pecas[int(i)][0])
		if nome.begins_with("@"):
			guardam.append(nome.substr(1))
	var r := []
	for t in main.toys:
		var toy := t as Toy
		if toy.cena != c.id or toy.slot or toy.holder or toy.mount or toy.lifted:
			continue
		if str(toy.get_meta("guardado", "")) in guardam:
			r.append(toy)
			continue
		var pos := toy.global_position
		for s in sups:
			if absf(pos.y - s.z) < 6.0 and pos.x >= s.x - 8.0 and pos.x <= s.y + 8.0:
				r.append(toy)
				break
	return r


## Uma peça mudou de lugar: os lugares de sentar/deitar dela (e quem está neles) vão junto.
func _peca_movida(i: int, d: Vector2, c: Cenario) -> void:
	if main.fazenda and c.id == Fazendinha.CENA:
		main.fazenda.queue_redraw()  # cadeados e frutas das árvores acompanham a árvore
	var ids := c.lugares_da(i)
	for s in main.slots:
		var sl := s as Slot
		if sl.cena != c.id:
			continue
		if int(sl.get_meta("movel", -1)) != i and not sl.id in ids:
			continue
		sl.area.position += d
		for k in sl.spots.size():
			sl.spots[k] += d
			if sl.occupants[k]:
				(sl.occupants[k] as Toy).global_position += d
		if sl.spots.size() > 0:
			sl.depth = Toy.depth_for(sl.spots[0].y)
		sl.queue_redraw()


# ---------------------------------------------------------------- guardar no aparelho

func _salvar() -> void:
	var tudo := {}
	var ordens := {}
	var apoios := {}
	for id in main.cenarios:
		if main.cenarios[id] is Cenario:
			var a := (main.cenarios[id] as Cenario).arrumacao()
			if not a.is_empty():
				tudo[id] = a
			var o := (main.cenarios[id] as Cenario).ordem_guardar()
			if not o.is_empty():
				ordens[id] = o
			if not o.is_empty() or not a.is_empty():
				apoios[id] = (main.cenarios[id] as Cenario).apoios_guardar()
	var guardadas := {}
	var novos := {}
	for id in main.cenarios:
		if main.cenarios[id] is Cenario:
			var c := main.cenarios[id] as Cenario
			var g := c.guardadas_guardar()
			if not g.is_empty():
				guardadas[id] = g
			var n := c.novos_guardar()
			if not n.is_empty():
				novos[id] = n
			if not g.is_empty() or not n.is_empty():
				apoios[id] = c.apoios_guardar()
				if not ordens.has(id):
					ordens[id] = c.ordem_guardar()
	var f := FileAccess.open(arquivo, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify({"versao": 3, "cenarios": tudo, "ordens": ordens, "apoios": apoios,
			"bau": bau, "uid": uid_prox, "guardadas": guardadas, "novos": novos}))


func _carregar() -> void:
	if not FileAccess.file_exists(arquivo):
		return
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(arquivo))
	if typeof(d) != TYPE_DICTIONARY:
		return
	# versão 3: o baú, os itens novos de cada cenário e as peças originais guardadas
	bau.clear()
	var b: Dictionary = (d as Dictionary).get("bau", {})
	for item in b:
		if Itens.existe(str(item)) and int(b[item]) > 0:
			bau[str(item)] = int(b[item])
	uid_prox = maxi(1, int((d as Dictionary).get("uid", 1)))
	var novos: Dictionary = (d as Dictionary).get("novos", {})
	for id in novos:
		if not main.cenarios.get(id) is Cenario:
			continue
		for n in novos[id]:
			if n is Array and n.size() == 4 and Itens.existe(str(n[1])):
				var c := main.cenarios[id] as Cenario
				var i := c.colocar_item(str(n[1]), Vector2(float(n[2]), float(n[3])), str(n[0]))
				_criar_lugar(c, i)
	var gs: Dictionary = (d as Dictionary).get("guardadas", {})
	for id in gs:
		if main.cenarios.get(id) is Cenario:
			var c := main.cenarios[id] as Cenario
			for ch in gs[id]:
				var i := c.indice_da_chave(str(ch))
				if i >= 0 and c.pode_guardar(i):
					c.guardar_peca(i)
	var cens: Dictionary = (d as Dictionary).get("cenarios", {})
	for id in cens:
		if not main.cenarios.get(id) is Cenario:
			continue
		var c := main.cenarios[id] as Cenario
		for chave in cens[id]:
			var i := c.indice_da_chave(str(chave))
			var v: Array = cens[id][chave]
			if i >= 0 and c.pode_decorar(i) and v.size() == 2:
				_mover_grupo(c, [i], Vector2(float(v[0]), float(v[1])))
	var ordens: Dictionary = (d as Dictionary).get("ordens", {})
	for id in ordens:
		if main.cenarios.get(id) is Cenario:
			(main.cenarios[id] as Cenario).usar_ordem(ordens[id])
	var apoios: Dictionary = (d as Dictionary).get("apoios", {})
	for id in apoios:
		if main.cenarios.get(id) is Cenario:
			(main.cenarios[id] as Cenario).usar_apoios(apoios[id])


# ---------------------------------------------------------------- baú

func _cartas_ordem() -> Array:
	var aqui := []
	var outros := []
	var c := _cenario() if pode() else null
	var itens := bau.keys()
	itens.sort()
	for item in itens:
		if c and Itens.combina(str(item), c.id):
			aqui.append(item)
		else:
			outros.append(item)
	return aqui + outros


func _por_pagina() -> int:
	return maxi(1, int((gaveta.size.x - 2.0 * 96.0) / (CARTA.x + 14.0)))


## Posição dos botões (dependem do tamanho da tela).
func _arruma_ui() -> void:
	var vis: Vector2 = main.get_viewport().get_visible_rect().size
	var mapa_aberto: bool = main.mapa != null and main.mapa.aberto()
	botao_loja.visible = not mapa_aberto and not (main.fazenda and main.fazenda.loja and main.fazenda.loja.aberta())
	botao_loja.position = BOTAO_POS + Vector2(0, BOTAO_TAM.y + BOTAO_VAO)
	selo_loja.visible = main.fazenda != null and main.fazenda.tem_novidade()
	botao_bau.visible = ligado and not mapa_aberto
	botao_bau.position = Vector2(BOTAO_POS.x, vis.y - BOTAO_TAM.y - 18.0)
	botao_bau.texture_normal = _tex_bau_aberto if gaveta.visible else _tex_bau
	gaveta.visible = gaveta.visible and ligado and not mapa_aberto
	gaveta.position = Vector2(BOTAO_POS.x + BOTAO_TAM.x + 14.0, vis.y - GAVETA_ALT - 14.0)
	gaveta.size = Vector2(vis.x - gaveta.position.x - 18.0, GAVETA_ALT)
	var paginas := maxi(1, int(ceil(float(bau.size()) / _por_pagina())))
	_pagina = clampi(_pagina, 0, paginas - 1)
	seta_esq.visible = gaveta.visible and _pagina > 0
	seta_dir.visible = gaveta.visible and _pagina < paginas - 1
	seta_esq.position = gaveta.position + Vector2(12, (GAVETA_ALT - 72.0) / 2.0)
	seta_dir.position = gaveta.position + Vector2(gaveta.size.x - 84.0, (GAVETA_ALT - 72.0) / 2.0)


func abrir_bau(sim: bool) -> void:
	if sim and not ligado:
		ligar()
	gaveta.visible = sim and ligado
	_pagina = 0
	gaveta.queue_redraw()


func abrir_loja() -> void:
	if main.fazenda and main.fazenda.loja:
		_esconder_balao()
		main.fazenda.loja.abrir()


func _virar(d: int) -> void:
	_pagina += d
	_arruma_ui()
	gaveta.queue_redraw()


## Quantos itens novos ainda cabem no cenário aberto.
func _cabe() -> bool:
	return _cenario().novos_aqui() < int(Itens.loja()["limite"])


func _desenha_gaveta() -> void:
	var caixa := StyleBoxFlat.new()
	caixa.bg_color = Color("#fff7ea")
	caixa.border_color = Color("#5b3a4f")
	caixa.set_border_width_all(5)
	caixa.set_corner_radius_all(30)
	gaveta.draw_style_box(caixa, Rect2(Vector2.ZERO, gaveta.size))
	_cartas.clear()
	var lista := _cartas_ordem()
	var n := _por_pagina()
	var x := 96.0
	var fonte := ThemeDB.fallback_font
	if lista.is_empty():
		var t := Itens.icone("botao_bau_aberto")
		if t:
			gaveta.draw_texture_rect(t, Rect2(Vector2(gaveta.size.x / 2.0 - 60.0, 30.0), Vector2(120, 120)), false, Color(1, 1, 1, 0.35))
		return
	var cabe := pode() and _cabe()
	for k in range(_pagina * n, mini(lista.size(), (_pagina + 1) * n)):
		var item := str(lista[k])
		var r := Rect2(Vector2(x, (GAVETA_ALT - CARTA.y) / 2.0), CARTA)
		var ok := pode() and Itens.combina(item, _cenario().id) and cabe
		_cartas.append([item, r, ok])
		var cor := Color.WHITE if ok else Color(1, 1, 1, 0.35)
		var fundo := StyleBoxFlat.new()
		fundo.bg_color = Color("#ffe3ef") if ok else Color("#eee8ec")
		fundo.border_color = Color("#5b3a4f")
		fundo.set_border_width_all(4)
		fundo.set_corner_radius_all(22)
		gaveta.draw_style_box(fundo, r)
		var t := Itens.textura(item)
		if t:
			var area := r.grow(-16.0)
			area.size.y -= 18.0
			var e := minf(area.size.x / t.get_width(), area.size.y / t.get_height())
			var tam := Vector2(t.get_width(), t.get_height()) * e
			gaveta.draw_texture_rect(t, Rect2(area.get_center() - tam / 2.0, tam), false, cor)
		if not ok and pode() and not Itens.combina(item, _cenario().id):
			# sinal pequeno de onde ele vai: casa (poltrona) ou quintal (árvore)
			var onde := Itens.icone("aba_casa" if str(Itens.ficha(item).get("onde", "")) == "dentro" else "aba_quintal")
			if onde:
				gaveta.draw_texture_rect(onde, Rect2(r.position + Vector2(8, CARTA.y - 52.0), Vector2(44, 44)), false)
		var q := int(bau[item])
		if q > 1:
			gaveta.draw_circle(r.position + Vector2(CARTA.x - 24.0, 24.0), 22.0, Color("#ff6fae"))
			gaveta.draw_string(fonte, r.position + Vector2(CARTA.x - 42.0, 35.0), "x%d" % q, HORIZONTAL_ALIGNMENT_CENTER, 36.0, 26, Color.WHITE)
		x += CARTA.x + 14.0


## Cartão do baú no ponto da tela: o item (ou "x" se o cartão está apagado; "" se não é cartão).
func carta_em(sp: Vector2) -> String:
	if not gaveta.visible:
		return ""
	var lp := sp - gaveta.position
	for c in _cartas:
		if (c[1] as Rect2).has_point(lp):
			return str(c[0]) if c[2] else "x"
	return "x" if Rect2(Vector2.ZERO, gaveta.size).has_point(lp) else ""


## Tira um item do baú e põe no cenário, já preso no dedo (ponto p do mundo).
func colocar(item: String, p: Vector2) -> bool:
	if not bau.has(item) or not pode() or not Itens.combina(item, _cenario().id) or not _cabe():
		return false
	var c := _cenario()
	var tam := Itens.tamanho(item)
	var uid := "n%d" % uid_prox
	uid_prox += 1
	var i := c.colocar_item(item, Vector2(p.x - tam.x / 2.0, p.y + tam.y / 2.0), uid)
	bau[item] = int(bau[item]) - 1
	if int(bau[item]) <= 0:
		bau.erase(item)
	_criar_lugar(c, i)
	_esconder_balao()
	_esconder_gaveta()
	_cen = c
	_grupo = [i]
	var r := c._rect_peca(i)
	_pega = p - r.position
	_antes = r.position
	_novo = true
	c.deco_ativa = i
	c.queue_redraw()
	gaveta.queue_redraw()
	main._log("tirou do baú: %s" % item)
	return true


## Guarda no baú a peça (e o que está em cima dela que também pode ir).
func guardar(c: Cenario, grupo: Array, festa := true) -> void:
	var foram := 0
	for j in grupo:
		var i := int(j)
		if not c.pode_guardar(i):
			continue
		for t in _apoiados(c, [i]):
			main._fall(t, (t as Toy).global_position)
		_tirar_lugar(c, i)
		var item := c.item_da_peca(i)
		c.guardar_peca(i)
		bau[item] = int(bau.get(item, 0)) + 1
		foram += 1
		main._log("guardou no baú: %s" % item)
	if foram > 0 and festa:
		main._sparkle(main.screen_to_world(botao_bau.get_global_rect().get_center()), 6)
		var tw := botao_bau.create_tween()
		tw.tween_property(botao_bau, "scale", Vector2(1.2, 1.2), 0.1)
		tw.tween_property(botao_bau, "scale", Vector2.ONE, 0.2)
	_esconder_balao()
	gaveta.queue_redraw()
	_salvar()


## Item comprado na loja: entra no baú, e o modo Decorar abre com o baú aberto (quando dá).
func receber(item: String) -> void:
	bau[item] = int(bau.get(item, 0)) + 1
	_salvar()
	if pode():
		ligar()
		abrir_bau(true)
		var lista := _cartas_ordem()
		_pagina = int(lista.find(item) / _por_pagina())
		gaveta.queue_redraw()
	main._log("comprou: %s (vai para o baú)" % item)


## Item que um personagem ou bicho usa (sentar, deitar): ganha um lugar que anda junto com ele.
func _criar_lugar(c: Cenario, i: int) -> void:
	var usa: Dictionary = Itens.ficha(str(c.itens.get(i, ""))).get("usa", {})
	if usa.is_empty():
		return
	var r := c._rect_peca(i)
	var spots: Array = []
	var pts: Array = []
	for sp in usa.get("spots", []):
		var v := r.position + Vector2(float(sp[0]) * r.size.x, float(sp[1]) * r.size.y)
		spots.append(v)
		pts.append([v.x, v.y])
	if spots.is_empty():
		return
	var sid := "item_" + str(c.uids[i])
	var area := Rect2(r.position.x, r.position.y - 80.0, r.size.x, r.size.y + 80.0)
	c.lugares.append({"id": sid, "area": [area.position.x, area.position.y, area.size.x, area.size.y], "spots": pts, "pose": str(usa.get("pose", "sentar"))})
	c._lugar_dono[c.lugares.size() - 1] = i
	var sl: Slot = main._add_slot(sid, area, spots, str(usa.get("pose", "sentar")), "", Toy.depth_for(float(spots[0].y)))
	sl.cena = c.id
	sl.visible = c.id == main.cena


func _tirar_lugar(c: Cenario, i: int) -> void:
	for k in c._lugar_dono.keys():
		if int(c._lugar_dono[k]) != i:
			continue
		var sid := str(c.lugares[k]["id"])
		for s in main.slots.duplicate():
			var sl := s as Slot
			if sl.cena == c.id and sl.id == sid:
				for t in sl.occupants:
					if t:
						main._leave_slot(t)
						main._fall(t, (t as Toy).global_position)
				main.slots.erase(sl)
				sl.queue_free()
		c.lugares[k]["area"] = [-9999.0, -9999.0, 0.0, 0.0]
		c._lugar_dono.erase(k)


func _mostrar_balao(c: Cenario, i: int) -> void:
	_balao_i = i
	_balao_t = 4.0
	balao.visible = true
	_pos_balao()


func _pos_balao() -> void:
	var c := _cenario()
	if _balao_i < 0 or _balao_i >= c.pecas.size() or c.guardadas.has(_balao_i):
		_esconder_balao()
		return
	var r := c._rect_peca(_balao_i)
	var sp: Vector2 = main.world_to_screen(Vector2(r.get_center().x, r.position.y))
	balao.position = sp - Vector2(balao.size.x / 2.0, balao.size.y + 6.0)


func _esconder_balao() -> void:
	_balao_i = -1
	if balao:
		balao.visible = false


func _guardar_balao() -> void:
	var i := _balao_i
	if i < 0 or not pode():
		return
	var c := _cenario()
	var grupo := [i]
	for j in c.carga(i):
		grupo.append(j)
	guardar(c, grupo)


## Enfeites comprados antes do baú (objetos soltos da fazendinha) viram itens normais, no mesmo lugar.
func _migrar_enfeites() -> void:
	if main.fazenda == null or main.fazenda.enfeites_antigos.is_empty():
		return
	for en in main.fazenda.enfeites_antigos:
		var item := str(en[0])
		if not Itens.da_loja(item):
			continue
		var c: Variant = main.cenarios.get(str(en[1]))
		if c is Cenario:
			var tam := Itens.tamanho(item)
			var uid := "n%d" % uid_prox
			uid_prox += 1
			var i := (c as Cenario).colocar_item(item, Vector2(float(en[2]) - tam.x / 2.0, float(en[3])), uid)
			_criar_lugar(c, i)
		else:
			bau[item] = int(bau.get(item, 0)) + 1
	main.fazenda.enfeites_antigos.clear()
	_salvar()
	main.fazenda.salvar()
