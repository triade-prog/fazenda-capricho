extends Node
## Roteiro automático do P-0: simula toques e confere cada interação.
## Rodar:  godot --path prototipo res://testes/roteiro.tscn -- --capturas=/caminho/da/pasta
## Sem --capturas, só confere (funciona também com --headless).

var main: Node2D
var falhas := 0
var capturas := ""


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--capturas="):
			capturas = a.get_slice("=", 1)
	main = load("res://main.tscn").instantiate()
	add_child(main)
	await _espera(0.5)
	await _roteiro()
	print("RESULTADO: ", "OK" if falhas == 0 else "%d FALHA(S)" % falhas)
	get_tree().quit(1 if falhas else 0)


func _roteiro() -> void:
	var cat: Toy = main._find("catarina")
	var bob: Toy = main._find("bob")
	await _foto("01_inicio")

	await _arrasta(Vector2(480, 660), Vector2(720, 600))
	_confere(cat.held_item != null and cat.held_item.kind == "pelucia", "Catarina segura a pelúcia")
	await _foto("02_segura_pelucia")

	await _arrasta(Vector2(1330, 532), Vector2(720, 600))
	_confere(cat.held_item != null and cat.held_item.kind == "biscoito", "troca: Catarina segura o biscoito")

	await _arrasta(Vector2(720, 600), Vector2(1060, 690), 0.25)
	await _foto("03_bob_come")
	await _espera(0.6)
	_confere(main._count("biscoito") == 0, "Bob comeu o biscoito da mão da Catarina")
	_confere(cat.held_item == null, "mão da Catarina ficou livre")

	await _toca(Vector2(1414, 515))
	await _espera(0.8)
	_confere(main._count("biscoito") == 1, "pote de biscoitos deu um biscoito")

	var p := cat.global_position + Vector2(0, -150)
	await _arrasta(p, Vector2(300, 200))
	_confere(cat.pose == "deitado", "Catarina deitou no beliche")
	p = bob.global_position + Vector2(0, -85)
	await _arrasta(p, Vector2(330, 200))
	_confere(bob.pose == "deitado", "Bob deitou junto")
	await _espera(1.2)
	await _foto("04_dormindo_juntos")

	await _arrasta(cat.to_global(Vector2(0, -150)), Vector2(340, 540))
	_confere(cat.pose == "dentro" and main.castle.is_open, "Catarina entrou no castelinho e a porta abriu")
	await _foto("05_castelinho_aberto")
	await _toca(Vector2(410, 520))
	_confere(not main.castle.is_open, "portinha fechou")
	_confere(main._toy_at(Vector2(340, 520), []) != cat, "com a porta fechada, Catarina fica escondida")
	await _foto("06_castelinho_fechado")
	await _toca(Vector2(340, 520))
	_confere(main.castle.is_open, "portinha abriu de novo")

	await _arrasta(cat.to_global(Vector2(0, -130)), Vector2(580, 250), 0.1)
	await _espera(0.55)
	await _foto("07_escorregador")
	await _espera(1.2)
	_confere(not cat.busy and cat.global_position.y > 600.0, "desceu o escorregador e chegou ao chão")

	await _arrasta(cat.to_global(Vector2(0, -150)), Vector2(75, 450), 0.1)
	await _espera(0.7)
	await _foto("08_escada")
	await _espera(1.4)
	_confere(cat.pose == "deitado", "subiu a escada e deitou na cama")

	p = bob.to_global(Vector2(0, -85))
	await _arrasta(p, Vector2(1000, 700))
	await _espera(0.5)
	var escova: Toy = main._find("escova")
	await _arrasta(escova.global_position + Vector2(0, -20), bob.global_position + Vector2(0, -80), 0.15)
	await _foto("09_escovando")
	await _espera(1.6)
	var almofada: Toy = main._find("almofada")
	await _arrasta(almofada.global_position + Vector2(0, -36), bob.global_position + Vector2(0, -80))
	_confere(bob.pose == "cochilando", "Bob cochilou na almofada")
	await _espera(1.2)
	await _foto("10_cochilo")
	await _espera(3.5)
	_confere(bob.pose == "em_pe", "Bob acordou do cochilo")

	await _toca(bob.global_position + Vector2(0, -85))
	await _espera(0.3)
	await _foto("11_toque_bob")


# ---------------------------------------------------------------- utilidades

func _confere(ok: bool, o_que: String) -> void:
	print(("  ok    " if ok else "  FALHA ") + o_que)
	if not ok:
		falhas += 1


func _espera(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _evento_toque(pos: Vector2, pressed: bool) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 0
	e.position = pos
	e.pressed = pressed
	main._unhandled_input(e)


func _toca(pos: Vector2) -> void:
	_evento_toque(pos, true)
	await get_tree().process_frame
	_evento_toque(pos, false)
	await _espera(0.35)


func _arrasta(de: Vector2, para: Vector2, espera_final: float = 0.6) -> void:
	_evento_toque(de, true)
	await get_tree().process_frame
	var passos := 12
	for i in range(1, passos + 1):
		var d := InputEventScreenDrag.new()
		d.index = 0
		d.position = de.lerp(para, float(i) / passos)
		main._unhandled_input(d)
		await get_tree().process_frame
	_evento_toque(para, false)
	await _espera(espera_final)


func _foto(nome: String) -> void:
	if capturas.is_empty():
		return
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(capturas.path_join(nome + ".png"))
