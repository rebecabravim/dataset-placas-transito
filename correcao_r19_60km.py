from pathlib import Path
import shutil


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_TXT = Path(
    "placas_organizadas/imagens_ja_feitas_train/r_19_60_km"
)

PASTA_PLACAS = Path(
    "placas_organizadas"
)

PASTA_DESTINO = Path(
    "placas_organizadas/train/R-19-_60km-h"
)

EXTENSOES_IMAGEM = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ============================================================
# FUNÇÕES
# ============================================================

def obter_arquivos_txt():
    """
    Retorna todos os arquivos TXT da pasta de origem.
    """

    if not PASTA_TXT.exists():
        print("ERRO: Pasta dos TXT não encontrada:")
        print(PASTA_TXT.resolve())
        return []

    return [
        arquivo
        for arquivo in PASTA_TXT.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() == ".txt"
    ]


def procurar_imagem(nome):
    """
    Procura uma imagem com o nome informado
    dentro da pasta placas_organizadas.

    A própria pasta dos TXT é ignorada.
    """

    for arquivo in PASTA_PLACAS.rglob("*"):

        if not arquivo.is_file():
            continue

        if arquivo.suffix.lower() not in EXTENSOES_IMAGEM:
            continue

        if arquivo.stem != nome:
            continue

        # Não procurar dentro da pasta dos TXT
        try:
            arquivo.relative_to(PASTA_TXT)
            continue
        except ValueError:
            pass

        return arquivo

    return None


def mover_imagem(imagem):
    """
    Move a imagem para a pasta R-19-_60km-h.
    """

    PASTA_DESTINO.mkdir(
        parents=True,
        exist_ok=True
    )

    destino = PASTA_DESTINO / imagem.name

    if destino.exists():
        print(
            f"DESTINO JÁ EXISTE: {destino}"
        )
        return False

    try:

        shutil.move(
            str(imagem),
            str(destino)
        )

        print(
            f"MOVIDA: {imagem}"
        )

        print(
            f"    -> {destino}"
        )

        return True

    except Exception as erro:

        print(
            f"ERRO AO MOVER: {imagem}"
        )

        print(
            f"Motivo: {erro}"
        )

        return False


# ============================================================
# EXECUÇÃO
# ============================================================

def main():

    print("=" * 70)
    print(
        "MOVER IMAGENS PARA R-19-_60km-h"
    )
    print("=" * 70)

    print()
    print("Pasta dos TXT:")
    print(PASTA_TXT.resolve())

    print()
    print("Pasta de destino:")
    print(PASTA_DESTINO.resolve())

    txts = obter_arquivos_txt()

    print()
    print(
        f"Arquivos TXT encontrados: {len(txts)}"
    )

    if not txts:

        print()
        print("Nenhum TXT encontrado.")
        return

    encontradas = 0
    movidas = 0
    nao_encontradas = 0
    ja_existentes = 0

    print()
    print("Procurando imagens...")
    print()

    for txt in txts:

        nome_imagem = txt.stem

        imagem = procurar_imagem(
            nome_imagem
        )

        if imagem is None:

            print(
                f"NÃO ENCONTRADA: {nome_imagem}"
            )

            nao_encontradas += 1

            continue

        encontradas += 1

        destino = PASTA_DESTINO / imagem.name

        if destino.exists():

            print(
                f"JÁ EXISTE NO DESTINO: {imagem.name}"
            )

            ja_existentes += 1

            continue

        if mover_imagem(imagem):

            movidas += 1

    print()
    print("=" * 70)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 70)

    print()
    print(
        f"TXT analisados: {len(txts)}"
    )

    print(
        f"Imagens encontradas: {encontradas}"
    )

    print(
        f"Imagens movidas: {movidas}"
    )

    print(
        f"Não encontradas: {nao_encontradas}"
    )

    print(
        f"Já existentes no destino: {ja_existentes}"
    )


if __name__ == "__main__":
    main()
