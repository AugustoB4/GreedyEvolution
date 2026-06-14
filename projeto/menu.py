from constantes import *
import pygame

class Menu:
    escala = 2
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        
        self.background = pygame.image.load("projeto/assets/sprites/background/StartMenuBGSprite.png").convert()
        self.background = pygame.transform.scale(self.background,(largura, altura))

        self.titulo = pygame.image.load("projeto/assets/sprites/ui/GreedyEvolutionTitleSprite.png").convert_alpha()
        self.titulo = pygame.transform.scale(self.titulo,(700, 180)
)
        self.startButton = pygame.image.load("projeto/assets/sprites/ui/StartButtonSprite.png").convert_alpha()
        self.startButton = pygame.transform.scale(self.startButton,(300, 100))

        self.quitButton = pygame.image.load("projeto/assets/sprites/ui/QuitButtonSprite.png").convert_alpha()
        self.quitButton = pygame.transform.scale(self.quitButton,(300, 100))
        
        self.tituloRect = self.titulo.get_rect(
            center = (largura //self.escala, 180)
        )
        self.startRect = self.startButton.get_rect(
            center = (largura //self.escala, 350)
        )
        self.quitRect = self.quitButton.get_rect(
            center = (largura //self.escala, 450)
        )
        
    def desenhar(self):
        self.tela.blit(self.background ,(0,0))
        self.tela.blit(self.titulo, self.tituloRect)
        self.tela.blit(self.startButton, self.startRect)
        self.tela.blit(self.quitButton, self.quitRect)
        
        pygame.display.flip()
        
    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                  if self.startRect.collidepoint(evento.pos):
                     return True
                  if self.quitRect.collidepoint(evento.pos):
                      return False
            self.desenhar()         
    