"""Vida nos cenários: peças que se mexem sozinhas, móveis de puxar e objetos de pegar, por cenário.

O para_jogo.py junta isto ao JOGO de cada módulo. Tipos de animação (scripts/cenario.gd):
fogo (crepita), agua (escorre), ondula, gira, balanca (pêndulo; pivo "topo" ou "base"), flutua (sobe e desce; "lado" = vai e vem).
"so_se" = {peça: [interativo, estado]}: a peça só aparece quando o interativo está naquele estado.
"moveis" são peças que a criança puxa de lado e onde os personagens sentam.
"""
VIDA = {
    "sala": {"objetos": ["almofada_rosa", "almofada_lilas", "livro_rosa", "livro_azul"],
             "superficies": [[1262, 1678, 512]]},
    "cozinha": {"animacoes": {"vapor": {"tipo": "flutua", "amp": 4, "vel": 2.6, "lado": 3},
                              "@torneira": {"tipo": "agua", "estado": 1}},
                "so_se": {"vapor": ["fogao", 1]}},
    "entrada": {"animacoes": {"moinho_helice": {"tipo": "gira", "vel": 0.9}}},
    "sede": {"animacoes": {"rede": {"tipo": "balanca", "amp": 0.025, "vel": 1.3}},
             "moveis": ["cadeira_deck"]},
    "casa_arvore": {"animacoes": {"balanco_assento": {"tipo": "balanca", "amp": 0.09, "vel": 1.8}}},
    "casa_arvore_dentro": {"animacoes": {"@passarinho": {"tipo": "flutua", "amp": 5, "vel": 3.0}},
                           "moveis": ["cadeirinha"]},
    "casinha": {"moveis": ["cadeirinha"]},
    "quarto_carol": {"moveis": ["banquinho"], "objetos": ["travesseiro"]},
    "estabulo": {"moveis": ["fardo"], "animacoes": {"@laguinho": {"tipo": "ondula", "estado": 1}}},
    "plantacao": {"animacoes": {"espantalho": {"tipo": "balanca", "pivo": "base", "amp": 0.03, "vel": 1.4},
                                "@borboleta": {"tipo": "flutua", "amp": 10, "vel": 2.4, "lado": 14},
                                "@abelha": {"tipo": "flutua", "amp": 6, "vel": 4.0, "lado": 10},
                                "minhoca": {"tipo": "flutua", "amp": 0, "vel": 3.0, "lado": 5}},
                  "moveis": ["carrinho"]},
    "pet_care": {"animacoes": {"bolha": {"tipo": "flutua", "amp": 9, "vel": 1.8, "lado": 4}}},
    "cabana": {"animacoes": {"passarinho": {"tipo": "flutua", "amp": 5, "vel": 3.0}, "chama": {"tipo": "fogo"}},
               "so_se": {"chama": ["fogueira", 1]},
               "moveis": ["tronco_banco"]},
}


def juntar(cena, jogo):
    v = VIDA.get(cena, {})
    jogo.setdefault("animacoes", {}).update(v.get("animacoes", {}))
    jogo["moveis"] = list(jogo.get("moveis", [])) + v.get("moveis", [])
    jogo["objetos"] = list(jogo.get("objetos", [])) + v.get("objetos", [])
    jogo.setdefault("so_se", {}).update(v.get("so_se", {}))
    jogo["superficies"] = list(jogo["superficies"]) + v.get("superficies", [])
