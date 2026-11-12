class_name ItemArt
extends Node2D
## Desenho provisório dos objetos do P-0 (feito por código, sem arquivos de arte).
## Origem na base do objeto. Será trocado pela arte final sem mudar a programação.

const OUTLINE := Color("#5a3a4a")

var kind := ""
var r := 40.0


func _init(p_kind: String = "", p_radius: float = 40.0) -> void:
	kind = p_kind
	r = p_radius


## Caixa (largura, altura) de cada objeto na arte final, em pixels do jogo.
const CAIXA := {"biscoito": Vector2(56, 56), "pelucia": Vector2(90, 104), "escova": Vector2(96, 60),
	"almofada": Vector2(92, 70)}


func _draw() -> void:
	if CAIXA.has(kind):
		var c: Vector2 = CAIXA[kind]
		if Arte.draw(self, "objeto_" + kind, Rect2(-c.x / 2.0, -c.y, c.x, c.y)):
			return
	match kind:
		"biscoito":
			_biscoito()
		"pelucia":
			_pelucia()
		"escova":
			_escova()
		"almofada":
			_almofada()


func _fill(pts: PackedVector2Array, col: Color, w: float = 4.0) -> void:
	draw_colored_polygon(pts, col)
	draw_polyline(Shapes.closed(pts), OUTLINE, w, true)


func _round_rect(rect: Rect2, col: Color, radius: int) -> void:
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(radius)
	sb.border_color = OUTLINE
	sb.set_border_width_all(4)
	sb.anti_aliasing = true
	draw_style_box(sb, rect)


func _biscoito() -> void:
	var c := Vector2(0, -r * 0.9)
	_fill(Shapes.heart(r, c), Color("#e9a55f"))
	draw_colored_polygon(Shapes.heart(r * 0.7, c + Vector2(0, -2)), Color("#f6c27f"))
	for p in [Vector2(-10, -8), Vector2(9, -12), Vector2(0, 6), Vector2(-14, 8), Vector2(13, 4)]:
		draw_circle(c + p * (r / 34.0), 3.0, Color("#ff6fa8"))


func _pelucia() -> void:
	var brown := Color("#b97a4b")
	var light := Color("#e8c19a")
	var body := Vector2(0, -r * 0.55)
	var head := Vector2(0, -r * 1.35)
	for e in [Vector2(-r * 0.45, -r * 1.75), Vector2(r * 0.45, -r * 1.75)]:
		draw_circle(e, r * 0.22, brown)
		draw_arc(e, r * 0.22, 0, TAU, 24, OUTLINE, 3.0, true)
		draw_circle(e, r * 0.11, light)
	_fill(Shapes.ellipse(body, Vector2(r * 0.62, r * 0.55)), brown)
	draw_colored_polygon(Shapes.ellipse(body + Vector2(0, 4), Vector2(r * 0.35, r * 0.32)), light)
	_fill(Shapes.ellipse(head, Vector2(r * 0.55, r * 0.48)), brown)
	draw_colored_polygon(Shapes.ellipse(head + Vector2(0, r * 0.14), Vector2(r * 0.25, r * 0.18)), light)
	draw_circle(head + Vector2(-r * 0.2, -r * 0.08), 3.5, OUTLINE)
	draw_circle(head + Vector2(r * 0.2, -r * 0.08), 3.5, OUTLINE)
	draw_circle(head + Vector2(0, r * 0.08), 4.0, OUTLINE)
	draw_colored_polygon(Shapes.heart(r * 0.2, body + Vector2(0, -2)), Color("#ff6fa8"))


func _escova() -> void:
	# cerdas brancas embaixo, cabeça roxa, cabo rosa com coração
	for i in 7:
		var x := r * 0.08 + i * r * 0.13
		draw_line(Vector2(x, -r * 0.42), Vector2(x, -r * 0.04), Color("#fff6fb"), 6.0, true)
		draw_line(Vector2(x, -r * 0.08), Vector2(x, -r * 0.02), OUTLINE, 6.0, true)
	_round_rect(Rect2(-r * 0.05, -r * 0.95, r * 1.05, r * 0.55), Color("#9b59d0"), 12)
	_round_rect(Rect2(-r * 1.0, -r * 0.82, r * 1.0, r * 0.32), Color("#ff8fbf"), 12)
	draw_colored_polygon(Shapes.heart(r * 0.18, Vector2(-r * 0.55, -r * 0.66)), Color.WHITE)
	draw_colored_polygon(Shapes.heart(r * 0.2, Vector2(r * 0.47, -r * 0.68)), Color("#e8c8ff"))


func _almofada() -> void:
	var c := Vector2(0, -r * 0.55)
	var pink := Color("#ffb3d1")
	for e in [Vector2(-r * 0.62, -r * 0.95), Vector2(r * 0.62, -r * 0.95)]:
		draw_circle(e, r * 0.24, pink)
		draw_arc(e, r * 0.24, 0, TAU, 24, OUTLINE, 3.0, true)
	_round_rect(Rect2(c.x - r, c.y - r * 0.5, r * 2.0, r * 1.0), pink, 26)
	draw_circle(c + Vector2(-r * 0.3, -r * 0.05), 4.0, OUTLINE)
	draw_circle(c + Vector2(r * 0.3, -r * 0.05), 4.0, OUTLINE)
	draw_colored_polygon(Shapes.ellipse(c + Vector2(0, r * 0.18), Vector2(r * 0.2, r * 0.12)), Color("#ffe3ef"))
	draw_circle(c + Vector2(0, r * 0.13), 3.5, OUTLINE)
