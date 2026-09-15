import os
import pygame

from mapa import MAPA
from itens import Tomate
from constantes import TILE_SIZE, VELOCIDADE
from caminhos import PLAYER_DIR


# Classe base

class Personagem:

    def __init__(self, x, y, sprite_path, teclas, jogo=None):

        self.pos_x = x
        self.pos_y = y
        self.teclas = teclas
        self.velocidade = VELOCIDADE
        self.objeto = None
        self.jogo = jogo

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

        if self.objeto is not None:
            self.objeto.atualizar()
            tela.blit(self.objeto.sprite, (self.objeto.x, self.objeto.y))

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

    def _aponta_para(self, alvo_rect):
        if self.direcao == "frente":
            return self.rect.bottom <= alvo_rect.top + 20 and self.rect.centery <= alvo_rect.centery

        if self.direcao == "costas":
            return self.rect.top >= alvo_rect.bottom - 20 and self.rect.centery >= alvo_rect.centery

        if self.direcao == "lado":
            if self.virado_esquerda:
                return self.rect.left >= alvo_rect.right - 20 and self.rect.centerx >= alvo_rect.centerx
            return self.rect.right <= alvo_rect.left + 20 and self.rect.centerx <= alvo_rect.centerx

        return False

    def pegar(self, ingrediente, armarios):
        area = self.area_interacao()

        if self.objeto:
            return

        itens_para_tentar = [ingrediente]
        if self.jogo is not None:
            itens_para_tentar.extend(
                item for item in self.jogo.itens_no_mapa
                if item is not ingrediente and item.dono is None
            )

        for item in itens_para_tentar:
            if item is None:
                continue

            if area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                if self.jogo is not None and item in self.jogo.itens_no_mapa:
                    self.jogo.itens_no_mapa.remove(item)
                return

        for armario in armarios:
            if area.colliderect(armario.rect) and self._aponta_para(armario.rect):
                if armario.ingrediente is not None and armario.ingrediente.dono is None:
                    armario.ingrediente.dono = self
                    self.objeto = armario.ingrediente
                    armario.ingrediente = None
                    return


    def cortar(self, ingrediente, tabuas):
        alvo = self.objeto if self.objeto is not None else ingrediente
        if alvo is None:
            return

        area = self.area_interacao()
        for tabua in tabuas:
            if area.colliderect(alvo.rect) and alvo.rect.colliderect(tabua.rect):
                if alvo.corte and not alvo.cortado:
                    alvo.cortar_ingrediente()
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

        if MAPA[linha][coluna] not in ("F", "B", "1", "2", "3"):
            return

        centro_x = (coluna * TILE_SIZE + TILE_SIZE // 2)
        centro_y = (linha * TILE_SIZE + TILE_SIZE // 2)

        self.objeto.dono = None
        self.objeto.x = (centro_x - self.objeto.rect.width // 2)
        self.objeto.y = (centro_y - self.objeto.rect.height // 2)
        self.objeto.rect.topleft = (self.objeto.x, self.objeto.y)

        if self.jogo is not None and self.objeto not in self.jogo.itens_no_mapa:
            self.jogo.itens_no_mapa.append(self.objeto)

        self.objeto = None

    def verificar_habilidades(self, evento, ingrediente, armarios):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["pegar"]:
                self.pegar(ingrediente, armarios)

            elif evento.key == self.teclas["largar"]:
                self.largar()

    def verificar_cortagem(self, evento, ingrediente, tabuas):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["cortar"]:
                alvo = self.objeto if self.objeto is not None else ingrediente
                self.cortar(alvo, tabuas)
    
class Romerio(Personagem):
    def __init__(self, x, y, jogo=None):
        teclas = {
            "pegar": pygame.K_RSHIFT,
            "largar": pygame.K_RCTRL,
            "cortar": pygame.K_SEMICOLON,
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN
        }
        super().__init__(x, y, os.path.join(PLAYER_DIR,"Romerio.png"),teclas,jogo)

class Brito(Personagem):
    def __init__(self, x, y, jogo=None):
        teclas = {
            "pegar": pygame.K_q,
            "largar": pygame.K_1,
            "cortar": pygame.K_2,
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "cima": pygame.K_w,
            "baixo": pygame.K_s
        }

        super().__init__(x, y, os.path.join(PLAYER_DIR, "Brito.png"),teclas,jogo)

    def desenhar(self, tela):
        return super().desenhar(tela)