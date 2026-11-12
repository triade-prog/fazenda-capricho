extends Node2D
## Quarto rosa da Catarina (desenho provisório por código): parede, piso, janela com vista da
## fazenda, beliche de coração, escada, escorregador, interior do castelinho e pote de biscoitos.
## A frente do castelinho (com a portinha roxa) fica em castle_front.gd, porque precisa ficar
## na frente de quem entra nele.

const OUTLINE := Color("#5a3a4a")
const WOOD := Color("#d79a62")
const PINK := Color("#ff8fbf")
const LIGHT_PINK := Color("#ffe3ef")
const PURPLE := Color("#b57be0")

const FLOOR_Y := 600.0
const SLIDE_P0 := Vector2(560, 300)
const SLIDE_P1 := Vector2(650, 590)
const SLIDE_P2 := Vector2(830, 612)


func _ready() -> void:
	z_index = -100


func _draw() -> void:
	_wall()
	_window()
	_floor()
	_rug()
	_table_and_jar()
	_bunk_bed()
	_ladder()
	_slide()


func _rect(r: Rect2, col: Color, outline := true) -> void:
	draw_rect(r, col)
	if outline:
		draw_rect(r, OUTLINE, false, 4.0)


func _wall() -> void:
	draw_rect(Rect2(0, 0, 1600, FLOOR_Y), Color("#ffd6e8"))
	for x in range(0, 1600, 80):
		draw_rect(Rect2(x, 0, 36, FLOOR_Y), Color("#ffe0ee"))
	# varal de coraçõezinhos
	var pts := PackedVector2Array()
	for i in 33:
		var x := i * 50.0
		pts.append(Vector2(x, 40 + sin(i * 0.5) * 10.0))
	draw_polyline(pts, Color("#c98bb0"), 2.0, true)
	for i in range(1, 32, 2):
		var col := PINK if i % 4 == 1 else PURPLE
		draw_colored_polygon(Shapes.heart(11, pts[i] + Vector2(0, 14)), col)
	draw_rect(Rect2(0, FLOOR_Y - 14, 1600, 14), Color("#f7a8c8"))


func _window() -> void:
	var w := Rect2(990, 120, 260, 230)
	draw_rect(w, Color("#bfe6ff"))
	draw_circle(Vector2(1200, 170), 26, Color("#fff3a0"))
	var clip := PackedVector2Array([w.position, Vector2(w.end.x, w.position.y), w.end, Vector2(w.position.x, w.end.y)])
	for hill in [[Vector2(1080, 360), Vector2(170, 80), Color("#9be08f")], [Vector2(1230, 370), Vector2(130, 70), Color("#82d47a")]]:
		for part in Geometry2D.intersect_polygons(Shapes.ellipse(hill[0], hill[1]), clip):
			draw_colored_polygon(part, hill[2])
	for p in [Vector2(1020, 315), Vector2(1060, 300), Vector2(1110, 310), Vector2(1170, 318), Vector2(1215, 306)]:
		draw_circle(p, 6, Color("#ff9ac8"))
		draw_circle(p, 2.5, Color("#fff3a0"))
	# arvorezinha rosa da fazenda
	draw_rect(Rect2(1135, 250, 10, 50), WOOD)
	draw_circle(Vector2(1140, 240), 26, Color("#ff9ac8"))
	draw_rect(w, Color.WHITE, false, 14.0)
	draw_line(Vector2(1120, 120), Vector2(1120, 350), Color.WHITE, 8.0)
	draw_line(Vector2(990, 235), Vector2(1250, 235), Color.WHITE, 8.0)
	draw_rect(w.grow(7), OUTLINE, false, 3.0)
	# cortinas
	for x0: float in [950.0, 1230.0]:
		var pts := PackedVector2Array([Vector2(x0, 100), Vector2(x0 + 60, 100), Vector2(x0 + 40, 250), Vector2(x0 + 30, 380), Vector2(x0, 380)])
		draw_colored_polygon(pts, PURPLE)
		draw_polyline(Shapes.closed(pts), OUTLINE, 3.0, true)
	draw_rect(Rect2(950, 92, 340, 12), WOOD)


func _floor() -> void:
	draw_rect(Rect2(0, FLOOR_Y, 1600, 300), Color("#f3cfa6"))
	var y := FLOOR_Y + 30.0
	var gap := 34.0
	while y < 900:
		draw_line(Vector2(0, y), Vector2(1600, y), Color("#e3b98c"), 2.0)
		gap *= 1.12
		y += gap


func _rug() -> void:
	draw_colored_polygon(Shapes.ellipse(Vector2(1000, 770), Vector2(340, 95)), Color("#c9a7f5"))
	draw_colored_polygon(Shapes.ellipse(Vector2(1000, 770), Vector2(290, 72)), Color("#dcc4fa"))
	draw_polyline(Shapes.closed(Shapes.ellipse(Vector2(1000, 770), Vector2(340, 95))), OUTLINE, 3.0, true)
	for i in 8:
		var a := TAU * i / 8.0
		draw_colored_polygon(Shapes.heart(10, Vector2(1000, 770) + Vector2(cos(a) * 230, sin(a) * 52)), Color.WHITE)


func _table_and_jar() -> void:
	# mesinha
	_rect(Rect2(1300, 572, 14, 80), WOOD)
	_rect(Rect2(1476, 572, 14, 80), WOOD)
	_rect(Rect2(1280, 556, 230, 20), Color("#e9b07a"))
	# pote de biscoitos (tocar para ganhar um biscoito)
	var jar := Rect2(1368, 478, 92, 78)
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.82, 0.93, 1.0, 0.85)
	sb.set_corner_radius_all(18)
	sb.border_color = OUTLINE
	sb.set_border_width_all(4)
	draw_style_box(sb, jar)
	for p in [Vector2(1392, 530), Vector2(1430, 522), Vector2(1412, 542)]:
		draw_colored_polygon(Shapes.heart(13, p), Color("#e9a55f"))
	_rect(Rect2(1376, 464, 76, 16), PINK)
	draw_circle(Vector2(1414, 460), 7, PURPLE)


func _bunk_bed() -> void:
	# interior do castelinho (aparece pela porta aberta)
	draw_rect(Rect2(120, 330, 420, 270), Color("#c46b98"))
	draw_colored_polygon(Shapes.heart(28, Vector2(240, 430)), Color("#d988b0"))
	draw_colored_polygon(Shapes.heart(28, Vector2(440, 430)), Color("#d988b0"))
	# colunas
	_rect(Rect2(98, 150, 22, 452), PINK)
	_rect(Rect2(540, 230, 22, 372), PINK)
	# cabeceira de coração
	var hb := Shapes.heart(70, Vector2(170, 205))
	draw_colored_polygon(hb, PINK)
	draw_polyline(Shapes.closed(hb), OUTLINE, 4.0, true)
	draw_colored_polygon(Shapes.heart(40, Vector2(170, 202)), Color("#ffb3d1"))
	# base e colchão da cama de cima
	_rect(Rect2(98, 300, 464, 34), PINK)
	_rect(Rect2(112, 268, 436, 34), Color("#fff0f6"))
	for x in range(130, 540, 60):
		draw_colored_polygon(Shapes.heart(8, Vector2(x + 20, 288)), Color("#ffb3d1"))
	# travesseiro
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color.WHITE
	sb.set_corner_radius_all(14)
	sb.border_color = OUTLINE
	sb.set_border_width_all(3)
	draw_style_box(sb, Rect2(124, 244, 84, 30))


func _ladder() -> void:
	draw_rect(Rect2(56, 290, 10, 312), WOOD)
	draw_rect(Rect2(92, 290, 10, 312), WOOD)
	draw_rect(Rect2(56, 290, 10, 312), OUTLINE, false, 2.0)
	draw_rect(Rect2(92, 290, 10, 312), OUTLINE, false, 2.0)
	var y := 320.0
	while y < 600:
		draw_line(Vector2(60, y), Vector2(98, y), Color("#b97a4b"), 7.0)
		y += 44.0


func _slide() -> void:
	var pts := PackedVector2Array()
	for i in 25:
		pts.append(Shapes.bezier(SLIDE_P0, SLIDE_P1, SLIDE_P2, i / 24.0))
	draw_polyline(pts, OUTLINE, 44.0, true)
	draw_polyline(pts, PURPLE, 36.0, true)
	var edge := PackedVector2Array()
	for p in pts:
		edge.append(p + Vector2(0, -12))
	draw_polyline(edge, Color("#ffb3d1"), 8.0, true)
	draw_circle(SLIDE_P2, 18, PURPLE)
