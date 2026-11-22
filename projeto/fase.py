import pygame
import os
from caminhos import FONTS_DIR
from constantes import *

class Fase:
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
        
        self.fonte_pontuacao = pygame.font.Font(os.path.join(FONTS_DIR, "Orbitron.ttf"), 22)

        self.fonte_tempo = pygame.font.Font(os.path.join(FONTS_DIR, "PressStart2P.ttf"), 14)

        self.fonte_progresso = pygame.font.Font(
            os.path.join(FONTS_DIR, "PressStart2P.ttf"), 9
        )

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
        if not self.encerrada and self.tempo > 0:
            self.tempo = max(0, self.tempo - dt)
        
    def desenhar(self, tela):
        minutos = int(self.tempo) // 60
        segundos = int(self.tempo) % 60

        texto_pontuacao = self.fonte_pontuacao.render(f"PONTOS: {self.pontuacao}", True, (255, 255, 255))
        texto_tempo = self.fonte_tempo.render(f"{minutos:02}:{segundos:02}", True, (255, 255, 255))

        tela.blit(texto_pontuacao, (20, 20))
        if self.definicao is not None:
            progresso = self.fonte_progresso.render(
                (
                    f"GALAXIA {self.definicao.galaxia}  "
                    f"FASE {self.definicao.fase_na_galaxia}  "
                    f"{self.definicao.dificuldade.upper()}  "
                    f"ACERTOS {self.entregas_corretas}/4"
                ),
                True,
                (255, 255, 255),
            )
            tela.blit(progresso, (20, 54))
        posicao_tempo = (tela.get_width() - texto_tempo.get_width() - 20,tela.get_height() - texto_tempo.get_height() - 20)

        tela.blit(texto_tempo, posicao_tempo)

    
