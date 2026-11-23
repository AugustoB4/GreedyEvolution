"""Testes estruturais dos modelos de mapa."""

import apoio
import pygame
import re
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from constantes import ALTURA, LARGURA, TILE_SIZE
from jogo import Jogo
from player import Personagem
from mapa import (
    CONFIGURACOES_MODELEX,
    MODULOS_BANCADAS,
    MODELO1, MODELO2, MODELO3, MODELO4, MODELO5,
    MODELO_6, MODELO_7, MODELO_8, MODELO_9,
    MODELEX1, MODELEX2, MODELEX3, MODELEX4, MODELEX5,
    MODELEX6, MODELEX7, MODELEX8, MODELEX9,
    MODELOS_BASE, MODELOS_MODULARES, Mapa, VARIANTES_COZINHA,
    compor_modelo_modular,
    gerar_modelos_modulares,
    problemas_validacao_modelo,
    normalizar_bancadas,
    validar_modelo,
    MODELOS_MAPA,
)


MODELOS_NOMEADOS = (
    ("MODELO1", MODELO1), ("MODELO2", MODELO2),
    ("MODELO3", MODELO3), ("MODELO4", MODELO4),
    ("MODELO5", MODELO5), ("MODELO_6", MODELO_6),
    ("MODELO_7", MODELO_7), ("MODELO_8", MODELO_8),
    ("MODELO_9", MODELO_9), ("MODELEX1", MODELEX1),
    ("MODELEX2", MODELEX2), ("MODELEX3", MODELEX3),
    ("MODELEX4", MODELEX4), ("MODELEX5", MODELEX5),
    ("MODELEX6", MODELEX6), ("MODELEX7", MODELEX7),
    ("MODELEX8", MODELEX8), ("MODELEX9", MODELEX9),
)

# Posições de Jogo.__init__; retângulo lógico de Personagem.__init__.
POSICOES_INICIAIS = (
    ("Romerio", 624, 192),
    ("Brito", 240, 240),
)

# Símbolos que Mapa.criar_colisoes transforma em obstáculos.
SIMBOLOS_COM_COLISAO = set("1234BCWSMNORLTUDQGVA")


class TestModelosMapa(unittest.TestCase):
    def test_modelos_tem_dimensoes_regulares_e_compativeis_com_tiles(self):
        linhas_esperadas = len(MODELOS_NOMEADOS[0][1])
        colunas_esperadas = len(MODELOS_NOMEADOS[0][1][0])

        for nome, modelo in MODELOS_NOMEADOS:
            with self.subTest(modelo=nome):
                self.assertEqual(
                    len(modelo), linhas_esperadas,
                    f"{nome}: quantidade de linhas diferente",
                )
                self.assertEqual(
                    [len(linha) for linha in modelo],
                    [colunas_esperadas] * linhas_esperadas,
                    f"{nome}: linhas com larguras diferentes",
                )

                largura_px = colunas_esperadas * TILE_SIZE
                altura_px = linhas_esperadas * TILE_SIZE
                self.assertEqual(largura_px % TILE_SIZE, 0)
                self.assertEqual(altura_px % TILE_SIZE, 0)
                self.assertEqual((largura_px, altura_px), (1008, 624))

                # Registra o enquadramento atual sem alterar a grade do mapa.
                self.assertEqual(largura_px - LARGURA, 8)
                self.assertEqual(altura_px - ALTURA, 24)

    def test_jogo_usa_as_novas_posicoes_iniciais(self):
        variante = VARIANTES_COZINHA["pizzaria"]
        with patch(
            "jogo.sortear_variante",
            return_value=("pizzaria", variante),
        ):
            jogo = Jogo()

        self.assertEqual((jogo.player1.pos_x, jogo.player1.pos_y), (624, 192))
        self.assertEqual((jogo.player2.pos_x, jogo.player2.pos_y), (240, 240))

    def test_simbolos_dos_modelos_existem_em_todos_os_estilos(self):
        estilos = ("classico", "pizzaria", "reator")
        simbolos_por_estilo = {
            estilo: set(Mapa(modelo=[], estilo=estilo).tiles)
            for estilo in estilos
        }

        for nome, modelo in MODELOS_NOMEADOS:
            simbolos_usados = set("".join(modelo))
            for estilo in estilos:
                with self.subTest(modelo=nome, estilo=estilo):
                    desconhecidos = simbolos_usados - simbolos_por_estilo[estilo]
                    self.assertEqual(
                        desconhecidos, set(),
                        f"{nome}: símbolos sem tile em {estilo}: "
                        f"{sorted(desconhecidos)}",
                    )

    def test_entrega_funcional_esta_em_N_e_M_e_apenas_visual(self):
        for nome, modelo in MODELOS_NOMEADOS:
            with self.subTest(modelo=nome):
                posicoes_n = {
                    (linha, coluna)
                    for linha, texto in enumerate(modelo)
                    for coluna, simbolo in enumerate(texto)
                    if simbolo == "N"
                }
                posicoes_m = {
                    (linha, coluna)
                    for linha, texto in enumerate(modelo)
                    for coluna, simbolo in enumerate(texto)
                    if simbolo == "M"
                }
                self.assertEqual(len(posicoes_n), 1, f"{nome}: esperado um N")
                self.assertEqual(len(posicoes_m), 1, f"{nome}: esperado um M")

                mapa = Mapa(modelo=modelo, estilo="classico")
                mapa.criar_colisoes()

                entregas = {
                    (entrega.posY // TILE_SIZE, entrega.posX // TILE_SIZE)
                    for entrega in mapa.entregas
                }
                self.assertEqual(
                    entregas, posicoes_n,
                    f"{nome}: somente N cria a estação funcional",
                )
                self.assertTrue(
                    entregas.isdisjoint(posicoes_m),
                    f"{nome}: M não pode ser estação funcional",
                )

                personagem = object.__new__(Personagem)
                hamburguer_n = SimpleNamespace(
                    nome="Hamburguer", dono=object(), em_montagem=True
                )
                personagem.objeto = hamburguer_n
                linha_n, coluna_n = next(iter(posicoes_n))
                area_n = pygame.Rect(
                    coluna_n * TILE_SIZE,
                    linha_n * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                with patch.object(
                    Personagem, "area_interacao", return_value=area_n
                ), patch("player.som_solta"):
                    resultado = personagem.largar(
                        [], [], [], [], [], [], [], mapa.entregas, modelo
                    )
                self.assertIs(resultado, hamburguer_n)
                self.assertIsNone(personagem.objeto)

                hamburguer_m = SimpleNamespace(
                    nome="Hamburguer", dono=object(), em_montagem=True
                )
                personagem.objeto = hamburguer_m
                linha_m, coluna_m = next(iter(posicoes_m))
                area_m = pygame.Rect(
                    coluna_m * TILE_SIZE,
                    linha_m * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                with patch.object(
                    Personagem, "area_interacao", return_value=area_m
                ), patch("player.som_solta"):
                    resultado = personagem.largar(
                        [], [], [], [], [], [], [], mapa.entregas, modelo
                    )
                self.assertIsNone(resultado)
                self.assertIs(
                    personagem.objeto,
                    hamburguer_m,
                    f"{nome}: largar em M não deve entregar o hambúrguer",
                )

                posicoes_com_colisao = {
                    (rect.y // TILE_SIZE, rect.x // TILE_SIZE)
                    for rect in mapa.colisoes
                }
                self.assertTrue(posicoes_n.issubset(posicoes_com_colisao))
                self.assertTrue(posicoes_m.issubset(posicoes_com_colisao))

    def test_posicoes_iniciais_nao_sobrepoem_obstaculos(self):
        for nome, modelo in MODELOS_NOMEADOS:
            for jogador, x, y in POSICOES_INICIAIS:
                # Personagem.rect tem deslocamento (16, 76) e tamanho 32 x 20.
                left, top = x + 16, y + 76
                width, height = 32, 20
                colunas = range(
                    left // TILE_SIZE,
                    (left + width - 1) // TILE_SIZE + 1,
                )
                linhas = range(
                    top // TILE_SIZE,
                    (top + height - 1) // TILE_SIZE + 1,
                )

                with self.subTest(modelo=nome, jogador=jogador):
                    bloqueios = []
                    fora_do_mapa = []
                    for linha in linhas:
                        for coluna in colunas:
                            if not (0 <= linha < len(modelo)):
                                fora_do_mapa.append((linha, coluna))
                            elif not (0 <= coluna < len(modelo[linha])):
                                fora_do_mapa.append((linha, coluna))
                            elif modelo[linha][coluna] in SIMBOLOS_COM_COLISAO:
                                bloqueios.append(
                                    (linha, coluna, modelo[linha][coluna])
                                )

                    self.assertEqual(
                        fora_do_mapa, [],
                        f"{nome}: posição de {jogador} fora do mapa",
                    )
                    self.assertEqual(
                        bloqueios, [],
                        f"{nome}: posição de {jogador} sobrepõe obstáculos",
                    )

    def test_todos_os_modelos_validam_acesso_e_equipamentos_nas_tres_cozinhas(self):
        for nome, modelo in MODELOS_NOMEADOS:
            for estilo in ("classico", "pizzaria", "reator"):
                with self.subTest(modelo=nome, estilo=estilo):
                    self.assertTrue(
                        validar_modelo(modelo, estilo),
                        problemas_validacao_modelo(modelo, estilo),
                    )

        self.assertEqual(len(MODELOS_MAPA), 18)
        for indice, modelo in enumerate(MODELOS_MAPA, start=1):
            for estilo in ("classico", "pizzaria", "reator"):
                with self.subTest(modelo=indice, estilo=estilo):
                    self.assertTrue(
                        validar_modelo(modelo, estilo),
                        problemas_validacao_modelo(modelo, estilo),
                    )


class TestMapasModulares(unittest.TestCase):
    def test_modelos_modulares_atuais_tem_a_grade_dos_modelos_base(self):
        self.assertEqual(len(MODELOS_MODULARES), len(MODELOS_BASE))
        linhas = len(MODELOS_BASE[0])
        larguras = [len(linha) for linha in MODELOS_BASE[0]]

        for numero, modelo in enumerate(MODELOS_MODULARES, start=1):
            with self.subTest(modelo=f"MODELEX{numero}"):
                self.assertEqual(len(modelo), linhas)
                self.assertEqual([len(linha) for linha in modelo], larguras)

    def test_normalizacao_divide_bancadas_longas_sem_remover_dispensadores(self):
        modelo_longo = list(MODELO1)
        modelo_longo[3] = "W1" + "1" * 11 + "F" * 7 + "W"
        modelo_longo[4] = "W1" + "2" * 11 + "F" * 7 + "W"
        modelo_longo[5] = "W1" + "F" * 18 + "W"
        normalizado_longo = normalizar_bancadas(modelo_longo)
        segmentos = re.findall(r"[234LT]+", normalizado_longo[4])
        self.assertEqual([len(segmento) for segmento in segmentos], [5, 5])

        for nome, modelo in MODELOS_NOMEADOS:
            with self.subTest(modelo=nome):
                normalizado = normalizar_bancadas(modelo)
                self.assertEqual(normalizado, modelo)
                for linha in normalizado[3:9]:
                    self.assertLessEqual(
                        max(
                            (len(run) for run in re.findall(r"[234LT]+", linha)),
                            default=0,
                        ),
                        6,
                    )

        self.assertTrue({"4", "3", "T", "L"}.issubset(set(MODELO_9[8])))

    def test_modulacao_rejeita_resultado_invalido_e_geracao_tem_fallback_limitado(self):
        mapa_invalido = list(MODELO1)
        linha = list(mapa_invalido[4])
        linha[4:6] = list("44")
        mapa_invalido[4] = "".join(linha)
        problemas = problemas_validacao_modelo(mapa_invalido, "classico")
        self.assertTrue(any("duplicados em sequência" in p for p in problemas))

        primeiro = gerar_modelos_modulares(semente=42)
        segundo = gerar_modelos_modulares(semente=42)
        self.assertEqual(primeiro, segundo)
        self.assertEqual(len(primeiro), len(MODELOS_BASE))

        fallback = gerar_modelos_modulares(
            semente=42,
            configuracoes=[],
            max_tentativas=0,
        )
        self.assertEqual(len(fallback), len(MODELOS_BASE))
        for modelo in fallback:
            for estilo in ("classico", "pizzaria", "reator"):
                self.assertTrue(validar_modelo(modelo, estilo))

    def test_combinacoes_de_bases_e_configuracoes_respeitam_posicoes(self):
        for indice_base, base in enumerate(MODELOS_BASE, start=1):
            for indice_config, configuracao in enumerate(
                CONFIGURACOES_MODELEX, start=1
            ):
                with self.subTest(
                    base=f"MODELO_BASE_{indice_base}",
                    configuracao=f"CONFIGURACAO_{indice_config}",
                ):
                    modelo = compor_modelo_modular(base, configuracao)
                    self.assertEqual(len(modelo), len(base))
                    self.assertEqual(
                        [len(linha) for linha in modelo],
                        [len(linha) for linha in base],
                    )

                    for nome, x, y in configuracao:
                        modulo = MODULOS_BANCADAS[nome]
                        for dy, linha_modulo in enumerate(modulo):
                            self.assertEqual(
                                modelo[y + dy][x:x + len(linha_modulo)],
                                linha_modulo,
                                f"{nome} não ficou na posição ({x}, {y})",
                            )

                    for estilo in ("classico", "pizzaria", "reator"):
                        self.assertTrue(
                            validar_modelo(modelo, estilo),
                            problemas_validacao_modelo(modelo, estilo),
                        )

    def test_composicao_rejeita_modulos_fora_dos_limites(self):
        largura = len(MODELO1[0])
        for nome, modulo in MODULOS_BANCADAS.items():
            with self.subTest(modulo=nome):
                x_fora = largura
                with self.assertRaisesRegex(ValueError, "ultrapassa os limites"):
                    compor_modelo_modular(MODELO1, [(nome, x_fora, 3)])

    def test_composicao_rejeita_mapa_base_com_grade_invalida(self):
        with self.assertRaisesRegex(ValueError, "13 linhas por 21 colunas"):
            compor_modelo_modular(MODELO1[:-1], [])

    def test_composicao_rejeita_sobreposicao_com_tile_existente(self):
        for nome in MODULOS_BANCADAS:
            with self.subTest(modulo=nome):
                with self.assertRaisesRegex(ValueError, "sobrepõe"):
                    compor_modelo_modular(MODELO1, [(nome, 0, 0)])


if __name__ == "__main__":
    unittest.main()
