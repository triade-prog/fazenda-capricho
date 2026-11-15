class_name Itens
extends RefCounted
## Ficha dos itens que podem ir para o baú e voltar a um cenário.
##
## Dois tipos de item:
##   - da loja: "vaso_flor", "poltrona"... (dados/itens.json; imagem em assets/itens/ ou assets/loja/);
##   - peça que já vinha num cenário e foi guardada: "sala/vaso_flores" (imagem do próprio cenário).
## Regras de cada peça dos cenários (fixa, só mover, parede, chão) em dados/moveis.json.

static var _loja := {}
static var _moveis := {}
static var _originais := {}      # "cena/nome" -> {w, h, onde, parede}
static var _tex := {}


static func loja() -> Dictionary:
	if _loja.is_empty():
		_loja = JSON.parse_string(FileAccess.get_file_as_string("res://dados/itens.json"))
	return _loja


static func moveis() -> Dictionary:
	if _moveis.is_empty():
		_moveis = JSON.parse_string(FileAccess.get_file_as_string("res://dados/moveis.json"))
	return _moveis


static func da_loja(item: String) -> bool:
	return loja()["itens"].has(item)


## A peça original guardada vira um item que pode voltar (registrada pelo cenário ao preparar).
static func registrar_original(cena: String, nome: String, w: float, h: float, parede: bool) -> void:
	_originais["%s/%s" % [cena, nome]] = {"w": w, "h": h, "onde": "dentro" if dentro(cena) else "fora", "parede": parede}


static func existe(item: String) -> bool:
	return da_loja(item) or _originais.has(item)


static func ficha(item: String) -> Dictionary:
	if da_loja(item):
		return loja()["itens"][item]
	return _originais.get(item, {})


static func tamanho(item: String) -> Vector2:
	var f := ficha(item)
	return Vector2(float(f.get("w", 80)), float(f.get("h", 80)))


static func parede(item: String) -> bool:
	return bool(ficha(item).get("parede", false))


static func dentro(cena: String) -> bool:
	return cena in moveis()["dentro"]


## O item combina com o cenário? (de casa só dentro, de quintal só fora; "todos" vai em qualquer um)
static func combina(item: String, cena: String) -> bool:
	var onde := str(ficha(item).get("onde", "todos"))
	if onde == "todos":
		return true
	return (onde == "dentro") == dentro(cena)


static func chao(cena: String) -> float:
	var c: Dictionary = moveis()["chao"]
	return float(c.get(cena, c["padrao"]))


static func textura(item: String) -> Texture2D:
	if _tex.has(item):
		return _tex[item]
	var caminhos: Array = []
	if item.contains("/"):
		var partes := item.split("/")
		caminhos.append("res://assets/cenario/%s/%s.png" % [partes[0], partes[1]])
	else:
		caminhos.append("res://assets/itens/%s.png" % item)
		caminhos.append("res://assets/loja/%s.png" % item)
	var t: Texture2D = null
	for c in caminhos:
		if ResourceLoader.exists(c):
			t = load(c) as Texture2D
			break
	_tex[item] = t
	return t


static func icone(nome: String) -> Texture2D:
	var c := "res://assets/itens/%s.png" % nome
	return load(c) as Texture2D if ResourceLoader.exists(c) else null
