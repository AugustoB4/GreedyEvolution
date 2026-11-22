"""Preparação mínima do Pygame para executar os testes sem abrir uma janela real."""

import atexit
import os
from pathlib import Path
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

PROJETO_DIR = Path(__file__).resolve().parents[1]
if str(PROJETO_DIR) not in sys.path:
    sys.path.insert(0, str(PROJETO_DIR))

import pygame

pygame.init()
pygame.display.set_mode((1, 1))
atexit.register(pygame.quit)
