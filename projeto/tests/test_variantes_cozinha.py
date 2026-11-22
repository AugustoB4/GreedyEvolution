"""Cobertura funcional das variantes pizzaria e reator."""

import apoio
import os
import pygame
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from caminhos import INGREDIENTS_DIR, ORDERS_DIR, PINS_DIR
from constantes import PONTUACAOFACIL, TEMPOFACIL
from fase import Fase
from itens import (
    Alface,
    AlgaCosmica,
    ArrozEstelar,
    Carne,
    Pao,
    Queijo,
    Massa,
    PeixeNebuloso,
    Pizza,
    QueijoLunar,
    Sushi,
    Tomate,
    TomateNebuloso,
)
from jogo import Jogo
from mapa import MODELO1, MODELOS_MAPA, Mapa, VARIANTES_COZINHA
from montagem import Montagem
from pedido import (
    PEDIDOS_POR_VARIANTE,
    PedidoFacil,
    PedidoPizzaDificil,
    PedidoPizzaFacil,
    PedidoPizzaMedio,
    PedidoMedio,
    PedidoSushiDificil,
    PedidoSushiFacil,
    PedidoSushiMedio,
)
from player import alfaces, carnes, paos, queijos, tomates


INGREDIENTES_TEMATICOS = {
    "Dough": Massa,
    "MoonCheese": QueijoLunar,
    "NebulaTomato": TomateNebuloso,
    "StarRice": ArrozEstelar,
    "CosmicSeaweed": AlgaCosmica,
    "NebulaFish": PeixeNebuloso,
}

FONTES_CLASSICAS = {
    "Bread": "armarios",
    "Cheese": "armarios_queijo",
    "Tomato": "armarios_tomate",
    "Lettuce": "armarios_alface",
    "Meat": "geladeiras",
}

LISTAS_CLASSICAS = (tomates, alfaces, queijos, paos, carnes)


def criar_jogo(variante, classe_pedido):
    with patch(
        "jogo.sortear_variante",
        return_value=(variante, VARIANTES_COZINHA[variante]),
    ), patch("jogo.random.choice", side_effect=[MODELO1, classe_pedido]):
        return Jogo()


def largar_na_area(jogo, personagem, area):
    with patch.object(personagem, "area_interacao", return_value=area), patch(
        "player.som_solta"
    ):
        return personagem.largar(
            jogo.lixeiras,
            jogo.tomates,
            jogo.alfaces,
            jogo.queijos,
            jogo.paos,
            jogo.carnes,
            jogo.montagens,
            jogo.entregas,
            jogo.mapa.mapa,
            jogo.ingredientes_tematicos,
            jogo.produtos,
        )


def pegar_na_area(jogo, personagem, area):
    evento = pygame.event.Event(
        pygame.KEYDOWN, {"key": personagem.teclas["pegar"]}
    )
    with patch.object(personagem, "area_interacao", return_value=area), patch(
        "jogo.pygame.event.get", return_value=[evento]
    ), patch("player.som_pegar"):
        jogo.verificarEventos()


def executar_tecla_na_area(
    jogo, personagem, habilidade, area, pedido_seguinte=None
):
    evento = pygame.event.Event(
        pygame.KEYDOWN, {"key": personagem.teclas[habilidade]}
    )
    with patch.object(personagem, "area_interacao", return_value=area), patch(
        "jogo.pygame.event.get", return_value=[evento]
    ):
        if pedido_seguinte is None:
            jogo.verificarEventos()
        else:
            with patch("jogo.random.choice", return_value=pedido_seguinte):
                jogo.verificarEventos()


def ingrediente_pronto(nome):
    ingrediente = INGREDIENTES_TEMATICOS[nome](0, 0)
    if nome == "StarRice":
        ingrediente.cru = False
        ingrediente.cozido = True
    elif ingrediente.corte:
        ingrediente.cortado = True
    return ingrediente


class TestIngredientesTematicos(unittest.TestCase):
    def test_ingredientes_tematicos_usam_sprites_existentes_e_preparos_previstos(self):
        for nome, classe in INGREDIENTES_TEMATICOS.items():
            with self.subTest(ingrediente=nome):
                ingrediente = classe(0, 0)
                self.assertTrue(Path(ingrediente.sprite_path).is_file())
                self.assertEqual(ingrediente.nome, nome)
                if ingrediente.corte:
                    sprite_cortado = Path(INGREDIENTS_DIR) / f"Sliced{nome}.png"
                    self.assertTrue(sprite_cortado.is_file())

        arroz = ArrozEstelar(0, 0)
        self.assertEqual(arroz.metodo_preparo, "cozinhar")
        self.assertFalse(arroz.corte)
        self.assertTrue(arroz.cru)
        self.assertFalse(arroz.cozido)

    def test_arroz_cozinha_e_troca_para_o_sprite_existente(self):
        arroz = ArrozEstelar(0, 0)
        arroz.cont = 499
        forno = SimpleNamespace(rect=pygame.Rect(arroz.rect))

        arroz.preparar_ingrediente([forno])

        sprite_cozido = pygame.transform.scale(
            pygame.image.load(
                os.path.join(INGREDIENTS_DIR, "CookedStarRice.png")
            ).convert_alpha(),
            (32, 32),
        )
        self.assertEqual(arroz.cont, 500)
        self.assertFalse(arroz.cru)
        self.assertTrue(arroz.cozido)
        self.assertEqual(
            pygame.image.tostring(arroz.sprite, "RGBA"),
            pygame.image.tostring(sprite_cozido, "RGBA"),
        )

    def test_produtos_tematicos_carregam_as_imagens_da_receita(self):
        produtos = (
            (Pizza(0, 0, "pizza_facil"), "1Pizza.png"),
            (Pizza(0, 0, "pizza_medio"), "2Pizza.png"),
            (Pizza(0, 0, "pizza_dificil"), "3Pizza.png"),
            (Sushi(0, 0, "sushi_facil"), "1Sushi.png"),
            (Sushi(0, 0, "sushi_medio"), "2Sushi.png"),
            (Sushi(0, 0, "sushi_dificil"), "3Sushi.png"),
        )
        for produto, sprite in produtos:
            with self.subTest(produto=produto.receita_id):
                self.assertEqual(Path(produto.sprite_path).name, sprite)
                self.assertTrue(Path(produto.sprite_path).is_file())


class TestReceitasTematicas(unittest.TestCase):
    def test_pedidos_tematicos_incluem_familia_receita_preparo_dificuldade_e_recompensa(self):
        pedidos = (
            (PedidoPizzaFacil, "pizza_facil", "pizza", "fácil", "1Pizza.png"),
            (PedidoPizzaMedio, "pizza_medio", "pizza", "médio", "2Pizza.png"),
            (PedidoPizzaDificil, "pizza_dificil", "pizza", "difícil", "3Pizza.png"),
            (PedidoSushiFacil, "sushi_facil", "sushi", "fácil", "1Sushi.png"),
            (PedidoSushiMedio, "sushi_medio", "sushi", "médio", "2Sushi.png"),
            (PedidoSushiDificil, "sushi_dificil", "sushi", "difícil", "3Sushi.png"),
        )
        for classe, receita_id, familia, dificuldade, sprite in pedidos:
            with self.subTest(receita=receita_id):
                pedido = classe()
                self.assertEqual(pedido.receita_id, receita_id)
                self.assertEqual(pedido.id, receita_id)
                self.assertEqual(pedido.familia, familia)
                self.assertEqual(pedido.produto_classe.__name__, familia.title())
                self.assertEqual(pedido.dificuldade, dificuldade)
                self.assertGreater(pedido.sprite.get_width(), 0)
                self.assertTrue(pedido.ingredientes)
                self.assertTrue(pedido.ingrediente_ids)
                self.assertTrue(pedido.preparos)
                self.assertTrue(Path(ORDERS_DIR, sprite).is_file())

        self.assertEqual(PedidoPizzaFacil().tempo, TEMPOFACIL)
        self.assertEqual(PedidoPizzaFacil().pontuacao, PONTUACAOFACIL)
        self.assertEqual(PedidoSushiFacil().tempo, TEMPOFACIL)
        self.assertEqual(PedidoSushiFacil().pontuacao, PONTUACAOFACIL)
        self.assertEqual(
            PedidoSushiDificil().ingrediente_ids.count("NebulaFish"), 2
        )

    def test_todas_as_receitas_validas_montam_o_produto_e_sprite_corretos(self):
        expected_sprites = {
            "pizza_facil": "1Pizza.png",
            "pizza_medio": "2Pizza.png",
            "pizza_dificil": "3Pizza.png",
            "sushi_facil": "1Sushi.png",
            "sushi_medio": "2Sushi.png",
            "sushi_dificil": "3Sushi.png",
        }
        for classes in PEDIDOS_POR_VARIANTE.values():
            if classes[0].__name__ == "PedidoFacil":
                continue
            for classe_pedido in classes:
                pedido = classe_pedido()
                montagem = Montagem(0, 0, pedido)
                for nome in pedido.ingrediente_ids:
                    self.assertTrue(
                        montagem.adicionar_ingrediente(
                            ingrediente_pronto(nome), "1"
                        )
                    )

                with self.subTest(receita=pedido.receita_id):
                    self.assertTrue(montagem.produto_pronto)
                    produto = montagem.pegar_ingrediente()
                    self.assertIsInstance(produto, pedido.produto_classe)
                    self.assertEqual(produto.receita_id, pedido.receita_id)
                    self.assertEqual(
                        Path(produto.sprite_path).name,
                        expected_sprites[pedido.receita_id],
                    )

    def test_montagem_recusa_ordem_errada_e_arroz_cru(self):
        pedido_pizza = PedidoPizzaMedio()
        montagem_pizza = Montagem(0, 0, pedido_pizza)
        for nome in reversed(pedido_pizza.ingrediente_ids):
            self.assertTrue(
                montagem_pizza.adicionar_ingrediente(
                    ingrediente_pronto(nome), "1"
                )
            )
        self.assertFalse(montagem_pizza.produto_pronto)

        pedido_sushi = PedidoSushiFacil()
        montagem_sushi = Montagem(0, 0, pedido_sushi)
        arroz_cru = ArrozEstelar(0, 0)
        alga_cortada = ingrediente_pronto("CosmicSeaweed")
        montagem_sushi.adicionar_ingrediente(arroz_cru, "1")
        montagem_sushi.adicionar_ingrediente(alga_cortada, "1")
        self.assertFalse(montagem_sushi.produto_pronto)

    def test_troca_de_pedido_revalida_duas_montagens_nas_tres_cozinhas(self):
        classes_ingredientes = {
            "Bread": Pao,
            "Cheese": Queijo,
            "Meat": Carne,
            "Tomato": Tomate,
            "Lettuce": Alface,
            **INGREDIENTES_TEMATICOS,
        }

        def montar(pedido):
            montagem = Montagem(0, 0, pedido)
            for nome in pedido.ingrediente_ids:
                ingrediente = classes_ingredientes[nome](0, 0)
                if nome == "Meat":
                    ingrediente.assado = True
                    ingrediente.cru = False
                elif ingrediente.metodo_preparo == "cozinhar":
                    ingrediente.cozido = True
                    ingrediente.cru = False
                else:
                    ingrediente.cortado = True
                self.assertTrue(montagem.adicionar_ingrediente(ingrediente, "1"))
            return montagem

        casos = (
            (PedidoFacil, PedidoMedio),
            (PedidoPizzaFacil, PedidoPizzaMedio),
            (PedidoSushiFacil, PedidoSushiMedio),
        )
        for classe_antiga, classe_nova in casos:
            with self.subTest(cozinha=classe_antiga.__name__):
                pedido_antigo = classe_antiga()
                pedido_novo = classe_nova()
                montagens = [montar(pedido_antigo) for _ in range(2)]
                conteudos_anteriores = [
                    [item.nome for item in montagem.ingredientes]
                    for montagem in montagens
                ]
                self.assertTrue(all(m.hamburguer_pronto for m in montagens))

                for montagem in montagens:
                    montagem.pedido = pedido_novo

                self.assertTrue(all(not m.hamburguer_pronto for m in montagens))
                self.assertEqual(
                    [
                        [item.nome for item in montagem.ingredientes]
                        for montagem in montagens
                    ],
                    conteudos_anteriores,
                )

                for montagem in montagens:
                    montagem.pedido = pedido_antigo
                self.assertTrue(all(m.hamburguer_pronto for m in montagens))
                produto = montagens[0].pegar_ingrediente()
                self.assertEqual(produto.receita_id, pedido_antigo.receita_id)


class TestDispensadoresTematicos(unittest.TestCase):
    def test_todos_os_modelos_tem_slots_para_as_estacoes_de_cada_cozinha(self):
        for modelo in MODELOS_MAPA:
            simbolos = set("".join(modelo))
            self.assertTrue({"3", "4", "T"}.issubset(simbolos))
            self.assertTrue({"3", "4", "R"}.issubset(simbolos))

    def test_dispensadores_tematicos_criam_itens_e_indicadores_por_estilo(self):
        casos = (
            (
                "pizzaria",
                PedidoPizzaFacil,
                {"Dough": Massa, "MoonCheese": QueijoLunar, "NebulaTomato": TomateNebuloso},
            ),
            (
                "reator",
                PedidoSushiFacil,
                {"StarRice": ArrozEstelar, "CosmicSeaweed": AlgaCosmica, "NebulaFish": PeixeNebuloso},
            ),
        )
        for variante, classe_pedido, ingredientes_esperados in casos:
            with self.subTest(variante=variante):
                jogo = criar_jogo(variante, classe_pedido)
                fontes = jogo.mapa.dispensadores_tematicos
                self.assertEqual(
                    {fonte.nome_ingrediente for fonte in fontes},
                    set(ingredientes_esperados),
                )
                self.assertTrue(jogo.mapa.armarios == [])
                self.assertTrue(jogo.mapa.geladeiras == [])

                personagem = jogo.player1
                for fonte in fontes:
                    self.assertIn(fonte.rect, jogo.mapa.colisoes)
                    self.assertTrue(
                        Path(PINS_DIR, variante, fonte.pin).is_file()
                    )
                    area = fonte.rect.copy()
                    with patch.object(
                        personagem, "area_interacao", return_value=area
                    ):
                        personagem.verificar_indicador(
                            jogo.lixeiras,
                            jogo.armarios,
                            jogo.armarios_queijo,
                            jogo.armarios_tomate,
                            jogo.armarios_alface,
                            jogo.geladeiras,
                            jogo.tomates,
                            jogo.alfaces,
                            jogo.queijos,
                            jogo.paos,
                            jogo.carnes,
                            fontes,
                            jogo.ingredientes_tematicos,
                            jogo.produtos,
                        )
                    self.assertEqual(personagem.indicador.nome, fonte.pin)

                    personagem.objeto = None
                    pegar_na_area(jogo, personagem, area)
                    ingrediente = personagem.objeto
                    self.assertIsInstance(
                        ingrediente, ingredientes_esperados[fonte.nome_ingrediente]
                    )
                    self.assertIs(ingrediente.dono, personagem)
                    self.assertIn(
                        ingrediente,
                        jogo.ingredientes_tematicos[fonte.nome_ingrediente],
                    )
                    jogo.ingredientes_tematicos[fonte.nome_ingrediente].remove(
                        ingrediente
                    )
                    personagem.objeto = None


class TestFluxosVariantes(unittest.TestCase):
    def test_ciclo_completo_de_entrega_nas_tres_cozinhas(self):
        casos = (
            ("classica", PedidoFacil),
            ("pizzaria", PedidoPizzaFacil),
            ("reator", PedidoSushiFacil),
        )
        snapshots = [list(lista) for lista in LISTAS_CLASSICAS]

        def restaurar_listas_classicas():
            for lista, snapshot in zip(LISTAS_CLASSICAS, snapshots):
                lista.clear()
                lista.extend(snapshot)

        self.addCleanup(restaurar_listas_classicas)
        for lista in LISTAS_CLASSICAS:
            lista.clear()

        for variante, classe_pedido in casos:
            with self.subTest(variante=variante):
                jogo = criar_jogo(variante, classe_pedido)
                pedido = jogo.pedido_atual
                personagem = jogo.player1
                montagem = jogo.montagens[0]

                for nome in pedido.ingrediente_ids:
                    if nome in FONTES_CLASSICAS:
                        fonte = getattr(jogo, FONTES_CLASSICAS[nome])[0]
                    else:
                        fonte = next(
                            fonte
                            for fonte in jogo.mapa.dispensadores_tematicos
                            if fonte.nome_ingrediente == nome
                        )
                    pegar_na_area(jogo, personagem, fonte.rect.copy())
                    ingrediente = personagem.objeto
                    self.assertEqual(ingrediente.nome, nome)

                    if ingrediente.metodo_preparo == "cortar":
                        tabua = jogo.mapa.tabuas[0]
                        with patch.object(
                            personagem,
                            "area_interacao",
                            return_value=tabua.rect.copy(),
                        ), patch("player.som_corte"):
                            personagem.cortar(
                                jogo.mapa.tabuas,
                                jogo.tomates,
                                jogo.alfaces,
                                jogo.queijos,
                                jogo.paos,
                                jogo.carnes,
                                jogo.ingredientes_tematicos,
                            )
                        self.assertTrue(ingrediente.cortado)
                    elif ingrediente.metodo_preparo in ("assar", "cozinhar"):
                        forno = jogo.mapa.fornos[0]
                        largar_na_area(jogo, personagem, forno.rect.copy())
                        self.assertIsNone(personagem.objeto)
                        ingrediente.cont = 499
                        ingrediente.preparar_ingrediente(jogo.mapa.fornos)
                        self.assertTrue(
                            ingrediente.assado or ingrediente.cozido
                        )
                        pegar_na_area(jogo, personagem, forno.rect.copy())
                        self.assertIs(personagem.objeto, ingrediente)

                    largar_na_area(jogo, personagem, montagem.rect.copy())
                    self.assertIsNone(personagem.objeto)

                self.assertTrue(montagem.produto_pronto)
                pegar_na_area(jogo, personagem, montagem.rect.copy())
                produto = personagem.objeto
                self.assertIsInstance(produto, pedido.produto_classe)
                self.assertEqual(produto.receita_id, pedido.receita_id)

                executar_tecla_na_area(
                    jogo,
                    personagem,
                    "largar",
                    jogo.entregas[0].rect.copy(),
                    PEDIDOS_POR_VARIANTE[jogo.tipo_pedido][0],
                )

                self.assertEqual(jogo.fase.tempo, 60 + TEMPOFACIL)
                self.assertEqual(jogo.fase.pontuacao, PONTUACAOFACIL)
                self.assertEqual(jogo.pedido_atual.familia, pedido.familia)
                self.assertIsNone(personagem.objeto)
                jogo.desenhar()

    def test_entrega_pune_produtos_de_outra_cozinha_ou_receita(self):
        jogo = object.__new__(Jogo)
        jogo.tipo_pedido = "pizza"
        jogo.pedido_atual = PedidoPizzaMedio()
        jogo.fase = Fase(tempo=100, pontuacao=50)
        jogo.montagens = [SimpleNamespace(pedido=jogo.pedido_atual)]
        produto_errado = Pizza(0, 0, "pizza_facil")
        pedido_medio = jogo.pedido_atual

        with patch("jogo.random.choice", return_value=PedidoPizzaFacil):
            jogo.processar_entrega(produto_errado)
        self.assertEqual(jogo.fase.tempo, 100 - pedido_medio.tempo // 2)
        self.assertEqual(jogo.fase.pontuacao, 35)

        jogo.pedido_atual = PedidoPizzaFacil()
        jogo.fase = Fase(tempo=100, pontuacao=50)
        produto_sushi = Sushi(0, 0, "sushi_facil")
        with patch("jogo.random.choice", return_value=PedidoPizzaFacil):
            jogo.processar_entrega(produto_sushi)
        self.assertEqual(jogo.fase.tempo, 100 - TEMPOFACIL // 2)
        self.assertEqual(jogo.fase.pontuacao, 50 - PONTUACAOFACIL)


if __name__ == "__main__":
    unittest.main()
