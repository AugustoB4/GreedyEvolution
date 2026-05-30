from constantes import *
from player import Romerio, Brito
import pygame

import pygame

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = int(LARGURA)
        self.altura = int(ALTURA)

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Greedy Evolution")

        self.player1 = Romerio(500, 500)
        self.player2 = Brito(501, 501)

        self.rodando = True
        self.clock = pygame.time.Clock()
        
    def menu(self):
        fonteTitulo = pygame.font.SysFont("Impact", 50)
        titulo = fonteTitulo.render("Greedy Evolution", True, AZUL)
        fonteTexto = pygame.font.SysFont("Arial", 30)
        texto = fonteTexto.render("Pressione Enter para iniciar o jogo", True, AZUL)

        menuRodando = True
        while menuRodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    menuRodando = False
                    self.rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        menuRodando = False

            self.tela.fill(PRETO)
            self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, self.altura // 3))
            self.tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, self.altura // 2))
            pygame.display.flip()

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
        pygame.display.flip()

    def iniciar(self):
        self.menu()
        while self.rodando == True:
            self.verificarEventos()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()
