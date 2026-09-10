from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta onde estão os arquivos TXT
PASTA_TXT = Path(
    "placas_organizadas/imagens_ja_feitas_train/proibido_estacionar"
)

# Pasta onde estão as imagens
PASTA_IMAGENS = Path(
    "placas_organizadas/train/R-6a-_Proibido_estacionar"
)

# Extensões consideradas como imagens
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

def remover_imagens_sem_txt():

    # --------------------------------------------------------
    # Verifica se as pastas existem
    # --------------------------------------------------------

    if not PASTA_TXT.exists():
        print("ERRO: a pasta dos TXT não foi encontrada:")
        print(PASTA_TXT.resolve())
        return

    if not PASTA_IMAGENS.exists():
        print("ERRO: a pasta das imagens não foi encontrada:")
        print(PASTA_IMAGENS.resolve())
        return

    # --------------------------------------------------------
    # Obtém os nomes dos TXT
    # --------------------------------------------------------

    nomes_txt = set()

    for arquivo_txt in PASTA_TXT.iterdir():

        if not arquivo_txt.is_file():
            continue

        if arquivo_txt.suffix.lower() != ".txt":
            continue

        nomes_txt.add(arquivo_txt.stem)

    # --------------------------------------------------------
    # OBRIGA a existência de TXT antes de continuar
    # --------------------------------------------------------

    if not nomes_txt:

        print()
        print("=" * 60)
        print("PROCESSAMENTO CANCELADO")
        print("=" * 60)
        print()
        print("Nenhum arquivo TXT foi encontrado.")
        print()
        print(
            "Nenhuma imagem foi apagada."
        )
        print()
        return

    # --------------------------------------------------------
    # Obtém as imagens
    # --------------------------------------------------------

    imagens = []

    for imagem in PASTA_IMAGENS.iterdir():

        if not imagem.is_file():
            continue

        if imagem.suffix.lower() not in EXTENSOES_IMAGEM:
            continue

        imagens.append(imagem)

    # --------------------------------------------------------
    # Identifica as imagens sem TXT
    # --------------------------------------------------------

    imagens_sem_txt = []

    for imagem in imagens:

        nome_imagem = imagem.stem

        if nome_imagem not in nomes_txt:
            imagens_sem_txt.append(imagem)

    # --------------------------------------------------------
    # MOSTRA O QUE SERÁ REMOVIDO ANTES DE APAGAR
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("RESULTADO DA COMPARAÇÃO")
    print("=" * 60)
    print()

    print(
        f"TXT encontrados: {len(nomes_txt)}"
    )

    print(
        f"Imagens encontradas: {len(imagens)}"
    )

    print(
        f"Imagens sem TXT: {len(imagens_sem_txt)}"
    )

    print()

    if not imagens_sem_txt:

        print(
            "Todas as imagens possuem um TXT correspondente."
        )
        return

    print("Imagens que serão removidas:")

    for imagem in sorted(imagens_sem_txt):
        print(f"  {imagem.name}")

    # --------------------------------------------------------
    # REMOVE AS IMAGENS
    # --------------------------------------------------------

    for imagem in imagens_sem_txt:
        imagem.unlink()

    # --------------------------------------------------------
    # RESULTADO FINAL
    # --------------------------------------------------------

    print()
    print(
        f"Imagens removidas: {len(imagens_sem_txt)}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    remover_imagens_sem_txt()