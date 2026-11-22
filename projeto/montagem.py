
import os
import pygame
from constantes import TILE_SIZE
from caminhos import ORDERS_DIR
from itens import Hamburguer, ProdutoFinal
import math


class Montagem:
    def __init__(self, x, y, pedido=None):
        self.x = x
        self.y = y
        
        self.animando = False
        self.tempo_animacao = 0
        self.duracao_animacao = 0.4

        self.ingredientes = []

        self.hamburguer = None
        self.hamburguer_pronto = False
        self.hamburguer_com_tomate = False
        self.hamburguer_com_alface = False
        self._pedido = None
        
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

        self.pedido = pedido

    @property
    def pedido(self):
        return self._pedido

    @pedido.setter
    def pedido(self, valor):
        self._pedido = valor
        if hasattr(self, "ingredientes"):
            self._verificar_hamburguer()

    @property
    def produto(self):
        return self.hamburguer

    @produto.setter
    def produto(self, valor):
        self.hamburguer = valor

    @property
    def produto_pronto(self):
        return self.hamburguer_pronto

    @produto_pronto.setter
    def produto_pronto(self, valor):
        self.hamburguer_pronto = valor
        
    def ponto_apoio(self, letra):
        x = self.rect.centerx
        y = self.rect.centery

        if letra in ("2", "3", "4", "D", "Q", "A", "C"):
            y -= 18

        return x, y

    def adicionar_ingrediente(self, ingrediente, letra):
        if isinstance(ingrediente, ProdutoFinal) or self.hamburguer is not None:
            return False

        if ingrediente in self.ingredientes:
            return False

        quantidade = len(self.ingredientes)
        
        if quantidade >= 5:
            return False
        
        centro_x, centro_y = self.ponto_apoio(letra)
              
        x = centro_x - ingrediente.rect.width // 2
        y = centro_y - ingrediente.rect.height // 2 - (quantidade * 8)

        ingrediente.dono = None
        ingrediente.em_montagem = True
        ingrediente.x = x
        ingrediente.y = y
        ingrediente.rect.topleft = (x, y)

        self.ingredientes.append(ingrediente)
        self._verificar_hamburguer()

        return True

    def colocar_hamburguer(self, hamburguer, letra):
        return self.colocar_produto(hamburguer, letra)

    def colocar_produto(self, produto, letra):
        if self.hamburguer is not None or self.ingredientes:
            return False

        if not isinstance(produto, ProdutoFinal):
            return False

        produto.dono = None
        produto.em_montagem = True
        centro_x, centro_y = self.ponto_apoio(letra)
        produto.x = centro_x - produto.rect.width // 2
        produto.y = centro_y - produto.rect.height // 2
        produto.rect.topleft = (produto.x, produto.y)
        self.hamburguer = produto
        self.hamburguer_pronto = False
        self.animando = False
        self.tempo_animacao = 0
        return True

    def _verificar_hamburguer(self):
        estava_pronto = self.hamburguer_pronto

        if self.pedido is None or self.hamburguer is not None:
            self.hamburguer_pronto = False
            self.hamburguer_com_tomate = False
            self.hamburguer_com_alface = False
            self.animando = False
            self.tempo_animacao = 0
            return

        nomes = {
            "Pão": "Bread",
            "Queijo": "Cheese",
            "Carne": "Meat",
            "Tomate": "Tomato",
            "Alface": "Lettuce"
        }

        ingredientes_esperados = getattr(
            self.pedido, "ingrediente_ids", None
        )
        if ingredientes_esperados is None:
            ingredientes_esperados = [
                nomes[nome] for nome in self.pedido.ingredientes
            ]

        ingredientes_colocados = [
            ingrediente.nome for ingrediente in self.ingredientes
        ]

        ordem_correta = (
            ingredientes_colocados == ingredientes_esperados
        )

        preparos = getattr(self.pedido, "preparos", {})

        def ingrediente_preparado(ingrediente):
            requisito = preparos.get(ingrediente.nome)
            if requisito is None:
                requisito = "assado" if ingrediente.nome == "Meat" else "cortado"

            if requisito == "assado":
                return ingrediente.assado and not ingrediente.queimado
            if requisito == "cozido":
                return ingrediente.cozido
            if requisito == "cortado":
                return ingrediente.cortado
            return False

        preparo_correto = all(
            ingrediente_preparado(ingrediente)
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

        if not self.hamburguer_pronto:
            self.animando = False
            self.tempo_animacao = 0
        elif not estava_pronto:
            self.animando = True
            self.tempo_animacao = 0
    
    def pegar_ingrediente(self):
        if self.hamburguer is not None:
            hamburguer = self.hamburguer
            self.hamburguer = None
            hamburguer.em_montagem = False
            return hamburguer

        if self.pedido is not None:
            # Revalidar aqui protege também contra mudanças de estado do ingrediente
            # feitas fora dos caminhos normais de adicionar ou retirar.
            self._verificar_hamburguer()

        if self.hamburguer_pronto:
            if hasattr(self.pedido, "criar_produto"):
                hamburguer = self.pedido.criar_produto(
                    self.rect.x, self.rect.y
                )
            else:
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
            if self.pedido is not None and hasattr(self.pedido, "sprite"):
                sprite = self.pedido.sprite
            else:
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
