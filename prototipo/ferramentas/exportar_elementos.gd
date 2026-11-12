extends Node
## Exporta cada elemento do quarto e cada objeto como PNG separado, com fundo transparente,
## para servir de referência na geração da arte final (3D).
##
## Rodar (precisa de tela; num servidor, use xvfb-run):
##   godot --path prototipo --rendering-driver opengl3 res://ferramentas/exportar_elementos.tscn -- --saida=/pasta

const RoomScript := preload("res://scripts/room.gd")
const MARGEM := 12

## nome do arquivo, tipo, função de desenho, retângulo no quarto (coordenadas do jogo), escala
const ELEMENTOS := [
	["beliche", "quarto", "_bunk_bed", Rect2(90, 100, 480, 510), 2.0],
	["castelo_interior", "quarto", "_castle_interior", Rect2(110, 320, 440, 290), 2.0],
	["castelo_frente_porta_fechada", "castelo", "fechado", Rect2(110, 290, 440, 320), 2.0],
	["castelo_frente_porta_aberta", "castelo", "aberto", Rect2(110, 290, 440, 320), 2.0],
	["escada", "quarto", "_ladder", Rect2(45, 280, 70, 330), 2.0],
	["escorregador", "quarto", "_slide", Rect2(520, 260, 350, 380), 2.0],
	["tapete", "quarto", "_rug", Rect2(650, 665, 700, 210), 2.0],
	["janela", "quarto", "_window", Rect2(930, 80, 380, 310), 2.0],
	["porta", "quarto", "_door", Rect2(1625, 240, 200, 370), 2.0],
	["quadro_ferradura", "quarto", "_picture", Rect2(1895, 150, 215, 190), 2.0],
	["mesinha", "quarto", "_table", Rect2(1272, 548, 245, 110), 2.0],
	["pote_biscoitos", "quarto", "_jar", Rect2(1355, 445, 120, 120), 2.0],
	["varal_coracoes", "quarto", "_garland", Rect2(0, 20, 2200, 60), 1.0],
	["parede", "quarto", "_wall", Rect2(0, 0, 2200, 600), 1.0],
	["piso", "quarto", "_floor", Rect2(0, 600, 2200, 300), 1.0],
]
const OBJETOS := [["biscoito", 26.0], ["pelucia", 40.0], ["escova", 46.0], ["almofada", 42.0]]

var saida := "user://elementos"
var vp: SubViewport


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--saida="):
			saida = a.get_slice("=", 1)
	DirAccess.make_dir_recursive_absolute(saida)
	vp = SubViewport.new()
	vp.size = Vector2i(2300, 1300)
	vp.transparent_bg = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(vp)
	for e in ELEMENTOS:
		var no: Node2D
		if e[1] == "castelo":
			var c := CastleFront.new()
			c.is_open = e[2] == "aberto"
			no = c
		else:
			var r := RoomScript.new()
			r.only = e[2]
			no = r
		await _exportar(no, e[3], e[4], e[0])
	for o in OBJETOS:
		var art := ItemArt.new(o[0], o[1])
		var holder := Node2D.new()
		holder.add_child(art)
		art.position = Vector2(o[1] * 1.2, o[1] * 2.2)
		await _exportar(holder, Rect2(0, 0, o[1] * 2.4, o[1] * 2.4), 4.0, "objeto_" + o[0])
	await _quarto_completo()
	print("Elementos exportados em ", ProjectSettings.globalize_path(saida))
	get_tree().quit()


func _exportar(no: Node2D, area: Rect2, escala: float, nome: String) -> void:
	no.scale = Vector2(escala, escala)
	no.position = -area.position * escala + Vector2(MARGEM, MARGEM)
	vp.add_child(no)
	no.z_index = 0
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var img := vp.get_texture().get_image()
	var usado := img.get_used_rect()
	if usado.size.x > 0:
		img = img.get_region(usado.grow(MARGEM).intersection(Rect2i(Vector2i.ZERO, img.get_size())))
	img.save_png(saida.path_join(nome + ".png"))
	print("  ", nome, "  ", img.get_width(), "x", img.get_height())
	no.queue_free()
	await get_tree().process_frame


## O quarto inteiro (2200 x 900) com todos os personagens na escala do jogo: referência de tamanho.
func _quarto_completo() -> void:
	var v := SubViewport.new()
	v.size = Vector2i(2200, 900)
	v.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(v)
	var jogo: Node2D = load("res://main.tscn").instantiate()
	v.add_child(jogo)
	await get_tree().create_timer(3.4).timeout  # espera a logo de abertura sumir
	for t in jogo.toys:
		t.play_state("idle")
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	v.get_texture().get_image().save_png(saida.path_join("referencia_quarto_completo.png"))
	print("  referencia_quarto_completo  2200x900")
