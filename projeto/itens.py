import os
import pygame

from constantes import VERMELHO
from caminhos import INGREDIENTS_DIR, ANIMATION_DIR


class Ingrediente:

    def carregar_animacao(self, caminho, tamanho):
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, tamanho)

    def __init__(self, x, y, sprite_path, nome):
        self.x = x
        self.y = y
        self.nome = nome
        self.sprite_path = sprite_path

        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))
        self.rect = self.sprite.get_rect(topleft=(x, y))

        self.barra_sheet = pygame.image.load( os.path.join(ANIMATION_DIR, "CookingBar.png")).convert_alpha()
        self.barras_cozimento = []

        for i in range(6):
            sprite = self.barra_sheet.subsurface((0, 1 + i * 10, 32, 10))
            sprite = pygame.transform.scale(sprite, (64, 20))
            self.barras_cozimento.append(sprite)

        self.dono = None
        self.corte = True
        self.cru = True
        self.assado = False
        self.queimado = False
        self.cortado = False
        self.cont = 0

        self.sprite_forno = self.carregar_animacao(
            os.path.join(ANIMATION_DIR, "UseOven.png"),
            (32, 32)
        )

    def atualizar(self):
        if self.dono:
            self.x = self.dono.pos_x + 16
            self.y = self.dono.pos_y - 20

        self.rect.topleft = (self.x, self.y)

    def cortar_ingrediente(self):
        if self.corte and not self.cortado:
            caminho = os.path.join(
                INGREDIENTS_DIR,
                "Sliced" + self.nome + ".png"
            )

            if os.path.exists(caminho):
                self.sprite = pygame.image.load(caminho).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (32, 32))

            self.cortado = True

    def assar_ingrediente(self, fornos):
        if self.nome != "Meat" or self.queimado:
            return

        for forno in fornos:
            if self.rect.colliderect(forno.rect) and self.dono == None:
                self.cont += 1

                if self.cont >= 800 and not self.queimado:
                    caminho = os.path.join(
                        INGREDIENTS_DIR, "BurnedMeat.png"
                    )
                    self.sprite = pygame.image.load(caminho).convert_alpha()
                    self.sprite = pygame.transform.scale(self.sprite, (32, 32))
                    self.queimado = True
                    self.assado = False
                    self.cru = False

                elif self.cont >= 500 and not self.assado and not self.queimado:
                    caminho = os.path.join(
                        INGREDIENTS_DIR, "CookedMeat.png"
                    )
                    self.sprite = pygame.image.load(caminho).convert_alpha()
                    self.sprite = pygame.transform.scale(self.sprite, (32, 32))
                    self.assado = True
                    self.cru = False

                return

    def desenhar_barra_preparo(self, tela, forno):
        if self.nome != "Meat" or self.cont == 0:
            return

        if self.cont < 300:
            indice = 0

        elif self.cont < 500:
            indice = 1

        elif self.cont < 600:
            indice = 2

        elif self.cont < 700:
            indice = 3

        elif self.cont < 800:
            indice = 4

        else:
            indice = 5

        barra = self.barras_cozimento[indice]

        tela.blit(barra ,(forno.posX - 16, forno.posY - 25))



    def desenhar(self, tela):
        tela.blit(self.sprite, (self.x, self.y))


class Tomate(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Tomato.png"), "Tomato")


class Alface(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Lettuce.png"), "Lettuce")


class Queijo(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Cheese.png"), "Cheese")


class Pao(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Bread.png"), "Bread")


class Carne(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "RawMeat.png"), "Meat")