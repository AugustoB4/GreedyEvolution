import pygame
from mapa import *
from constantes import *

# Classe base
class Personagem:
    def __init__(self, x, y, sprite_path, teclas):

        self.pos_x = x
        self.pos_y = y
        self.teclas = teclas
        self.velocidade = VELOCIDADE
        self.objeto = None

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()

        self.largura_sprite = self.sprite_sheet.get_width() // 3
        self.altura_sprite = self.sprite_sheet.get_height()

        self.direcao = "frente"
        self.virado_esquerda = False

        self.frames = {
            "frente": 0,
            "lado": 1,
            "costas": 2
        }

    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()
    
        if teclas_pressionadas[self.teclas["esquerda"]]:
            self.pos_x -= VELOCIDADE
            self.direcao = "lado"
            self.virado_esquerda = False

        if teclas_pressionadas[self.teclas["direita"]]:
            self.pos_x += VELOCIDADE
            self.direcao = "lado"
            self.virado_esquerda = True

        if teclas_pressionadas[self.teclas["cima"]]:
            self.pos_y -= VELOCIDADE
            self.direcao = "costas"

        if teclas_pressionadas[self.teclas["baixo"]]:
            self.pos_y += VELOCIDADE
            self.direcao = "frente"

    def desenhar(self, tela):
        indice = self.frames[self.direcao]

        area = pygame.Rect(
            indice * self.largura_sprite,
            0,
            self.largura_sprite,
            self. altura_sprite
        )

        sprite = self.sprite_sheet.subsurface(area)

        if self.virado_esquerda:
            sprite = pygame.transform.flip(sprite,True, False)

        sprite = pygame.transform.scale(sprite,(64, 96))
        tela.blit(sprite,(self.pos_x, self.pos_y))

    def cortar(self):
         pass

    def pegar(self, objeto):
            
        if self.objeto is None:
            self.objeto = objeto
            print("Pegou")

    def largar(self):
        if self.objeto is not None:
            self.objeto = None
            print("Largou")


    def verificar_habilidades(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["pegar"]:
                print("Tentou Pegar")
            elif evento.key == self.teclas["largar"]:
                self.largar()

# Romerio herda Personagem
class Romerio(Personagem):
    def __init__(self, x, y):
        teclas = {
            "pegar": pygame.K_RCTRL,
            "largar": pygame.K_RSHIFT,
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN
        }

        super().__init__(x, y, "projeto/assets/sprites/player/Romerio.png", teclas)

# Brito 
class Brito(Personagem):
    def __init__(self, x, y):
        teclas = {
            "pegar": pygame.K_z,
            "largar": pygame.K_x,
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "cima": pygame.K_w,
            "baixo": pygame.K_s
        }

        super().__init__(x, y, "projeto/assets/sprites/player/Brito.png", teclas)

    def desenhar(self, tela):
        return super().desenhar(tela)

