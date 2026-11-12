class_name Arte
extends RefCounted
## Arte final do cenário (assets/cenario/<nome>.png). Se a imagem não existir, quem chama
## desenha a versão provisória por código.

const PASTA := "res://assets/cenario/"
static var _cache := {}


static func tex(nome: String) -> Texture2D:
	if not _cache.has(nome):
		var path := PASTA + nome + ".png"
		_cache[nome] = load(path) as Texture2D if ResourceLoader.exists(path) else null
	return _cache[nome]


## Desenha a imagem dentro de `rect`: esticando (stretch) ou mantendo a proporção, centrada na
## horizontal e apoiada na base do retângulo. Devolve false se a imagem não existir.
static func draw(ci: CanvasItem, nome: String, rect: Rect2, stretch := false) -> bool:
	var t := tex(nome)
	if t == null:
		return false
	if stretch:
		ci.draw_texture_rect(t, rect, false)
		return true
	var s := minf(rect.size.x / t.get_width(), rect.size.y / t.get_height())
	var size := Vector2(t.get_width(), t.get_height()) * s
	var pos := Vector2(rect.position.x + (rect.size.x - size.x) / 2.0, rect.end.y - size.y)
	ci.draw_texture_rect(t, Rect2(pos, size), false)
	return true


## Repete a imagem na horizontal com altura `h`, espelhando uma vez sim, uma vez não,
## para não aparecer emenda.
static func draw_tiled(ci: CanvasItem, nome: String, y: float, h: float, largura: float) -> bool:
	var t := tex(nome)
	if t == null:
		return false
	var w := t.get_width() * h / t.get_height()
	var x := 0.0
	var i := 0
	while x < largura:
		if i % 2 == 0:
			ci.draw_texture_rect(t, Rect2(x, y, w, h), false)
		else:
			ci.draw_set_transform(Vector2(x + w, y), 0.0, Vector2(-1, 1))
			ci.draw_texture_rect(t, Rect2(0, 0, w, h), false)
			ci.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
		x += w
		i += 1
	return true
