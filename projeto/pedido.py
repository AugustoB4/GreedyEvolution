import os
import pygame
from player import Personagem
from constantes import *
from caminhos import *
class Pedido:
    def __init__(self, tempo=TEMPOFACIL, pronto=False, pontuacao=PONTUACAOFACIL, nome=""):

        self.sprite = pygame.image.load(os.path.join(ORDERS_DIR, nome)).convert_alpha()

        self.tempo = tempo
        self.estado = pronto
        self.pontuacao = pontuacao

        self.ingredientes = []

class PedidoFacil(Pedido):
    def __init__(self, tempo=TEMPOFACIL, pronto=False, pontuacao=PONTUACAOFACIL, nome="1Hamburguer.png"):

        super().__init__(tempo, pronto, pontuacao, nome)
        self.ingredientes = ["Pão", "Queijo", "Carne"]


class PedidoMedio(Pedido):
    def __init__(self, tempo=TEMPOMEDIO, pronto=False, pontuacao=PONTUACAOMEDIO, nome="2Hamburguer.png"):

        super().__init__(tempo, pronto, pontuacao, nome)
        self.ingredientes = ["Pão", "Tomate", "Queijo", "Carne"]


class PedidoDificil(Pedido):
    def __init__(self, tempo=TEMPODIFICIL, pronto=False,
                 pontuacao=PONTUACAODIFICIL, nome="3Hamburguer.png"):

        super().__init__(tempo, pronto, pontuacao, nome)
        self.ingredientes = ["Pão", "Alface", "Tomate", "Queijo", "Carne"]


class ReceitaTV:
    def __init__(self):
        self.sprite = pygame.image.load(os.path.join(TILES_DIR, "RecipeTV.png")).convert_alpha()
        
        self.fonte_titulo = pygame.font.Font(os.path.join(FONTS_DIR, "Orbitron.ttf"), 20)
        self.fonte_ingredientes = pygame.font.Font(os.path.join(FONTS_DIR, "PressStart2P.ttf"), 9)
        
        self.largura = TILE_SIZE * 3
        self.altura = TILE_SIZE * 3

        self.sprite = pygame.transform.scale(self.sprite,(self.largura, self.altura))
        
    def desenhar(self, tela, pedido, jogador1: Personagem, jogador2: Personagem):
        self.x = tela.get_width() - self.largura - 20
        self.y = 0
        
        tv_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        
        painel = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        
        if jogador1.rect.colliderect(tv_rect) or jogador2.rect.colliderect(tv_rect):
            painel.set_alpha(155)
        else:
            painel.set_alpha(255)

        painel.blit(self.sprite, (0, 0))
        titulo = self.fonte_titulo.render("PEDIDO", True, BRANCO)

        painel.blit(titulo, (15, 12))
        imagem_pedido = pygame.transform.scale(pedido.sprite, (40, 40))

        painel.blit(imagem_pedido, (12, 48))

        for indice, ingrediente in enumerate(pedido.ingredientes):
            texto = self.fonte_ingredientes.render(ingrediente.upper(), True, BRANCO)

            painel.blit(texto, (58, 48 + indice * 17))
            
        tela.blit(painel, (self.x, self.y))
            
                
                
                
