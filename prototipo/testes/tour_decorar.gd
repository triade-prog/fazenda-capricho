extends Node
## Passeio do modo Decorar: liga o modo em cada cenário, tira foto e lista o que cada peça leva junto.
## Rodar: godot --path prototipo res://testes/tour_decorar.tscn -- --capturas=/pasta

var main: Node2D
var capturas := ""


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--capturas="):
			capturas = a.get_slice("=", 1)
	Fazendinha.arquivo = "user://tour_fazendinha.json"
	Decoracao.arquivo = "user://tour_decoracao.json"
	for f in [Fazendinha.arquivo, Decoracao.arquivo]:
		if FileAccess.file_exists(f):
			DirAccess.remove_absolute(f)
	main = load("res://main.tscn").instantiate()
	add_child(main)
	await get_tree().create_timer(3.4).timeout
	for id in main.cenarios:
		if not main.cenarios[id] is Cenario:
			continue
		var c: Cenario = main.cenarios[id]
		main._ir_pelo_mapa(id)
		await get_tree().create_timer(1.3).timeout
		main.decoracao.ligar()
		print("== ", id)
		for i in range(1, c.pecas.size()):
			var nome := c.chave_peca(i)
			if not c.pode_decorar(i):
				print("   fixa    ", nome)
			elif c.eh_parte(i):
				print("   parte   ", nome, " de ", c.chave_peca(c._pai(i)))
			else:
				var leva := []
				for j in c.carga(i):
					leva.append(c.chave_peca(j))
				print("   move    ", nome, "  leva: ", leva, "  lugares: ", c.lugares_da(i), "  sup: ", c.superficies_da(i).size())
		for k in c.lugares.size():
			if not c._lugar_dono.has(k):
				print("   !! lugar sem dono: ", c.lugares[k]["id"])
		for k in c.superficies.size():
			if not c._sup_dono.has(k):
				print("   !! superfície sem dono: ", c.superficies[k])
		var n := ceili(c.largura / 1300.0)
		for k in n:
			main.camera_to(650.0 + k * (c.largura - 1300.0) / maxf(n - 1, 1))
			await get_tree().create_timer(0.15).timeout
			if capturas != "":
				await RenderingServer.frame_post_draw
				get_viewport().get_texture().get_image().save_png(capturas.path_join("%s_%d.png" % [id, k]))
		# leva cada peça um pouco e confere que ela e o que está nela andaram igual
		var dc: Decoracao = main.decoracao
		for i in range(1, c.pecas.size()):
			if not c.pode_decorar(i) or c.eh_parte(i):
				continue
			var r := c._rect_peca(i)
			var toque := r.get_center()
			if c.peca_deco_em(toque) != i:
				continue  # coberta por outra peça no meio
			main.camera_to(toque.x)
			if not dc.pegar(toque):
				print("   !! não pegou ", c.chave_peca(i))
				continue
			var grupo := dc._grupo.duplicate()
			var antes := {}
			for g in grupo:
				antes[g] = c._rect_peca(g).position
			dc.levar(toque + Vector2(60, -25))
			dc.soltar()
			var d0: Vector2 = c._rect_peca(i).position - antes[i]
			for g in grupo:
				if (c._rect_peca(g).position - antes[g]).distance_to(d0) > 0.5:
					print("   !! ", c.chave_peca(g), " não foi junto com ", c.chave_peca(i))
			if d0.length() < 1.0:
				print("   !! ", c.chave_peca(i), " não andou")
		main.decoracao.desligar()
	print("FIM")
	get_tree().quit()
