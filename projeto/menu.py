import pygame

class Menu:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        
        self.backgroud = pygame.image.load("assets/StartMenuBGSprite.png").convert()
        
        self.titulo = pygame.image.load("assets/GreedyEvolutionTitleSprite.png").convert_alpha()
        
        self.startButton = pygame.image.load("assets/StartButtonSprite.png").convert_alpha()
        
        self.quitButton = pygame.image.load("assets/QuitButtonSprite.png").convert_alpha()
        
        self.tituloRect = self.titulo.get_rect(
            center = (largura //2, 180)
        )
        self.startRect = self.startButton.get_rect(
            center = (largura //2, 400)
        )
        self.quitRect = self.quitButton.get_rect(
            center = (largura //2, 520)
        )