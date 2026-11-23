import os
import pygame
import random
import re
from collections import deque

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
    "W1FF11111FFFFF111FFNM",
    "W1FF22322FFFFF2LTFF1W",
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
    "W1S2B11112OS111112R1W",
    "W1FFFFFFFFFFFFFFFFF1W",
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

LARGURA_BANCADA_MAXIMA = 6
DISTANCIA_MAXIMA_INICIAL_EQUIPAMENTO = 24
DISTANCIA_MAXIMA_ENTRE_INGREDIENTES = 24


def normalizar_bancadas(modelo, largura_maxima=LARGURA_BANCADA_MAXIMA):
    """Divide bancadas frontais longas em segmentos sem remover dispensadores."""
    if largura_maxima < 1:
        raise ValueError("A largura máxima de bancada deve ser positiva")
    if modelo and any(len(linha) != len(modelo[0]) for linha in modelo):
        raise ValueError("O mapa-base precisa ter linhas retangulares")
    matriz = [list(linha) for linha in modelo]
    y_final = min(9, len(matriz))
    for y in range(3, y_final):
        while True:
            excedentes = [
                (match.start(), match.end())
                for match in re.finditer(r"[234LT]+", "".join(matriz[y]))
                if match.end() - match.start() > largura_maxima
            ]
            if not excedentes:
                break

            inicio, fim = excedentes[0]
            candidatos = [
                indice
                for indice in range(inicio, fim)
                if matriz[y][indice] == "2"
                and y > 0
                and matriz[y - 1][indice] == "1"
                and indice - inicio <= largura_maxima
                and fim - indice - 1 <= largura_maxima
            ]
            if not candidatos:
                break

            divisao = min(
                candidatos,
                key=lambda indice: (
                    abs((indice - inicio) - (fim - indice - 1)),
                    abs(indice - (inicio + fim - 1) / 2),
                ),
            )
            matriz[y][divisao] = "F"
            matriz[y - 1][divisao] = "F"

    return ["".join(linha) for linha in matriz]


for _modelo_base in MODELOS_BASE:
    _modelo_base[:] = normalizar_bancadas(_modelo_base)

MODULOS_BANCADAS = {
    "dupla": ("1111", "2332"),
    "dupla_ingredientes": ("1111", "2LT2"),
    "dupla_queijo": ("1111", "4332"),
    "ilha_6": ("111111", "223322"),
    "ilha_6_ingredientes": ("111111", "2L2T22"),
    "ilha_6_mista": ("111111", "432324"),
}

def compor_modelo_modular(base, posicionamentos):
    if len(base) != 13 or any(len(linha) != 21 for linha in base):
        raise ValueError("O mapa-base precisa ter 13 linhas por 21 colunas")
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

    return normalizar_bancadas(["".join(linha) for linha in matriz])

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


def _remapear_modelo(modelo, estilo):
    remapeamento = SIMBOLOS_POR_ESTILO.get(estilo, {})
    return [
        "".join(remapeamento.get(simbolo, simbolo) for simbolo in linha)
        for linha in modelo
    ]


def _distancias_piso(pisos, origens):
    origens_validas = [origem for origem in origens if origem in pisos]
    distancias = {origem: 0 for origem in origens_validas}
    fila = deque(origens_validas)
    while fila:
        x, y = fila.popleft()
        for vizinho in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if vizinho in pisos and vizinho not in distancias:
                distancias[vizinho] = distancias[(x, y)] + 1
                fila.append(vizinho)
    return distancias


def _celulas_de_acesso(modelo, posicao, pisos):
    x, y = posicao
    return tuple(
        vizinho
        for vizinho in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        if vizinho in pisos
    )


def problemas_validacao_modelo(modelo, estilo="classico"):
    """Lista falhas estruturais, de acesso e de distribuição do mapa."""
    if not modelo or len(modelo) != 13 or any(len(linha) != 21 for linha in modelo):
        return ("grade precisa ter 13 linhas por 21 colunas",)

    modelo_estilo = _remapear_modelo(modelo, estilo)
    simbolos_validos = set("WF1234SBOYINMRLTU@")
    simbolos_validos.update(SIMBOLOS_POR_ESTILO.get(estilo, {}).values())
    simbolos_validos.update(DISPENSADORES_TEMATICOS.get(estilo, {}))
    usados = set("".join(modelo_estilo))
    desconhecidos = usados - simbolos_validos
    problemas = []
    if desconhecidos:
        problemas.append(f"símbolos sem tile: {sorted(desconhecidos)}")

    if estilo == "classico":
        ingredientes = ("3", "4", "T", "L", "R")
    elif estilo == "pizzaria":
        ingredientes = ("D", "Q", "V")
    elif estilo == "reator":
        ingredientes = ("A", "C", "G")
    else:
        problemas.append(f"estilo desconhecido: {estilo}")
        return tuple(problemas)

    texto = "".join(modelo_estilo)
    for simbolo in ingredientes:
        if simbolo not in texto:
            problemas.append(f"ingrediente obrigatório ausente: {simbolo}")
    for simbolo in "SOB":
        if simbolo not in texto:
            problemas.append(f"equipamento obrigatório ausente: {simbolo}")
    for simbolo in "NMU":
        if texto.count(simbolo) != 1:
            problemas.append(f"esperado exatamente um equipamento {simbolo}")

    # Os módulos frontais precisam de uma bancada de apoio alinhada acima.
    # Os símbolos da linha superior são estações de parede e não entram nesta regra.
    for y in range(3, 9):
        linha = modelo[y]
        for match in re.finditer(r"[234LT]+", linha):
            inicio, fim = match.span()
            if fim - inicio > LARGURA_BANCADA_MAXIMA:
                problemas.append(
                    f"bancada frontal com {fim - inicio} tiles na linha {y}"
                )
            if any(modelo[y - 1][x] != "1" for x in range(inicio, fim)):
                problemas.append(f"bancada sem apoio alinhado na linha {y}")
            if any(modelo[y + 1][x] != "F" for x in range(inicio, fim)):
                problemas.append(f"bancada bloqueia o acesso na linha {y}")
        if any(duplicado in linha for duplicado in ("44", "TT", "LL")):
            problemas.append(f"dispensadores duplicados em sequência na linha {y}")

    pisos = {
        (x, y)
        for y, linha in enumerate(modelo_estilo)
        for x, simbolo in enumerate(linha)
        if simbolo == "F"
    }
    inicio_jogador_1 = ((624 + 32) // TILE_SIZE, (192 + 86) // TILE_SIZE)
    inicio_jogador_2 = ((240 + 32) // TILE_SIZE, (240 + 86) // TILE_SIZE)
    distancias_inicio = _distancias_piso(pisos, (inicio_jogador_1,))
    distancias_inicio_2 = _distancias_piso(pisos, (inicio_jogador_2,))
    if inicio_jogador_1 not in pisos or inicio_jogador_2 not in pisos:
        problemas.append("jogadores não começam no mesmo corredor acessível")

    simbolos_estacao = set(ingredientes) | set("SOBNU")
    posicoes_estacoes = {
        simbolo: [
            (x, y)
            for y, linha in enumerate(modelo_estilo)
            for x, atual in enumerate(linha)
            if atual == simbolo
        ]
        for simbolo in simbolos_estacao
    }
    celulas_interativas = {
        (x, y)
        for y in range(3, 9)
        for x, simbolo in enumerate(modelo_estilo[y])
        if simbolo in set("234")
        | set(SIMBOLOS_POR_ESTILO.get(estilo, {}).values())
    }
    grupos_acesso = {}
    todas_estacoes = set(celulas_interativas)
    for simbolo, posicoes in posicoes_estacoes.items():
        acessos = {
            acesso
            for posicao in posicoes
            for acesso in _celulas_de_acesso(modelo_estilo, posicao, pisos)
        }
        if not acessos:
            problemas.append(f"equipamento {simbolo} sem piso de acesso")
        elif not all(
            any(acesso in distancias for acesso in acessos)
            for distancias in (distancias_inicio, distancias_inicio_2)
        ):
            problemas.append(f"equipamento {simbolo} inacessível a um jogador")
        if simbolo in ingredientes:
            grupos_acesso[simbolo] = acessos
        todas_estacoes.update(posicoes)

    for posicao in celulas_interativas:
        acessos = _celulas_de_acesso(modelo_estilo, posicao, pisos)
        if not acessos or not all(
            any(acesso in distancias for acesso in acessos)
            for distancias in (distancias_inicio, distancias_inicio_2)
        ):
            problemas.append("bancada sem acesso transitável")

    distancia_maxima = 0
    for posicao in todas_estacoes:
        acessos = _celulas_de_acesso(modelo_estilo, posicao, pisos)
        for distancias_inicio_jogador in (distancias_inicio, distancias_inicio_2):
            distancias = [
                distancias_inicio_jogador[acesso]
                for acesso in acessos
                if acesso in distancias_inicio_jogador
            ]
            if distancias:
                distancia_maxima = max(distancia_maxima, min(distancias))
    if distancia_maxima > DISTANCIA_MAXIMA_INICIAL_EQUIPAMENTO:
        problemas.append("equipamento essencial distante das posições iniciais")

    nomes_ingredientes = list(ingredientes)
    for indice, nome_a in enumerate(nomes_ingredientes):
        acessos_a = grupos_acesso.get(nome_a, set())
        distancias = _distancias_piso(pisos, acessos_a)
        for nome_b in nomes_ingredientes[indice + 1:]:
            acessos_b = grupos_acesso.get(nome_b, set())
            distancias_validas = [distancias[p] for p in acessos_b if p in distancias]
            if distancias_validas and min(distancias_validas) > DISTANCIA_MAXIMA_ENTRE_INGREDIENTES:
                problemas.append(f"ingredientes {nome_a} e {nome_b} muito distantes")

    return tuple(dict.fromkeys(problemas))


def validar_modelo(modelo, estilo="classico"):
    return not problemas_validacao_modelo(modelo, estilo)


SEMENTE_MODELOS_MODULARES = 261122
MAX_TENTATIVAS_MAPA_MODULAR = len(MODELOS_BASE) * len(CONFIGURACOES_MODELEX)


def gerar_modelos_modulares(
    semente=SEMENTE_MODELOS_MODULARES,
    configuracoes=None,
    max_tentativas=None,
):
    """Gera uma variante por base com tentativas limitadas e fallback válido."""
    rng = random.Random(semente)
    bases = rng.sample(MODELOS_BASE, len(MODELOS_BASE))
    configs = CONFIGURACOES_MODELEX if configuracoes is None else configuracoes
    indices_configs = list(range(len(configs)))
    limite = (
        MAX_TENTATIVAS_MAPA_MODULAR
        if max_tentativas is None
        else max(0, int(max_tentativas))
    )
    tentativas = 0
    configs_usadas = set()
    modelos = []

    for base in bases:
        escolhido = None
        ordem_configs = rng.sample(indices_configs, len(indices_configs))
        for indice_config in ordem_configs:
            if indice_config in configs_usadas:
                continue
            if tentativas >= limite:
                break
            tentativas += 1
            try:
                candidato = compor_modelo_modular(base, configs[indice_config])
            except (IndexError, KeyError, TypeError, ValueError):
                continue
            if all(
                validar_modelo(candidato, estilo)
                for estilo in ("classico", "pizzaria", "reator")
            ):
                escolhido = candidato
                configs_usadas.add(indice_config)
                break

        if escolhido is None:
            fallback = base if all(
                validar_modelo(base, estilo)
                for estilo in ("classico", "pizzaria", "reator")
            ) else MODELO1
            escolhido = list(fallback)
        modelos.append(escolhido)

    return modelos


MODELOS_MODULARES = gerar_modelos_modulares()
(
    MODELEX1,
    MODELEX2,
    MODELEX3,
    MODELEX4,
    MODELEX5,
    MODELEX6,
    MODELEX7,
    MODELEX8,
    MODELEX9,
) = MODELOS_MODULARES
MODELOS_MAPA = [*MODELOS_BASE, *MODELOS_MODULARES]

VARIANTES_COZINHA = {
    "classica": {"estilo": "classico", "pedido": "hamburguer", "modelos": MODELOS_MAPA},
    "pizzaria": {"estilo": "pizzaria", "pedido": "pizza", "modelos": MODELOS_MAPA},
    "reator": {"estilo": "reator", "pedido": "sushi", "modelos": MODELOS_MAPA},
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

        # Fornos são superfícies de preparo e aceitam ingredientes largados.
        return self.mapa[linha][coluna] in ("F", "B", "O")

