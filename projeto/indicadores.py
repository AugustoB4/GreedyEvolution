from caminhos import PINS_DIR, pins_dir_estilo
from constantes import MARGEM, TAMANHO, ESPESSURA, CIANO
import pygame
import os

class Indicador:
    def __init__(self, alvo, nome, estilo="classico"):
        self.alvo = alvo
        self.nome = nome 
        self.estilo = estilo
        caminho = os.path.join(pins_dir_estilo(estilo),self.nome)

        self.sprite = pygame.image.load(caminho).convert_alpha()
        
    def desenhar_marcadores(self, tela):
        alvo = self.alvo.rect

        x = alvo.left - MARGEM
        y = alvo.top - MARGEM

        largura = alvo.width + MARGEM * 2
        altura = alvo.height + MARGEM * 2
        
        pygame.draw.circle(tela, (255, 255, 0), alvo.center, 2)
    
        pygame.draw.line(tela, CIANO, (x, y), (x + TAMANHO, y), ESPESSURA)
        pygame.draw.line(tela, CIANO, (x, y), (x, y + TAMANHO), ESPESSURA)

        pygame.draw.line(tela, CIANO, (x + largura - TAMANHO, y), (x + largura, y), ESPESSURA)
        pygame.draw.line(tela, CIANO, (x + largura, y), (x + largura, y + TAMANHO), ESPESSURA)

        pygame.draw.line(tela, CIANO, (x, y + altura - TAMANHO), (x, y + altura), ESPESSURA)
        pygame.draw.line(tela, CIANO, (x, y + altura), (x + TAMANHO, y + altura), ESPESSURA)

        pygame.draw.line(tela, CIANO, (x + largura - TAMANHO, y + altura), (x + largura, y + altura), ESPESSURA)
        pygame.draw.line(tela, CIANO, (x + largura, y + altura - TAMANHO), (x + largura, y + altura), ESPESSURA)
         
    def desenhar(self, tela):
        self.desenhar_marcadores(tela)
        
        self.posicaox = self.alvo.rect.centerx - self.sprite.get_width() // 2
        self.posicaoy = self.alvo.rect.top - 35 
        
        tela.blit(self.sprite, (self.posicaox, self.posicaoy))
        
class IndPegar(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "GrabPin.png", estilo)
        
class IndSoltar(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "ArrowPin.png", estilo)
        
class IndPegarPao(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "BreadPin.png", estilo)
        
        
class IndPegarQueijo(Indicador):
    def __init__(self, player,estilo="classico"):
        super().__init__(player, "CheesePin.png", estilo)
        
        
class IndPegarTomate(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "TomatoPin.png", estilo)
        
        
class IndPegarAlface(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "LettucePin.png", estilo)
        
        
class IndPegarCarne(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "MeatPin.png", estilo)
        
        
class IndJogarLixo(Indicador):
    def __init__(self, player, estilo="classico"):
        super().__init__(player, "TrashPin.png", estilo)
        
    