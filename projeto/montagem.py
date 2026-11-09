
import pygame
from constantes import TILE_SIZE


class Montagem:
    def __init__(self, x, y, pedido=None):
        self.x = x
        self.y = y
        self.pedido = pedido
        self.ingredientes = []

        self.rect = pygame.Rect(
            x, y, TILE_SIZE, TILE_SIZE
        )

    def adicionar_ingrediente(self, ingrediente):
        if ingrediente in self.ingredientes:
            return False

        quantidade = len(self.ingredientes)
        
        if quantidade >= 5:
            return False
              
        x = self.rect.centerx - ingrediente.rect.width // 2
        y = self.rect.centery - ingrediente.rect.height // 2 - (quantidade * 8)

        ingrediente.dono = None
        ingrediente.x = x
        ingrediente.y = y
        ingrediente.rect.topleft = (x, y)

        self.ingredientes.append(ingrediente)

        return True
    
    def pegar_ingrediente(self):
        if not self.ingredientes:
            return None

        return self.ingredientes.pop()

    def desenhar(self, tela):
        for ingrediente in self.ingredientes:
            tela.blit(ingrediente.sprite, ingrediente.rect)
