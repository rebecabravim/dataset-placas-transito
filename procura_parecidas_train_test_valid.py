from pathlib import Path
import imagehash
from PIL import Image


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PLACAS = Path("placas_organizadas")

ARQUIVO_RELATORIO = Path(
    "relatorio_imagens_parecidas_iguais" \
    "_por_phash_classes_selecionadas.txt"
)

# ------------------------------------------------------------
# Somente estas classes serão analisadas
# ------------------------------------------------------------

CLASSES_SELECIONADAS = {
    "R-19-_60km-h",
    "A-32b-_Passagem_sinalizada_de_pedestres",
    "R-24a-_Sentido_unico",
    "R-6a-_Proibido_estacionar",
    "R-6c-_Proibido_parar_e_estacionar",
    "A-18-_Lombada",
    "A-2b-_Curva_a_direita",
    "R-1-_Pare",
    "R-2-_De_a_preferencia",
    "A-32a-_Transito_de_pedestres",
    "A-2a-_Curva_a_esquerda",
    "R-4a-_Proibido_virar_a_esquerda",
    "R-5a-_Proibido_retornar_a_esquerda",
    "R-15-_Altura_maxima",
}

# Extensões consideradas como imagens
EXTENSOES_IMAGENS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}

# ------------------------------------------------------------
# Distância máxima entre os pHashes
#
# 0 = praticamente idênticas
# 1-5 = pequenas diferenças
# valores maiores = maior tolerância
# ------------------------------------------------------------

DISTANCIA_MAXIMA = 5


# ============================================================
# FUNÇÕES
# ============================================================

def obter_imagens(pasta):
    """
    Retorna todas as imagens existentes dentro da pasta,
    incluindo imagens em subpastas.
    """
    imagens = []

    if not pasta.exists():
        return imagens

    for arquivo in pasta.rglob("*"):

        if (
            arquivo.is_file()
            and arquivo.suffix.lower() in EXTENSOES_IMAGENS
        ):
            imagens.append(arquivo)

    return imagens


def obter_imagens_das_classes_selecionadas(pasta):
    """
    Obtém somente as imagens pertencentes às classes
    selecionadas.
    """
    imagens = []

    if not pasta.exists():
        return imagens

    for nome_classe in sorted(CLASSES_SELECIONADAS):

        pasta_classe = pasta / nome_classe

        if not pasta_classe.exists():
            continue

        if not pasta_classe.is_dir():
            continue

        imagens.extend(
            obter_imagens(pasta_classe)
        )

    return imagens


def calcular_phash(imagem):
    """
    Calcula o hash perceptual da imagem.
    """
    with Image.open(imagem) as arquivo:

        arquivo = arquivo.convert("RGB")

        return imagehash.phash(arquivo)


def calcular_hashes(imagens):
    """
    Calcula o pHash de todas as imagens.
    """
    hashes = {}

    total = len(imagens)

    for numero, imagem in enumerate(
        imagens,
        start=1
    ):

        print(
            f"Calculando pHash: "
            f"{numero}/{total} - {imagem.name}"
        )

        try:

            hash_imagem = calcular_phash(imagem)

            hashes[imagem] = hash_imagem

        except Exception as erro:

            print()
            print(
                f"ERRO ao processar: {imagem}"
            )
            print(
                f"Motivo: {erro}"
            )
            print()

    return hashes


def encontrar_grupos_duplicados(hashes):
    """
    Encontra grupos de imagens visualmente iguais ou
    muito semelhantes através da distância entre pHashes.
    """
    imagens = list(hashes.keys())

    grupos = []
    imagens_agrupadas = set()

    for indice, imagem in enumerate(imagens):

        if imagem in imagens_agrupadas:
            continue

        grupo = [
            imagem
        ]

        hash_imagem = hashes[imagem]

        for outra_imagem in imagens:

            if outra_imagem == imagem:
                continue

            if outra_imagem in imagens_agrupadas:
                continue

            outro_hash = hashes[outra_imagem]

            distancia = (
                hash_imagem - outro_hash
            )

            if distancia <= DISTANCIA_MAXIMA:

                grupo.append(
                    outra_imagem
                )

        if len(grupo) > 1:

            grupos.append(grupo)

            for imagem_grupo in grupo:

                imagens_agrupadas.add(
                    imagem_grupo
                )

    return grupos


def obter_caminho_relativo(imagem):
    """
    Retorna o caminho da imagem relativo à pasta
    placas_organizadas.
    """
    try:

        return imagem.relative_to(
            PASTA_PLACAS
        )

    except ValueError:

        return imagem


def obter_conjunto(imagem):
    """
    Identifica se a imagem pertence a train, valid ou test.
    """
    caminho_relativo = obter_caminho_relativo(
        imagem
    )

    partes = caminho_relativo.parts

    if len(partes) > 0:
        return partes[0]

    return ""


def obter_classe(imagem):
    """
    Identifica a classe da imagem.
    """
    caminho_relativo = obter_caminho_relativo(
        imagem
    )

    partes = caminho_relativo.parts

    if len(partes) > 1:
        return partes[1]

    return ""


def gerar_relatorio(grupos, hashes):
    """
    Gera o relatório das imagens duplicadas.
    """
    linhas = []

    linhas.append("=" * 90)
    linhas.append(
        "IMAGENS DUPLICADAS POR CONTEÚDO VISUAL"
    )
    linhas.append("=" * 90)

    linhas.append("")
    linhas.append(
        "Somente classes selecionadas"
    )
    linhas.append(
        "Conjuntos analisados: train, valid e test"
    )
    linhas.append(
        f"Distância máxima do pHash: "
        f"{DISTANCIA_MAXIMA}"
    )

    linhas.append("")

    total_ocorrencias = 0

    for numero_grupo, grupo in enumerate(
        grupos,
        start=1
    ):

        total_ocorrencias += len(grupo)

        hash_referencia = hashes[grupo[0]]

        linhas.append("")
        linhas.append(
            f"GRUPO {numero_grupo}"
        )
        linhas.append(
            f"Hash: {hash_referencia}"
        )
        linhas.append(
            f"Quantidade de ocorrências: "
            f"{len(grupo)}"
        )
        linhas.append("")

        for imagem in sorted(grupo):

            caminho = obter_caminho_relativo(
                imagem
            )

            conjunto = obter_conjunto(
                imagem
            )

            classe = obter_classe(
                imagem
            )

            linhas.append(
                f"  {caminho}"
            )

            linhas.append(
                f"    Conjunto: {conjunto}"
            )

            linhas.append(
                f"    Classe: {classe}"
            )

        linhas.append(
            "-" * 90
        )

    linhas.append("")
    linhas.append("=" * 90)
    linhas.append(
        f"Total de grupos duplicados: "
        f"{len(grupos)}"
    )
    linhas.append(
        f"Total de ocorrências duplicadas: "
        f"{total_ocorrencias}"
    )
    linhas.append("=" * 90)

    return "\n".join(linhas)


# ============================================================
# EXECUÇÃO
# ============================================================

def main():

    print("=" * 70)
    print(
        "VERIFICAÇÃO DE IMAGENS REPETIDAS POR PHASH"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    print()
    print(
        "Procurando imagens das classes selecionadas "
        "em train..."
    )

    imagens_train = (
        obter_imagens_das_classes_selecionadas(
            PASTA_PLACAS / "train"
        )
    )

    print(
        f"Imagens encontradas em train: "
        f"{len(imagens_train)}"
    )

    # --------------------------------------------------------
    # VALID
    # --------------------------------------------------------

    print()
    print(
        "Procurando imagens das classes selecionadas "
        "em valid..."
    )

    imagens_valid = (
        obter_imagens_das_classes_selecionadas(
            PASTA_PLACAS / "valid"
        )
    )

    print(
        f"Imagens encontradas em valid: "
        f"{len(imagens_valid)}"
    )

    # --------------------------------------------------------
    # TEST
    # --------------------------------------------------------

    print()
    print(
        "Procurando imagens das classes selecionadas "
        "em test..."
    )

    imagens_test = (
        obter_imagens_das_classes_selecionadas(
            PASTA_PLACAS / "test"
        )
    )

    print(
        f"Imagens encontradas em test: "
        f"{len(imagens_test)}"
    )

    # --------------------------------------------------------
    # Junta todos os conjuntos
    # --------------------------------------------------------

    imagens = (
        imagens_train
        + imagens_valid
        + imagens_test
    )

    print()
    print(
        f"Total de imagens para análise: "
        f"{len(imagens)}"
    )

    if not imagens:

        print()
        print(
            "Nenhuma imagem encontrada."
        )

        return

    # --------------------------------------------------------
    # Calcula pHash
    # --------------------------------------------------------

    print()
    print(
        "Calculando pHash das imagens..."
    )
    print()

    hashes = calcular_hashes(
        imagens
    )

    # --------------------------------------------------------
    # Procura duplicadas
    # --------------------------------------------------------

    print()
    print(
        "Comparando os pHashes..."
    )

    grupos = encontrar_grupos_duplicados(
        hashes
    )

    # --------------------------------------------------------
    # Gera relatório
    # --------------------------------------------------------

    print()
    print(
        f"Grupos duplicados encontrados: "
        f"{len(grupos)}"
    )

    print()
    print(
        "Gerando relatório..."
    )

    relatorio = gerar_relatorio(
        grupos,
        hashes
    )

    with open(
        ARQUIVO_RELATORIO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(relatorio)

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "PROCESSAMENTO CONCLUÍDO"
    )
    print("=" * 70)
    print()
    print(
        f"Relatório salvo em:"
    )
    print(
        f"{ARQUIVO_RELATORIO.resolve()}"
    )


if __name__ == "__main__":
    main()