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
            center = (largura //2, 600)
        )
        
    def desenhar(self):
        self.tela.blit(self.backgroud ,(0,0))
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
                
                  if self.startRect.collidedict(evento.pos):
                     return True
                  if self.quitRect.collidedict(evento.pos):
                      return False
                  
        self.desenhar()         
    