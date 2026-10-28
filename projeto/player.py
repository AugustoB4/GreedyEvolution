import os
import pygame

from mapa import *
from itens import *
from constantes import *
from caminhos import PLAYER_DIR


# Classe base
tomates = []
queijos = []
paos = []
carnes  = []
alfaces = []

class Personagem:
    def __init__(self, x, y, sprite_path, teclas):

        self.pos_x = x
        self.pos_y = y
        self.teclas = teclas
        self.velocidade = VELOCIDADE
        self.objeto = None

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()

        self.largura_sprite = (self.sprite_sheet.get_width() // 3)

        self.altura_sprite = (
            self.sprite_sheet.get_height()
        )

        self.rect = pygame.Rect(
            self.pos_x + 16,
            self.pos_y + 76,
            32,
            20
        )

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

        self.rect.x += dirX

        for parede in colisoes:
            if self.rect.colliderect(parede):
                if dirX > 0:
                    self.rect.right = parede.left

                elif dirX < 0:
                    self.rect.left = parede.right

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
            self.altura_sprite
        )

        sprite = self.sprite_sheet.subsurface(area)

        if self.virado_esquerda:
            sprite = pygame.transform.flip(
                sprite,
                True,
                False
            )

        sprite = pygame.transform.scale(
            sprite,
            (64, 96)
        )

        tela.blit(
            sprite,
            (self.pos_x, self.pos_y)
        )

        pygame.draw.rect(
            tela,
            (255, 0, 0),
            self.area_interacao(),
            2
        )

    def area_interacao(self):
        if self.direcao == "frente":
            area = pygame.Rect(
                self.rect.x,
                self.rect.bottom,
                self.rect.width,
                TILE_SIZE
            )

        elif self.direcao == "costas":
            area = pygame.Rect(
                self.rect.x,
                self.rect.top - 30,
                self.rect.width,
                TILE_SIZE
            )

        elif self.direcao == "lado":
            if self.virado_esquerda:
                area = pygame.Rect(
                    self.rect.right,
                    self.rect.y,
                    TILE_SIZE,
                    self.rect.height
                )

            else:
                area = pygame.Rect(
                    self.rect.left - 30,
                    self.rect.y,
                    TILE_SIZE,
                    self.rect.height
                )

        return area

    def pegar(self, armarios, armarios_queijo, armarios_tomate, armarios_alface,
              geladeiras, tomates, alfaces, queijos, paos, carnes):
        area = self.area_interacao()

        if self.objeto:
            return

        for item in list(tomates):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                return
            
        for item in list(alfaces):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                return
            
        for item in list(queijos):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                return
            
        for item in list(paos):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                return
            
        for item in list(carnes):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                return

        for armario_tomate in armarios_tomate:
            if area.colliderect(armario_tomate.rect):
                tomate_do_armario = Tomate(armario_tomate.posX, armario_tomate.posY)
                tomate_do_armario.dono = self
                self.objeto = tomate_do_armario
                tomates.append(tomate_do_armario)
                return
            
        for armario_alface in armarios_alface:
            if area.colliderect(armario_alface.rect):
                alface_do_armario = Alface(armario_alface.posX, armario_alface.posY)
                alface_do_armario.dono = self
                self.objeto = alface_do_armario
                alfaces.append(alface_do_armario)
                return

        for armario_queijo in armarios_queijo:
            if area.colliderect(armario_queijo.rect):
                queijo_do_armario = Queijo(armario_queijo.posX, armario_queijo.posY)
                queijo_do_armario.dono = self
                self.objeto = queijo_do_armario 
                queijos.append(queijo_do_armario)
                return
            
        for armario in armarios:
            if area.colliderect(armario.rect):
                pao_do_armario = Pao(armario.posX, armario.posY)
                pao_do_armario.dono = self
                self.objeto = pao_do_armario
                paos.append(pao_do_armario)
                return

        for geladeira in geladeiras:
            if area.colliderect(geladeira.rect):
                carne_da_geladeira = Carne(geladeira.posX, geladeira.posY)
                carne_da_geladeira.dono = self
                self.objeto = carne_da_geladeira
                carnes.append(carne_da_geladeira)
                return

    def cortar(self, tabuas, tomates, alfaces, queijos, paos, carnes):
        area = self.area_interacao()

        for tabua in tabuas:
            if not area.colliderect(tabua.rect):
                continue

            if self.objeto:
                if self.objeto.corte and not self.objeto.cortado:
                    self.objeto.cortar_ingrediente()
                return

            for item in tomates:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        return

            for item in alfaces:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        return

            for item in queijos:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        return

            for item in paos:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        return

            for item in carnes:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        return

    def largar(self):
        if not self.objeto:
            return

        area = self.area_interacao()

        coluna = area.centerx // TILE_SIZE
        linha = area.centery // TILE_SIZE

        if linha < 0 or linha >= len(MAPA):
            return

        if coluna < 0 or coluna >= len(MAPA[linha]):
            return

        centro_x = (coluna * TILE_SIZE + TILE_SIZE // 2)
        centro_y = (linha * TILE_SIZE + TILE_SIZE // 2)

        self.objeto.dono = None
        self.objeto.x = (centro_x - self.objeto.rect.width // 2)
        self.objeto.y = (centro_y - self.objeto.rect.height // 2)
        self.objeto.rect.topleft = (self.objeto.x, self.objeto.y)
        self.objeto = None

    def verificar_habilidades(self, evento, armarios, armarios_queijo, armarios_tomate,
                              armarios_alface, geladeiras, tomates, alfaces, queijos,
                              paos, carnes):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["pegar"]:
                self.pegar(armarios, armarios_queijo, armarios_tomate, armarios_alface,
                           geladeiras, tomates, alfaces, queijos, paos, carnes)

            elif evento.key == self.teclas["largar"]:
                self.largar()

    def verificar_cortagem(self, evento, tabuas, tomates, alfaces, queijos, paos,
                           carnes):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["cortar"]:
                self.cortar(tabuas, tomates, alfaces, queijos, paos, carnes)
class Romerio(Personagem):
    def __init__(self, x, y):
        teclas = {
            "pegar": pygame.K_RSHIFT,
            "largar": pygame.K_RCTRL,
            "cortar": pygame.K_SEMICOLON,
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN
        }
        super().__init__(x, y, os.path.join(PLAYER_DIR,"Romerio.png"),teclas)

class Brito(Personagem):
    def __init__(self, x, y):
        teclas = {
            "pegar": pygame.K_q,
            "largar": pygame.K_1,
            "cortar": pygame.K_2,
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "cima": pygame.K_w,
            "baixo": pygame.K_s
        }

        super().__init__(x, y, os.path.join(PLAYER_DIR, "Brito.png"),teclas)

    def desenhar(self, tela):
        return super().desenhar(tela)
