class_name MapaFazenda
extends CanvasLayer
## Mapa da fazenda: o botão da ferradura (canto de cima à esquerda) abre o mapa ilustrado, visto de cima
## (imagem de referência de Carol, 15/11/2026). Tocar num lugar leva a câmera para lá. A Casa e a Casa na
## Árvore têm mais de um cenário: o toque abre um balão para escolher o cômodo.
## Peças, posições e nomes vêm de dados/mapa_fazenda.json (gerado por ferramentas/cenario2d/mapa_fazenda.py).
## O mapa é desenhado em 1600 × 1200 e cabe inteiro na tela; o fundo sobra para os lados.

signal escolheu(cena: String)

const DADOS := "res://dados/mapa_fazenda.json"
const PECAS := "res://assets/mapa/fazenda/%s.png"
const FONTE := "res://assets/fontes/Fredoka-SemiBold.ttf"
const OUTLINE := Color("#5b3a4f")
const TEXTO := Color("#a3336f")
const GRAMA := Color("#9ed883")

var botao: TextureButton
var painel: Control
var quadro: Control                 # área de 1600 × 1200, escalada para caber na tela
var figurinhas := {}                # cena -> botão que leva até ela (lugar do mapa ou figurinha do balão)
var lugares := {}                   # lugar -> TextureButton
var cena_atual := "quarto"
var marcador: Control
var balao: PanelContainer
var balao_de := ""
var _d: Dictionary = {}
var _lugar_da_cena := {}            # cena -> lugar do mapa
var _fonte: Font
var _t := 0.0


func _init() -> void:
	layer = 6


func _ready() -> void:
	_d = JSON.parse_string(FileAccess.get_file_as_string(DADOS))
	_fonte = load(FONTE)
	botao = _botao_imagem("res://assets/mapa/botao_mapa.png", Vector2(140, 140))
	botao.position = Vector2(18, 18)
	botao.pressed.connect(abrir)
	add_child(botao)

	painel = Control.new()
	painel.set_anchors_preset(Control.PRESET_FULL_RECT)
	painel.mouse_filter = Control.MOUSE_FILTER_STOP   # com o mapa aberto, nada atrás recebe toque
	painel.visible = false
	painel.draw.connect(func() -> void: painel.draw_rect(Rect2(Vector2.ZERO, painel.size), GRAMA))
	painel.resized.connect(_arruma)
	painel.gui_input.connect(_toque_no_mapa)
	add_child(painel)

	quadro = Control.new()
	quadro.size = Vector2(_d["tela"][0], _d["tela"][1])
	quadro.mouse_filter = Control.MOUSE_FILTER_IGNORE
	painel.add_child(quadro)

	_imagem("fundo", _d["fundo"])
	for dec in _d["decoracao"]:
		_imagem(dec[0], [dec[1], dec[2], dec[3], dec[4]])
	for lugar in _d["ordem"]:
		var l: Dictionary = _d["lugares"][lugar]
		var r: Array = l["rect"]
		var b := _botao_imagem(PECAS % lugar, Vector2(r[2], r[3]))
		b.position = Vector2(r[0], r[1])
		b.name = "lugar_" + lugar
		b.pressed.connect(_toca_lugar.bind(lugar))
		quadro.add_child(b)
		lugares[lugar] = b
		for dest in l["destinos"]:
			_lugar_da_cena[dest[0]] = lugar
			if l["destinos"].size() == 1:
				figurinhas[dest[0]] = b
	for lugar in _d["ordem"]:
		_placa_nome(lugar)

	var ui: Dictionary = _d["ui"]
	var t := _imagem("placa_titulo", ui["titulo"])
	_texto(t, ui["titulo_texto"][0], 46, Color.WHITE, Vector2(0, 78))
	_texto(t, ui["titulo_texto"][1], 50, Color("#ffc2df"), Vector2(0, 128))
	var fx := _imagem("faixa_aviso", ui["faixa"])
	_texto(fx, ui["faixa_texto"], 38, TEXTO, Vector2(0, fx.size.y / 2.0 - 4), false)

	marcador = _imagem("marcador", [0, 0, ui["marcador"][0], ui["marcador"][1]])
	var rosto := TextureRect.new()
	rosto.texture = load(PECAS % "_rosto_catarina")
	rosto.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rosto.position = Vector2(15, 12)
	rosto.size = Vector2(100, 100)
	rosto.mouse_filter = Control.MOUSE_FILTER_IGNORE
	marcador.add_child(rosto)

	var f: Array = ui["fechar"]
	var fechar := _botao_imagem(PECAS % "botao_fechar", Vector2(f[2], f[3]))
	fechar.name = "Fechar"
	fechar.position = Vector2(f[0], f[1])
	fechar.pressed.connect(fechar_mapa)
	quadro.add_child(fechar)

	_monta_balao()
	_arruma()


# ---------------------------------------------------------------- montagem

func _botao_imagem(arquivo: String, tamanho: Vector2) -> TextureButton:
	var b := TextureButton.new()
	b.texture_normal = load(arquivo)
	b.ignore_texture_size = true
	b.stretch_mode = TextureButton.STRETCH_SCALE
	b.custom_minimum_size = tamanho
	b.size = tamanho
	b.pivot_offset = tamanho / 2.0
	b.button_down.connect(func() -> void: b.scale = Vector2(0.94, 0.94))
	b.button_up.connect(func() -> void: b.scale = Vector2.ONE)
	return b


func _imagem(nome: String, r: Array) -> TextureRect:
	var im := TextureRect.new()
	im.texture = load(PECAS % nome)
	im.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	im.stretch_mode = TextureRect.STRETCH_SCALE
	im.position = Vector2(r[0], r[1])
	im.size = Vector2(r[2], r[3])
	im.mouse_filter = Control.MOUSE_FILTER_IGNORE
	quadro.add_child(im)
	return im


func _rotulo(texto: String, tamanho: int, cor: Color, contorno := false) -> Label:
	var l := Label.new()
	l.text = texto
	var ls := LabelSettings.new()
	ls.font = _fonte
	ls.font_size = tamanho
	ls.font_color = cor
	if contorno:
		ls.outline_size = 10
		ls.outline_color = TEXTO
	l.label_settings = ls
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return l


## Texto centrado na largura de `pai`, com o centro vertical em centro.y.
func _texto(pai: Control, texto: String, tamanho: int, cor: Color, centro: Vector2, contorno := true) -> Label:
	var l := _rotulo(texto, tamanho, cor, contorno)
	l.position = Vector2(0, centro.y - tamanho)
	l.size = Vector2(pai.size.x, tamanho * 2)
	pai.add_child(l)
	return l


func _placa_nome(lugar: String) -> void:
	var l: Dictionary = _d["lugares"][lugar]
	var pw: float = _d["ui"]["placa_nome"][0]
	var ph: float = _d["ui"]["placa_nome"][1]
	var largura := maxf(pw, _fonte.get_string_size(l["rotulo"], HORIZONTAL_ALIGNMENT_LEFT, -1, 34).x + 60.0)
	var p := _imagem("placa_nome", [l["placa"][0] - largura / 2.0, l["placa"][1] - ph / 2.0, largura, ph])
	p.name = "placa_" + lugar
	p.mouse_filter = Control.MOUSE_FILTER_STOP     # tocar no nome também vale
	p.gui_input.connect(func(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed:
			_toca_lugar(lugar))
	_texto(p, l["rotulo"], 34, TEXTO, Vector2(0, ph / 2.0 - 4), false)


## Balão com as figurinhas dos cômodos (Casa e Casa na Árvore).
func _monta_balao() -> void:
	balao = PanelContainer.new()
	var st := StyleBoxFlat.new()
	st.bg_color = Color("#fff7ef")
	st.border_color = OUTLINE
	st.set_border_width_all(4)
	st.set_corner_radius_all(34)
	st.set_content_margin_all(22)
	st.shadow_color = Color(0.35, 0.15, 0.3, 0.25)
	st.shadow_size = 10
	st.shadow_offset = Vector2(0, 6)
	balao.add_theme_stylebox_override("panel", st)
	balao.visible = false
	balao.mouse_filter = Control.MOUSE_FILTER_STOP
	quadro.add_child(balao)
	for lugar in _d["ordem"]:
		var l: Dictionary = _d["lugares"][lugar]
		if l["destinos"].size() < 2:
			continue
		var fila := HBoxContainer.new()
		fila.name = lugar
		fila.add_theme_constant_override("separation", 18)
		fila.visible = false
		balao.add_child(fila)
		for dest in l["destinos"]:
			var col := VBoxContainer.new()
			col.add_theme_constant_override("separation", 2)
			fila.add_child(col)
			var b := _botao_imagem("res://assets/mapa/%s.png" % dest[0], Vector2(176, 132))
			b.pressed.connect(_escolhe.bind(dest[0]))
			col.add_child(b)
			figurinhas[dest[0]] = b
			var nome := _rotulo(dest[1], 26, TEXTO)
			nome.custom_minimum_size = Vector2(176, 36)
			col.add_child(nome)


# ---------------------------------------------------------------- abrir, fechar, escolher

func aberto() -> bool:
	return painel.visible


func abrir() -> void:
	painel.visible = true
	botao.visible = false
	_fecha_balao()
	_arruma()
	painel.modulate.a = 0.0
	create_tween().tween_property(painel, "modulate:a", 1.0, 0.15)


func fechar_mapa() -> void:
	_fecha_balao()
	painel.visible = false
	botao.visible = true


func _escolhe(cena: String) -> void:
	fechar_mapa()
	escolheu.emit(cena)


func _toca_lugar(lugar: String) -> void:
	var destinos: Array = _d["lugares"][lugar]["destinos"]
	if destinos.size() == 1:
		_escolhe(destinos[0][0])
	elif balao.visible and balao_de == lugar:
		_fecha_balao()
	else:
		_abre_balao(lugar)


func _abre_balao(lugar: String) -> void:
	balao_de = lugar
	for fila in balao.get_children():
		fila.visible = fila.name == lugar
	balao.visible = true
	balao.reset_size()
	var r: Array = _d["lugares"][lugar]["rect"]
	var tela := quadro.size
	var pos := Vector2(r[0] + r[2] / 2.0 - balao.size.x / 2.0, r[1] + r[3] * 0.25 - balao.size.y)
	pos.x = clampf(pos.x, 20.0, tela.x - balao.size.x - 20.0)
	pos.y = clampf(pos.y, 20.0, tela.y - balao.size.y - 20.0)
	balao.position = pos
	balao.pivot_offset = Vector2(balao.size.x / 2.0, balao.size.y)
	balao.scale = Vector2(0.6, 0.6)
	create_tween().tween_property(balao, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func _fecha_balao() -> void:
	if balao:
		balao.visible = false
	balao_de = ""


## Toque no gramado (fora dos lugares): fecha o balão; sem balão, não faz nada (o X fecha o mapa).
func _toque_no_mapa(e: InputEvent) -> void:
	if e is InputEventMouseButton and e.pressed:
		_fecha_balao()


# ---------------------------------------------------------------- tamanho e "você está aqui"

func _arruma() -> void:
	if quadro == null:
		return
	var s := minf(painel.size.x / quadro.size.x, painel.size.y / quadro.size.y)
	quadro.scale = Vector2(s, s)
	quadro.position = (painel.size - quadro.size * s) / 2.0
	var lugar: String = _lugar_da_cena.get(cena_atual, "")
	marcador.visible = lugar != ""
	if lugar != "":
		var r: Array = _d["lugares"][lugar]["rect"]
		var ponta: Array = _d["ui"]["marcador_ponta"]
		marcador.position = Vector2(r[0] + r[2] * ponta[0] - marcador.size.x / 2.0, r[1] + r[3] * ponta[1] - marcador.size.y)
		marcador.pivot_offset = Vector2(marcador.size.x / 2.0, marcador.size.y)
	painel.queue_redraw()


func _process(delta: float) -> void:
	if painel.visible and marcador.visible:
		_t += delta
		marcador.scale = Vector2.ONE * (1.0 + 0.06 * sin(_t * 4.0))
