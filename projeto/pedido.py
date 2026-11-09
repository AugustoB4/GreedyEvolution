import os
import pygame
from constantes import *
from caminhos import *
class Pedido:
    def __init__(self, tempo=TEMPOFACIL, pronto=False, pontuacao=PONTUACAOFACIL, nome=""):

        self.sprite = pygame.image.load(os.path.join(ORDERS_DIR, nome))

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
        self.sprite = pygame.image.load(os.path.join(TILES_DIR, "RecipeTV.png"))
        
    def verificar_pedido(self, pedido, montagem):
        if pedido.__class__ == montagem.__class__:
            self.pedidocorreto = True
            return self.pedidocorreto
                
                
                
