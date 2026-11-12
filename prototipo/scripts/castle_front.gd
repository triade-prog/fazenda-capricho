class_name CastleFront
extends Node2D
## Frente do castelinho de ursinhos (embaixo do beliche), com a portinha roxa.
## Fica na frente de quem está dentro do castelo: com a porta fechada, quem entrou some.

const OUTLINE := Color("#5a3a4a")
const WALL := Color("#ffb3d1")
const DOOR := Color("#9b59d0")
const DOOR_CENTER := Vector2(340, 470)   # centro do arco da porta
const DOOR_R := 46.0
const BASE_Y := 600.0

var is_open := false


func _ready() -> void:
	z_index = Toy.depth_for(BASE_Y)


func set_open(v: bool) -> void:
	if v == is_open:
		return
	is_open = v
	queue_redraw()


func toggle() -> void:
	set_open(not is_open)


## Área de toque da porta: fechada = a própria porta; aberta = a folha da porta, ao lado.
func door_hit(p: Vector2) -> bool:
	var closed := Rect2(DOOR_CENTER.x - DOOR_R, DOOR_CENTER.y - DOOR_R, DOOR_R * 2.0, BASE_Y - DOOR_CENTER.y + DOOR_R)
	if is_open:
		return Rect2(closed.end.x - 4, closed.position.y, 46, closed.size.y).has_point(p)
	return closed.has_point(p)


func _draw() -> void:
	var l := DOOR_CENTER.x - DOOR_R
	var r := DOOR_CENTER.x + DOOR_R
	# paredes ao redor da abertura
	draw_rect(Rect2(120, 334, l - 120, BASE_Y - 334), WALL)
	draw_rect(Rect2(r, 334, 540 - r, BASE_Y - 334), WALL)
	var top := PackedVector2Array([Vector2(l, 334), Vector2(r, 334), Vector2(r, DOOR_CENTER.y)])
	for i in range(1, 16):
		var a := -PI * i / 16.0
		top.append(DOOR_CENTER + Vector2(cos(a), sin(a)) * DOOR_R)
	top.append(Vector2(l, DOOR_CENTER.y))
	draw_colored_polygon(top, WALL)
	# ameias
	for x in range(130, 540, 52):
		draw_rect(Rect2(x, 334, 26, 14), Color("#ff9ac4"))
	# contorno do castelo e da abertura
	draw_rect(Rect2(120, 334, 420, BASE_Y - 334), OUTLINE, false, 4.0)
	draw_arc(DOOR_CENTER, DOOR_R, PI, TAU, 24, OUTLINE, 4.0, true)
	draw_line(Vector2(l, DOOR_CENTER.y), Vector2(l, BASE_Y), OUTLINE, 4.0)
	draw_line(Vector2(r, DOOR_CENTER.y), Vector2(r, BASE_Y), OUTLINE, 4.0)
	# almofadas de ursinho na parede
	_bear(Vector2(205, 470))
	_bear(Vector2(470, 470))
	# portinha roxa
	if is_open:
		var leaf := PackedVector2Array([Vector2(r, DOOR_CENTER.y - DOOR_R), Vector2(r + 38, DOOR_CENTER.y - DOOR_R + 14), Vector2(r + 38, BASE_Y - 6), Vector2(r, BASE_Y)])
		draw_colored_polygon(leaf, DOOR)
		draw_polyline(Shapes.closed(leaf), OUTLINE, 3.0, true)
		draw_circle(Vector2(r + 28, 540), 5, Color("#ffd84d"))
	else:
		draw_circle(DOOR_CENTER, DOOR_R, DOOR)
		draw_rect(Rect2(l, DOOR_CENTER.y, DOOR_R * 2.0, BASE_Y - DOOR_CENTER.y), DOOR)
		draw_arc(DOOR_CENTER, DOOR_R, PI, TAU, 24, OUTLINE, 4.0, true)
		draw_colored_polygon(Shapes.heart(16, DOOR_CENTER + Vector2(0, 4)), Color("#e8c8ff"))
		draw_circle(Vector2(r - 14, 540), 6, Color("#ffd84d"))
		draw_arc(Vector2(r - 14, 540), 6, 0, TAU, 16, OUTLINE, 2.0, true)


func _bear(c: Vector2) -> void:
	var brown := Color("#c98b5c")
	for e in [c + Vector2(-26, -28), c + Vector2(26, -28)]:
		draw_circle(e, 15, brown)
		draw_arc(e, 15, 0, TAU, 20, OUTLINE, 3.0, true)
	draw_circle(c, 38, brown)
	draw_arc(c, 38, 0, TAU, 32, OUTLINE, 3.0, true)
	draw_colored_polygon(Shapes.ellipse(c + Vector2(0, 12), Vector2(16, 12)), Color("#efd0b0"))
	draw_circle(c + Vector2(-13, -6), 4, OUTLINE)
	draw_circle(c + Vector2(13, -6), 4, OUTLINE)
	draw_circle(c + Vector2(0, 8), 4.5, OUTLINE)
