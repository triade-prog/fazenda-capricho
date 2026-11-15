class_name AvisoTelaInicio
extends CanvasLayer
## Dica para os pais: no iPad, o Safari pode apagar o que um site guardou se ele ficar 7 dias sem
## ser aberto. Pelo ícone na Tela de Início isso não acontece. A dica aparece só no navegador do
## iPad/iPhone (não no ícone da Tela de Início), no máximo uma vez por dia, e some com um toque.

static var arquivo := "user://avisos.json"

const OUTLINE := Color("#5b3a4f")

var painel: Control


func _init() -> void:
	layer = 9


## true quando vale mostrar: jogo na web, num iPad/iPhone, aberto pelo Safari (não pelo ícone).
static func precisa() -> bool:
	if not OS.has_feature("web"):
		return false
	var js := "(function(){var ios=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);" + \
		"var sozinho=(window.navigator.standalone===true)||window.matchMedia('(display-mode: standalone)').matches;return ios&&!sozinho;})()"
	return bool(JavaScriptBridge.eval(js, true))


## Mostra a dica se ainda não apareceu hoje.
func talvez_mostrar(forcar := false) -> bool:
	if not forcar and not precisa():
		return false
	var hoje := Time.get_date_string_from_system()
	var d := _ler()
	if not forcar and str(d.get("tela_inicio", "")) == hoje:
		return false
	d["tela_inicio"] = hoje
	var f := FileAccess.open(arquivo, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(d))
	_montar()
	return true


func aberto() -> bool:
	return painel != null and painel.visible


func fechar() -> void:
	if painel:
		painel.visible = false


func _ler() -> Dictionary:
	if not FileAccess.file_exists(arquivo):
		return {}
	var d: Variant = JSON.parse_string(FileAccess.get_file_as_string(arquivo))
	return d if d is Dictionary else {}


func _montar() -> void:
	painel = Control.new()
	painel.set_anchors_preset(Control.PRESET_FULL_RECT)
	painel.mouse_filter = Control.MOUSE_FILTER_STOP
	painel.gui_input.connect(func(e: InputEvent) -> void:
		if (e is InputEventMouseButton and e.pressed) or (e is InputEventScreenTouch and e.pressed):
			fechar())
	add_child(painel)
	var fundo := ColorRect.new()
	fundo.color = Color(0.36, 0.23, 0.31, 0.45)
	fundo.set_anchors_preset(Control.PRESET_FULL_RECT)
	fundo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	painel.add_child(fundo)
	var caixa := PanelContainer.new()
	var estilo := StyleBoxFlat.new()
	estilo.bg_color = Color("#fff7ea")
	estilo.border_color = OUTLINE
	estilo.set_border_width_all(6)
	estilo.set_corner_radius_all(36)
	estilo.set_content_margin_all(36)
	caixa.add_theme_stylebox_override("panel", estilo)
	caixa.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caixa.set_anchors_preset(Control.PRESET_CENTER)
	caixa.custom_minimum_size = Vector2(760, 0)
	painel.add_child(caixa)
	var coluna := VBoxContainer.new()
	coluna.add_theme_constant_override("separation", 18)
	coluna.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caixa.add_child(coluna)
	for linha in [["Para não perder a fazenda", 46], ["No Safari, toque em Compartilhar (o quadradinho com a seta para cima) e depois em \"Adicionar à Tela de Início\". Jogue sempre pelo ícone que aparecer.", 30], ["Pelo Safari, o iPad pode apagar o jogo salvo se ficar 7 dias sem abrir.", 26], ["Toque para continuar", 28]]:
		var l := Label.new()
		l.text = str(linha[0])
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.custom_minimum_size = Vector2(680, 0)
		l.add_theme_font_size_override("font_size", int(linha[1]))
		l.add_theme_color_override("font_color", OUTLINE)
		l.mouse_filter = Control.MOUSE_FILTER_IGNORE
		coluna.add_child(l)
	# centraliza depois de saber o tamanho
	caixa.resized.connect(func() -> void:
		caixa.position = (painel.size - caixa.size) / 2.0)
	painel.resized.connect(func() -> void:
		caixa.position = (painel.size - caixa.size) / 2.0)
