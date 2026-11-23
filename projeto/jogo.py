import pygame
import random

from constantes import *
from campanha import (
    ENTREGAS_PARA_CONCLUIR,
    FASES_CAMPANHA,
    ProgressoCampanha,
    TEMPO_INICIAL_FASE,
    TEMPO_MAXIMO_FASE,
    TOTAL_FASES,
    calcular_estrelas,
)
from fase import Fase
from pedido import *
from menu import Menu
from player import Romerio, Brito
from itens import *
from mapa import Mapa, VARIANTES_COZINHA, sortear_variante
from pedido import ReceitaTV
from interface_campanha import InterfaceCampanha, PAINEIS_TUTORIAL

from sons import som_inicial, som_face

class Jogo:
    def __init__(
        self,
        campanha=False,
        indice_fase=0,
        progresso=None,
        caminho_progresso=None,
    ):
        pygame.init()

        self.campanha_ativa = campanha
        self.caminho_progresso = caminho_progresso
        self.progresso_campanha = None
        self.indice_fase_campanha = None
        self.definicao_fase = None
        self.resultado_fase = None

        if campanha:
            if not 0 <= indice_fase < TOTAL_FASES:
                raise ValueError("Índice de fase fora da campanha disponível")
            self.indice_fase_campanha = indice_fase
            self.definicao_fase = FASES_CAMPANHA[indice_fase]
            self.progresso_campanha = (
                progresso
                if progresso is not None
                else ProgressoCampanha(caminho_progresso)
            )

        self.largura = int(LARGURA)
        self.altura = int(ALTURA)

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("Greedy Evolution")

        if campanha:
            self.nome_variante = self.definicao_fase.variante
            variante = VARIANTES_COZINHA[self.nome_variante]
        else:
            self.nome_variante, variante = sortear_variante()

        self.estilo = variante["estilo"]
        self.tipo_pedido = variante["pedido"]

        self.modelo_mapa = random.choice(variante["modelos"])
        
        self.mapa = Mapa(
            modelo=self.modelo_mapa,
            estilo=self.estilo
        )

        self.mapa.criar_colisoes()

        self.largura_logica = len(self.mapa.mapa[0]) * TILE_SIZE
        self.altura_logica = len(self.mapa.mapa) * TILE_SIZE
        self.superficie_jogo = pygame.Surface(
            (self.largura_logica, self.altura_logica)
        )

        self.escala_jogo = min(
            self.largura / self.largura_logica,
            self.altura / self.altura_logica,
        )
        self.tamanho_renderizado = (
            round(self.largura_logica * self.escala_jogo),
            round(self.altura_logica * self.escala_jogo),
        )
        self.posicao_renderizada = (
            (self.largura - self.tamanho_renderizado[0]) // 2,
            (self.altura - self.tamanho_renderizado[1]) // 2,
        )
        self.fase = Fase(
            tempo=TEMPO_INICIAL_FASE if campanha else TEMPOINICIAL,
            definicao=self.definicao_fase,
            limite_tempo=TEMPO_MAXIMO_FASE if campanha else None,
        )
        self.televisao = ReceitaTV(self.estilo)
        self.montagens = self.mapa.montagens
        self.ingredientes_tematicos = {
            dispensador.nome_ingrediente: []
            for dispensador in self.mapa.dispensadores_tematicos
        }
        # Cada partida mantém suas próprias listas; os nomes globais antigos de
        # player.py continuam disponíveis para compatibilidade com consumidores.
        self.tomates = []
        self.queijos = []
        self.paos = []
        self.carnes = []
        self.alfaces = []
        self.produtos = []
        if campanha:
            self.pedido_atual = criar_pedido_ponderado(
                self.tipo_pedido,
                self.definicao_fase,
            )
        else:
            self.pedido_atual = random.choice(
                pedidos_da_variante(self.tipo_pedido)
            )()
        for montagem in self.montagens:
            montagem.pedido = self.pedido_atual
        
        self.armarios = self.mapa.armarios
        self.armarios_queijo = self.mapa.armarios_queijo
        self.armarios_tomate = self.mapa.armarios_tomate
        self.armarios_alface = self.mapa.armarios_alface
        self.geladeiras = self.mapa.geladeiras
        self.lixeiras = self.mapa.lixos
        self.entregas = self.mapa.entregas

        self.player1 = Romerio(624, 192, self.estilo)
        self.player2 = Brito(240, 240, self.estilo)

        self.rodando = True
        self.clock = pygame.time.Clock()
        
    def processar_entrega(self, produto):
        modo_campanha = getattr(self, "campanha_ativa", False)
        if modo_campanha:
            if self.fase.encerrada:
                return False
            if self.fase.tempo <= 0:
                self.fase.encerrar("derrota")
                self.resultado_fase = {"resultado": "derrota", "estrelas": 0}
                return False

        pedido = self.pedido_atual
        pedido_correto = (
            isinstance(produto, ProdutoFinal)
            and isinstance(produto, pedido.produto_classe)
            and produto.familia == pedido.familia
            and produto.receita_id == pedido.receita_id
        )
        self.fase.destacar_entrega(pedido_correto)

        if modo_campanha and pedido_correto:
            self.fase.registrar_acerto(
                pedido.tempo,
                pedido.pontuacao,
            )
            if self.fase.entregas_corretas >= ENTREGAS_PARA_CONCLUIR:
                estrelas = calcular_estrelas(
                    self.definicao_fase.dificuldade,
                    self.fase.pontuacao,
                    self.fase.tempo,
                )
                self.fase.encerrar("vitoria", estrelas)
                melhor = self.progresso_campanha.registrar_resultado(
                    self.definicao_fase.numero,
                    estrelas,
                )
                persistido = getattr(
                    self.progresso_campanha,
                    "resultado_persistido",
                    getattr(self.progresso_campanha, "erro_salvamento", None)
                    is None,
                )
                self.resultado_fase = {
                    "resultado": "vitoria",
                    "estrelas": estrelas,
                    "melhor_classificacao": melhor,
                    "pontuacao": self.fase.pontuacao,
                    "tempo": self.fase.tempo,
                    "persistido": persistido,
                    "erro_salvamento": (
                        None
                        if persistido
                        else getattr(
                            self.progresso_campanha,
                            "erro_salvamento",
                            "Não foi possível confirmar o salvamento.",
                        )
                    ),
                }
            else:
                self.gerar_pedido()
        elif pedido_correto:
            self.fase.aumentar_tempo_pontuacao(
                pedido.tempo,
                pedido.pontuacao,
            )
            self.fase.entregas_corretas += 1
        else:
            self.fase.diminuir_tempo_pontuacao(
                pedido.tempo,
                pedido.pontuacao,
            )

        if not modo_campanha or not pedido_correto:
            self.gerar_pedido()
        return pedido_correto
        
    def gerar_pedido(self):
        if getattr(self, "campanha_ativa", False):
            if self.fase.encerrada:
                return self.pedido_atual
            self.pedido_atual = criar_pedido_ponderado(
                self.tipo_pedido,
                self.definicao_fase,
            )
            for montagem in self.montagens:
                montagem.pedido = self.pedido_atual
            return self.pedido_atual

        variante = getattr(self, "tipo_pedido", "hamburguer")
        self.pedido_atual = random.choice(
            pedidos_da_variante(variante)
        )()

        for montagem in self.montagens:
            montagem.pedido = self.pedido_atual

    def verificarEventos(self, dt=1 / 60):
        eventos = pygame.event.get()
        teclas_pressionadas = pygame.key.get_pressed()
        self.player1.atualizar_direcao(teclas_pressionadas)
        self.player2.atualizar_direcao(teclas_pressionadas)

        for evento in eventos:
            if getattr(self, "campanha_ativa", False) and self.fase.encerrada:
                break
            if evento.type == pygame.QUIT:
                self.rodando = False

            hamburguer1 = self.player1.verificar_habilidades(
            evento, self.armarios, self.armarios_queijo,
            self.armarios_tomate, self.armarios_alface,
            self.geladeiras, self.tomates, self.alfaces,
            self.queijos, self.paos, self.carnes,
            self.lixeiras, self.montagens, self.entregas, self.mapa.mapa,
            self.mapa.dispensadores_tematicos,
            self.ingredientes_tematicos, self.produtos,
            )

            if hamburguer1 is not None:
                self.processar_entrega(hamburguer1)

            if getattr(self, "campanha_ativa", False) and self.fase.encerrada:
                break

            hamburguer2 = self.player2.verificar_habilidades(
                evento, self.armarios, self.armarios_queijo,
                self.armarios_tomate, self.armarios_alface,
                self.geladeiras, self.tomates, self.alfaces,
                self.queijos, self.paos, self.carnes,
                self.lixeiras, self.montagens, self.entregas, self.mapa.mapa,
                self.mapa.dispensadores_tematicos,
                self.ingredientes_tematicos, self.produtos,
            )

            if hamburguer2 is not None:
                self.processar_entrega(hamburguer2)

            if getattr(self, "campanha_ativa", False) and self.fase.encerrada:
                break

            self.player1.verificar_cortagem(
                evento, self.mapa.tabuas, self.tomates,
                self.alfaces, self.queijos, self.paos, self.carnes,
                self.ingredientes_tematicos,
            )

            self.player2.verificar_cortagem(
                evento, self.mapa.tabuas, self.tomates,
                self.alfaces, self.queijos, self.paos, self.carnes,
                self.ingredientes_tematicos,
            )

        if getattr(self, "campanha_ativa", False) and self.fase.encerrada:
            return

        ingredientes_chao = [
            *self.tomates, *self.queijos, *self.paos,
            *self.carnes, *self.alfaces,
            *(
                ingrediente
                for lista in self.ingredientes_tematicos.values()
                for ingrediente in lista
            ),
        ]
        self.player1.mover(self.mapa.colisoes, ingredientes_chao, dt=dt)
        self.player2.mover(self.mapa.colisoes, ingredientes_chao, dt=dt)
        
        self.player1.verificar_indicador(
            self.lixeiras, self.armarios, self.armarios_queijo,
            self.armarios_tomate, self.armarios_alface, self.geladeiras,
            self.tomates, self.alfaces, self.queijos, self.paos, self.carnes,
            self.mapa.dispensadores_tematicos,
            self.ingredientes_tematicos, self.produtos,
            self.montagens, self.entregas,
        )
        self.player2.verificar_indicador(
            self.lixeiras, self.armarios, self.armarios_queijo,
            self.armarios_tomate, self.armarios_alface, self.geladeiras,
            self.tomates, self.alfaces, self.queijos, self.paos, self.carnes,
            self.mapa.dispensadores_tematicos,
            self.ingredientes_tematicos, self.produtos,
            self.montagens, self.entregas,
        )

        for tomate in self.tomates:
            tomate.atualizar()
        for queijo in self.queijos:
            queijo.atualizar()
        for alface in self.alfaces:
            alface.atualizar()
        for pao in self.paos:
            pao.atualizar()
        for carne in self.carnes:
            carne.atualizar()
            carne.assar_ingrediente(self.mapa.fornos, dt)

        for lista in self.ingredientes_tematicos.values():
            for ingrediente in lista:
                ingrediente.atualizar()
                ingrediente.preparar_ingrediente(self.mapa.fornos, dt)

        for produto in self.produtos:
            produto.atualizar()
            
    def desenhar(self):
        self.superficie_jogo.fill(PRETO)
        self.mapa.desenhar(self.superficie_jogo)
        ingredientes_tematicos = getattr(self, "ingredientes_tematicos", {})
        itens_em_preparo = list(self.carnes)
        for lista in ingredientes_tematicos.values():
            itens_em_preparo.extend(lista)
        self.mapa.desenhar_preparo(self.superficie_jogo, itens_em_preparo)

        for tomate in self.tomates:
            tomate.desenhar(self.superficie_jogo)

        for queijo in self.queijos:
            queijo.desenhar(self.superficie_jogo)

        for alface in self.alfaces:
            alface.desenhar(self.superficie_jogo)

        for pao in self.paos:
            pao.desenhar(self.superficie_jogo)

        for carne in self.carnes:
            carne.desenhar(self.superficie_jogo)

        for montagem in self.montagens:
            montagem.desenhar(self.superficie_jogo)

        for lista in ingredientes_tematicos.values():
            for ingrediente in lista:
                ingrediente.desenhar(self.superficie_jogo)

        for produto in getattr(self, "produtos", ()):
            produto.desenhar(self.superficie_jogo)

        self.player1.desenhar_indicador(self.superficie_jogo)
        self.player2.desenhar_indicador(self.superficie_jogo)

        self.player1.desenhar(self.superficie_jogo)
        self.player2.desenhar(self.superficie_jogo)

        superficie_redimensionada = pygame.transform.scale(
            self.superficie_jogo,
            self.tamanho_renderizado,
        )
        self.tela.fill(PRETO)
        self.tela.blit(superficie_redimensionada, self.posicao_renderizada)
        self.fase.desenhar(self.tela)
        self.televisao.desenhar(
            self.tela,
            self.pedido_atual,
            self.player1,
            self.player2,
            self.escala_jogo,
            self.posicao_renderizada,
            self.superficie_jogo.get_width(),
        )
        pygame.display.flip()
    def reiniciar(self):
        som_inicial.stop()
        som_face.stop()
        self.player1.parar_som_andar()
        self.player2.parar_som_andar()

        # Limpa referências mantidas por consumidores externos antes de trocar
        # pelas listas isoladas da nova partida.
        for lista in (self.tomates, self.queijos, self.paos, self.carnes, self.alfaces):
            lista.clear()

        if self.campanha_ativa:
            self.__init__(
                campanha=True,
                indice_fase=self.indice_fase_campanha,
                progresso=self.progresso_campanha,
                caminho_progresso=self.caminho_progresso,
            )
        else:
            self.__init__()

    def _carregar_fase_campanha(self, indice_fase):
        if hasattr(self, "player1"):
            self.player1.parar_som_andar()
            self.player2.parar_som_andar()
        som_face.stop()
        som_inicial.stop()
        for lista in (self.tomates, self.queijos, self.paos, self.carnes, self.alfaces):
            lista.clear()
        self.__init__(
            campanha=True,
            indice_fase=indice_fase,
            progresso=self.progresso_campanha,
            caminho_progresso=self.caminho_progresso,
        )

    def _tutorial_se_necessario(self, interface, indice_fase):
        definicao = FASES_CAMPANHA[indice_fase]
        if (
            definicao.fase_na_galaxia != 1
            or definicao.galaxia not in PAINEIS_TUTORIAL
        ):
            return "iniciar"

        return interface.executar_tutorial(definicao.galaxia)

    def _executar_fase_campanha(self):
        while self.rodando and not self.fase.encerrada:
            dt = self.clock.tick(60) / 1000
            self.fase.atualizar(dt)

            if self.fase.tempo <= 0:
                self.fase.encerrar("derrota")
                self.resultado_fase = {
                    "resultado": "derrota",
                    "estrelas": 0,
                    "melhor_classificacao": self.progresso_campanha.melhor_classificacao(
                        self.definicao_fase.numero
                    ),
                    "pontuacao": self.fase.pontuacao,
                    "tempo": 0,
                }
                break

            for montagem in self.montagens:
                montagem.atualizar(dt)

            self.verificarEventos(dt)
            if self.rodando and not self.fase.encerrada:
                self.desenhar()

        if not self.rodando:
            return "sair"
        return self.fase.resultado

    def _iniciar_campanha(self):
        som_inicial.play()
        acao = Menu(self.tela, self.largura, self.altura, "inicio").executar()
        if acao != "start":
            self.rodando = False
            som_inicial.stop()
            som_face.stop()
            pygame.quit()
            return
        som_inicial.stop()

        while self.rodando:
            interface = InterfaceCampanha(self.tela, self.largura, self.altura)
            som_inicial.play(-1)
            acao, indice_fase = interface.executar_selecao(self.progresso_campanha)
            som_inicial.stop()

            if acao == "sair":
                self.rodando = False
                break
            if acao == "menu":
                som_inicial.play()
                acao_menu = Menu(
                    self.tela, self.largura, self.altura, "inicio"
                ).executar()
                som_inicial.stop()
                if acao_menu != "start":
                    self.rodando = False
                continue
            if acao != "fase" or indice_fase is None:
                continue

            indice_atual = indice_fase
            while self.rodando:
                interface = InterfaceCampanha(self.tela, self.largura, self.altura)
                som_inicial.play(-1)
                acao_tutorial = self._tutorial_se_necessario(
                    interface,
                    indice_atual,
                )
                som_inicial.stop()
                if acao_tutorial == "sair":
                    self.rodando = False
                    break
                if acao_tutorial == "campanha":
                    break

                self._carregar_fase_campanha(indice_atual)
                som_face.play(-1)
                resultado = self._executar_fase_campanha()
                som_face.stop()
                self.player1.parar_som_andar()
                self.player2.parar_som_andar()

                if resultado == "sair":
                    self.rodando = False
                    break

                interface = InterfaceCampanha(self.tela, self.largura, self.altura)
                melhor = self.progresso_campanha.melhor_classificacao(
                    self.definicao_fase.numero
                )
                resultado_fase = getattr(self, "resultado_fase", None) or {}
                resultado_persistido = (
                    resultado_fase.get("persistido", True)
                    if resultado == "vitoria"
                    else True
                )
                proxima_desbloqueada = (
                    resultado_persistido
                    and self.indice_fase_campanha + 1 < TOTAL_FASES
                    and self.progresso_campanha.fase_desbloqueada(
                        self.definicao_fase.numero + 1
                    )
                )
                campanha_concluida = self.progresso_campanha.dados[
                    "campanha_concluida"
                ]

                som_inicial.play(-1)
                acao_resultado = interface.executar_resultado(
                    self.definicao_fase,
                    self.fase.pontuacao,
                    self.fase.tempo,
                    self.fase.estrelas,
                    melhor,
                    resultado == "vitoria",
                    proxima_desbloqueada,
                    campanha_concluida,
                    erro_salvamento=(
                        resultado_fase.get("erro_salvamento")
                        if not resultado_persistido
                        else None
                    ),
                )
                som_inicial.stop()

                if acao_resultado == "sair":
                    self.rodando = False
                    break
                if acao_resultado == "repetir":
                    continue
                if (
                    acao_resultado == "avancar"
                    and proxima_desbloqueada
                    and resultado_persistido
                ):
                    indice_atual += 1
                    continue
                break

        som_inicial.stop()
        som_face.stop()
        if hasattr(self, "player1"):
            self.player1.parar_som_andar()
            self.player2.parar_som_andar()
        pygame.quit()

    def iniciar(self):
        if self.campanha_ativa:
            return self._iniciar_campanha()

        som_inicial.play()
        menu = Menu(self.tela, self.largura, self.altura, "inicio")
        acao = menu.executar()

        if acao != "start":
            self.rodando = False
            som_inicial.stop()
            som_face.stop()
            self.player1.parar_som_andar()
            self.player2.parar_som_andar()
            pygame.quit()
            return

        som_inicial.stop()
        som_face.play(-1)

        while self.rodando:
            dt = self.clock.tick(60) / 1000
            self.fase.atualizar(dt)

            if self.fase.tempo <= 0:
                som_face.stop()
                som_inicial.stop()
                self.player1.parar_som_andar()
                self.player2.parar_som_andar()
                menu = Menu(self.tela, self.largura, self.altura, "gameover")

                acao = menu.executar()

                if acao == "retry":
                    self.reiniciar()

                    som_face.play(-1)
                    continue
                    
                elif acao == "quit":
                    self.rodando = False
                    break

            for montagem in self.montagens:
                montagem.atualizar(dt)

            self.verificarEventos(dt)
            self.desenhar()

        som_inicial.stop()
        som_face.stop()
        self.player1.parar_som_andar()
        self.player2.parar_som_andar()
        pygame.quit()
