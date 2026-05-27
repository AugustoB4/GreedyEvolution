import pygame
import sys
from constantes import*
from player import Romerio, Brito
# Inicialização do pygame 
pygame.init()
tela = pygame.display.set.mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu jogo")
relogio = pygame.time.Clock()

# Instancia os jogadores a partir do outro arquivo
romerito = Romerio(200,300)
brito = Brito(600, 300)

# loop principal do jogo
while True:
    # 1 Evento
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # 2 movimentação
    romerito.mover()
    brito.mover() 
    
    tela.fill("PRETO")
    
    romerito.desenhar(tela)
    brito.desenhar(tela)
    
    pygame.display.flip()
    relogio.tick(60)
        




 



