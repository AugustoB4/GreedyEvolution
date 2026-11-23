"""Telas de selecao de campanha, mini tutorial e resultado de fase."""

import os
import pygame

from campanha import FASES_CAMPANHA, FASES_POR_GALAXIA, GALAXIAS, TOTAL_FASES
from caminhos import BACKGROUND_DIR, FASES_DIR, FONTS_DIR, TUTORIALS_DIR, UI_DIR


ARTES_GALAXIAS = {
    1: "galaxia_1_cozinha_classica.png",
    2: "galaxia_2_pizzaria.png",
    3: "galaxia_3_reator.png",
    4: "galaxia_4_em_construcao.png",
    5: "galaxia_5_em_construcao.png",
}

PAINEIS_TUTORIAL = {
    1: "painel_receita_1_hamburguer.png",
    2: "painel_receita_2_pizza.png",
    3: "painel_receita_3_sushi.png",
}


class InterfaceCampanha:
    LARGURA_CARD_GALAXIA = 168
    ALTURA_CARD_GALAXIA = 205

    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(BACKGROUND_DIR, "StartMenuBG.png")).convert(),
            (largura, altura),
        )
        self.fonte_titulo = pygame.font.Font(
            os.path.join(FONTS_DIR, "Orbitron.ttf"), 25
        )
        self.fonte_texto = pygame.font.Font(
            os.path.join(FONTS_DIR, "PressStart2P.ttf"), 9
        )
        self.fonte_pequena = pygame.font.Font(
            os.path.join(FONTS_DIR, "PressStart2P.ttf"), 7
        )
        self.imagens_galaxia = {
            numero: pygame.image.load(os.path.join(FASES_DIR, nome)).convert_alpha()
            for numero, nome in ARTES_GALAXIAS.items()
        }
        self.imagens_tutorial = {
            numero: pygame.image.load(os.path.join(TUTORIALS_DIR, nome)).convert_alpha()
            for numero, nome in PAINEIS_TUTORIAL.items()
        }
        self.imagem_vitoria = pygame.image.load(
            os.path.join(UI_DIR, "GameWin.png")
        ).convert_alpha()
        self.imagem_derrota = pygame.image.load(
            os.path.join(UI_DIR, "GameOver.png")
        ).convert_alpha()
        self.imagens_botoes_resultado = {
            "avancar": self._carregar_frames_botao_resultado("ButtonContinue.png"),
            "repetir": self._carregar_frames_botao_resultado("ButtonRetry.png"),
            "campanha": self._carregar_frames_botao_resultado("ButtonQuit.png"),
        }
        self.galaxia_selecionada = 1
        self.rects_galaxias = {}
        self.rects_fases = {}
        self.rects_botoes_resultado = {}
        self.rect_voltar = pygame.Rect(35, altura - 53, 190, 38)

    def _carregar_frames_botao_resultado(self, nome):
        spritesheet = pygame.image.load(
            os.path.join(UI_DIR, nome)
        ).convert_alpha()
        if spritesheet.get_width() % 2:
            raise ValueError(f"Spritesheet de botão inválido: {nome}")

        largura_frame = spritesheet.get_width() // 2
        altura_frame = spritesheet.get_height()
        tamanho = (largura_frame * 2, altura_frame * 2)
        return tuple(
            pygame.transform.scale(
                spritesheet.subsurface(
                    pygame.Rect(indice * largura_frame, 0, largura_frame, altura_frame)
                ).copy(),
                tamanho,
            )
            for indice in range(2)
        )

    def _desenhar_botao_resultado(self, acao, rect, hover=False):
        imagem = self.imagens_botoes_resultado[acao][1 if hover else 0]
        self.tela.blit(imagem, rect)

    def _texto_centralizado(self, texto, fonte, cor, y, destino=None):
        destino = self.tela if destino is None else destino
        imagem = fonte.render(texto, True, cor)
        destino.blit(imagem, imagem.get_rect(center=(destino.get_width() // 2, y)))
        return imagem

    def _botao(self, rect, texto, ativo=True, hover=False):
        if ativo:
            cor_fundo = (42, 73, 105) if not hover else (61, 105, 142)
            cor_borda = (111, 225, 232)
            cor_texto = (255, 255, 255)
        else:
            cor_fundo = (32, 35, 48)
            cor_borda = (80, 83, 96)
            cor_texto = (150, 151, 160)
        pygame.draw.rect(self.tela, cor_fundo, rect, border_radius=5)
        pygame.draw.rect(self.tela, cor_borda, rect, width=2, border_radius=5)
        imagem = self.fonte_pequena.render(texto, True, cor_texto)
        self.tela.blit(imagem, imagem.get_rect(center=rect.center))

    def desenhar_selecao(self, progresso):
        self.tela.blit(self.background, (0, 0))
        self._texto_centralizado(
            "CAMPANHA ESPACIAL", self.fonte_titulo, (255, 255, 255), 27
        )
        self.rects_galaxias = {}
        mouse = pygame.mouse.get_pos()

        margem = 42
        espacamento = (self.largura - margem * 2 - self.LARGURA_CARD_GALAXIA * 5) // 4
        for numero in range(1, 6):
            x = margem + (numero - 1) * (self.LARGURA_CARD_GALAXIA + espacamento)
            rect = pygame.Rect(x, 49, self.LARGURA_CARD_GALAXIA, self.ALTURA_CARD_GALAXIA)
            self.rects_galaxias[numero] = rect
            disponivel = numero <= 3 and progresso.galaxia_desbloqueada(numero)
            selecionavel = numero <= 3 and progresso.galaxia_desbloqueada(numero)
            fundo = (20, 25, 43) if numero != self.galaxia_selecionada else (34, 55, 77)
            pygame.draw.rect(self.tela, fundo, rect, border_radius=7)
            borda = (113, 224, 230) if numero == self.galaxia_selecionada else (89, 101, 120)
            pygame.draw.rect(self.tela, borda, rect, width=2, border_radius=7)

            imagem = self.imagens_galaxia[numero]
            tamanho = 132
            escala = pygame.transform.smoothscale(imagem, (tamanho, tamanho))
            self.tela.blit(escala, (x + (rect.width - tamanho) // 2, 56))

            if numero <= 3 and not disponivel:
                sobreposicao = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
                sobreposicao.fill((0, 0, 0, 145))
                self.tela.blit(sobreposicao, (x + (rect.width - tamanho) // 2, 56))

            texto_galaxia = self.fonte_pequena.render(
                f"GALÁXIA {numero}", True, (245, 245, 255)
            )
            self.tela.blit(
                texto_galaxia,
                texto_galaxia.get_rect(center=(rect.centerx, 201)),
            )
            # Desenha os nomes dentro de cada cartao sem depender de novo recurso visual.
            if numero <= 3:
                nome = GALAXIAS[numero - 1].nome.upper()
                status = "JOGÁVEL" if disponivel else "BLOQUEADA"
                quantidade_fases = f"{len(FASES_POR_GALAXIA[numero])} FASES"
            else:
                nome = "REGIÃO FUTURA"
                status = "EM CONSTRUÇÃO"
                quantidade_fases = "NÃO JOGÁVEL"
            linhas = (nome, status, quantidade_fases)
            for indice_linha, linha in enumerate(linhas):
                texto = self.fonte_pequena.render(linha, True, (220, 225, 235))
                self.tela.blit(
                    texto,
                    texto.get_rect(center=(rect.centerx, 220 + indice_linha * 13)),
                )

            if selecionavel and rect.collidepoint(mouse):
                pygame.draw.rect(self.tela, (255, 232, 132), rect, width=2, border_radius=7)

        fases_galaxia = FASES_POR_GALAXIA[self.galaxia_selecionada]
        nome_galaxia = GALAXIAS[self.galaxia_selecionada - 1].nome.upper()
        self._texto_centralizado(
            f"{nome_galaxia} — FASES", self.fonte_texto, (255, 255, 255), 276
        )

        self.rects_fases = {}
        largura_fase = 164
        altura_fase = 115
        espacamento_fase = 16
        quantidade = len(fases_galaxia)
        largura_total = quantidade * largura_fase + (quantidade - 1) * espacamento_fase
        inicio_x = (self.largura - largura_total) // 2
        for indice_local, fase in enumerate(fases_galaxia):
            rect = pygame.Rect(
                inicio_x + indice_local * (largura_fase + espacamento_fase),
                296,
                largura_fase,
                altura_fase,
            )
            self.rects_fases[fase.indice] = rect
            desbloqueada = progresso.fase_desbloqueada(fase.numero)
            hover = rect.collidepoint(mouse)
            self._botao(rect, "", ativo=desbloqueada, hover=hover)
            linhas = (
                f"FASE {fase.fase_na_galaxia}",
                fase.dificuldade.upper(),
                f"ESTRELAS {progresso.melhor_classificacao(fase.numero)}/3",
                "DISPONÍVEL" if desbloqueada else "BLOQUEADA",
            )
            for indice_linha, linha in enumerate(linhas):
                cor = (255, 255, 255) if desbloqueada else (156, 157, 166)
                texto = self.fonte_pequena.render(linha, True, cor)
                self.tela.blit(
                    texto,
                    texto.get_rect(center=(rect.centerx, rect.y + 21 + indice_linha * 21)),
                )

        total = progresso.total_estrelas()
        self._texto_centralizado(
            f"PROGRESSO: {total}/{TOTAL_FASES * 3} ESTRELAS  |  "
            f"{progresso.percentual_campanha()}%",
            self.fonte_pequena,
            (220, 226, 236),
            450,
        )
        if progresso.dados["campanha_concluida"]:
            self._texto_centralizado(
                "CAMPANHA EXPOTEC CONCLUÍDA",
                self.fonte_pequena,
                (255, 226, 115),
                478,
            )
        if progresso.erro_salvamento:
            self._texto_centralizado(
                "AVISO: O PROGRESSO NÃO PÔDE SER SALVO",
                self.fonte_pequena,
                (255, 155, 135),
                503,
            )

        self._botao(self.rect_voltar, "VOLTAR AO MENU", hover=self.rect_voltar.collidepoint(mouse))
        pygame.display.flip()

    def executar_selecao(self, progresso):
        while True:
            self.desenhar_selecao(progresso)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair", None
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    return "menu", None
                if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
                    continue
                if self.rect_voltar.collidepoint(evento.pos):
                    return "menu", None
                for numero, rect in self.rects_galaxias.items():
                    if rect.collidepoint(evento.pos):
                        if numero <= 3 and progresso.galaxia_desbloqueada(numero):
                            self.galaxia_selecionada = numero
                        break
                else:
                    for indice, rect in self.rects_fases.items():
                        if rect.collidepoint(evento.pos):
                            numero_fase = FASES_CAMPANHA[indice].numero
                            if progresso.fase_desbloqueada(numero_fase):
                                return "fase", indice
                            break

    def executar_tutorial(self, numero_galaxia):
        imagem = self.imagens_tutorial[numero_galaxia]
        largura_original, altura_original = imagem.get_size()
        fator = min((self.largura - 80) / largura_original, 0.88 * self.altura / altura_original)
        tamanho = (
            max(1, round(largura_original * fator)),
            max(1, round(altura_original * fator)),
        )
        imagem_escalada = pygame.transform.smoothscale(imagem, tamanho)
        posicao = (
            (self.largura - tamanho[0]) // 2,
            max(15, (self.altura - tamanho[1] - 70) // 2),
        )
        botoes = [
            ("iniciar", "COMEÇAR A FASE", pygame.Rect(self.largura // 2 - 250, self.altura - 53, 230, 38)),
            ("campanha", "VOLTAR À CAMPANHA", pygame.Rect(self.largura // 2 + 20, self.altura - 53, 230, 38)),
        ]

        while True:
            self.tela.blit(self.background, (0, 0))
            self.tela.blit(imagem_escalada, posicao)
            mouse = pygame.mouse.get_pos()
            for _, texto, rect in botoes:
                self._botao(rect, texto, hover=rect.collidepoint(mouse))
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "iniciar"
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    return "campanha"
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for acao, _, rect in botoes:
                        if rect.collidepoint(evento.pos):
                            return acao

    def executar_resultado(
        self,
        definicao,
        pontuacao,
        tempo_restante,
        estrelas,
        melhor_classificacao,
        venceu,
        proxima_desbloqueada,
        campanha_concluida,
        erro_salvamento=None,
    ):
        titulo = self.imagem_vitoria if venceu else self.imagem_derrota
        titulo_largura = min(titulo.get_width(), self.largura - 80)
        titulo_altura = round(titulo.get_height() * titulo_largura / titulo.get_width())
        titulo_escalado = (
            titulo
            if titulo.get_size() == (titulo_largura, titulo_altura)
            else pygame.transform.scale(
                titulo, (titulo_largura, titulo_altura)
            )
        )
        botoes = []
        pode_avancar = (
            venceu
            and proxima_desbloqueada
            and not campanha_concluida
            and not erro_salvamento
        )
        if pode_avancar:
            botoes.append("avancar")
        botoes.extend(("repetir", "campanha"))

        espacamento = 18
        larguras_botoes = [
            self.imagens_botoes_resultado[acao][0].get_width()
            for acao in botoes
        ]
        altura_botoes = max(
            self.imagens_botoes_resultado[acao][0].get_height()
            for acao in botoes
        )
        largura_total = sum(larguras_botoes) + (len(botoes) - 1) * espacamento
        inicio_x = (self.largura - largura_total) // 2
        y_botoes = self.altura - 84 + (48 - altura_botoes) // 2
        self.rects_botoes_resultado = {}
        x = inicio_x
        for acao, largura in zip(botoes, larguras_botoes):
            altura = self.imagens_botoes_resultado[acao][0].get_height()
            self.rects_botoes_resultado[acao] = pygame.Rect(
                x,
                y_botoes + (altura_botoes - altura) // 2,
                largura,
                altura,
            )
            x += largura + espacamento
        tempo_segundos = max(0, int(tempo_restante))
        linhas = [
            f"GALÁXIA {definicao.galaxia}: {definicao.nome_galaxia}",
            f"FASE {definicao.fase_na_galaxia} | {definicao.dificuldade.upper()}",
            f"PONTUAÇÃO FINAL: {pontuacao}",
            f"TEMPO RESTANTE: {tempo_segundos // 60:02}:{tempo_segundos % 60:02}",
        ]
        if venceu:
            linhas.extend(
                (
                    f"ESTRELAS NESTA TENTATIVA: {estrelas}/3",
                    f"MELHOR CLASSIFICAÇÃO: {melhor_classificacao}/3",
                )
            )
            if campanha_concluida:
                linhas.append("CAMPANHA CONCLUÍDA")
            elif erro_salvamento:
                linhas.append("AVANÇO BLOQUEADO: SALVAMENTO PENDENTE")
            elif proxima_desbloqueada:
                proxima_fase = FASES_CAMPANHA[definicao.indice + 1]
                if proxima_fase.galaxia != definicao.galaxia:
                    linhas.append("NOVA GALÁXIA DESBLOQUEADA")
                else:
                    linhas.append("PRÓXIMA FASE DESBLOQUEADA")
            elif definicao.numero == TOTAL_FASES:
                linhas.append("CAMPANHA AINDA NÃO CONCLUÍDA")
            else:
                linhas.append("PRÓXIMA FASE AINDA BLOQUEADA")
        else:
            linhas.extend(
                (
                    "FASE PERDIDA: O TEMPO ACABOU",
                    f"MELHOR CLASSIFICAÇÃO PRESERVADA: {melhor_classificacao}/3",
                )
            )

        if erro_salvamento:
            linhas.extend(
                (
                    "ERRO AO SALVAR O PROGRESSO",
                    "ESTA TENTATIVA NÃO FOI PERSISTIDA",
                )
            )

        while True:
            self.tela.blit(self.background, (0, 0))
            self.tela.blit(
                titulo_escalado,
                titulo_escalado.get_rect(center=(self.largura // 2, 64)),
            )
            y = 135
            for linha in linhas:
                self._texto_centralizado(
                    linha, self.fonte_pequena, (245, 247, 255), y
                )
                y += 30
            mouse = pygame.mouse.get_pos()
            for acao, rect in self.rects_botoes_resultado.items():
                self._desenhar_botao_resultado(
                    acao,
                    rect,
                    hover=rect.collidepoint(mouse),
                )
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    return "campanha"
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for acao, rect in self.rects_botoes_resultado.items():
                        if rect.collidepoint(evento.pos):
                            return acao
