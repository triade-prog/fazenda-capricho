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

var id := ""
var largura := 2200.0
var pecas: Array = []
var interativos := {}
var objetos: Array = []           # peças que dá para pegar: {tipo, x, y (base), w, h}
var lugares: Array = []
var superficies: Array[Vector3] = []
var _tex := {}


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
	for s in data.get("superficies", []):
		superficies.append(Vector3(s[0], s[1], s[2]))
	return self


func _textura(nome: String) -> Texture2D:
	if not _tex.has(nome):
		var path := "res://assets/cenario/%s/%s.png" % [id, nome]
		_tex[nome] = load(path) as Texture2D if ResourceLoader.exists(path) else null
	return _tex[nome]


func _draw() -> void:
	for p in pecas:
		var nome := str(p[0])
		if nome.begins_with("@"):
			var d: Dictionary = interativos[nome.substr(1)]
			nome = str(d["estados"][int(d.get("estado", 0))])
		var t := _textura(nome)
		if t:
			draw_texture_rect(t, Rect2(p[1], p[2], p[3], p[4]), false)


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
	interativos[iid]["estado"] = e
	queue_redraw()


func alternar(iid: String) -> int:
	var n: int = interativos[iid]["estados"].size()
	set_estado(iid, (estado(iid) + 1) % n)
	return estado(iid)


func destino(iid: String) -> String:
	return str(interativos[iid].get("leva", ""))
