from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta com as classes do train
PASTA_TRAIN = Path("placas_organizadas/train")

# Pasta principal das placas
PASTA_PLACAS = Path("placas_organizadas")


# ============================================================
# FUNÇÕES
# ============================================================

def obter_imagens(pasta):
    """
    Retorna todas as imagens existentes dentro da pasta,
    incluindo imagens em subpastas.
    """
    extensoes = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    imagens = []

    if not pasta.exists():
        return imagens

    for arquivo in pasta.rglob("*"):
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes:
            imagens.append(arquivo)

    return imagens


def criar_indice_por_nome(imagens):
    """
    Cria um índice usando o nome do arquivo como chave.

    Exemplo:
        {
            "imagem1.jpg": [
                caminho1,
                caminho2
            ]
        }
    """
    indice = {}

    for imagem in imagens:
        nome = imagem.name

        if nome not in indice:
            indice[nome] = []

        indice[nome].append(imagem)

    return indice


def obter_imagens_train():
    """
    Obtém as imagens de todas as classes existentes
    dentro de pastas_organizadas/train.
    """
    imagens = []

    if not PASTA_TRAIN.exists():
        print(f"ATENÇÃO: Pasta não encontrada: {PASTA_TRAIN}")
        return imagens

    for pasta_classe in PASTA_TRAIN.iterdir():

        if not pasta_classe.is_dir():
            continue

        imagens.extend(obter_imagens(pasta_classe))

    return imagens


def obter_imagens_duplicadas():
    """
    Procura todas as pastas cujo nome começa com
    'imagens_duplicadas_' dentro de placas_organizadas.
    """
    imagens = []

    if not PASTA_PLACAS.exists():
        return imagens

    for pasta in PASTA_PLACAS.iterdir():

        if not pasta.is_dir():
            continue

        if pasta.name.startswith("imagens_duplicadas_"):
            imagens.extend(obter_imagens(pasta))

    return imagens


def obter_imagens_valid_test():
    """
    Obtém todas as imagens de valid e test.
    """
    imagens = []

    pasta_valid = PASTA_PLACAS / "valid"
    pasta_test = PASTA_PLACAS / "test"

    imagens.extend(obter_imagens(pasta_valid))
    imagens.extend(obter_imagens(pasta_test))

    return imagens


def verificar_repeticoes(imagens_origem, imagens_valid_test):
    """
    Compara os nomes das imagens da origem com os nomes
    encontrados em valid e test.
    """
    indice_valid_test = criar_indice_por_nome(imagens_valid_test)

    repeticoes = []

    for imagem in imagens_origem:
        nome = imagem.name

        if nome in indice_valid_test:
            repeticoes.append(
                (imagem, indice_valid_test[nome])
            )

    return repeticoes


# ============================================================
# EXECUÇÃO
# ============================================================

def main():
    print("=" * 70)
    print("VERIFICAÇÃO DE IMAGENS REPETIDAS")
    print("=" * 70)

    print("\nProcurando imagens de todas as classes em train...")
    imagens_train = obter_imagens_train()

    print(f"Imagens encontradas em train: {len(imagens_train)}")

    print("\nProcurando imagens nas pastas imagens_duplicadas_*...")
    imagens_duplicadas = obter_imagens_duplicadas()

    print(f"Imagens encontradas nas pastas duplicadas: {len(imagens_duplicadas)}")

    imagens_origem = imagens_train + imagens_duplicadas

    print("\nProcurando imagens em valid e test...")
    imagens_valid_test = obter_imagens_valid_test()

    print(f"Imagens encontradas em valid/test: {len(imagens_valid_test)}")

    print("\nVerificando repetições...")

    repeticoes = verificar_repeticoes(
        imagens_origem,
        imagens_valid_test
    )

    print("\n" + "=" * 70)
    print("RESULTADO")
    print("=" * 70)

    if not repeticoes:
        print("\nNenhuma imagem repetida foi encontrada ou as imagens não possuem mesmo nome.")
        return

    print(f"\nForam encontradas {len(repeticoes)} imagens repetidas:\n")

    for imagem_origem, locais_encontrados in repeticoes:

        print(f"IMAGEM: {imagem_origem.name}")

        print("Origem:")
        print(f"  {imagem_origem}")

        print("Encontrada em:")

        for local in locais_encontrados:
            print(f"  {local}")

        print("-" * 70)

    print(f"\nTotal de imagens repetidas: {len(repeticoes)}")


if __name__ == "__main__":
    main()