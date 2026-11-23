"""Regras fixas da campanha e persistencia local do progresso."""

from dataclasses import dataclass
import copy
import json
import os
from pathlib import Path
import tempfile


@dataclass(frozen=True)
class DefinicaoGalaxia:
    numero: int
    nome: str
    variante: str
    estilo: str
    tipo_pedido: str
    dificuldades: tuple


@dataclass(frozen=True)
class DefinicaoFase:
    indice: int
    numero: int
    galaxia: int
    fase_na_galaxia: int
    nome_galaxia: str
    variante: str
    estilo: str
    tipo_pedido: str
    dificuldade: str


GALAXIAS = (
    DefinicaoGalaxia(
        1,
        "Cozinha Classica",
        "classica",
        "classico",
        "hamburguer",
        ("fácil", "médio", "difícil"),
    ),
    DefinicaoGalaxia(
        2,
        "Pizzaria",
        "pizzaria",
        "pizzaria",
        "pizza",
        ("fácil", "médio", "médio", "difícil"),
    ),
    DefinicaoGalaxia(
        3,
        "Reator",
        "reator",
        "reator",
        "sushi",
        ("fácil", "médio", "médio", "médio", "difícil"),
    ),
)

GALAXIAS_EM_CONSTRUCAO = (4, 5)


def _criar_fases():
    fases = []
    for galaxia in GALAXIAS:
        for numero_local, dificuldade in enumerate(galaxia.dificuldades, start=1):
            indice = len(fases)
            fases.append(
                DefinicaoFase(
                    indice=indice,
                    numero=indice + 1,
                    galaxia=galaxia.numero,
                    fase_na_galaxia=numero_local,
                    nome_galaxia=galaxia.nome,
                    variante=galaxia.variante,
                    estilo=galaxia.estilo,
                    tipo_pedido=galaxia.tipo_pedido,
                    dificuldade=dificuldade,
                )
            )
    return tuple(fases)


FASES_CAMPANHA = _criar_fases()
TOTAL_FASES = len(FASES_CAMPANHA)
FASES_POR_GALAXIA = {
    galaxia.numero: tuple(
        fase for fase in FASES_CAMPANHA if fase.galaxia == galaxia.numero
    )
    for galaxia in GALAXIAS
}

LIMITES_PONTUACAO_ESTRELAS = {
    "fácil": (40, 55),
    "médio": (55, 70),
    "difícil": (70, 80),
}
TEMPO_MINIMO_DUAS_ESTRELAS = 15
TEMPO_MINIMO_TRES_ESTRELAS = 45
ENTREGAS_PARA_CONCLUIR = 4
TEMPO_INICIAL_FASE = 60
TEMPO_MAXIMO_FASE = 120
BONUS_MINIMO_TEMPO = 5


def calcular_estrelas(dificuldade, pontuacao, tempo_restante, fase_concluida=True):
    if not fase_concluida:
        return 0

    limites = LIMITES_PONTUACAO_ESTRELAS[dificuldade]
    if (
        pontuacao >= limites[1]
        and tempo_restante >= TEMPO_MINIMO_TRES_ESTRELAS
    ):
        return 3
    if (
        pontuacao >= limites[0]
        and tempo_restante >= TEMPO_MINIMO_DUAS_ESTRELAS
    ):
        return 2
    return 1


def caminho_padrao_progresso():
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        pasta = Path(local_app_data) / "GreedyEvolution"
    else:
        pasta = Path.home() / ".local" / "share" / "GreedyEvolution"
    return pasta / "progresso_campanha.json"


class ProgressoCampanha:
    VERSAO = 2
    VERSOES_MIGRAVEIS = (1, VERSAO)

    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho is not None else caminho_padrao_progresso()
        self.erro_salvamento = None
        self.resultado_persistido = True
        self.dados = self._carregar()

    @staticmethod
    def _dados_padrao():
        return {
            "versao": ProgressoCampanha.VERSAO,
            "fases_desbloqueadas": [1],
            "galaxias_desbloqueadas": [1],
            "melhores_estrelas": {
                str(numero): 0 for numero in range(1, TOTAL_FASES + 1)
            },
            "tutoriais_exibidos": {str(numero): False for numero in range(1, 4)},
            "campanha_concluida": False,
        }

    def _carregar(self):
        try:
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError, TypeError):
            return self._dados_padrao()

        versao = dados.get("versao") if isinstance(dados, dict) else None
        if type(versao) is not int or versao not in self.VERSOES_MIGRAVEIS:
            return self._dados_padrao()

        padrao = self._dados_padrao()
        estrelas_brutas = dados.get("melhores_estrelas", {})
        if isinstance(estrelas_brutas, dict):
            for numero in range(1, TOTAL_FASES + 1):
                valor = estrelas_brutas.get(str(numero), 0)
                if type(valor) is int and 0 <= valor <= 3:
                    padrao["melhores_estrelas"][str(numero)] = valor

        tutoriais_brutos = dados.get("tutoriais_exibidos", {})
        if isinstance(tutoriais_brutos, dict):
            for numero in range(1, 4):
                padrao["tutoriais_exibidos"][str(numero)] = (
                    tutoriais_brutos.get(str(numero)) is True
                )

        # A versão 1 gravava o tutorial como visto ao abrir a tela, antes de
        # o jogador escolher iniciar. Sem resultado na fase 1, esse marcador
        # pode ser falso; redefina somente esse tutorial e preserve o progresso.
        if (
            versao == 1
            and padrao["tutoriais_exibidos"]["1"]
            and padrao["melhores_estrelas"]["1"] == 0
        ):
            padrao["tutoriais_exibidos"]["1"] = False

        fases_desbloqueadas = [1]
        for numero_fase in range(1, TOTAL_FASES + 1):
            if numero_fase not in fases_desbloqueadas:
                # Recordes em fases ainda bloqueadas não são resultados válidos.
                padrao["melhores_estrelas"][str(numero_fase)] = 0
                continue
            if (
                numero_fase < TOTAL_FASES
                and padrao["melhores_estrelas"][str(numero_fase)] >= 1
            ):
                fases_desbloqueadas.append(numero_fase + 1)

        galaxias_desbloqueadas = sorted(
            {
                FASES_CAMPANHA[fase - 1].galaxia
                for fase in fases_desbloqueadas
            }
        )
        padrao["fases_desbloqueadas"] = fases_desbloqueadas
        padrao["galaxias_desbloqueadas"] = galaxias_desbloqueadas
        padrao["campanha_concluida"] = (
            padrao["melhores_estrelas"][str(TOTAL_FASES)] >= 1
        )
        return padrao

    def salvar(self):
        temporario = None
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            descritor, nome_temporario = tempfile.mkstemp(
                prefix=f".{self.caminho.name}.",
                suffix=".tmp",
                dir=self.caminho.parent,
            )
            temporario = Path(nome_temporario)
            with os.fdopen(descritor, "w", encoding="utf-8") as arquivo:
                json.dump(self.dados, arquivo, ensure_ascii=False, indent=2)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self.caminho)
            self.erro_salvamento = None
            return True
        except OSError as erro:
            self.erro_salvamento = str(erro)
            if temporario is not None:
                try:
                    temporario.unlink(missing_ok=True)
                except OSError:
                    pass
            return False

    def fase_desbloqueada(self, numero_fase):
        return numero_fase in self.dados["fases_desbloqueadas"]

    def galaxia_desbloqueada(self, numero_galaxia):
        return numero_galaxia in self.dados["galaxias_desbloqueadas"]

    def melhor_classificacao(self, numero_fase):
        return self.dados["melhores_estrelas"].get(str(numero_fase), 0)

    def tutorial_exibido(self, numero_galaxia):
        return self.dados["tutoriais_exibidos"].get(str(numero_galaxia), False)

    def marcar_tutorial_exibido(self, numero_galaxia):
        chave = str(numero_galaxia)
        if chave not in self.dados["tutoriais_exibidos"]:
            return False
        if self.dados["tutoriais_exibidos"][chave]:
            return True

        dados_anteriores = self.dados
        dados_novos = copy.deepcopy(dados_anteriores)
        dados_novos["tutoriais_exibidos"][chave] = True
        self.dados = dados_novos
        if not self.salvar():
            self.dados = dados_anteriores
            return False
        return True

    def registrar_resultado(self, numero_fase, estrelas):
        if (
            type(numero_fase) is not int
            or not 1 <= numero_fase <= TOTAL_FASES
            or type(estrelas) is not int
            or not 1 <= estrelas <= 3
        ):
            raise ValueError("Fase ou classificação fora dos limites da campanha")
        if not self.fase_desbloqueada(numero_fase):
            raise ValueError("Não é possível registrar resultado de fase bloqueada")

        self.resultado_persistido = True
        dados_anteriores = self.dados
        dados_novos = copy.deepcopy(dados_anteriores)
        chave = str(numero_fase)
        melhor_anterior = dados_anteriores["melhores_estrelas"][chave]
        mudou = estrelas > melhor_anterior
        if mudou:
            dados_novos["melhores_estrelas"][chave] = estrelas

        desbloqueadas = set(dados_novos["fases_desbloqueadas"])
        if estrelas >= 1 and numero_fase < TOTAL_FASES:
            desbloqueadas.add(numero_fase + 1)

        fases_ordenadas = sorted(desbloqueadas)
        if fases_ordenadas != dados_novos["fases_desbloqueadas"]:
            dados_novos["fases_desbloqueadas"] = fases_ordenadas
            mudou = True

        galaxias = sorted(
            {
                FASES_CAMPANHA[fase - 1].galaxia
                for fase in fases_ordenadas
            }
        )
        if galaxias != dados_novos["galaxias_desbloqueadas"]:
            dados_novos["galaxias_desbloqueadas"] = galaxias
            mudou = True

        campanha_concluida = (
            dados_novos["melhores_estrelas"][str(TOTAL_FASES)] >= 1
        )
        if dados_novos["campanha_concluida"] != campanha_concluida:
            dados_novos["campanha_concluida"] = campanha_concluida
            mudou = True

        if mudou:
            self.dados = dados_novos
            if not self.salvar():
                self.dados = dados_anteriores
                self.resultado_persistido = False
                return melhor_anterior
        return max(melhor_anterior, estrelas)

    def total_estrelas(self):
        return sum(self.dados["melhores_estrelas"].values())

    def percentual_campanha(self):
        return round(self.total_estrelas() / (TOTAL_FASES * 3) * 100)
