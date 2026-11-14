class_name Lojinha
extends CanvasLayer
## Lojinha de enfeites: abre ao tocar na banca da Plantação (ou no botão da cestinha em cima dela).
## Cada cartão mostra o desenho do enfeite e o preço em ferradurinhas; tocar compra, se der.
## O que o nível ainda não liberou aparece com cadeado. Catálogo em dados/fazendinha.json ("loja").

signal comprou(tipo: String)

const OUTLINE := Color("#5b3a4f")
const CARTAO := Vector2(230, 250)

var fazenda: Fazendinha
var painel: Control
var cartoes := {}                 # tipo -> Button
var fechar: TextureButton


func _init() -> void:
	layer = 6


func preparar(p_fazenda: Fazendinha) -> Lojinha:
	fazenda = p_fazenda
	painel = Control.new()
	painel.set_anchors_preset(Control.PRESET_FULL_RECT)
	painel.mouse_filter = Control.MOUSE_FILTER_STOP   # com a lojinha aberta, nada atrás recebe toque
	painel.visible = false
	painel.draw.connect(_fundo)
	painel.resized.connect(_arruma)
	painel.gui_input.connect(func(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed:
			fechar_loja())
	add_child(painel)
	for tipo in fazenda.dados["loja"]["enfeites"]:
		var c := _cartao(str(tipo))
		painel.add_child(c)
		cartoes[tipo] = c
	fechar = TextureButton.new()
	fechar.texture_normal = load("res://assets/mapa/botao_fechar.png")
	fechar.ignore_texture_size = true
	fechar.stretch_mode = TextureButton.STRETCH_SCALE
	fechar.size = Vector2(96, 96)
	fechar.pressed.connect(fechar_loja)
	painel.add_child(fechar)
	return self


func _imagem(nome: String, tam: Vector2) -> TextureRect:
	var t := TextureRect.new()
	t.texture = load("res://assets/loja/%s.png" % nome)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.size = tam
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return t


func _cartao(tipo: String) -> Button:
	var d: Dictionary = fazenda.dados["loja"]["enfeites"][tipo]
	var b := Button.new()
	b.name = tipo
	b.size = CARTAO
	b.pivot_offset = CARTAO / 2.0
	b.focus_mode = Control.FOCUS_NONE
	var caixa := StyleBoxFlat.new()
	caixa.bg_color = Color("#fff7ea")
	caixa.border_color = OUTLINE
	caixa.set_border_width_all(5)
	caixa.set_corner_radius_all(26)
	for estilo in ["normal", "hover", "pressed", "disabled", "focus"]:
		b.add_theme_stylebox_override(estilo, caixa)
	var img := _imagem(tipo, Vector2(170, 150))
	img.position = Vector2(30, 18)
	b.add_child(img)
	var moeda := _imagem("ferradurinha", Vector2(52, 52))
	moeda.position = Vector2(48, 184)
	b.add_child(moeda)
	var preco := Label.new()
	preco.name = "Preco"
	preco.text = str(int(d["preco"]))
	preco.position = Vector2(108, 178)
	preco.add_theme_font_size_override("font_size", 46)
	preco.add_theme_color_override("font_color", OUTLINE)
	preco.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(preco)
	var cad := _imagem("cadeado", Vector2(80, 90))
	cad.name = "Cadeado"
	cad.position = Vector2(75, 50)
	b.add_child(cad)
	b.pressed.connect(_toque.bind(tipo))
	return b


func aberta() -> bool:
	return painel != null and painel.visible


func abrir() -> void:
	painel.visible = true
	atualizar()
	_arruma()
	painel.modulate.a = 0.0
	create_tween().tween_property(painel, "modulate:a", 1.0, 0.15)


func fechar_loja() -> void:
	painel.visible = false


## Cadeado no que o nível não liberou; mais apagado o que as ferradurinhas ainda não pagam.
func atualizar() -> void:
	for tipo in cartoes:
		var d: Dictionary = fazenda.dados["loja"]["enfeites"][tipo]
		var b: Button = cartoes[tipo]
		var liberado := fazenda.nivel >= int(d["nivel"])
		(b.get_node("Cadeado") as Control).visible = not liberado
		b.modulate = Color.WHITE if liberado and fazenda.ferraduras >= int(d["preco"]) else Color(1, 1, 1, 0.55)


func _toque(tipo: String) -> void:
	var b: Button = cartoes[tipo]
	if fazenda.comprar(tipo):
		comprou.emit(tipo)
		fechar_loja()  # a criança vê o enfeite novo cair ao lado da banca
	else:  # ainda não dá: o cartão só balança
		var tw := b.create_tween()
		for a in [-0.06, 0.06, -0.04, 0.0]:
			tw.tween_property(b, "rotation", a, 0.06)


func _arruma() -> void:
	if cartoes.is_empty():
		return
	var n := cartoes.size()
	var colunas := 5
	var linhas := int(ceil(n / float(colunas)))
	var folga := 26.0
	# os cartões encolhem em telas pequenas
	var e := minf(1.0, minf((painel.size.x - 120.0) / (colunas * (CARTAO.x + folga)), (painel.size.y - 200.0) / (linhas * (CARTAO.y + folga))))
	var passo := (CARTAO + Vector2(folga, folga)) * e
	var origem := (painel.size - Vector2(colunas, linhas) * passo) / 2.0 + Vector2(0, 30)
	var k := 0
	for tipo in cartoes:
		var b: Button = cartoes[tipo]
		b.scale = Vector2(e, e)
		b.pivot_offset = Vector2.ZERO
		b.position = origem + Vector2(k % colunas, k / colunas) * passo + Vector2(folga, folga) * e / 2.0
		k += 1
	fechar.position = Vector2(painel.size.x - 96 - 18, 18)
	painel.queue_redraw()


func _fundo() -> void:
	painel.draw_rect(Rect2(Vector2.ZERO, painel.size), Color(0.36, 0.23, 0.31, 0.45))
	var r := Rect2(40, 110, painel.size.x - 80, painel.size.y - 150)
	var caixa := StyleBoxFlat.new()
	caixa.bg_color = Color("#ffe3ef")
	caixa.border_color = OUTLINE
	caixa.set_border_width_all(6)
	caixa.set_corner_radius_all(40)
	painel.draw_style_box(caixa, r)
