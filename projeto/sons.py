
import os
import pygame
from caminhos import SOUNDS_DIR
from caminhos import SOUNDS_FS
from caminhos import SOUNDS_BT
from caminhos import SOUNDS_PG
from caminhos import SOUNDS_CT
from caminhos import SOUNDS_AD
from caminhos import SOUNDS_FN

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
som_face.set_volume(0.5)

som_botoes = pygame.mixer.Sound(os.path.join(SOUNDS_BT, "Som_botoes.mp3"))
som_botoes.set_volume(0.5)

som_pegar = pygame.mixer.Sound(os.path.join(SOUNDS_PG, "som_coleta_pegar.mp3"))
som_pegar.set_volume(0.5)

som_corte = pygame.mixer.Sound(os.path.join(SOUNDS_CT, "corte_faca.mp3"))
som_corte.set_volume(0.5)

som_andar = pygame.mixer.Sound(os.path.join(SOUNDS_AD, "som_andar.mp3"))
som_andar.set_volume(0.5)

som_forno = pygame.mixer.Sound(os.path.join(SOUNDS_FN, "fritura_fogao.mp3"))
som_forno.set_volume(0.5)






