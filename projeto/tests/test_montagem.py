import apoio
import unittest

from itens import Alface, Carne, Pao, Queijo, Tomate
from montagem import Montagem
from pedido import PedidoDificil, PedidoFacil, PedidoMedio


CLASSES_INGREDIENTES = {
    "Pão": Pao,
    "Queijo": Queijo,
    "Carne": Carne,
    "Tomate": Tomate,
    "Alface": Alface,
}


def criar_montagem(pedido, nomes=None, carne_assada=True, carne_queimada=False):
    montagem = Montagem(0, 0, pedido)
    nomes = nomes or pedido.ingredientes

    for nome in nomes:
        ingrediente = CLASSES_INGREDIENTES[nome](0, 0)
        if ingrediente.nome == "Meat":
            ingrediente.assado = carne_assada
            ingrediente.queimado = carne_queimada
            ingrediente.cru = not carne_assada
        else:
            ingrediente.cortado = True
        montagem.adicionar_ingrediente(ingrediente, "1")

    return montagem


class TestMontagem(unittest.TestCase):
    def test_receitas_de_hamburguer_atuais_ficam_prontas(self):
        receitas = (
            (PedidoFacil, False, False),
            (PedidoMedio, True, False),
            (PedidoDificil, True, True),
        )

        for classe_pedido, com_tomate, com_alface in receitas:
            with self.subTest(pedido=classe_pedido.__name__):
                pedido = classe_pedido()
                montagem = criar_montagem(pedido)

                self.assertTrue(montagem.hamburguer_pronto)
                hamburguer = montagem.pegar_ingrediente()
                self.assertEqual(hamburguer.nome, "Hamburguer")
                self.assertEqual(hamburguer.com_tomate, com_tomate)
                self.assertEqual(hamburguer.com_alface, com_alface)

    def test_receita_na_ordem_errada_nao_fica_pronta(self):
        pedido = PedidoFacil()
        ordem_errada = ["Queijo", "Pão", "Carne"]

        montagem = criar_montagem(pedido, nomes=ordem_errada)

        self.assertFalse(montagem.hamburguer_pronto)

    def test_carne_crua_impede_concluir_a_receita(self):
        montagem = criar_montagem(PedidoFacil(), carne_assada=False)

        self.assertFalse(montagem.hamburguer_pronto)

    def test_carne_queimada_impede_concluir_a_receita(self):
        montagem = criar_montagem(
            PedidoFacil(), carne_assada=False, carne_queimada=True
        )

        self.assertFalse(montagem.hamburguer_pronto)

    def test_pedido_novo_revalida_montagem_sem_descartar_ingredientes(self):
        montagem = criar_montagem(PedidoFacil())
        ingredientes_anteriores = list(montagem.ingredientes)

        montagem.pedido = PedidoMedio()

        self.assertFalse(montagem.hamburguer_pronto)
        self.assertEqual(montagem.ingredientes, ingredientes_anteriores)
        self.assertTrue(all(item.em_montagem for item in ingredientes_anteriores))

        retirado = montagem.pegar_ingrediente()

        self.assertEqual(retirado.nome, "Meat")
        self.assertIsNone(getattr(retirado, "receita_id", None))
        self.assertEqual(montagem.ingredientes, ingredientes_anteriores[:-1])

    def test_duas_montagens_e_preparo_alterado_sao_revalidados(self):
        montagens = [criar_montagem(PedidoFacil()) for _ in range(2)]
        ingredientes_anteriores = [list(m.ingredientes) for m in montagens]

        for montagem in montagens:
            self.assertTrue(montagem.hamburguer_pronto)
            montagem.pedido = PedidoMedio()
            self.assertFalse(montagem.hamburguer_pronto)

        for montagem, ingredientes in zip(montagens, ingredientes_anteriores):
            self.assertEqual(montagem.ingredientes, ingredientes)

        carne = montagens[0].ingredientes[-1]
        carne.queimado = True
        carne.assado = False
        montagens[0].pedido = PedidoFacil()
        produto = montagens[0].pegar_ingrediente()

        self.assertEqual(produto.nome, "Meat")
        self.assertFalse(montagens[0].hamburguer_pronto)

    def test_ingredientes_podem_ser_reordenados_para_o_pedido_novo(self):
        montagem = criar_montagem(PedidoFacil(), nomes=["Pão", "Queijo"])
        montagem.pedido = PedidoMedio()
        queijo = montagem.pegar_ingrediente()
        tomate = Tomate(0, 0)
        tomate.cortado = True

        self.assertFalse(montagem.hamburguer_pronto)
        self.assertTrue(montagem.adicionar_ingrediente(tomate, "1"))
        self.assertTrue(montagem.adicionar_ingrediente(queijo, "1"))
        carne = Carne(0, 0)
        carne.assado = True
        carne.cru = False
        self.assertTrue(montagem.adicionar_ingrediente(carne, "1"))
        self.assertTrue(montagem.hamburguer_pronto)
        self.assertEqual(
            [item.nome for item in montagem.ingredientes],
            ["Bread", "Tomato", "Cheese", "Meat"],
        )


if __name__ == "__main__":
    unittest.main()
