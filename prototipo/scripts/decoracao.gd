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

static var arquivo := "user://decoracao.json"

const BOTAO_POS := Vector2(18, 172)
const BOTAO_TAM := Vector2(140, 140)
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


## Liga cada cenário ao modo Decorar e põe as peças onde a criança deixou da última vez.
func preparar(m: Node2D) -> void:
	main = m
	for id in main.cenarios:
		var c = main.cenarios[id]
		if c is Cenario:
			(c as Cenario).preparar_deco()
			(c as Cenario).peca_movida.connect(_peca_movida.bind(c))
	_carregar()


func pode() -> bool:
	return main != null and main.cena != "quarto" and main.cenarios.get(main.cena) is Cenario


func alternar() -> void:
	if ligado:
		desligar()
	else:
		ligar()


func ligar() -> void:
	if not pode():
		return
	ligado = true
	botao.texture_normal = _tex_pronto
	_cenario().decorando = true
	_cenario().queue_redraw()
	main._log("modo Decorar ligado")


func desligar() -> void:
	if _cen:
		soltar()
	ligado = false
	botao.texture_normal = _tex_decorar
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
	if i < 0:
		return false
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


func soltar() -> void:
	if _cen == null:
		return
	var c := _cen
	var i := int(_grupo[0])
	var r := c._rect_peca(i)
	c.deco_ativa = -1
	c.queue_redraw()
	if r.position.distance_to(_antes) > 2.0:
		main._sparkle(Vector2(r.get_center().x, r.end.y - 10.0), 4)
		main._log("decorou: %s foi para (%d, %d)" % [c.chave_peca(i), r.position.x, r.position.y])
		_cen = null
		_salvar()
	else:
		c.sacudir(i)  # só tocou: dá uma balançadinha
		_cen = null
	_grupo = []


## Enquanto leva uma peça perto da borda da tela, o cenário rola junto (como ao arrastar um personagem).
func _process(delta: float) -> void:
	if main == null:
		return
	var mostra: bool = pode() and not (main.mapa and main.mapa.aberto())
	botao.visible = mostra
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
	for id in main.cenarios:
		if main.cenarios[id] is Cenario:
			var a := (main.cenarios[id] as Cenario).arrumacao()
			if not a.is_empty():
				tudo[id] = a
	var f := FileAccess.open(arquivo, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify({"versao": 1, "cenarios": tudo}))


func _carregar() -> void:
	if not FileAccess.file_exists(arquivo):
		return
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(arquivo))
	if typeof(d) != TYPE_DICTIONARY:
		return
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
