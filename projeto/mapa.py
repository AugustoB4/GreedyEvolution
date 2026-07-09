import pygame
from constantes import TILE_SIZE

MAPA = [
    "WWWWWWWWWWWWWWWWWWWWW",
    "WFFFFF22S222B22FFFFFW",
    "WFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFW",
    "WFFFFF222222221FFFFFW",
    "WFFFFFFFFFFFFF1FFFFFW",
    "WFFFFFFFFFFFFF1FFFFFW",
    "WFFFFFFFFFFFFF2FFFFFW",
    "WFFFFFFFFFFFFFFFFFFFW",
    "WWWWWWWWWWWWWWWWWWWWW",
]

class Mapa:
    def __init__(self):
        self.tiles = {
            'F': pygame.image.load("projeto/assets/sprites/tiles/Floor.png").convert_alpha(),
            'W': pygame.image.load("projeto/assets/sprites/tiles/Wall.png").convert_alpha(),
            '1': pygame.image.load("projeto/assets/sprites/tiles/CounterUp.png").convert_alpha(),
            '2': pygame.image.load("projeto/assets/sprites/tiles/CounterFront.png").convert_alpha(),
            'S': pygame.image.load("projeto/assets/sprites/tiles/Sink.png").convert_alpha(),
            'B': pygame.image.load("projeto/assets/sprites/tiles/CuttingBoard.png").convert_alpha()
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
                if letra in ("1","2","B","C", "W", "S"):
                    self.colisoes.append(
                        pygame.Rect(
                            coluna * TILE_SIZE,
                            linha * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                    )
        