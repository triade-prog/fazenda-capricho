class_name MapaFazenda
extends CanvasLayer
## Mapa da fazenda: o botão da ferradura (canto de cima à esquerda) abre um painel com uma
## figurinha de cada lugar; tocar numa figurinha leva a câmera para lá. Sem letras: a criança
## reconhece o lugar pelo desenho. O coração marca onde ela está.
## As posições são frações da tela (o jogo estica para qualquer iPad).

signal escolheu(cena: String)

const OUTLINE := Color("#5b3a4f")
## cena -> centro da figurinha (fração da tela). Arrumação parecida com docs/mapa_cenarios.png.
const LUGARES := {
	"entrada": Vector2(0.50, 0.14), "plantacao": Vector2(0.78, 0.14),
	"sala": Vector2(0.22, 0.38), "sede": Vector2(0.50, 0.38), "estabulo": Vector2(0.78, 0.38),
	"quarto": Vector2(0.08, 0.63), "quarto_carol": Vector2(0.22, 0.63), "cozinha": Vector2(0.36, 0.63),
	"casa_arvore": Vector2(0.56, 0.63), "pet_care": Vector2(0.90, 0.63),
	"casa_arvore_dentro": Vector2(0.42, 0.87), "cabana": Vector2(0.58, 0.87), "casinha": Vector2(0.74, 0.87),
}
const CAMINHOS := [["sala", "sede"], ["sala", "quarto"], ["sala", "quarto_carol"], ["sala", "cozinha"],
	["sede", "entrada"], ["sede", "plantacao"], ["sede", "estabulo"], ["sede", "casa_arvore"],
	["estabulo", "plantacao"], ["estabulo", "pet_care"],
	["casa_arvore", "casa_arvore_dentro"], ["casa_arvore", "cabana"], ["casa_arvore", "casinha"]]

var botao: TextureButton
var painel: Control
var figurinhas := {}              # cena -> TextureButton
var aqui: TextureRect
var cena_atual := "quarto"
var _t := 0.0


func _init() -> void:
	layer = 6


func _ready() -> void:
	botao = _botao("botao_mapa", Vector2(140, 140))
	botao.position = Vector2(18, 18)
	botao.pressed.connect(abrir)
	add_child(botao)

	painel = Control.new()
	painel.set_anchors_preset(Control.PRESET_FULL_RECT)
	painel.mouse_filter = Control.MOUSE_FILTER_STOP   # com o mapa aberto, nada atrás recebe toque
	painel.visible = false
	painel.draw.connect(_desenha_fundo)
	painel.resized.connect(_arruma)
	painel.gui_input.connect(_toque_fora)
	add_child(painel)
	for cena in LUGARES:
		var f := _botao(cena, Vector2(200, 150))
		f.pressed.connect(_escolhe.bind(cena))
		painel.add_child(f)
		figurinhas[cena] = f
	aqui = TextureRect.new()
	aqui.texture = load("res://assets/mapa/aqui.png")
	aqui.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	aqui.size = Vector2(64, 64)
	aqui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	painel.add_child(aqui)
	var fechar := _botao("botao_fechar", Vector2(96, 96))
	fechar.name = "Fechar"
	fechar.pressed.connect(fechar_mapa)
	painel.add_child(fechar)
	_arruma()


func _botao(imagem: String, tamanho: Vector2) -> TextureButton:
	var b := TextureButton.new()
	b.texture_normal = load("res://assets/mapa/%s.png" % imagem)
	b.ignore_texture_size = true
	b.stretch_mode = TextureButton.STRETCH_SCALE
	b.custom_minimum_size = tamanho
	b.size = tamanho
	b.pivot_offset = tamanho / 2.0
	b.button_down.connect(func() -> void: b.scale = Vector2(0.92, 0.92))
	b.button_up.connect(func() -> void: b.scale = Vector2.ONE)
	return b


func aberto() -> bool:
	return painel.visible


func abrir() -> void:
	painel.visible = true
	botao.visible = false
	_arruma()
	painel.modulate.a = 0.0
	create_tween().tween_property(painel, "modulate:a", 1.0, 0.15)


func fechar_mapa() -> void:
	painel.visible = false
	botao.visible = true


func _escolhe(cena: String) -> void:
	fechar_mapa()
	escolheu.emit(cena)


func _toque_fora(e: InputEvent) -> void:
	if e is InputEventMouseButton and e.pressed:
		fechar_mapa()


func _centro(cena: String) -> Vector2:
	return (LUGARES[cena] as Vector2) * painel.size


func _arruma() -> void:
	if figurinhas.is_empty():
		return
	# a figurinha encolhe em telas estreitas para as colunas não encostarem
	var w := minf(240.0, painel.size.x * 0.135)
	var tam := Vector2(w, w * 0.75)
	for cena in figurinhas:
		var f: TextureButton = figurinhas[cena]
		f.custom_minimum_size = tam
		f.size = tam
		f.pivot_offset = tam / 2.0
		f.position = _centro(cena) - tam / 2.0
	var fechar: TextureButton = painel.get_node("Fechar")
	fechar.position = Vector2(painel.size.x - 96 - 18, 18)
	if LUGARES.has(cena_atual):
		aqui.position = _centro(cena_atual) + Vector2(tam.x / 2.0 - 44, -tam.y / 2.0 - 20)
	aqui.visible = LUGARES.has(cena_atual)
	painel.queue_redraw()


func _desenha_fundo() -> void:
	painel.draw_rect(Rect2(Vector2.ZERO, painel.size), Color(1.0, 0.9, 0.95))
	for par in CAMINHOS:
		var a := _centro(par[0])
		var b := _centro(par[1])
		painel.draw_line(a, b, OUTLINE, 16.0, true)
		painel.draw_line(a, b, Color("#f6d9b0"), 10.0, true)


func _process(delta: float) -> void:
	if painel.visible:
		_t += delta
		aqui.scale = Vector2.ONE * (1.0 + 0.12 * sin(_t * 5.0))
		aqui.pivot_offset = aqui.size / 2.0
