extends Node2D
## Fazenda Capricho — Protótipo de interação P-0 (quarto da Catarina).
##
## O que este protótipo testa (GDD, seção 8):
##   arrastar personagens e objetos, segurar objeto na mão, deitar no beliche, descer o
##   escorregador, subir a escada, entrar no castelinho, abrir/fechar a portinha roxa e
##   combinar objeto + personagem (petisco no Bob, escova, pelúcia, almofada).
##
## Como a interação funciona:
##   - toque curto: o personagem/objeto reage (tabela "toques" em dados/interacoes.json);
##   - tocar e arrastar: pega; ao soltar, a ordem de decisão é
##       1. combinação objeto + alvo (tabela "combinacoes")  -> reação
##       2. objeto sobre personagem com mão                  -> segura na mão
##       3. personagem sobre um lugar (cama, castelo...)     -> encaixa
##       4. caso contrário                                   -> cai na superfície abaixo
##   - enquanto arrasta, o lugar ou personagem que vai receber o soltar brilha.
##
## Cenários: o quarto (room.gd, desenhado por código/arte 3D) e os cenários montados por dados
## (cenario.gd + dados/cenarios/<id>.json). Portas ligam um ao outro: tocar na porta leva só a
## câmera; soltar um personagem na porta leva o personagem junto (com o que estiver segurando).

const DATA_PATH := "res://dados/interacoes.json"
const RoomScript := preload("res://scripts/room.gd")

var W := 2200.0                  # largura do cenário que está na tela
const H := 900.0
const FLOOR_Y := 600.0
const DRAG_START := 10.0
const JAR_RECT := Rect2(1360, 448, 108, 112)
const MAX_COOKIES := 3
const TEXT_COLOR := Color("#7a3fa8")
const DROP_SLACK := 40.0    # folga ao soltar algo sobre um personagem
const LIFT := 40.0          # quanto o personagem sobe acima do dedo ao ser pego
const EDGE := 110.0         # faixa da borda da tela que faz o quarto rolar
const EDGE_SPEED := 650.0
## Onde a câmera para ao chegar pelo mapa (x no cenário); sem valor, o meio do cenário.
const MAPA_CHEGADA := {"quarto": 720.0, "sede": 1060.0, "estabulo": 1000.0, "plantacao": 800.0, "casa_arvore": 950.0}
const QUARTO_PORTA := Rect2(1640, 250, 170, 350)   # porta do quarto: leva à Sala

var castle: CastleFront
var cena := "quarto"              # cenário que está na tela
var cenarios := {}                # id -> nó do cenário (room.gd ou Cenario)
var porta_quarto_aberta: Sprite2D
var mapa: MapaFazenda             # botão da ferradura + mapa da fazenda
var trocando := false             # durante a passagem de um cenário para outro
var cam: Camera2D
var toys: Array[Toy] = []
var slots: Array[Slot] = []
var slot_castelo: Slot
## Superfícies onde as coisas se apoiam: Vector3(x inicial, x final, altura).
var surfaces: Array[Vector3] = [
	Vector3(112.0, 548.0, 270.0),    # colchão do beliche
	Vector3(1282.0, 1508.0, 558.0),  # mesinha
]
var combos := {}
var taps := {}

var press_pos := Vector2.ZERO
var press_screen := Vector2.ZERO
var last_screen := Vector2.ZERO
var panning := false
var pan_velocity := 0.0
var last_move_time := 0
var press_toy: Toy = null
var press_ui := ""
var drag_toy: Toy = null
var drag_offset := Vector2.ZERO
var dragging := false
var touch_index := -1
var last_x := 0.0
var hl_toy: Toy = null
var zzz_timer := 0.0
var idle_timer := 4.0


func _ready() -> void:
	_load_data()
	var room: Node2D = RoomScript.new()
	add_child(room)
	cenarios["quarto"] = room
	castle = CastleFront.new()
	add_child(castle)
	_make_slots()
	_make_porta_quarto()
	_add_cenario("sala")
	_add_cenario("cozinha")
	for id in ["sede", "entrada", "quarto_carol", "estabulo", "plantacao", "pet_care",
			"casa_arvore", "casa_arvore_dentro", "cabana", "casinha"]:
		_add_cenario(id)
	_make_toys()
	_setup_camera()
	mapa = MapaFazenda.new()
	add_child(mapa)
	mapa.escolheu.connect(_ir_pelo_mapa)
	_show_intro()


# ---------------------------------------------------------------- montagem da cena

func _load_data() -> void:
	var data: Variant = null
	var res := load(DATA_PATH)
	if res is JSON:
		data = (res as JSON).data
	else:
		data = JSON.parse_string(FileAccess.get_file_as_string(DATA_PATH))
	if typeof(data) != TYPE_DICTIONARY:
		push_error("Não foi possível ler " + DATA_PATH)
		return
	for c in data.get("combinacoes", []):
		combos[str(c["item"]) + "|" + str(c["alvo"])] = c
	for t in data.get("toques", []):
		taps[str(t["alvo"])] = t


func _make_slots() -> void:
	# Cama de cima: área alta para pegar qualquer soltar acima do beliche.
	_add_slot("cama", Rect2(112, 0, 408, 320), [Vector2(445, 270), Vector2(480, 272), Vector2(250, 272)], "deitar", "",
		Toy.depth_for(300.0))
	slot_castelo = _add_slot("castelo", Rect2(270, 396, 116, 224), [Vector2(318, 598), Vector2(342, 598)],
		"dentro", "", castle.z_index - 1)
	_add_slot("escorregador", Rect2(520, 180, 120, 150), [], "", "escorregar", 0)
	_add_slot("escada", Rect2(36, 330, 80, 272), [], "", "subir", 0)


## Cenário montado por dados (ver scripts/cenario.gd), com seus lugares; começa escondido.
func _add_cenario(id: String) -> Cenario:
	var c := Cenario.new().carregar(id)
	add_child(c)
	c.visible = false
	cenarios[id] = c
	for l in c.lugares:
		var a: Array = l["area"]
		var spots: Array = []
		for sp in l["spots"]:
			spots.append(Vector2(sp[0], sp[1]))
		var s := _add_slot(str(l["id"]), Rect2(a[0], a[1], a[2], a[3]), spots, str(l.get("pose", "deitar")), "",
			Toy.depth_for(float(spots[0].y)) if spots.size() > 0 else 0)
		s.cena = id
		s.visible = false
	for o in c.objetos:
		_add_objeto(id, o)
	return c


## Objeto solto de um cenário (comidinha, xícara...), com a imagem da própria peça.
func _add_objeto(id: String, o: Dictionary) -> Toy:
	var spr := Sprite2D.new()
	var tex := load("res://assets/cenario/%s/%s.png" % [id, o["tipo"]]) as Texture2D
	spr.texture = tex
	spr.centered = false
	spr.scale = Vector2(float(o["w"]) / tex.get_width(), float(o["h"]) / tex.get_height())
	spr.position = Vector2(-float(o["w"]) / 2.0, -float(o["h"]))
	var t := Toy.new()
	t.kind = str(o["tipo"])
	var arte := Node2D.new()  # o Toy mexe na escala da arte (squash): o sprite fica um nível abaixo
	arte.add_child(spr)
	t.setup_art(arte, maxf(26.0, maxf(float(o["w"]), float(o["h"])) / 2.0))
	t.grab_offset = Vector2(0, -float(o["h"]) / 2.0)
	t.position = Vector2(o["x"], o["y"])
	t.cena = id
	t.set_meta("origem", id)
	t.visible = id == cena
	add_child(t)
	toys.append(t)
	return t


## Repõe os objetos do cenário que foram comidos (abrir a geladeira traz as comidinhas de volta).
func _repor_objetos() -> int:
	var n := 0
	for o in (cenarios[cena] as Cenario).objetos:
		var existe := false
		for x in toys:
			existe = existe or (x.kind == str(o["tipo"]) and str(x.get_meta("origem", "")) == cena)
		if not existe:
			var t := _add_objeto(cena, o)
			t.squash = Vector2(0.2, 0.2)
			t.play_anim().tween_property(t, "squash", Vector2.ONE, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			_sparkle(t.global_position + Vector2(0, -20), 3)
			n += 1
	return n


## A porta do quarto aberta usa a mesma arte da porta da Sala, por cima do desenho do quarto.
func _make_porta_quarto() -> void:
	porta_quarto_aberta = Sprite2D.new()
	var tex := load("res://assets/cenario/sala/porta_aberta.png") as Texture2D
	porta_quarto_aberta.texture = tex
	porta_quarto_aberta.centered = false
	porta_quarto_aberta.position = QUARTO_PORTA.position
	porta_quarto_aberta.scale = QUARTO_PORTA.size / Vector2(tex.get_width(), tex.get_height())
	porta_quarto_aberta.z_index = -99
	porta_quarto_aberta.visible = false
	add_child(porta_quarto_aberta)


func _add_slot(id: String, area: Rect2, spots: Array, pose: String, action: String, depth: int) -> Slot:
	var s := Slot.new()
	s.setup(id, area, spots, pose, action, depth)
	add_child(s)
	slots.append(s)
	return s


func _make_toys() -> void:
	# Catarina: folha de pet 3D (arte/animacoes/catarina_pet), como a Nina.
	var cat := _add_pet("catarina", "res://assets/personagens/catarina_pet.json", 300.0, Vector2(720, 730))
	cat.can_hold = true
	cat.can_lie = true
	cat.head_offset = Vector2(2, -244)     # o objeto segurado fica no colo ("colo" no JSON)
	cat.grab_offset = Vector2(0, -150)
	cat.lie_half_width = 60.0

	# Bob: folha 3D montada de tiras (arte/animacoes/bob_pet); vira para o lado em que é levado
	var bob := _add_pet("bob", "res://assets/personagens/bob_pet.json", 170.0, Vector2(1090, 770))
	bob.flips = true
	bob.head_offset = Vector2(34, -112)
	bob.grab_offset = Vector2(0, -85)

	# Tabela de escala (Catarina = 1,0 = 300 px): ver GDD, seção 7.
	var carol := _add_character("carol", "res://assets/personagens/carol.png", 405.0, Vector2(1180, 700))
	carol.can_hold = true
	carol.can_lie = true
	carol.can_ride = true
	carol.hand_offset = Vector2(58, -147)
	carol.head_offset = Vector2(1, -330)
	carol.grab_offset = Vector2(0, -200)
	carol.lie_half_width = 70.0
	carol.too_big_for.assign(["castelo"])

	# Nina: primeira personagem com folha de pet (ações desenhadas): ver _add_pet().
	var nina := _add_pet("nina", "res://assets/personagens/nina_pet.json", 185.0, Vector2(600, 860))
	nina.head_offset = Vector2(0, -144)
	nina.grab_offset = Vector2(0, -90)

	var leo := _add_character("leo", "res://assets/personagens/leo.png", 105.0, Vector2(1400, 860))
	leo.flips = true
	leo.head_offset = Vector2(18, -55)
	leo.grab_offset = Vector2(0, -50)

	var zoe := _add_character("zoe", "res://assets/personagens/zoe.png", 125.0, Vector2(235, 790))
	zoe.flips = true
	zoe.head_offset = Vector2(9, -88)
	zoe.grab_offset = Vector2(0, -60)

	var lumi := _add_character("lumi", "res://assets/personagens/lumi.png", 390.0, Vector2(1950, 870))
	lumi.flips = true
	lumi.head_offset = Vector2(111, -295)
	lumi.grab_offset = Vector2(0, -200)
	lumi.seat_offset = Vector2(-24, -223)
	lumi.too_big_for.assign(["cama", "castelo", "escorregador", "escada"])

	cat.can_ride = true

	_add_item("biscoito", 26.0, Vector2(1330, 558))
	_add_item("pelucia", 40.0, Vector2(480, 700))
	_add_item("escova", 46.0, Vector2(1700, 700))
	_add_item("almofada", 42.0, Vector2(880, 840))


func _add_character(kind: String, path: String, height: float, pos: Vector2) -> Toy:
	var t := Toy.new()
	t.kind = kind
	t.is_character = true
	t.setup_sprite(load(path) as Texture2D, height)
	t.position = pos
	add_child(t)
	toys.append(t)
	return t


## Personagem com folha no formato de pet (JSON ao lado da imagem, ver assets/personagens/nina_pet.json).
func _add_pet(kind: String, json_path: String, height: float, pos: Vector2) -> Toy:
	var data: Dictionary = (load(json_path) as JSON).data
	var tex: Texture2D = null
	if data.has("sheet"):
		tex = load(json_path.get_base_dir().path_join(str(data["sheet"]))) as Texture2D
	var t := Toy.new()
	t.kind = kind
	t.is_character = true
	t.setup_atlas(tex, data, height, json_path.get_base_dir())
	t.position = pos
	add_child(t)
	toys.append(t)
	return t


func _add_item(kind: String, radius: float, pos: Vector2) -> Toy:
	var t := Toy.new()
	t.kind = kind
	t.setup_art(ItemArt.new(kind, radius), radius)
	t.position = pos
	add_child(t)
	toys.append(t)
	return t


# ---------------------------------------------------------------- abertura

## Logo animada (folha de 8 quadros da R01, 160 ms por quadro) sobre fundo rosa.
## Some sozinha em 2,5 s ou com um toque.
func _show_intro() -> void:
	var layer := CanvasLayer.new()
	layer.layer = 10
	add_child(layer)
	var bg := ColorRect.new()
	bg.color = Color(1, 0.84, 0.91)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_STOP
	layer.add_child(bg)
	var logo := Sprite2D.new()
	logo.texture = load("res://assets/marca/logo_fazenda_capricho_pulso_8f.png") as Texture2D
	logo.hframes = 4
	logo.vframes = 2
	bg.add_child(logo)
	var place := func() -> void:
		var vis := get_viewport().get_visible_rect().size
		logo.position = vis / 2.0 + Vector2(0, -20)
		var sc := minf(vis.x * 0.7 / 768.0, vis.y * 0.7 / 512.0)
		logo.scale = Vector2(sc, sc)
	place.call()
	get_viewport().size_changed.connect(place)
	var anim := create_tween().set_loops()
	anim.tween_interval(0.16)
	anim.tween_callback(func() -> void: logo.frame = (logo.frame + 1) % 8)
	var state := {"fechando": false}
	var close := func() -> void:
		if state["fechando"]:
			return
		state["fechando"] = true
		var tw := create_tween()
		tw.tween_property(bg, "modulate:a", 0.0, 0.35)
		tw.tween_callback(func() -> void:
			anim.kill()
			get_viewport().size_changed.disconnect(place)
			layer.queue_free())
	bg.gui_input.connect(func(ev: InputEvent) -> void:
		if ev is InputEventScreenTouch and (ev as InputEventScreenTouch).pressed:
			close.call())
	get_tree().create_timer(2.5).timeout.connect(close)


# ---------------------------------------------------------------- câmera (iPad, estilo Avatar World)
# O quarto (2200 x 900) é mais largo que a tela do iPad: a altura inteira cabe e a criança rola
# para os lados arrastando o dedo num espaço vazio, ou levando um personagem até a borda.

func _setup_camera() -> void:
	cam = Camera2D.new()
	add_child(cam)
	cam.make_current()
	get_viewport().size_changed.connect(_fit_camera)
	_fit_camera()
	camera_to(720.0)


func _fit_camera() -> void:
	var vis := get_viewport().get_visible_rect().size
	var z := vis.y / H
	cam.zoom = Vector2(z, z)
	camera_to(cam.position.x)


func camera_to(x: float) -> void:
	var half := get_viewport().get_visible_rect().size.x / cam.zoom.x / 2.0
	cam.position = Vector2(clampf(x, half, maxf(half, W - half)), H / 2.0)


func screen_to_world(sp: Vector2) -> Vector2:
	var vis := get_viewport().get_visible_rect().size
	return cam.position + (sp - vis / 2.0) / cam.zoom.x


func world_to_screen(wp: Vector2) -> Vector2:
	var vis := get_viewport().get_visible_rect().size
	return (wp - cam.position) * cam.zoom.x + vis / 2.0


# ---------------------------------------------------------------- entrada (toque e mouse)

func _unhandled_input(event: InputEvent) -> void:
	# O mouse é convertido em toque (emulate_touch_from_mouse), então só tratamos toque.
	# Um dedo de cada vez: outros dedos na tela são ignorados.
	if trocando:
		return
	if event is InputEventScreenTouch:
		var st := event as InputEventScreenTouch
		if st.pressed:
			if mapa and (mapa.aberto() or mapa.botao.get_global_rect().has_point(st.position)):
				return  # o toque é do botão da ferradura ou do mapa
			if touch_index == -1:
				touch_index = st.index
				_on_press(st.position)
		elif st.index == touch_index:
			touch_index = -1
			_on_release(st.position)
	elif event is InputEventScreenDrag:
		var sd := event as InputEventScreenDrag
		if sd.index == touch_index:
			_on_move(sd.position)


func _on_press(sp: Vector2) -> void:
	var p := screen_to_world(sp)
	press_pos = p
	press_screen = sp
	last_screen = sp
	press_toy = null
	press_ui = ""
	dragging = false
	panning = false
	pan_velocity = 0.0
	var t := _toy_at(p, [])
	if cena != "quarto":
		var iid: String = (cenarios[cena] as Cenario).interativo_em(p)
		if t:
			press_toy = t
		elif iid != "":
			press_ui = "i:" + iid
		else:
			press_ui = "rolar"
	elif t and t.z_index > castle.z_index:
		press_toy = t
	elif castle.door_hit(p):
		press_ui = "porta"
	elif t:
		press_toy = t
	elif JAR_RECT.has_point(p):
		press_ui = "pote"
	elif QUARTO_PORTA.has_point(p):
		press_ui = "porta_quarto"
	else:
		press_ui = "rolar"


func _on_move(sp: Vector2) -> void:
	var moved := sp.distance_to(press_screen) > DRAG_START
	if press_toy and not dragging and moved:
		_start_drag(press_toy, screen_to_world(sp))
	elif press_ui == "rolar" and moved:
		panning = true
	if panning:
		var dx := (sp.x - last_screen.x) / cam.zoom.x
		camera_to(cam.position.x - dx)
		pan_velocity = clampf(-dx / maxf(get_process_delta_time(), 0.001), -2500.0, 2500.0)
	last_screen = sp
	if dragging:
		_drag_to(screen_to_world(sp))


func _drag_to(p: Vector2) -> void:
	p = p.clamp(Vector2(10, 10), Vector2(W - 10, H - 10))
	drag_toy.global_position = p + drag_offset
	if absf(p.x - last_x) > 4.0:
		drag_toy.face_left(p.x < last_x)
		# folha de pet: corre para o lado em que está sendo levado
		if drag_toy.flips:
			drag_toy.play_state("running-right")  # a figura é espelhada para a esquerda
		else:
			drag_toy.play_state("running-left" if p.x < last_x else "running-right")
		last_x = p.x
		last_move_time = Time.get_ticks_msec()
	_update_highlight(_drop_point(p))


## O personagem fica um pouco acima do dedo (para o dedo não cobrir o rosto);
## o que conta para soltar é o ponto do corpo, não a ponta do dedo.
func _drop_point(finger: Vector2) -> Vector2:
	return finger + Vector2(0, -LIFT)


func _on_release(sp: Vector2) -> void:
	var p := screen_to_world(sp)
	if dragging:
		var t := drag_toy
		dragging = false
		drag_toy = null
		_clear_highlight()
		t.lifted = false
		var fp := p.clamp(Vector2(10, 10), Vector2(W - 10, H - 10))
		_drop(t, _drop_point(fp))
	elif panning:
		panning = false  # continua rolando um pouco (inércia), em _process
	elif press_toy:
		_tap(press_toy)
	elif press_ui == "porta":
		castle.toggle()
		_sparkle(CastleFront.DOOR_CENTER, 4)
		_log("porta " + ("aberta" if castle.is_open else "fechada"))
	elif press_ui == "pote":
		_spawn_cookie()
	elif press_ui == "porta_quarto":
		_abrir_e_ir(null, "sala")
	elif press_ui.begins_with("i:"):
		_tocar_interativo(press_ui.substr(2))
	press_toy = null
	press_ui = ""


## Enquanto arrasta perto da borda da tela, o quarto rola junto (como no Avatar World).
func _edge_scroll(delta: float) -> void:
	var vis := get_viewport().get_visible_rect().size
	var dir := 0.0
	if last_screen.x < EDGE:
		dir = -1.0
	elif last_screen.x > vis.x - EDGE:
		dir = 1.0
	if dir == 0.0:
		return
	var before := cam.position.x
	camera_to(cam.position.x + dir * EDGE_SPEED * delta)
	if cam.position.x != before:
		_drag_to(screen_to_world(last_screen))


func _log(msg: String) -> void:
	print("[P-0] ", msg)


func _toy_at(p: Vector2, exclude: Array, slack: float = 14.0) -> Toy:
	var best: Toy = null
	for t in _toys_aqui():
		if t in exclude or t.busy or not t.visible:
			continue
		if t.slot == slot_castelo and not castle.is_open:
			continue  # escondido atrás da porta fechada
		if t.hit(p, slack) and (best == null or t.z_index > best.z_index):
			best = t
	return best


# ---------------------------------------------------------------- arrastar e soltar

func _start_drag(t: Toy, p: Vector2) -> void:
	dragging = true
	drag_toy = t
	t.kill_move()
	t.play_anim().tween_property(t, "squash", Vector2.ONE, 0.01)
	if t.holder:
		t.holder.held_item = null
		t.holder = null
	if t.mount:
		t.mount.rider = null
		t.mount = null
	_leave_slot(t)
	t.pose = "em_pe"
	t.play_state("idle")  # acorda (folha de pet)
	t.lifted = true
	t.z_index = 450
	drag_offset = -t.grab_offset + Vector2(0, -LIFT)
	last_x = p.x


func _leave_slot(t: Toy) -> void:
	if t.slot:
		t.slot.occupants[t.spot_index] = null
		t.slot = null
		t.spot_index = -1
	t.rotation = 0.0
	t.scale = Vector2.ONE


## Decide o que aconteceria se `t` fosse solto no ponto `p`.
func _resolve(t: Toy, p: Vector2) -> Dictionary:
	if not t.is_character:
		var alvo := _toy_at(p, [t], DROP_SLACK)
		if alvo and alvo.holder:
			alvo = alvo.holder  # soltou sobre o que alguém segura: vale a pessoa
		if alvo:
			var key := t.kind + "|" + alvo.kind
			if combos.has(key):
				return {"tipo": "combo", "item": t, "alvo": alvo, "regra": combos[key], "destaque": alvo}
			if alvo.can_hold:
				return {"tipo": "segurar", "alvo": alvo, "destaque": alvo}
		return {"tipo": "chao"}

	var excl: Array = [t]
	if t.held_item:
		excl.append(t.held_item)
	var other := _toy_at(p, excl, DROP_SLACK)
	if other and other.holder and other.holder != t:
		other = other.holder
	if other:
		# personagem segurando algo, levado até alguém (Catarina leva o biscoito ao Bob)
		if t.held_item and combos.has(t.held_item.kind + "|" + other.kind):
			return {"tipo": "combo", "item": t.held_item, "alvo": other,
				"regra": combos[t.held_item.kind + "|" + other.kind], "destaque": other}
		# alguém levado até quem segura algo (Bob levado até a Catarina com biscoito)
		if other.held_item and combos.has(other.held_item.kind + "|" + t.kind):
			return {"tipo": "combo", "item": other.held_item, "alvo": t,
				"regra": combos[other.held_item.kind + "|" + t.kind], "destaque": other}
		# personagem levado até um objeto solto
		if not other.is_character:
			if combos.has(other.kind + "|" + t.kind):
				return {"tipo": "combo", "item": other, "alvo": t,
					"regra": combos[other.kind + "|" + t.kind], "destaque": other}
			if t.can_hold:
				return {"tipo": "pegar", "item": other, "destaque": other}
		# montar no cavalo: soltar quem pode montar em cima de quem tem sela livre
		if t.can_ride and other.seat_offset != Vector2.ZERO and other.rider == null:
			return {"tipo": "montar", "alvo": other, "destaque": other}
	for s in _slots_aqui():
		if s.area.has_point(p) and s.accepts(t):
			return {"tipo": "vaga", "slot": s}
	return {"tipo": "chao"}


func _drop(t: Toy, p: Vector2) -> void:
	t.play_state("idle")
	if t.is_character:
		var dest := _porta_em(p)
		if dest != "":
			_abrir_e_ir(t, dest)
			return
	var plan := _resolve(t, p)
	match str(plan["tipo"]):
		"combo":
			if t != plan["item"]:
				_fall(t, t.global_position)
			_do_combo(plan["item"], plan["alvo"], plan["regra"])
		"segurar":
			_attach(t, plan["alvo"])
		"pegar":
			_fall(t, t.global_position)
			_attach(plan["item"], t)
		"vaga":
			_enter_slot(t, plan["slot"])
		"montar":
			_mount(t, plan["alvo"])
		_:
			_fall(t, t.global_position)
			for s in _slots_aqui():
				if t.is_character and s.area.has_point(p) and not s.accepts(t):
					_blocked(t)  # soltou num lugar onde não cabe
					break


## Reação de "não deu": orelhas baixas (folha de pet) ou balançar a cabeça.
func _blocked(t: Toy) -> void:
	_log("%s não cabe aqui" % t.kind)
	if t.has_anim("failed"):
		t.play_state("failed", "idle")
	else:
		_add_wiggle(t.play_anim(), t, 4, 5.0)
	_bubble(t, "Hmm, aqui não cabe...")


func _update_highlight(p: Vector2) -> void:
	var plan := _resolve(drag_toy, p)
	for s in _slots_aqui():
		s.highlight = plan.get("slot") == s
	var tt: Toy = plan.get("destaque")
	if tt != hl_toy:
		if hl_toy:
			hl_toy.modulate = Color.WHITE
		hl_toy = tt
		if hl_toy:
			hl_toy.modulate = Color(1.2, 1.2, 1.12)


func _clear_highlight() -> void:
	for s in _slots_aqui():
		s.highlight = false
	if hl_toy:
		hl_toy.modulate = Color.WHITE
	hl_toy = null


func _attach(item: Toy, who: Toy) -> void:
	if who.held_item and who.held_item != item:
		var old := who.held_item
		old.holder = null
		who.held_item = null
		_fall(old, who.global_position + Vector2(80, 0))
	item.kill_move()
	item.holder = who
	who.held_item = item
	_pop(item)
	_sparkle(who.hand_global(), 3)
	_log("%s segura %s" % [who.kind, item.kind])


## Cai até a superfície logo abaixo (colchão, mesinha ou piso).
func _fall(t: Toy, from: Vector2) -> void:
	var target := _surface_point(from)
	t.kill_move()
	t.rotation = 0.0  # objeto que estava no colo de alguém deitado volta a ficar em pé
	t.global_position = from
	var d := from.distance_to(target)
	if d < 3.0:
		t.global_position = target
		_land(t)
		return
	t.move_tween = t.create_tween()
	t.move_tween.tween_property(t, "global_position", target, clampf(sqrt(d) / 30.0, 0.12, 0.5)) \
		.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	t.move_tween.tween_callback(_land.bind(t))


func _surface_point(p: Vector2) -> Vector2:
	var x := clampf(p.x, 40.0, W - 40.0)
	if p.y >= FLOOR_Y + 10.0:
		return Vector2(x, minf(p.y, H - 12.0))
	var best := FLOOR_Y + 14.0
	for s in _superficies():
		if x >= s.x and x <= s.y and s.z >= p.y - 30.0 and s.z < best:
			best = s.z
	return Vector2(x, best)


func _land(t: Toy) -> void:
	if t.is_animating():
		return
	var tw := t.play_anim()
	tw.tween_property(t, "squash", Vector2(1.12, 0.88), 0.07)
	tw.tween_property(t, "squash", Vector2.ONE, 0.14).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


# ---------------------------------------------------------------- lugares interativos

func _mount(t: Toy, horse: Toy) -> void:
	t.kill_move()
	t.mount = horse
	horse.rider = t
	t.pose = "montado"
	_log("%s montou em %s" % [t.kind, horse.kind])
	_pop(t)
	_sparkle(horse.seat_global(), 4)
	var tw := horse.play_anim()
	tw.tween_property(horse, "squash", Vector2(1.04, 0.96), 0.1)
	tw.tween_property(horse, "squash", Vector2.ONE, 0.15)
	_bubble(horse, "Ehêhêhê!")


func _enter_slot(t: Toy, s: Slot) -> void:
	if s.action == "escorregar":
		_slide(t)
		return
	if s.action == "subir":
		_climb(t)
		return
	var i := s.free_spot()
	if i < 0:
		_fall(t, t.global_position)
		return
	if s == slot_castelo:
		castle.set_open(true)
	_log("%s -> %s" % [t.kind, s.id])
	s.occupants[i] = t
	t.slot = s
	t.spot_index = i
	t.z_index = s.depth
	var target: Vector2 = s.spots[i]
	var rot := 0.0
	var sc := Vector2.ONE
	if s.pose == "deitar":
		t.pose = "deitado"
		t.sleep()
		if t.can_lie:
			rot = -PI / 2.0
			sc = Vector2(0.8, 0.8)
			target += Vector2(0, -t.lie_half_width * 0.8)
		else:
			sc = Vector2(0.9, 0.9)
		if t.kind == "catarina":
			_bubble(t, "Boa noite!")
	elif s.pose == "dentro":
		t.pose = "dentro"
		sc = Vector2(0.85, 0.85)
		_bubble(t, "Cheguei no castelinho!")
	t.kill_move()
	t.move_tween = t.create_tween().set_parallel(true)
	t.move_tween.tween_property(t, "global_position", target, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	t.move_tween.tween_property(t, "rotation", rot, 0.25)
	t.move_tween.tween_property(t, "scale", sc, 0.25)


func _slide(t: Toy) -> void:
	t.busy = true
	t.z_index = 300
	t.kill_move()
	t.move_tween = t.create_tween()
	t.move_tween.tween_property(t, "global_position", RoomScript.SLIDE_P0 + Vector2(0, -6), 0.15)
	t.move_tween.tween_method(_slide_step.bind(t), 0.0, 1.0, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
	t.move_tween.tween_callback(_slide_end.bind(t))
	_bubble(t, "Uiii!")


func _slide_step(v: float, t: Toy) -> void:
	t.global_position = Shapes.bezier(RoomScript.SLIDE_P0, RoomScript.SLIDE_P1, RoomScript.SLIDE_P2, v) + Vector2(0, -6)
	t.art.rotation = -0.3 * sin(v * PI)
	if randf() < 0.35:
		var col := Color("#ffe066") if randf() < 0.5 else Color("#ff9ac8")
		_spark(t.global_position + Vector2(randf_range(-30, 30), randf_range(-30, 0)), col)


func _slide_end(t: Toy) -> void:
	_log("%s desceu o escorregador" % t.kind)
	t.busy = false
	t.art.rotation = 0.0
	_fall(t, t.global_position + Vector2(40, 12))


func _climb(t: Toy) -> void:
	t.busy = true
	t.z_index = 300
	t.kill_move()
	t.move_tween = t.create_tween()
	t.move_tween.tween_property(t, "global_position", Vector2(80, 600), 0.2)
	t.move_tween.tween_property(t, "global_position", Vector2(80, 285), 1.1).set_trans(Tween.TRANS_SINE)
	t.move_tween.tween_callback(_climb_end.bind(t))
	var tw := t.play_anim()
	for i in 8:
		tw.tween_property(t.art, "rotation_degrees", 6.0 if i % 2 == 0 else -6.0, 0.14)
	tw.tween_property(t.art, "rotation_degrees", 0.0, 0.1)


func _climb_end(t: Toy) -> void:
	_log("%s subiu a escada" % t.kind)
	t.busy = false
	for s in _slots_aqui():
		if s.id == "cama" and s.free_spot() >= 0:
			_enter_slot(t, s)
			return
	_fall(t, Vector2(150, 620))


# ---------------------------------------------------------------- reações

func _tap(t: Toy) -> void:
	_log("toque " + t.kind)
	if t.pose == "deitado" or t.pose == "cochilando":
		_bubble(t, "Zzz...")
		_hop(t, 8.0)
		return
	var rule: Dictionary = taps.get(t.kind, {})
	var falas: Array = rule.get("falas", [])
	var fala := ""
	if not falas.is_empty():
		fala = str(falas.pick_random())
	var reacao := str(rule.get("reacao", ""))
	if t.has_anim("waving"):
		t.play_state("waving", "idle")  # folha de pet: acena com a pata
	elif fala.begins_with("Atchim"):
		_sneeze(t)
	elif reacao == "girar":
		var tw := t.play_anim()
		tw.tween_property(t, "squash", Vector2(0.05, 1.0), 0.18)
		tw.tween_callback(func() -> void: t.face_left(not t.sprite.flip_h))
		tw.tween_property(t, "squash", Vector2.ONE, 0.18)
	else:
		_hop(t, 30.0)
		if str(rule.get("reacao", "")) == "latir":
			_add_wiggle(t.anim_tween, t, 4, 6.0)
	_bubble(t, fala)
	if t.held_item and t.held_item.kind == "pelucia":
		_hearts(t.head_global(), 3)  # abraço na pelúcia


func _do_combo(item: Toy, alvo: Toy, regra: Dictionary) -> void:
	_log("%s + %s -> %s" % [item.kind, alvo.kind, str(regra.get("reacao", ""))])
	match str(regra.get("reacao", "")):
		"comer":
			_consume(item, alvo)
			var tw := alvo.play_anim()
			for i in 3:
				tw.tween_property(alvo, "squash", Vector2(1.07, 0.93), 0.1)
				tw.tween_property(alvo, "squash", Vector2.ONE, 0.1)
			_add_wiggle(tw, alvo, 6, 7.0)  # abanar (o rabo separado vem com a arte em partes)
			_hearts(alvo.head_global(), 5)
		"escovar":
			_brush(item, alvo)
			_add_wiggle(alvo.play_anim(), alvo, 6, 4.0)
		"brincar":
			var tw := alvo.play_anim()
			for i in 2:
				tw.tween_property(alvo.art, "position:y", -45.0, 0.16).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
				tw.tween_property(alvo.art, "position:y", 0.0, 0.16).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
			if item.holder == null:
				_fall(item, alvo.global_position + Vector2(-110, 0))
			_hearts(alvo.head_global(), 3)
		"cochilar":
			_nap(alvo, item)
		_:
			_hop(alvo, 20.0)
	# folha de pet: a ação desenhada acompanha a reação
	var acao := {"comer": "jumping", "brincar": "jumping", "escovar": "waiting", "cochilar": "waiting"}
	alvo.play_state(str(acao.get(str(regra.get("reacao", "")), "jumping")), "idle")
	_bubble(alvo, str(regra.get("fala", "")))


func _consume(item: Toy, alvo: Toy) -> void:
	if item.holder:
		item.holder.held_item = null
		item.holder = null
	toys.erase(item)
	item.kill_move()
	item.busy = true
	item.z_index = alvo.z_index + 1
	var tw := item.create_tween().set_parallel(true)
	tw.tween_property(item, "global_position", alvo.head_global() + Vector2(0, 30), 0.25)
	tw.tween_property(item, "modulate:a", 0.0, 0.35)
	tw.chain().tween_callback(item.queue_free)


func _brush(item: Toy, alvo: Toy) -> void:
	var body := alvo.to_global(Vector2(0, -alvo.display_size().y * 0.5))
	for i in 6:
		_spark(body + Vector2(randf_range(-80, 80), randf_range(-50, 40)), Color("#fff6a8"))
	if item.holder:
		return  # escovando pela mão da Catarina
	item.kill_move()
	item.busy = true
	item.z_index = alvo.z_index + 1
	item.move_tween = item.create_tween()
	item.move_tween.tween_property(item, "global_position", body + Vector2(-50, 20), 0.12)
	for i in 3:
		item.move_tween.tween_property(item, "global_position", body + Vector2(50, 20), 0.18)
		item.move_tween.tween_property(item, "global_position", body + Vector2(-50, 20), 0.18)
	item.move_tween.tween_callback(_brush_end.bind(item, alvo))


func _brush_end(item: Toy, alvo: Toy) -> void:
	item.busy = false
	_fall(item, alvo.global_position + Vector2(120, -10))


func _nap(alvo: Toy, item: Toy) -> void:
	if item.holder:
		item.holder.held_item = null
		item.holder = null
	item.kill_move()
	item.busy = true
	item.global_position = alvo.global_position + Vector2(0, 4)
	item.z_index = alvo.z_index - 1
	alvo.pose = "cochilando"
	alvo.sleep()
	var tw := alvo.play_anim()
	tw.tween_property(alvo, "squash", Vector2(1.06, 0.88), 0.3)
	get_tree().create_timer(4.0).timeout.connect(_nap_end.bind(alvo, item))


func _nap_end(alvo: Toy, item: Toy) -> void:
	item.busy = false
	if alvo.pose == "cochilando" and not alvo.lifted:
		alvo.pose = "em_pe"
		alvo.play_state("idle")
		_hop(alvo, 25.0)
		_bubble(alvo, "Au!")


func _spawn_cookie() -> void:
	if _count("biscoito") >= MAX_COOKIES:
		_float_text(JAR_RECT.get_center() + Vector2(0, -60), "Já tem biscoito!", 28)
		return
	var c := _add_item("biscoito", 26.0, Vector2(1414, 470))
	_log("pote deu biscoito")
	var tw := c.play_anim()
	c.squash = Vector2(0.2, 0.2)
	tw.tween_property(c, "squash", Vector2.ONE, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_fall(c, Vector2(1414 + randf_range(-110, -55), 470))
	_sparkle(JAR_RECT.get_center(), 4)


# ---------------------------------------------------------------- animações e efeitos

func _hop(t: Toy, h: float) -> void:
	var tw := t.play_anim()
	tw.tween_property(t.art, "position:y", -h, 0.14).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(t.art, "position:y", 0.0, 0.14).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_property(t, "squash", Vector2(1.1, 0.9), 0.06)
	tw.tween_property(t, "squash", Vector2.ONE, 0.12)


func _sneeze(t: Toy) -> void:
	var tw := t.play_anim()
	tw.tween_property(t, "squash", Vector2(0.92, 1.1), 0.25)
	tw.tween_property(t, "squash", Vector2(1.15, 0.85), 0.06)
	tw.tween_property(t, "squash", Vector2.ONE, 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _add_wiggle(tw: Tween, t: Toy, n: int, deg: float) -> void:
	if tw == null or not tw.is_valid():
		return
	for i in n:
		tw.tween_property(t.art, "rotation_degrees", deg if i % 2 == 0 else -deg, 0.07)
	tw.tween_property(t.art, "rotation_degrees", 0.0, 0.07)


func _pop(t: Toy) -> void:
	var tw := t.play_anim()
	tw.tween_property(t, "squash", Vector2(1.2, 1.2), 0.08)
	tw.tween_property(t, "squash", Vector2.ONE, 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _bubble(t: Toy, text: String) -> void:
	_float_text(t.head_global() + Vector2(0, -24), text, 34)


func _float_text(p: Vector2, text: String, font_size: int) -> void:
	if text.is_empty():
		return
	var l := Label.new()
	l.text = text
	var ls := LabelSettings.new()
	ls.font_size = font_size
	ls.font_color = TEXT_COLOR
	ls.outline_size = 12
	ls.outline_color = Color.WHITE
	l.label_settings = ls
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	l.size = Vector2(420, font_size * 1.6)
	l.position = Vector2(clampf(p.x - 210.0, 0.0, W - 420.0), maxf(p.y - font_size * 1.6, 0.0))
	l.z_index = 430
	add_child(l)
	var tw := l.create_tween().set_parallel(true)
	tw.tween_property(l, "position:y", l.position.y - 50.0, 1.4).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(l, "modulate:a", 0.0, 0.5).set_delay(0.9)
	tw.chain().tween_callback(l.queue_free)


func _hearts(p: Vector2, n: int) -> void:
	for i in n:
		var f := FxShape.new("coracao", Color("#ff6fa8") if i % 2 == 0 else Color("#ff9ac8"), randf_range(10.0, 16.0))
		_float_fx(f, p + Vector2(randf_range(-40, 40), randf_range(-10, 10)), i * 0.08)


func _sparkle(p: Vector2, n: int) -> void:
	for i in n:
		_spark(p + Vector2(randf_range(-40, 40), randf_range(-30, 30)), Color("#ffe066"))


func _spark(p: Vector2, col: Color) -> void:
	_float_fx(FxShape.new("estrela", col, randf_range(7.0, 12.0)), p, 0.0)


func _float_fx(f: Node2D, p: Vector2, delay: float) -> void:
	f.position = p
	add_child(f)
	var tw := f.create_tween().set_parallel(true)
	tw.tween_property(f, "position:y", p.y - randf_range(50.0, 90.0), 0.9).set_delay(delay)
	tw.tween_property(f, "modulate:a", 0.0, 0.5).set_delay(delay + 0.4)
	tw.chain().tween_callback(f.queue_free)


func _count(kind: String) -> int:
	var n := 0
	for t in _toys_aqui():
		if t.kind == kind:
			n += 1
	return n


func _find(kind: String) -> Toy:
	for t in _toys_aqui():
		if t.kind == kind:
			return t
	return null


# ---------------------------------------------------------------- cenários e portas

func _toys_aqui() -> Array[Toy]:
	var r: Array[Toy] = []
	for t in toys:
		if t.cena == cena:
			r.append(t)
	return r


func _slots_aqui() -> Array[Slot]:
	var r: Array[Slot] = []
	for s in slots:
		if s.cena == cena:
			r.append(s)
	return r


func _superficies() -> Array[Vector3]:
	if cena == "quarto":
		return surfaces
	return (cenarios[cena] as Cenario).superficies


## Para onde leva a porta que está no ponto p ("" se não há porta que leve a algum lugar).
func _porta_em(p: Vector2) -> String:
	if cena == "quarto":
		return "sala" if QUARTO_PORTA.has_point(p) else ""
	var c := cenarios[cena] as Cenario
	var iid := c.interativo_em(p)
	return c.destino(iid) if iid != "" else ""


## x de chegada no cenário `dest` vindo do cenário atual (diante da porta que liga os dois).
func _chegada(dest: String) -> float:
	if dest == "quarto":
		return QUARTO_PORTA.get_center().x
	var c := cenarios[dest] as Cenario
	for iid in c.interativos:
		if c.destino(iid) == cena:
			return float(c.interativos[iid].get("chegada", c.rect_de(iid).get_center().x))
	return W / 2.0


func _porta_para(dest: String) -> String:
	var c := cenarios[cena] as Cenario
	for iid in c.interativos:
		if c.destino(iid) == dest:
			return iid
	return ""


## Toque numa peça interativa de um cenário montado por dados.
func _tocar_interativo(iid: String) -> void:
	var c := cenarios[cena] as Cenario
	var r := c.rect_de(iid)
	if c.interativos[iid].has("leva"):
		if c.destino(iid) != "":
			_abrir_e_ir(null, c.destino(iid))
		else:
			c.alternar(iid)  # porta de um cômodo que ainda não existe: só abre e fecha
			_sparkle(r.get_center(), 3)
			_log("%s %s" % [iid, "aberta" if c.estado(iid) == 1 else "fechada"])
		return
	var e := c.alternar(iid)
	_sparkle(r.get_center(), 5 if e == 1 else 2)
	if e == 1 and c.interativos[iid].get("repoe", false) and _repor_objetos() > 0:
		_log("%s repôs as comidinhas" % iid)
	_log("%s -> %s" % [iid, c.interativos[iid]["estados"][e]])


## Viagem pelo mapa da fazenda: só a câmera vai (os personagens ficam onde estão).
func _ir_pelo_mapa(dest: String) -> void:
	if trocando or dest == cena or not cenarios.has(dest):
		return
	trocando = true
	_log("mapa: a câmera vai para %s" % dest)
	var x: float = MAPA_CHEGADA.get(dest, -1.0)
	var veu := ColorRect.new()
	veu.color = Color(1, 0.88, 0.94, 0.0)
	veu.set_anchors_preset(Control.PRESET_FULL_RECT)
	veu.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var camada := CanvasLayer.new()
	camada.layer = 5
	camada.add_child(veu)
	add_child(camada)
	var tw := create_tween()
	tw.tween_property(veu, "color:a", 1.0, 0.2)
	tw.tween_callback(func() -> void:
		var origem := cena
		_fechar_portas(origem)
		_mostrar_cenario(dest)
		camera_to(x if x >= 0.0 else W / 2.0))
	tw.tween_property(veu, "color:a", 0.0, 0.25)
	tw.tween_callback(func() -> void:
		camada.queue_free()
		trocando = false)


## Abre a porta e passa para o outro cenário; com `t`, o personagem (e quem vai com ele) vai junto.
func _abrir_e_ir(t: Toy, dest: String) -> void:
	if trocando:
		return
	if cena == "quarto":
		porta_quarto_aberta.visible = true
		_sparkle(QUARTO_PORTA.get_center(), 4)
	else:
		var iid := _porta_para(dest)
		if iid != "":
			(cenarios[cena] as Cenario).set_estado(iid, 1)
			_sparkle((cenarios[cena] as Cenario).rect_de(iid).get_center(), 4)
	var x := _chegada(dest)
	var grupo: Array[Toy] = []
	if t:
		for o in [t, t.held_item, t.rider, t.mount]:
			if o and not (o in grupo):
				grupo.append(o)
		var cavalo := t.mount if t.mount else t
		if cavalo.rider and not (cavalo.rider in grupo):
			grupo.append(cavalo.rider)
		if cavalo.rider and cavalo.rider.held_item and not (cavalo.rider.held_item in grupo):
			grupo.append(cavalo.rider.held_item)
	trocando = true
	_log("%s vai para %s" % ["a câmera" if t == null else t.kind, dest])
	var veu := ColorRect.new()
	veu.color = Color(1, 0.88, 0.94, 0.0)
	veu.set_anchors_preset(Control.PRESET_FULL_RECT)
	veu.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var camada := CanvasLayer.new()
	camada.layer = 5
	camada.add_child(veu)
	add_child(camada)
	var tw := create_tween()
	tw.tween_interval(0.25)
	tw.tween_property(veu, "color:a", 1.0, 0.2)
	tw.tween_callback(func() -> void:
		var origem := cena
		_mostrar_cenario(dest)
		_fechar_portas(origem)
		for o in grupo:
			o.cena = dest
			o.visible = true
		if t:
			var cavalo := t.mount if t.mount else t
			cavalo.kill_move()
			cavalo.global_position = Vector2(x, FLOOR_Y + 120.0)
			if cavalo.held_item:
				cavalo.held_item.global_position = cavalo.hand_global()
		camera_to(x)
		_abrir_chegada(origem))
	tw.tween_property(veu, "color:a", 0.0, 0.25)
	tw.tween_callback(func() -> void:
		camada.queue_free()
		trocando = false
		if t:
			_pop(t.mount if t.mount else t)
			_hearts((t.mount if t.mount else t).head_global(), 2))


func _mostrar_cenario(dest: String) -> void:
	cena = dest
	if mapa:
		mapa.cena_atual = dest
	W = (cenarios[dest] as Cenario).largura if cenarios[dest] is Cenario else 2200.0
	for id in cenarios:
		(cenarios[id] as Node2D).visible = id == dest
		if id != dest and cenarios[id] is Cenario:
			(cenarios[id] as Cenario).soltar()
	castle.visible = dest == "quarto"
	for t in toys:
		t.visible = t.cena == dest
	for s in slots:
		s.visible = s.cena == dest


func _fechar_portas(origem: String) -> void:
	if origem == "quarto":
		porta_quarto_aberta.visible = false
		return
	var c := cenarios[origem] as Cenario
	for iid in c.interativos:
		if c.destino(iid) != "":
			c.set_estado(iid, 0)


## A porta por onde se chega fica aberta um instante e fecha.
func _abrir_chegada(origem: String) -> void:
	if cena == "quarto":
		porta_quarto_aberta.visible = true
		get_tree().create_timer(0.9).timeout.connect(func() -> void:
			if cena == "quarto":
				porta_quarto_aberta.visible = false)
		return
	var c := cenarios[cena] as Cenario
	var iid := _porta_para(origem)
	if iid == "":
		return
	c.set_estado(iid, 1)
	get_tree().create_timer(0.9).timeout.connect(func() -> void: c.set_estado(iid, 0))


# ---------------------------------------------------------------- vida no cenário

## Quem tem as linhas de olhar da folha de pet acompanha com a cabeça o que está sendo arrastado.
func _update_looks() -> void:
	for t in _toys_aqui():
		if not t.has_anim("look-row-9") or t == drag_toy or t.lifted or t.busy or t.pose != "em_pe":
			continue
		var looking := t.anim_state.begins_with("look")
		if not dragging or drag_toy == null:
			if looking:
				t.play_state("idle")
			continue
		if not looking and t.anim_state != "idle":
			continue  # não interrompe um aceno ou um pulo
		var d := drag_toy.global_position + drag_toy.grab_offset - t.head_global()
		if d.length() > 900.0:
			if looking:
				t.play_state("idle")
			continue
		# 0° = para cima, sentido horário, 16 direções de 22,5°
		var ang := fposmod(rad_to_deg(atan2(d.x, -d.y)), 360.0)
		var idx := int(round(ang / 22.5)) % 16
		t.hold_frame("look-row-9" if idx < 8 else "look-row-10", idx % 8)


func _process(delta: float) -> void:
	_update_looks()
	if dragging:
		_edge_scroll(delta)
		if drag_toy and drag_toy.anim_state.begins_with("running") \
				and Time.get_ticks_msec() - last_move_time > 250:
			drag_toy.play_state("idle")  # parou de mexer o dedo
	elif not panning and absf(pan_velocity) > 5.0:
		camera_to(cam.position.x + pan_velocity * delta)
		pan_velocity = lerpf(pan_velocity, 0.0, minf(1.0, 6.0 * delta))
	zzz_timer -= delta
	if zzz_timer <= 0.0:
		zzz_timer = 1.1
		for t in _toys_aqui():
			if (t.pose == "deitado" or t.pose == "cochilando") and not t.lifted:
				_float_text(t.head_global() + Vector2(randf_range(-6, 18), 0), "z", 26)
	idle_timer -= delta
	if idle_timer <= 0.0:
		idle_timer = randf_range(3.5, 7.0)
		var bob := _find("bob")
		if bob and bob.pose == "em_pe" and not bob.lifted and not bob.busy and not bob.is_animating():
			_add_wiggle(bob.play_anim(), bob, 4, 4.0)  # Bob fica inquieto de vez em quando
		if cena == "quarto" and _count("biscoito") == 0:
			_sparkle(JAR_RECT.get_center(), 2)  # dica: o pote dá biscoitos
