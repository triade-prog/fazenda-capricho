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

	await _arrasta(Vector2(480, 660), Vector2(720, 560))
	_confere(cat.held_item != null and cat.held_item.kind == "pelucia", "Catarina segura a pelúcia")
	await _foto("02_segura_pelucia")

	var x0: float = main.cam.position.x
	await _mostra(1400.0)
	_confere(main.cam.position.x > x0 + 100.0, "gesto no espaço vazio rola o quarto")
	await _foto("02b_quarto_rolado")
	await _arrasta(Vector2(1330, 532), Vector2(720, 560))
	_confere(cat.held_item != null and cat.held_item.kind == "biscoito", "troca: Catarina segura o biscoito")

	await _arrasta(cat.global_position + Vector2(0, -150), Vector2(1060, 660), 0.25)
	await _foto("03_bob_come")
	await _espera(0.6)
	_confere(main._count("biscoito") == 0, "Bob comeu o biscoito da mão da Catarina")
	_confere(cat.held_item == null, "mão da Catarina ficou livre")

	await _toca(Vector2(1414, 515))
	await _espera(0.8)
	_confere(main._count("biscoito") == 1, "pote de biscoitos deu um biscoito")

	main.camera_to(1600.0)
	await _espera(0.2)
	var cam_antes: float = main.cam.position.x
	var p := cat.global_position + Vector2(0, -150)
	await _arrasta(p, Vector2(300, 200))
	_confere(main.cam.position.x < cam_antes - 100.0, "levar a Catarina até a borda rola o quarto")
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
# Todos os toques são enviados em coordenadas de TELA, como um dedo de verdade no iPad.
# Se o destino está fora da tela, o dedo vai até a borda e espera o quarto rolar.

func _confere(ok: bool, o_que: String) -> void:
	print(("  ok    " if ok else "  FALHA ") + o_que)
	if not ok:
		falhas += 1


func _espera(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _vis() -> Vector2:
	return get_viewport().get_visible_rect().size


func _na_tela(wp: Vector2, margem: float = 150.0) -> bool:
	var sp: Vector2 = main.world_to_screen(wp)
	return sp.x > margem and sp.x < _vis().x - margem


func _evento(sp: Vector2, pressed: bool) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 0
	e.position = sp
	e.pressed = pressed
	main._unhandled_input(e)


func _move(sp: Vector2) -> void:
	var d := InputEventScreenDrag.new()
	d.index = 0
	d.position = sp
	main._unhandled_input(d)


## Arrasta o dedo de sp_de até sp_para (tela), em passos, um por quadro.
func _desliza(sp_de: Vector2, sp_para: Vector2, passos: int = 12) -> void:
	for i in range(1, passos + 1):
		_move(sp_de.lerp(sp_para, float(i) / passos))
		await get_tree().process_frame


## Rola o quarto com um gesto no espaço vazio da parede até a posição x ficar visível.
func _mostra(x: float) -> void:
	for tentativa in 5:
		if _na_tela(Vector2(x, 450)):
			return
		var zoom: float = main.cam.zoom.x
		var dx := clampf((main.cam.position.x - x) * zoom, -_vis().x * 0.6, _vis().x * 0.6)
		var y: float = main.world_to_screen(Vector2(0, 110)).y
		var de := Vector2(_vis().x / 2.0 - dx / 2.0, y)
		_evento(de, true)
		await get_tree().process_frame
		await _desliza(de, de + Vector2(dx, 0), 8)
		var antes: float = main.cam.position.x
		_evento(de + Vector2(dx, 0), false)
		await _espera(0.6)
		if is_equal_approx(antes, main.cam.position.x) and absf(dx) > 1.0 and tentativa > 0:
			return  # já está no fim do quarto


func _toca(wp: Vector2) -> void:
	await _mostra(wp.x)
	var sp: Vector2 = main.world_to_screen(wp)
	_evento(sp, true)
	await get_tree().process_frame
	_evento(sp, false)
	await _espera(0.35)


## Pega em `de` e solta com o corpo do personagem em `para` (coordenadas do quarto).
func _arrasta(de: Vector2, para: Vector2, espera_final: float = 0.6) -> void:
	await _mostra(de.x)
	var sp: Vector2 = main.world_to_screen(de)
	_evento(sp, true)
	await get_tree().process_frame
	var dedo := para + Vector2(0, main.LIFT)  # o personagem fica acima do dedo
	if not _na_tela(dedo, 160.0):
		# leva o dedo até a borda e espera o quarto rolar
		var borda_x := 50.0 if dedo.x < main.screen_to_world(sp).x else _vis().x - 50.0
		var borda := Vector2(borda_x, main.world_to_screen(dedo).y)
		await _desliza(sp, borda)
		sp = borda
		var parado := 0
		while not _na_tela(dedo, 160.0) and parado < 5:
			var antes: float = main.cam.position.x
			await get_tree().process_frame
			parado = parado + 1 if main.cam.position.x == antes else 0  # chegou ao fim do quarto
	await _desliza(sp, main.world_to_screen(dedo))
	_evento(main.world_to_screen(dedo), false)
	await _espera(espera_final)


func _foto(nome: String) -> void:
	if capturas.is_empty():
		return
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(capturas.path_join(nome + ".png"))
