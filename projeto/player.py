import os
import pygame

import math
from mapa import *
from itens import *
from constantes import *
from indicadores import *
from caminhos import PLAYER_DIR
from sons import som_pegar, som_corte, som_andar


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
        self.indicador = None
        self.controle_andar = None
        self.andando = False
        self.tempo_animacao = 0
        
        self.oscilacao = 0
        self.inclinacao = 0

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
        
    def atualizar_animacao(self):
        tempo = pygame.time.get_ticks() / 1000
        
        if self.andando:
            amplitude = 2
            frequencia = 12
            
        else:
            amplitude = 1
            frequencia = 3
            
        self.oscilacao = math.sin(tempo * frequencia) * amplitude

    def mover(self, colisoes):
        teclas_pressionadas = pygame.key.get_pressed()

        dirX = 0
        dirY = 0
        
        posicao_anterior_x = self.pos_x
        posicao_anterior_y = self.pos_y

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
        self.atualizar_animacao()

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
        
        self.andando = (self.pos_x != posicao_anterior_x or self.pos_y != posicao_anterior_y)

        if self.andando:
            if self.controle_andar is None or not self.controle_andar.get_busy():
                self.controle_andar = som_andar.play(loops=-1)
        elif self.controle_andar is not None:
            self.controle_andar.stop()
            self.controle_andar = None

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

        centro = (self.pos_x + 32,self.pos_y + 48 + self.oscilacao)

        sprite_rect = sprite.get_rect(center=centro)
        tela.blit(sprite, sprite_rect)

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
    
    def verificar_indicador(self, lixeiras, armarios, armarios_queijo,armarios_tomate, armarios_alface,geladeiras, tomates, alfaces,queijos, paos, carnes):
        area = self.area_interacao()
        encontrou = False

        for lista in (tomates, alfaces, queijos, paos, carnes):
            for item in lista:
                if item is None:
                    continue

                if item.dono is None and area.colliderect(item.rect):
                    encontrou = True
                    if self.indicador is None:
                        self.indicador = IndPegar(self)
                    break

            if encontrou:
                break

        if not encontrou:
            fontes = ((lixeiras, IndSoltar), (armarios, IndPegarPao),(armarios_queijo, IndPegarQueijo),(armarios_tomate, IndPegarTomate),(armarios_alface, IndPegarAlface),(geladeiras, IndPegarCarne))
            for lista, classe_indicador in fontes:
                for armario in lista:
                    if area.colliderect(armario.rect):
                        encontrou = True

                        if self.indicador is None:
                            self.indicador = classe_indicador(self)
                        break

                if encontrou:
                    break

        if not encontrou:
            self.indicador = None 
            
    def desenhar_indicador(self, tela):
        if self.indicador is not None:
            self.indicador.desenhar(tela)  

    def pegar(self, armarios, armarios_queijo, armarios_tomate, armarios_alface, geladeiras, tomates, alfaces, queijos, paos, carnes, montagens):
        
        area = self.area_interacao()

        if self.objeto:
            return
        
        for montagem in montagens:
            if area.colliderect(montagem.rect):
                ingredientes_montados = list(montagem.ingredientes)
                ingrediente = montagem.pegar_ingrediente()

                if ingrediente:
                    if ingrediente.nome == "Hamburguer":
                        for item_montado in ingredientes_montados:
                            for lista in (tomates, alfaces, queijos, paos, carnes):
                                if item_montado in lista:
                                    lista.remove(item_montado)
                                    break
                        paos.append(ingrediente)

                    ingrediente.dono = self
                    self.objeto = ingrediente
                    ingrediente.atualizar()
                    som_pegar.play()
                    
                    return

        for item in list(tomates):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                som_pegar.play()
                return
            
        for item in list(alfaces):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                som_pegar.play()
                return
            
        for item in list(queijos):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                som_pegar.play()
                return
            
        for item in list(paos):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                som_pegar.play()
                return
            
        for item in list(carnes):
            if item is None:
                continue
            if item.dono is None and area.colliderect(item.rect):
                item.dono = self
                self.objeto = item
                som_pegar.play()
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
                        som_corte.play()
                        return

            for item in alfaces:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        som_corte.play()
                        return

            for item in queijos:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        som_corte.play()
                        return

            for item in paos:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        som_corte.play()
                        return

            for item in carnes:
                if item and item.dono is None and item.corte and not item.cortado:
                    if item.rect.colliderect(tabua.rect):
                        item.cortar_ingrediente()
                        som_corte.play()
                        return


    def largar(self, lixeiras, tomates, alfaces, queijos, paos, carnes, montagens, entregas):
        if not self.objeto:
            return

        area = self.area_interacao()
        ingrediente = self.objeto
        
        for entrega in entregas:
            if area.colliderect(entrega.rect):

                if ingrediente.nome != "Hamburguer":
                    return None

                ingrediente.dono = None
                ingrediente.em_montagem = False

                if ingrediente in paos:
                    paos.remove(ingrediente)

                self.objeto = None

                return ingrediente

        coluna = area.centerx // TILE_SIZE
        linha = area.centery // TILE_SIZE

        for lix in lixeiras:
            if area.colliderect(lix.rect):
                for lista in (tomates, queijos, paos, carnes, alfaces):
                    if ingrediente in lista:
                        lista.remove(ingrediente)
                        break
                
                ingrediente.dono = None
                self.objeto = None
                return

                

        if linha < 0 or linha >= len(MAPA):
            return

        if coluna < 0 or coluna >= len(MAPA[linha]):
            return

        letra = MAPA[linha][coluna]
        
        if letra in ("1", "2", "3", "4"):
            for montagem in montagens:
                if montagem.rect.collidepoint(area.center):
                    if ingrediente.nome == "Hamburguer":
                        colocado = montagem.colocar_hamburguer(ingrediente)
                        if colocado and ingrediente in paos:
                            paos.remove(ingrediente)
                    else:
                        colocado = montagem.adicionar_ingrediente(ingrediente)

                    if colocado:
                        self.objeto = None

                    return

        if letra not in ("F", "B", "O"):
            return

        centro_x = coluna * TILE_SIZE + TILE_SIZE // 2
        centro_y = linha * TILE_SIZE + TILE_SIZE // 2

        ingrediente = self.objeto
        ingrediente.dono = None

        ingrediente.x = centro_x - ingrediente.rect.width // 2
        ingrediente.y = centro_y - ingrediente.rect.height // 2
        ingrediente.rect.topleft = (ingrediente.x, ingrediente.y)

        self.objeto = None

    def verificar_habilidades(self, evento, armarios, armarios_queijo, armarios_tomate,armarios_alface, geladeiras, tomates, alfaces, queijos,paos, carnes, lixeiras, montagens, entregas):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["pegar"]:
                self.pegar(armarios, armarios_queijo, armarios_tomate,armarios_alface, geladeiras, tomates,alfaces, queijos, paos, carnes, montagens)

            elif evento.key == self.teclas["largar"]:
                return self.largar(lixeiras, tomates, alfaces, queijos, paos, carnes, montagens, entregas)

    def verificar_cortagem(
        self, evento, tabuas, tomates, alfaces, queijos, paos, carnes
    ):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["cortar"]:
                self.cortar(
                    tabuas, tomates, alfaces, queijos, paos, carnes
                )


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
        super().__init__(
            x, y, os.path.join(PLAYER_DIR, "Romerio.png"), teclas
        )


class Brito(Personagem):
    def __init__(self, x, y):
        teclas = {
            "pegar": pygame.K_LSHIFT,
            "largar": pygame.K_LCTRL,
            "cortar": pygame.K_q,
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "cima": pygame.K_w,
            "baixo": pygame.K_s
        }
        super().__init__(
            x, y, os.path.join(PLAYER_DIR, "Brito.png"), teclas
        )

    def desenhar(self, tela):
        return super().desenhar(tela)
