import pygame
from constantes import VERMELHO

class Tomate:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.raio = 16

        self.cor = (VERMELHO)

    def desenhar(self, tela):

        pygame.draw.circle(
            tela,
            self.cor,
            (self.x, self.y),
            self.raio
        )