from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PLACAS = Path("placas_organizadas")

ARQUIVO_RELATORIO = Path(
    "relatorio_imagens_duplicadas_classes_selecionadas.txt"
)

# Esta classe nunca será alterada
CLASSE_PROTEGIDA = "R-19-_60km-h"


# ============================================================
# FUNÇÕES
# ============================================================

def obter_imagens_para_apagar():
    """
    Lê o relatório e retorna somente imagens de valid e test.

    Imagens de train são completamente ignoradas.

    A classe R-19-_60km-h nunca será alterada.
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
        # SEGURANÇA:
        #
        # Somente linhas começando com valid\ ou test\
        # podem ser consideradas.
        #
        # Qualquer linha começando com train\ é ignorada.
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
        # valid\A-18-_Lombada\arquivo.jpg
        #
        # partes[0] = valid
        # partes[1] = A-18-_Lombada
        # partes[2] = arquivo.jpg
        # ----------------------------------------------------

        partes = linha.split("\\")

        if len(partes) < 3:
            continue

        classe = partes[1]

        # ----------------------------------------------------
        # SEGURANÇA:
        #
        # Nunca alterar R-19-_60km-h
        # ----------------------------------------------------

        if classe == CLASSE_PROTEGIDA:
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

        print(
            f"  {imagem}"
        )


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
    print("- VALID: APAGAR")
    print("- TEST: APAGAR")
    print("- TRAIN: MANTER")
    print(
        f"- {CLASSE_PROTEGIDA}: NÃO ALTERAR"
    )

    # --------------------------------------------------------
    # Lê o relatório
    # --------------------------------------------------------

    print()
    print(
        "Lendo relatório..."
    )

    imagens = obter_imagens_para_apagar()

    # Remove duplicações
    imagens = list(
        dict.fromkeys(imagens)
    )

    # --------------------------------------------------------
    # Separa por conjunto
    # --------------------------------------------------------

    imagens_valid = [
        imagem
        for imagem in imagens
        if "\\valid\\" in str(imagem)
    ]

    imagens_test = [
        imagem
        for imagem in imagens
        if "\\test\\" in str(imagem)
    ]

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
    print(
        "ATENÇÃO"
    )
    print("=" * 70)

    print()
    print(
        "Somente imagens de VALID e TEST serão apagadas."
    )

    print(
        "Nenhuma imagem de TRAIN será alterada."
    )

    print(
        f"A classe '{CLASSE_PROTEGIDA}' será preservada."
    )

    confirmacao = input(
        "\nDigite SIM para confirmar: "
    ).strip().upper()

    if confirmacao != "SIM":

        print()
        print(
            "Operação cancelada."
        )

        return

    # --------------------------------------------------------
    # Remove
    # --------------------------------------------------------

    print()
    print(
        "Removendo imagens..."
    )
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
    print(
        "PROCESSAMENTO CONCLUÍDO"
    )
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
