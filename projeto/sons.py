
import os
import pygame
from caminhos import SOUNDS_DIR
from caminhos import SOUNDS_FS

pygame.init()
class Sons:
    def __init__(self):
        pygame.mixer.init()


som_inicial = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "Fundo_espaço-menu.mp3"))

som_face = pygame.mixer.Sound(os.path.join(SOUNDS_FS, "Fundo_face.mp3"))





