class_name Fazendinha
extends Node2D
## Jogo da fazendinha na Plantação: preparar a terra, plantar, regar, colher e vender.
##   enxadinha num quadradinho de terra dura   -> terra fofinha
##   pacotinho de sementes na terra fofinha     -> planta (custa ferradurinhas; cenoura sai de graça se faltar)
##   regador cheio na planta                    -> passa um estágio na hora (o regador enche na bica)
##   o tempo também faz crescer; a nuvem de chuva rega tudo; planta pronta nunca estraga
##   tocar na planta pronta                     -> colhe (os legumes pulam para o chão; ganha estrelinhas)
##   soltar a colheita na banca ou na cesta     -> vende por ferradurinhas
##   tocar numa árvore do pomar com frutas      -> as frutas caem; voltam com o tempo ou com uma rega
## Números (preços, tempos, posições) em dados/fazendinha.json. Sem punição: nada murcha, nada se perde.
## O progresso fica guardado no aparelho (user://fazendinha.json): ao abrir de novo, a fazendinha está
## como ficou, e as plantas cresceram pelo tempo que o jogo passou fechado.

const CENA := "plantacao"
const LARGURA := 200.0            # largura de um quadradinho
const SALVAR_A_CADA := 5.0        # segundos entre um salvamento e outro
const MAX_FECHADO := 900.0        # tempo fechado que conta para crescer (basta para tudo ficar pronto)

static var arquivo := "user://fazendinha.json"   # o roteiro de teste troca por outro arquivo

var main: Node2D                  # main.gd (efeitos, objetos e cenários)
var cen: Cenario
var dados: Dictionary = {}
var ferraduras := 0
var estrelas := 0
var terreno_aberto := false
var plots: Array = []             # {x, base, aberto, estado: "dura"|"fofa"|"planta", cultura, estagio (1..4), t}
var regador: Toy
var regador_cheio := true
var enxada: Toy
var pacotes := {}                 # cultura -> Toy
var relogio := {}                 # id (morango_1, macieira...) -> segundos contados
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
		plots.append({"x": float(q[0]), "base": float(q[1]), "aberto": bool(q[2]), "estado": "dura", "cultura": "", "estagio": 0, "t": 0.0})
	regador = _objeto("regador_cheio", dados["regador"], Vector2(80, 55))
	enxada = _objeto("enxada", dados["enxada"], Vector2(45, 90))
	for c in dados["pacotes"]:
		if not dados["culturas"][c].get("libera_com_terreno", false):
			pacotes[c] = _objeto("sementes_" + c, dados["pacotes"][c], Vector2(60, 80))
	cen.set_estado("nuvem", 0)  # a nuvem só chove quando a criança toca nela
	_fazer_hud()
	carregar()


func _objeto(tipo: String, pos: Array, tam: Vector2) -> Toy:
	return main._add_objeto(CENA, {"tipo": tipo, "x": pos[0], "y": pos[1], "w": tam.x, "h": tam.y})


func _textura(nome: String) -> Texture2D:
	if not _tex.has(nome):
		_tex[nome] = load("res://assets/cenario/%s/%s.png" % [CENA, nome]) as Texture2D
	return _tex[nome]


# ---------------------------------------------------------------- desenho

func _imagem(q: Dictionary) -> String:
	if not q["aberto"]:
		return "terra_fechada"
	if q["estado"] == "planta":
		return "%s_%d" % [q["cultura"], q["estagio"]]
	return "terra_" + str(q["estado"])


func rect_de(i: int) -> Rect2:
	var q: Dictionary = plots[i]
	var h := 70.0
	if q["estado"] == "planta":
		h = float(dados["culturas"][q["cultura"]]["altura"])
	return Rect2(q["x"], q["base"] - h, LARGURA, h)


func _draw() -> void:
	for i in plots.size():
		draw_texture_rect(_textura(_imagem(plots[i])), rect_de(i), false)


## Qual quadradinho está no ponto p (-1 se nenhum). A planta alta conta só da metade para baixo,
## para não roubar o toque de quem está atrás dela.
func alvo_em(p: Vector2) -> int:
	for i in plots.size():
		var r := rect_de(i)
		if r.size.y > 120.0:
			r = Rect2(r.position.x, r.end.y - 150.0, r.size.x, 150.0)
		if r.has_point(p):
			return i
	return -1


# ---------------------------------------------------------------- toque

func toque(i: int) -> void:
	var q: Dictionary = plots[i]
	var c := rect_de(i).get_center()
	if not q["aberto"]:
		var falta: int = int(dados["abrir_terreno_estrelas"]) - estrelas
		main._float_text(c + Vector2(0, -50), "Faltam %d estrelinhas" % falta, 30)
		_bump(txt_estrelas)
	elif q["estado"] == "dura":
		_dica(enxada)
	elif q["estado"] == "fofa":
		for k in pacotes:
			_dica(pacotes[k])
	elif int(q["estagio"]) < 4:
		_dica(regador)
		if not regador_cheio:
			main._sparkle(_r(dados["bica"]).get_center(), 4)
	else:
		_colher(i)


## Toque numa peça do cenário (árvore, canteiro de morango, nuvem). true = a fazendinha cuidou do toque.
func toque_cenario(iid: String) -> bool:
	if dados["arvores"].has(iid):
		if cen.estado(iid) == 1:
			_sacudir(iid)
		else:
			_dica(regador)
		return true
	if iid.begins_with("morango_"):
		if cen.estado(iid) == 3:
			var m: Dictionary = dados["morango"]
			var r := cen.rect_de(iid)
			_soltar_colheita(str(m["colheita"]), int(m["quantos"]), Vector2(r.get_center().x, r.position.y + 30.0))
			cen.set_estado(iid, 0)
			relogio[iid] = 0.0
			_ganhar_estrelas(int(m["estrelas"]), r.get_center())
			main._log("colheu morango")
		else:
			_dica(regador)
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
		if i != -1 and plots[i]["aberto"] and plots[i]["estado"] == "dura":
			plots[i]["estado"] = "fofa"
			queue_redraw()
			main._sparkle(rect_de(i).get_center(), 5)
			main._log("enxada: terra fofinha")
		_volta(enxada, dados["enxada"])
		return true
	for c in pacotes:
		if t == pacotes[c]:
			if i != -1 and plots[i]["aberto"] and plots[i]["estado"] == "fofa":
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
	if iid.begins_with("morango_") and cen.estado(iid) < 3:
		cen.set_estado(iid, cen.estado(iid) + 1)
		relogio[iid] = 0.0
		_encher(false)
		main._sparkle(cen.rect_de(iid).get_center(), 5)
	elif dados["arvores"].has(iid) and cen.estado(iid) == 0:
		cen.set_estado(iid, 1)
		relogio[iid] = 0.0
		_encher(false)
		main._sparkle(cen.rect_de(iid).get_center() + Vector2(0, -120), 6)


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
	for iid in ["morango_1", "morango_2"]:
		if cen.estado(iid) < 3:
			cen.set_estado(iid, cen.estado(iid) + 1)
			relogio[iid] = 0.0
	main._log("choveu")


# ---------------------------------------------------------------- colher e vender

func _colher(i: int) -> void:
	var q: Dictionary = plots[i]
	var c: Dictionary = dados["culturas"][q["cultura"]]
	var r := rect_de(i)
	main._log("colheu %s" % q["cultura"])
	q["estado"] = "dura"
	q["cultura"] = ""
	q["estagio"] = 0
	queue_redraw()
	_soltar_colheita(str(c["colheita"]), int(c["quantos"]), Vector2(r.get_center().x, r.end.y - 90.0))
	_ganhar_estrelas(int(c["estrelas"]), r.get_center())


## As frutas ou legumes pulam para o chão, um ao lado do outro, e viram objetos de pegar.
func _soltar_colheita(tipo: String, n: int, de: Vector2) -> void:
	var tam: Array = dados["tamanhos"][tipo]
	for k in n:
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
	_soltar_colheita(str(a["fruta"]), int(a["quantos"]), Vector2(r.get_center().x, r.position.y + 170.0))
	main._sparkle(Vector2(r.get_center().x, r.position.y + 150.0), 5)
	main._log("sacudiu %s" % iid)


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
	estrelas += n
	_voa("estrelinha", onde + Vector2(0, -60))
	_atualiza_hud()
	_bump(txt_estrelas)
	if not terreno_aberto and estrelas >= int(dados["abrir_terreno_estrelas"]):
		_abrir_terreno()


## Com estrelinhas suficientes, os quadradinhos com cadeado se abrem e chega a semente de tomate.
func _abrir_terreno() -> void:
	terreno_aberto = true
	for i in plots.size():
		if not plots[i]["aberto"]:
			plots[i]["aberto"] = true
			main._sparkle(rect_de(i).get_center(), 8)
			main._hearts(rect_de(i).get_center() + Vector2(0, -40), 3)
	for c in dados["pacotes"]:
		if not pacotes.has(c):
			pacotes[c] = _objeto("sementes_" + c, dados["pacotes"][c], Vector2(60, 80))
			_dica(pacotes[c])
	queue_redraw()
	main._log("terreno novo aberto")


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
	for iid in ["morango_1", "morango_2"]:
		if cen.estado(iid) < 3:
			relogio[iid] = float(relogio.get(iid, 0.0)) + delta
			if float(relogio[iid]) >= float(dados["morango"]["tempo"]) / 3.0:
				relogio[iid] = 0.0
				cen.set_estado(iid, cen.estado(iid) + 1)
	for iid in dados["arvores"]:
		if cen.estado(iid) == 0:
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
	for iid in ["morango_1", "morango_2", "macieira", "laranjeira", "bananeira"]:
		pecas[iid] = cen.estado(iid)
	var d := {
		"v": 1,
		"salvo_em": agora if agora >= 0.0 else Time.get_unix_time_from_system(),
		"ferraduras": ferraduras, "estrelas": estrelas, "terreno_aberto": terreno_aberto,
		"plots": plots, "pecas": pecas, "relogio": relogio,
		"regador": {"cheio": regador_cheio, "x": regador.global_position.x, "y": regador.global_position.y},
		"soltos": _soltos(),
	}
	var f := FileAccess.open(arquivo, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(d))
		f.close()


## Recupera a fazendinha guardada e faz crescer o que cresceria com o jogo fechado.
func carregar(agora: float = -1.0) -> bool:
	if not FileAccess.file_exists(arquivo):
		return false
	var lido: Variant = JSON.parse_string(FileAccess.get_file_as_string(arquivo))
	if not (lido is Dictionary) or int(lido.get("v", 0)) != 1:
		return false
	var d: Dictionary = lido
	ferraduras = int(d.get("ferraduras", ferraduras))
	estrelas = int(d.get("estrelas", estrelas))
	var salvos: Array = d.get("plots", [])
	for i in mini(plots.size(), salvos.size()):
		var q: Dictionary = salvos[i]
		var cultura := str(q.get("cultura", ""))
		if str(q.get("estado", "")) == "planta" and not dados["culturas"].has(cultura):
			continue  # cultura que não existe mais: o quadradinho fica como está
		plots[i]["aberto"] = bool(q.get("aberto", plots[i]["aberto"]))
		plots[i]["estado"] = str(q.get("estado", "dura"))
		plots[i]["cultura"] = cultura
		plots[i]["estagio"] = clampi(int(q.get("estagio", 0)), 0, 4)
		plots[i]["t"] = float(q.get("t", 0.0))
	if bool(d.get("terreno_aberto", false)) and not terreno_aberto:
		terreno_aberto = true
		for c in dados["pacotes"]:
			if not pacotes.has(c):
				pacotes[c] = _objeto("sementes_" + c, dados["pacotes"][c], Vector2(60, 80))
	var pecas: Dictionary = d.get("pecas", {})
	for iid in pecas:
		if cen.interativos.has(iid):
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
