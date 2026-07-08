from constantes import *
from menu import Menu
from player import Romerio, Brito
from itens import Tomate
from mapa import Mapa
import pygame

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = int(LARGURA)
        self.altura = int(ALTURA)

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Greedy Evolution")

        self.mapa = Mapa()

        self.background = pygame.image.load("projeto/assets/sprites/background/StartMenuBG.png").convert()
        self.background = pygame.transform.scale(self.background,(self.largura, self.altura))

        self.tomate = Tomate(500, 300)
        self.player1 = Romerio(750, 200)
        self.player2 = Brito(250, 200)

        self.rodando = True
        self.clock = pygame.time.Clock()
        
    def verificarEventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            self.player1.verificar_habilidades(evento)
            self.player2.verificar_habilidades(evento)
        self.player1.mover()
        self.player2.mover()
        if evento.type == pygame.KEYDOWN:

            if evento.key == self.player1.teclas["pegar"]:
                self.player1.pegar(self.tomate)

            if evento.key == self.player2.teclas["pegar"]:
                self.player2.pegar(self.tomate)

        if abs(self.player1.pos_x - self.tomate.x) < 40 and \
           abs(self.player1.pos_y - self.tomate.y) < 40:

            self.player1.pegar(self.tomate)

    

    def desenhar(self):
        self.tela.fill(PRETO)
        self.mapa.desenhar(self.tela)
        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)

        self.tomate.desenhar(self.tela)
        
        pygame.display.flip()

    def iniciar(self):
        menu = Menu(self.tela,self.largura,self.altura)
        if not menu.executar():
            self.rodando = False
        while self.rodando == True:
            self.verificarEventos()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()
