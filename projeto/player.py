import pygame
from constantes import *

# Classe base
class Personagem:
    def __init__(self, x, y, cor, teclas):
        self.pos_x = x
        self.pos_y = y
        self.cor = cor
        self.teclas = teclas

    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()

        if teclas_pressionadas[self.teclas["esquerda"]]:
            self.pos_x -= VELOCIDADE

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

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.pos_x, self.pos_y, 50, 50))


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

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (self.pos_x, self.pos_y), 25)