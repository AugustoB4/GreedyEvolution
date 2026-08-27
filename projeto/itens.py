import pygame
from constantes import VERMELHO

class Ingrediente:
    def __init__(self, x, y, sprite_path):

        self.x = x
        self.y = y

        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))

        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))

        self.dono = None

    def atualizar(self):
        if self.dono:
            self.x = self.dono.pos_x + 16
            self.y = self.dono.pos_y - 20
        self.rect.topleft = (self.x, self.y)

    def desenhar(self, tela):
        tela.blit(self.sprite, (self.x, self.y))

class Tomate(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x,y,"projeto/assets/sprites/ingredients/Tomato.png")
        self.corte = True
        self.cortado = False

class Queijo(Ingrediente):
    def __init__(self, x, y):
        super().__init__( x, y,"projeto/assets/sprites/ingredients/Cheese.png")
        self.corte = True
        self.cortado = False

class Pao(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, "projeto/assets/sprites/ingredients/Bread.png")
        self.corte = True
        self.cortado = False