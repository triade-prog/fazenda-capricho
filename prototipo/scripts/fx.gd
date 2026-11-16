class_name FxShape
extends Node2D
## Efeitos de feedback: coraçõezinhos, estrelinhas de brilho.

var kind := "coracao"
var color := Color("#ff6fa8")
var size := 14.0


func _init(p_kind: String = "coracao", p_color: Color = Color(1.0, 0.44, 0.66), p_size: float = 14.0) -> void:
	kind = p_kind
	color = p_color
	size = p_size
	z_index = 420


func _draw() -> void:
	match kind:
		"coracao":
			draw_colored_polygon(Shapes.heart(size), color)
		"estrela":
			draw_colored_polygon(Shapes.star(size), color)
		"nao":  # bolinha com um X: "não deu"
			draw_circle(Vector2.ZERO, size, Color.WHITE)
			draw_arc(Vector2.ZERO, size, 0.0, TAU, 32, color, size * 0.22, true)
			var k := size * 0.45
			draw_line(Vector2(-k, -k), Vector2(k, k), color, size * 0.24, true)
			draw_line(Vector2(-k, k), Vector2(k, -k), color, size * 0.24, true)
