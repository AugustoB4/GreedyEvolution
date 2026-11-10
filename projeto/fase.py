import pygame
import os
from caminhos import FONTS_DIR
from constantes import *

class Fase:
    def __init__(self, tempo=TEMPOINICIAL, pontuacao=0):
        self.tempo = tempo
        self.pontuacao = pontuacao
        
        self.fonte_pontuacao = pygame.font.Font(os.path.join(FONTS_DIR, "Orbitron.ttf"), 22)

        self.fonte_tempo = pygame.font.Font(os.path.join(FONTS_DIR, "PressStart2P.ttf"), 14)

    def aumentar_tempo_pontuacao(self, adicional_tempo, adicional_ponto):
        self.tempo += adicional_tempo
        self.pontuacao += adicional_ponto

    def diminuir_tempo_pontuacao(self, tempo_pedido, decrescimo_ponto):
        decrescimo_tempo = int(tempo_pedido / 2)

        self.tempo = max(0, self.tempo - decrescimo_tempo)
        self.pontuacao = max(0, self.pontuacao - decrescimo_ponto)
        
    def atualizar(self, dt):
        if self.tempo > 0:
            self.tempo = max(0, self.tempo - dt)
        
    def desenhar(self, tela):
        minutos = int(self.tempo) // 60
        segundos = int(self.tempo) % 60

        texto_pontuacao = self.fonte_pontuacao.render(f"PONTOS: {self.pontuacao}", True, (255, 255, 255))
        texto_tempo = self.fonte_tempo.render(f"{minutos:02}:{segundos:02}", True, (255, 255, 255))

        tela.blit(texto_pontuacao, (20, 20))
        posicao_tempo = (tela.get_width() - texto_tempo.get_width() - 20,tela.get_height() - texto_tempo.get_height() - 20)

        tela.blit(texto_tempo, posicao_tempo)

    
