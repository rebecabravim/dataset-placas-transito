from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_TRAIN = Path("placas_organizadas/train")

ARQUIVO_RELATORIO = Path(
    "relatorio_imagens_repetidas_train.txt"
)

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

EXTENSOES_IMAGENS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


# ============================================================
# FUNÇÕES
# ============================================================

def obter_imagens():
    """
    Percorre todas as classes dentro de train e retorna
    todas as imagens encontradas.
    """
    imagens = []

    if not PASTA_TRAIN.exists():
        return imagens

    for pasta_classe in PASTA_TRAIN.iterdir():

        if not pasta_classe.is_dir():
            continue

        for arquivo in pasta_classe.rglob("*"):

            if (
                arquivo.is_file()
                and arquivo.suffix.lower() in EXTENSOES_IMAGENS
            ):
                imagens.append(arquivo)

    return imagens


def criar_indice_por_nome(imagens):
    """
    Agrupa as imagens pelo nome do arquivo.
    """
    indice = {}

    for imagem in imagens:

        nome = imagem.name

        if nome not in indice:
            indice[nome] = []

        indice[nome].append(imagem)

    return indice


def obter_classe(imagem):
    """
    Obtém o nome da classe da imagem.

    Exemplo:

        placas_organizadas/train/R-1-_Pare/imagem.jpg

    Retorna:

        R-1-_Pare
    """
    caminho_relativo = imagem.relative_to(PASTA_TRAIN)

    partes = caminho_relativo.parts

    if len(partes) >= 2:
        return partes[0]

    return ""


def classe_selecionada(imagem):
    """
    Verifica se a imagem pertence a uma das classes selecionadas.
    """
    classe = obter_classe(imagem)

    return classe in CLASSES_SELECIONADAS


def gerar_relatorio(indice):
    """
    Gera o relatório somente com imagens repetidas
    dentro de train.
    """
    linhas = []

    linhas.append("=" * 80)
    linhas.append("IMAGENS REPETIDAS DENTRO DE TRAIN")
    linhas.append("=" * 80)

    imagens_repetidas = 0

    for nome, locais in sorted(indice.items()):

        if len(locais) <= 1:
            continue

        imagens_repetidas += 1

        linhas.append("")
        linhas.append(f"Imagem: {nome}")
        linhas.append("")

        for local in sorted(locais):

            caminho_relativo = local.relative_to(PASTA_TRAIN)

            if classe_selecionada(local):
                linhas.append(f"  * {caminho_relativo}")
            else:
                linhas.append(f"    {caminho_relativo}")

        linhas.append("-" * 80)

    linhas.append("")
    linhas.append("=" * 80)
    linhas.append(
        f"Total de imagens repetidas: {imagens_repetidas}"
    )
    linhas.append("=" * 80)

    return "\n".join(linhas)


# ============================================================
# EXECUÇÃO
# ============================================================

def main():

    print("Procurando imagens em train...")

    imagens = obter_imagens()

    print(f"Total de imagens encontradas: {len(imagens)}")

    print("Verificando imagens repetidas...")

    indice = criar_indice_por_nome(imagens)

    relatorio = gerar_relatorio(indice)

    with open(
        ARQUIVO_RELATORIO,
        "w",
        encoding="utf-8"
    ) as arquivo:
        arquivo.write(relatorio)

    print(
        f"Relatório salvo em: {ARQUIVO_RELATORIO}"
    )


if __name__ == "__main__":
    main()