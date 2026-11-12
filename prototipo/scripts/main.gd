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

const DATA_PATH := "res://dados/interacoes.json"
const RoomScript := preload("res://scripts/room.gd")

const W := 1600.0
const H := 900.0
const FLOOR_Y := 600.0
const DRAG_START := 10.0
const JAR_RECT := Rect2(1360, 448, 108, 112)
const MAX_COOKIES := 3
const TEXT_COLOR := Color("#7a3fa8")

var castle: CastleFront
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
	add_child(RoomScript.new())
	castle = CastleFront.new()
	add_child(castle)
	_make_slots()
	_make_toys()


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
	_add_slot("cama", Rect2(112, 0, 408, 320), [Vector2(445, 270), Vector2(480, 272)], "deitar", "",
		Toy.depth_for(300.0))
	slot_castelo = _add_slot("castelo", Rect2(285, 420, 112, 200), [Vector2(340, 598), Vector2(372, 598)],
		"dentro", "", castle.z_index - 1)
	_add_slot("escorregador", Rect2(520, 180, 120, 150), [], "", "escorregar", 0)
	_add_slot("escada", Rect2(36, 330, 80, 272), [], "", "subir", 0)


func _add_slot(id: String, area: Rect2, spots: Array, pose: String, action: String, depth: int) -> Slot:
	var s := Slot.new()
	s.setup(id, area, spots, pose, action, depth)
	add_child(s)
	slots.append(s)
	return s


func _make_toys() -> void:
	var cat := _add_character("catarina", "res://assets/personagens/catarina.png", 300.0, Vector2(720, 730))
	cat.can_hold = true
	cat.can_lie = true
	cat.hand_offset = Vector2(51, -102)    # mão direita (lado direito da tela)
	cat.head_offset = Vector2(9, -235)
	cat.grab_offset = Vector2(0, -150)
	cat.lie_half_width = 60.0

	var bob := _add_character("bob", "res://assets/personagens/bob.png", 170.0, Vector2(1090, 770))
	bob.flips = true
	bob.head_offset = Vector2(56, -120)
	bob.grab_offset = Vector2(0, -85)

	_add_item("biscoito", 26.0, Vector2(1330, 558))
	_add_item("pelucia", 34.0, Vector2(480, 700))
	_add_item("escova", 34.0, Vector2(1240, 690))
	_add_item("almofada", 36.0, Vector2(880, 840))


func _add_character(kind: String, path: String, height: float, pos: Vector2) -> Toy:
	var t := Toy.new()
	t.kind = kind
	t.is_character = true
	t.setup_sprite(load(path) as Texture2D, height)
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


# ---------------------------------------------------------------- entrada (toque e mouse)

func _unhandled_input(event: InputEvent) -> void:
	# O mouse é convertido em toque (emulate_touch_from_mouse), então só tratamos toque.
	if event is InputEventScreenTouch:
		var st := event as InputEventScreenTouch
		if st.pressed:
			if touch_index == -1:
				touch_index = st.index
				_on_press(_to_world(st.position))
		elif st.index == touch_index:
			touch_index = -1
			_on_release(_to_world(st.position))
	elif event is InputEventScreenDrag:
		var sd := event as InputEventScreenDrag
		if sd.index == touch_index:
			_on_move(_to_world(sd.position))


func _to_world(p: Vector2) -> Vector2:
	return get_canvas_transform().affine_inverse() * p


func _on_press(p: Vector2) -> void:
	press_pos = p
	press_toy = null
	press_ui = ""
	dragging = false
	var t := _toy_at(p, [])
	if t and t.z_index > castle.z_index:
		press_toy = t
	elif castle.door_hit(p):
		press_ui = "porta"
	elif t:
		press_toy = t
	elif JAR_RECT.has_point(p):
		press_ui = "pote"


func _on_move(p: Vector2) -> void:
	if press_toy and not dragging and p.distance_to(press_pos) > DRAG_START:
		_start_drag(press_toy, p)
	if dragging:
		p = p.clamp(Vector2(10, 10), Vector2(W - 10, H - 10))
		drag_toy.global_position = p + drag_offset
		if absf(p.x - last_x) > 4.0:
			drag_toy.face_left(p.x < last_x)
			last_x = p.x
		_update_highlight(p)


func _on_release(p: Vector2) -> void:
	if dragging:
		var t := drag_toy
		dragging = false
		drag_toy = null
		_clear_highlight()
		t.lifted = false
		_drop(t, p.clamp(Vector2(10, 10), Vector2(W - 10, H - 10)))
	elif press_toy:
		_tap(press_toy)
	elif press_ui == "porta":
		castle.toggle()
		_sparkle(CastleFront.DOOR_CENTER, 4)
	elif press_ui == "pote":
		_spawn_cookie()
	press_toy = null
	press_ui = ""


func _toy_at(p: Vector2, exclude: Array) -> Toy:
	var best: Toy = null
	for t in toys:
		if t in exclude or t.busy or not t.visible:
			continue
		if t.slot == slot_castelo and not castle.is_open:
			continue  # escondido atrás da porta fechada
		if t.hit(p) and (best == null or t.z_index > best.z_index):
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
	_leave_slot(t)
	t.pose = "em_pe"
	t.lifted = true
	t.z_index = 450
	drag_offset = -t.grab_offset
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
		var alvo := _toy_at(p, [t])
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
	var other := _toy_at(p, excl)
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
	for s in slots:
		if s.area.has_point(p) and s.accepts(t):
			return {"tipo": "vaga", "slot": s}
	return {"tipo": "chao"}


func _drop(t: Toy, p: Vector2) -> void:
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
		_:
			_fall(t, t.global_position)


func _update_highlight(p: Vector2) -> void:
	var plan := _resolve(drag_toy, p)
	for s in slots:
		s.highlight = plan.get("slot") == s
	var tt: Toy = plan.get("destaque")
	if tt != hl_toy:
		if hl_toy:
			hl_toy.modulate = Color.WHITE
		hl_toy = tt
		if hl_toy:
			hl_toy.modulate = Color(1.2, 1.2, 1.12)


func _clear_highlight() -> void:
	for s in slots:
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


## Cai até a superfície logo abaixo (colchão, mesinha ou piso).
func _fall(t: Toy, from: Vector2) -> void:
	var target := _surface_point(from)
	t.kill_move()
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
	for s in surfaces:
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
	s.occupants[i] = t
	t.slot = s
	t.spot_index = i
	t.z_index = s.depth
	var target: Vector2 = s.spots[i]
	var rot := 0.0
	var sc := Vector2.ONE
	if s.pose == "deitar":
		t.pose = "deitado"
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
	t.busy = false
	for s in slots:
		if s.id == "cama" and s.free_spot() >= 0:
			_enter_slot(t, s)
			return
	_fall(t, Vector2(150, 620))


# ---------------------------------------------------------------- reações

func _tap(t: Toy) -> void:
	if t.pose == "deitado" or t.pose == "cochilando":
		_bubble(t, "Zzz...")
		_hop(t, 8.0)
		return
	var rule: Dictionary = taps.get(t.kind, {})
	var falas: Array = rule.get("falas", [])
	var fala := ""
	if not falas.is_empty():
		fala = str(falas.pick_random())
	if fala.begins_with("Atchim"):
		_sneeze(t)
	else:
		_hop(t, 30.0)
		if str(rule.get("reacao", "")) == "latir":
			_add_wiggle(t.anim_tween, t, 4, 6.0)
	_bubble(t, fala)
	if t.held_item and t.held_item.kind == "pelucia":
		_hearts(t.head_global(), 3)  # abraço na pelúcia


func _do_combo(item: Toy, alvo: Toy, regra: Dictionary) -> void:
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
	var tw := alvo.play_anim()
	tw.tween_property(alvo, "squash", Vector2(1.06, 0.88), 0.3)
	get_tree().create_timer(4.0).timeout.connect(_nap_end.bind(alvo, item))


func _nap_end(alvo: Toy, item: Toy) -> void:
	item.busy = false
	if alvo.pose == "cochilando" and not alvo.lifted:
		alvo.pose = "em_pe"
		_hop(alvo, 25.0)
		_bubble(alvo, "Au!")


func _spawn_cookie() -> void:
	if _count("biscoito") >= MAX_COOKIES:
		_float_text(JAR_RECT.get_center() + Vector2(0, -60), "Já tem biscoito!", 28)
		return
	var c := _add_item("biscoito", 26.0, Vector2(1414, 470))
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
	for t in toys:
		if t.kind == kind:
			n += 1
	return n


func _find(kind: String) -> Toy:
	for t in toys:
		if t.kind == kind:
			return t
	return null


# ---------------------------------------------------------------- vida no cenário

func _process(delta: float) -> void:
	zzz_timer -= delta
	if zzz_timer <= 0.0:
		zzz_timer = 1.1
		for t in toys:
			if (t.pose == "deitado" or t.pose == "cochilando") and not t.lifted:
				_float_text(t.head_global() + Vector2(randf_range(-6, 18), 0), "z", 26)
	idle_timer -= delta
	if idle_timer <= 0.0:
		idle_timer = randf_range(3.5, 7.0)
		var bob := _find("bob")
		if bob and bob.pose == "em_pe" and not bob.lifted and not bob.busy and not bob.is_animating():
			_add_wiggle(bob.play_anim(), bob, 4, 4.0)  # Bob fica inquieto de vez em quando
		if _count("biscoito") == 0:
			_sparkle(JAR_RECT.get_center(), 2)  # dica: o pote dá biscoitos
