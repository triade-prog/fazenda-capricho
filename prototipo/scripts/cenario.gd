class_name Cenario
extends Node2D
## Cenário montado por dados (dados/cenarios/<id>.json): peças em PNG de assets/cenario/<id>/,
## na mesma posição da prévia em arte/cenario/<id>/. Peças com estados (portas, abajur, fogo)
## trocam de imagem com um toque; quem cuida do toque é o main.gd.
##
## Formato do JSON (gerado por ferramentas/cenario2d/para_jogo.py):
##   "pecas": [[nome, x, y, w, h], ...]  em ordem de desenho; "@id" = peça interativa
##   "interativos": {id: {"estados": [...], "estado", "x", "y", "w", "h", "leva", "chegada"}}
##   "lugares": [{"id", "area": [x, y, w, h], "spots": [[x, y]...], "pose"}]
##   "superficies": [[x inicial, x final, altura], ...]
##   "animacoes": {peça ou "@id": {"tipo": "fogo" | "gira" | "balanca" | "flutua", ...}}  peças que se mexem sozinhas
##   "moveis": [peça, ...]  móveis que dá para puxar de lado (cadeiras, banquinhos)
##
## Modo Decorar (decoracao.gd): cada peça pode ser levada para outro lugar; o deslocamento fica em
## "deco" e leva junto o que está em cima dela (enfeites, lugares de sentar/deitar, superfícies).

signal peca_movida(i: int, d: Vector2)   # o modo Decorar mudou uma peça de lugar

var id := ""
var largura := 2200.0
var pecas: Array = []
var interativos := {}
var objetos: Array = []           # peças que dá para pegar: {tipo, x, y (base), w, h}
var lugares: Array = []
var superficies: Array[Vector3] = []
var animacoes := {}
var moveis: Array = []
var so_se := {}                   # peça -> [interativo, estado]: só aparece nesse estado
var desloc := {}                  # índice da peça -> quanto o móvel foi puxado (x)
var deco := {}                    # índice da peça -> Vector2 (arrumação do modo Decorar)
var decorando := false            # modo Decorar ligado: mostra o contorno das peças que mudam de lugar
var deco_ativa := -1              # peça que está sendo levada no modo Decorar
var _lugar_dono := {}             # índice do lugar -> peça em que ele está (sofá, cama, rede)
var _sup_dono := {}               # índice da superfície -> peça em que ela está (mesa, prateleira)
var _sac := {}                    # índice da peça -> tempo que falta da balançadinha
var _t := 0.0
var _tex := {}

const SACUDIDA := 0.45


func carregar(cena: String) -> Cenario:
	id = cena
	name = "Cenario_" + cena
	z_index = -100
	var path := "res://dados/cenarios/%s.json" % cena
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	largura = float(data.get("largura", 2200))
	pecas = data["pecas"]
	interativos = data.get("interativos", {})
	lugares = data.get("lugares", [])
	objetos = data.get("objetos", [])
	animacoes = data.get("animacoes", {})
	moveis = data.get("moveis", [])
	so_se = data.get("so_se", {})
	set_process(false)
	for s in data.get("superficies", []):
		superficies.append(Vector3(s[0], s[1], s[2]))
	return self


func _textura(nome: String) -> Texture2D:
	if not _tex.has(nome):
		var path := "res://assets/cenario/%s/%s.png" % [id, nome]
		_tex[nome] = load(path) as Texture2D if ResourceLoader.exists(path) else null
	return _tex[nome]


func _draw() -> void:
	for i in pecas.size():
		var p: Array = pecas[i]
		var chave := str(p[0])
		var nome := chave
		var est := 0
		if nome.begins_with("@"):
			var d: Dictionary = interativos[nome.substr(1)]
			est = int(d.get("estado", 0))
			nome = str(d["estados"][est])
		if not _aparece(chave):
			continue
		var t := _textura(nome)
		if t == null:
			continue
		var r := _rect_peca(i)
		var a: Dictionary = animacoes.get(chave, {})
		if not a.is_empty() and a.has("estado") and int(a["estado"]) != est:
			a = {}
		if a.is_empty() and not _sac.has(i):
			draw_texture_rect(t, r, false)
			continue
		var pivo := Vector2(r.get_center().x, r.end.y)
		var rot := 0.0
		var esc := Vector2.ONE
		var fase := float(i) * 1.7
		match str(a.get("tipo", "")):
			"fogo":  # chama crepitando: estica e encolhe a partir da base
				esc = Vector2(1.0 + 0.05 * sin(_t * 9.0 + fase), 1.0 + 0.09 * sin(_t * 13.0 + fase) + 0.04 * sin(_t * 23.0))
				rot = 0.035 * sin(_t * 7.0 + fase)
			"agua":  # filete de água: treme a partir de cima
				pivo = Vector2(r.get_center().x, r.position.y)
				esc = Vector2(1.0 + 0.10 * sin(_t * 17.0), 1.0 + 0.05 * sin(_t * 11.0))
			"ondula":  # água parada com ondinhas: respira a partir do meio
				pivo = r.get_center()
				esc = Vector2(1.0 + 0.015 * sin(_t * 2.6), 1.0 + 0.05 * sin(_t * 3.4))
			"gira":
				pivo = r.get_center()
				rot = _t * float(a.get("vel", 1.2))
			"balanca":
				if str(a.get("pivo", "topo")) == "topo":
					pivo = Vector2(r.get_center().x, r.position.y)
				rot = float(a.get("amp", 0.06)) * sin(_t * float(a.get("vel", 1.6)) + fase)
			"flutua":
				pivo.y += float(a.get("amp", 8.0)) * sin(_t * float(a.get("vel", 2.0)) + fase)
				pivo.x += float(a.get("lado", 0.0)) * sin(_t * float(a.get("vel", 2.0)) * 0.6 + fase)
		if _sac.has(i):
			rot += 0.07 * sin(_t * 26.0) * float(_sac[i]) / SACUDIDA
		var base := Vector2(r.get_center().x, r.end.y)
		if str(a.get("tipo", "")) in ["gira", "ondula"]:
			base = r.get_center()
		elif str(a.get("tipo", "")) == "agua":
			base = Vector2(r.get_center().x, r.position.y)
		elif str(a.get("tipo", "")) == "balanca" and str(a.get("pivo", "topo")) == "topo":
			base = Vector2(r.get_center().x, r.position.y)
		draw_set_transform(pivo, rot, esc)
		draw_texture_rect(t, Rect2(r.position - base, r.size), false)
		if str(a.get("tipo", "")) == "fogo":
			_faiscas(r.size, fase)
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	if decorando:
		_contornos()


## Faíscas subindo do fogo (desenhadas no sistema da chama: origem na base, no meio).
func _faiscas(tam: Vector2, fase: float) -> void:
	for k in 4:
		var u := fposmod(_t * (0.55 + 0.12 * k) + k * 0.31 + fase, 1.0)
		var x := (float(k) / 3.0 - 0.5) * tam.x * 0.6 + 6.0 * sin(_t * 5.0 + k)
		var cor := Color(1.0, 0.85 - 0.3 * u, 0.3, 1.0 - u)
		draw_circle(Vector2(x, -tam.y * (0.5 + 0.9 * u)), 3.5 * (1.0 - u) + 1.0, cor)


func _process(delta: float) -> void:
	_t += delta
	for i in _sac.keys():
		_sac[i] = float(_sac[i]) - delta
		if _sac[i] <= 0.0:
			_sac.erase(i)
	if animacoes.is_empty() and _sac.is_empty():
		set_process(false)
	queue_redraw()


func _notification(what: int) -> void:
	if what == NOTIFICATION_VISIBILITY_CHANGED:
		set_process(is_visible_in_tree() and not (animacoes.is_empty() and _sac.is_empty()))


func _aparece(chave: String) -> bool:
	if not so_se.has(chave):
		return true
	var c: Array = so_se[chave]
	return estado(str(c[0])) == int(c[1])


func _rect_peca(i: int) -> Rect2:
	var p: Array = pecas[i]
	var dd: Vector2 = deco.get(i, Vector2.ZERO)
	return Rect2(p[1] + float(desloc.get(i, 0.0)) + dd.x, p[2] + dd.y, p[3], p[4])


## Peça parada (enfeite) que está no ponto: a de cima. -1 se não há (o fundo não conta).
func peca_em(p: Vector2) -> int:
	var achou := -1
	for i in range(1, pecas.size()):
		if str(pecas[i][0]).begins_with("@") or not _rect_peca(i).has_point(p) or not _aparece(str(pecas[i][0])):
			continue
		# só enfeites pequenos balançam (um móvel grande balançando deixaria para trás o que está em cima dele)
		if eh_movel(i) or (float(pecas[i][3]) <= 330.0 and float(pecas[i][4]) <= 300.0):
			achou = i
	return achou


## Balançadinha de um enfeite tocado.
func sacudir(i: int) -> void:
	_sac[i] = SACUDIDA
	set_process(true)


func eh_movel(i: int) -> bool:
	return i >= 0 and str(pecas[i][0]) in moveis


## Puxa um móvel de lado; devolve quanto ele andou de verdade.
func mover(i: int, dx: float) -> float:
	var x0 := float(pecas[i][1])
	var antes := float(desloc.get(i, 0.0))
	var novo := clampf(x0 + antes + dx, 20.0, largura - float(pecas[i][3]) - 20.0) - x0
	desloc[i] = novo
	queue_redraw()
	return novo - antes


## Solta as imagens da memória (ao sair do cenário); voltam a ser carregadas quando ele aparece.
func soltar() -> void:
	_tex.clear()


func rect_de(iid: String) -> Rect2:
	var d: Dictionary = interativos[iid]
	return Rect2(d["x"], d["y"], d["w"], d["h"])


## Qual peça interativa está no ponto (a de cima, se houver mais de uma).
func interativo_em(p: Vector2) -> String:
	var achou := ""
	for iid in interativos:
		if rect_de(iid).has_point(p):
			achou = iid
	return achou


func estado(iid: String) -> int:
	return int(interativos[iid].get("estado", 0))


func set_estado(iid: String, e: int) -> void:
	var n: int = interativos[iid]["estados"].size()
	interativos[iid]["estado"] = clampi(e, 0, maxi(n - 1, 0))
	queue_redraw()


func alternar(iid: String) -> int:
	var n: int = interativos[iid]["estados"].size()
	if n == 0:
		return 0
	set_estado(iid, (estado(iid) + 1) % n)
	return estado(iid)


func destino(iid: String) -> String:
	return str(interativos[iid].get("leva", ""))


# ---------------------------------------------------------------- modo Decorar

## Peças que não mudam de lugar: o fundo, portas e plaquinhas de caminho (levam a outro cenário),
## peças enormes (a casa, a árvore da casinha) e as que a fazendinha usa pela posição.
const DECO_FIXAS := {"plantacao": ["banca", "bica"]}
const DECO_MAX := Vector2(700.0, 560.0)


func pode_decorar(i: int) -> bool:
	if i <= 0 or i >= pecas.size():
		return false
	var nome := str(pecas[i][0])
	if nome.begins_with("@") and destino(nome.substr(1)) != "":
		return false
	if nome.begins_with("placa_") or nome in DECO_FIXAS.get(id, []):
		return false
	return float(pecas[i][3]) <= DECO_MAX.x and float(pecas[i][4]) <= DECO_MAX.y


## Peça que dá para levar no ponto p (a de cima). -1 se não há.
func peca_deco_em(p: Vector2) -> int:
	var achou := -1
	for i in range(1, pecas.size()):
		if pode_decorar(i) and _rect_peca(i).has_point(p):
			achou = i
	return achou


## O que está em cima da peça i e vai junto com ela (enfeite na estante, vaso na mesa, fogo na lareira).
func carga(i: int) -> Array:
	var r := _rect_peca(i)
	var leva := []
	for j in range(i + 1, pecas.size()):
		if not pode_decorar(j):
			continue
		var rj := _rect_peca(j)
		var pe := Vector2(rj.get_center().x, rj.end.y)
		# está em cima (ou pendurado) se é menor e o pé fica dentro da peça, acima da base dela
		if rj.get_area() < r.get_area() and r.has_point(pe) and pe.y <= r.end.y - 1.0:
			leva.append(j)
	return leva


## Descobre em que peça está cada lugar (sofá, cama) e cada superfície (mesa, prateleira).
## Chamado uma vez, com as peças ainda na posição original.
func preparar_deco() -> void:
	_lugar_dono.clear()
	_sup_dono.clear()
	for k in lugares.size():
		var a: Array = lugares[k]["area"]
		var ra := Rect2(a[0], a[1], a[2], a[3])
		var melhor := 0.0
		for i in range(1, pecas.size()):
			if not pode_decorar(i):
				continue
			var cobre := _rect_peca(i).intersection(ra).get_area() / maxf(ra.get_area(), 1.0)
			if cobre > 0.3 and cobre >= melhor:
				melhor = cobre
				_lugar_dono[k] = i
	for k in superficies.size():
		var sp: Vector3 = superficies[k]
		var meio := Vector2((sp.x + sp.y) / 2.0, sp.z + 4.0)
		for i in range(1, pecas.size()):
			if pode_decorar(i) and _rect_peca(i).has_point(meio) and float(pecas[i][3]) >= (sp.y - sp.x) * 0.7:
				_sup_dono[k] = i


func lugares_da(i: int) -> Array:
	var r := []
	for k in _lugar_dono:
		if _lugar_dono[k] == i:
			r.append(str(lugares[k]["id"]))
	return r


## Superfícies (e prateleiras) em que as coisas se apoiam na peça i.
func superficies_da(i: int) -> Array[Vector3]:
	var r: Array[Vector3] = []
	for k in _sup_dono:
		if _sup_dono[k] == i:
			r.append(superficies[k])
	var nome := str(pecas[i][0])
	if nome.begins_with("@"):
		for pr in interativos[nome.substr(1)].get("prateleiras", []):
			r.append(Vector3(pr[0], pr[1], pr[2]))
	return r


## Leva a peça i (só ela) d pixels; o que pertence a ela (lugares, superfícies, área de toque) vai junto.
func deslocar(i: int, d: Vector2) -> void:
	if d == Vector2.ZERO:
		return
	deco[i] = deco.get(i, Vector2.ZERO) + d
	var nome := str(pecas[i][0])
	if nome.begins_with("@"):
		var it: Dictionary = interativos[nome.substr(1)]
		it["x"] = float(it["x"]) + d.x
		it["y"] = float(it["y"]) + d.y
		if it.has("prateleiras"):
			var novas := []
			for pr in it["prateleiras"]:
				novas.append([float(pr[0]) + d.x, float(pr[1]) + d.x, float(pr[2]) + d.y])
			it["prateleiras"] = novas
	for k in _sup_dono:
		if _sup_dono[k] == i:
			superficies[k] += Vector3(d.x, d.x, d.y)
	for k in _lugar_dono:
		if _lugar_dono[k] == i:
			var a: Array = lugares[k]["area"]
			lugares[k]["area"] = [float(a[0]) + d.x, float(a[1]) + d.y, a[2], a[3]]
	peca_movida.emit(i, d)
	queue_redraw()


## Nome estável de cada peça para o salvamento: "vaso_flores#2" = o segundo vaso_flores.
func chave_peca(i: int) -> String:
	var nome := str(pecas[i][0])
	var n := 0
	for j in i:
		if str(pecas[j][0]) == nome:
			n += 1
	return "%s#%d" % [nome, n]


## Arrumação para guardar: {chave da peça: [dx, dy]} (só as que saíram do lugar).
func arrumacao() -> Dictionary:
	var r := {}
	for i in deco:
		var d: Vector2 = deco[i]
		if d.length() > 0.5:
			r[chave_peca(i)] = [snappedf(d.x, 0.1), snappedf(d.y, 0.1)]
	return r


func indice_da_chave(chave: String) -> int:
	for i in pecas.size():
		if chave_peca(i) == chave:
			return i
	return -1


## Contorno tracejado nas peças que mudam de lugar; a que está sendo levada fica dourada.
func _contornos() -> void:
	for i in range(1, pecas.size()):
		if not pode_decorar(i):
			continue
		var r := _rect_peca(i).grow(4.0)
		if i == deco_ativa:
			draw_rect(r, Color(1.0, 0.85, 0.3, 0.25), true)
			draw_rect(r, Color("#f2c14e"), false, 5.0)
		else:
			_tracejado(r, Color(1, 1, 1, 0.85), 3.0)


func _tracejado(r: Rect2, cor: Color, larg: float) -> void:
	var cantos := [r.position, Vector2(r.end.x, r.position.y), r.end, Vector2(r.position.x, r.end.y), r.position]
	for k in 4:
		var a: Vector2 = cantos[k]
		var b: Vector2 = cantos[k + 1]
		var n := maxi(1, int(a.distance_to(b) / 14.0))
		for m in range(0, n, 2):
			draw_line(a.lerp(b, float(m) / n), a.lerp(b, minf(1.0, float(m + 1) / n)), cor, larg)
