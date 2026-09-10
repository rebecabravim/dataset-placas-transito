from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta onde estão os arquivos TXT
PASTA_TXT = Path(
    "placas_organizadas/imagens_ja_feitas_train/r-4a-proibido-virar-esquerda"
)

# Pasta onde estão as imagens
PASTA_IMAGENS = Path(
    "placas_organizadas/train/R-4a-_Proibido_virar_a_esquerda"
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

def remover_txts_sem_imagem():

    # --------------------------------------------------------
    # Verifica se as pastas existem
    # --------------------------------------------------------

    if not PASTA_IMAGENS.exists():
        print("ERRO: a pasta das imagens não foi encontrada:")
        print(PASTA_IMAGENS.resolve())
        return

    if not PASTA_TXT.exists():
        print("ERRO: a pasta dos TXT não foi encontrada:")
        print(PASTA_TXT.resolve())
        return

    # --------------------------------------------------------
    # Obtém os nomes das imagens
    # --------------------------------------------------------

    nomes_imagens = set()

    for imagem in PASTA_IMAGENS.iterdir():

        if not imagem.is_file():
            continue

        if imagem.suffix.lower() not in EXTENSOES_IMAGEM:
            continue

        nomes_imagens.add(imagem.stem)

    # --------------------------------------------------------
    # Segurança:
    # se nenhuma imagem for encontrada, não apaga TXT
    # --------------------------------------------------------

    if not nomes_imagens:

        print()
        print("=" * 60)
        print("PROCESSAMENTO CANCELADO")
        print("=" * 60)
        print()
        print("Nenhuma imagem foi encontrada.")
        print("Nenhum TXT foi apagado.")
        return

    # --------------------------------------------------------
    # Procura os TXT que não possuem imagem correspondente
    # --------------------------------------------------------

    txts_sem_imagem = []

    for arquivo_txt in PASTA_TXT.iterdir():

        if not arquivo_txt.is_file():
            continue

        if arquivo_txt.suffix.lower() != ".txt":
            continue

        nome_txt = arquivo_txt.stem

        if nome_txt not in nomes_imagens:
            txts_sem_imagem.append(arquivo_txt)

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print()

    print(
        f"Imagens encontradas: {len(nomes_imagens)}"
    )

    print(
        f"TXT sem imagem correspondente: "
        f"{len(txts_sem_imagem)}"
    )

    print()

    if not txts_sem_imagem:

        print(
            "Todos os TXT possuem uma imagem correspondente."
        )
        return

    print("TXT que serão removidos:")

    for arquivo_txt in sorted(txts_sem_imagem):
        print(f"  {arquivo_txt.name}")

    # --------------------------------------------------------
    # Remove os TXT
    # --------------------------------------------------------

    for arquivo_txt in txts_sem_imagem:
        arquivo_txt.unlink()

    print()
    print(
        f"TXT removidos: {len(txts_sem_imagem)}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    remover_txts_sem_imagem()