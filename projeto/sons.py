
import os
import pygame

from caminhos import SOUNDS_DIR

pygame.init()
class Sons:
    def __init__(self):
        pygame.mixer.init()


som_inicial = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "Fundo_espaço-menu.mp3"))

