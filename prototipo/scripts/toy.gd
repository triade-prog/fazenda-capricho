class_name Toy
extends Node2D
## Qualquer coisa que a criança pode pegar: personagens, animais e objetos.
## A origem (position) fica nos pés / na base, para apoiar em superfícies e ordenar a profundidade.
##
## Camadas:
##   - o próprio Toy (position, rotation, scale) = onde está e em que pose (em pé, deitado...);
##   - `art` (sprite ou desenho) = animação: respirar, pular, balançar, amassar.

var kind := ""                    # id usado na tabela de interações (ex.: "bob", "biscoito")
var is_character := false
var can_hold := false             # tem mão para segurar objetos
var can_lie := false              # deita girando o corpo (humanos)
var flips := false                # vira para o lado em que está sendo arrastado
var hand_offset := Vector2.ZERO   # posição da mão, relativa aos pés
var head_offset := Vector2(0, -100)
var grab_offset := Vector2(0, -50)  # ponto do corpo que fica sob o dedo ao arrastar
var lie_half_width := 40.0
var can_ride := false             # pode montar no cavalo
var seat_offset := Vector2.ZERO   # onde fica a sela (só para quem pode ser montado)
var too_big_for: Array[String] = []  # lugares onde não cabe (ex.: Lumi não entra no castelinho)
var mount: Toy = null             # em quem está montado
var rider: Toy = null             # quem está montado em mim
var hit_radius := 40.0            # objetos desenhados: raio de toque

var art: Node2D
var sprite: Sprite2D
var base_art_scale := Vector2.ONE
var squash := Vector2.ONE         # usado pelas animações de amassar/esticar

var held_item: Toy = null         # o que este personagem segura
var holder: Toy = null            # quem está segurando este objeto
var slot: Slot = null
var spot_index := -1
var pose := "em_pe"               # em_pe, deitado, dentro, cochilando
var lifted := false
var busy := false                 # em animação de deslocamento (escorregar, subir)
var move_tween: Tween
var anim_tween: Tween

var _t := 0.0
var _breath_speed := 2.2

# Animação por folha no formato "pet" (uma linha da grade por ação): ver setup_atlas().
var anim_rows := {}               # ação -> {"row", "frames", "ms", "loop"}
var anim_state := ""
var anim_frame := 0
var anim_hold := false            # quadro parado (ex.: olhando numa direção)
var _anim_t := 0.0
var _anim_next := ""
var _atlas_cols := 1
var _atlas_size := Vector2.ZERO


func setup_sprite(tex: Texture2D, display_height: float) -> void:
	sprite = Sprite2D.new()
	sprite.texture = tex
	sprite.centered = false
	sprite.offset = Vector2(-tex.get_width() / 2.0, -tex.get_height())
	var s := display_height / tex.get_height()
	base_art_scale = Vector2(s, s)
	art = sprite
	add_child(sprite)
	_t = randf() * TAU


## Personagem animado por folha de pet: grade `cols` x `rows_count`, quadro `cell`, pés na linha
## `ground_y` do quadro e altura do desenho `char_height` (em pixels do quadro).
## Imagens das ações já carregadas (compartilhadas entre personagens e cenas).
static var _row_tex := {}
var _atlas_dir := ""
var sleep_state := ""             # quadro de olhos fechados usado para dormir
var sleep_frame := 0


## Aceita dois formatos: folha única (data["columns"], "rows_count") ou uma imagem por ação
## (data["rows"][ação]["sheet"]), carregada só quando a ação é usada.
func setup_atlas(tex: Texture2D, data: Dictionary, display_height: float, base_dir: String = "") -> void:
	_atlas_dir = base_dir
	_atlas_cols = int(data.get("columns", 1))
	var cell := Vector2(float(data["cell_width"]), float(data["cell_height"]))
	sprite = Sprite2D.new()
	if tex:
		sprite.texture = tex
		sprite.hframes = _atlas_cols
		sprite.vframes = int(data["rows_count"])
	sprite.centered = false
	sprite.offset = Vector2(-cell.x / 2.0, -float(data["ground_y"]))
	var s := display_height / float(data["char_height"])
	base_art_scale = Vector2(s, s)
	_atlas_size = Vector2(display_height * 0.75, display_height)
	art = sprite
	add_child(sprite)
	anim_rows = data["rows"]
	if data.has("colo"):
		hand_offset = Vector2(0, -float(data["colo"]) * display_height)
	if data.has("sleep"):
		sleep_state = str(data["sleep"]["state"])
		sleep_frame = int(data["sleep"]["frame"])
	_breath_speed = 0.0  # a respiração já está desenhada na linha "idle"
	play_state("idle")
	_anim_t = randf() * 150.0


func has_anim(state: String) -> bool:
	return anim_rows.has(state)


## Toca uma ação da folha. Se `then` for dado, a ação toca uma vez e depois passa para `then`.
func play_state(state: String, then: String = "") -> void:
	if not anim_rows.has(state):
		return
	if state == anim_state and then == "" and not anim_hold:
		return
	anim_state = state
	anim_frame = 0
	anim_hold = false
	_anim_t = 0.0
	var row: Dictionary = anim_rows[state]
	_anim_next = then if then != "" else ("" if bool(row["loop"]) else "idle")
	_apply_frame()


## Mostra um quadro parado de uma ação (usado para olhar numa direção).
func hold_frame(state: String, index: int) -> void:
	if not anim_rows.has(state):
		return
	anim_state = state
	anim_frame = clampi(index, 0, int(anim_rows[state]["frames"]) - 1)
	anim_hold = true
	_anim_next = ""
	_apply_frame()


func _apply_frame() -> void:
	var row: Dictionary = anim_rows[anim_state]
	if row.has("sheet"):
		var path := _atlas_dir.path_join(str(row["sheet"]))
		if not _row_tex.has(path):
			_row_tex[path] = load(path) as Texture2D
		var tex: Texture2D = _row_tex[path]
		if sprite.texture != tex:
			sprite.texture = tex
			sprite.hframes = int(row["frames"])
			sprite.vframes = 1
		sprite.frame = anim_frame
	else:
		sprite.frame = int(row["row"]) * _atlas_cols + anim_frame


## Dormindo: quadro de olhos fechados (personagens com folha de pet).
func sleep() -> void:
	if sleep_state != "":
		hold_frame(sleep_state, sleep_frame)


func _advance_anim(delta: float) -> void:
	if anim_rows.is_empty() or anim_hold or anim_state == "":
		return
	var row: Dictionary = anim_rows[anim_state]
	_anim_t += delta * 1000.0
	while _anim_t >= float(row["ms"]):
		_anim_t -= float(row["ms"])
		anim_frame += 1
		if anim_frame >= int(row["frames"]):
			if _anim_next != "":
				play_state(_anim_next)
				return
			anim_frame = 0
		_apply_frame()


func setup_art(node: Node2D, radius: float) -> void:
	art = node
	hit_radius = radius
	grab_offset = Vector2(0, -radius)
	add_child(node)
	_t = randf() * TAU
	_breath_speed = 0.0


func display_size() -> Vector2:
	if _atlas_size != Vector2.ZERO:
		return _atlas_size
	if sprite:
		return sprite.texture.get_size() * base_art_scale
	return Vector2(hit_radius * 2.0, hit_radius * 2.0)


## Sombra suave nos pés: ajuda a ler onde cada coisa está apoiada no chão.
func _draw() -> void:
	if holder != null or mount != null or pose != "em_pe" or busy:
		return
	var w := display_size().x * (0.32 if is_character else 0.45)
	var a := 0.06 if lifted else 0.13
	draw_colored_polygon(Shapes.ellipse(Vector2.ZERO, Vector2(w, w * 0.16), 24), Color(0.35, 0.15, 0.3, a))


func _process(delta: float) -> void:
	queue_redraw()
	_advance_anim(delta)
	_t += delta * _breath_speed
	var lift := 1.08 if lifted else 1.0
	var b := sin(_t) * 0.012
	art.scale = base_art_scale * squash * Vector2(lift * (1.0 - b * 0.5), lift * (1.0 + b))
	if holder != null:
		# acompanha a mão (ou o colo) e o giro de quem segura: deitada, o objeto deita junto
		global_position = holder.to_global(Vector2(holder.hand_offset.x * holder._facing(),
			holder.hand_offset.y + hit_radius * 0.7))
		rotation = holder.rotation
		z_index = (holder.mount.z_index if holder.mount else holder.z_index) + 1
	elif mount != null:
		# atrás do corpo do cavalo: as pernas somem e o cavaleiro parece sentado na sela
		global_position = mount.seat_global() + Vector2(0, RIDE_DROP)
		z_index = mount.z_index - 1
	elif slot == null and not lifted and not busy:
		z_index = depth_for(global_position.y)


static func depth_for(y: float) -> int:
	return clampi(int(y / 5.0), 0, 400)


func _facing() -> float:
	return -1.0 if (sprite and sprite.flip_h) else 1.0


const RIDE_DROP := 110.0  # pés do cavaleiro abaixo da sela: a cintura fica na sela


func seat_global() -> Vector2:
	return to_global(Vector2(seat_offset.x * _facing(), seat_offset.y))


func hand_global() -> Vector2:
	return to_global(Vector2(hand_offset.x * _facing(), hand_offset.y))


func head_global() -> Vector2:
	return to_global(Vector2(head_offset.x * _facing(), head_offset.y))


func face_left(left: bool) -> void:
	if sprite and flips:
		sprite.flip_h = left


## Toque generoso: alguns pixels de folga ao redor do desenho, pensando em dedos pequenos.
## `slack` = folga em pixels: pequena para tocar, maior para soltar algo em cima.
func hit(p: Vector2, slack: float = 14.0) -> bool:
	if sprite == null:
		var c := to_global(Vector2(0, -hit_radius))
		return c.distance_to(p) <= hit_radius + maxf(10.0, slack)
	var offsets: Array[Vector2] = [Vector2.ZERO]
	for ring in [slack * 0.5, slack]:
		for i in 8:
			offsets.append(Vector2.from_angle(TAU * i / 8.0) * ring)
	for o in offsets:
		var lp := sprite.to_local(p + o)
		if sprite.get_rect().has_point(lp) and sprite.is_pixel_opaque(lp):
			return true
	return false


func kill_move() -> void:
	if move_tween and move_tween.is_valid():
		move_tween.kill()
	move_tween = null


## Começa uma animação nova do desenho (pular, balançar, amassar), cancelando a anterior.
func play_anim() -> Tween:
	if anim_tween and anim_tween.is_valid():
		anim_tween.kill()
	art.position = Vector2.ZERO
	art.rotation = 0.0
	squash = Vector2.ONE
	anim_tween = create_tween()
	return anim_tween


func is_animating() -> bool:
	return anim_tween != null and anim_tween.is_running()
