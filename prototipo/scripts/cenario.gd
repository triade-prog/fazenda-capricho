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

var id := ""
var largura := 2200.0
var pecas: Array = []
var interativos := {}
var objetos: Array = []           # peças que dá para pegar: {tipo, x, y (base), w, h}
var lugares: Array = []
var superficies: Array[Vector3] = []
var animacoes := {}
var moveis: Array = []
var desloc := {}                  # índice da peça -> quanto o móvel foi puxado (x)
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
		var t := _textura(nome)
		if t == null:
			continue
		var r := Rect2(p[1] + float(desloc.get(i, 0.0)), p[2], p[3], p[4])
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
		if str(a.get("tipo", "")) == "gira":
			base = r.get_center()
		elif str(a.get("tipo", "")) == "balanca" and str(a.get("pivo", "topo")) == "topo":
			base = Vector2(r.get_center().x, r.position.y)
		draw_set_transform(pivo, rot, esc)
		draw_texture_rect(t, Rect2(r.position - base, r.size), false)
		if str(a.get("tipo", "")) == "fogo":
			_faiscas(r.size, fase)
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


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


func _rect_peca(i: int) -> Rect2:
	var p: Array = pecas[i]
	return Rect2(p[1] + float(desloc.get(i, 0.0)), p[2], p[3], p[4])


## Peça parada (enfeite) que está no ponto: a de cima. -1 se não há (o fundo não conta).
func peca_em(p: Vector2) -> int:
	var achou := -1
	for i in range(1, pecas.size()):
		if str(pecas[i][0]).begins_with("@") or not _rect_peca(i).has_point(p):
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
