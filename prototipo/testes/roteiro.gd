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
	# o teste usa um arquivo de salvamento só dele e começa sempre do zero
	Fazendinha.arquivo = "user://teste_fazendinha.json"
	if FileAccess.file_exists(Fazendinha.arquivo):
		DirAccess.remove_absolute(Fazendinha.arquivo)
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
	pel.kill_move()
	pel.global_position = Vector2(2050, 820)  # fora do caminho: o rolar do quarto varia de uma rodada para outra

	# castelinho cheio: a Nina fica triste
	var leo: Toy = main._find("leo")
	var zoe: Toy = main._find("zoe")
	await _arrasta(leo.global_position + Vector2(0, -50), Vector2(340, 540))
	await _arrasta(zoe.global_position + Vector2(0, -60), Vector2(340, 540))
	_confere(leo.slot != null and zoe.slot != null, "Leo e Zoe entraram no castelinho")
	await _arrasta(nina.global_position + Vector2(0, -90), Vector2(340, 540), 0.3)
	_confere(nina.anim_state == "failed" and nina.slot == null, "castelinho cheio: Nina fica triste e não entra")
	await _foto("19_nina_triste")

	# Sala: a porta do quarto leva à Sala, e de volta
	if cat.slot or cat.mount:
		await _arrasta(cat.to_global(Vector2(0, -235)), Vector2(1250, 640))  # pela cabeça: montada, o corpo fica atrás da Lumi
	_confere(cat.mount == null and cat.slot == null, "Catarina está no chão, pronta para ir à porta")
	await _arrasta(cat.to_global(Vector2(0, -235)), Vector2(1725, 560), 1.2)
	_confere(main.cena == "sala" and cat.cena == "sala", "Catarina passa pela porta do quarto e chega na Sala")
	_confere(not bob.visible, "na Sala, quem ficou no quarto não aparece")
	await _foto("20_sala_chegada")
	var c: Cenario = main.cenarios["sala"]
	var abajur := c.estado("abajur")
	await _toca(c.rect_de("abajur").get_center())
	_confere(c.estado("abajur") != abajur, "tocar no abajur acende/apaga")
	await _toca(c.rect_de("fogo").get_center())
	_confere(c.estado("fogo") == 0, "tocar no fogo da lareira deixa o fogo baixo")
	var urso: Toy = main._find("ursinho")
	_confere(urso != null and not urso.visible, "os brinquedos começam guardados no cesto")
	await _toca(c.rect_de("cesto").get_center())
	_confere(c.estado("cesto") == 1 and urso.visible, "tocar no cesto solta os brinquedos no chão")
	await _foto("20c_cesto_brinquedos")
	# Quarto da Carol: a porta da flor
	await _vai("porta_carol", "quarto_carol", "28_quarto_carol")
	var qg: Cenario = main.cenarios["quarto_carol"]
	var laco: Toy = main._find("laco")
	await _toca(qg.rect_de("gaveta_esq").position + Vector2(65, 120))
	_confere(qg.estado("gaveta_esq") == 1 and laco.visible, "tocar no criado-mudo abre a gaveta e mostra o laço")
	_confere(main._find("travesseiro") != null, "os travesseiros da cama são de pegar")
	await _foto("28b_gaveta_aberta")
	var qc: Cenario = main.cenarios["quarto_carol"]
	await _toca(qc.rect_de("guarda_roupa").get_center())
	_confere(qc.estado("guarda_roupa") == 1, "tocar no guarda-roupa da Carol abre as portas")
	await _vai("porta_sala", "sala", "")

	# Cozinha: a porta da panela leva à Cozinha
	var k: Cenario = main.cenarios["cozinha"]
	await _toca(c.rect_de("porta_cozinha").get_center())
	await _espera(0.8)
	_confere(main.cena == "cozinha", "tocar na porta da panela leva à Cozinha")
	await _toca(k.rect_de("fogao").get_center())
	_confere(k.estado("fogao") == 0, "tocar no fogão tira o vapor da panela")
	await _toca(k.rect_de("tigela_cao").get_center())
	_confere(k.estado("tigela_cao") == 0, "tocar na tigela do cão esvazia a tigela")
	await _toca(k.rect_de("prato_pia").get_center())
	_confere(k.estado("prato_pia") == 1, "tocar no prato sujo da pia deixa o prato limpo")
	await _toca(k.rect_de("torneira").get_center())
	_confere(k.estado("torneira") == 1, "tocar na torneira abre a água")
	_confere(not k._aparece("vapor"), "com o fogão apagado a fumacinha some")
	await _toca(k.rect_de("fogao").get_center())
	_confere(k.estado("fogao") == 1 and k._aparece("vapor"), "acender o fogão traz as chaminhas e a fumacinha")
	await _foto("20b_cozinha")
	await _toca(k.rect_de("porta_sala").get_center())
	await _espera(0.8)
	_confere(main.cena == "sala", "a porta da casinha volta para a Sala")
	await _arrasta(cat.to_global(Vector2(0, -150)), Vector2(1500, 470), 1.0)
	_confere(cat.slot != null and cat.slot.id == "sofa", "Catarina deita no sofá da Sala")
	await _foto("21_sala_sofa")
	await _toca(c.rect_de("porta_catarina").get_center())
	await _espera(0.8)
	_confere(main.cena == "quarto" and cat.cena == "sala", "tocar na porta da Sala volta para o quarto (Catarina fica na Sala)")
	_confere(not cat.visible, "Catarina não aparece no quarto enquanto está na Sala")
	await _foto("22_volta_quarto")
	await _toca(Vector2(1725, 450))
	await _espera(0.8)
	_confere(main.cena == "sala" and cat.visible, "a porta do quarto leva de novo à Sala")

	# Catarina vai à Cozinha e come
	await _arrasta(cat.to_global(Vector2(0, -150)), c.rect_de("porta_cozinha").get_center(), 1.2)
	_confere(main.cena == "cozinha" and cat.cena == "cozinha", "Catarina passa pela porta da panela e chega na Cozinha")
	var xic: Toy = main._find("xicara")
	await _arrasta(xic.global_position + Vector2(0, -18), cat.to_global(Vector2(0, -150)))
	_confere(cat.held_item == xic, "Catarina segura a xícara")
	var maca: Toy = main._find("maca")
	_confere(maca != null and not maca.visible, "com a geladeira fechada a maçã fica guardada lá dentro")
	var gel := k.rect_de("geladeira").position + Vector2(40, 30)
	await _toca(gel)
	_confere(k.estado("geladeira") == 1 and maca.visible, "abrir a geladeira mostra as comidinhas nas prateleiras")
	await _foto("23_geladeira_por_dentro")
	await _arrasta(maca.global_position + Vector2(0, -16), cat.to_global(Vector2(0, -150)), 1.0)
	_confere(main._find("maca") == null, "Catarina come a maçã tirada da geladeira")
	var queijo: Toy = main._find("queijo")
	await _arrasta(queijo.global_position + Vector2(0, -14), Vector2(700, 560), 0.9)
	var banana: Toy = main._find("banana")
	await _toca(gel)
	_confere(k.estado("geladeira") == 0 and not banana.visible and queijo.visible,
		"fechar a geladeira esconde o que ficou dentro, e o queijo tirado continua fora")
	await _arrasta(queijo.global_position + Vector2(0, -14), Vector2(420, 380), 0.9)
	_confere(queijo.global_position.y > 590.0, "com a geladeira fechada o queijo não entra: cai no chão")
	await _toca(gel)
	_confere(main._find("maca") != null and main._find("maca").visible, "abrir a geladeira de novo traz a maçã de volta")
	await _arrasta(queijo.global_position + Vector2(0, -14), Vector2(420, 380), 0.9)
	_confere(absf(queijo.global_position.y - 400.0) < 3.0, "o queijo volta para a prateleira da geladeira aberta")
	await _toca(gel)
	_confere(not queijo.visible, "e some junto quando a geladeira fecha")
	await _toca(gel)
	# cadeiras de puxar, enfeites que balançam
	var ic := -1
	for i in k.pecas.size():
		if str(k.pecas[i][0]) == "cadeira" and ic < 0:
			ic = i
	var rc: Rect2 = k._rect_peca(ic)
	await _arrasta(rc.position + Vector2(55, 190), rc.position + Vector2(55 - 180, 190), 0.4)
	_confere(absf(float(k.desloc.get(ic, 0.0)) + 180.0) < 30.0, "a cadeira da cozinha é puxada de lado")
	rc = k._rect_peca(ic)
	await _arrasta(cat.to_global(Vector2(0, -235)), rc.position + Vector2(55, 60), 0.9)
	_confere(cat.slot != null and cat.slot.id.begins_with("movel"), "Catarina senta na cadeira puxada")
	var xcat := cat.global_position.x
	await _arrasta(rc.position + Vector2(12, 215), rc.position + Vector2(12 - 100, 215), 0.4)
	_confere(xcat - cat.global_position.x > 60.0, "puxar a cadeira leva junto quem está sentado")
	await _foto("24b_cadeira_puxada")
	var iv := -1
	for i in k.pecas.size():
		if str(k.pecas[i][0]) == "vaso_flores" and iv < 0:
			iv = i
	await _toca(k._rect_peca(iv).get_center())
	_confere(k._sac.has(iv), "tocar num enfeite parado dá uma balançadinha")
	_confere(c.animacoes.has("@fogo"), "o fogo da lareira tem animação de crepitar")
	await _foto("24_geladeira_aberta")

	# Sede e Entrada: a porta da frente da Sala leva à Sede; o caminho de pedras leva à Entrada
	var sd: Cenario = main.cenarios["sede"]
	var en: Cenario = main.cenarios["entrada"]
	await _arrasta(cat.to_global(Vector2(0, -235)), k.rect_de("porta_sala").get_center(), 1.2)
	_confere(main.cena == "sala" and cat.cena == "sala" and xic.cena == "sala", "Catarina volta à Sala levando a xícara")
	await _arrasta(cat.to_global(Vector2(0, -235)), c.rect_de("porta_frente").get_center(), 1.2)
	_confere(main.cena == "sede" and cat.cena == "sede", "Catarina sai pela porta da frente e chega na Sede")
	_confere(main.W == 3000.0, "a Sede é mais larga que os cômodos (3000)")
	await _foto("25_sede_chegada")
	await _toca(sd.rect_de("lanterna_esq").get_center())
	_confere(sd.estado("lanterna_esq") == 1, "tocar na lanterna da varanda acende")
	await _toca(sd.rect_de("luzinhas_2").get_center())
	_confere(sd.estado("luzinhas_2") == 0, "tocar nas luzinhas do deck apaga")
	await _arrasta(cat.to_global(Vector2(0, -235)), Vector2(2075, 430), 1.0)
	_confere(cat.slot != null and cat.slot.id == "rede", "Catarina deita na rede")
	await _foto("26_sede_rede")
	await _toca(sd.rect_de("caminho").get_center())
	await _espera(0.8)
	_confere(main.cena == "entrada" and main.W == 2200.0, "tocar no caminho de pedras leva à Entrada")
	await _toca(en.rect_de("correio").get_center())
	_confere(en.estado("correio") == 0, "tocar no correio fecha a caixinha")
	await _toca(en.rect_de("floreira_dir").get_center())
	_confere(en.estado("floreira_dir") == 1, "tocar na floreira colhida faz as flores nascerem")
	await _foto("27_entrada")
	await _toca(en.rect_de("portao").get_center())
	await _espera(0.8)
	_confere(main.cena == "sede", "o portão da Entrada leva à Sede")

	# Volta pela fazenda: as plaquinhas de caminho ligam os cenários de fora (mapa em docs/mapa_cenarios.png)
	await _vai("seta_estabulo", "estabulo", "30_sede_placas")
	await _toca(main.cenarios["estabulo"].rect_de("balde").get_center())
	_confere(main.cenarios["estabulo"].estado("balde") == 0, "tocar no balde do estábulo esvazia a água")
	await _foto("31_estabulo_baia")
	await _vai("seta_pet_care", "pet_care", "32_estabulo_pasto")
	await _toca(main.cenarios["pet_care"].rect_de("banheira").get_center())
	_confere(main.cenarios["pet_care"].estado("banheira") == 0, "tocar na banheira do Pet Care tira a espuma")
	await _toca(main.cenarios["pet_care"].rect_de("cercadinho").position + Vector2(60, 90))
	_confere(main.cenarios["pet_care"].estado("cercadinho") == 1, "tocar no cercadinho abre o portãozinho")
	await _foto("33_pet_care")
	await _vai("seta_estabulo", "estabulo", "34_pet_care_placa")
	await _vai("seta_plantacao", "plantacao", "")
	await _fazendinha()
	await _vai("seta_estabulo", "estabulo", "39b_plantacao_placas")
	await _vai("seta_sede", "sede", "")
	await _vai("seta_arvore", "casa_arvore", "37_sede_placa_arvore")
	await _foto("38_casa_arvore_chegada")
	await _vai("porta", "casa_arvore_dentro", "39_casa_arvore_porta")
	await _toca(main.cenarios["casa_arvore_dentro"].rect_de("bau").get_center())
	_confere(main.cenarios["casa_arvore_dentro"].estado("bau") == 0, "tocar no baú da casa na árvore fecha a tampa")
	await _foto("40_dentro")
	await _vai("porta", "casa_arvore", "41_dentro_porta")
	await _vai("seta_cabana", "cabana", "42_casa_arvore_placas")
	await _toca(main.cenarios["cabana"].rect_de("fogueira").get_center())
	_confere(main.cenarios["cabana"].estado("fogueira") == 0, "tocar na fogueira da Cabana apaga o brilho")
	await _toca(main.cenarios["cabana"].rect_de("fogueira").get_center())
	_confere(main.cenarios["cabana"]._aparece("chama"), "acender a fogueira traz a chama que crepita")
	await _foto("43_cabana")
	await _vai("seta_arvore", "casa_arvore", "44_cabana_placa")
	await _vai("seta_casinha", "casinha", "")
	await _toca(main.cenarios["casinha"].rect_de("toldo").position + Vector2(40, 30))  # longe dos potinhos
	_confere(main.cenarios["casinha"].estado("toldo") == 0, "tocar no toldo da Casinha fecha o toldo")
	await _foto("45_casinha")
	await _vai("seta_arvore", "casa_arvore", "46_casinha_placa")
	await _vai("seta_sede", "sede", "")

	# Mapa da fazenda: o botão da ferradura abre o mapa; tocar numa figurinha leva a câmera
	main.mapa.botao.pressed.emit()
	await _espera(0.3)
	_confere(main.mapa.aberto() and main.mapa.cena_atual == "sede", "o botão da ferradura abre o mapa, com o coração na Sede")
	await _foto("50_mapa")
	main.mapa.figurinhas["pet_care"].pressed.emit()
	await _espera(0.8)
	_confere(not main.mapa.aberto() and main.cena == "pet_care", "tocar na figurinha do Pet Care leva para lá e fecha o mapa")
	_confere(cat.cena == "sede", "pelo mapa só a câmera viaja (a Catarina fica na Sede)")
	main.mapa.abrir()
	main.mapa.figurinhas["quarto"].pressed.emit()
	await _espera(0.8)
	_confere(main.cena == "quarto" and main.castle.visible, "pelo mapa dá para voltar ao quarto da Catarina")
	await _foto("51_botao_no_quarto")
	main.mapa.abrir()
	main.mapa.fechar_mapa()
	_confere(main.cena == "quarto" and not main.mapa.aberto(), "fechar o mapa deixa tudo como estava")


# ---------------------------------------------------------------- fazendinha (Plantação)

func _fazendinha() -> void:
	var fz: Fazendinha = main.fazenda
	var pl: Cenario = main.cenarios["plantacao"]
	var q0: Vector2 = fz.rect_de(0).get_center()
	await _toca(q0)
	_confere(fz.plots[0]["estado"] == "dura", "tocar na terra dura só dá a dica (a enxadinha pula)")
	await _foto("35_plantacao_inicio")
	await _arrasta(fz.enxada.global_position + Vector2(0, -45), q0)
	_confere(fz.plots[0]["estado"] == "fofa", "enxadinha no quadradinho deixa a terra fofinha")
	_confere(fz.enxada.global_position.distance_to(Vector2(345, 890)) < 5.0, "a enxadinha volta para o lugar dela")
	await _arrasta(fz.pacotes["cenoura"].global_position + Vector2(0, -40), q0)
	_confere(fz.plots[0]["cultura"] == "cenoura" and fz.plots[0]["estagio"] == 1 and fz.ferraduras == 28, "pacotinho na terra fofinha planta a cenoura por 2 ferradurinhas")
	await _arrasta(fz.regador.global_position + Vector2(0, -27), fz.rect_de(0).get_center())
	_confere(fz.plots[0]["estagio"] == 2 and not fz.regador_cheio, "regar faz a planta crescer um estágio e esvazia o regador")
	await _arrasta(fz.regador.global_position + Vector2(0, -27), fz.rect_de(0).get_center())
	_confere(fz.plots[0]["estagio"] == 2, "regador vazio não rega")
	await _arrasta(fz.regador.global_position + Vector2(0, -27), Vector2(85, 720))
	_confere(fz.regador_cheio, "o regador enche na bica")
	await _arrasta(fz.regador.global_position + Vector2(0, -27), fz.rect_de(0).get_center())
	_confere(fz.plots[0]["estagio"] == 3, "regar de novo: mais um estágio")
	await _foto("36_plantacao_crescendo")
	await _toca(pl.rect_de("nuvem").get_center())
	_confere(fz.plots[0]["estagio"] == 4 and pl.estado("nuvem") == 1, "a nuvem de chuva rega tudo: a cenoura fica pronta")
	await _toca(fz.rect_de(0).end - Vector2(25, 25))  # no canto: o regador ficou no meio
	await _espera(0.6)
	_confere(fz.plots[0]["estado"] == "dura" and main._count("colheita_cenoura") == 3 and fz.estrelas == 1, "tocar na planta pronta colhe 3 cenouras e dá 1 estrelinha")
	await _foto("37_plantacao_colheita")
	var cen1: Toy = main._find("colheita_cenoura")
	await _arrasta(cen1.global_position + Vector2(0, -30), pl.rect_de("cesta").get_center())
	_confere(fz.ferraduras == 33 and main._count("colheita_cenoura") == 2, "soltar a cenoura na cesta vende por 5 ferradurinhas")
	# o tempo também faz crescer
	await _arrasta(fz.enxada.global_position + Vector2(0, -45), fz.rect_de(1).get_center())
	await _arrasta(fz.pacotes["alface"].global_position + Vector2(0, -40), fz.rect_de(1).get_center())
	fz.passar(21.0)
	_confere(fz.plots[1]["cultura"] == "alface" and fz.plots[1]["estagio"] == 2, "com o tempo a alface cresce sozinha")
	# quadradinho com cadeado e terreno novo
	await _toca(fz.rect_de(5).get_center())
	_confere(not fz.aberto(5) and fz.nivel == 1, "quadradinho com cadeado continua fechado (faltam estrelinhas)")
	await _toca(fz.rect_de(9).get_center())
	_confere(not fz.aberto(9) and not fz.pacotes.has("morango"), "canteiro de morango com cadeado ainda não aceita plantar")
	fz._ganhar_estrelas(9, fz.rect_de(5).get_center())
	_confere(fz.nivel == 2 and fz.aberto(5) and fz.pacotes.has("tomate") and fz.pacotes.has("girassol"), "com 10 estrelinhas: nível 2, terreno novo, tomate e girassol")
	await _foto("38_plantacao_nivel_2")
	# girassol na covinha (só aceita a semente dele)
	await _arrasta(fz.pacotes["cenoura"].global_position + Vector2(0, -40), fz.rect_de(7).get_center())
	_confere(fz.plots[7]["estado"] == "fofa", "a covinha do girassol não aceita semente de cenoura")
	await _arrasta(fz.pacotes["girassol"].global_position + Vector2(0, -40), fz.rect_de(7).get_center())
	_confere(fz.plots[7]["cultura"] == "girassol" and fz.ferraduras == 28, "girassol plantado na covinha por 3 ferradurinhas")
	fz.passar(41.0)
	fz.passar(41.0)
	fz.passar(41.0)
	_confere(fz.plots[7]["estagio"] == 4, "o girassol cresce com o tempo até ficar mais alto que a Catarina")
	await _mostra(1735.0)
	await _foto("38b_girassol")
	await _toca(Vector2(1735, 600))
	await _espera(0.6)
	_confere(fz.plots[7]["estado"] == "fofa" and main._count("girassol_cabeca") == 1 and fz.estrelas == 11, "colher o girassol dá a flor e 1 estrelinha; a covinha fica pronta para plantar de novo")
	# níveis 3 e 4: morango e abóbora
	fz._ganhar_estrelas(34, fz.rect_de(11).get_center())
	_confere(fz.nivel == 4 and fz.aberto(9) and fz.aberto(11) and fz.pacotes.has("morango") and fz.pacotes.has("abobora"), "45 estrelinhas: nível 4, com morango e abóbora")
	_confere(pl.estado("laranjeira") == 1 and pl.estado("bananeira") == 0, "a laranjeira abre no nível 4; a bananeira continua fechada")
	fz.ferraduras = 40
	await _arrasta(fz.pacotes["morango"].global_position + Vector2(0, -40), fz.rect_de(9).get_center())
	await _arrasta(fz.pacotes["abobora"].global_position + Vector2(0, -40), fz.rect_de(11).get_center())
	_confere(fz.plots[9]["cultura"] == "morango" and fz.plots[11]["cultura"] == "abobora" and fz.ferraduras == 27, "morango (5) e abóbora (8) plantados nos lugares deles")
	fz.chover()
	fz.chovendo = 0.0
	fz.chover()
	fz.chovendo = 0.0
	fz.chover()
	_confere(fz.plots[9]["estagio"] == 4 and fz.plots[11]["estagio"] == 4, "três chuvas: morango pronto e abóbora gigante")
	await _mostra(1300.0)
	await _foto("38c_abobora_gigante")
	await _toca(fz.rect_de(11).get_center())
	await _espera(0.6)
	_confere(main._count("abobora_media") == 1 and fz.estrelas == 48, "colher a abóbora dá uma abóbora para vender e 3 estrelinhas")
	# flores
	var fl: Rect2 = pl.rect_de("canteiro_flores")
	await _toca(fl.get_center())
	await _espera(0.6)
	_confere(pl.estado("canteiro_flores") == 0 and main._count("flor_tulipa") == 1 and fz.estrelas == 49, "tocar no canteiro de flores colhe três flores diferentes")
	await _toca(pl.rect_de("bananeira").get_center())
	_confere(pl.estado("bananeira") == 0 and main._count("banana") == 0, "bananeira com cadeado: nada cai")
	fz.ferraduras = 31
	fz.estrelas = 10
	fz._atualiza_nivel(false)
	# pomar e banca
	var mac: Rect2 = pl.rect_de("macieira")
	await _toca(Vector2(mac.get_center().x, mac.end.y - 120.0))
	await _espera(0.6)
	_confere(pl.estado("macieira") == 0 and main._count("maca") == 4 and fz.estrelas == 11, "tocar na macieira derruba 3 maçãs e dá 1 estrelinha")
	var maca: Toy = main._find("maca")
	await _arrasta(maca.global_position + Vector2(0, -16), Vector2(2660, 850))
	_confere(fz.ferraduras == 35 and main._count("maca") == 3, "soltar a maçã na banca vende por 4 ferradurinhas")
	await _foto("39_plantacao_banca")
	fz.passar(181.0)
	_confere(pl.estado("macieira") == 1, "com o tempo as maçãs voltam")

	# salvamento: guarda, estraga tudo de propósito e recupera
	var agora := 1000000.0
	fz.plots[1]["estagio"] = 2
	fz.plots[1]["t"] = 0.0
	fz.salvar(agora)
	var macas: int = main._count("maca")
	var cenouras: int = main._count("colheita_cenoura")
	var onde: Vector2 = fz.regador.global_position
	fz.ferraduras = 0
	fz.estrelas = 0
	fz.plots[1]["estado"] = "dura"
	fz.regador.global_position = Vector2(2000, 800)
	main._find("colheita_cenoura").global_position = Vector2(2000, 850)
	_confere(fz.carregar(agora), "a fazendinha guardada é recuperada")
	await get_tree().process_frame
	_confere(fz.ferraduras == 35 and fz.estrelas == 11 and fz.nivel == 2, "ferradurinhas, estrelinhas e nível voltam como estavam")
	_confere(fz.plots[1]["cultura"] == "alface" and fz.plots[1]["estagio"] == 2 and fz.aberto(5) and not fz.aberto(9), "os quadradinhos voltam como estavam")
	_confere(main._count("maca") == macas and main._count("colheita_cenoura") == cenouras, "a colheita solta no chão continua lá, sem duplicar")
	_confere(fz.regador.global_position.distance_to(onde) < 2.0, "o regador volta para onde foi deixado")
	fz.carregar(agora + 25.0)
	await get_tree().process_frame
	_confere(fz.plots[1]["estagio"] == 3, "25 s com o jogo fechado: a alface cresce um estágio")
	fz.carregar(agora + 100000.0)
	await get_tree().process_frame
	_confere(fz.plots[1]["estagio"] == 4 and fz.plots[1]["estado"] == "planta", "muito tempo fechado: a alface fica pronta e espera, sem estragar")


# ---------------------------------------------------------------- utilidades
# Todos os toques são enviados em coordenadas de TELA, como um dedo de verdade no iPad.
# Se o destino está fora da tela, o dedo vai até a borda e espera o quarto rolar.

## Toca na porta ou plaquinha `iid` do cenário atual e confere que chegou em `dest`.
func _vai(iid: String, dest: String, foto: String) -> void:
	var de: String = main.cena
	var r: Rect2 = main.cenarios[de].rect_de(iid)
	if foto != "":
		await _mostra(r.get_center().x)
		await _foto(foto)
	await _toca(r.get_center())
	await _espera(0.8)
	_confere(main.cena == dest, "%s: %s leva a %s" % [de, iid, dest])


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
