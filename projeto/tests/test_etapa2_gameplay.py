"""Regressões de movimento, interação e acesso aos mapas da etapa 2."""

import apoio
import pygame
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from constantes import TILE_SIZE
from itens import ArrozEstelar, Massa, Pizza, Pao, Tomate
from mapa import (
    CONFIGURACOES_MODELEX,
    MODELOS_BASE,
    MODELOS_MAPA,
    SIMBOLOS_POR_ESTILO,
    VARIANTES_COZINHA,
    Mapa,
    compor_modelo_modular,
)
from jogo import Jogo
from montagem import Montagem
from player import (
    CHANCE_ESCORREGAR,
    DURACAO_ESCORREGAO_MS,
    Brito,
    Romerio,
    alfaces,
    carnes,
    paos,
    queijos,
    tomates,
)


SIMBOLOS_COM_COLISAO = set("1234BCWSMNORLTUDQGVA")
POSICOES_INICIAIS = ((624, 192), (240, 240))
DISPENSADORES = {
    "classico": set("34TLR"),
    "pizzaria": set("DQV"),
    "reator": set("ACG"),
}


class TeclasPressionadas(dict):
    def __getitem__(self, tecla):
        return self.get(tecla, False)


def argumentos_indicador(**opcionais):
    argumentos = [[], [], [], [], [], [], [], [], [], [], []]
    argumentos.extend((
        opcionais.get("dispensadores"),
        opcionais.get("ingredientes_tematicos"),
        opcionais.get("produtos"),
        opcionais.get("montagens"),
        opcionais.get("entregas"),
    ))
    return argumentos


def remapear(modelo, estilo):
    remapeamento = SIMBOLOS_POR_ESTILO.get(estilo, {})
    return [
        "".join(remapeamento.get(simbolo, simbolo) for simbolo in linha)
        for linha in modelo
    ]


def celulas_alcancaveis(modelo, estilo):
    mapa = remapear(modelo, estilo)
    pisos = {
        (coluna, linha)
        for linha, texto in enumerate(mapa)
        for coluna, simbolo in enumerate(texto)
        if simbolo not in SIMBOLOS_COM_COLISAO
    }
    alcancaveis = set()
    componentes_jogadores = []

    for pos_x, pos_y in POSICOES_INICIAIS:
        inicio = (
            (pos_x + 32) // TILE_SIZE,
            (pos_y + 86) // TILE_SIZE,
        )
        if inicio not in pisos:
            raise AssertionError(f"Posição inicial bloqueada: {estilo} {inicio}")

        vistos = {inicio}
        fila = [inicio]
        while fila:
            coluna, linha = fila.pop()
            for vizinho in (
                (coluna + 1, linha),
                (coluna - 1, linha),
                (coluna, linha + 1),
                (coluna, linha - 1),
            ):
                if vizinho in pisos and vizinho not in vistos:
                    vistos.add(vizinho)
                    fila.append(vizinho)
        componentes_jogadores.append(vistos)
        alcancaveis.update(vistos)

    if len(componentes_jogadores) == 2 and not (
        componentes_jogadores[0] & componentes_jogadores[1]
    ):
        raise AssertionError(f"Os jogadores começam separados: {estilo}")

    return mapa, alcancaveis


class TestEscorregoes(unittest.TestCase):
    def test_passar_por_ingrediente_tem_chance_baixa_e_recupera_controle(self):
        personagem = Romerio(100, 100)
        ingrediente = Tomate(149, 176)
        teclas = TeclasPressionadas({personagem.teclas["direita"]: True})

        with (
            patch("player.pygame.key.get_pressed", return_value=teclas),
            patch("player.pygame.time.get_ticks", return_value=1000),
            patch("player.random.random", return_value=0.0) as sorteio,
            patch("player.som_andar") as som_andar,
        ):
            personagem.mover([], [ingrediente])

        self.assertEqual(CHANCE_ESCORREGAR, 0.05)
        self.assertEqual(DURACAO_ESCORREGAO_MS, 600)
        self.assertTrue(personagem.escorregando)
        self.assertFalse(personagem.andando)
        self.assertIsNone(personagem.controle_andar)
        self.assertEqual(personagem.pos_x, 104)
        som_andar.play.return_value.stop.assert_called_once_with()

        # A animação de queda usa a spritesheet de escorregão existente.
        with patch("player.pygame.time.get_ticks", return_value=1250):
            personagem.desenhar(pygame.Surface((256, 256), pygame.SRCALPHA))

        evento_pegar = SimpleNamespace(
            type=pygame.KEYDOWN,
            key=personagem.teclas["pegar"],
        )
        with patch("player.pygame.time.get_ticks", return_value=1500):
            personagem.verificar_habilidades(
                evento_pegar,
                [], [], [], [], [], [], [], [], [], [], [], [], [],
                ["F"], [], {}, [],
            )
            personagem.mover([], [ingrediente])

        self.assertTrue(personagem.escorregando)
        self.assertEqual(personagem.pos_x, 104)
        sorteio.assert_called_once_with()

        with (
            patch("player.pygame.time.get_ticks", return_value=1600),
            patch("player.pygame.key.get_pressed", return_value=teclas),
        ):
            personagem.mover([], [ingrediente])

        self.assertFalse(personagem.escorregando)
        self.assertEqual(personagem.pos_x, 108)
        sorteio.assert_called_once_with()

    def test_falha_de_sorteio_nao_rola_novamente_durante_a_mesma_passagem(self):
        personagem = Brito(100, 100)
        ingrediente = Tomate(149, 176)
        teclas = TeclasPressionadas({personagem.teclas["direita"]: True})

        with (
            patch("player.pygame.key.get_pressed", return_value=teclas),
            patch("player.pygame.time.get_ticks", return_value=1000),
            patch("player.random.random", return_value=0.99) as sorteio,
            patch("player.som_andar"),
        ):
            personagem.mover([], [ingrediente])
            personagem.mover([], [ingrediente])

        self.assertFalse(personagem.escorregando)
        sorteio.assert_called_once_with()

    def test_ingredientes_carregados_ou_montados_nao_disparam_escorregao(self):
        personagem = Romerio(100, 100)
        carregado = Tomate(149, 176)
        carregado.dono = personagem
        montado = Pao(149, 176)
        montado.em_montagem = True
        teclas = TeclasPressionadas({personagem.teclas["direita"]: True})

        with (
            patch("player.pygame.key.get_pressed", return_value=teclas),
            patch("player.pygame.time.get_ticks", return_value=1000),
            patch("player.random.random") as sorteio,
            patch("player.som_andar"),
        ):
            personagem.mover([], [carregado, montado])

        self.assertFalse(personagem.escorregando)
        sorteio.assert_not_called()


class TestMovimento(unittest.TestCase):
    def _mover_por_um_segundo(self, personagem, teclas, quadros, dt):
        with (
            patch("player.pygame.key.get_pressed", return_value=teclas),
            patch("player.som_andar"),
        ):
            for _ in range(quadros):
                personagem.mover([], dt=dt)

    def test_distancia_horizontal_e_independente_do_fps(self):
        deslocamentos = []
        for quadros, dt in ((30, 1 / 30), (60, 1 / 60)):
            personagem = Romerio(100, 100)
            x_inicial = personagem.pos_x
            teclas = TeclasPressionadas({personagem.teclas["direita"]: True})
            self._mover_por_um_segundo(personagem, teclas, quadros, dt)
            deslocamentos.append(personagem.pos_x - x_inicial)

        self.assertEqual(deslocamentos, [240, 240])

    def test_movimento_diagonal_nao_e_mais_rapido_que_horizontal(self):
        personagem = Romerio(100, 100)
        x_inicial, y_inicial = personagem.pos_x, personagem.pos_y
        teclas = TeclasPressionadas({
            personagem.teclas["direita"]: True,
            personagem.teclas["baixo"]: True,
        })

        self._mover_por_um_segundo(personagem, teclas, 60, 1 / 60)

        deslocamento_x = personagem.pos_x - x_inicial
        deslocamento_y = personagem.pos_y - y_inicial
        self.assertAlmostEqual(deslocamento_x, deslocamento_y, delta=1)
        self.assertAlmostEqual(
            (deslocamento_x**2 + deslocamento_y**2) ** 0.5,
            240,
            delta=1,
        )

    def test_subpassos_de_fps_baixo_nao_atravessam_estacoes(self):
        personagem = Romerio(0, 0)
        obstaculo = pygame.Rect(60, personagem.rect.y, 48, 48)
        teclas = TeclasPressionadas({personagem.teclas["direita"]: True})

        with (
            patch("player.pygame.key.get_pressed", return_value=teclas),
            patch("player.som_andar"),
        ):
            personagem.mover([obstaculo], dt=0.5)

        self.assertEqual(personagem.rect.right, obstaculo.left)
        self.assertFalse(personagem.rect.colliderect(obstaculo))

    def test_jogo_entrega_ingredientes_das_tres_cozinhas_ao_movimento(self):
        casos = (
            ("classica", "classico", Tomate, None),
            ("pizzaria", "pizzaria", Massa, "Dough"),
            ("reator", "reator", ArrozEstelar, "StarRice"),
        )
        listas_classicas = (tomates, queijos, paos, carnes, alfaces)
        snapshots = [list(lista) for lista in listas_classicas]

        def restaurar_listas():
            for lista, snapshot in zip(listas_classicas, snapshots):
                lista.clear()
                lista.extend(snapshot)

        self.addCleanup(restaurar_listas)

        for nome, estilo, classe_ingrediente, lista_nome in casos:
            with self.subTest(cozinha=nome):
                entrada = VARIANTES_COZINHA[nome]
                with patch(
                    "jogo.sortear_variante",
                    return_value=(nome, entrada),
                ):
                    jogo = Jogo()

                jogo.mapa.colisoes.clear()
                personagem = jogo.player1
                personagem.pos_x = 100
                personagem.pos_y = 100
                personagem.rect.topleft = (116, 176)
                ingrediente = classe_ingrediente(149, 176)
                if lista_nome is None:
                    jogo.tomates.append(ingrediente)
                else:
                    jogo.ingredientes_tematicos[lista_nome].append(ingrediente)

                teclas = TeclasPressionadas({
                    personagem.teclas["direita"]: True,
                })
                with (
                    patch("jogo.pygame.event.get", return_value=[]),
                    patch("player.pygame.key.get_pressed", return_value=teclas),
                    patch("player.random.random", return_value=0.0),
                    patch("player.som_andar"),
                ):
                    jogo.verificarEventos()

                self.assertTrue(personagem.escorregando)


class TestInteracoesEPosicionamento(unittest.TestCase):
    def test_area_de_interacao_aponta_para_a_celula_nas_quatro_direcoes(self):
        personagem = Romerio(4 * TILE_SIZE, 4 * TILE_SIZE)
        coluna = personagem.rect.centerx // TILE_SIZE
        linha = personagem.rect.centery // TILE_SIZE
        casos = (
            ("frente", False, (coluna, linha + 1)),
            ("costas", False, (coluna, linha - 1)),
            ("lado", True, (coluna + 1, linha)),
            ("lado", False, (coluna - 1, linha)),
        )

        for direcao, flip, esperado in casos:
            with self.subTest(direcao=direcao, flip=flip):
                personagem.direcao = direcao
                personagem.virado_esquerda = flip
                area = personagem.area_interacao()
                self.assertEqual(
                    (area.x // TILE_SIZE, area.y // TILE_SIZE),
                    esperado,
                )
                self.assertEqual(area.size, (TILE_SIZE, TILE_SIZE))

    def test_movimento_para_na_colisao_com_estacao(self):
        personagem = Romerio(96, 96)
        obstaculo = pygame.Rect(148, 160, TILE_SIZE, TILE_SIZE)
        teclas = TeclasPressionadas({personagem.teclas["direita"]: True})

        with (
            patch("player.pygame.key.get_pressed", return_value=teclas),
            patch("player.som_andar") as som_andar,
        ):
            personagem.mover([obstaculo])
            personagem.mover([obstaculo])

        self.assertEqual(personagem.rect.right, obstaculo.left)
        self.assertFalse(personagem.rect.colliderect(obstaculo))
        self.assertFalse(personagem.andando)
        som_andar.play.return_value.stop.assert_called_once_with()

    def test_direcao_atualiza_antes_de_interacoes_no_mesmo_quadro_para_ambos(self):
        with patch(
            "jogo.sortear_variante",
            return_value=("classica", VARIANTES_COZINHA["classica"]),
        ):
            jogo = Jogo()

        jogo.montagens = []
        tomate1 = Tomate(624, 192)
        tomate2 = Tomate(240, 240)
        jogo.tomates.extend((tomate1, tomate2))
        teclas = TeclasPressionadas({
            pygame.K_UP: True,
            pygame.K_w: True,
            pygame.K_KP1: True,
            pygame.K_f: True,
        })
        eventos = [
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_KP1}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_f}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w}),
        ]

        with (
            patch("jogo.pygame.event.get", return_value=eventos),
            patch("jogo.pygame.key.get_pressed", return_value=teclas),
            patch("player.som_pegar"),
            patch("player.som_andar"),
        ):
            jogo.verificarEventos()

        self.assertIs(jogo.player1.objeto, tomate1)
        self.assertIs(jogo.player2.objeto, tomate2)
        self.assertEqual(jogo.player1.direcao, "costas")
        self.assertEqual(jogo.player2.direcao, "costas")

    def test_ingrediente_solto_fica_na_celula_a_frente_em_todas_as_direcoes(self):
        modelo = ["F" * 21 for _ in range(13)]
        casos = (
            ("frente", False, (0, 1)),
            ("costas", False, (0, -1)),
            ("lado", True, (1, 0)),
            ("lado", False, (-1, 0)),
        )

        for direcao, flip, (delta_x, delta_y) in casos:
            with self.subTest(direcao=direcao, flip=flip):
                personagem = Romerio(4 * TILE_SIZE, 4 * TILE_SIZE)
                personagem.direcao = direcao
                personagem.virado_esquerda = flip
                ingrediente = Tomate(0, 0)
                ingrediente.dono = personagem
                personagem.objeto = ingrediente
                tomates = [ingrediente]
                celula_atual = (
                    personagem.rect.centerx // TILE_SIZE,
                    personagem.rect.centery // TILE_SIZE,
                )
                celula_alvo = (
                    celula_atual[0] + delta_x,
                    celula_atual[1] + delta_y,
                )

                with patch("player.som_solta"):
                    personagem.largar(
                        [], tomates, [], [], [], [], [], [], modelo
                    )

                self.assertIsNone(personagem.objeto)
                self.assertIsNone(ingrediente.dono)
                self.assertEqual(
                    (
                        ingrediente.rect.centerx // TILE_SIZE,
                        ingrediente.rect.centery // TILE_SIZE,
                    ),
                    celula_alvo,
                )

    def test_montagens_e_dispensadores_nao_compartilham_celula_tematica(self):
        estilos = ("classico", "pizzaria", "reator")
        for numero, modelo in enumerate(MODELOS_MAPA, start=1):
            for estilo in estilos:
                with self.subTest(modelo=numero, estilo=estilo):
                    mapa = Mapa(modelo=modelo, estilo=estilo)
                    mapa.criar_colisoes()
                    for montagem in mapa.montagens:
                        for fonte in mapa.dispensadores_tematicos:
                            self.assertFalse(
                                montagem.rect.colliderect(fonte.rect),
                                f"{estilo} mapa {numero}: montagem sobre "
                                f"dispensador {fonte.simbolo}",
                            )

                    for montagem in mapa.montagens:
                        coluna = montagem.rect.x // TILE_SIZE
                        linha = montagem.rect.y // TILE_SIZE
                        vizinhos = (
                            (coluna, linha - 1),
                            (coluna, linha + 1),
                            (coluna - 1, linha),
                            (coluna + 1, linha),
                        )
                        self.assertTrue(any(
                            0 <= y < len(mapa.mapa)
                            and 0 <= x < len(mapa.mapa[y])
                            and mapa.mapa[y][x] == "F"
                            for x, y in vizinhos
                        ))

    def test_produto_montado_usa_o_ponto_de_apoio_da_superficie(self):
        montagem = Montagem(3 * TILE_SIZE, 3 * TILE_SIZE)
        pizza = Pizza(0, 0, "pizza_facil")

        self.assertTrue(montagem.colocar_produto(pizza, "2"))
        self.assertEqual(pizza.rect.center, montagem.ponto_apoio("2"))

    def test_indicadores_sinalizam_retirada_montagem_e_entrega(self):
        personagem = Romerio(0, 0)
        montagem = Montagem(0, 0)
        pao_montado = Pao(0, 0)
        self.assertTrue(montagem.adicionar_ingrediente(pao_montado, "1"))
        argumentos = argumentos_indicador(montagens=[montagem])
        argumentos[1] = [SimpleNamespace(rect=montagem.rect.copy())]

        with patch.object(
            personagem, "area_interacao", return_value=montagem.rect.copy()
        ):
            personagem.verificar_indicador(*argumentos)
        self.assertEqual(personagem.indicador.nome, "GrabPin.png")
        self.assertIs(personagem.alvo_indicador, montagem)

        personagem.objeto = Tomate(0, 0)
        montagem_vazia = Montagem(48, 0)
        entrega = SimpleNamespace(rect=pygame.Rect(96, 0, 48, 48))
        with patch.object(
            personagem, "area_interacao", return_value=montagem_vazia.rect.copy()
        ):
            personagem.verificar_indicador(
                *argumentos_indicador(montagens=[montagem_vazia])
            )
        self.assertEqual(personagem.indicador.nome, "ArrowPin.png")
        self.assertIs(personagem.alvo_indicador, montagem_vazia)

        personagem.objeto = Pizza(0, 0, "pizza_facil")
        with patch.object(
            personagem, "area_interacao", return_value=entrega.rect.copy()
        ):
            personagem.verificar_indicador(
                *argumentos_indicador(entregas=[entrega])
            )
        self.assertEqual(personagem.indicador.nome, "ArrowPin.png")
        self.assertIs(personagem.alvo_indicador, entrega)


class TestAcessoDosMapas(unittest.TestCase):
    def test_estacoes_e_montagens_sao_alcancaveis_nas_18_plantas_e_81_combinacoes(self):
        mapas = [
            (f"modelo_{indice}", modelo)
            for indice, modelo in enumerate(MODELOS_MAPA, start=1)
        ]
        mapas.extend(
            (
                f"base_{indice_base}_config_{indice_config}",
                compor_modelo_modular(base, configuracao),
            )
            for indice_base, base in enumerate(MODELOS_BASE, start=1)
            for indice_config, configuracao in enumerate(
                CONFIGURACOES_MODELEX, start=1
            )
        )

        self.assertEqual(len(MODELOS_MAPA), 18)
        self.assertEqual(
            len(CONFIGURACOES_MODELEX) * len(MODELOS_BASE),
            81,
        )

        for nome, modelo in mapas:
            for estilo in ("classico", "pizzaria", "reator"):
                with self.subTest(mapa=nome, estilo=estilo):
                    mapa_estilo, alcancaveis = celulas_alcancaveis(
                        modelo, estilo
                    )
                    fontes_esperadas = DISPENSADORES[estilo]
                    fontes_encontradas = {
                        simbolo
                        for linha in mapa_estilo
                        for simbolo in linha
                        if simbolo in fontes_esperadas
                    }
                    self.assertEqual(fontes_encontradas, fontes_esperadas)

                    operaveis = set("BONU") | fontes_esperadas
                    for linha, texto in enumerate(mapa_estilo):
                        for coluna, simbolo in enumerate(texto):
                            tem_acesso_por_piso = any(
                                vizinho in alcancaveis
                                for vizinho in (
                                    (coluna + 1, linha),
                                    (coluna - 1, linha),
                                    (coluna, linha + 1),
                                    (coluna, linha - 1),
                                )
                            )
                            if simbolo in operaveis:
                                self.assertTrue(
                                    tem_acesso_por_piso,
                                    f"{nome}/{estilo}: estação {simbolo} "
                                    f"inacessível em {(coluna, linha)}",
                                )
                            if simbolo in "1234":
                                vizinhos = (
                                    (coluna + 1, linha),
                                    (coluna - 1, linha),
                                    (coluna, linha + 1),
                                    (coluna, linha - 1),
                                )
                                tem_piso_adjacente = any(
                                    0 <= y < len(mapa_estilo)
                                    and 0 <= x < len(mapa_estilo[y])
                                    and mapa_estilo[y][x] == "F"
                                    for x, y in vizinhos
                                )
                                if tem_piso_adjacente:
                                    self.assertTrue(
                                        tem_acesso_por_piso,
                                        f"{nome}/{estilo}: montagem "
                                        f"inacessível em {(coluna, linha)}",
                                    )


class TestPontosParaLargar(unittest.TestCase):
    def test_ajudante_reconhece_superficies_de_largar_incluindo_forno(self):
        mapa = object.__new__(Mapa)
        mapa.mapa = ["FBOX"]

        self.assertTrue(mapa.pode_largar(0, 0))
        self.assertTrue(mapa.pode_largar(TILE_SIZE, 0))
        self.assertTrue(mapa.pode_largar(2 * TILE_SIZE, 0))
        self.assertFalse(mapa.pode_largar(3 * TILE_SIZE, 0))
        self.assertFalse(mapa.pode_largar(-1, 0))
        self.assertFalse(mapa.pode_largar(0, -1))
        self.assertFalse(mapa.pode_largar(0, TILE_SIZE))


if __name__ == "__main__":
    unittest.main()
