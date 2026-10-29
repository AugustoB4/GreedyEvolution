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
        if self.nome != "Meat" or self.assado or self.queimado:
            return

        for forno in fornos:
            if self.rect.colliderect(forno.rect):
                self.cont += 1

                if self.cont >= 40:
                    caminho = os.path.join(
                        INGREDIENTS_DIR, "BurnedMeat.png"
                    )
                    self.sprite = pygame.image.load(caminho).convert_alpha()
                    self.sprite = pygame.transform.scale(self.sprite, (32, 32))
                    self.queimado = True
                    self.assado = False

                elif self.cont >= 8:
                    caminho = os.path.join(
                        INGREDIENTS_DIR, "CookedMeat.png"
                    )
                    self.sprite = pygame.image.load(caminho).convert_alpha()
                    self.sprite = pygame.transform.scale(self.sprite, (32, 32))
                    self.assado = True
                    self.cru = False

                return

    def desenhar_animacao_forno(self, tela, forno):
        if self.nome == "Meat" and self.cont > 0 and not self.queimado:
            tela.blit(self.sprite_forno, (forno.posX, forno.posY))

    def desenhar_barra_preparo(self, tela, forno):
        if self.nome != "Meat" or self.cont == 0 or self.assado or self.queimado:
            return

        largura = 32
        altura = 5
        progresso = min(self.cont / 40, 1)

        pygame.draw.rect(
            tela, (60, 60, 60),
            (forno.posX, forno.posY - 8, largura, altura)
        )
        pygame.draw.rect(
            tela, (255, 180, 0),
            (forno.posX, forno.posY - 8, int(largura * progresso), altura)
        )

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