import apoio
import pygame
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from fase import Fase
from itens import Alface, Carne, Hamburguer, Pao, Queijo, Tomate
from jogo import Jogo
from mapa import VARIANTES_COZINHA
from pedido import PedidoFacil, PedidoMedio
from caminhos import PLAYER_DIR
from player import Brito, Romerio, alfaces, carnes, paos, queijos, tomates


LISTAS_INGREDIENTES = (
    tomates,
    queijos,
    paos,
    carnes,
    alfaces,
)


def criar_jogo_minimo():
    jogo = object.__new__(Jogo)
    jogo.pedido_atual = PedidoFacil()
    jogo.fase = Fase(tempo=60, pontuacao=20)
    jogo.montagens = [
        SimpleNamespace(pedido=jogo.pedido_atual),
        SimpleNamespace(pedido=jogo.pedido_atual),
    ]
    return jogo


def criar_jogo_pizzaria():
    with patch(
        "jogo.sortear_variante",
        return_value=("pizzaria", VARIANTES_COZINHA["pizzaria"]),
    ):
        return Jogo()


class TestEntrega(unittest.TestCase):
    def test_entrega_correta_adiciona_recompensa_e_atualiza_pedidos(self):
        jogo = criar_jogo_minimo()
        hamburguer = Hamburguer(0, 0)

        with patch("jogo.random.choice", return_value=PedidoMedio):
            jogo.processar_entrega(hamburguer)

        self.assertEqual(jogo.fase.tempo, 90)
        self.assertEqual(jogo.fase.pontuacao, 30)
        self.assertIsInstance(jogo.pedido_atual, PedidoMedio)
        for montagem in jogo.montagens:
            self.assertIs(montagem.pedido, jogo.pedido_atual)

    def test_entrega_incorreta_aplica_penalidade(self):
        jogo = criar_jogo_minimo()
        hamburguer = Hamburguer(0, 0, com_tomate=True)

        with patch("jogo.random.choice", return_value=PedidoMedio):
            jogo.processar_entrega(hamburguer)

        self.assertEqual(jogo.fase.tempo, 45)
        self.assertEqual(jogo.fase.pontuacao, 10)
        self.assertIsInstance(jogo.pedido_atual, PedidoMedio)


class TestCaminhosSpritesPersonagens(unittest.TestCase):
    def test_caminhos_e_arquivos_dos_dois_personagens_por_estilo(self):
        personagem = object.__new__(Romerio)
        estilos = ("classico", "pizzaria", "reator")
        personagens = ("Romerio", "Brito")
        pasta_base = Path(PLAYER_DIR)

        for estilo in estilos:
            pasta_esperada = (
                pasta_base
                if estilo == "classico"
                else pasta_base / estilo
            )

            for nome in personagens:
                with self.subTest(estilo=estilo, personagem=nome):
                    caminhos = personagem.caminhos_personagem(nome, estilo)
                    nomes_arquivos = (
                        f"{nome}.png",
                        f"{nome}_Walk.png",
                        f"{nome}_Slip.png",
                    )

                    self.assertEqual(
                        tuple(Path(caminho) for caminho in caminhos),
                        tuple(pasta_esperada / arquivo for arquivo in nomes_arquivos),
                    )
                    for caminho in caminhos:
                        self.assertTrue(
                            Path(caminho).is_file(),
                            f"Sprite não encontrado: {caminho}",
                        )

    def test_romerio_e_brito_carregam_os_tres_sprites_por_estilo(self):
        estilos = ("classico", "pizzaria", "reator")
        personagens = (Romerio, Brito)

        for estilo in estilos:
            for classe_personagem in personagens:
                with self.subTest(
                    estilo=estilo,
                    personagem=classe_personagem.__name__,
                ):
                    personagem = classe_personagem(0, 0, estilo=estilo)

                    self.assertIsInstance(personagem.sprite_sheet, pygame.Surface)
                    self.assertIsInstance(personagem.sprite_walk, pygame.Surface)
                    self.assertIsInstance(personagem.sprite_slip, pygame.Surface)
                    self.assertGreater(personagem.sprite_sheet.get_width(), 0)
                    self.assertGreater(personagem.sprite_walk.get_width(), 0)
                    self.assertGreater(personagem.sprite_slip.get_width(), 0)


class TestReinicializacao(unittest.TestCase):
    def test_reiniciar_com_estilo_classico_carrega_os_dois_personagens(self):
        jogo = criar_jogo_pizzaria()

        with patch(
            "jogo.sortear_variante",
            return_value=("classica", VARIANTES_COZINHA["classica"]),
        ):
            jogo.reiniciar()

        self.assertEqual(jogo.estilo, "classico")
        for personagem in (jogo.player1, jogo.player2):
            self.assertEqual(personagem.estilo, "classico")
            self.assertGreater(personagem.sprite_sheet.get_width(), 0)
            self.assertGreater(personagem.sprite_walk.get_width(), 0)
            self.assertGreater(personagem.sprite_slip.get_width(), 0)

    def test_reiniciar_cria_estado_novo_sem_referencias_antigas(self):
        for lista in LISTAS_INGREDIENTES:
            lista.clear()

        self.addCleanup(self.limpar_listas)

        jogo = criar_jogo_pizzaria()
        jogadores_antigos = (jogo.player1, jogo.player2)
        mapa_antigo = jogo.mapa
        fase_antiga = jogo.fase
        pedido_antigo = jogo.pedido_atual
        montagens_antigas = jogo.montagens

        listas_antigas = (
            jogo.tomates,
            jogo.queijos,
            jogo.paos,
            jogo.carnes,
            jogo.alfaces,
        )
        ids_listas_antigas = tuple(id(lista) for lista in listas_antigas)

        tomate_antigo = Tomate(0, 0)
        tomate_antigo.dono = jogo.player1
        jogo.player1.objeto = tomate_antigo
        jogo.tomates.append(tomate_antigo)

        queijo_antigo = Queijo(0, 0)
        queijo_antigo.dono = jogo.player2
        jogo.player2.objeto = queijo_antigo
        jogo.queijos.append(queijo_antigo)

        pao_antigo = Pao(0, 0)
        jogo.paos.append(pao_antigo)
        montagens_antigas[0].adicionar_ingrediente(pao_antigo, "1")

        carne_antiga = Carne(0, 0)
        jogo.carnes.append(carne_antiga)

        alface_antiga = Alface(0, 0)
        jogo.alfaces.append(alface_antiga)

        objetos_antigos = {
            tomate_antigo,
            queijo_antigo,
            pao_antigo,
            carne_antiga,
            alface_antiga,
        }

        with patch(
            "jogo.sortear_variante",
            return_value=("pizzaria", VARIANTES_COZINHA["pizzaria"]),
        ):
            jogo.reiniciar()

        self.assertIsNot(jogo.player1, jogadores_antigos[0])
        self.assertIsNot(jogo.player2, jogadores_antigos[1])
        self.assertIsNot(jogo.mapa, mapa_antigo)
        self.assertIsNot(jogo.fase, fase_antiga)
        self.assertIsNot(jogo.pedido_atual, pedido_antigo)
        self.assertIsNot(jogo.montagens, montagens_antigas)

        listas_novas = (
            jogo.tomates,
            jogo.queijos,
            jogo.paos,
            jogo.carnes,
            jogo.alfaces,
        )
        self.assertNotEqual(
            tuple(id(lista) for lista in listas_novas),
            ids_listas_antigas,
        )
        self.assertTrue(
            {id(lista) for lista in listas_antigas}.isdisjoint(
                id(lista) for lista in listas_novas
            )
        )

        for lista in listas_antigas:
            self.assertEqual(lista, [])
        for lista in listas_novas:
            self.assertEqual(lista, [])
            self.assertTrue(objetos_antigos.isdisjoint(lista))

        for lista_antiga, lista_global in zip(listas_novas, LISTAS_INGREDIENTES):
            self.assertIsNot(lista_antiga, lista_global)

        self.assertIsNone(jogo.player1.objeto)
        self.assertIsNone(jogo.player2.objeto)
        self.assertIs(jogo.montagens, jogo.mapa.montagens)

        for montagem in jogo.montagens:
            self.assertEqual(montagem.ingredientes, [])
            self.assertIsNone(montagem.hamburguer)
            self.assertFalse(montagem.hamburguer_pronto)
            self.assertIs(montagem.pedido, jogo.pedido_atual)
            self.assertTrue(objetos_antigos.isdisjoint(montagem.ingredientes))
            self.assertNotIn(montagem.hamburguer, objetos_antigos)

        fontes = (
            jogo.armarios
            + jogo.armarios_queijo
            + jogo.armarios_tomate
            + jogo.armarios_alface
            + jogo.geladeiras
        )
        for fonte in fontes:
            self.assertNotIn(fonte.ingrediente, objetos_antigos)
            self.assertIsNone(fonte.ingrediente.dono)

        self.assertNotIn(jogadores_antigos[0], (jogo.player1, jogo.player2))
        self.assertNotIn(jogadores_antigos[1], (jogo.player1, jogo.player2))

    def test_instancias_de_jogo_nao_compartilham_listas_de_ingredientes(self):
        primeiro = criar_jogo_pizzaria()
        segundo = criar_jogo_pizzaria()
        tomate = Tomate(0, 0)

        primeiro.tomates.append(tomate)

        self.assertEqual(primeiro.tomates, [tomate])
        self.assertEqual(segundo.tomates, [])
        self.assertIsNot(primeiro.tomates, segundo.tomates)
        self.assertIsNot(primeiro.tomates, tomates)

    @staticmethod
    def limpar_listas():
        for lista in LISTAS_INGREDIENTES:
            lista.clear()


class TestTransicoesAudio(unittest.TestCase):
    def test_menu_para_partida_e_gameover_interrompem_a_musica_anterior(self):
        jogo = criar_jogo_pizzaria()
        jogo.fase.tempo = 0
        eventos_audio = []
        acoes_menu = iter(("start", "quit"))

        with (
            patch("jogo.Menu") as menu,
            patch("jogo.som_inicial") as musica_menu,
            patch("jogo.som_face") as musica_partida,
            patch("jogo.pygame.quit"),
        ):
            musica_menu.play.side_effect = lambda *args: eventos_audio.append(
                "menu_play"
            )
            musica_menu.stop.side_effect = lambda *args: eventos_audio.append(
                "menu_stop"
            )
            musica_partida.play.side_effect = lambda *args: eventos_audio.append(
                "partida_play"
            )
            musica_partida.stop.side_effect = lambda *args: eventos_audio.append(
                "partida_stop"
            )

            def escolher_acao():
                acao = next(acoes_menu)
                if acao == "quit":
                    self.assertTrue(musica_partida.stop.called)
                return acao

            menu.return_value.executar.side_effect = escolher_acao
            jogo.iniciar()

        self.assertEqual(musica_menu.play.call_count, 1)
        self.assertEqual(musica_partida.play.call_args.args, (-1,))
        self.assertLess(
            eventos_audio.index("menu_stop"),
            eventos_audio.index("partida_play"),
        )
        self.assertLess(
            eventos_audio.index("partida_play"),
            eventos_audio.index("partida_stop"),
        )

    def test_retry_para_canais_antigos_e_nao_reinicia_musica_do_menu(self):
        jogo = criar_jogo_pizzaria()
        jogadores_antigos = (jogo.player1, jogo.player2)
        canais_antigos = (Mock(), Mock())
        for jogador, canal in zip(jogadores_antigos, canais_antigos):
            jogador.controle_andar = canal
            jogador.andando = True

        acoes_menu = iter(("start", "retry", "quit"))
        eventos_audio = []

        with (
            patch("jogo.Menu") as menu,
            patch("jogo.som_inicial") as musica_menu,
            patch("jogo.som_face") as musica_partida,
            patch(
                "jogo.sortear_variante",
                return_value=("classica", VARIANTES_COZINHA["classica"]),
            ),
            patch(
                "jogo.Fase.atualizar",
                side_effect=lambda dt: setattr(jogo.fase, "tempo", 0),
            ),
            patch("jogo.pygame.quit"),
        ):
            musica_menu.play.side_effect = lambda *args: eventos_audio.append(
                "menu_play"
            )
            musica_menu.stop.side_effect = lambda *args: eventos_audio.append(
                "menu_stop"
            )
            musica_partida.play.side_effect = lambda *args: eventos_audio.append(
                "partida_play"
            )
            musica_partida.stop.side_effect = lambda *args: eventos_audio.append(
                "partida_stop"
            )
            menu.return_value.executar.side_effect = lambda: next(acoes_menu)

            jogo.iniciar()

        self.assertEqual(musica_menu.play.call_count, 1)
        self.assertEqual(musica_partida.play.call_count, 2)
        self.assertEqual(eventos_audio.count("menu_play"), 1)
        self.assertLess(
            eventos_audio.index("menu_stop"),
            eventos_audio.index("partida_play"),
        )
        for canal in canais_antigos:
            canal.stop.assert_called_once_with()

        self.assertIsNot(jogo.player1, jogadores_antigos[0])
        self.assertIsNot(jogo.player2, jogadores_antigos[1])
        self.assertIsNone(jogo.player1.controle_andar)
        self.assertIsNone(jogo.player2.controle_andar)
        self.assertTrue(jogadores_antigos[0].andando)
        self.assertTrue(jogadores_antigos[1].andando)

    def test_sair_da_partida_para_musicas_e_canais_de_caminhada(self):
        jogo = criar_jogo_pizzaria()
        canais = (Mock(), Mock())
        for jogador, canal in zip((jogo.player1, jogo.player2), canais):
            jogador.controle_andar = canal

        with (
            patch("jogo.Menu") as menu,
            patch("jogo.som_inicial") as musica_menu,
            patch("jogo.som_face") as musica_partida,
            patch("jogo.pygame.quit") as pygame_quit,
            patch.object(
                jogo,
                "verificarEventos",
                side_effect=lambda dt: setattr(jogo, "rodando", False),
            ),
            patch.object(jogo, "desenhar"),
        ):
            menu.return_value.executar.return_value = "start"
            jogo.iniciar()

        musica_menu.stop.assert_called()
        musica_partida.stop.assert_called()
        pygame_quit.assert_called_once_with()
        for canal in canais:
            canal.stop.assert_called_once_with()

    def test_sair_do_menu_inicial_interrompe_a_musica(self):
        jogo = criar_jogo_pizzaria()

        with (
            patch("jogo.Menu") as menu,
            patch("jogo.som_inicial") as musica_menu,
            patch("jogo.som_face") as musica_partida,
            patch("jogo.pygame.quit") as pygame_quit,
        ):
            menu.return_value.executar.return_value = "quit"
            jogo.iniciar()

        musica_menu.play.assert_called_once_with()
        musica_menu.stop.assert_called_once_with()
        musica_partida.stop.assert_called_once_with()
        musica_partida.play.assert_not_called()
        pygame_quit.assert_called_once_with()


class TestSonsDasAcoes(unittest.TestCase):
    def test_pegar_ingrediente_do_chao_toca_o_som_uma_vez(self):
        personagem = object.__new__(Romerio)
        personagem.objeto = None
        tomate = Tomate(0, 0)
        area = pygame.Rect(0, 0, 48, 48)

        with (
            patch.object(personagem, "area_interacao", return_value=area),
            patch("player.som_pegar") as som_pegar,
        ):
            personagem.pegar(
                [], [], [], [], [], [tomate], [], [], [], [], []
            )

        self.assertIs(personagem.objeto, tomate)
        self.assertIs(tomate.dono, personagem)
        som_pegar.play.assert_called_once_with()

    def test_pegar_ingrediente_de_montagem_toca_o_som_uma_vez(self):
        personagem = object.__new__(Romerio)
        personagem.objeto = None
        personagem.pos_x = 0
        personagem.pos_y = 0
        pao = Pao(0, 0)
        montagem = SimpleNamespace(
            rect=pygame.Rect(0, 0, 48, 48),
            ingredientes=[],
            pegar_ingrediente=Mock(return_value=pao),
        )

        with (
            patch.object(
                personagem,
                "area_interacao",
                return_value=pygame.Rect(0, 0, 48, 48),
            ),
            patch("player.som_pegar") as som_pegar,
        ):
            personagem.pegar(
                [], [], [], [], [], [], [], [], [], [], [montagem]
            )

        montagem.pegar_ingrediente.assert_called_once_with()
        self.assertIs(personagem.objeto, pao)
        self.assertIs(pao.dono, personagem)
        som_pegar.play.assert_called_once_with()

    def test_pegar_dos_dispensadores_toca_o_som_uma_vez(self):
        casos = (
            ("tomate", 2, 5, Tomate),
            ("alface", 3, 6, Alface),
            ("queijo", 1, 7, Queijo),
            ("pao", 0, 8, Pao),
            ("carne", 4, 9, Carne),
        )

        for nome, indice_dispensador, indice_lista, classe in casos:
            with self.subTest(dispensador=nome):
                personagem = object.__new__(Romerio)
                personagem.objeto = None
                argumentos = [[] for _ in range(11)]
                argumentos[indice_dispensador] = [SimpleNamespace(
                    posX=0,
                    posY=0,
                    rect=pygame.Rect(0, 0, 48, 48),
                )]

                with (
                    patch.object(
                        personagem,
                        "area_interacao",
                        return_value=pygame.Rect(0, 0, 48, 48),
                    ),
                    patch("player.som_pegar") as som_pegar,
                ):
                    personagem.pegar(*argumentos)

                self.assertIsInstance(personagem.objeto, classe)
                self.assertIs(personagem.objeto.dono, personagem)
                self.assertEqual(len(argumentos[indice_lista]), 1)
                som_pegar.play.assert_called_once_with()

    def test_cortar_ingrediente_solto_na_tabua_toca_o_som_uma_vez(self):
        personagem = object.__new__(Romerio)
        personagem.objeto = None
        tomate = Tomate(0, 0)
        tabua = SimpleNamespace(rect=pygame.Rect(0, 0, 48, 48))

        with (
            patch.object(
                personagem,
                "area_interacao",
                return_value=pygame.Rect(0, 0, 48, 48),
            ),
            patch("player.som_corte") as som_corte,
        ):
            personagem.cortar([tabua], [tomate], [], [], [], [])

        self.assertTrue(tomate.cortado)
        som_corte.play.assert_called_once_with()

    def test_cortar_ingrediente_carregado_permitido_toca_o_som_uma_vez(self):
        personagem = object.__new__(Romerio)
        tomate = Tomate(0, 0)
        tomate.dono = personagem
        personagem.objeto = tomate
        tabua = SimpleNamespace(rect=pygame.Rect(0, 0, 48, 48))

        with (
            patch.object(
                personagem,
                "area_interacao",
                return_value=pygame.Rect(0, 0, 48, 48),
            ),
            patch("player.som_corte") as som_corte,
        ):
            personagem.cortar([tabua], [], [], [], [], [])

        self.assertTrue(tomate.cortado)
        som_corte.play.assert_called_once_with()


class TestRenderizacao(unittest.TestCase):
    def test_superficie_logica_tem_as_dimensoes_do_mapa(self):
        jogo = criar_jogo_pizzaria()

        self.assertEqual(jogo.superficie_jogo.get_size(), (1008, 624))
        self.assertEqual(
            (jogo.largura_logica, jogo.altura_logica),
            (1008, 624),
        )
        self.assertEqual(
            jogo.superficie_interface.get_size(),
            (jogo.largura, jogo.altura),
        )
        self.assertIs(
            jogo.superficie_interface.get_parent(),
            jogo.superficie_jogo,
        )

    def test_redimensionamento_preserva_proporcao_e_cabe_na_janela(self):
        jogo = criar_jogo_pizzaria()
        largura, altura = jogo.tamanho_renderizado

        self.assertAlmostEqual(
            jogo.escala_jogo,
            min(1000 / 1008, 600 / 624),
        )
        self.assertEqual((largura, altura), (969, 600))
        self.assertLessEqual(largura, jogo.largura)
        self.assertLessEqual(altura, jogo.altura)
        self.assertAlmostEqual(
            largura / altura,
            jogo.largura_logica / jogo.altura_logica,
            delta=0.001,
        )

    def test_area_redimensionada_fica_centralizada(self):
        jogo = criar_jogo_pizzaria()
        x, y = jogo.posicao_renderizada
        largura, altura = jogo.tamanho_renderizado

        margem_esquerda = x
        margem_direita = jogo.largura - x - largura
        margem_superior = y
        margem_inferior = jogo.altura - y - altura

        self.assertEqual((margem_superior, margem_inferior), (0, 0))
        self.assertLessEqual(
            abs(margem_esquerda - margem_direita),
            1,
        )
        self.assertEqual((margem_esquerda, margem_direita), (15, 16))

    def test_desenhar_renderiza_toda_a_cena_antes_de_apresentar(self):
        eventos = []

        def registrar(nome):
            def desenhar(superficie, *args):
                eventos.append(("desenho", nome, superficie))
            return desenhar

        class JanelaDeTeste:
            def fill(self, cor):
                eventos.append(("limpar_janela", cor))

            def blit(self, superficie, posicao):
                eventos.append(("apresentar", superficie, posicao))

        jogo = object.__new__(Jogo)
        jogo.superficie_jogo = pygame.Surface((1008, 624))
        jogo.superficie_interface = jogo.superficie_jogo.subsurface(
            (0, 0, 1000, 600)
        )
        jogo.tamanho_renderizado = (969, 600)
        jogo.posicao_renderizada = (15, 0)
        jogo.tela = JanelaDeTeste()

        jogo.mapa = SimpleNamespace(
            desenhar=registrar("mapa"),
            desenhar_preparo=registrar("preparo"),
        )
        jogo.tomates = [SimpleNamespace(desenhar=registrar("tomate"))]
        jogo.queijos = [SimpleNamespace(desenhar=registrar("queijo"))]
        jogo.alfaces = [SimpleNamespace(desenhar=registrar("alface"))]
        jogo.paos = [SimpleNamespace(desenhar=registrar("pao"))]
        jogo.carnes = [SimpleNamespace(desenhar=registrar("carne"))]
        jogo.montagens = [SimpleNamespace(desenhar=registrar("montagem"))]
        jogo.player1 = SimpleNamespace(
            desenhar_indicador=registrar("indicador1"),
            desenhar=registrar("jogador1"),
        )
        jogo.player2 = SimpleNamespace(
            desenhar_indicador=registrar("indicador2"),
            desenhar=registrar("jogador2"),
        )
        jogo.fase = SimpleNamespace(desenhar=registrar("fase"))
        jogo.televisao = SimpleNamespace(desenhar=registrar("receita"))
        jogo.pedido_atual = object()

        transformar = pygame.transform.scale

        def redimensionar(superficie, tamanho):
            resultado = transformar(superficie, tamanho)
            eventos.append(("redimensionar", superficie, tamanho, resultado))
            return resultado

        with patch(
            "jogo.pygame.transform.scale",
            side_effect=redimensionar,
        ), patch("jogo.pygame.display.flip"):
            jogo.desenhar()

        indices_desenho = [
            indice
            for indice, evento in enumerate(eventos)
            if evento[0] == "desenho"
        ]
        indice_redimensionamento = next(
            indice
            for indice, evento in enumerate(eventos)
            if evento[0] == "redimensionar"
        )
        indice_apresentacao = next(
            indice
            for indice, evento in enumerate(eventos)
            if evento[0] == "apresentar"
        )

        self.assertTrue(indices_desenho)
        self.assertLess(max(indices_desenho), indice_redimensionamento)
        self.assertLess(indice_redimensionamento, indice_apresentacao)

        for evento in eventos:
            if evento[0] != "desenho":
                continue
            superficie = evento[2]
            self.assertTrue(
                superficie is jogo.superficie_jogo
                or superficie is jogo.superficie_interface,
                f"{evento[1]} foi desenhado fora da superfície lógica",
            )

        evento_redimensionamento = eventos[indice_redimensionamento]
        evento_apresentacao = eventos[indice_apresentacao]
        self.assertIs(evento_redimensionamento[1], jogo.superficie_jogo)
        self.assertEqual(evento_redimensionamento[2], (969, 600))
        self.assertIs(
            evento_apresentacao[1],
            evento_redimensionamento[3],
        )

    def test_coordenadas_dos_objetos_nao_mudam_ao_desenhar(self):
        jogo = criar_jogo_pizzaria()
        tomate = Tomate(48, 96)
        jogo.tomates.append(tomate)
        self.addCleanup(
            lambda: jogo.tomates.remove(tomate)
            if tomate in jogo.tomates
            else None
        )

        posicoes_jogadores = (
            (jogo.player1.pos_x, jogo.player1.pos_y, jogo.player1.rect.topleft),
            (jogo.player2.pos_x, jogo.player2.pos_y, jogo.player2.rect.topleft),
        )
        posicao_tomate = (tomate.x, tomate.y, tomate.rect.topleft)
        posicoes_montagens = tuple(
            montagem.rect.topleft for montagem in jogo.montagens
        )
        objetos_estacoes = (
            jogo.mapa.tabuas
            + jogo.mapa.fornos
            + jogo.armarios
            + jogo.armarios_queijo
            + jogo.armarios_tomate
            + jogo.armarios_alface
            + jogo.geladeiras
            + jogo.entregas
            + jogo.lixeiras
        )
        posicoes_estacoes = tuple(
            (objeto.posX, objeto.posY) for objeto in objetos_estacoes
        )

        jogo.desenhar()

        self.assertEqual(
            (
                (jogo.player1.pos_x, jogo.player1.pos_y, jogo.player1.rect.topleft),
                (jogo.player2.pos_x, jogo.player2.pos_y, jogo.player2.rect.topleft),
            ),
            posicoes_jogadores,
        )
        self.assertEqual(
            (tomate.x, tomate.y, tomate.rect.topleft),
            posicao_tomate,
        )
        self.assertEqual(
            tuple(montagem.rect.topleft for montagem in jogo.montagens),
            posicoes_montagens,
        )
        self.assertEqual(
            tuple(
                (objeto.posX, objeto.posY)
                for objeto in objetos_estacoes
            ),
            posicoes_estacoes,
        )
        self.assertEqual(jogo.televisao.x, 836)

    def test_menus_de_inicio_e_gameover_recebem_a_janela_original(self):
        jogo = criar_jogo_pizzaria()
        jogo.fase.tempo = 0

        with (
            patch("jogo.Menu") as menu,
            patch("jogo.som_inicial"),
            patch("jogo.som_face"),
            patch("jogo.pygame.quit"),
        ):
            menu.return_value.executar.side_effect = ["start", "quit"]
            jogo.iniciar()

        self.assertEqual(menu.call_count, 2)
        chamada_inicio, chamada_gameover = menu.call_args_list
        self.assertIs(chamada_inicio.args[0], jogo.tela)
        self.assertEqual(
            chamada_inicio.args[1:],
            (jogo.largura, jogo.altura, "inicio"),
        )
        self.assertIs(chamada_gameover.args[0], jogo.tela)
        self.assertEqual(
            chamada_gameover.args[1:],
            (jogo.largura, jogo.altura, "gameover"),
        )

if __name__ == "__main__":
    unittest.main()
