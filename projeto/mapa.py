import os
import pygame

from constantes import TILE_SIZE
from caminhos import TILES_DIR
from itens import Tomate


MAPA = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B22332122O22B221W",
    "W1FFFFFFFF1FFFFFFFF1W",
    "W1FF1111FF2FF1111FFNM",
    "W1FF2332FFTFF4332FF1W",
    "W1FFFFFFFFTFFFFFFFF1W",
    "W1FFFFFFFF2FFFFFFFF1W",
    "W1FF1111FFTFF1111FF1W",
    "W1FF2332FFTFF2332FF1W",
    "W1FFFFFFFF1FFFFFFFF1W",
    "W1FFFFFFFF1FFFFFFFF1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

"W = Wall / Parede"
"F = Floor / Chão"
"1 = 1Counter / Bancada de trás"
"2 = 2Counter / Primeira bancada de frente"
"3 = 3Counter / Segunda bancada de frente (com armários)"
"4 = CounterCheese / Segunda bancada de frente (com queijo)"
"S = Sink / Pia"
"O = Oven / Fogão"
"B = CuttingBoard / Tábua de corte"
"Y = RightWindow / Janela da direita"
"I = MiddleWindow / Janela do meio"
"T = TreadMill / Esteira de velocidade"
"N = DeliveryBelt / Esteira de Delivery"
"M = DeliveryWindow / Janela de Delivery"


class Tabua:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y

        self.rect = pygame.Rect(self.posX, self.posY, 32, 32)

class Armario:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.ingrediente = None

        self.rect = pygame.Rect(self.posX, self.posY, 32, 32)

class Mapa:
    def __init__(self):
        self.tabuas = []
        self.armarios = []
        self.colisoes = []
        self.tiles = {

            'F': pygame.image.load(os.path.join(TILES_DIR, "Floor.png")).convert_alpha(),
            'W': pygame.image.load(os.path.join(TILES_DIR, "Wall.png")).convert_alpha(),
            'M': pygame.image.load(os.path.join(TILES_DIR, "DeliveryWindow.png")).convert_alpha(),
            'N': pygame.image.load(os.path.join(TILES_DIR, "DeliveryBelt.png")).convert_alpha(),
            '1': pygame.image.load(os.path.join(TILES_DIR, "CounterUp.png")).convert_alpha(),
            '2': pygame.image.load(os.path.join(TILES_DIR, "CounterFront.png")).convert_alpha(),
            '3': pygame.image.load(os.path.join(TILES_DIR, "CounterFront2.png")).convert_alpha(),
            '4': pygame.image.load(os.path.join(TILES_DIR, "CounterCheese.png")).convert_alpha(),
            'S': pygame.image.load(os.path.join(TILES_DIR, "Sink.png")).convert_alpha(),
            'B': pygame.image.load(os.path.join(TILES_DIR, "CuttingBoard.png")).convert_alpha(),
            'Y': pygame.image.load(os.path.join(TILES_DIR, "RightWindow.png")).convert_alpha(),
            'I': pygame.image.load(os.path.join(TILES_DIR, "MiddleWindow.png")).convert_alpha(),
            'T': pygame.image.load(os.path.join(TILES_DIR, "TreadMill.png")).convert_alpha(),
            'O': pygame.image.load(os.path.join(TILES_DIR, "Oven.png")).convert_alpha(),
        }

    def desenhar(self, tela):
        for linha, caractere in enumerate(MAPA):
            for coluna, letra in enumerate(caractere):
                sprite = self.tiles[letra]
                if letra == "Y" and coluna == 19:
                    sprite = pygame.transform.flip(sprite, True, False) # Virar os tiles em qualquer direção

                tela.blit(sprite,(coluna * TILE_SIZE, linha * TILE_SIZE))

        # os tomates dentro do armário ficam ocultos até o clique de pegar

    def criar_colisoes(self):
        self.colisoes.clear()
        self.tabuas.clear()
        self.armarios.clear()

        for linha, texto in enumerate(MAPA):
            for coluna, letra in enumerate(texto):
                if letra in ("1", "2", "3", "4", "B", "C", "W", "S", "M", "O", "N"): # Adiciona colisão ao tile
                    self.colisoes.append(
                        pygame.Rect(
                            coluna * TILE_SIZE,
                            linha * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                    )

                if letra == "B":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    self.tabuas.append(Tabua(x, y))

                if letra == "3":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    armario = Armario(x, y)
                    armario.ingrediente = Tomate(x, y)
                    self.armarios.append(armario)

    def pode_largar(self, x, y):
        coluna = x // TILE_SIZE
        linha = y // TILE_SIZE

        if linha < 0 or linha >= len(MAPA):
            return False

        if coluna < 0 or coluna >= len(MAPA[linha]):
            return False

        return MAPA[linha][coluna] in ("F", "B","1", "2", "3")

