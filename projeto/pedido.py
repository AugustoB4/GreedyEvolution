import os
import random
import pygame
from player import Personagem
from constantes import *
from caminhos import *
from itens import Hamburguer, Pizza, Sushi


class Pedido:
    def __init__(
        self,
        tempo=TEMPOFACIL,
        pronto=False,
        pontuacao=PONTUACAOFACIL,
        nome="",
    ):

        self.sprite = pygame.image.load(os.path.join(ORDERS_DIR, nome)).convert_alpha()

        self.tempo = tempo
        self.estado = pronto
        self.pontuacao = pontuacao
        self.ingredientes = []
        self.ingrediente_ids = []
        self.preparos = {}
        self.receita_id = None
        self.id = None
        self.familia = None
        self.produto = None
        self.produto_classe = None
        self.dificuldade = None

    def configurar_receita(
        self,
        receita_id,
        familia,
        produto,
        produto_classe,
        dificuldade,
        ingredientes,
        ingrediente_ids,
        preparos,
    ):
        self.receita_id = receita_id
        self.id = receita_id
        self.familia = familia
        self.produto = produto
        self.produto_classe = produto_classe
        self.dificuldade = dificuldade
        self.ingredientes = list(ingredientes)
        self.ingrediente_ids = list(ingrediente_ids)
        self.preparos = dict(preparos)

    def criar_produto(self, x, y):
        if self.produto_classe is Hamburguer:
            com_tomate = "Tomato" in self.ingrediente_ids
            com_alface = "Lettuce" in self.ingrediente_ids
            return Hamburguer(
                x,
                y,
                com_tomate=com_tomate,
                com_alface=com_alface,
                receita_id=self.receita_id,
            )

        return self.produto_classe(x, y, receita_id=self.receita_id)

class PedidoFacil(Pedido):
    def __init__(self, tempo=TEMPOFACIL, pronto=False, pontuacao=PONTUACAOFACIL, nome="1Hamburguer.png"):

        super().__init__(tempo, pronto, pontuacao, nome)
        self.configurar_receita(
            "hamburguer_facil", "hamburguer", "Hambúrguer", Hamburguer,
            "fácil", ["Pão", "Queijo", "Carne"],
            ["Bread", "Cheese", "Meat"],
            {"Bread": "cortado", "Cheese": "cortado", "Meat": "assado"},
        )


class PedidoMedio(Pedido):
    def __init__(self, tempo=TEMPOMEDIO, pronto=False, pontuacao=PONTUACAOMEDIO, nome="2Hamburguer.png"):

        super().__init__(tempo, pronto, pontuacao, nome)
        self.configurar_receita(
            "hamburguer_medio", "hamburguer", "Hambúrguer", Hamburguer,
            "médio", ["Pão", "Tomate", "Queijo", "Carne"],
            ["Bread", "Tomato", "Cheese", "Meat"],
            {
                "Bread": "cortado", "Tomato": "cortado",
                "Cheese": "cortado", "Meat": "assado",
            },
        )


class PedidoDificil(Pedido):
    def __init__(self, tempo=TEMPODIFICIL, pronto=False,
                 pontuacao=PONTUACAODIFICIL, nome="3Hamburguer.png"):

        super().__init__(tempo, pronto, pontuacao, nome)
        self.configurar_receita(
            "hamburguer_dificil", "hamburguer", "Hambúrguer", Hamburguer,
            "difícil", ["Pão", "Alface", "Tomate", "Queijo", "Carne"],
            ["Bread", "Lettuce", "Tomato", "Cheese", "Meat"],
            {
                "Bread": "cortado", "Lettuce": "cortado",
                "Tomato": "cortado", "Cheese": "cortado",
                "Meat": "assado",
            },
        )


class PedidoPizzaFacil(Pedido):
    def __init__(self):
        super().__init__(TEMPOFACIL, False, PONTUACAOFACIL, "1Pizza.png")
        self.configurar_receita(
            "pizza_facil", "pizza", "Pizza", Pizza, "fácil",
            ["Massa"], ["Dough"], {"Dough": "cortado"},
        )


class PedidoPizzaMedio(Pedido):
    def __init__(self):
        super().__init__(TEMPOMEDIO, False, PONTUACAOMEDIO, "2Pizza.png")
        self.configurar_receita(
            "pizza_medio", "pizza", "Pizza", Pizza, "médio",
            ["Massa", "Queijo lunar"], ["Dough", "MoonCheese"],
            {"Dough": "cortado", "MoonCheese": "cortado"},
        )


class PedidoPizzaDificil(Pedido):
    def __init__(self):
        super().__init__(TEMPODIFICIL, False, PONTUACAODIFICIL, "3Pizza.png")
        self.configurar_receita(
            "pizza_dificil", "pizza", "Pizza", Pizza, "difícil",
            ["Massa", "Queijo lunar", "Tomate nebuloso"],
            ["Dough", "MoonCheese", "NebulaTomato"],
            {
                "Dough": "cortado", "MoonCheese": "cortado",
                "NebulaTomato": "cortado",
            },
        )


class PedidoSushiFacil(Pedido):
    def __init__(self):
        super().__init__(TEMPOFACIL, False, PONTUACAOFACIL, "1Sushi.png")
        self.configurar_receita(
            "sushi_facil", "sushi", "Sushi", Sushi, "fácil",
            ["Arroz estelar", "Alga cósmica"],
            ["StarRice", "CosmicSeaweed"],
            {"StarRice": "cozido", "CosmicSeaweed": "cortado"},
        )


class PedidoSushiMedio(Pedido):
    def __init__(self):
        super().__init__(TEMPOMEDIO, False, PONTUACAOMEDIO, "2Sushi.png")
        self.configurar_receita(
            "sushi_medio", "sushi", "Sushi", Sushi, "médio",
            ["Arroz estelar", "Alga cósmica", "Peixe nebuloso"],
            ["StarRice", "CosmicSeaweed", "NebulaFish"],
            {
                "StarRice": "cozido", "CosmicSeaweed": "cortado",
                "NebulaFish": "cortado",
            },
        )


class PedidoSushiDificil(Pedido):
    def __init__(self):
        super().__init__(TEMPODIFICIL, False, PONTUACAODIFICIL, "3Sushi.png")
        self.configurar_receita(
            "sushi_dificil", "sushi", "Sushi", Sushi, "difícil",
            [
                "Arroz estelar", "Alga cósmica",
                "Peixe nebuloso", "Peixe nebuloso",
            ],
            ["StarRice", "CosmicSeaweed", "NebulaFish", "NebulaFish"],
            {
                "StarRice": "cozido", "CosmicSeaweed": "cortado",
                "NebulaFish": "cortado",
            },
        )


PEDIDOS_POR_VARIANTE = {
    "hamburguer": (PedidoFacil, PedidoMedio, PedidoDificil),
    "pizza": (PedidoPizzaFacil, PedidoPizzaMedio, PedidoPizzaDificil),
    "sushi": (PedidoSushiFacil, PedidoSushiMedio, PedidoSushiDificil),
}

PROBABILIDADES_PEDIDOS_POR_DIFICULDADE = {
    "fácil": (70, 25, 5),
    "médio": (30, 50, 20),
    "difícil": (10, 35, 55),
}


def pedidos_da_variante(variante):
    return PEDIDOS_POR_VARIANTE[variante]


def criar_pedido_ponderado(variante, dificuldade):
    """Cria somente pedidos da cozinha informada, com pesos da dificuldade."""
    classes_pedido = pedidos_da_variante(variante)
    pesos = PROBABILIDADES_PEDIDOS_POR_DIFICULDADE[dificuldade]
    classe_pedido = random.choices(classes_pedido, weights=pesos, k=1)[0]
    return classe_pedido()


class ReceitaTV:
    def __init__(self, estilo="classico"):
        tiles_dir = os.path.join(TILES_DIR, estilo) if estilo != "classico" else TILES_DIR
        self.sprite = pygame.image.load(os.path.join(tiles_dir, "RecipeTV.png")).convert_alpha()
        
        self.fonte_titulo = pygame.font.Font(os.path.join(FONTS_DIR, "Orbitron.ttf"), 20)
        caminho_fonte_ingredientes = os.path.join(
            FONTS_DIR, "PressStart2P.ttf"
        )
        self.fontes_ingredientes = tuple(
            pygame.font.Font(caminho_fonte_ingredientes, tamanho)
            for tamanho in (9, 7, 6)
        )
        self.fonte_ingredientes = self.fontes_ingredientes[0]
        
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
            texto = None
            for fonte in self.fontes_ingredientes:
                texto = fonte.render(ingrediente.upper(), True, BRANCO)
                if texto.get_width() <= self.largura - 66:
                    break

            painel.blit(texto, (58, 48 + indice * 17))
            
        tela.blit(painel, (self.x, self.y))
            
                
                
                
