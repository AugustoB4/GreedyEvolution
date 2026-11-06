from caminhos import PINS_DIR
import pygame
import os

class Indicador:
    def __init__(self, player, nome):
        self.player = player
        self.nome = nome 
        
        self.sprite = pygame.image.load(os.path.join(PINS_DIR, self.nome)).convert_alpha()
        
        
    def desenhar(self, tela):
        self.posicaox = self.player.rect.centerx + 15
        self.posicaoy = self.player.rect.top - 75
        tela.blit(self.sprite, (self.posicaox, self.posicaoy))
        
class IndPegar(Indicador):
    def __init__(self, player):
        super().__init__(player, "GrabPin.png")
        
class IndSoltar(Indicador):
    def __init__(self, player):
        super().__init__(player, "ArrowPin.png")
        
class IndPegarPao(Indicador):
    def __init__(self, player):
        super().__init__(player, "BreadPin.png")
        
        
class IndPegarQueijo(Indicador):
    def __init__(self, player):
        super().__init__(player, "CheesePin.png")
        
        
class IndPegarTomate(Indicador):
    def __init__(self, player):
        super().__init__(player, "TomatoPin.png")
        
        
class IndPegarAlface(Indicador):
    def __init__(self, player):
        super().__init__(player, "LettucePin.png")
        
        
class IndPegarCarne(Indicador):
    def __init__(self, player):
        super().__init__(player, "MeatPin.png")
        
        
class IndJogarLixo(Indicador):
    def __init__(self, player):
        super().__init__(player, "TrashPin.png")
        
    