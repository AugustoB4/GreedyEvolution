import pygame

from constantes import *
from menu import Menu
from player import Romerio, Brito
from itens import *
from mapa import Mapa

from sons import som_inicial
from caminhos import BACKGROUND_DIR
class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = int(LARGURA)
        self.altura = int(ALTURA)

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("Greedy Evolution")

        som_inicial.play()

        self.mapa1 = Mapa()
        self.mapa1.criar_colisoes()

        self.background = pygame.image.load(
            os.path.join(
                BACKGROUND_DIR,
                "StartMenuBG.png"
            )
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (self.largura, self.altura)
        )

        self.tomate = Tomate(500, 300)
        self.queijo = Queijo(450, 300)

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

            self.player1.verificar_habilidades(evento, self.queijo)
            self.player2.verificar_habilidades(evento, self.queijo)

            self.player1.verificar_cortagem(evento, self.tomate, self.mapa1.tabuas)
            self.player2.verificar_cortagem(evento, self.tomate, self.mapa1.tabuas)

            self.player1.verificar_cortagem(evento, self.queijo, self.mapa1.tabuas)
            self.player2.verificar_cortagem(evento, self.queijo, self.mapa1.tabuas)

        self.player1.mover(self.mapa1.colisoes)
        self.player2.mover(self.mapa1.colisoes)

        self.tomate.atualizar()
        self.queijo.atualizar()

    def desenhar(self):
        self.tela.fill(PRETO)
        self.mapa1.desenhar(self.tela)

        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)

        self.tomate.desenhar(self.tela)
        self.queijo.desenhar(
            self.tela
        )

        pygame.display.flip()

    def iniciar(self):
        menu = Menu(self.tela, self.largura, self.altura)
        if not menu.executar():
            self.rodando = False

        while self.rodando == True:
            self.verificarEventos()
            self.desenhar()
            self.clock.tick(60)
        pygame.quit()

