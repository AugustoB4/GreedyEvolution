import apoio
import unittest

from fase import Fase


class TestFase(unittest.TestCase):
    def test_acerto_soma_tempo_e_pontuacao(self):
        fase = Fase(tempo=60, pontuacao=5)

        fase.aumentar_tempo_pontuacao(30, 10)

        self.assertEqual(fase.tempo, 90)
        self.assertEqual(fase.pontuacao, 15)

    def test_erro_reduz_metade_do_tempo_do_pedido_e_os_pontos(self):
        fase = Fase(tempo=60, pontuacao=30)

        fase.diminuir_tempo_pontuacao(45, 15)

        self.assertEqual(fase.tempo, 38)
        self.assertEqual(fase.pontuacao, 15)

    def test_penalidade_nao_deixa_tempo_ou_pontuacao_negativos(self):
        fase = Fase(tempo=5, pontuacao=3)

        fase.diminuir_tempo_pontuacao(30, 10)

        self.assertEqual(fase.tempo, 0)
        self.assertEqual(fase.pontuacao, 0)

    def test_cronometro_para_em_zero(self):
        fase = Fase(tempo=1.5)

        fase.atualizar(1.0)
        self.assertEqual(fase.tempo, 0.5)

        fase.atualizar(3.0)
        fase.atualizar(1.0)
        self.assertEqual(fase.tempo, 0)


if __name__ == "__main__":
    unittest.main()
