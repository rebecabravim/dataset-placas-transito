from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta que será analisada
PASTA_DATASET = Path("placas_organizadas")

# Arquivo onde o resultado será salvo
ARQUIVO_SAIDA = Path("contagem_arquivos.txt")


# ============================================================
# FUNÇÃO PARA CONTAR ARQUIVOS
# ============================================================

def contar_arquivos(pasta):
    """
    Conta todos os arquivos existentes diretamente dentro
    de uma pasta.

    Não conta subpastas como arquivos.
    """

    total = 0

    for item in pasta.iterdir():

        if item.is_file():
            total += 1

    return total


# ============================================================
# PROCESSAMENTO
# ============================================================

def gerar_relatorio():

    if not PASTA_DATASET.exists():
        print(
            f"ERRO: a pasta '{PASTA_DATASET}' não foi encontrada."
        )
        return

    linhas_relatorio = []

    linhas_relatorio.append(
        "RELATÓRIO DE ARQUIVOS DO DATASET"
    )
    linhas_relatorio.append("=" * 60)
    linhas_relatorio.append("")

    total_geral = 0

    # --------------------------------------------------------
    # Percorre as divisões: train, valid e test
    # --------------------------------------------------------

    for nome_divisao in ["train", "valid", "test"]:

        pasta_divisao = PASTA_DATASET / nome_divisao

        if not pasta_divisao.exists():

            linhas_relatorio.append(
                f"[{nome_divisao}]"
            )
            linhas_relatorio.append(
                "Pasta não encontrada."
            )
            linhas_relatorio.append("")

            continue

        linhas_relatorio.append(
            f"[{nome_divisao.upper()}]"
        )
        linhas_relatorio.append("-" * 60)

        total_divisao = 0

        # ----------------------------------------------------
        # Percorre as subpastas da divisão
        # ----------------------------------------------------

        subpastas = sorted(
            [
                item
                for item in pasta_divisao.iterdir()
                if item.is_dir()
            ],
            key=lambda caminho: caminho.name.lower()
        )

        for pasta_classe in subpastas:

            quantidade = contar_arquivos(
                pasta_classe
            )

            linhas_relatorio.append(
                f"{pasta_classe.name}: {quantidade} arquivos"
            )

            total_divisao += quantidade

        # ----------------------------------------------------
        # Total da divisão
        # ----------------------------------------------------

        linhas_relatorio.append("")
        linhas_relatorio.append(
            f"TOTAL {nome_divisao.upper()}: "
            f"{total_divisao} arquivos"
        )
        linhas_relatorio.append("")

        total_geral += total_divisao

    # --------------------------------------------------------
    # Total geral
    # --------------------------------------------------------

    linhas_relatorio.append("=" * 60)
    linhas_relatorio.append(
        f"TOTAL GERAL: {total_geral} arquivos"
    )
    linhas_relatorio.append("=" * 60)

    # --------------------------------------------------------
    # Salva o relatório
    # --------------------------------------------------------

    with open(
        ARQUIVO_SAIDA,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            "\n".join(linhas_relatorio)
        )

    # --------------------------------------------------------
    # Também mostra no terminal
    # --------------------------------------------------------

    print("\n".join(linhas_relatorio))

    print()
    print(
        f"Relatório salvo em: "
        f"{ARQUIVO_SAIDA.resolve()}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    gerar_relatorio()
