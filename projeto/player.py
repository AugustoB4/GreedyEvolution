import os
import pygame

import math
import random
from mapa import *
from itens import *
from constantes import *
from indicadores import *
from caminhos import PLAYER_DIR
from sons import som_pegar, som_corte, som_andar, som_solta


# Classe base
tomates = []
queijos = []
paos = []
carnes  = []
alfaces = []

CHANCE_ESCORREGAR = 0.05
DURACAO_ESCORREGAO_MS = 600

class Personagem:
    def __init__(self, x, y, sprite_path, walk_path, slip_path, teclas, estilo="classico"):

        self.pos_x = x
        self.pos_y = y
        self.teclas = teclas
        self.estilo = estilo
        self.velocidade = VELOCIDADE
        self.objeto = None
        self.indicador = None
        self.alvo_indicador = None
        self.controle_andar = None
        self.andando = False
        self.tempo_animacao = 0
        self.escorregando = False
        self.inicio_escorregao = None
        self._ingredientes_sob_os_pes = set()
        
        self.oscilacao = 0
        self.inclinacao = 0

        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha() #Idle
        self.sprite_walk = pygame.image.load(walk_path).convert_alpha()#Caminhada
        self.sprite_slip = pygame.image.load(slip_path).convert_alpha() #escorrego

        self.largura_sprite = (self.sprite_sheet.get_width() // 3)
        self.altura_sprite = (self.sprite_sheet.get_height())
        
        self.largura_walk = self.sprite_walk.get_width() // 8
        self.altura_walk = self.sprite_walk.get_height() // 3

        self.largura_slip = self.sprite_slip.get_width() // 6
        self.altura_slip = self.sprite_slip.get_height() // 3

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
        
    def caminhos_personagem(self, nome, estilo):
        pasta = (
            os.path.join(PLAYER_DIR, estilo)
            if estilo and estilo != "classico"
            else PLAYER_DIR
        )
        
        idle = os.path.join(pasta, f"{nome}.png")
        walk = os.path.join(pasta, f"{nome}_Walk.png")
        slip = os.path.join(pasta, f"{nome}_Slip.png")

        return idle, walk, slip
        
    def atualizar_animacao(self):
        tempo = pygame.time.get_ticks() / 1000
        
        if self.andando:
            amplitude = 2
            frequencia = 12
            
        else:
            amplitude = 1
            frequencia = 3
            
        self.oscilacao = math.sin(tempo * frequencia) * amplitude

    def _atualizar_estado_escorregao(self):
        if not getattr(self, "escorregando", False):
            return False

        agora = pygame.time.get_ticks()
        if agora - self.inicio_escorregao < DURACAO_ESCORREGAO_MS:
            self.andando = False
            self.oscilacao = 0
            self.parar_som_andar()
            return True

        self.escorregando = False
        self.inicio_escorregao = None
        self.andando = False
        return False

    def _verificar_escorregao(self, ingredientes_chao, movimento):
        sobrepostos = {
            id(ingrediente)
            for ingrediente in ingredientes_chao or ()
            if ingrediente is not None
            and getattr(ingrediente, "dono", None) is None
            and not getattr(ingrediente, "em_montagem", False)
            and self.rect.colliderect(ingrediente.rect)
        }
        novos = sobrepostos - self._ingredientes_sob_os_pes

        if movimento:
            for identificador in novos:
                if random.random() < CHANCE_ESCORREGAR:
                    self.escorregando = True
                    self.inicio_escorregao = pygame.time.get_ticks()
                    self.andando = False
                    self.oscilacao = 0
                    self.parar_som_andar()
                    break

        self._ingredientes_sob_os_pes = sobrepostos

    def atualizar_direcao(self, teclas_pressionadas):
        if getattr(self, "escorregando", False):
            return

        if teclas_pressionadas[self.teclas["esquerda"]]:
            self.direcao = "lado"
            self.virado_esquerda = False

        if teclas_pressionadas[self.teclas["direita"]]:
            self.direcao = "lado"
            self.virado_esquerda = True

        if teclas_pressionadas[self.teclas["cima"]]:
            self.direcao = "costas"

        if teclas_pressionadas[self.teclas["baixo"]]:
            self.direcao = "frente"

    def mover(self, colisoes, ingredientes_chao=None):
        if self._atualizar_estado_escorregao():
            self._verificar_escorregao(ingredientes_chao, False)
            return

        teclas_pressionadas = pygame.key.get_pressed()

        dirX = 0
        dirY = 0

        posicao_anterior_x = self.pos_x
        posicao_anterior_y = self.pos_y

        self.atualizar_direcao(teclas_pressionadas)

        if teclas_pressionadas[self.teclas["esquerda"]]:
            dirX = -self.velocidade

        if teclas_pressionadas[self.teclas["direita"]]:
            dirX = self.velocidade

        if teclas_pressionadas[self.teclas["cima"]]:
            dirY = -self.velocidade

        if teclas_pressionadas[self.teclas["baixo"]]:
            dirY = self.velocidade

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

        self._verificar_escorregao(ingredientes_chao, self.andando)

    def parar_som_andar(self):
        if self.controle_andar is not None:
            self.controle_andar.stop()
            self.controle_andar = None

    def desenhar(self, tela):
        if getattr(self, "escorregando", False):
            decorrido = pygame.time.get_ticks() - self.inicio_escorregao
            coluna = min(
                5,
                max(0, decorrido * 6 // DURACAO_ESCORREGAO_MS),
            )
            linha = self.frames[self.direcao]
            area = pygame.Rect(
                coluna * self.largura_slip,
                linha * self.altura_slip,
                self.largura_slip,
                self.altura_slip,
            )
            sprite = self.sprite_slip.subsurface(area)

        elif self.andando:

            coluna = (pygame.time.get_ticks() // 100) % 8
            linha = self.frames[self.direcao]

            area = pygame.Rect(coluna * self.largura_walk, linha * self.altura_walk, self.largura_walk, self.altura_walk)
            sprite = self.sprite_walk.subsurface(area)

        else:
            indice = self.frames[self.direcao]

            area = pygame.Rect(indice * self.largura_sprite, 0, self.largura_sprite, self.altura_sprite)

            sprite = self.sprite_sheet.subsurface(area)

        if self.virado_esquerda:
            sprite = pygame.transform.flip(sprite, True, False)

        sprite = pygame.transform.scale(sprite, (64, 96))
        centro = (self.pos_x + 32,self.pos_y + 48 + self.oscilacao)

        sprite_rect = sprite.get_rect(center=centro)
        tela.blit(sprite, sprite_rect)

    def area_interacao(self):
        coluna = self.rect.centerx // TILE_SIZE
        linha = self.rect.centery // TILE_SIZE

        if self.direcao == "frente":
            linha += 1
        elif self.direcao == "costas":
            linha -= 1
        elif self.direcao == "lado":
            coluna += 1 if self.virado_esquerda else -1

        return pygame.Rect(
            coluna * TILE_SIZE,
            linha * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )
    
    def verificar_indicador(
        self, lixeiras, armarios, armarios_queijo, armarios_tomate,
        armarios_alface, geladeiras, tomates, alfaces, queijos, paos, carnes,
        dispensadores_tematicos=None, ingredientes_tematicos=None,
        produtos=None, montagens=None, entregas=None,
    ):
        area = self.area_interacao()
        encontrou = False
        alvo = None

        if getattr(self, "escorregando", False):
            self.indicador = None
            self.alvo_indicador = None
            return

        if self.objeto is not None:
            for lixeira in lixeiras:
                if area.colliderect(lixeira.rect):
                    self.indicador = IndSoltar(lixeira, self.estilo)
                    self.alvo_indicador = lixeira
                    return

            for montagem in montagens or ():
                if not area.colliderect(montagem.rect):
                    continue

                produto = getattr(montagem, "produto", None)
                if produto is None:
                    produto = getattr(montagem, "hamburguer", None)
                ingredientes = montagem.ingredientes
                if isinstance(self.objeto, ProdutoFinal) or getattr(
                    self.objeto, "nome", None
                ) == "Hamburguer":
                    aceita = produto is None and not ingredientes
                else:
                    aceita = (
                        produto is None
                        and len(ingredientes) < 5
                        and self.objeto not in ingredientes
                    )

                if aceita:
                    self.indicador = IndSoltar(montagem, self.estilo)
                    self.alvo_indicador = montagem
                    return

            produto_final = isinstance(self.objeto, ProdutoFinal) or getattr(
                self.objeto, "nome", None
            ) == "Hamburguer"
            if produto_final:
                for entrega in entregas or ():
                    if area.colliderect(entrega.rect):
                        self.indicador = IndSoltar(entrega, self.estilo)
                        self.alvo_indicador = entrega
                        return

            self.indicador = None
            self.alvo_indicador = None
            return

        for montagem in montagens or ():
            if not area.colliderect(montagem.rect):
                continue
            produto = getattr(montagem, "produto", None)
            if produto is None:
                produto = getattr(montagem, "hamburguer", None)
            if not (
                produto is not None
                or montagem.ingredientes
                or montagem.produto_pronto
            ):
                continue
            self.indicador = IndPegar(montagem, self.estilo)
            self.alvo_indicador = montagem
            return

        for lista in (tomates, alfaces, queijos, paos, carnes):
            for item in lista:
                if item is None:
                    continue

                if (
                    item.dono is None
                    and not getattr(item, "em_montagem", False)
                    and area.colliderect(item.rect)
                ):
                    encontrou = True
                    alvo = item
                    if self.indicador is None or not isinstance(self.indicador, IndPegar):
                        self.indicador = IndPegar(item, self.estilo)
                    else:
                        self.indicador.alvo = item
                    break

            if encontrou:
                break

        if not encontrou:
            fontes = ((lixeiras, IndSoltar), (armarios, IndPegarPao),(armarios_queijo, IndPegarQueijo),(armarios_tomate, IndPegarTomate),(armarios_alface, IndPegarAlface),(geladeiras, IndPegarCarne))
            for lista, classe_indicador in fontes:
                for armario in lista:
                    if area.colliderect(armario.rect):
                        encontrou = True
                        alvo = armario
                        
                        if self.indicador is None or not isinstance(self.indicador, classe_indicador):
                            self.indicador = classe_indicador(armario, self.estilo)
                        else:
                            self.indicador.alvo = armario
                            
                        break

                if encontrou:
                    break

        if not encontrou:
            listas_tematicas = list((ingredientes_tematicos or {}).values())
            if produtos is not None:
                listas_tematicas.append(produtos)
            for lista in listas_tematicas:
                for item in lista:
                    if (
                        item.dono is None
                        and not getattr(item, "em_montagem", False)
                        and area.colliderect(item.rect)
                    ):
                        encontrou = True
                        alvo = item
                        if self.indicador is None or not isinstance(
                            self.indicador, IndPegar
                        ):
                            self.indicador = IndPegar(item, self.estilo)
                        else:
                            self.indicador.alvo = item
                        break
                if encontrou:
                    break

        if not encontrou:
            for dispensador in dispensadores_tematicos or ():
                if not area.colliderect(dispensador.rect):
                    continue
                encontrou = True
                alvo = dispensador
                if (
                    self.indicador is None
                    or not isinstance(self.indicador, Indicador)
                    or self.indicador.nome != dispensador.pin
                ):
                    self.indicador = Indicador(
                        dispensador, dispensador.pin, self.estilo
                    )
                else:
                    self.indicador.alvo = dispensador
                break

        self.alvo_indicador = alvo
        
        if not encontrou:
            self.indicador = None 
            
    def desenhar_indicador(self, tela):
        if self.indicador is not None:
            self.indicador.desenhar(tela)  

    def pegar(
        self, armarios, armarios_queijo, armarios_tomate, armarios_alface,
        geladeiras, tomates, alfaces, queijos, paos, carnes, montagens,
        dispensadores_tematicos=None, ingredientes_tematicos=None,
        produtos=None,
    ):
        
        area = self.area_interacao()

        if self.objeto:
            return
        
        for montagem in montagens:
            if area.colliderect(montagem.rect):
                ingredientes_montados = list(montagem.ingredientes)
                ingrediente = montagem.pegar_ingrediente()

                if ingrediente:
                    if isinstance(ingrediente, ProdutoFinal) or ingrediente.nome == "Hamburguer":
                        for item_montado in ingredientes_montados:
                            listas = [tomates, alfaces, queijos, paos, carnes]
                            listas.extend((ingredientes_tematicos or {}).values())
                            for lista in listas:
                                if item_montado in lista:
                                    lista.remove(item_montado)
                                    break
                        if isinstance(ingrediente, Hamburguer):
                            paos.append(ingrediente)
                        elif produtos is not None:
                            produtos.append(ingrediente)

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

        listas_tematicas = list((ingredientes_tematicos or {}).values())
        if produtos is not None:
            listas_tematicas.append(produtos)
        for lista in listas_tematicas:
            for item in list(lista):
                if item is None:
                    continue
                if item.dono is None and area.colliderect(item.rect):
                    item.dono = self
                    self.objeto = item
                    item.atualizar()
                    som_pegar.play()
                    return

        for armario_tomate in armarios_tomate:
            if area.colliderect(armario_tomate.rect):
                tomate_do_armario = Tomate(armario_tomate.posX, armario_tomate.posY)
                tomate_do_armario.dono = self
                self.objeto = tomate_do_armario
                tomates.append(tomate_do_armario)
                som_pegar.play()
                return
            
        for armario_alface in armarios_alface:
            if area.colliderect(armario_alface.rect):
                alface_do_armario = Alface(armario_alface.posX, armario_alface.posY)
                alface_do_armario.dono = self
                self.objeto = alface_do_armario
                alfaces.append(alface_do_armario)
                som_pegar.play()
                return

        for armario_queijo in armarios_queijo:
            if area.colliderect(armario_queijo.rect):
                queijo_do_armario = Queijo(armario_queijo.posX, armario_queijo.posY)
                queijo_do_armario.dono = self
                self.objeto = queijo_do_armario 
                queijos.append(queijo_do_armario)
                som_pegar.play()
                return
            
        for armario in armarios:
            if area.colliderect(armario.rect):
                pao_do_armario = Pao(armario.posX, armario.posY)
                pao_do_armario.dono = self
                self.objeto = pao_do_armario
                paos.append(pao_do_armario)
                som_pegar.play()
                return

        for geladeira in geladeiras:
            if area.colliderect(geladeira.rect):
                carne_da_geladeira = Carne(geladeira.posX, geladeira.posY)
                carne_da_geladeira.dono = self
                self.objeto = carne_da_geladeira
                carnes.append(carne_da_geladeira)
                som_pegar.play()
                return

        for dispensador in dispensadores_tematicos or ():
            if not area.colliderect(dispensador.rect):
                continue

            ingrediente = dispensador.classe_ingrediente(
                dispensador.posX, dispensador.posY
            )
            ingrediente.dono = self
            self.objeto = ingrediente
            if ingredientes_tematicos is not None:
                ingredientes_tematicos.setdefault(
                    dispensador.nome_ingrediente, []
                ).append(ingrediente)
            som_pegar.play()
            return

    def cortar(
        self, tabuas, tomates, alfaces, queijos, paos, carnes,
        ingredientes_tematicos=None,
    ):
        if getattr(self, "escorregando", False):
            return

        area = self.area_interacao()

        for tabua in tabuas:
            if not area.colliderect(tabua.rect):
                continue

            if self.objeto:
                if self.objeto.corte and not self.objeto.cortado:
                    self.objeto.cortar_ingrediente()
                    som_corte.play()
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

            for lista in (ingredientes_tematicos or {}).values():
                for item in lista:
                    if item and item.dono is None and item.corte and not item.cortado:
                        if item.rect.colliderect(tabua.rect):
                            item.cortar_ingrediente()
                            som_corte.play()
                            return


    def largar(
        self, lixeiras, tomates, alfaces, queijos, paos, carnes, montagens,
        entregas, mapa_atual, ingredientes_tematicos=None, produtos=None,
    ):
        if not self.objeto:
            return

        area = self.area_interacao()
        ingrediente = self.objeto
        
        for entrega in entregas:
            if area.colliderect(entrega.rect):

                if not (
                    isinstance(ingrediente, ProdutoFinal)
                    or getattr(ingrediente, "nome", None) == "Hamburguer"
                ):
                    return None

                ingrediente.dono = None
                ingrediente.em_montagem = False

                listas_objetos = [tomates, alfaces, queijos, paos, carnes]
                listas_objetos.extend((ingredientes_tematicos or {}).values())
                if produtos is not None:
                    listas_objetos.append(produtos)
                for lista in listas_objetos:
                    if ingrediente in lista:
                        lista.remove(ingrediente)
                        break
                
                som_solta.play()
                self.objeto = None
                return ingrediente
              

        coluna = area.centerx // TILE_SIZE
        linha = area.centery // TILE_SIZE

        for lix in lixeiras:
            if area.colliderect(lix.rect):
                listas_objetos = [tomates, queijos, paos, carnes, alfaces]
                listas_objetos.extend((ingredientes_tematicos or {}).values())
                if produtos is not None:
                    listas_objetos.append(produtos)
                for lista in listas_objetos:
                    if ingrediente in lista:
                        lista.remove(ingrediente)
                        break
                
                ingrediente.dono = None
                som_solta.play()
                self.objeto = None
                return

                

        if linha < 0 or linha >= len(mapa_atual):
            return

        if coluna < 0 or coluna >= len(mapa_atual[linha]):
            return

        letra = mapa_atual[linha][coluna]

        for montagem in montagens:
            if not montagem.rect.collidepoint(area.center):
                continue

            if isinstance(ingrediente, ProdutoFinal) or getattr(
                ingrediente, "nome", None
            ) == "Hamburguer":
                if hasattr(montagem, "colocar_produto"):
                    colocado = montagem.colocar_produto(ingrediente, letra)
                else:
                    colocado = montagem.colocar_hamburguer(ingrediente, letra)
                listas_produtos = [paos]
                if produtos is not None:
                    listas_produtos.append(produtos)
                if colocado:
                    for lista in listas_produtos:
                        if ingrediente in lista:
                            lista.remove(ingrediente)
                            break
            else:
                colocado = montagem.adicionar_ingrediente(ingrediente, letra)

            if colocado:
                som_solta.play()
                self.objeto = None
            return

        ingredientes = [tomates, paos, carnes, queijos, alfaces]
        ingredientes.extend((ingredientes_tematicos or {}).values())
        if produtos is not None:
            ingredientes.append(produtos)
        for lista in ingredientes:
            for ingrediente in lista:
                if ingrediente is None or ingrediente.dono is not None:
                    continue

                coluna_ingrediente = ingrediente.rect.centerx // TILE_SIZE
                linha_ingrediente = ingrediente.rect.centery // TILE_SIZE

                if coluna_ingrediente == coluna and linha_ingrediente == linha:
                    return

        if letra not in ("F", "B", "O"):
            return

        centro_x = coluna * TILE_SIZE + TILE_SIZE // 2
        centro_y = linha * TILE_SIZE + TILE_SIZE // 2
        
        if letra in ("O", "B"):
            centro_y -= 18

        ingrediente = self.objeto
        ingrediente.dono = None

        ingrediente.x = centro_x - ingrediente.rect.width // 2
        ingrediente.y = centro_y - ingrediente.rect.height // 2
        ingrediente.rect.topleft = (ingrediente.x, ingrediente.y)

        som_solta.play()
        self.objeto = None

    def verificar_habilidades(
        self, evento, armarios, armarios_queijo, armarios_tomate,
        armarios_alface, geladeiras, tomates, alfaces, queijos, paos,
        carnes, lixeiras, montagens, entregas, mapa_atual,
        dispensadores_tematicos=None, ingredientes_tematicos=None,
        produtos=None,
    ):
        if getattr(self, "escorregando", False):
            return None

        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["pegar"]:
                self.pegar(
                    armarios, armarios_queijo, armarios_tomate,
                    armarios_alface, geladeiras, tomates, alfaces,
                    queijos, paos, carnes, montagens,
                    dispensadores_tematicos, ingredientes_tematicos,
                    produtos,
                )

            elif evento.key == self.teclas["largar"]:
                return self.largar(
                    lixeiras, tomates, alfaces, queijos, paos, carnes,
                    montagens, entregas, mapa_atual,
                    ingredientes_tematicos, produtos,
                )

    def verificar_cortagem(
        self, evento, tabuas, tomates, alfaces, queijos, paos, carnes,
        ingredientes_tematicos=None,
    ):
        if getattr(self, "escorregando", False):
            return

        if evento.type == pygame.KEYDOWN:
            if evento.key == self.teclas["cortar"]:
                self.cortar(
                    tabuas, tomates, alfaces, queijos, paos, carnes,
                    ingredientes_tematicos,
                )


class Romerio(Personagem):
    def __init__(self, x, y, estilo="classico"):
        teclas = {
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN,
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "pegar": pygame.K_KP1,
            "largar": pygame.K_KP2,
            "cortar": pygame.K_KP3
        }
        
        idle, walk, slip = self.caminhos_personagem("Romerio", estilo)
        super().__init__(x, y, idle, walk, slip, teclas, estilo)


class Brito(Personagem):
    def __init__(self, x, y, estilo="classico"):
        teclas = {
            "cima": pygame.K_w,
            "baixo": pygame.K_s,
            "esquerda": pygame.K_a,
            "direita": pygame.K_d,
            "pegar": pygame.K_z,
            "largar": pygame.K_x,
            "cortar": pygame.K_c
        }
        
        idle, walk, slip = self.caminhos_personagem("Brito", estilo)
        super().__init__(x, y, idle, walk, slip, teclas, estilo)

    def desenhar(self, tela):
        return super().desenhar(tela)
