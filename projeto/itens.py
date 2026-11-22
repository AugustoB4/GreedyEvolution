import os
import pygame

from constantes import VERMELHO
from caminhos import INGREDIENTS_DIR, ANIMATION_DIR, ORDERS_DIR
from sons import som_forno


class Ingrediente:

    def carregar_animacao(self, caminho, tamanho):
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, tamanho)

    def __init__(self, x, y, sprite_path, nome):
        self.x = x
        self.y = y
        self.nome = nome
        self.sprite_path = sprite_path
        self.estava_no_forno= False

        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))
        self.rect = self.sprite.get_rect(topleft=(x, y))

        self.barra_sheet = pygame.image.load( os.path.join(ANIMATION_DIR, "CookingBar.png")).convert_alpha()
        self.barras_cozimento = []

        for i in range(6):
            sprite = self.barra_sheet.subsurface((0, 1 + i * 10, 32, 10))
            sprite = pygame.transform.scale(sprite, (64, 20))
            self.barras_cozimento.append(sprite)

        self.dono = None
        self.em_montagem = False
        self.corte = True
        self.cru = True
        self.assado = False
        self.cozido = False
        self.queimado = False
        self.cortado = False
        self.cont = 0
        self.metodo_preparo = "cortar"

        self.sprite_forno = self.carregar_animacao(
            os.path.join(ANIMATION_DIR, "UseOven.png"),
            (32, 32)
        )

    def atualizar(self):
        if self.dono:
            self.x = self.dono.pos_x + 16
            self.y = self.dono.pos_y - 20

        self.rect.topleft = (self.x, self.y)

    def cortar_ingrediente(self):
        if self.corte and not self.cortado:
            caminho = os.path.join(
                INGREDIENTS_DIR,
                "Sliced" + self.nome + ".png"
            )

            if os.path.exists(caminho):
                self.sprite = pygame.image.load(caminho).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (32, 32))

            self.cortado = True

    def assar_ingrediente(self, fornos, dt=1 / 60):
        if self.nome != "Meat" or self.queimado:
            return

        esta_no_forno = (
            self.dono is None
            and any(self.rect.colliderect(forno.rect) for forno in fornos)
        )

        if not esta_no_forno:
            self.estava_no_forno = False
            return

        if not self.estava_no_forno:
            som_forno.play()
            self.estava_no_forno = True

        self.cont += max(0.0, float(dt)) * 60

        if self.cont >= 800:
            caminho = os.path.join(INGREDIENTS_DIR, "BurnedMeat.png")
            self.sprite = pygame.image.load(caminho).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
            self.queimado = True
            self.assado = False
            self.cru = False

        elif self.cont >= 500 and not self.assado:
            caminho = os.path.join(INGREDIENTS_DIR, "CookedMeat.png")
            self.sprite = pygame.image.load(caminho).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
            self.assado = True
            self.cru = False

    def cozinhar_ingrediente(self, fornos, dt=1 / 60):
        if self.nome != "StarRice" or self.cozido:
            return

        esta_no_forno = (
            self.dono is None
            and any(self.rect.colliderect(forno.rect) for forno in fornos)
        )

        if not esta_no_forno:
            self.estava_no_forno = False
            return

        if not self.estava_no_forno:
            som_forno.play()
            self.estava_no_forno = True

        self.cont += max(0.0, float(dt)) * 60
        if self.cont >= 500:
            caminho = os.path.join(INGREDIENTS_DIR, "CookedStarRice.png")
            self.sprite = pygame.image.load(caminho).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
            self.cozido = True
            self.cru = False

    def preparar_ingrediente(self, fornos, dt=1 / 60):
        if self.metodo_preparo == "assar":
            self.assar_ingrediente(fornos, dt)
        elif self.metodo_preparo == "cozinhar":
            self.cozinhar_ingrediente(fornos, dt)

    def desenhar_barra_preparo(self, tela, forno):
        if self.metodo_preparo not in ("assar", "cozinhar") or self.cont == 0:
            return
        if self.metodo_preparo == "cozinhar" and self.cozido:
            return

        if self.cont < 300:
            indice = 0

        elif self.cont < 500:
            indice = 1

        elif self.cont < 600:
            indice = 2

        elif self.cont < 700:
            indice = 3

        elif self.cont < 800:
            indice = 4

        else:
            indice = 5

        barra = self.barras_cozimento[indice]

        tela.blit(barra ,(forno.posX - 16, forno.posY - 25))



    def desenhar(self, tela):
        if self.em_montagem:
            return

        tela.blit(self.sprite, (self.x, self.y))


class Tomate(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Tomato.png"), "Tomato")


class Alface(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Lettuce.png"), "Lettuce")


class Queijo(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Cheese.png"), "Cheese")


class Pao(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Bread.png"), "Bread")


class Carne(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "RawMeat.png"), "Meat")
        self.metodo_preparo = "assar"


class Massa(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "Dough.png"), "Dough")


class QueijoLunar(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "MoonCheese.png"), "MoonCheese")


class TomateNebuloso(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "NebulaTomato.png"), "NebulaTomato")


class ArrozEstelar(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "StarRice.png"), "StarRice")
        self.corte = False
        self.metodo_preparo = "cozinhar"


class AlgaCosmica(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "CosmicSeaweed.png"), "CosmicSeaweed")


class PeixeNebuloso(Ingrediente):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(INGREDIENTS_DIR, "NebulaFish.png"), "NebulaFish")


class ProdutoFinal(Ingrediente):
    def __init__(self, x, y, nome, familia, receita_id, sprite):
        super().__init__(x, y, os.path.join(ORDERS_DIR, sprite), nome)
        self.corte = False
        self.metodo_preparo = None
        self.familia = familia
        self.receita_id = receita_id
        self.tipo_objeto = "produto"


class Hamburguer(ProdutoFinal):
    def __init__(
        self, x, y, com_tomate=False, com_alface=False, receita_id=None
    ):
        if com_alface:
            sprite = "3Hamburguer.png"
        elif com_tomate:
            sprite = "2Hamburguer.png"
        else:
            sprite = "1Hamburguer.png"
        if receita_id is None:
            receita_id = {
                (False, False): "hamburguer_facil",
                (True, False): "hamburguer_medio",
                (True, True): "hamburguer_dificil",
            }.get((com_tomate, com_alface), "hamburguer_personalizado")
        super().__init__(x, y, "Hamburguer", "hamburguer", receita_id, sprite)
        self.com_tomate = com_tomate
        self.com_alface = com_alface


class Pizza(ProdutoFinal):
    def __init__(self, x, y, receita_id="pizza_facil"):
        sprite = {
            "pizza_facil": "1Pizza.png",
            "pizza_medio": "2Pizza.png",
            "pizza_dificil": "3Pizza.png",
        }.get(receita_id, "1Pizza.png")
        super().__init__(x, y, "Pizza", "pizza", receita_id, sprite)


class Sushi(ProdutoFinal):
    def __init__(self, x, y, receita_id="sushi_facil"):
        sprite = {
            "sushi_facil": "1Sushi.png",
            "sushi_medio": "2Sushi.png",
            "sushi_dificil": "3Sushi.png",
        }.get(receita_id, "1Sushi.png")
        super().__init__(x, y, "Sushi", "sushi", receita_id, sprite)
