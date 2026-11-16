class_name Sons
extends Node
## Sons curtinhos de retorno (toque, pegar, soltar, "não", moeda, passagem, bichinhos).
## Os WAVs ficam em assets/sons/ e são provisórios (ferramentas/sons/gerar_sons.py): um arquivo novo
## com o mesmo nome troca o som sem mexer no código. O jogo funciona igual com o iPad no mudo.
## Uso em qualquer script: Sons.tocar("moeda")  ou  Sons.bicho("bob")

const PASTA := "res://assets/sons/%s.wav"
const VOZES := 6                    # sons ao mesmo tempo
const VOLUME_DB := -6.0
const BICHOS := {
	"bob": "cachorro", "nina": "cachorro", "leo": "gato", "zoe": "gato", "lumi": "cavalo",
	"catarina": "pessoa", "carol": "pessoa",
}

static var _eu: Sons = null
var _players: Array[AudioStreamPlayer] = []
var _prox := 0
var _cache := {}


func _ready() -> void:
	_eu = self
	for i in VOZES:
		var p := AudioStreamPlayer.new()
		p.volume_db = VOLUME_DB
		add_child(p)
		_players.append(p)


static func tocar(nome: String, tom: float = 1.0) -> void:
	if _eu == null or not is_instance_valid(_eu):
		return
	_eu._tocar(nome, tom)


## O som de cada personagem quando a criança toca nele (com um tom um pouco diferente por bicho).
static func bicho(kind: String) -> void:
	var nome: String = BICHOS.get(kind, "toque")
	var tom := 1.0
	match kind:
		"nina": tom = 0.85
		"zoe": tom = 1.15
		"carol": tom = 0.85
	tocar(nome, tom * randf_range(0.96, 1.04))


func _tocar(nome: String, tom: float) -> void:
	if not _cache.has(nome):
		var path := PASTA % nome
		_cache[nome] = load(path) if ResourceLoader.exists(path) else null
	var s: AudioStream = _cache[nome]
	if s == null:
		return
	var p := _players[_prox]
	_prox = (_prox + 1) % _players.size()
	p.stream = s
	p.pitch_scale = tom
	p.play()
