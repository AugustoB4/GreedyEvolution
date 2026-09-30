import pygame
from constantes import *

class Fase:
    def __init__(self, tempo=TEMPOINICIAL, pontuacao=0):
        self.tempo = tempo
        self.pontuacao = pontuacao

    def aumentar_tempo_pontuacao(self, adicional_tempo, adicional_ponto):
        self.tempo += adicional_tempo
        self.pontuacao += adicional_ponto

    def diminuir_tempo_pontuacao(self, decrescimo_tempo, tempo_pedido, decrescimo_ponto):
        decrescimo_tempo = int(tempo_pedido/2)
        self.tempo -= decrescimo_tempo
        self.pontuacao -= decrescimo_ponto

