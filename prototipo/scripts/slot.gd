class_name Slot
extends Node2D
## Lugar interativo onde um personagem se encaixa ao ser solto: cama, castelinho,
## escorregador, escada. Brilha quando o personagem arrastado está por cima.

var id := ""
var area := Rect2()               # região (em coordenadas da tela) que aceita o soltar
var spots: Array[Vector2] = []    # pontos onde os personagens ficam (pés)
var occupants: Array = []
var pose := ""                    # "deitar", "dentro" ou "" para lugares de ação
var action := ""                  # "escorregar", "subir" ou "" para lugares de ficar
var depth := 0                    # z_index de quem está no lugar
var highlight := false:
	set(v):
		if v != highlight:
			highlight = v
			queue_redraw()


func setup(p_id: String, p_area: Rect2, p_spots: Array, p_pose: String, p_action: String, p_depth: int) -> Slot:
	id = p_id
	area = p_area
	spots.assign(p_spots)
	occupants.resize(spots.size())
	occupants.fill(null)
	pose = p_pose
	action = p_action
	depth = p_depth
	z_index = 380
	return self


func accepts(t: Toy) -> bool:
	return t.is_character and not (id in t.too_big_for) and (action != "" or free_spot() >= 0)


func free_spot() -> int:
	for i in spots.size():
		if occupants[i] == null:
			return i
	return -1


func _draw() -> void:
	if not highlight:
		return
	var c := area.get_center()
	var r := maxf(area.size.x, area.size.y) * 0.55
	draw_circle(c, r, Color(1.0, 1.0, 0.75, 0.28))
	draw_arc(c, r, 0.0, TAU, 64, Color(1.0, 0.95, 0.5, 0.9), 5.0, true)
