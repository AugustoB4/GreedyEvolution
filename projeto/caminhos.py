import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
BASE_FS = os.path.dirname(
    os.path.abspath(__file__)
)
BASE_BT = os.path.dirname(
    os.path.abspath(__file__)
)
BASE_PG = os.path.dirname(
    os.path.abspath(__file__)
)
BASE_CT = os.path.dirname(
    os.path.abspath(__file__)
)
BASE_FT = os.path.dirname(
    os.path.abspath(__file__)
)

SPRITES_DIR = os.path.join(
    BASE_DIR, "assets", "sprites"
)

BACKGROUND_DIR = os.path.join(
    SPRITES_DIR, "background"
)

ANIMATION_DIR = os.path.join(
    SPRITES_DIR, "animations"
)

PINS_DIR = os.path.join(
    SPRITES_DIR, "pins"
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
SOUNDS_FS = os.path.join(
    BASE_FS, "assets", "sounds"
)
SOUNDS_BT = os.path.join(
    BASE_BT, "assets", "sounds"

)
SOUNDS_PG = os.path.join(
    BASE_PG, "assets", "sounds"
)
SOUNDS_CT = os.path.join(
    BASE_CT, "assets", "sounds"
)
SOUNDS_FT = os.path.join(
    BASE_FT, "assets", "sounds"
)