import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SPRITES_DIR = os.path.join(
    BASE_DIR, "assets", "sprites"
)

BACKGROUND_DIR = os.path.join(
    SPRITES_DIR, "background"
)

INGREDIENTS_DIR = os.path.join(
    SPRITES_DIR, "ingredients"
)

PLAYER_DIR = os.path.join(
    SPRITES_DIR, "player"
)

TILES_DIR = os.path.join(
    SPRITES_DIR, "tiles"
)

UI_DIR = os.path.join(
    SPRITES_DIR, "ui"
)

SOUNDS_DIR = os.path.join(
    BASE_DIR, "assets", "sounds"
)