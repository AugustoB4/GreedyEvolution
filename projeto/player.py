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

        self.rect = pygame.Rect(self.pos_x + 16, self.pos_y + 76, 32, 20)

        self.direcao = "frente"
        self.virado_esquerda = False

        self.frames = {
            "frente": 0,
            "lado": 1,
            "costas": 2
        }

    def mover(self, colisoes):
        teclas_pressionadas = pygame.key.get_pressed()
        dirX = 0
        dirY = 0

        if teclas_pressionadas[self.teclas["esquerda"]]:
            dirX = -VELOCIDADE
            self.direcao = "lado"
            self.virado_esquerda = False

        if teclas_pressionadas[self.teclas["direita"]]:
            dirX = VELOCIDADE
            self.direcao = "lado"
            self.virado_esquerda = True

        if teclas_pressionadas[self.teclas["cima"]]:
            dirY = -VELOCIDADE
            self.direcao = "costas"

        if teclas_pressionadas[self.teclas["baixo"]]:
            dirY = VELOCIDADE
            self.direcao = "frente"
        if self.objeto:

           self.objeto.x = self.pos_x + 20
           self.objeto.y = self.pos_y

        self.rect.x += dirX

        for parede in colisoes:
             if self.rect.colliderect(parede):
                if dirX > 0:
                    self.rect.right = parede.left
                elif dirX < 0:
                    self.rect.left = parede.right

    # Movimento Y
        self.rect.y += dirY

        for parede in colisoes:
            if self.rect.colliderect(parede):
                if dirY > 0:
                    self.rect.bottom = parede.top
                elif dirY < 0:
                    self.rect.top = parede.bottom

        self.pos_x = self.rect.x - 16
        self.pos_y = self.rect.y - 76

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
        if self.objeto:
            print("estou carregando a comida")

        distancia_x = abs(self.pos_x - objeto.x)
        distancia_y = abs(self.pos_y - objeto.y)

        if distancia_x < 50 and distancia_y < 50:

            
         if objeto.dono is None:
             objeto.dono = self
             self.objeto = objeto
             print("Pegou")

    def largar(self):
        if self.objeto:
            self.objeto.x = self.pos_x
            self.objeto.y = self.pos_y
            self.objeto.dono = None
            self.objeto = None
        print("Largou")


    def verificar_habilidades(self, evento, tomate):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["pegar"]:
                self.pegar(tomate)
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

