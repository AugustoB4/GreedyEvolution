import apoio
import pygame
import unittest
from types import SimpleNamespace

from campanha import FASES_CAMPANHA
from fase import Fase
from pedido import PedidoFacil, ReceitaTV


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

    def test_hud_destaca_por_tres_segundos_e_retorna_com_fade(self):
        fase = Fase(tempo=60, definicao=FASES_CAMPANHA[0])
        self.assertEqual(fase.opacidade_hud, 128)

        fase.destacar_entrega(correta=True)
        self.assertEqual(fase.opacidade_hud, 255)
        self.assertEqual(
            fase._animacao_pontuacao_restante,
            fase.DURACAO_ANIMACAO_VALORES,
        )
        self.assertEqual(
            fase._animacao_tempo_restante,
            fase.DURACAO_ANIMACAO_VALORES,
        )

        fase.atualizar(2.99)
        self.assertEqual(fase.opacidade_hud, 255)
        fase.destacar_entrega(correta=False)
        self.assertEqual(fase._hud_destaque_restante, 3.0)
        self.assertEqual(fase._animacao_pontuacao_restante, 0.0)
        fase.atualizar(3.0)
        self.assertEqual(fase.opacidade_hud, 255)

        fase.atualizar(0.2)
        self.assertGreater(fase.opacidade_hud, fase.OPACIDADE_HUD_PADRAO)
        self.assertLess(fase.opacidade_hud, 255)
        fase.atualizar(0.25)
        self.assertEqual(fase.opacidade_hud, fase.OPACIDADE_HUD_PADRAO)

    def test_hud_empilha_indicadores_e_mantem_cronometro_centralizado_embaixo(self):
        fase = Fase(tempo=61, pontuacao=12, definicao=FASES_CAMPANHA[0])
        tela = pygame.Surface((1000, 600))
        fundo = (31, 47, 63)
        tela.fill(fundo)

        fase.desenhar(tela)
        rects_iniciais = dict(fase.hud_rects)
        textos_iniciais = {
            chave: id(imagem)
            for chave, (_, imagem) in fase._hud_textos.items()
        }
        sombras_iniciais = {
            chave: id(imagem)
            for chave, (_, imagem) in fase._hud_sombras.items()
        }
        fase.desenhar(tela)
        textos_reutilizados = {
            chave: id(imagem)
            for chave, (_, imagem) in fase._hud_textos.items()
        }
        sombras_reutilizadas = {
            chave: id(imagem)
            for chave, (_, imagem) in fase._hud_sombras.items()
        }

        self.assertEqual(textos_reutilizados, textos_iniciais)
        self.assertEqual(sombras_reutilizadas, sombras_iniciais)
        self.assertEqual(
            tuple(rects_iniciais),
            ("pontuacao", "acertos", "galaxia", "fase", "dificuldade", "tempo"),
        )
        indicadores = [
            rects_iniciais[chave]
            for chave in ("pontuacao", "acertos", "galaxia", "fase", "dificuldade")
        ]
        self.assertTrue(all(rect.left == 18 for rect in indicadores))
        self.assertTrue(
            all(a.bottom < b.top for a, b in zip(indicadores, indicadores[1:]))
        )
        self.assertEqual(rects_iniciais["tempo"].centerx, 500)
        self.assertEqual(rects_iniciais["tempo"].bottom, 588)
        self.assertGreaterEqual(rects_iniciais["tempo"].height, 22)
        self.assertFalse(hasattr(fase, "_hud_superficie"))
        self.assertEqual(tela.get_at((300, 120))[:3], fundo)
        self.assertEqual(tela.get_at((500, 520))[:3], fundo)
        self.assertTrue(
            all(
                imagem.get_alpha() == fase.OPACIDADE_HUD_PADRAO
                for _, imagem in fase._hud_textos.values()
            )
        )
        self.assertTrue(
            all(
                imagem.get_alpha() == fase.OPACIDADE_HUD_PADRAO
                for _, imagem in fase._hud_sombras.values()
            )
        )

        fase.destacar_entrega(correta=True)
        fase.aumentar_tempo_pontuacao(10, 5)
        fase.atualizar(0.2)
        fase.desenhar(tela)
        self.assertEqual(fase.hud_rects["tempo"].centerx, 500)
        self.assertEqual(fase.hud_rects["tempo"].bottom, 588)
        self.assertNotEqual(id(fase._hud_textos["pontuacao"][1]), textos_iniciais["pontuacao"])
        self.assertAlmostEqual(
            fase._fator_animacao(fase._animacao_pontuacao_restante), 1.14
        )

    def test_entregas_corretas_consecutivas_reiniciam_animacao_sem_mover_o_hud(self):
        fase = Fase(tempo=60)
        tela = pygame.Surface((1000, 600))
        fase.destacar_entrega(correta=True)
        fase.atualizar(0.3)
        fase.desenhar(tela)
        centro_tempo_inicial = fase.hud_rects["tempo"].centerx

        fase.destacar_entrega(correta=True)
        fase.atualizar(0.2)
        fase.desenhar(tela)

        self.assertAlmostEqual(fase._hud_destaque_restante, 2.8)
        self.assertAlmostEqual(fase._animacao_pontuacao_restante, 0.2)
        self.assertEqual(fase.hud_rects["tempo"].centerx, centro_tempo_inicial)
        self.assertEqual(fase.hud_rects["tempo"].bottom, 588)
        self.assertEqual(fase._hud_textos["pontuacao"][1].get_alpha(), 255)

    def test_tv_restaura_opacidade_apos_colisao_sem_depender_da_hud(self):
        televisao = ReceitaTV()
        tela = pygame.Surface((1000, 600))
        jogador1 = SimpleNamespace(rect=pygame.Rect(0, 300, 32, 20))
        jogador2 = SimpleNamespace(rect=pygame.Rect(100, 300, 32, 20))
        pedido = PedidoFacil()

        televisao.desenhar(tela, pedido, jogador1, jogador2)
        self.assertEqual(televisao.superficie_painel.get_alpha(), 255)
        self.assertEqual(televisao.superficie_conteudo.get_alpha(), 255)

        jogador1.rect.topleft = (836, 0)
        televisao.desenhar(tela, pedido, jogador1, jogador2)
        self.assertEqual(televisao.superficie_painel.get_alpha(), 155)
        self.assertEqual(televisao.superficie_conteudo.get_alpha(), 155)

        jogador1.rect.topleft = (300, 300)
        fase = Fase(tempo=60)
        fase.destacar_entrega(correta=True)
        televisao.desenhar(
            tela,
            pedido,
            jogador1,
            jogador2,
            600 / 624,
            (15, 0),
            1008,
        )
        self.assertEqual(fase.opacidade_hud, 255)
        self.assertEqual(televisao.superficie_painel.get_alpha(), 255)
        self.assertEqual(televisao.superficie_conteudo.get_alpha(), 255)

        jogador1.rect.topleft = (836, 0)
        televisao.desenhar(
            tela,
            pedido,
            jogador1,
            jogador2,
            600 / 624,
            (15, 0),
            1008,
        )
        self.assertEqual(televisao.superficie_painel.get_alpha(), 155)
        jogador1.rect.topleft = (300, 300)
        televisao.desenhar(
            tela,
            pedido,
            jogador1,
            jogador2,
            600 / 624,
            (15, 0),
            1008,
        )
        self.assertEqual(televisao.superficie_painel.get_alpha(), 255)

    def test_hud_usa_coordenadas_diretas_e_opacidade_exata(self):
        fase = Fase(tempo=61, pontuacao=12, definicao=FASES_CAMPANHA[0])
        janela = pygame.Surface((1000, 600))
        mapa_redimensionado = pygame.Surface((1008, 624))
        fase.desenhar(janela)
        posicoes_janela = dict(fase.hud_rects)
        fase.desenhar(mapa_redimensionado)

        self.assertEqual(fase.hud_rects["pontuacao"].topleft, (18, 14))
        self.assertEqual(posicoes_janela["tempo"].centerx, 500)
        self.assertEqual(posicoes_janela["tempo"].bottom, 588)
        self.assertEqual(fase.hud_rects["tempo"].centerx, 504)
        self.assertEqual(fase.hud_rects["tempo"].bottom, 612)
        self.assertNotEqual(
            fase.hud_rects["tempo"].topleft,
            posicoes_janela["tempo"].topleft,
        )
        fase.destacar_entrega(correta=True)
        fase.desenhar(janela)
        self.assertTrue(
            all(
                imagem.get_alpha() == 255
                for _, imagem in fase._hud_textos.values()
            )
        )


if __name__ == "__main__":
    unittest.main()
