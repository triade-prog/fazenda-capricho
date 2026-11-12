extends Node
## Captura a Catarina em várias situações, para inspeção visual (não é teste automático).
var main: Node2D
var saida := ""

func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--capturas="):
			saida = a.get_slice("=", 1)
	main = load("res://main.tscn").instantiate()
	add_child(main)
	await get_tree().create_timer(3.4).timeout
	var cat: Toy = main._find("catarina")
	var pel: Toy = main._find("pelucia")
	main.camera_to(cat.global_position.x)
	# 1) segurando a pelúcia, parada
	main._attach(pel, cat)
	await _foto("p1_segura_parada", cat)
	# 2) segurando, arrastada com o dedo para a direita (correndo)
	var sp: Vector2 = main.world_to_screen(cat.global_position + Vector2(0, -150))
	_toque(sp, true)
	await get_tree().process_frame
	for i in 10:
		_arrasto(sp + Vector2(12 * (i + 1), 0))
		await get_tree().process_frame
	await _foto("p2_correndo_segurando", cat)
	for i in 10:
		_arrasto(sp + Vector2(120 - 12 * (i + 1), 0))
		await get_tree().process_frame
	await _foto("p3_correndo_esquerda", cat)
	_toque(sp, false)
	await get_tree().create_timer(0.8).timeout
	# 4) acenando segurando
	cat.play_state("waving", "idle")
	await get_tree().create_timer(0.3).timeout
	await _foto("p4_acenando", cat)
	await get_tree().create_timer(0.6).timeout
	# 5) failed
	cat.play_state("failed", "idle")
	await get_tree().create_timer(0.5).timeout
	await _foto("p5_failed", cat)
	await get_tree().create_timer(1.0).timeout
	# 6) olhando para objeto arrastado (cima-esquerda)
	var alm: Toy = main._find("almofada")
	var sa: Vector2 = main.world_to_screen(alm.global_position + Vector2(0, -36))
	_toque(sa, true)
	await get_tree().process_frame
	var alvo: Vector2 = main.world_to_screen(cat.head_global() + Vector2(-260, -200))
	for i in 10:
		_arrasto(sa.lerp(alvo, (i + 1) / 10.0))
		await get_tree().process_frame
	await _foto("p6_olhando", cat)
	_toque(alvo, false)
	await get_tree().create_timer(0.6).timeout
	# 7) deitada
	for s in main.slots:
		if s.id == "cama":
			main._enter_slot(cat, s)
	await get_tree().create_timer(0.6).timeout
	main.camera_to(300)
	await _foto("p7_deitada", cat)
	# 8) montada
	main._leave_slot(cat)
	cat.pose = "em_pe"
	var lumi: Toy = main._find("lumi")
	main._mount(cat, lumi)
	await get_tree().create_timer(0.5).timeout
	main.camera_to(lumi.global_position.x)
	await _foto("p8_montada", cat)
	get_tree().quit()

func _toque(p: Vector2, on: bool) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 0
	e.position = p
	e.pressed = on
	main._unhandled_input(e)


func _arrasto(p: Vector2) -> void:
	var e := InputEventScreenDrag.new()
	e.index = 0
	e.position = p
	main._unhandled_input(e)


func _foto(nome: String, alvo: Toy) -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(saida.path_join(nome + ".png"))
