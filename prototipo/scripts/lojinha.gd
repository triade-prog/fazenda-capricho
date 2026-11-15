class_name Lojinha
extends CanvasLayer
## Loja da fazenda: abre pelo botão da cestinha (embaixo da poltrona, em qualquer cenário) ou na
## banca da Plantação. Quatro abas por desenho, sem precisar ler: quintal (árvore), casa (poltrona),
## bichinhos (patinha) e construções (casinha). Cada cartão mostra o desenho do item, o preço em
## ferradurinhas e quantos já estão no baú; o que o nível ainda não abriu tem cadeado com o número do
## nível, e o que ainda não dá para pagar fica apagado e balança. Comprar manda o item para o baú
## (dá para comprar o mesmo item de novo). Item que acabou de abrir tem a estrelinha de novo.
## Catálogo em dados/itens.json.

signal comprou(tipo: String)

const OUTLINE := Color("#5b3a4f")
const CARTAO := Vector2(230, 250)
const COLUNAS := 5
const LINHAS := 2

var fazenda: Fazendinha
var painel: Control
var cartoes := {}                 # tipo -> Button (os da aba aberta)
var abas := {}                    # aba -> TextureButton
var aba := "quintal"
var pagina := 0
var fechar: TextureButton
var seta_esq: TextureButton
var seta_dir: TextureButton
var contador: Label


func _init() -> void:
	layer = 6


func preparar(p_fazenda: Fazendinha) -> Lojinha:
	fazenda = p_fazenda
	painel = Control.new()
	painel.set_anchors_preset(Control.PRESET_FULL_RECT)
	painel.mouse_filter = Control.MOUSE_FILTER_STOP   # com a loja aberta, nada atrás recebe toque
	painel.visible = false
	painel.draw.connect(_fundo)
	painel.resized.connect(_arruma)
	add_child(painel)
	for a in Itens.loja()["abas"]:
		var b := _botao_img(Itens.icone("aba_" + str(a)), Vector2(110, 110))
		b.pressed.connect(_trocar_aba.bind(str(a)))
		painel.add_child(b)
		abas[str(a)] = b
	fechar = _botao_img(load("res://assets/mapa/botao_fechar.png"), Vector2(96, 96))
	fechar.pressed.connect(fechar_loja)
	painel.add_child(fechar)
	seta_esq = _botao_img(Itens.icone("seta_esq"), Vector2(80, 80))
	seta_esq.pressed.connect(func() -> void: _virar(-1))
	painel.add_child(seta_esq)
	seta_dir = _botao_img(Itens.icone("seta_dir"), Vector2(80, 80))
	seta_dir.pressed.connect(func() -> void: _virar(1))
	painel.add_child(seta_dir)
	var moeda := _imagem("ferradurinha", Vector2(64, 64))
	moeda.name = "Moeda"
	painel.add_child(moeda)
	contador = Label.new()
	contador.add_theme_font_size_override("font_size", 54)
	contador.add_theme_color_override("font_color", OUTLINE)
	contador.mouse_filter = Control.MOUSE_FILTER_IGNORE
	painel.add_child(contador)
	_montar_aba()
	return self


func _botao_img(tex: Texture2D, tam: Vector2) -> TextureButton:
	var b := TextureButton.new()
	b.texture_normal = tex
	b.ignore_texture_size = true
	b.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	b.size = tam
	b.pivot_offset = tam / 2.0
	b.focus_mode = Control.FOCUS_NONE
	return b


func _imagem(nome: String, tam: Vector2) -> TextureRect:
	var t := TextureRect.new()
	t.texture = load("res://assets/loja/%s.png" % nome)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.size = tam
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return t


func _itens_da_aba() -> Array:
	var r := []
	for item in Itens.loja()["itens"]:
		if str(Itens.loja()["itens"][item]["aba"]) == aba:
			r.append(str(item))
	r.sort_custom(func(a: String, b: String) -> bool:
		var na := int(Itens.ficha(a)["nivel"])
		var nb := int(Itens.ficha(b)["nivel"])
		return na < nb or (na == nb and int(Itens.ficha(a)["preco"]) < int(Itens.ficha(b)["preco"])))
	return r


func _paginas() -> int:
	return maxi(1, int(ceil(float(_itens_da_aba().size()) / (COLUNAS * LINHAS))))


func _montar_aba() -> void:
	for t in cartoes:
		(cartoes[t] as Node).queue_free()
	cartoes.clear()
	var lista := _itens_da_aba()
	pagina = clampi(pagina, 0, _paginas() - 1)
	for k in range(pagina * COLUNAS * LINHAS, mini(lista.size(), (pagina + 1) * COLUNAS * LINHAS)):
		var c := _cartao(str(lista[k]))
		painel.add_child(c)
		cartoes[str(lista[k])] = c
	if painel.visible:
		atualizar()
	_arruma()


func _cartao(tipo: String) -> Button:
	var d: Dictionary = Itens.ficha(tipo)
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
	var img := TextureRect.new()
	img.texture = Itens.textura(tipo)
	img.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	img.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	img.size = Vector2(170, 150)
	img.position = Vector2(30, 18)
	img.mouse_filter = Control.MOUSE_FILTER_IGNORE
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
	cad.position = Vector2(75, 40)
	b.add_child(cad)
	var nv := Label.new()
	nv.name = "Nivel"
	nv.text = str(int(d["nivel"]))
	nv.size = Vector2(80, 50)
	nv.position = Vector2(75, 128)
	nv.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nv.add_theme_font_size_override("font_size", 40)
	nv.add_theme_color_override("font_color", OUTLINE)
	nv.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(nv)
	var tem := Label.new()
	tem.name = "Tem"
	tem.size = Vector2(70, 46)
	tem.position = Vector2(CARTAO.x - 78, 8)
	tem.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tem.add_theme_font_size_override("font_size", 32)
	tem.add_theme_color_override("font_color", Color.WHITE)
	var bola := StyleBoxFlat.new()
	bola.bg_color = Color("#ff6fae")
	bola.set_corner_radius_all(23)
	tem.add_theme_stylebox_override("normal", bola)
	tem.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(tem)
	var novo := TextureRect.new()
	novo.name = "Novo"
	novo.texture = Itens.icone("selo_novo")
	novo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	novo.size = Vector2(56, 56)
	novo.position = Vector2(4, 4)
	novo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(novo)
	b.pressed.connect(_toque.bind(tipo))
	return b


func aberta() -> bool:
	return painel != null and painel.visible


func abrir() -> void:
	painel.visible = true
	_montar_aba()
	atualizar()
	_arruma()
	painel.modulate.a = 0.0
	create_tween().tween_property(painel, "modulate:a", 1.0, 0.15)


func fechar_loja() -> void:
	painel.visible = false


func _trocar_aba(a: String) -> void:
	aba = a
	pagina = 0
	_montar_aba()


func _virar(d: int) -> void:
	pagina += d
	_montar_aba()


## Cadeado no que o nível não abriu; mais apagado o que as ferradurinhas ainda não pagam;
## quantos já estão no baú; estrelinha no que abriu e a criança ainda não viu (a partir daqui, viu).
func atualizar() -> void:
	var bau: Dictionary = fazenda.main.decoracao.bau if fazenda.main.decoracao else {}
	for tipo in cartoes:
		var d: Dictionary = Itens.ficha(tipo)
		var b: Button = cartoes[tipo]
		var liberado := fazenda.nivel >= int(d["nivel"])
		(b.get_node("Cadeado") as Control).visible = not liberado
		(b.get_node("Nivel") as Control).visible = not liberado
		var q := int(bau.get(tipo, 0))
		(b.get_node("Tem") as Label).text = "x%d" % q
		(b.get_node("Tem") as Control).visible = q > 0
		(b.get_node("Novo") as Control).visible = liberado and not fazenda.vistos.has(tipo)
		b.modulate = Color.WHITE if liberado and fazenda.ferraduras >= int(d["preco"]) else Color(1, 1, 1, 0.55)
		if liberado:
			fazenda.vistos[tipo] = true
	for a in abas:
		(abas[a] as Control).modulate = Color.WHITE if a == aba else Color(1, 1, 1, 0.55)
	contador.text = str(fazenda.ferraduras)


func _toque(tipo: String) -> void:
	var b: Button = cartoes[tipo]
	if fazenda.comprar(tipo):
		comprou.emit(tipo)
		fechar_loja()  # o item vai para o baú, e o modo Decorar abre com o baú aberto
	else:  # ainda não dá: o cartão só balança
		var tw := b.create_tween()
		for a in [-0.06, 0.06, -0.04, 0.0]:
			tw.tween_property(b, "rotation", a, 0.06)


func _arruma() -> void:
	if painel == null:
		return
	var folga := 26.0
	# os cartões encolhem em telas pequenas
	var e := minf(1.0, minf((painel.size.x - 260.0) / (COLUNAS * (CARTAO.x + folga)), (painel.size.y - 300.0) / (LINHAS * (CARTAO.y + folga))))
	e = maxf(e, 0.3)
	var passo := (CARTAO + Vector2(folga, folga)) * e
	var origem := (painel.size - Vector2(COLUNAS, LINHAS) * passo) / 2.0 + Vector2(0, 70)
	var k := 0
	for tipo in cartoes:
		var b: Button = cartoes[tipo]
		b.scale = Vector2(e, e)
		b.pivot_offset = Vector2.ZERO
		b.position = origem + Vector2(k % COLUNAS, k / COLUNAS) * passo + Vector2(folga, folga) * e / 2.0
		k += 1
	var n := abas.size()
	var x0 := painel.size.x / 2.0 - n * 130.0 / 2.0
	var i := 0
	for a in abas:
		(abas[a] as Control).position = Vector2(x0 + i * 130.0 + 10.0, 50.0)
		i += 1
	fechar.position = Vector2(painel.size.x - 96 - 18, 18)
	(painel.get_node("Moeda") as Control).position = Vector2(70, 70)
	contador.position = Vector2(140, 66)
	seta_esq.position = Vector2(50, painel.size.y / 2.0 + 30.0)
	seta_dir.position = Vector2(painel.size.x - 130.0, painel.size.y / 2.0 + 30.0)
	seta_esq.visible = pagina > 0
	seta_dir.visible = pagina < _paginas() - 1
	painel.queue_redraw()


func _fundo() -> void:
	painel.draw_rect(Rect2(Vector2.ZERO, painel.size), Color(0.36, 0.23, 0.31, 0.45))
	var r := Rect2(40, 40, painel.size.x - 80, painel.size.y - 70)
	var caixa := StyleBoxFlat.new()
	caixa.bg_color = Color("#ffe3ef")
	caixa.border_color = OUTLINE
	caixa.set_border_width_all(6)
	caixa.set_corner_radius_all(40)
	painel.draw_style_box(caixa, r)
