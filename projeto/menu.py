
import os
import pygame

from caminhos import BACKGROUND_DIR, UI_DIR
from sons import som_botoes


class Menu:
    ESCALA_TITULO = 7
    ESCALA_BOTAO = 4

    CONFIGURACOES = {
        "inicio": {
            "titulo": "GameTittle.png",
            "botoes": [
                ("start", "ButtonStart.png"),
                ("quit", "ButtonQuit.png")
            ]
        },

        "gameover": {
            "titulo": "GameOver.png",
            "botoes": [
                ("retry", "ButtonRetry.png"),
                ("quit", "ButtonQuit.png")
            ]
        },

        "gamewin": {
            "titulo": "GameWin.png",
            "botoes": [
                ("continue", "ButtonContinue.png"),
                ("retry", "ButtonRetry.png"),
                ("quit", "ButtonQuit.png")
            ]
        }
    }

    def __init__(self, tela, largura, altura, tipo="inicio"):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.tipo = tipo

        self.background = pygame.image.load(os.path.join(BACKGROUND_DIR, "StartMenuBG.png")).convert()
        self.background = pygame.transform.scale(self.background, (largura, altura))

        self.botoes = []

        self.montar_interface()

    def montar_interface(self):
        configuracao = self.CONFIGURACOES[self.tipo]
        caminho_titulo = os.path.join(UI_DIR, configuracao["titulo"])
        self.titulo = pygame.image.load(caminho_titulo).convert_alpha()
        self.titulo = pygame.transform.scale_by(self.titulo, self.ESCALA_TITULO)
        self.titulo_rect = self.titulo.get_rect(center=(self.largura // 2, 150))
        quantidade = len(configuracao["botoes"])

        if quantidade == 2:
            posicoes_y = [350, 460]

        else:
            posicoes_y = [300, 400, 500]

        for i, (acao, arquivo) in enumerate(configuracao["botoes"]):
            botao = self.criar_botao(arquivo, acao, posicoes_y[i])
            self.botoes.append(botao)

    def criar_botao(self, arquivo, acao, posicao_y):
        caminho = os.path.join(UI_DIR, arquivo)
        spritesheet = pygame.image.load(caminho).convert_alpha()

        largura, altura = spritesheet.get_size()
        largura_metade = largura // 2

        normal = spritesheet.subsurface(pygame.Rect(0, 0, largura_metade, altura)).copy()
        hover = spritesheet.subsurface(pygame.Rect(largura_metade, 0, largura_metade, altura)).copy()

        tamanho = (largura_metade * self.ESCALA_BOTAO, altura * self.ESCALA_BOTAO)

        normal = pygame.transform.scale(normal, tamanho)
        hover = pygame.transform.scale(hover, tamanho)

        rect = normal.get_rect(center=(self.largura // 2, posicao_y))

        return {"acao": acao, "normal": normal, "hover": hover, "rect": rect}

    def desenhar(self):
        posicao_mouse = pygame.mouse.get_pos()

        self.tela.blit(self.background, (0, 0))
        self.tela.blit(self.titulo, self.titulo_rect)

        for botao in self.botoes:
            if botao["rect"].collidepoint(posicao_mouse):
                imagem = botao["hover"]

            else:
                imagem = botao["normal"]
            self.tela.blit(imagem, botao["rect"])
        pygame.display.flip()

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "quit"

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for botao in self.botoes:
                        if botao["rect"].collidepoint(evento.pos):
                            som_botoes.play()
                            return botao["acao"]

            self.desenhar()
