import pygame
from constantes import TILE_SIZE

MAPA = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B22332122222B222W",
    "W1FFFFFFFF1FFFFFFFFFW",
    "W1FF1111FF2FFFFFFFFFW",
    "W1FF2332FFTFFFFFFFFFW",
    "W1FFFFFFFFTFFFFFFFFFW",
    "W1FFFFFFFF2FFFFFFFFFW",
    "W1FF1111FFTFFFFFFFFFF",
    "W1FF2332FFTFFFFFFFFFF",
    "W1FFFFFFFF1FFFFFFFFFW",
    "W1FFFFFFFF1FFFFFFFFFW",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

class Tabua:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y

        self.rect = pygame.Rect(self.posX, self.posY, 32, 32)


class Mapa:
    def __init__(self):
        self.tiles = {
            'F': pygame.image.load("projeto/assets/sprites/tiles/Floor.png").convert_alpha(),
            'W': pygame.image.load("projeto/assets/sprites/tiles/Wall.png").convert_alpha(),
            '1': pygame.image.load("projeto/assets/sprites/tiles/CounterUp.png").convert_alpha(),
            '2': pygame.image.load("projeto/assets/sprites/tiles/CounterFront.png").convert_alpha(),
            '3': pygame.image.load("projeto/assets/sprites/tiles/CounterFront2.png").convert_alpha(),
            'S': pygame.image.load("projeto/assets/sprites/tiles/Sink.png").convert_alpha(),
            'B': pygame.image.load("projeto/assets/sprites/tiles/CuttingBoard.png").convert_alpha(),
            'Y': pygame.image.load("projeto/assets/sprites/tiles/RightWindow.png").convert_alpha(),
            'I': pygame.image.load("projeto/assets/sprites/tiles/MiddleWindow.png").convert_alpha(),
            'T': pygame.image.load("projeto/assets/sprites/tiles/TreadMill.png").convert_alpha(),
        }

    def desenhar(self, tela):
        for linha, caractere in enumerate(MAPA):
            for coluna, letra in enumerate(caractere):
                tela.blit(self.tiles[letra], (coluna * TILE_SIZE, linha * TILE_SIZE))

    colisoes = []
    def criar_colisoes(self):
        self.colisoes.clear()
        for linha, texto in enumerate(MAPA):
            for coluna, letra in enumerate(texto):
                if letra in ("1","2","3","B","C", "W", "S"):
                    self.colisoes.append(
                        pygame.Rect(
                            coluna * TILE_SIZE,
                            linha * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                    )

        