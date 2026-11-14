class_name Fazendinha
extends Node2D
## Jogo da fazendinha na Plantação: preparar a terra, plantar, regar, colher e vender.
##   enxadinha num quadradinho de terra dura   -> terra fofinha
##   pacotinho de sementes no lugar certo       -> planta (custa ferradurinhas; cenoura sai de graça se faltar)
##       lavoura (quadradinhos): cenoura, alface, tomate · covinhas: girassol e abóbora · canteiro baixo: morango
##   regador cheio na planta                    -> passa um estágio na hora (o regador enche na bica)
##   o tempo também faz crescer; a nuvem de chuva rega tudo; planta pronta nunca estraga
##   tocar na planta pronta                     -> colhe (a colheita pula para o chão; ganha estrelinhas)
##   soltar a colheita na banca ou na cesta     -> vende por ferradurinhas
##   tocar numa árvore ou no canteiro de flores -> as frutas/flores caem; voltam com o tempo ou com uma rega
##   estrelinhas sobem o nível, e cada nível libera lugares, sementes e árvores (cadeado = ainda fechado)
## Números (preços, tempos, níveis, posições) em dados/fazendinha.json. Sem punição: nada murcha, nada se perde.
## O progresso fica guardado no aparelho (user://fazendinha.json): ao abrir de novo, a fazendinha está
## como ficou, e as plantas cresceram pelo tempo que o jogo passou fechado.

const CENA := "plantacao"
const SALVAR_A_CADA := 5.0        # segundos entre um salvamento e outro
const MAX_FECHADO := 900.0        # tempo fechado que conta para crescer (basta para tudo ficar pronto)
const ESCALA_GIRASSOL := [0.0, 0.0, 0.4, 0.7, 1.0]   # tamanho do girassol em cada estágio
const ABOBORAS := {2: ["abobora_pequena", Vector2(60, 50)], 3: ["abobora_media", Vector2(110, 90)], 4: ["abobora_gigante", Vector2(160, 150)]}

static var arquivo := "user://fazendinha.json"   # o roteiro de teste troca por outro arquivo

var main: Node2D                  # main.gd (efeitos, objetos e cenários)
var cen: Cenario
var dados: Dictionary = {}
var ferraduras := 0
var estrelas := 0
var nivel := 1
var plots: Array = []             # {x, base, nivel, lugar, estado: "dura"|"fofa"|"planta", cultura, estagio (1..4), t}
var regador: Toy
var regador_cheio := true
var enxada: Toy
var pacotes := {}                 # cultura -> Toy
var relogio := {}                 # id da árvore -> segundos contados
var chovendo := 0.0
var hud: CanvasLayer
var txt_ferraduras: Label
var txt_estrelas: Label
var _tex := {}
var _desde_salvar := 0.0


func preparar(p_main: Node2D) -> void:
	main = p_main
	cen = main.cenarios[CENA]
	dados = JSON.parse_string(FileAccess.get_file_as_string("res://dados/fazendinha.json"))
	ferraduras = int(dados["inicio"]["ferraduras"])
	estrelas = int(dados["inicio"]["estrelas"])
	z_index = -99
	visible = false
	for q in dados["quadradinhos"]:
		var lugar := str(q[3])
		plots.append({"x": float(q[0]), "base": float(q[1]), "nivel": int(q[2]), "lugar": lugar,
			"estado": "dura" if lugar == "terra" else "fofa", "cultura": "", "estagio": 0, "t": 0.0})
	regador = _objeto("regador_cheio", dados["regador"], Vector2(80, 55))
	enxada = _objeto("enxada", dados["enxada"], Vector2(45, 90))
	cen.set_estado("nuvem", 0)  # a nuvem só chove quando a criança toca nela
	_fazer_hud()
	_atualiza_nivel(false)
	carregar()


func _objeto(tipo: String, pos: Array, tam: Vector2) -> Toy:
	return main._add_objeto(CENA, {"tipo": tipo, "x": pos[0], "y": pos[1], "w": tam.x, "h": tam.y})


func _textura(nome: String) -> Texture2D:
	if not _tex.has(nome):
		_tex[nome] = load("res://assets/cenario/%s/%s.png" % [CENA, nome]) as Texture2D
	return _tex[nome]


# ---------------------------------------------------------------- níveis

func _nivel_de(n_estrelas: int) -> int:
	var n := 0
	for limite in dados["niveis"]:
		if n_estrelas >= int(limite):
			n += 1
	return maxi(n, 1)


## Estrelinhas que faltam para chegar ao nível n.
func faltam_para(n: int) -> int:
	var niveis: Array = dados["niveis"]
	return maxi(int(niveis[clampi(n - 1, 0, niveis.size() - 1)]) - estrelas, 0)


func aberto(i: int) -> bool:
	return nivel >= int(plots[i]["nivel"])


## Recalcula o nível e põe no jogo o que ele libera; com festa quando a criança acabou de subir.
func _atualiza_nivel(festa: bool) -> void:
	var antes := nivel
	nivel = _nivel_de(estrelas)
	for c in dados["pacotes"]:
		if not pacotes.has(c) and nivel >= int(dados["culturas"][c]["nivel"]):
			pacotes[c] = _objeto("sementes_" + c, dados["pacotes"][c], Vector2(60, 80))
			if festa:
				_dica(pacotes[c])
	for iid in dados["arvores"]:
		var n := int(dados["arvores"][iid]["nivel"])
		if nivel < n:
			cen.set_estado(iid, 0)       # árvore ainda fechada fica sem frutas
		elif antes < n and festa:
			cen.set_estado(iid, 1)       # acabou de abrir: já vem carregada
			main._sparkle(cen.rect_de(iid).get_center(), 8)
	if festa and nivel > antes:
		for i in plots.size():
			if int(plots[i]["nivel"]) > antes and aberto(i):
				main._sparkle(rect_de(i).get_center(), 8)
				main._hearts(rect_de(i).get_center() + Vector2(0, -40), 3)
		main._float_text(main.cam.position + Vector2(-90, -160), "Nível %d!" % nivel, 60)
		main._log("nível %d" % nivel)
	queue_redraw()


# ---------------------------------------------------------------- desenho

## Onde o quadradinho aparece (e onde aceita toque e soltar), conforme o lugar e o estágio.
func rect_de(i: int) -> Rect2:
	var q: Dictionary = plots[i]
	var e := int(q["estagio"]) if q["estado"] == "planta" else 0
	match str(q["lugar"]):
		"terra":
			var h := float(dados["culturas"][q["cultura"]]["altura"]) if e > 0 else 70.0
			return Rect2(q["x"], q["base"] - h, 200.0, h)
		"morango":
			return Rect2(q["x"], q["base"] - 110.0, 160.0, 110.0)
		"abobora":
			if e >= 2:
				var tam: Vector2 = ABOBORAS[e][1]
				return Rect2(q["x"] + 80.0 - tam.x / 2.0, q["base"] - tam.y, tam.x, tam.y)
		"girassol":
			if e >= 2:
				var k: float = ESCALA_GIRASSOL[e]
				return Rect2(q["x"], q["base"] - 10.0 - 405.0 * k, 160.0, 405.0 * k + 10.0)
	return Rect2(q["x"], q["base"] - 80.0, 160.0, 80.0)   # covinha


func _draw() -> void:
	for i in plots.size():
		var q: Dictionary = plots[i]
		var e := int(q["estagio"]) if q["estado"] == "planta" else 0
		var fechado := not aberto(i)
		var cor := Color(0.8, 0.78, 0.8) if fechado else Color.WHITE
		var r := rect_de(i)
		match str(q["lugar"]):
			"terra":
				var img := "terra_" + str(q["estado"])
				if fechado:
					img = "terra_fechada"
				elif e > 0:
					img = "%s_%d" % [q["cultura"], e]
				draw_texture_rect(_textura(img), r, false)
			"morango":
				draw_texture_rect(_textura("morango_%d" % e), r, false, cor)
			"abobora":
				if e >= 2:
					draw_texture_rect(_textura(ABOBORAS[e][0]), r, false)
				else:
					draw_texture_rect(_textura("covinha_broto" if e == 1 else "covinha"), r, false, cor)
			"girassol":
				var cova := Rect2(q["x"], q["base"] - 80.0, 160.0, 80.0)
				draw_texture_rect(_textura("covinha_broto" if e == 1 else "covinha"), cova, false, cor)
				if e >= 2:
					var k: float = ESCALA_GIRASSOL[e]
					var cx: float = q["x"] + 80.0
					var topo: float = q["base"] - 10.0 - 360.0 * k
					draw_texture_rect(_textura("girassol_caule"), Rect2(cx - 45.0 * k, topo, 90.0 * k, 360.0 * k), false)
					draw_texture_rect(_textura("girassol_cabeca"), Rect2(cx - 45.0 * k, topo - 5.0 * k, 90.0 * k, 90.0 * k), false)
		if fechado and q["lugar"] != "terra":
			draw_texture_rect(_textura("cadeado"), Rect2(r.get_center() + Vector2(-25, -34), Vector2(50, 56)), false)
	for iid in _fechadas():
		var r := cen.rect_de(iid)
		draw_texture_rect(_textura("cadeado"), Rect2(Vector2(r.get_center().x - 30.0, r.end.y - 150.0), Vector2(60, 67)), false)


## Árvores e peças especiais que o nível ainda não liberou.
func _fechadas() -> Array:
	var r: Array = []
	for iid in dados["arvores"]:
		if nivel < int(dados["arvores"][iid]["nivel"]):
			r.append(iid)
	for iid in dados["especiais"]:
		if nivel < int(dados["especiais"][iid]):
			r.append(iid)
	return r


## Qual quadradinho está no ponto p (-1 se nenhum). A planta alta conta só da metade para baixo,
## para não roubar o toque de quem está atrás dela.
func alvo_em(p: Vector2) -> int:
	for i in plots.size():
		var r := rect_de(i)
		if r.size.y > 150.0:
			r = Rect2(r.position.x, r.end.y - 150.0, r.size.x, 150.0)
		if r.has_point(p):
			return i
	return -1


# ---------------------------------------------------------------- toque

func _falta(onde: Vector2, n: int) -> void:
	main._float_text(onde + Vector2(0, -50), "Faltam %d estrelinhas" % faltam_para(n), 30)
	_bump(txt_estrelas)


func toque(i: int) -> void:
	var q: Dictionary = plots[i]
	var c := rect_de(i).get_center()
	if not aberto(i):
		_falta(c, int(q["nivel"]))
	elif q["estado"] == "dura":
		_dica(enxada)
	elif q["estado"] == "fofa":
		for k in pacotes:
			if dados["culturas"][k]["lugar"] == q["lugar"]:
				_dica(pacotes[k])
	elif int(q["estagio"]) < 4:
		_dica(regador)
		if not regador_cheio:
			main._sparkle(_r(dados["bica"]).get_center(), 4)
	else:
		_colher(i)


## Toque numa peça do cenário (árvore, canteiro de flores, nuvem). true = a fazendinha cuidou do toque.
func toque_cenario(iid: String) -> bool:
	if dados["arvores"].has(iid):
		var a: Dictionary = dados["arvores"][iid]
		if nivel < int(a["nivel"]):
			_falta(cen.rect_de(iid).get_center(), int(a["nivel"]))
		elif cen.estado(iid) == 1:
			_sacudir(iid)
		else:
			_dica(regador)
		return true
	if dados["especiais"].has(iid) and nivel < int(dados["especiais"][iid]):
		_falta(cen.rect_de(iid).get_center(), int(dados["especiais"][iid]))
		return true
	if iid == "nuvem":
		chover()
		return true
	return false


func _dica(t: Toy) -> void:
	if t and is_instance_valid(t):
		main._pop(t)
		main._sparkle(t.global_position + Vector2(0, -30), 4)


# ---------------------------------------------------------------- soltar objetos

## Um objeto foi solto na Plantação. true = a fazendinha já cuidou dele (não cai no chão como os outros).
func soltar(t: Toy, p: Vector2) -> bool:
	var i := alvo_em(p)
	if i == -1:
		i = alvo_em(t.global_position + Vector2(0, -10))
	if t == enxada:
		if i != -1 and aberto(i) and plots[i]["estado"] == "dura":
			plots[i]["estado"] = "fofa"
			queue_redraw()
			main._sparkle(rect_de(i).get_center(), 5)
			main._log("enxada: terra fofinha")
		_volta(enxada, dados["enxada"])
		return true
	for c in pacotes:
		if t == pacotes[c]:
			if i != -1 and aberto(i) and plots[i]["estado"] == "fofa" and plots[i]["lugar"] == dados["culturas"][c]["lugar"]:
				_plantar(i, c)
			_volta(t, dados["pacotes"][c])
			return true
	if t == regador:
		_regar(i, p)
		return false  # o regador fica onde foi solto
	if dados["vende"].has(t.kind) and t.holder == null:
		var banca := _r(dados["banca"]).grow(30.0)
		var cesta := cen.rect_de("cesta").grow(30.0)
		for r in [banca, cesta]:
			if r.has_point(p) or r.has_point(t.global_position + Vector2(0, -10)):
				_vender(t, r.get_center())
				return true
	return false


func _volta(t: Toy, casa: Array) -> void:
	main._fall(t, Vector2(casa[0], casa[1]))
	main._pop(t)


func _plantar(i: int, cultura: String) -> void:
	var preco := int(dados["culturas"][cultura]["semente"])
	if ferraduras < preco:
		if cultura != "cenoura":
			main._float_text(rect_de(i).get_center() + Vector2(0, -50), "Faltam ferradurinhas", 30)
			_bump(txt_ferraduras)
			_dica(pacotes.get("cenoura"))
			return
		preco = 0  # rede de segurança: a cenoura nunca falta
	ferraduras -= preco
	var q: Dictionary = plots[i]
	q["estado"] = "planta"
	q["cultura"] = cultura
	q["estagio"] = 1
	q["t"] = 0.0
	queue_redraw()
	_atualiza_hud()
	main._sparkle(rect_de(i).get_center(), 4)
	main._log("plantou %s (-%d)" % [cultura, preco])


func _regar(i: int, p: Vector2) -> void:
	var r := _r(dados["bica"]).grow(40.0)
	if r.has_point(p) or r.has_point(regador.global_position + Vector2(0, -20)):
		_encher(true)
		main._sparkle(r.get_center(), 5)
		main._log("regador cheio")
		return
	if not regador_cheio:
		return
	if i != -1 and plots[i]["estado"] == "planta" and int(plots[i]["estagio"]) < 4:
		_crescer(i)
		_encher(false)
		main._log("regou %s" % plots[i]["cultura"])
		return
	var iid := cen.interativo_em(p)
	if dados["arvores"].has(iid) and cen.estado(iid) == 0 and nivel >= int(dados["arvores"][iid]["nivel"]):
		cen.set_estado(iid, 1)
		relogio[iid] = 0.0
		_encher(false)
		main._sparkle(cen.rect_de(iid).get_center(), 6)


func _encher(cheio: bool) -> void:
	regador_cheio = cheio
	var spr := regador.art.get_child(0) as Sprite2D
	spr.texture = _textura("regador_cheio" if cheio else "regador_vazio")


func _crescer(i: int) -> void:
	var q: Dictionary = plots[i]
	q["estagio"] = int(q["estagio"]) + 1
	q["t"] = 0.0
	queue_redraw()
	if visible:
		main._sparkle(rect_de(i).get_center(), 7 if int(q["estagio"]) == 4 else 3)


## A nuvem de chuva rega todos os canteiros de uma vez.
func chover() -> void:
	if chovendo > 0.0:
		return
	chovendo = 2.5
	cen.set_estado("nuvem", 1)
	for i in plots.size():
		if plots[i]["estado"] == "planta" and int(plots[i]["estagio"]) < 4:
			_crescer(i)
	main._log("choveu")


# ---------------------------------------------------------------- colher e vender

func _colher(i: int) -> void:
	var q: Dictionary = plots[i]
	var c: Dictionary = dados["culturas"][q["cultura"]]
	var r := rect_de(i)
	main._log("colheu %s" % q["cultura"])
	q["estado"] = "dura" if q["lugar"] == "terra" else "fofa"
	q["cultura"] = ""
	q["estagio"] = 0
	queue_redraw()
	_soltar_colheita([str(c["colheita"])], int(c["quantos"]), Vector2(r.get_center().x, r.end.y - 90.0))
	_ganhar_estrelas(int(c["estrelas"]), r.get_center())


## As frutas, flores ou legumes pulam para o chão, um ao lado do outro, e viram objetos de pegar.
func _soltar_colheita(tipos: Array, n: int, de: Vector2) -> void:
	for k in n:
		var tipo := str(tipos[k % tipos.size()])
		var tam: Array = dados["tamanhos"][tipo]
		var x := de.x + (k - (n - 1) / 2.0) * 62.0 + randf_range(-8, 8)
		var chao := Vector2(clampf(x, 40.0, cen.largura - 40.0), randf_range(835.0, 880.0))
		var t: Toy = main._add_objeto(CENA, {"tipo": tipo, "x": de.x, "y": de.y, "w": tam[0], "h": tam[1]})
		t.squash = Vector2(0.3, 0.3)
		t.move_tween = t.create_tween().set_parallel(true)
		t.move_tween.tween_property(t, "squash", Vector2.ONE, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		t.move_tween.tween_property(t, "global_position:x", chao.x, 0.45)
		t.move_tween.tween_property(t, "global_position:y", chao.y, 0.45).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)


func _sacudir(iid: String) -> void:
	var a: Dictionary = dados["arvores"][iid]
	var r := cen.rect_de(iid)
	cen.set_estado(iid, 0)
	relogio[iid] = 0.0
	var de := Vector2(r.get_center().x, r.position.y + minf(170.0, r.size.y * 0.5))
	_soltar_colheita(a["fruta"], int(a["quantos"]), de)
	main._sparkle(de, 5)
	main._log("sacudiu %s" % iid)
	_ganhar_estrelas(int(a.get("estrelas", 0)), de)


func _vender(t: Toy, onde: Vector2) -> void:
	var preco := int(dados["vende"][t.kind])
	main._log("vendeu %s (+%d)" % [t.kind, preco])
	main.toys.erase(t)
	t.kill_move()
	t.queue_free()
	ferraduras += preco
	cen.set_estado("cesta", 1)
	main._sparkle(onde + Vector2(0, -40), 5)
	_voa("ferradurinha", onde + Vector2(0, -50))
	main._float_text(onde + Vector2(0, -110), "+%d" % preco, 36)
	_atualiza_hud()
	_bump(txt_ferraduras)


func _ganhar_estrelas(n: int, onde: Vector2) -> void:
	if n <= 0:
		return
	estrelas += n
	_voa("estrelinha", onde + Vector2(0, -60))
	_atualiza_hud()
	_bump(txt_estrelas)
	_atualiza_nivel(true)


## Uma ferradurinha ou estrelinha sobe e some (vai para o contador).
func _voa(imagem: String, de: Vector2) -> void:
	var s := Sprite2D.new()
	s.texture = _textura(imagem)
	s.scale = Vector2.ONE * (44.0 / s.texture.get_width())
	s.position = de
	s.z_index = 500
	main.add_child(s)
	var tw := s.create_tween().set_parallel(true)
	tw.tween_property(s, "position:y", de.y - 150.0, 0.7).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(s, "modulate:a", 0.0, 0.7).set_ease(Tween.EASE_IN)
	tw.chain().tween_callback(s.queue_free)


# ---------------------------------------------------------------- tempo

## Chamado a cada quadro, mesmo com a criança em outro cenário: a plantação continua crescendo.
func passar(delta: float) -> void:
	_desde_salvar += delta
	if _desde_salvar >= SALVAR_A_CADA:
		salvar()
	_crescer_com_o_tempo(delta)


func _crescer_com_o_tempo(delta: float) -> void:
	if chovendo > 0.0:
		chovendo -= delta
		if chovendo <= 0.0:
			cen.set_estado("nuvem", 0)
	for i in plots.size():
		var q: Dictionary = plots[i]
		if q["estado"] == "planta" and int(q["estagio"]) < 4:
			q["t"] = float(q["t"]) + delta
			if float(q["t"]) >= float(dados["culturas"][q["cultura"]]["tempo"]) / 3.0:
				_crescer(i)
	for iid in dados["arvores"]:
		if cen.estado(iid) == 0 and nivel >= int(dados["arvores"][iid]["nivel"]):
			relogio[iid] = float(relogio.get(iid, 0.0)) + delta
			if float(relogio[iid]) >= float(dados["arvores"][iid]["tempo"]):
				relogio[iid] = 0.0
				cen.set_estado(iid, 1)


# ---------------------------------------------------------------- salvamento

func _notification(what: int) -> void:
	# ao fechar o jogo ou trocar de aplicativo no iPad, guarda na hora
	if what in [NOTIFICATION_WM_CLOSE_REQUEST, NOTIFICATION_APPLICATION_PAUSED,
			NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_WM_WINDOW_FOCUS_OUT]:
		if main:
			salvar()


func _soltos() -> Array:
	var r: Array = []
	for t in main.toys:
		if t.cena == CENA and dados["vende"].has(t.kind) and t.holder == null:
			r.append([t.kind, snappedf(t.global_position.x, 1.0), snappedf(t.global_position.y, 1.0)])
	return r


func salvar(agora: float = -1.0) -> void:
	_desde_salvar = 0.0
	var pecas := {}
	for iid in dados["arvores"]:
		pecas[iid] = cen.estado(iid)
	var d := {
		"v": 1,
		"salvo_em": agora if agora >= 0.0 else Time.get_unix_time_from_system(),
		"ferraduras": ferraduras, "estrelas": estrelas,
		"plots": plots, "pecas": pecas, "relogio": relogio,
		"regador": {"cheio": regador_cheio, "x": regador.global_position.x, "y": regador.global_position.y},
		"soltos": _soltos(),
	}
	var f := FileAccess.open(arquivo, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(d))
		f.close()


## Recupera a fazendinha guardada e faz crescer o que cresceria com o jogo fechado.
## Aceita também o salvamento da primeira versão (só a lavoura): o que não existia começa do zero.
func carregar(agora: float = -1.0) -> bool:
	if not FileAccess.file_exists(arquivo):
		return false
	var lido: Variant = JSON.parse_string(FileAccess.get_file_as_string(arquivo))
	if not (lido is Dictionary) or int(lido.get("v", 0)) != 1:
		return false
	var d: Dictionary = lido
	ferraduras = int(d.get("ferraduras", ferraduras))
	estrelas = int(d.get("estrelas", estrelas))
	_atualiza_nivel(false)
	var salvos: Array = d.get("plots", [])
	for i in mini(plots.size(), salvos.size()):
		var q: Dictionary = salvos[i]
		var cultura := str(q.get("cultura", ""))
		var estado := str(q.get("estado", ""))
		if estado == "planta" and (not dados["culturas"].has(cultura) or dados["culturas"][cultura]["lugar"] != plots[i]["lugar"]):
			continue  # cultura que não existe mais ou lugar que mudou: o quadradinho fica como está
		if not estado in ["dura", "fofa", "planta"] or (estado == "dura" and plots[i]["lugar"] != "terra"):
			continue
		plots[i]["estado"] = estado
		plots[i]["cultura"] = cultura
		plots[i]["estagio"] = clampi(int(q.get("estagio", 0)), 0, 4)
		plots[i]["t"] = float(q.get("t", 0.0))
	var pecas: Dictionary = d.get("pecas", {})
	for iid in pecas:
		if dados["arvores"].has(iid) and nivel >= int(dados["arvores"][iid]["nivel"]):
			cen.set_estado(iid, int(pecas[iid]))
	relogio.clear()
	var rel: Dictionary = d.get("relogio", {})
	for iid in rel:
		relogio[iid] = float(rel[iid])
	var rg: Dictionary = d.get("regador", {})
	_encher(bool(rg.get("cheio", true)))
	if rg.has("x"):
		regador.kill_move()
		regador.global_position = Vector2(float(rg["x"]), float(rg["y"]))
	# a colheita solta no chão volta para onde estava
	for t in main.toys.duplicate():
		if t.cena == CENA and dados["vende"].has(t.kind) and t.holder == null:
			main.toys.erase(t)
			t.queue_free()
	for s in d.get("soltos", []):
		if dados["tamanhos"].has(str(s[0])):
			var tam: Array = dados["tamanhos"][str(s[0])]
			main._add_objeto(CENA, {"tipo": str(s[0]), "x": float(s[1]), "y": float(s[2]), "w": tam[0], "h": tam[1]})
	# o tempo que o jogo ficou fechado também faz crescer
	var t_agora := agora if agora >= 0.0 else Time.get_unix_time_from_system()
	var fechado := clampf(t_agora - float(d.get("salvo_em", t_agora)), 0.0, MAX_FECHADO)
	while fechado > 0.0:
		var passo := minf(fechado, 5.0)
		_crescer_com_o_tempo(passo)
		fechado -= passo
	queue_redraw()
	_atualiza_hud()
	return true


# ---------------------------------------------------------------- contador

func mostrar(sim: bool) -> void:
	visible = sim
	hud.visible = sim


func _fazer_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 4
	hud.visible = false
	add_child(hud)
	var caixa := TextureRect.new()
	caixa.texture = _textura("contador")
	caixa.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	caixa.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caixa.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	caixa.offset_left = -398.0
	caixa.offset_right = -18.0
	caixa.offset_top = 18.0
	caixa.offset_bottom = 18.0 + 380.0 * 70.0 / 300.0
	hud.add_child(caixa)
	txt_ferraduras = _numero(caixa, 84.0)
	txt_estrelas = _numero(caixa, 268.0)
	_atualiza_hud()


func _numero(caixa: Control, x: float) -> Label:
	var l := Label.new()
	l.position = Vector2(x, 14.0)
	l.size = Vector2(90, 60)
	l.pivot_offset = Vector2(30, 30)
	l.add_theme_font_size_override("font_size", 44)
	l.add_theme_color_override("font_color", Color("#5b3a4f"))
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caixa.add_child(l)
	return l


func _atualiza_hud() -> void:
	txt_ferraduras.text = str(ferraduras)
	txt_estrelas.text = str(estrelas)


func _bump(l: Label) -> void:
	var tw := l.create_tween()
	tw.tween_property(l, "scale", Vector2(1.35, 1.35), 0.08)
	tw.tween_property(l, "scale", Vector2.ONE, 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _r(a: Array) -> Rect2:
	return Rect2(a[0], a[1], a[2], a[3])
