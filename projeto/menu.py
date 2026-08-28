
import os
import pygame

from constantes import *
from caminhos import BACKGROUND_DIR, UI_DIR


class Menu:

    escala = 2

    def __init__(self, tela, largura, altura):

        self.tela = tela
        self.largura = largura
        self.altura = altura

        self.background = pygame.image.load(os.path.join(BACKGROUND_DIR,"StartMenuBG.png" )).convert()
        self.background = pygame.transform.scale(self.background, (largura, altura))

        self.titulo = pygame.image.load(os.path.join(UI_DIR, "GameTittle.png")).convert_alpha()
        self.titulo = pygame.transform.scale(self.titulo,(700, 180))


        self.startButton = pygame.image.load(os.path.join(UI_DIR, "ButtonStart.png")).convert_alpha()
        self.startButton = pygame.transform.scale(self.startButton, (400, 100))

        self.largStart, self.altuStart = (self.startButton.get_size())

        self.areaCorteDireita = pygame.Rect(0, 0, self.largStart // 2, self.altuStart)

        self.areaCorteEsquerda = pygame.Rect(self.largStart // 2, 0, self.largStart // 2, self.altuStart)

        self.startCortadoDireita = (self.startButton.subsurface(self.areaCorteDireita))

        self.startCortadoEsquerda = (self.startButton.subsurface(self.areaCorteEsquerda))


        self.quitButton = pygame.image.load(os.path.join(UI_DIR, "ButtonQuit.png")).convert_alpha()
        self.quitButton = pygame.transform.scale(self.quitButton, (400, 100))

        self.largQuit, self.altuQuit = (self.quitButton.get_size())

        self.areaCorteDireita = pygame.Rect(0, 0, self.largQuit // 2, self.altuQuit)

        self.areaCorteEsquerda = pygame.Rect(self.largQuit // 2, 0, self.largQuit // 2, self.altuQuit)

        self.quitCortadoDireita = (self.quitButton.subsurface(self.areaCorteDireita))

        self.quitCortadoEsquerda = (self.quitButton.subsurface(self.areaCorteEsquerda))

        self.tituloRect = self.titulo.get_rect(center=(largura // self.escala, 150))
        self.startRect = self.startButton.get_rect(center=(largura // 1.7, 350))
        self.quitRect = self.quitButton.get_rect(center=(largura // 1.7, 450))

        self.colisaoQuit = (self.quitCortadoDireita.get_rect(center=(largura // 2, 450)))

        self.colisaoStart = (self.startCortadoDireita.get_rect(center=(largura // 2, 350)))

    def desenhar(self):
        posicaoMouse = pygame.mouse.get_pos()

        self.tela.blit(self.background,(0, 0))

        self.tela.blit(self.titulo,self.tituloRect)

        if self.colisaoStart.collidepoint(posicaoMouse):
            self.tela.blit(self.startCortadoEsquerda,self.startRect)

        else:
            self.tela.blit(self.startCortadoDireita,self.startRect)

        if self.colisaoQuit.collidepoint(posicaoMouse):
            self.tela.blit(self.quitCortadoEsquerda,self.quitRect)

        else:
            self.tela.blit(self.quitCortadoDireita,self.quitRect)

        pygame.display.flip()

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.startRect.collidepoint(evento.pos):
                        return True

                    if self.quitRect.collidepoint(evento.pos):
                        return False

            self.desenhar()

