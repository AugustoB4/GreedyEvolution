import math
import os

import pygame

from caminhos import FONTS_DIR
from constantes import BRANCO, TEMPOINICIAL


class Fase:
    OPACIDADE_HUD_PADRAO = 128
    DURACAO_DESTAQUE_HUD = 3.0
    DURACAO_FADE_HUD = 0.45
    DURACAO_ANIMACAO_VALORES = 0.4
    FATOR_DESTAQUE_VALORES = 1.14

    def __init__(
        self,
        tempo=TEMPOINICIAL,
        pontuacao=0,
        definicao=None,
        limite_tempo=None,
    ):
        self.tempo = tempo
        self.pontuacao = pontuacao
        self.definicao = definicao
        self.limite_tempo = limite_tempo
        self.entregas_corretas = 0
        self.encerrada = False
        self.resultado = None
        self.estrelas = 0

        caminho_fonte = os.path.join(FONTS_DIR, "PressStart2P.ttf")
        self.fonte_pontuacao = pygame.font.Font(caminho_fonte, 10)
        self.fonte_tempo = pygame.font.Font(caminho_fonte, 22)
        self.fonte_progresso = pygame.font.Font(caminho_fonte, 9)

        self._hud_destaque_restante = 0.0
        self._hud_fade_restante = 0.0
        self._animacao_pontuacao_restante = 0.0
        self._animacao_tempo_restante = 0.0
        self._hud_textos = {}
        self._hud_sombras = {}
        self.hud_rects = {}

    @property
    def opacidade_hud(self):
        if self._hud_destaque_restante > 0:
            return 255
        if self._hud_fade_restante > 0:
            progresso = 1 - self._hud_fade_restante / self.DURACAO_FADE_HUD
            progresso = max(0.0, min(1.0, progresso))
            suavizado = progresso * progresso * (3 - 2 * progresso)
            return round(
                self.OPACIDADE_HUD_PADRAO
                + (255 - self.OPACIDADE_HUD_PADRAO) * (1 - suavizado)
            )
        return self.OPACIDADE_HUD_PADRAO

    def destacar_entrega(self, correta=True):
        self._hud_destaque_restante = self.DURACAO_DESTAQUE_HUD
        self._hud_fade_restante = self.DURACAO_FADE_HUD
        if correta:
            self._animacao_pontuacao_restante = self.DURACAO_ANIMACAO_VALORES
            self._animacao_tempo_restante = self.DURACAO_ANIMACAO_VALORES

    def aumentar_tempo_pontuacao(self, adicional_tempo, adicional_ponto):
        if self.encerrada:
            return
        novo_tempo = self.tempo + adicional_tempo
        if self.limite_tempo is not None:
            novo_tempo = min(self.limite_tempo, novo_tempo)
        self.tempo = novo_tempo
        self.pontuacao += adicional_ponto

    def registrar_acerto(self, tempo_base, adicional_ponto):
        """Aplica bônus progressivo e conta apenas uma entrega válida."""
        if self.encerrada:
            return 0

        multiplicador_em_decimos = max(0, 10 - 3 * self.entregas_corretas)
        bonus = max(5, (int(tempo_base) * multiplicador_em_decimos) // 10)
        self.aumentar_tempo_pontuacao(bonus, adicional_ponto)
        self.entregas_corretas += 1
        return bonus

    def diminuir_tempo_pontuacao(self, tempo_pedido, decrescimo_ponto):
        if self.encerrada:
            return
        decrescimo_tempo = int(tempo_pedido / 2)
        self.tempo = max(0, self.tempo - decrescimo_tempo)
        self.pontuacao = max(0, self.pontuacao - decrescimo_ponto)

    def encerrar(self, resultado, estrelas=0):
        if self.encerrada:
            return False
        self.resultado = resultado
        self.estrelas = estrelas
        self.encerrada = True
        return True

    def atualizar(self, dt):
        dt = max(0.0, float(dt))
        if not self.encerrada and self.tempo > 0:
            self.tempo = max(0, self.tempo - dt)

        if self._hud_destaque_restante > 0:
            anterior = self._hud_destaque_restante
            self._hud_destaque_restante = max(0.0, anterior - dt)
            if anterior > 0 and self._hud_destaque_restante == 0:
                self._hud_fade_restante = self.DURACAO_FADE_HUD
        elif self._hud_fade_restante > 0:
            self._hud_fade_restante = max(0.0, self._hud_fade_restante - dt)

        self._animacao_pontuacao_restante = max(
            0.0, self._animacao_pontuacao_restante - dt
        )
        self._animacao_tempo_restante = max(
            0.0, self._animacao_tempo_restante - dt
        )

    def _texto_hud(self, chave, texto, fonte, cor=BRANCO):
        existente = self._hud_textos.get(chave)
        if existente is None or existente[0] != texto:
            existente = (texto, fonte.render(texto, True, cor))
            self._hud_textos[chave] = existente
        return existente[1]

    def _fator_animacao(self, restante):
        if restante <= 0:
            return 1.0
        progresso = 1 - restante / self.DURACAO_ANIMACAO_VALORES
        return 1 + (self.FATOR_DESTAQUE_VALORES - 1) * math.sin(
            math.pi * max(0.0, min(1.0, progresso))
        )

    def _desenhar_linha(
        self, tela, chave, texto, fonte, x, y, restante=0.0, anchor=None
    ):
        imagem = self._texto_hud(chave, texto, fonte)
        sombra_cache = self._hud_sombras.get(chave)
        if sombra_cache is None or sombra_cache[0] != texto:
            sombra_cache = (
                texto,
                fonte.render(texto, True, (10, 13, 28)),
            )
            self._hud_sombras[chave] = sombra_cache
        sombra = sombra_cache[1]
        fator = self._fator_animacao(restante)
        if fator != 1.0:
            tamanho = (
                max(1, round(imagem.get_width() * fator)),
                max(1, round(imagem.get_height() * fator)),
            )
            imagem = pygame.transform.scale(imagem, tamanho)
            sombra = pygame.transform.scale(sombra, tamanho)
        imagem.set_alpha(self.opacidade_hud)
        sombra.set_alpha(self.opacidade_hud)
        rect = imagem.get_rect(**(anchor or {"topleft": (x, y)}))
        tela.blit(sombra, rect.move(1, 1))
        tela.blit(imagem, rect)
        self.hud_rects[chave] = rect
        return rect

    def desenhar(self, tela):
        self.hud_rects = {}
        linhas = [
            (
                "pontuacao",
                f"PONTOS: {self.pontuacao}",
                self.fonte_pontuacao,
                self._animacao_pontuacao_restante,
            ),
            (
                "acertos",
                (
                    f"ACERTOS: {self.entregas_corretas}/4"
                    if self.definicao is not None
                    else f"ACERTOS: {self.entregas_corretas}"
                ),
                self.fonte_progresso,
                0.0,
            ),
        ]

        if self.definicao is not None:
            dificuldade = (
                self.definicao.dificuldade.upper()
                .replace("Á", "A")
                .replace("É", "E")
                .replace("Í", "I")
            )
            linhas.extend((
                (
                    "galaxia",
                    f"GALAXIA: {self.definicao.galaxia}",
                    self.fonte_progresso,
                    0.0,
                ),
                (
                    "fase",
                    f"FASE: {self.definicao.fase_na_galaxia}",
                    self.fonte_progresso,
                    0.0,
                ),
                (
                    "dificuldade",
                    f"DIF: {dificuldade}",
                    self.fonte_progresso,
                    0.0,
                ),
            ))

        margem_x = 18
        margem_y = 14
        altura_linha = 20
        for indice, (chave, texto, fonte, restante) in enumerate(linhas):
            self._desenhar_linha(
                tela,
                chave,
                texto,
                fonte,
                margem_x,
                margem_y + indice * altura_linha,
                restante,
            )

        minutos = int(self.tempo) // 60
        segundos = int(self.tempo) % 60
        self._desenhar_linha(
            tela,
            "tempo",
            f"{minutos:02}:{segundos:02}",
            self.fonte_tempo,
            0,
            tela.get_height() - 12,
            self._animacao_tempo_restante,
            anchor={
                "midbottom": (tela.get_width() // 2, tela.get_height() - 12)
            },
        )
