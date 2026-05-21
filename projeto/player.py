
import pygame
from constantes import *

#Romerio
class Romerio:
    def __init__(self,x,y):
        self.pos_x = x
        self.pos_y = y
        

        def mover(self):
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.pos_x -= VELOCIDADE
            if teclas[pygame.K_RIGHT]:
                self.pos_x += VELOCIDADE
            if teclas[pygame.K_UP]:
                self.pos_y -= VELOCIDADE
            if teclas[pygame.K_DOWN]:
                self.pos_y += VELOCIDADE


            def desenhar(self,tela, ROSA):
                pygame.draw.rect(tela, LARANJA, (200, 300), 50)

            def cortar(self):
                pass

            def pegar(self):
                pass

            def largar(self):
                pass

#Brito
class Brito:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y


    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_A]:
            self.pos_x -= VELOCIDADE
        if teclas[pygame.K_D]:
            self.pos_x += VELOCIDADE
        if teclas[pygame.K_W]:
            self.pos_y -= VELOCIDADE
        if teclas[pygame.K_S]:
            self.pos_y += VELOCIDADE

        def desenhar(self,tela,AZUL):
            pygame.draw.circle(tela, AZUL, (300, 200), 50)

        def cortar(self):
            pass

        def pegar(self):
            pass

        def largar(self):
            pass