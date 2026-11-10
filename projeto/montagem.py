
import os
import pygame
from constantes import TILE_SIZE
from caminhos import ORDERS_DIR
from itens import Hamburguer
import math


class Montagem:
    def __init__(self, x, y, pedido=None):
        self.x = x
        self.y = y
        
        self.animando = False
        self.tempo_animacao = 0
        self.duracao_animacao = 0.4

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
        estava_pronto = self.hamburguer_pronto

        if self.pedido is None:
            self.hamburguer_pronto = False
            return

        nomes = {
            "Pão": "Bread",
            "Queijo": "Cheese",
            "Carne": "Meat",
            "Tomate": "Tomato",
            "Alface": "Lettuce"
        }

        ingredientes_esperados = [
            nomes[nome] for nome in self.pedido.ingredientes
        ]

        ingredientes_colocados = [
            ingrediente.nome for ingrediente in self.ingredientes
        ]

        ordem_correta = (
            ingredientes_colocados == ingredientes_esperados
        )

        preparo_correto = all(
            (
                ingrediente.assado and not ingrediente.queimado
                if ingrediente.nome == "Meat"
                else ingrediente.cortado
            )
            for ingrediente in self.ingredientes
        )

        self.hamburguer_com_tomate = any(
            ingrediente.nome == "Tomato"
            for ingrediente in self.ingredientes
        )

        self.hamburguer_com_alface = any(
            ingrediente.nome == "Lettuce"
            for ingrediente in self.ingredientes
        )

        self.hamburguer_pronto = (
            ordem_correta and preparo_correto
        )

        if not estava_pronto and self.hamburguer_pronto:
            self.animando = True
            self.tempo_animacao = 0
    
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
            self.animando = False
            self.tempo_animacao = 0
            return hamburguer

        if not self.ingredientes:
            return None

        ingrediente = self.ingredientes.pop()
        ingrediente.em_montagem = False
        self._verificar_hamburguer()
        return ingrediente
    
    def atualizar(self, dt):
        if self.animando:
            self.tempo_animacao += dt

            if self.tempo_animacao >= self.duracao_animacao:
                self.animando = False
                self.tempo_animacao = self.duracao_animacao

    def desenhar(self, tela):
        if self.hamburguer is not None:
            tela.blit(self.hamburguer.sprite, self.hamburguer.rect)
            return

        if self.hamburguer_pronto:
            sprite = self.sprites_hamburguer[
                (self.hamburguer_com_tomate, self.hamburguer_com_alface)
            ]

            escala = 1

            if self.animando:
                progresso = self.tempo_animacao / self.duracao_animacao
                escala = 1 + 0.3 * math.sin(progresso * math.pi)

            largura = int(TILE_SIZE * escala)
            altura = int(TILE_SIZE * escala)

            sprite_animado = pygame.transform.scale(
                sprite,
                (largura, altura)
            )

            rect = sprite_animado.get_rect(center=self.rect.center)
            tela.blit(sprite_animado, rect)
            return

        for ingrediente in self.ingredientes:
            tela.blit(ingrediente.sprite, ingrediente.rect)
