"""Testes de referência para ingredientes, montagem, pedidos e entrega clássica."""

import apoio
import pygame
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from constantes import (
    PONTUACAODIFICIL,
    PONTUACAOFACIL,
    PONTUACAOMEDIO,
    TEMPODIFICIL,
    TEMPOFACIL,
    TEMPOMEDIO,
)
from fase import Fase
from itens import Alface, ArrozEstelar, Carne, Hamburguer, Pao, Queijo, Tomate
from jogo import Jogo
from montagem import Montagem
from pedido import PedidoDificil, PedidoFacil, PedidoMedio


CLASSES_INGREDIENTES = {
    "Pão": Pao,
    "Queijo": Queijo,
    "Carne": Carne,
    "Tomate": Tomate,
    "Alface": Alface,
}


def criar_ingrediente_preparado(nome, preparo_carne="assada"):
    ingrediente = CLASSES_INGREDIENTES[nome](0, 0)
    if ingrediente.nome == "Meat":
        ingrediente.cru = preparo_carne == "crua"
        ingrediente.assado = preparo_carne == "assada"
        ingrediente.queimado = preparo_carne == "queimada"
    else:
        ingrediente.cortado = True
    return ingrediente


def criar_montagem(pedido, nomes=None, preparo_carne="assada"):
    montagem = Montagem(0, 0, pedido)
    nomes = pedido.ingredientes if nomes is None else nomes

    for nome in nomes:
        ingrediente = criar_ingrediente_preparado(nome, preparo_carne)
        if not montagem.adicionar_ingrediente(ingrediente, "1"):
            raise AssertionError(f"Não foi possível inserir {nome}")

    return montagem


def criar_jogo_minimo(pedido, montagens=None):
    jogo = object.__new__(Jogo)
    jogo.pedido_atual = pedido
    jogo.fase = Fase(tempo=90, pontuacao=40)
    jogo.montagens = montagens or [
        SimpleNamespace(pedido=pedido),
        SimpleNamespace(pedido=pedido),
    ]
    return jogo


class TestIngredientesClassicos(unittest.TestCase):
    def test_cinco_ingredientes_comecam_no_estado_inicial(self):
        for nome, classe in CLASSES_INGREDIENTES.items():
            with self.subTest(ingrediente=nome):
                ingrediente = classe(0, 0)
                self.assertTrue(ingrediente.corte)
                self.assertTrue(ingrediente.cru)
                self.assertFalse(ingrediente.assado)
                self.assertFalse(ingrediente.queimado)
                self.assertFalse(ingrediente.cortado)
                self.assertIsNone(ingrediente.dono)
                self.assertFalse(ingrediente.em_montagem)

    def test_cortar_ingredientes_marca_estado_e_e_idempotente(self):
        for nome, classe in CLASSES_INGREDIENTES.items():
            with self.subTest(ingrediente=nome):
                ingrediente = classe(0, 0)
                ingrediente.cortar_ingrediente()
                ingrediente.cortar_ingrediente()
                self.assertTrue(ingrediente.cortado)

    def test_carne_transita_de_crua_para_assada_no_forno(self):
        carne = Carne(0, 0)
        forno = SimpleNamespace(rect=pygame.Rect(carne.rect))
        carne.cont = 499

        carne.assar_ingrediente([forno])

        self.assertEqual(carne.cont, 500)
        self.assertFalse(carne.cru)
        self.assertTrue(carne.assado)
        self.assertFalse(carne.queimado)

    def test_carne_transita_de_assada_para_queimada_no_limite(self):
        carne = Carne(0, 0)
        carne.assado = True
        carne.cru = False
        carne.cont = 799
        forno = SimpleNamespace(rect=pygame.Rect(carne.rect))

        carne.assar_ingrediente([forno])

        self.assertTrue(carne.queimado)
        self.assertFalse(carne.assado)
        self.assertFalse(carne.cru)

    def test_carne_nao_avanca_preparo_fora_do_forno(self):
        carne = Carne(0, 0)
        carne.cont = 499

        carne.assar_ingrediente([])

        self.assertEqual(carne.cont, 499)
        self.assertTrue(carne.cru)
        self.assertFalse(carne.assado)
        self.assertFalse(carne.queimado)

    def test_carne_e_arroz_mantem_duracao_em_30_e_60_fps(self):
        for dt in (1 / 60, 1 / 30):
            with self.subTest(fps=round(1 / dt)):
                carne = Carne(0, 0)
                arroz = ArrozEstelar(0, 0)
                forno_carne = SimpleNamespace(rect=pygame.Rect(carne.rect))
                forno_arroz = SimpleNamespace(rect=pygame.Rect(arroz.rect))
                tempo_carne = 0.0
                tempo_arroz = 0.0

                with patch("itens.som_forno"):
                    while not carne.assado:
                        carne.assar_ingrediente([forno_carne], dt)
                        tempo_carne += dt
                    while not arroz.cozido:
                        arroz.preparar_ingrediente([forno_arroz], dt)
                        tempo_arroz += dt

                    while not carne.queimado:
                        carne.assar_ingrediente([forno_carne], dt)
                        tempo_carne += dt

                self.assertAlmostEqual(tempo_arroz, 500 / 60, delta=dt)
                self.assertAlmostEqual(tempo_carne, 800 / 60, delta=dt)
                self.assertTrue(carne.queimado)
                self.assertTrue(arroz.cozido)


class TestMontagemClassica(unittest.TestCase):
    def test_insercao_marca_ingrediente_e_recusa_repeticao(self):
        montagem = Montagem(10, 20)
        pao = Pao(100, 100)
        pao.dono = object()

        self.assertTrue(montagem.adicionar_ingrediente(pao, "1"))
        self.assertFalse(montagem.adicionar_ingrediente(pao, "1"))
        self.assertEqual(montagem.ingredientes, [pao])
        self.assertIsNone(pao.dono)
        self.assertTrue(pao.em_montagem)

    def test_montagem_limita_a_cinco_ingredientes(self):
        montagem = Montagem(0, 0)
        ingredientes = [classe(0, 0) for classe in CLASSES_INGREDIENTES.values()]

        for ingrediente in ingredientes:
            self.assertTrue(montagem.adicionar_ingrediente(ingrediente, "1"))

        sexto = Tomate(0, 0)
        self.assertFalse(montagem.adicionar_ingrediente(sexto, "1"))
        self.assertEqual(len(montagem.ingredientes), 5)
        self.assertFalse(sexto.em_montagem)

    def test_retirada_remove_o_ultimo_e_preserva_a_ordem_restante(self):
        montagem = Montagem(0, 0)
        ingredientes = [Pao(0, 0), Queijo(0, 0), Carne(0, 0)]
        for ingrediente in ingredientes:
            montagem.adicionar_ingrediente(ingrediente, "1")

        retirado = montagem.pegar_ingrediente()

        self.assertIs(retirado, ingredientes[-1])
        self.assertEqual(montagem.ingredientes, ingredientes[:2])
        self.assertFalse(retirado.em_montagem)

    def test_montagem_recusa_inserir_hamburguer_pronto_como_ingrediente(self):
        montagem = Montagem(0, 0)

        self.assertFalse(
            montagem.adicionar_ingrediente(Hamburguer(0, 0), "1")
        )
        self.assertEqual(montagem.ingredientes, [])

    def test_receitas_validas_geram_hamburguer_com_os_ingredientes_corretos(self):
        receitas = (
            (PedidoFacil, False, False),
            (PedidoMedio, True, False),
            (PedidoDificil, True, True),
        )
        for classe_pedido, com_tomate, com_alface in receitas:
            with self.subTest(pedido=classe_pedido.__name__):
                montagem = criar_montagem(classe_pedido())
                self.assertTrue(montagem.hamburguer_pronto)

                hamburguer = montagem.pegar_ingrediente()

                self.assertIsInstance(hamburguer, Hamburguer)
                self.assertEqual(hamburguer.com_tomate, com_tomate)
                self.assertEqual(hamburguer.com_alface, com_alface)
                self.assertEqual(montagem.ingredientes, [])

    def test_receitas_invalidas_por_ordem_ou_estado_da_carne_nao_ficam_prontas(self):
        casos = (
            (PedidoFacil(), ["Queijo", "Pão", "Carne"], "assada"),
            (PedidoFacil(), None, "crua"),
            (PedidoFacil(), None, "queimada"),
        )
        for pedido, nomes, preparo_carne in casos:
            with self.subTest(nomes=nomes, preparo_carne=preparo_carne):
                montagem = criar_montagem(pedido, nomes, preparo_carne)
                self.assertFalse(montagem.hamburguer_pronto)


class TestPedidosClassicos(unittest.TestCase):
    def test_pedidos_definem_receita_tempo_e_pontuacao(self):
        casos = (
            (
                PedidoFacil,
                ["Pão", "Queijo", "Carne"],
                TEMPOFACIL,
                PONTUACAOFACIL,
            ),
            (
                PedidoMedio,
                ["Pão", "Tomate", "Queijo", "Carne"],
                TEMPOMEDIO,
                PONTUACAOMEDIO,
            ),
            (
                PedidoDificil,
                ["Pão", "Alface", "Tomate", "Queijo", "Carne"],
                TEMPODIFICIL,
                PONTUACAODIFICIL,
            ),
        )
        for classe_pedido, ingredientes, tempo, pontuacao in casos:
            with self.subTest(pedido=classe_pedido.__name__):
                pedido = classe_pedido()
                self.assertEqual(pedido.ingredientes, ingredientes)
                self.assertEqual(pedido.tempo, tempo)
                self.assertEqual(pedido.pontuacao, pontuacao)


class TestEntregaClassica(unittest.TestCase):
    def test_hamburguer_de_cada_receita_corresponde_ao_pedido(self):
        receitas = (
            (PedidoFacil, False, False),
            (PedidoMedio, True, False),
            (PedidoDificil, True, True),
        )
        for classe_pedido, com_tomate, com_alface in receitas:
            with self.subTest(pedido=classe_pedido.__name__):
                pedido = classe_pedido()
                jogo = criar_jogo_minimo(pedido)
                hamburguer = Hamburguer(
                    0, 0, com_tomate=com_tomate, com_alface=com_alface
                )

                with patch("jogo.random.choice", return_value=PedidoFacil):
                    jogo.processar_entrega(hamburguer)

                self.assertEqual(jogo.fase.tempo, 90 + pedido.tempo)
                self.assertEqual(jogo.fase.pontuacao, 40 + pedido.pontuacao)

    def test_entrega_recusa_objeto_sem_tipo_hamburguer_sem_lancar_excecao(self):
        pedido = PedidoFacil()
        jogo = criar_jogo_minimo(pedido)

        with patch("jogo.random.choice", return_value=PedidoMedio):
            jogo.processar_entrega(object())

        self.assertEqual(jogo.fase.tempo, 90 - pedido.tempo // 2)
        self.assertEqual(jogo.fase.pontuacao, 40 - pedido.pontuacao)
        self.assertIsInstance(jogo.pedido_atual, PedidoMedio)

    def test_entrega_recusa_objeto_com_atributos_semelhantes_a_hamburguer(self):
        pedido = PedidoFacil()
        jogo = criar_jogo_minimo(pedido)
        objeto_parecido = SimpleNamespace(com_tomate=False, com_alface=False)

        with patch("jogo.random.choice", return_value=PedidoMedio):
            jogo.processar_entrega(objeto_parecido)

        self.assertEqual(jogo.fase.tempo, 90 - pedido.tempo // 2)
        self.assertEqual(jogo.fase.pontuacao, 40 - pedido.pontuacao)


class TestFluxoCozinhaClassica(unittest.TestCase):
    def test_fluxo_ingrediente_preparo_montagem_entrega_e_recompensa(self):
        pedido = PedidoFacil()
        montagem = Montagem(0, 0, pedido)
        pao = Pao(0, 0)
        queijo = Queijo(0, 0)
        carne = Carne(0, 0)
        for ingrediente in (pao, queijo):
            ingrediente.cortar_ingrediente()

        carne.cont = 499
        forno = SimpleNamespace(rect=pygame.Rect(carne.rect))
        carne.assar_ingrediente([forno])

        self.assertTrue(pao.cortado)
        self.assertTrue(queijo.cortado)
        self.assertTrue(carne.assado)
        for ingrediente in (pao, queijo, carne):
            self.assertTrue(montagem.adicionar_ingrediente(ingrediente, "1"))
        self.assertTrue(montagem.hamburguer_pronto)

        hamburguer = montagem.pegar_ingrediente()
        jogo = criar_jogo_minimo(pedido, montagens=[montagem])
        with patch("jogo.random.choice", return_value=PedidoMedio):
            jogo.processar_entrega(hamburguer)

        self.assertEqual(jogo.fase.tempo, 90 + pedido.tempo)
        self.assertEqual(jogo.fase.pontuacao, 40 + pedido.pontuacao)
        self.assertIsInstance(jogo.pedido_atual, PedidoMedio)
        self.assertIs(montagem.pedido, jogo.pedido_atual)


if __name__ == "__main__":
    unittest.main()
