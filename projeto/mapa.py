import os
import pygame
import random

from constantes import TILE_SIZE
from caminhos import tiles_dir_estilo
from montagem import Montagem
from itens import *

MODELO1 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B22332222O22B2R1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FF1111FFFFF1111FFNM",
    "W1FF2LT2FFFFF2334FF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FF1111FFFFF1111FF1W",
    "W1FF4332FFFFF2TL2FF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1UFFFFFFFFFFFFFFFF1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO2 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B233R2222O22B221W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1F111111FFF111111F1W",
    "W1F22LT22FFF22LT22F1W",
    "W1FFFFFFFFFFFFFFFFFNM",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1F111111FFF111111F1W",
    "W1F243342FFF243342F1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFU1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO3 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1R2B22322O22322B2S1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1F111111FFFFF111FFNM",
    "W1F223322FFFFF2LTFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FF111FFFFF111111F1W",
    "W1FF432FFFFF22LT22F1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFUFFFFFFFF1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO4 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B2O222233222B2R1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1F11FFFFFFFFFF11FF1W",
    "W1FLTFFFFFFFFFF43FF1W",
    "W1FFFFF111111FFFFFF1W",
    "W1FFFFF223322FFFFFFNM",
    "W1F11FFFFFFFFFF11FF1W",
    "W1F43FFFFFFFFFFTLFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFUFFFFFFFF1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO5 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1R2B2233222O222B2S1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1111111111FFFFFFFF1W",
    "W122LT2TL22FFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFFNM",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFF1111111111W",
    "W1FFFFFFFF2234342221W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFU1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO_6 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W132B2O222R222O2B2S1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFFNM",
    "W1111111FFFFFFF11111W",
    "W122LT22FFFFFFF22221W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W11111FFFFFFF1111111W",
    "W12222FFFFFFF2433421W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFUFFFFFFFF1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO_7 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B222O2223322B2R1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1F1111FFFFFF1111FF1W",
    "W1F2LT2FFFFFF4334FFNM",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFF111111FFFFFF1W",
    "W1FFFFF223322FFFFFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFU1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO_8 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1R2B233222O222B22S1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1F111111FFFFFFFFFF1W",
    "W1F22LT22FFFFFFFFFF1W",
    "W1FFFFFFFFFFFF111111W",
    "W1FFFFFFFFFFFF222221W",
    "W1F111111FFFFFFFFFF1W",
    "W1F243342FFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFUFFFFFFNM",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]

MODELO_9 = [
    "WYIIIIIIIIIIIIIIIIIYW",
    "W1S2B11112OS211112R1W",
    "W1FFF1111FFF1111FFF1W",
    "W1FFF1111FFF1111FFF1W",
    "W1FFF2LT2FFF2334FFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FFFFFFFFFFFFFFFFF1W",
    "W1FF1111111111111FF1W",
    "W1FF4332222222TL2FF1W",
    "W1FFFFFFFFFFFFFFFFFNM",
    "W1UFFFFFFFFFFFFFFFF1W",
    "W1111111111111111111W",
    "WWWWWWWWWWWWWWWWWWWWW",
]



MODELOS_BASE = [MODELO1, MODELO2, MODELO3, MODELO4, MODELO5, MODELO_6, MODELO_7, MODELO_8, MODELO_9]

MODULOS_BANCADAS = {
    "dupla": ("1111", "2332"),
    "dupla_ingredientes": ("1111", "2LT2"),
    "dupla_queijo": ("1111", "4332"),
    "ilha_6": ("111111", "223322"),
    "ilha_6_ingredientes": ("111111", "22LTT2"),
    "ilha_6_mista": ("111111", "443344"),
}

def compor_modelo_modular(base, posicionamentos):
    matriz = [list(linha) for linha in base]

    for y in range(3, 9):
        for x in range(2, 19):
            if matriz[y][x] in "1234LT":
                matriz[y][x] = "F"

    for nome, x, y in posicionamentos:
        modulo = MODULOS_BANCADAS[nome]
        for dy, linha_modulo in enumerate(modulo):
            for dx, tile in enumerate(linha_modulo):
                px, py = x + dx, y + dy
                if not (0 <= py < len(matriz) and 0 <= px < len(matriz[py])):
                    raise ValueError(f"Módulo {nome} ultrapassa os limites do mapa")
                if matriz[py][px] != "F":
                    raise ValueError(f"Módulo {nome} sobrepõe o tile {matriz[py][px]} em {(px, py)}")
                matriz[py][px] = tile

    return ["".join(linha) for linha in matriz]

CONFIGURACOES_MODELEX = [
    [
        ("ilha_6", 3, 3),
        ("ilha_6_ingredientes", 12, 3),
        ("ilha_6_ingredientes", 3, 7),
        ("ilha_6_mista", 12, 7),
    ],
    [
        ("dupla", 3, 3),
        ("ilha_6_ingredientes", 12, 3),
        ("ilha_6_ingredientes", 3, 7),
        ("dupla_queijo", 14, 7),
    ],
    [
        ("dupla_ingredientes", 3, 3),
        ("ilha_6_mista", 12, 3),
        ("ilha_6", 3, 7),
        ("dupla_queijo", 14, 7),
    ],
    [
        ("ilha_6_ingredientes", 3, 3),
        ("dupla", 14, 3),
        ("dupla_queijo", 3, 7),
        ("ilha_6_ingredientes", 12, 7),
    ],
    [
        ("dupla", 3, 3),
        ("dupla_ingredientes", 14, 3),
        ("ilha_6_mista", 3, 7),
        ("ilha_6_ingredientes", 12, 7),
    ],
    [
        ("ilha_6", 3, 3),
        ("dupla_queijo", 14, 3),
        ("dupla_ingredientes", 3, 7),
        ("ilha_6_mista", 12, 7),
    ],
    [
        ("dupla_queijo", 3, 3),
        ("ilha_6_ingredientes", 12, 3),
        ("ilha_6_mista", 3, 7),
        ("dupla", 14, 7),
    ],
    [
        ("ilha_6_mista", 3, 3),
        ("dupla_queijo", 14, 3),
        ("ilha_6_ingredientes", 3, 7),
        ("dupla_ingredientes", 14, 7),
    ],
    [
        ("dupla_ingredientes", 3, 3),
        ("dupla_queijo", 14, 3),
        ("ilha_6", 3, 7),
        ("ilha_6_mista", 12, 7),
    ],
]

BASES_EMBARALHADAS = random.sample(
    MODELOS_BASE,
    len(MODELOS_BASE)
)

MODELOS_MODULARES = []

for base, configuracao in zip(
    BASES_EMBARALHADAS,
    CONFIGURACOES_MODELEX
):
    modelo = compor_modelo_modular(
        base,
        configuracao
    )

    MODELOS_MODULARES.append(modelo)

(
    MODELEX1,
    MODELEX2,
    MODELEX3,
    MODELEX4,
    MODELEX5,
    MODELEX6,
    MODELEX7,
    MODELEX8,
    MODELEX9
) = MODELOS_MODULARES

"W = Wall / Parede"
"F = Floor / Chão"
"1 = 1Counter / Bancada de trás"
"2 = 2Counter / Primeira bancada de frente"
"3 = 3Counter / Segunda bancada de frente (com armários)"
"4 = CounterCheese / Segunda bancada de frente (com queijo)"
"S = Sink / Pia"
"O = Oven / Fogão"
"B = CuttingBoard / Tábua de corte"
"Y = RightWindow / Janela da direita"
"I = MiddleWindow / Janela do meio"
"T = TreadMill / Esteira de velocidade"
"N = DeliveryBelt / Esteira de Delivery"
"M = DeliveryWindow / Janela de Delivery"
"R = Refrigerator / Geladeira"

MODELOS_MAPA = [
    *MODELOS_BASE,
    *MODELOS_MODULARES
]

VARIANTES_COZINHA = {
    "classica": {
        "estilo": "classico",
        "pedido": "hamburguer",
        "modelos": MODELOS_MAPA
    },

    "pizzaria": {
        "estilo": "pizzaria",
        "pedido": "pizza",
        "modelos": MODELOS_MAPA
    },

    "reator": {
        "estilo": "reator",
        "pedido": "sushi",
        "modelos": MODELOS_MAPA
    }
}


SIMBOLOS_POR_ESTILO = {
    "pizzaria": {"3": "D", "4": "Q", "T": "V", "L": "2", "R": "2"},
    "reator": {"3": "A", "4": "C", "R": "G", "T": "2", "L": "2"},
}


DISPENSADORES_TEMATICOS = {
    "pizzaria": {
        "D": (Massa, "Dough", "DoughPin.png"),
        "Q": (QueijoLunar, "MoonCheese", "MoonCheesePin.png"),
        "V": (TomateNebuloso, "NebulaTomato", "NebulaTomatoPin.png"),
    },
    "reator": {
        "A": (ArrozEstelar, "StarRice", "StarRicePin.png"),
        "C": (AlgaCosmica, "CosmicSeaweed", "CosmicSeaweedPin.png"),
        "G": (PeixeNebuloso, "NebulaFish", "NebulaFishPin.png"),
    },
}


def sortear_variante():
    nome = random.choice(list(VARIANTES_COZINHA))

    return nome, VARIANTES_COZINHA[nome]
class Tabua:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y

        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)
        
class Forno:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        
        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)

class Armario:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.ingrediente = None

        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)

class ArmarioQueijo:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.ingrediente = None

        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)
class ArmarioTomate:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.ingrediente = None

        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)
        
class ArmarioAlface:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.ingrediente = None

        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)
        
class Geladeira:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.ingrediente = None

        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)

class Lixeira:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y


        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)
        
class Entrega:
     def __init__(self, x, y):
        self.posX = x
        self.posY = y


        self.rect = pygame.Rect(self.posX, self.posY, 48, 48)


class DispensadorIngrediente:
    def __init__(self, x, y, classe_ingrediente, nome_ingrediente, pin, simbolo):
        self.posX = x
        self.posY = y
        self.classe_ingrediente = classe_ingrediente
        self.nome_ingrediente = nome_ingrediente
        self.pin = pin
        self.simbolo = simbolo
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

class Mapa:
    def __init__(self, modelo=None, estilo="classico"):
        self.modelo_original = modelo if modelo is not None else MODELO1
        self.estilo = estilo
        remapeamento = SIMBOLOS_POR_ESTILO.get(estilo, {})
        if remapeamento:
            self.mapa = [
                "".join(remapeamento.get(simbolo, simbolo) for simbolo in linha)
                for linha in self.modelo_original
            ]
        else:
            self.mapa = self.modelo_original
        self.tiles_dir = tiles_dir_estilo(estilo)
        self.tabuas = []
        self.fornos = []
        self.armarios = []
        self.armarios_tomate = []
        self.armarios_alface = []
        self.armarios_queijo = []
        self.geladeiras = []
        self.lixos = []
        self.entregas = []
        self.dispensadores_tematicos = []
        self.colisoes = []
        self.tiles = {

            'F': pygame.image.load(os.path.join(self.tiles_dir, "Floor.png")).convert_alpha(),
            'W': pygame.image.load(os.path.join(self.tiles_dir, "Wall.png")).convert_alpha(),
            'M': pygame.image.load(os.path.join(self.tiles_dir, "DeliveryWindow2.png")).convert_alpha(),
            'N': pygame.image.load(os.path.join(self.tiles_dir, "DeliveryBelt.png")).convert_alpha(),
            '1': pygame.image.load(os.path.join(self.tiles_dir, "CounterUp.png")).convert_alpha(),
            '2': pygame.image.load(os.path.join(self.tiles_dir, "CounterFront.png")).convert_alpha(),
            '3': pygame.image.load(os.path.join(self.tiles_dir, "CounterFront2.png")).convert_alpha(),
            '4': pygame.image.load(os.path.join(self.tiles_dir, "CounterCheese.png")).convert_alpha(),
            'S': pygame.image.load(os.path.join(self.tiles_dir, "Sink.png")).convert_alpha(),
            'B': pygame.image.load(os.path.join(self.tiles_dir, "CuttingBoard.png")).convert_alpha(),
            'Y': pygame.image.load(os.path.join(self.tiles_dir, "RIghtWindow.png")).convert_alpha(),
            'I': pygame.image.load(os.path.join(self.tiles_dir, "MiddleWindow.png")).convert_alpha(),
            '@': pygame.image.load(os.path.join(self.tiles_dir, "TreadMill.png")).convert_alpha(),
            'O': pygame.image.load(os.path.join(self.tiles_dir, "Oven.png")).convert_alpha(),
            'R': pygame.image.load(os.path.join(self.tiles_dir, "Refrigerator.png")).convert_alpha(),
            'L': pygame.image.load(os.path.join(self.tiles_dir, "LettuceDispenser.png")).convert_alpha(),
            'T': pygame.image.load(os.path.join(self.tiles_dir, "TomatoDispenser.png")).convert_alpha(),
            'U': pygame.image.load(os.path.join(self.tiles_dir, "TrashCan.png")).convert_alpha()
        }


        if estilo in ("pizzaria", "reator"):
            self.tiles.update({
                'D': pygame.image.load(os.path.join(self.tiles_dir, "DoughDispenser.png")).convert_alpha(),
                'Q': pygame.image.load(os.path.join(self.tiles_dir, "MoonCheeseDispenser.png")).convert_alpha(),
                'G': pygame.image.load(os.path.join(self.tiles_dir, "NebulaFishDispenser.png")).convert_alpha(),
                'V': pygame.image.load(os.path.join(self.tiles_dir, "NebulaTomatoDispenser.png")).convert_alpha(),
                'A': pygame.image.load(os.path.join(self.tiles_dir, "StarRiceDispenser.png")).convert_alpha(),
                'C': pygame.image.load(os.path.join(self.tiles_dir, "CosmicSeaweedDispenser.png")).convert_alpha(),
            })
        
        self.montagens = []

        for linha, texto in enumerate(self.mapa):
            for coluna, letra in enumerate(texto):

                if letra in ("1", "2", "3", "4"):
                    vizinhos = (
                        (coluna, linha - 1),
                        (coluna, linha + 1),
                        (coluna - 1, linha),
                        (coluna + 1, linha),
                    )
                    tem_piso_de_acesso = any(
                        0 <= y < len(self.mapa)
                        and 0 <= x < len(self.mapa[y])
                        and self.mapa[y][x] == "F"
                        for x, y in vizinhos
                    )
                    if not tem_piso_de_acesso:
                        continue

                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE

                    montagem = Montagem(x, y)
                    self.montagens.append(montagem)

    def desenhar(self, tela):
        for linha, caractere in enumerate(self.mapa):
            for coluna, letra in enumerate(caractere):
                sprite = self.tiles[letra]
                if letra == "Y" and coluna == 19:
                    sprite = pygame.transform.flip(sprite, True, False) # Virar os tiles em qualquer direção
                    
                if letra == "M" and coluna == 20:
                    sprite = pygame.transform.rotate(sprite, -90) # ROtaciona a imagem em graus
                    
                if letra == "W" and coluna == 0:
                    sprite = pygame.transform.rotate(sprite, 90) 
                    
                if letra == "W" and linha == 13:
                    sprite = pygame.transform.rotate(sprite, 180)
                    
                if letra == "W" and coluna == 20:
                    sprite = pygame.transform.rotate(sprite, -90) 
                    
                if letra == "R":
                    sprite = pygame.transform.scale(self.tiles["R"], (TILE_SIZE, TILE_SIZE * 2))
                    tela.blit(sprite,(coluna * TILE_SIZE, linha * TILE_SIZE - TILE_SIZE))
                    continue

                tela.blit(sprite,(coluna * TILE_SIZE, linha * TILE_SIZE))



    def desenhar_preparo(self, tela, ingredientes):
        for ingrediente in ingredientes:
            if ingrediente.metodo_preparo not in ("assar", "cozinhar"):
                continue
            for forno in self.fornos:
                if ingrediente.rect.colliderect(forno.rect):
                    ingrediente.desenhar_barra_preparo(tela, forno)


    def criar_colisoes(self):
        self.colisoes.clear()
        self.tabuas.clear()
        self.fornos.clear()
        self.armarios.clear()
        self.armarios_tomate.clear()
        self.armarios_alface.clear()
        self.armarios_queijo.clear()
        self.geladeiras.clear()
        self.entregas.clear()
        self.lixos.clear()
        self.dispensadores_tematicos.clear()
        
        
        for linha, texto in enumerate(self.mapa):
            for coluna, letra in enumerate(texto):
                if letra in ("1", "2", "3", "4", "B", "C", "W", "S", "M", "O", "N", "R", "L", "T", "U", "D", "Q", "G", "V", "A"): # Adiciona colisão ao tile
                    self.colisoes.append(
                        pygame.Rect(
                            coluna * TILE_SIZE,
                            linha * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                    )

                if letra == "U":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    self.lixos.append(Lixeira(x, y))

                if letra == "B":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    self.tabuas.append(Tabua(x, y))


                if letra == "O":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    self.fornos.append(Forno(x, y))

                if letra == "3":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    armario = Armario(x, y)
                    armario.ingrediente = Pao(x, y)
                    self.armarios.append(armario)

                if letra == "T":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    armario_tomate = ArmarioTomate(x, y)
                    armario_tomate.ingrediente = Tomate(x, y)
                    self.armarios_tomate.append(armario_tomate)
                
                if letra == "L":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    armario_alface = ArmarioAlface(x, y)
                    armario_alface.ingrediente = Alface(x, y)
                    self.armarios_alface.append(armario_alface)

                if letra == "4":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    armario_queijo = ArmarioQueijo(x, y)
                    armario_queijo.ingrediente = Queijo(x, y)
                    self.armarios_queijo.append(armario_queijo)
                    
                if letra == "R":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    geladeira = Geladeira(x, y)
                    geladeira.ingrediente = Carne(x, y)
                    self.geladeiras.append(geladeira)
                    
                if letra == "N":
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    entrega = Entrega(x, y)
                    self.entregas.append(entrega)

                configuracao_dispensador = DISPENSADORES_TEMATICOS.get(
                    self.estilo, {}
                ).get(letra)
                if configuracao_dispensador:
                    classe_ingrediente, nome_ingrediente, pin = configuracao_dispensador
                    x = coluna * TILE_SIZE
                    y = linha * TILE_SIZE
                    self.dispensadores_tematicos.append(
                        DispensadorIngrediente(
                            x, y, classe_ingrediente, nome_ingrediente,
                            pin, letra,
                        )
                    )
                    

    def pode_largar(self, x, y):
        coluna = x // TILE_SIZE
        linha = y // TILE_SIZE

        if linha < 0 or linha >= len(self.mapa):
            return False

        if coluna < 0 or coluna >= len(self.mapa[linha]):
            return False

        return self.mapa[linha][coluna] in ("F", "B")

