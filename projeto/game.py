import pygame

from constantes import *
from player import Romerio, Brito


class Game:
    def __init__(self):

        pygame.init()

        self.largura = LARGURA
        self.altura = ALTURA

        self.tela = pygame.display.set_mode((self.largura, self.altura))

        pygame.display.set_caption("Gredy Evolution")

        self.clock = pygame.time.Clock()

        self.rodando = True

        self.player1 = Romerio(300, 300)
        self.player2 = Brito(500, 300)

    def verificar_eventos(self):
        for eventos in pygame.event.get():

            if eventos.type == pygame.QUIT:
                self.rodando = False
            
        self.player1.mover()
        self.player2.mover()

    def desenhar(self):
        self.tela.fill((0, 0, 0))

        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)

        pygame.display.flip()

    def iniciar(self):
        while self.rodando:

            self.verificar_eventos()

            self.desenhar()

            self.clock.tick(60)

        pygame.quit()