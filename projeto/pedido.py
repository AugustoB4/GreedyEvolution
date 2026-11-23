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

# A distribuição é indexada pela posição dentro da galáxia. Ao começar uma
# galáxia, a progressão retorna ao primeiro degrau sem mudar os critérios de
# estrelas, que continuam definidos em DefinicaoFase.dificuldade.
DIFICULDADES_PEDIDO = ("fácil", "médio", "difícil")
PROBABILIDADES_PEDIDOS_POR_FASE_LOCAL = {
    1: (70, 20, 10),
    2: (65, 25, 10),
    3: (60, 30, 10),
    4: (55, 33, 12),
    5: (50, 35, 15),
}


def pedidos_da_variante(variante):
    return PEDIDOS_POR_VARIANTE[variante]


def probabilidades_pedidos_da_fase(fase):
    """Retorna os pesos fácil/médio/difícil para uma fase da campanha."""
    fase_local = getattr(fase, "fase_na_galaxia", fase)
    if type(fase_local) is not int or fase_local not in PROBABILIDADES_PEDIDOS_POR_FASE_LOCAL:
        raise ValueError("Fase local sem distribuição de pedidos configurada")
    pesos = PROBABILIDADES_PEDIDOS_POR_FASE_LOCAL[fase_local]
    if any(peso < 0 for peso in pesos) or sum(pesos) != 100:
        raise ValueError("A distribuição de pedidos deve somar 100%")
    return pesos


def sortear_dificuldade_pedido(fase):
    pesos = probabilidades_pedidos_da_fase(fase)
    return random.choices(DIFICULDADES_PEDIDO, weights=pesos, k=1)[0]


def criar_pedido_ponderado(variante, fase):
    """Sorteia uma dificuldade da fase e cria uma receita dessa cozinha.

    A string de dificuldade preserva compatibilidade com chamadas antigas,
    que usavam os pesos legados para escolher uma classe diretamente.
    """
    classes_pedido = pedidos_da_variante(variante)
    if isinstance(fase, str):
        pesos = PROBABILIDADES_PEDIDOS_POR_DIFICULDADE[fase]
        classe_pedido = random.choices(classes_pedido, weights=pesos, k=1)[0]
        return classe_pedido()

    dificuldade = sortear_dificuldade_pedido(fase)
    classe_por_dificuldade = dict(zip(DIFICULDADES_PEDIDO, classes_pedido))
    classe_pedido = classe_por_dificuldade[dificuldade]
    return classe_pedido()


class ReceitaTV:
    def __init__(self, estilo="classico"):
        tiles_dir = os.path.join(TILES_DIR, estilo) if estilo != "classico" else TILES_DIR
        self.sprite = pygame.image.load(os.path.join(tiles_dir, "RecipeTV.png")).convert_alpha()
        
        self.fonte_titulo = pygame.font.Font(
            os.path.join(FONTS_DIR, "PressStart2P.ttf"), 8
        )
        self.texto_titulo = self.fonte_titulo.render("PEDIDO", True, BRANCO)
        caminho_fonte_ingredientes = os.path.join(
            FONTS_DIR, "PressStart2P.ttf"
        )
        self.fontes_ingredientes = tuple(
            pygame.font.Font(caminho_fonte_ingredientes, tamanho)
            for tamanho in (9, 7, 6)
        )
        self.fonte_ingredientes = self.fontes_ingredientes[0]
        self._cache_ingredientes = {}
        
        self.largura = TILE_SIZE * 3
        self.altura = TILE_SIZE * 3

        self.sprite = pygame.transform.scale(self.sprite,(self.largura, self.altura))
        tamanho_painel = (self.largura, self.altura)
        self.superficie_painel = pygame.Surface(
            tamanho_painel, pygame.SRCALPHA
        )
        self.superficie_conteudo = pygame.Surface(
            tamanho_painel, pygame.SRCALPHA
        )
        
    def desenhar(
        self,
        tela,
        pedido,
        jogador1: Personagem,
        jogador2: Personagem,
        escala=1.0,
        deslocamento=(0, 0),
        largura_base=None,
    ):
        escala = max(0.01, float(escala))
        deslocamento_x, deslocamento_y = deslocamento
        largura_base = largura_base or tela.get_width()
        tamanho = (
            max(1, round(self.largura * escala)),
            max(1, round(self.altura * escala)),
        )
        self.x = deslocamento_x + round(
            (largura_base - self.largura - 20) * escala
        )
        self.y = deslocamento_y
        tv_rect = pygame.Rect(self.x, self.y, *tamanho)

        retangulos_jogadores = []
        for jogador in (jogador1, jogador2):
            rect = jogador.rect
            retangulos_jogadores.append(
                pygame.Rect(
                    deslocamento_x + round(rect.x * escala),
                    deslocamento_y + round(rect.y * escala),
                    max(1, round(rect.width * escala)),
                    max(1, round(rect.height * escala)),
                )
            )
        alpha = (
            155
            if any(rect.colliderect(tv_rect) for rect in retangulos_jogadores)
            else 255
        )

        painel = self.superficie_painel
        painel.fill((0, 0, 0, 0))
        painel.blit(self.sprite, (0, 0))
        painel.set_alpha(alpha)
        painel_renderizado = (
            painel if tamanho == (self.largura, self.altura)
            else pygame.transform.scale(painel, tamanho)
        )
        tela.blit(painel_renderizado, tv_rect.topleft)

        conteudo = self.superficie_conteudo
        conteudo.fill((0, 0, 0, 0))
        conteudo.blit(self.texto_titulo, (15, 12))
        imagem_pedido = pygame.transform.scale(pedido.sprite, (40, 40))

        conteudo.blit(imagem_pedido, (12, 48))

        for indice, ingrediente in enumerate(pedido.ingredientes):
            chave = ingrediente.upper()
            texto = self._cache_ingredientes.get(chave)
            if texto is None:
                for fonte in self.fontes_ingredientes:
                    texto = fonte.render(chave, True, BRANCO)
                    if texto.get_width() <= self.largura - 66:
                        break
                self._cache_ingredientes[chave] = texto

            conteudo.blit(texto, (58, 48 + indice * 17))
            
        conteudo.set_alpha(alpha)
        conteudo_renderizado = (
            conteudo if tamanho == (self.largura, self.altura)
            else pygame.transform.scale(conteudo, tamanho)
        )
        tela.blit(conteudo_renderizado, tv_rect.topleft)
            
                
                
                
