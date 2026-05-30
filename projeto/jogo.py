from constantes import *
from player import Romerio, Brito
import pygame

import pygame

class Jogo:
    def __init__(self):
        pygame.init

        self.largura = int(LARGURA)
        self.altura = int(ALTURA)

        self.tela = pygame.display.set_mode((self.largura, self.altura))

        self.player1 = Romerio(500, 500)
        self.player2 = Brito(501, 501)

        self.rodando = True
        self.clock = pygame.time.Clock()

    def verificarEventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
        self.player1.mover()
        self.player2.mover()

    def desenhar(self):
        self.tela.fill((PRETO))
        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)
        pygame.display.update()

    def iniciar(self):
        while self.rodando == True:
            self.verificarEventos()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()
