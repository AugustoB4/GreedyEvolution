import pygame
from constantes import TILE_SIZE

MAPA = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFCCCCCCCCCCCCCCCCCCCCCCCCCCFFW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

class Mapa:
    def __init__(self):
        self.tiles = {
            'F': pygame.image.load("projeto/assets/sprites/tiles/floor.png").convert_alpha(),
            'W': pygame.image.load("projeto/assets/sprites/tiles/wall.png").convert_alpha(),
            'C': pygame.image.load("projeto/assets/sprites/tiles/counter0.png").convert_alpha()
        }

    def desenhar(self, tela):
        for linha, caractere in enumerate(MAPA):
            for coluna, letra in enumerate(caractere):
                tela.blit(self.tiles[letra], (coluna * TILE_SIZE, linha * TILE_SIZE))