import pygame
from constantes import *

class PedidoFacil:
    def __init__(self, tempo=TEMPOFACIL, pronto=False, pontuacao=PONTUACAOFACIL):

        self.tempo = tempo
        self.estado = pronto
        self.pontuacao = pontuacao

        self.ingredientes = ["Pão", "Queijo", "Carne"]

    def verificar_pedido(self, pedido):
        pass

class PedidoMedio:
    def __init__(self, tempo=TEMPOMEDIO, pronto=False, pontuacao=PONTUACAOMEDIO):
    
        self.tempo = tempo
        self.estado = pronto
        self.pontuacao = pontuacao

        self.ingredientes = ["Pão", "Tomate", "Queijo", "Carne"]
    
    def verificar_pedido(self, pedido):
        pass

class PedidoDificil:
    def __init__(self, tempo=TEMPODIFICIL, pronto=False, pontuacao=PONTUACAODIFICIL):

        self.tempo = tempo
        self.estado = pronto
        self.pontuacao = pontuacao

        self.ingredientes = ["Pão", "Alface", "Tomate", "Queijo", "Carne"]
     
    def verificar_pedido(self, pedido):
        pass