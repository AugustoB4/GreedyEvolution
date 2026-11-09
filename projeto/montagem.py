
import os
import pygame
from constantes import TILE_SIZE
from caminhos import ORDERS_DIR
from itens import Hamburguer


class Montagem:
    def __init__(self, x, y, pedido=None):
        self.x = x
        self.y = y
        self.pedido = pedido
        self.ingredientes = []
        self.hamburguer = None
        self.hamburguer_pronto = False
        self.hamburguer_com_tomate = False
        self.hamburguer_com_alface = False
        self.sprites_hamburguer = {}
        for receita, nome_sprite in (
            ((False, False), "1Hamburguer.png"),
            ((True, False), "2Hamburguer.png"),
            ((True, True), "3Hamburguer.png"),
        ):
            sprite = pygame.image.load(
                os.path.join(ORDERS_DIR, nome_sprite)
            ).convert_alpha()
            self.sprites_hamburguer[receita] = pygame.transform.scale(
                sprite, (TILE_SIZE, TILE_SIZE)
            )

        self.rect = pygame.Rect(
            x, y, TILE_SIZE, TILE_SIZE
        )

    def adicionar_ingrediente(self, ingrediente):
        if ingrediente.nome == "Hamburguer" or self.hamburguer is not None:
            return False

        if ingrediente in self.ingredientes:
            return False

        quantidade = len(self.ingredientes)
        
        if quantidade >= 5:
            return False
              
        x = self.rect.centerx - ingrediente.rect.width // 2
        y = self.rect.centery - ingrediente.rect.height // 2 - (quantidade * 8)

        ingrediente.dono = None
        ingrediente.em_montagem = True
        ingrediente.x = x
        ingrediente.y = y
        ingrediente.rect.topleft = (x, y)

        self.ingredientes.append(ingrediente)
        self._verificar_hamburguer()

        return True

    def colocar_hamburguer(self, hamburguer):
        if self.hamburguer is not None or self.ingredientes:
            return False

        hamburguer.dono = None
        hamburguer.em_montagem = True
        hamburguer.x = self.rect.centerx - hamburguer.rect.width // 2
        hamburguer.y = self.rect.centery - hamburguer.rect.height // 2
        hamburguer.rect.topleft = (hamburguer.x, hamburguer.y)
        self.hamburguer = hamburguer
        return True

    def _verificar_hamburguer(self):
        pao_cortado = any(
            ingrediente.nome == "Bread" and ingrediente.cortado
            for ingrediente in self.ingredientes
        )
        carne_assada = any(
            ingrediente.nome == "Meat"
            and ingrediente.assado
            and not ingrediente.queimado
            for ingrediente in self.ingredientes
        )
        queijo_cortado = any(
            ingrediente.nome == "Cheese" and ingrediente.cortado
            for ingrediente in self.ingredientes
        )
        tomates = [
            ingrediente
            for ingrediente in self.ingredientes
            if ingrediente.nome == "Tomato"
        ]
        tomate_cortado = bool(tomates) and all(
            ingrediente.cortado for ingrediente in tomates
        )
        alfaces = [
            ingrediente
            for ingrediente in self.ingredientes
            if ingrediente.nome == "Lettuce"
        ]
        alface_cortado = bool(alfaces) and all(
            ingrediente.cortado for ingrediente in alfaces
        )
        self.hamburguer_com_tomate = tomate_cortado
        self.hamburguer_com_alface = alface_cortado
        self.hamburguer_pronto = (
            pao_cortado
            and carne_assada
            and queijo_cortado
            and tomate_cortado
            and alface_cortado
        )
    
    def pegar_ingrediente(self):
        if self.hamburguer is not None:
            hamburguer = self.hamburguer
            self.hamburguer = None
            hamburguer.em_montagem = False
            return hamburguer

        if self.hamburguer_pronto:
            hamburguer = Hamburguer(
                self.rect.x,
                self.rect.y,
                self.hamburguer_com_tomate,
                self.hamburguer_com_alface,
            )
            self.ingredientes.clear()
            self.hamburguer_pronto = False
            self.hamburguer_com_tomate = False
            self.hamburguer_com_alface = False
            return hamburguer

        if not self.ingredientes:
            return None

        ingrediente = self.ingredientes.pop()
        ingrediente.em_montagem = False
        self._verificar_hamburguer()
        return ingrediente

    def desenhar(self, tela):
        if self.hamburguer is not None:
            tela.blit(self.hamburguer.sprite, self.hamburguer.rect)
            return

        if self.hamburguer_pronto:
            tela.blit(
                self.sprites_hamburguer[
                    (self.hamburguer_com_tomate, self.hamburguer_com_alface)
                ],
                self.rect,
            )
            return

        for ingrediente in self.ingredientes:
            tela.blit(ingrediente.sprite, ingrediente.rect)
