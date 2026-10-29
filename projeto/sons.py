
import os
import pygame
from caminhos import SOUNDS_DIR
from caminhos import SOUNDS_FS
from caminhos import SOUNDS_BT

pygame.init()
class Sons:
    def __init__(self):
        pygame.mixer.init()
    def carregar_som(self, caminho, volume=0.5):
     som = pygame.mixer.Sound(caminho)
     som.set_volume(volume)
     return som
    
som_inicial = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "Fundo_espaço-menu.mp3"))

som_face = pygame.mixer.Sound(os.path.join(SOUNDS_FS, "Fundo_face.mp3"))
som_face.set_volume(0.3)

som_botoes = pygame.mixer.Sound(os.path.join(SOUNDS_BT, "Som_botoes.mp3"))
som_botoes.set_volume(0.5)

        





