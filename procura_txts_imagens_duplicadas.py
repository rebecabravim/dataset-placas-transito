from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta que contém as imagens duplicadas
PASTA_IMAGENS = Path(
    "placas_organizadas/"
    "imagens_duplicadas_train_somente_das_labels_escolhidas"
)

# Informe aqui as 3 pastas que contêm os arquivos TXT
PASTA_TXT_1 = Path("placas_organizadas/imagens_ja_feitas_train/proibido_estacionar")
PASTA_TXT_2 = Path("placas_organizadas/imagens_ja_feitas_train/placa_pedestre")
PASTA_TXT_3 = Path("placas_organizadas/imagens_ja_feitas_train/r_19_60_km")

PASTAS_TXT = [
    PASTA_TXT_1,
    PASTA_TXT_2,
    PASTA_TXT_3
]

# Extensões de imagens que serão verificadas
EXTENSOES_IMAGEM = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ============================================================
# PROCESSAMENTO
# ============================================================

def verificar_txts():

    if not PASTA_IMAGENS.exists():
        print("ERRO: a pasta de imagens não foi encontrada:")
        print(PASTA_IMAGENS.resolve())
        return

    # --------------------------------------------------------
    # Obtém os nomes das imagens
    # --------------------------------------------------------

    nomes_imagens = set()

    for arquivo in PASTA_IMAGENS.iterdir():

        if not arquivo.is_file():
            continue

        if arquivo.suffix.lower() not in EXTENSOES_IMAGEM:
            continue

        nomes_imagens.add(arquivo.stem)

    # --------------------------------------------------------
    # Procura os TXT nas três pastas
    # --------------------------------------------------------

    txts_encontrados = []

    for pasta_txt in PASTAS_TXT:

        if not pasta_txt.exists():
            print(
                f"AVISO: pasta não encontrada: "
                f"{pasta_txt}"
            )
            continue

        for arquivo_txt in pasta_txt.iterdir():

            if not arquivo_txt.is_file():
                continue

            if arquivo_txt.suffix.lower() != ".txt":
                continue

            nome_txt = arquivo_txt.stem

            # ------------------------------------------------
            # Verifica se existe uma imagem com o mesmo nome
            # ------------------------------------------------

            if nome_txt in nomes_imagens:

                txts_encontrados.append(
                    (
                        arquivo_txt.name,
                        pasta_txt.name
                    )
                )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print()

    print(
        f"Quantidade de TXT encontrados: "
        f"{len(txts_encontrados)}"
    )

    print()

    if txts_encontrados:

        print("TXT encontrados:")

        for nome_txt, nome_pasta in sorted(txts_encontrados):
            print(
                f"{nome_txt} → {nome_pasta}"
            )

    else:

        print(
            "Nenhum TXT possui uma imagem correspondente."
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    verificar_txts()