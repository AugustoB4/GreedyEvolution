import os
import pygame
import random

from constantes import *
from fase import Fase
from pedido import *
from menu import Menu
from player import Romerio, Brito, tomates, queijos, paos, carnes, alfaces
from itens import *
from mapa import Mapa
from pedido import ReceitaTV

from sons import som_inicial, som_face
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
        self.fase = Fase()
        self.televisao = ReceitaTV()
        self.montagens = self.mapa1.montagens
        self.pedido_atual = random.choice([PedidoFacil,PedidoMedio,PedidoDificil])()
        for montagem in self.montagens:
            montagem.pedido = self.pedido_atual
        
        self.armarios = self.mapa1.armarios
        self.armarios_queijo = self.mapa1.armarios_queijo
        self.armarios_tomate = self.mapa1.armarios_tomate
        self.armarios_alface = self.mapa1.armarios_alface
        self.geladeiras = self.mapa1.geladeiras
        self.lixeiras = self.mapa1.lixos
        self.entregas = self.mapa1.entregas

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
        self.tomates = tomates
        self.queijos = queijos
        self.paos = paos
        self.carnes = carnes
        self.alfaces = alfaces

        self.player1 = Romerio(750, 200)
        self.player2 = Brito(250, 200)

        self.rodando = True
        self.clock = pygame.time.Clock()
        
    def processar_entrega(self, hamburguer):
        tomate_esperado = "Tomate" in self.pedido_atual.ingredientes
        alface_esperada = "Alface" in self.pedido_atual.ingredientes

        pedido_correto = (hamburguer.com_tomate == tomate_esperado and hamburguer.com_alface == alface_esperada
        )

        if pedido_correto: 
            self.fase.aumentar_tempo_pontuacao(self.pedido_atual.tempo, self.pedido_atual.pontuacao)
        else:
            self.fase.diminuir_tempo_pontuacao(self.pedido_atual.tempo, self.pedido_atual.pontuacao)

        self.gerar_pedido()
        
    def gerar_pedido(self):
        self.pedido_atual = random.choice([
            PedidoFacil,
            PedidoMedio,
            PedidoDificil
        ])()

        for montagem in self.montagens:
            montagem.pedido = self.pedido_atual

    def verificarEventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            hamburguer1 = self.player1.verificar_habilidades(
            evento, self.armarios, self.armarios_queijo,
            self.armarios_tomate, self.armarios_alface,
            self.geladeiras, self.tomates, self.alfaces,
            self.queijos, self.paos, self.carnes,
            self.lixeiras, self.montagens, self.entregas)

            hamburguer2 = self.player2.verificar_habilidades(
                evento, self.armarios, self.armarios_queijo,
                self.armarios_tomate, self.armarios_alface,
                self.geladeiras, self.tomates, self.alfaces,
                self.queijos, self.paos, self.carnes,
                self.lixeiras, self.montagens, self.entregas
            )

            if hamburguer1 is not None:
                self.processar_entrega(hamburguer1)

            if hamburguer2 is not None:
                self.processar_entrega(hamburguer2)

            self.player1.verificar_cortagem(
                evento, self.mapa1.tabuas, self.tomates,
                self.alfaces, self.queijos, self.paos, self.carnes
            )

            self.player2.verificar_cortagem(
                evento, self.mapa1.tabuas, self.tomates,
                self.alfaces, self.queijos, self.paos, self.carnes
            )

        self.player1.mover(self.mapa1.colisoes)
        self.player2.mover(self.mapa1.colisoes)
        
        self.player1.verificar_indicador(self.lixeiras, self.armarios, self.armarios_queijo, self.armarios_tomate, self.armarios_alface, self.geladeiras, self.tomates, self.alfaces, self.queijos, self.paos, self.carnes)
        self.player2.verificar_indicador(self.lixeiras, self.armarios, self.armarios_queijo, self.armarios_tomate, self.armarios_alface, self.geladeiras, self.tomates, self.alfaces, self.queijos, self.paos, self.carnes)

        for tomate in self.tomates:
            tomate.atualizar()
        for queijo in self.queijos:
            queijo.atualizar()
        for alface in self.alfaces:
            alface.atualizar()
        for pao in self.paos:
            pao.atualizar()
        for carne in self.carnes:
            carne.atualizar()
            carne.assar_ingrediente(self.mapa1.fornos)
            
    def desenhar(self):
        self.tela.fill(PRETO)
        self.mapa1.desenhar(self.tela)
        
        
        self.mapa1.desenhar_preparo(self.tela, self.carnes)
        
        self.player1.desenhar_indicador(self.tela)
        self.player2.desenhar_indicador(self.tela)
        
        self.player1.desenhar(self.tela)
        self.player2.desenhar(self.tela)
        
        for tomate in self.tomates:
            tomate.desenhar(self.tela)
            
        for queijo in self.queijos:
            queijo.desenhar(self.tela)
            
        for alface in self.alfaces:
            alface.desenhar(self.tela)
            
        for pao in self.paos:
            pao.desenhar(self.tela)
            
        for carne in self.carnes:
            carne.desenhar(self.tela)

        for montagem in self.montagens:
            montagem.desenhar(self.tela)
        
        self.fase.desenhar(self.tela)
        self.televisao.desenhar(self.tela,self.pedido_atual)
        pygame.display.flip()

    def iniciar(self):
        menu = Menu(self.tela, self.largura, self.altura)
        if not menu.executar():
            self.rodando = False
        else:
            som_inicial.stop()
            som_face.play(-1)
           
        while self.rodando == True:
            dt = self.clock.tick(60) / 1000
            
            self.fase.atualizar(dt)
            
            for montagem in self.montagens:
                montagem.atualizar(dt)
        
            self.verificarEventos()
            self.desenhar()
        pygame.quit()