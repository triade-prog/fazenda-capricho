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


func setup_art(node: Node2D, radius: float) -> void:
	art = node
	hit_radius = radius
	grab_offset = Vector2(0, -radius)
	add_child(node)
	_t = randf() * TAU
	_breath_speed = 0.0


func display_size() -> Vector2:
	if sprite:
		return sprite.texture.get_size() * base_art_scale
	return Vector2(hit_radius * 2.0, hit_radius * 2.0)


func _process(delta: float) -> void:
	_t += delta * _breath_speed
	var lift := 1.08 if lifted else 1.0
	var b := sin(_t) * 0.012
	art.scale = base_art_scale * squash * Vector2(lift * (1.0 - b * 0.5), lift * (1.0 + b))
	if holder != null:
		global_position = holder.hand_global() + Vector2(0, hit_radius * 0.7)
		z_index = holder.z_index + 1
	elif slot == null and not lifted and not busy:
		z_index = depth_for(global_position.y)


static func depth_for(y: float) -> int:
	return clampi(int(y / 5.0), 0, 400)


func _facing() -> float:
	return -1.0 if (sprite and sprite.flip_h) else 1.0


func hand_global() -> Vector2:
	return to_global(Vector2(hand_offset.x * _facing(), hand_offset.y))


func head_global() -> Vector2:
	return to_global(Vector2(head_offset.x * _facing(), head_offset.y))


func face_left(left: bool) -> void:
	if sprite and flips:
		sprite.flip_h = left


## Toque generoso: alguns pixels de folga ao redor do desenho, pensando em dedos pequenos.
func hit(p: Vector2) -> bool:
	if sprite == null:
		var c := to_global(Vector2(0, -hit_radius))
		return c.distance_to(p) <= hit_radius + 10.0
	for o in [Vector2.ZERO, Vector2(14, 0), Vector2(-14, 0), Vector2(0, 14), Vector2(0, -14)]:
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
