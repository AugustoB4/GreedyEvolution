"""Cobertura do fluxo de campanha sem janela real ou sorteios probabilisticos."""

import apoio
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pygame

from campanha import (
    ENTREGAS_PARA_CONCLUIR,
    FASES_CAMPANHA,
    FASES_POR_GALAXIA,
    GALAXIAS,
    GALAXIAS_EM_CONSTRUCAO,
    ProgressoCampanha,
    TEMPO_MAXIMO_FASE,
    calcular_estrelas,
)
from fase import Fase
from interface_campanha import (
    ARTES_GALAXIAS,
    PAINEIS_TUTORIAL,
    InterfaceCampanha,
)
from itens import Hamburguer
from jogo import Jogo
from pedido import (
    PROBABILIDADES_PEDIDOS_POR_DIFICULDADE,
    PedidoFacil,
    PedidoMedio,
    PedidoPizzaMedio,
    PedidoSushiDificil,
    criar_pedido_ponderado,
)


class TestEstruturaCampanha(unittest.TestCase):
    def test_campanha_tem_12_fases_com_dificuldades_e_cozinhas_fixas(self):
        self.assertEqual(len(FASES_CAMPANHA), 12)
        self.assertEqual(tuple(map(len, FASES_POR_GALAXIA.values())), (3, 4, 5))
        self.assertEqual(
            tuple(f.dificuldade for f in FASES_POR_GALAXIA[1]),
            ("fácil", "médio", "difícil"),
        )
        self.assertEqual(
            tuple(f.dificuldade for f in FASES_POR_GALAXIA[2]),
            ("fácil", "médio", "médio", "difícil"),
        )
        self.assertEqual(
            tuple(f.dificuldade for f in FASES_POR_GALAXIA[3]),
            ("fácil", "médio", "médio", "médio", "difícil"),
        )
        self.assertEqual(
            tuple(f.variante for f in FASES_CAMPANHA),
            ("classica",) * 3 + ("pizzaria",) * 4 + ("reator",) * 5,
        )
        self.assertEqual(GALAXIAS_EM_CONSTRUCAO, (4, 5))
        self.assertEqual(tuple(g.numero for g in GALAXIAS), (1, 2, 3))

    def test_dificuldades_usam_as_probabilidades_aprovadas(self):
        self.assertEqual(
            PROBABILIDADES_PEDIDOS_POR_DIFICULDADE,
            {"fácil": (70, 25, 5), "médio": (30, 50, 20), "difícil": (10, 35, 55)},
        )

    def test_sorteio_ponderado_preserva_as_receitas_da_variante(self):
        with patch("pedido.random.choices", return_value=[PedidoFacil]) as sorteio:
            pedido = criar_pedido_ponderado("hamburguer", "fácil")
        self.assertIsInstance(pedido, PedidoFacil)
        self.assertEqual(sorteio.call_args.kwargs["weights"], (70, 25, 5))

        with patch("pedido.random.choices", return_value=[PedidoPizzaMedio]) as sorteio:
            pedido = criar_pedido_ponderado("pizza", "médio")
        self.assertIsInstance(pedido, PedidoPizzaMedio)
        self.assertEqual(sorteio.call_args.args[0][1].__name__, "PedidoPizzaMedio")
        self.assertEqual(sorteio.call_args.kwargs["weights"], (30, 50, 20))

        with patch("pedido.random.choices", return_value=[PedidoSushiDificil]) as sorteio:
            pedido = criar_pedido_ponderado("sushi", "difícil")
        self.assertEqual(pedido.familia, "sushi")
        self.assertEqual(pedido.produto_classe.__name__, "Sushi")
        self.assertEqual(sorteio.call_args.args[0][2].__name__, "PedidoSushiDificil")
        self.assertEqual(sorteio.call_args.kwargs["weights"], (10, 35, 55))


class TestEstrelasEBonus(unittest.TestCase):
    def test_limites_de_estrelas_exigem_pontuacao_e_tempo(self):
        limites = {
            "fácil": ((40, 15, 2), (55, 45, 3)),
            "médio": ((55, 15, 2), (70, 45, 3)),
            "difícil": ((70, 15, 2), (80, 45, 3)),
        }
        for dificuldade, faixas in limites.items():
            with self.subTest(dificuldade=dificuldade):
                (pontos2, tempo2, _), (pontos3, tempo3, _) = faixas
                self.assertEqual(calcular_estrelas(dificuldade, pontos2 - 1, tempo2), 1)
                self.assertEqual(calcular_estrelas(dificuldade, pontos2, tempo2 - 1), 1)
                self.assertEqual(calcular_estrelas(dificuldade, pontos2, tempo2), 2)
                self.assertEqual(calcular_estrelas(dificuldade, pontos3 - 1, tempo3), 2)
                self.assertEqual(calcular_estrelas(dificuldade, pontos3, tempo3 - 1), 2)
                self.assertEqual(calcular_estrelas(dificuldade, pontos3, tempo3), 3)

    def test_fase_incompleta_nao_conquista_estrelas(self):
        self.assertEqual(calcular_estrelas("fácil", 999, 120, False), 0)

    def test_bonus_progressivo_arredonda_para_baixo_e_para_no_minimo(self):
        esperado = {
            30: (30, 21, 12, 5),
            45: (45, 31, 18, 5),
            50: (50, 35, 20, 5),
        }
        for tempo_base, valores in esperado.items():
            fase = Fase(tempo=0)
            observados = tuple(
                fase.registrar_acerto(tempo_base, 0)
                for _ in range(4)
            )
            with self.subTest(tempo_base=tempo_base):
                self.assertEqual(observados, valores)

    def test_limite_de_tempo_penalidade_e_contador_de_acertos(self):
        fase = Fase(tempo=115, limite_tempo=TEMPO_MAXIMO_FASE)
        fase.registrar_acerto(30, 10)
        self.assertEqual(fase.tempo, 120)
        self.assertEqual(fase.entregas_corretas, 1)

        fase.diminuir_tempo_pontuacao(45, 15)
        self.assertEqual(fase.entregas_corretas, 1)
        self.assertEqual(fase.tempo, 98)
        self.assertEqual(fase.pontuacao, 0)

    def test_fase_encerrada_congela_tempo_pontuacao_e_acertos(self):
        fase = Fase(tempo=44, pontuacao=17)
        fase.encerrar("vitoria", 2)
        fase.atualizar(10)
        self.assertEqual(fase.registrar_acerto(50, 20), 0)
        fase.diminuir_tempo_pontuacao(50, 20)
        self.assertEqual((fase.tempo, fase.pontuacao, fase.entregas_corretas), (44, 17, 0))


class TestPersistenciaCampanha(unittest.TestCase):
    def test_primeiro_acesso_progresso_recordes_e_tutoriais_persistem(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "progresso.json"
            progresso = ProgressoCampanha(caminho)
            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertFalse(progresso.galaxia_desbloqueada(2))
            self.assertEqual(progresso.melhor_classificacao(1), 0)

            progresso.registrar_resultado(1, 2)
            progresso.registrar_resultado(1, 1)
            progresso.marcar_tutorial_exibido(1)
            progresso.marcar_tutorial_exibido(3)
            carregado = ProgressoCampanha(caminho)

            self.assertEqual(carregado.melhor_classificacao(1), 2)
            self.assertEqual(carregado.dados["fases_desbloqueadas"], [1, 2])
            self.assertTrue(carregado.galaxia_desbloqueada(1))
            self.assertTrue(carregado.tutorial_exibido(1))
            self.assertFalse(carregado.tutorial_exibido(2))
            self.assertTrue(carregado.tutorial_exibido(3))

    def test_avanco_entre_galaxias_e_conclusao_somente_apos_12_com_dois_pontos(self):
        with tempfile.TemporaryDirectory() as diretorio:
            progresso = ProgressoCampanha(Path(diretorio) / "progresso.json")
            for numero in range(1, 12):
                progresso.registrar_resultado(numero, 2)
            self.assertTrue(progresso.galaxia_desbloqueada(2))
            self.assertTrue(progresso.galaxia_desbloqueada(3))
            self.assertFalse(progresso.dados["campanha_concluida"])

            progresso.registrar_resultado(12, 1)
            self.assertFalse(progresso.dados["campanha_concluida"])
            progresso.registrar_resultado(12, 2)
            self.assertTrue(progresso.dados["campanha_concluida"])

    def test_uma_estrela_nao_desbloqueia_e_nao_rebloqueia_progresso(self):
        with tempfile.TemporaryDirectory() as diretorio:
            progresso = ProgressoCampanha(Path(diretorio) / "progresso.json")
            progresso.registrar_resultado(1, 2)
            progresso.registrar_resultado(1, 1)
            self.assertTrue(progresso.fase_desbloqueada(2))
            self.assertEqual(progresso.melhor_classificacao(1), 2)
            self.assertFalse(progresso.fase_desbloqueada(3))

            progresso.registrar_resultado(1, 3)
            progresso.registrar_resultado(1, 1)
            self.assertTrue(progresso.fase_desbloqueada(2))
            self.assertEqual(progresso.melhor_classificacao(1), 3)

    def test_arquivo_ausente_ou_corrompido_usa_estado_seguro(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "progresso.json"
            self.assertEqual(ProgressoCampanha(caminho).dados["fases_desbloqueadas"], [1])
            caminho.write_text("{ inválido", encoding="utf-8")
            progresso = ProgressoCampanha(caminho)
            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertEqual(progresso.dados["melhores_estrelas"]["12"], 0)

    def test_dados_invalidos_nao_criam_desbloqueios_ou_recordes_impossiveis(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "progresso.json"
            caminho.write_text(
                json.dumps({
                    "versao": 1,
                    "fases_desbloqueadas": [1, 12],
                    "melhores_estrelas": {"1": 9, "2": 2},
                    "tutoriais_exibidos": {"1": True},
                }),
                encoding="utf-8",
            )
            progresso = ProgressoCampanha(caminho)
            self.assertEqual(progresso.melhor_classificacao(1), 0)
            self.assertEqual(progresso.melhor_classificacao(2), 0)
            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertFalse(progresso.fase_desbloqueada(12))

    def test_desbloqueios_continuos_sem_recordes_nao_sao_confiaveis(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "progresso.json"
            caminho.write_text(
                json.dumps({
                    "versao": 1,
                    "fases_desbloqueadas": list(range(1, 13)),
                    "melhores_estrelas": {},
                }),
                encoding="utf-8",
            )

            progresso = ProgressoCampanha(caminho)

            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertEqual(progresso.dados["galaxias_desbloqueadas"], [1])
            self.assertEqual(progresso.total_estrelas(), 0)
            self.assertFalse(progresso.dados["campanha_concluida"])

    def test_recordes_de_fases_bloqueadas_sao_ignorados_e_recordes_validos_reconstroem(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "progresso.json"
            caminho.write_text(
                json.dumps({
                    "versao": 1,
                    "fases_desbloqueadas": [1],
                    "melhores_estrelas": {"1": 2, "2": 1, "3": 3, "12": 3},
                }),
                encoding="utf-8",
            )

            progresso = ProgressoCampanha(caminho)

            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1, 2])
            self.assertEqual(progresso.melhor_classificacao(1), 2)
            self.assertEqual(progresso.melhor_classificacao(2), 1)
            self.assertEqual(progresso.melhor_classificacao(3), 0)
            self.assertEqual(progresso.melhor_classificacao(12), 0)
            self.assertFalse(progresso.dados["campanha_concluida"])

    def test_versao_incompativel_e_campos_ausentes_usam_estado_seguro(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "progresso.json"
            caminho.write_text(
                json.dumps({"versao": 999, "melhores_estrelas": {"12": 3}}),
                encoding="utf-8",
            )
            progresso = ProgressoCampanha(caminho)
            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertEqual(progresso.total_estrelas(), 0)

            caminho.write_text(json.dumps({"versao": 1}), encoding="utf-8")
            progresso = ProgressoCampanha(caminho)
            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertEqual(progresso.total_estrelas(), 0)

    def test_resultado_de_fase_bloqueada_e_recusado(self):
        with tempfile.TemporaryDirectory() as diretorio:
            progresso = ProgressoCampanha(Path(diretorio) / "progresso.json")
            with self.assertRaises(ValueError):
                progresso.registrar_resultado(2, 3)
            self.assertEqual(progresso.dados["fases_desbloqueadas"], [1])
            self.assertEqual(progresso.total_estrelas(), 0)

    def test_falha_de_gravacao_reverte_memoria_e_preserva_arquivo_atomico(self):
        for erro in (PermissionError, IsADirectoryError):
            with self.subTest(erro=erro.__name__), tempfile.TemporaryDirectory() as diretorio:
                caminho = Path(diretorio) / "progresso.json"
                progresso = ProgressoCampanha(caminho)
                progresso.registrar_resultado(1, 2)
                conteudo_anterior = caminho.read_bytes()
                dados_anteriores = json.loads(conteudo_anterior)

                with patch("campanha.os.replace", side_effect=erro("bloqueado")):
                    melhor = progresso.registrar_resultado(2, 2)

                self.assertEqual(melhor, 0)
                self.assertEqual(progresso.dados, dados_anteriores)
                self.assertEqual(caminho.read_bytes(), conteudo_anterior)
                self.assertTrue(progresso.erro_salvamento)
                self.assertFalse(progresso.fase_desbloqueada(3))
                self.assertEqual(
                    list(Path(diretorio).glob(".progresso.json.*.tmp")), []
                )

    def test_falha_ao_salvar_tutorial_reverte_sinalizador_em_memoria(self):
        with tempfile.TemporaryDirectory() as diretorio:
            progresso = ProgressoCampanha(Path(diretorio) / "progresso.json")
            with patch("campanha.os.replace", side_effect=PermissionError("negado")):
                salvo = progresso.marcar_tutorial_exibido(1)

            self.assertFalse(salvo)
            self.assertFalse(progresso.tutorial_exibido(1))
            self.assertTrue(progresso.erro_salvamento)


class TestEntregaDeCampanha(unittest.TestCase):
    def criar_jogo_minimo(self, tempo=60):
        jogo = object.__new__(Jogo)
        jogo.campanha_ativa = True
        jogo.indice_fase_campanha = 0
        jogo.definicao_fase = FASES_CAMPANHA[0]
        jogo.fase = Fase(tempo=tempo, definicao=jogo.definicao_fase, limite_tempo=120)
        jogo.pedido_atual = PedidoFacil()
        jogo.montagens = [SimpleNamespace(pedido=jogo.pedido_atual)]
        jogo.tipo_pedido = "hamburguer"
        jogo.progresso_campanha = SimpleNamespace(
            registrar_resultado=lambda numero, estrelas: estrelas,
        )
        jogo.resultado_fase = None
        return jogo

    def test_quatro_entregas_corretas_concluem_apos_aplicar_quarto_bonus(self):
        jogo = self.criar_jogo_minimo()
        produto = Hamburguer(0, 0)
        with patch("jogo.criar_pedido_ponderado", return_value=PedidoFacil()) as proximo:
            for _ in range(4):
                self.assertTrue(jogo.processar_entrega(produto))

        self.assertEqual(jogo.fase.entregas_corretas, ENTREGAS_PARA_CONCLUIR)
        self.assertTrue(jogo.fase.encerrada)
        self.assertEqual(jogo.fase.resultado, "vitoria")
        self.assertEqual(jogo.fase.pontuacao, 40)
        self.assertEqual(jogo.fase.tempo, 120)
        self.assertEqual(jogo.fase.estrelas, 2)
        self.assertEqual(proximo.call_count, 3)

        self.assertFalse(jogo.processar_entrega(produto))
        self.assertEqual((jogo.fase.pontuacao, jogo.fase.tempo), (40, 120))
        self.assertEqual(proximo.call_count, 3)

    def test_pedido_incorreto_aplica_penalidade_sem_contar_acerto(self):
        jogo = self.criar_jogo_minimo()
        produto_incorreto = Hamburguer(0, 0, com_tomate=True)
        with patch("jogo.criar_pedido_ponderado", return_value=PedidoMedio()):
            self.assertFalse(jogo.processar_entrega(produto_incorreto))
        self.assertEqual(jogo.fase.entregas_corretas, 0)
        self.assertEqual(jogo.fase.pontuacao, 0)
        self.assertEqual(jogo.fase.tempo, 45)

    def test_pedido_incorreto_nao_avanca_a_reducao_do_bonus(self):
        jogo = self.criar_jogo_minimo()
        produto = Hamburguer(0, 0)
        with patch("jogo.criar_pedido_ponderado", return_value=PedidoFacil()):
            jogo.processar_entrega(produto)
            jogo.processar_entrega(Hamburguer(0, 0, com_tomate=True))
            bonus_segundo_acerto = jogo.fase.registrar_acerto(30, 0)
        self.assertEqual(bonus_segundo_acerto, 21)

    def test_estrelas_usam_a_pontuacao_liquida_apos_penalidade(self):
        jogo = self.criar_jogo_minimo()
        with patch("jogo.criar_pedido_ponderado", return_value=PedidoFacil()):
            for _ in range(3):
                self.assertTrue(jogo.processar_entrega(Hamburguer(0, 0)))
            self.assertFalse(
                jogo.processar_entrega(Hamburguer(0, 0, com_tomate=True))
            )
            self.assertTrue(jogo.processar_entrega(Hamburguer(0, 0)))

        self.assertEqual(jogo.fase.pontuacao, 30)
        self.assertEqual(jogo.fase.estrelas, 1)

    def test_tempo_zero_prevalece_sobre_entrega_que_ainda_nao_foi_processada(self):
        jogo = self.criar_jogo_minimo(tempo=0)
        self.assertFalse(jogo.processar_entrega(Hamburguer(0, 0)))
        self.assertEqual(jogo.fase.resultado, "derrota")
        self.assertEqual(jogo.fase.entregas_corretas, 0)
        self.assertEqual(jogo.fase.pontuacao, 0)

    def test_resultado_da_fase_marca_se_a_persistencia_falhou(self):
        jogo = self.criar_jogo_minimo()
        jogo.progresso_campanha = SimpleNamespace(
            erro_salvamento="acesso negado",
            registrar_resultado=lambda numero, estrelas: 0,
        )
        with patch("jogo.criar_pedido_ponderado", return_value=PedidoFacil()):
            for _ in range(4):
                jogo.processar_entrega(Hamburguer(0, 0))

        self.assertFalse(jogo.resultado_fase["persistido"])
        self.assertEqual(jogo.resultado_fase["melhor_classificacao"], 0)


class TestInicializacaoEInterfaceCampanha(unittest.TestCase):
    def test_inicializacao_fixa_cozinha_dificuldade_e_pedidos_por_galaxia(self):
        with tempfile.TemporaryDirectory() as diretorio:
            progresso = ProgressoCampanha(Path(diretorio) / "progresso.json")
            for indice, variante, estilo, tipo in (
                (0, "classica", "classico", "hamburguer"),
                (3, "pizzaria", "pizzaria", "pizza"),
                (7, "reator", "reator", "sushi"),
            ):
                with self.subTest(variante=variante):
                    jogo = Jogo(campanha=True, indice_fase=indice, progresso=progresso)
                    self.assertEqual(jogo.nome_variante, variante)
                    self.assertEqual(jogo.estilo, estilo)
                    self.assertEqual(jogo.tipo_pedido, tipo)
                    self.assertEqual(jogo.fase.definicao, FASES_CAMPANHA[indice])
                    self.assertEqual(jogo.fase.tempo, 60)
                    self.assertEqual(jogo.fase.limite_tempo, 120)

    def test_recursos_de_campanha_renderizam_em_pygame_simulado(self):
        tela = pygame.Surface((1000, 600))
        interface = InterfaceCampanha(tela, 1000, 600)
        with tempfile.TemporaryDirectory() as diretorio:
            progresso = ProgressoCampanha(Path(diretorio) / "progresso.json")
            interface.desenhar_selecao(progresso)
            self.assertEqual(set(interface.imagens_galaxia), set(ARTES_GALAXIAS))
            self.assertEqual(set(interface.imagens_tutorial), set(PAINEIS_TUTORIAL))
            for imagem in interface.imagens_galaxia.values():
                self.assertGreater(imagem.get_width(), 0)
                self.assertGreater(imagem.get_height(), 0)
            for imagem in interface.imagens_tutorial.values():
                self.assertGreater(imagem.get_width(), 0)
                self.assertGreater(imagem.get_height(), 0)

            clique_fase_bloqueada = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {"button": 1, "pos": interface.rects_fases[1].center},
            )
            with patch(
                "interface_campanha.pygame.event.get",
                side_effect=[
                    [clique_fase_bloqueada],
                    [pygame.event.Event(pygame.QUIT)],
                ],
            ):
                self.assertEqual(
                    interface.executar_selecao(progresso), ("sair", None)
                )

            clique_primeira_fase = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN,
                {"button": 1, "pos": interface.rects_fases[0].center},
            )
            with patch(
                "interface_campanha.pygame.event.get",
                return_value=[clique_primeira_fase],
            ):
                self.assertEqual(
                    interface.executar_selecao(progresso), ("fase", 0)
                )

            for numero_galaxia in PAINEIS_TUTORIAL:
                with patch(
                    "interface_campanha.pygame.event.get",
                    return_value=[pygame.event.Event(pygame.QUIT)],
                ):
                    self.assertEqual(
                        interface.executar_tutorial(numero_galaxia), "sair"
                    )

            with patch(
                "interface_campanha.pygame.event.get",
                return_value=[pygame.event.Event(pygame.QUIT)],
            ):
                self.assertEqual(
                    interface.executar_resultado(
                        FASES_CAMPANHA[0], 40, 30, 2, 2, True, True, False
                    ),
                    "sair",
                )

            with patch(
                "interface_campanha.pygame.event.get",
                return_value=[pygame.event.Event(pygame.QUIT)],
            ):
                self.assertEqual(
                    interface.executar_resultado(
                        FASES_CAMPANHA[-1], 80, 50, 3, 3, True, False, True
                    ),
                    "sair",
                )

            with patch(
                "interface_campanha.pygame.event.get",
                return_value=[pygame.event.Event(pygame.QUIT)],
            ):
                self.assertEqual(
                    interface.executar_resultado(
                        FASES_CAMPANHA[0], 0, 0, 0, 0, False, False, False
                    ),
                    "sair",
                )

    def test_resultado_final_explica_duas_estrelas_e_falha_de_salvamento(self):
        interface = InterfaceCampanha(pygame.Surface((1000, 600)), 1000, 600)
        textos = []
        interface._texto_centralizado = lambda texto, *args, **kwargs: textos.append(texto)
        with (
            patch(
                "interface_campanha.pygame.event.get",
                return_value=[pygame.event.Event(pygame.QUIT)],
            ),
            patch("interface_campanha.pygame.display.flip"),
        ):
            self.assertEqual(
                interface.executar_resultado(
                    FASES_CAMPANHA[-1], 30, 10, 1, 0, True, False, False,
                    erro_salvamento="acesso negado",
                ),
                "sair",
            )

        self.assertIn("CONQUISTE 2 ESTRELAS PARA CONCLUIR CAMPANHA", textos)
        self.assertIn("ERRO AO SALVAR O PROGRESSO", textos)
        self.assertIn("ESTA TENTATIVA NÃO FOI PERSISTIDA", textos)

    def test_fluxo_simulado_avanca_sequencialmente_pelas_12_fases(self):
        with tempfile.TemporaryDirectory() as diretorio:
            jogo = object.__new__(Jogo)
            jogo.tela = pygame.Surface((1000, 600))
            jogo.largura = 1000
            jogo.altura = 600
            jogo.rodando = True
            jogo.caminho_progresso = Path(diretorio) / "progresso.json"
            jogo.progresso_campanha = ProgressoCampanha(jogo.caminho_progresso)
            tutoriais = []
            resultados = []

            class InterfaceSimulada:
                selecoes = 0

                def __init__(self, *_):
                    pass

                def executar_selecao(self, progresso):
                    type(self).selecoes += 1
                    if type(self).selecoes == 1:
                        return "fase", 0
                    return "sair", None

                def executar_tutorial(self, galaxia):
                    tutoriais.append(galaxia)
                    return "iniciar"

                def executar_resultado(
                    self, definicao, pontuacao, tempo, estrelas, melhor,
                    venceu, proxima_desbloqueada, campanha_concluida,
                    erro_salvamento=None,
                ):
                    resultados.append(definicao.numero)
                    if campanha_concluida:
                        return "campanha"
                    return "avancar" if proxima_desbloqueada else "repetir"

            def carregar(indice):
                jogo.indice_fase_campanha = indice
                jogo.definicao_fase = FASES_CAMPANHA[indice]
                jogo.fase = Fase(
                    tempo=60,
                    definicao=jogo.definicao_fase,
                    limite_tempo=TEMPO_MAXIMO_FASE,
                )
                jogo.player1 = SimpleNamespace(parar_som_andar=lambda: None)
                jogo.player2 = SimpleNamespace(parar_som_andar=lambda: None)

            def concluir_fase():
                jogo.fase.pontuacao = 80
                jogo.fase.tempo = 50
                jogo.fase.encerrar("vitoria", 2)
                jogo.progresso_campanha.registrar_resultado(
                    jogo.definicao_fase.numero, 2
                )
                return "vitoria"

            with patch("jogo.Menu", return_value=SimpleNamespace(executar=lambda: "start")), \
                 patch("jogo.InterfaceCampanha", InterfaceSimulada), \
                 patch("jogo.som_inicial"), patch("jogo.som_face"), \
                 patch("jogo.pygame.quit"), \
                 patch.object(jogo, "_carregar_fase_campanha", side_effect=carregar), \
                 patch.object(jogo, "_executar_fase_campanha", side_effect=concluir_fase):
                jogo._iniciar_campanha()

            self.assertEqual(resultados, list(range(1, 13)))
            self.assertEqual(tutoriais, [1, 2, 3])
            self.assertTrue(jogo.progresso_campanha.dados["campanha_concluida"])


if __name__ == "__main__":
    unittest.main()
