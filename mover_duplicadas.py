from pathlib import Path
import shutil


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta principal do conjunto de treinamento
PASTA_TRAIN = Path("placas_organizadas/train")

# Pasta onde serão armazenadas as imagens duplicadas
PASTA_SAIDA = Path(
    "placas_organizadas/"
    "imagens_duplicadas_train_somente_das_labels_escolhidas"
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
    "R-15-_Altura_maxima"
}

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

def encontrar_e_mover_imagens_duplicadas():

    if not PASTA_TRAIN.exists():
        print(
            f"ERRO: a pasta '{PASTA_TRAIN}' não foi encontrada."
        )
        return

    # --------------------------------------------------------
    # Verifica se todas as classes selecionadas existem
    # --------------------------------------------------------

    print("Verificando as classes selecionadas...")
    print()

    classes_inexistentes = []

    for nome_classe in CLASSES_SELECIONADAS:

        pasta_classe = PASTA_TRAIN / nome_classe

        if not pasta_classe.exists():
            classes_inexistentes.append(nome_classe)

    if classes_inexistentes:

        print("AVISO: as seguintes pastas não foram encontradas:")

        for nome_classe in sorted(classes_inexistentes):
            print(f"  - {nome_classe}")

        print()

    # --------------------------------------------------------
    # Dicionário:
    #
    # nome da imagem -> lista de caminhos onde ela aparece
    #
    # IMPORTANTE:
    # somente as classes selecionadas entram neste dicionário.
    # --------------------------------------------------------

    imagens = {}

    classes_processadas = 0

    for nome_classe in sorted(CLASSES_SELECIONADAS):

        pasta_classe = PASTA_TRAIN / nome_classe

        if not pasta_classe.exists():
            continue

        classes_processadas += 1

        print(
            f"Analisando: {nome_classe}"
        )

        for arquivo in pasta_classe.iterdir():

            if not arquivo.is_file():
                continue

            if arquivo.suffix.lower() not in EXTENSOES_IMAGEM:
                continue

            nome_imagem = arquivo.name

            if nome_imagem not in imagens:
                imagens[nome_imagem] = []

            imagens[nome_imagem].append(arquivo)

    # --------------------------------------------------------
    # Identifica somente as imagens que aparecem em mais de
    # uma das classes selecionadas
    # --------------------------------------------------------

    imagens_duplicadas = {
        nome: caminhos
        for nome, caminhos in imagens.items()
        if len(caminhos) > 1
    }

    # --------------------------------------------------------
    # Cria a pasta de saída
    # --------------------------------------------------------

    PASTA_SAIDA.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Copia somente uma ocorrência de cada imagem duplicada
    # para a pasta de saída.
    #
    # Depois remove TODAS as ocorrências dessas imagens das
    # classes selecionadas.
    # --------------------------------------------------------

    total_imagens_duplicadas = 0
    total_ocorrencias_removidas = 0

    for nome_imagem, caminhos in imagens_duplicadas.items():

        destino = PASTA_SAIDA / nome_imagem

        # ----------------------------------------------------
        # Mantém somente uma cópia na pasta de saída
        # ----------------------------------------------------

        if not destino.exists():

            origem = caminhos[0]

            shutil.copy2(
                origem,
                destino
            )

        # ----------------------------------------------------
        # Remove todas as ocorrências das classes selecionadas
        # ----------------------------------------------------

        for caminho in caminhos:

            if caminho.exists():

                caminho.unlink()

                total_ocorrencias_removidas += 1

        total_imagens_duplicadas += 1

    # --------------------------------------------------------
    # RELATÓRIO
    # --------------------------------------------------------

    imagens_unicas = sum(
        1
        for caminhos in imagens.values()
        if len(caminhos) == 1
    )

    print()
    print("=" * 60)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 60)
    print()

    print(
        f"Classes selecionadas: "
        f"{len(CLASSES_SELECIONADAS)}"
    )

    print(
        f"Classes encontradas: "
        f"{classes_processadas}"
    )

    print(
        f"Imagens distintas analisadas: "
        f"{len(imagens)}"
    )

    print(
        f"Imagens duplicadas encontradas: "
        f"{total_imagens_duplicadas}"
    )

    print(
        f"Ocorrências removidas das classes: "
        f"{total_ocorrencias_removidas}"
    )

    print()

    print(
        "Pasta de destino:"
    )

    print(
        f"{PASTA_SAIDA.resolve()}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    encontrar_e_mover_imagens_duplicadas()