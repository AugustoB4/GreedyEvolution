import pygame
from constantes import *

# Classe base
class Personagem:
    def __init__(self, x, y, sprite_path, teclas):

        self.pos_x = x
        self.pos_y = y
        self.teclas = teclas
        self.velocidade = VELOCIDADE

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()

        self.largura_sprite = self.sprite_sheet.get_width() // 3
        self.altura_sprite = self.sprite_sheet.get_height() 

        self.direcao = "frente"
        self.virado_esquerda = False

        self.frames = {
            "frente": 0,
            "lado": 1,
            "costas": 2
        }

    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()

        if teclas_pressionadas[self.teclas["esquerda"]]:
            self.pos_x -= VELOCIDADE
            self.direcao = "lado"

        if teclas_pressionadas[self.teclas["direita"]]:
            self.pos_x += VELOCIDADE
            self.direcao = "lado"

        if teclas_pressionadas[self.teclas["cima"]]:
            self.pos_y -= VELOCIDADE
            self.direcao = "costas"

        if teclas_pressionadas[self.teclas["baixo"]]:
            self.pos_y += VELOCIDADE
            self.direcao = "frente"
    def desenhar(self, tela):
        indice = self.frames[self.direcao]

        area = pygame.Rect(
            indice * self.largura_sprite,
            0,
            self.largura_sprite,
            self. altura_sprite
        )

        sprite = self.sprite_sheet.subsurface(area)

        if self.virado_esquerda:
            sprite = pygame.transform.flip(sprite,True, False)
        tela.blit(
            sprite,
            (self.pos_x, self.pos_y)
        )

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

        super().__init__(x, y, "assets/sprites/player/Player1IdleSprite.png", teclas)


# Brito 
class Brito(Personagem):
    def __init__(self, x, y):
        teclas = {
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "cima": pygame.K_w,
            "baixo": pygame.K_s
        }

        super().__init__(x, y, "assets/sprites/player/Player2IdleSprite.png", teclas)



