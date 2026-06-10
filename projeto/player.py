import pygame
from constantes import *

# Classe base
class Personagem:
    def __init__(self, x, y, cor, teclas):

        self.pos_x = x
        self.pos_y = y

        self.teclas = teclas

        self.velocidade = VELOCIDADE

        self.sprite_sheet = pygame.image.load(sprite_pach).convert_alpha()

        self.largura_sprite = self.sprite_sheet.get_width() // 3
        self.altura_sprite = self.sprite_sheet.get_height() 
    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()

        if teclas_pressionadas[self.teclas["esquerda"]]:
            self.pos_x -= VELOCIDADE
            self.direcao = "lado"

        if teclas_pressionadas[self.teclas["direita"]]:
            self.pos_x += VELOCIDADE

        if teclas_pressionadas[self.teclas["cima"]]:
            self.pos_y -= VELOCIDADE

        if teclas_pressionadas[self.teclas["baixo"]]:
            self.pos_y += VELOCIDADE

    def cortar(self):
        pass

    def pegar(self):
        pass

    def largar(self):
        pass


# Romerio herda Personagem
class Romerio(Personagem):
    def __init__(self, x, y):
        teclas = {
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN
        }

        super().__init__(x, y, LARANJA, teclas)

        self.sprite = pygame.image.load("assets/sprites/player/Player1IdleSprite.png").convvert_alpha()


        self.sprite = pygame.transform.scale(self.sprite,(64, 64))

    def desenhar(self, tela):
     tela.blit(self.sprite, (self.pos_x, self.pos_y))

# Brito 
class Brito(Personagem):
    def __init__(self, x, y):
        teclas = {
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "cima": pygame.K_w,
            "baixo": pygame.K_s
        }

        super().__init__(x, y, AZUL, teclas)


        self.sprite = pygame.image.load(
            "assets/sprites/player/Player2IdleSprite.png"
        ).convert_alpha()

        self.sprite = pygame.transform.scale(
            self.sprite,
            (64, 64)
        )

    def desenhar(self, tela):
        tela.blit(self.sprite, (self.pos_x, self.pos_y))