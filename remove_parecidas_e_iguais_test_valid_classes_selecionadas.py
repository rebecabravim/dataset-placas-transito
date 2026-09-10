from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PLACAS = Path("placas_organizadas")

ARQUIVO_RELATORIO = Path(
    "relatorio_imagens_parecidas_por_phash_classes_selecionadas.txt"
)


# ============================================================
# FUNÇÕES
# ============================================================

def obter_imagens_para_apagar():
    """
    Lê o relatório e retorna somente imagens de valid e test.

    Imagens de train são completamente ignoradas.

    Todas as classes podem ser alteradas, inclusive:
    R-19-_60km-h
    """

    imagens_para_apagar = []

    if not ARQUIVO_RELATORIO.exists():

        print("ERRO: Relatório não encontrado:")
        print(ARQUIVO_RELATORIO.resolve())

        return imagens_para_apagar

    with open(
        ARQUIVO_RELATORIO,
        "r",
        encoding="utf-8"
    ) as arquivo:

        linhas = arquivo.readlines()

    for linha in linhas:

        linha = linha.strip()

        # ----------------------------------------------------
        # Somente caminhos de valid e test são considerados.
        #
        # Caminhos de train são ignorados.
        # ----------------------------------------------------

        if linha.startswith("valid\\"):

            conjunto = "valid"

        elif linha.startswith("test\\"):

            conjunto = "test"

        else:

            continue

        # ----------------------------------------------------
        # Divide o caminho
        #
        # Exemplo:
        #
        # valid\R-19-_60km-h\arquivo.jpg
        #
        # partes[0] = valid
        # partes[1] = R-19-_60km-h
        # partes[2] = arquivo.jpg
        # ----------------------------------------------------

        partes = linha.split("\\")

        if len(partes) < 3:
            continue

        # ----------------------------------------------------
        # Monta o caminho completo
        # ----------------------------------------------------

        caminho = (
            PASTA_PLACAS
            / Path(*partes)
        )

        imagens_para_apagar.append(
            caminho
        )

    return imagens_para_apagar


def mostrar_imagens(imagens):
    """
    Mostra as imagens que serão apagadas.
    """

    for imagem in imagens:
        print(f"  {imagem}")


def remover_imagens(imagens):
    """
    Remove as imagens selecionadas.
    """

    removidas = 0
    inexistentes = 0
    erros = 0

    for imagem in imagens:

        if not imagem.exists():

            print(
                f"ARQUIVO NÃO ENCONTRADO: {imagem}"
            )

            inexistentes += 1

            continue

        try:

            imagem.unlink()

            print(
                f"APAGADA: {imagem}"
            )

            removidas += 1

        except Exception as erro:

            print(
                f"ERRO ao apagar: {imagem}"
            )

            print(
                f"Motivo: {erro}"
            )

            erros += 1

    return (
        removidas,
        inexistentes,
        erros
    )


# ============================================================
# EXECUÇÃO
# ============================================================

def main():

    print("=" * 70)
    print(
        "REMOÇÃO DE DUPLICADAS DE VALID E TEST"
    )
    print("=" * 70)

    print()
    print("REGRAS:")
    print()
    print("- VALID: APAGAR DUPLICADAS")
    print("- TEST: APAGAR DUPLICADAS")
    print("- TRAIN: MANTER")
    print("- TODAS AS CLASSES PODEM SER ALTERADAS")

    # --------------------------------------------------------
    # Lê o relatório
    # --------------------------------------------------------

    print()
    print("Lendo relatório...")

    imagens = obter_imagens_para_apagar()

    # Remove possíveis repetições do próprio relatório
    imagens = list(
        dict.fromkeys(imagens)
    )

    # --------------------------------------------------------
    # Separa por conjunto usando o caminho
    # --------------------------------------------------------

    imagens_valid = []
    imagens_test = []

    for imagem in imagens:

        partes = imagem.relative_to(
            PASTA_PLACAS
        ).parts

        if len(partes) < 1:
            continue

        conjunto = partes[0]

        if conjunto == "valid":

            imagens_valid.append(imagem)

        elif conjunto == "test":

            imagens_test.append(imagem)

    # --------------------------------------------------------
    # Resumo
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)

    print()
    print(
        f"Imagens para apagar em VALID: "
        f"{len(imagens_valid)}"
    )

    print(
        f"Imagens para apagar em TEST: "
        f"{len(imagens_test)}"
    )

    print(
        f"Total para apagar: "
        f"{len(imagens)}"
    )

    # --------------------------------------------------------
    # Nenhuma imagem
    # --------------------------------------------------------

    if not imagens:

        print()
        print(
            "Nenhuma imagem será apagada."
        )

        return

    # --------------------------------------------------------
    # Mostra VALID
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "IMAGENS DE VALID QUE SERÃO APAGADAS"
    )
    print("=" * 70)

    print()

    mostrar_imagens(
        imagens_valid
    )

    # --------------------------------------------------------
    # Mostra TEST
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "IMAGENS DE TEST QUE SERÃO APAGADAS"
    )
    print("=" * 70)

    print()

    mostrar_imagens(
        imagens_test
    )

    # --------------------------------------------------------
    # Confirmação
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("ATENÇÃO")
    print("=" * 70)

    print()
    print(
        "Somente imagens de VALID e TEST serão apagadas."
    )

    print(
        "Nenhuma imagem de TRAIN será alterada."
    )

    print(
        "A classe R-19-_60km-h também poderá ser alterada."
    )

    confirmacao = input(
        "\nDigite SIM para confirmar: "
    ).strip().upper()

    if confirmacao != "SIM":

        print()
        print("Operação cancelada.")

        return

    # --------------------------------------------------------
    # Remove
    # --------------------------------------------------------

    print()
    print("Removendo imagens...")
    print()

    (
        removidas,
        inexistentes,
        erros
    ) = remover_imagens(
        imagens
    )

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 70)

    print()
    print(
        f"Imagens apagadas: {removidas}"
    )

    print(
        f"Arquivos não encontrados: {inexistentes}"
    )

    print(
        f"Erros: {erros}"
    )


if __name__ == "__main__":
    main()
