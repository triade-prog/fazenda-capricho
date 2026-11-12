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
	await _espera(0.6)
	await _foto("00_abertura")
	await _espera(2.6)  # a logo de abertura some sozinha
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

	# ---- personagens novos: Carol, Nina, Leo, Zoe e Lumi
	var carol: Toy = main._find("carol")
	var nina: Toy = main._find("nina")
	var lumi: Toy = main._find("lumi")
	_confere(carol != null and nina != null and lumi != null and main._find("leo") != null \
		and main._find("zoe") != null, "Carol, Nina, Leo, Zoe e Lumi estão no quarto")
	await _foto("12_todos")

	var biscoito: Toy = main._find("biscoito")
	await _arrasta(biscoito.global_position + Vector2(0, -26), nina.global_position + Vector2(0, -90), 0.9)
	_confere(main._find("biscoito") == null, "Nina comeu o biscoito")

	await _arrasta(cat.to_global(Vector2(0, -150)), lumi.seat_global() + Vector2(0, -20))
	_confere(cat.mount == lumi and lumi.rider == cat, "Catarina montou na Lumi")
	await _foto("13_montada")
	var antes := lumi.global_position
	await _arrasta(lumi.global_position + Vector2(60, -200), Vector2(1500, 640), 0.8)
	_confere(lumi.global_position.distance_to(antes) > 100.0 and cat.mount == lumi \
		and cat.global_position.distance_to(lumi.seat_global() + Vector2(0, Toy.RIDE_DROP)) < 2.0,
		"Lumi levou a Catarina junto")
	var virada := lumi.sprite.flip_h
	await _toca(lumi.global_position + Vector2(-80, -250))
	await _espera(0.5)
	_confere(lumi.sprite.flip_h != virada, "Lumi gira ao ser tocada")
	await _foto("14_lumi_passeio")

	await _arrasta(lumi.global_position + Vector2(60, -200), Vector2(340, 520))
	_confere(lumi.slot == null, "Lumi não entra no castelinho (grande demais)")

	await _arrasta(carol.to_global(Vector2(0, -200)), Vector2(300, 200))
	_confere(carol.pose == "deitado", "Carol deitou no beliche")
	await _espera(0.8)
	await _foto("15_carol_cama")

	# ---- Bob 3D: corre e vira para o lado em que é levado
	main.camera_to(bob.global_position.x)
	await _espera(0.2)
	var sb: Vector2 = main.world_to_screen(bob.global_position + Vector2(0, -85))
	_evento(sb, true)
	await get_tree().process_frame
	await _desliza(sb, sb + Vector2(-220, 0), 12)
	_confere(bob.anim_state == "running-right" and bob.sprite.flip_h, "Bob corre virado para a esquerda ao ser levado para a esquerda")
	await _foto("14b_bob_corre")
	await _desliza(sb + Vector2(-220, 0), sb + Vector2(-20, 0), 12)
	_confere(not bob.sprite.flip_h, "Bob vira para a direita")
	_evento(sb + Vector2(-20, 0), false)
	await _espera(0.6)
	_confere(bob.anim_state == "idle", "Bob para de correr ao ser solto")

	# ---- Catarina com folha de pet 3D
	main.camera_to(cat.global_position.x)
	await _espera(0.2)
	if cat.pose == "em_pe" and cat.mount == null:
		await _toca(cat.global_position + Vector2(0, -150))
	else:
		await _arrasta(cat.to_global(Vector2(0, -150)), Vector2(900, 560))
		await _toca(cat.global_position + Vector2(0, -150))
	_confere(cat.anim_state == "waving", "Catarina (3D) acena ao ser tocada")
	await _foto("15b_catarina_acena")
	await _espera(0.8)

	# ---- Nina com folha de pet (ações desenhadas)
	main.camera_to(600.0)
	await _espera(0.2)
	await _toca(nina.global_position + Vector2(0, -90))
	_confere(nina.anim_state == "waving", "Nina acena com a pata ao ser tocada")
	await _foto("16_nina_acena")
	await _espera(0.8)
	_confere(nina.anim_state == "idle", "Nina volta a ficar parada depois do aceno")

	# arrastando a Nina para a direita: ela corre
	var sp: Vector2 = main.world_to_screen(nina.global_position + Vector2(0, -90))
	_evento(sp, true)
	await get_tree().process_frame
	await _desliza(sp, sp + Vector2(260, 0), 14)
	_confere(nina.anim_state == "running-right", "Nina corre para a direita enquanto é arrastada")
	await _foto("17_nina_corre")
	await _desliza(sp + Vector2(260, 0), sp + Vector2(40, 0), 14)
	_confere(nina.anim_state == "running-left", "Nina corre para a esquerda")
	_evento(sp + Vector2(40, 0), false)
	await _espera(0.6)
	_confere(nina.anim_state == "idle", "Nina para de correr ao ser solta")

	# arrastando a pelúcia: a Nina acompanha com o olhar
	var pel: Toy = main._find("pelucia")
	if pel.holder:
		pel = main._find("almofada")
	main.camera_to(pel.global_position.x)
	await _espera(0.2)
	sp = main.world_to_screen(pel.global_position + Vector2(0, -36))
	_evento(sp, true)
	await get_tree().process_frame
	await _desliza(sp, main.world_to_screen(nina.head_global() + Vector2(-260, -60)), 10)
	await get_tree().process_frame
	_confere(nina.anim_state.begins_with("look"), "Nina olha para o objeto que está sendo arrastado")
	await _foto("18_nina_olha")
	_evento(main.world_to_screen(nina.head_global() + Vector2(-260, -60)), false)
	await _espera(0.6)

	# castelinho cheio: a Nina fica triste
	var leo: Toy = main._find("leo")
	var zoe: Toy = main._find("zoe")
	await _arrasta(leo.global_position + Vector2(0, -50), Vector2(340, 540))
	await _arrasta(zoe.global_position + Vector2(0, -60), Vector2(340, 540))
	_confere(leo.slot != null and zoe.slot != null, "Leo e Zoe entraram no castelinho")
	await _arrasta(nina.global_position + Vector2(0, -90), Vector2(340, 540), 0.3)
	_confere(nina.anim_state == "failed" and nina.slot == null, "castelinho cheio: Nina fica triste e não entra")
	await _foto("19_nina_triste")


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
