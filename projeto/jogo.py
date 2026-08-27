from constantes import *
from menu import Menu
from player import Romerio, Brito, Personagem
from itens import Tomate
from mapa import Mapa
import pygame
from sons import som_inicial

class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = int(LARGURA)
        self.altura = int(ALTURA)

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Greedy Evolution")
        som_inicial.play()


        self.mapa = Mapa()
        self.mapa.criar_colisoes()

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
            self.player1.verificar_habilidades(evento, self.tomate)
            self.player2.verificar_habilidades(evento, self.tomate)
        self.player1.mover(self.mapa.colisoes)
        self.player2.mover(self.mapa.colisoes)
        self.tomate.atualizar()
    

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
