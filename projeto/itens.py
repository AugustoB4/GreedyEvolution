import os
import pygame

from constantes import VERMELHO
from caminhos import INGREDIENTS_DIR
class Ingrediente:
    def __init__(self, x, y, sprite_path, nome):

        self.x = x
        self.y = y
        self.nome = nome
        self.sprite_path = sprite_path
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.dono = None
        self.corte = True
        self.cortado = False

    def atualizar(self):
        if self.dono:
            self.x = self.dono.pos_x + 16
            self.y = self.dono.pos_y - 20

        self.rect.topleft = (self.x, self.y)

    def cortar_ingrediente(self):
        if self.corte and not self.cortado:
            caminho = os.path.join(INGREDIENTS_DIR, "Sliced" + self.nome + ".png")

            self.sprite = pygame.image.load(caminho).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
            self.cortado = True

    def desenhar(self, tela):
        tela.blit(self.sprite, (self.x, self.y))
class Tomate(Ingrediente):
    def __init__(self, x, y):
        super().__init__( x, y, os.path.join(INGREDIENTS_DIR, "Tomato.png"), "Tomato")


class Queijo(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Cheese.png"), "Cheese")
class Pao(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Bread.png"), "Bread")

