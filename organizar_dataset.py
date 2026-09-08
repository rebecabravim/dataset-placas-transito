import shutil
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta onde está o dataset original
PASTA_DATASET = Path(".")

# Pasta onde será criado o dataset reorganizado
PASTA_SAIDA = Path("placas_organizadas")

# Divisões do dataset
DIVISOES = ["train", "valid", "test"]

# Extensões de imagens aceitas
EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def ler_classes(caminho_labels):
    """
    Lê o arquivo _darknet.labels e cria um dicionário:

        ID da classe -> nome da classe

    Exemplo:

        0 -> "-A-12- Intersecao em circulo"
        1 -> "-A-13a- Confluencia a esquerda"
        ...

    O ID é determinado pela posição da classe no arquivo,
    começando em zero.
    """

    classes = {}

    with open(caminho_labels, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    for id_classe, linha in enumerate(linhas):

        nome_classe = linha.strip()

        # Ignora linhas vazias
        if not nome_classe:
            continue

        classes[id_classe] = nome_classe

    return classes


def limpar_nome_classe(nome_classe):
    """
    Limpa o nome da classe para ser utilizado como nome de pasta.

    Exemplos:

        "-R-1- Pare"
        -> "R-1_Pare"

        "-A-12- Intersecao em circulo"
        -> "A-12_Intersecao_em_circulo"

    Regras:
    - remove hífens extras no início e no fim;
    - substitui espaços por underscores;
    - elimina espaços duplicados;
    """

    nome = nome_classe.strip()

    # Remove hífens que estejam no início
    nome = nome.lstrip("-")

    # Remove hífens que estejam no final
    nome = nome.rstrip("-")

    # Substitui múltiplos espaços por um único espaço
    nome = " ".join(nome.split())

    # Substitui espaços por underscore
    nome = nome.replace(" ", "_")

    return nome


def ler_ids_classes_anotacao(caminho_anotacao):
    """
    Lê TODAS as linhas de uma anotação YOLO.

    Cada linha possui o formato:

        id_classe centro_x centro_y largura altura

    Exemplo:

        61 0.731891 0.266134 0.302702 0.445979
        51 0.728918 0.725567 0.312200 0.453711

    Retorna um conjunto contendo todos os IDs encontrados.

    Neste exemplo:

        {61, 51}

    Usamos um conjunto (set) para evitar copiar a mesma imagem
    duas vezes para a mesma classe caso uma classe apareça em
    mais de uma linha.
    """

    ids_classes = set()

    with open(caminho_anotacao, "r", encoding="utf-8") as arquivo:

        for numero_linha, linha in enumerate(arquivo, start=1):

            linha = linha.strip()

            # Ignora linhas vazias
            if not linha:
                continue

            partes = linha.split()

            # Uma anotação YOLO deve possuir pelo menos 5 valores:
            #
            # classe x y largura altura
            #
            if len(partes) < 5:
                print(
                    f"AVISO: anotação inválida em "
                    f"{caminho_anotacao} "
                    f"(linha {numero_linha})"
                )
                continue

            try:
                id_classe = int(partes[0])
            except ValueError:
                print(
                    f"AVISO: ID de classe inválido em "
                    f"{caminho_anotacao} "
                    f"(linha {numero_linha})"
                )
                continue

            ids_classes.add(id_classe)

    return ids_classes


def copiar_imagem_para_classe(
    caminho_imagem,
    pasta_divisao_saida,
    nome_classe
):
    """
    Copia uma imagem para a pasta correspondente à classe.

    Exemplo:

        placas_organizadas/
            train/
                R-1_Pare/
                    imagem001.jpg
    """

    pasta_classe = pasta_divisao_saida / nome_classe

    # Cria a pasta da classe caso ela ainda não exista
    pasta_classe.mkdir(parents=True, exist_ok=True)

    caminho_destino = pasta_classe / caminho_imagem.name

    # Copia a imagem preservando metadados
    shutil.copy2(caminho_imagem, caminho_destino)


# ============================================================
# PROCESSAMENTO DE UMA DIVISÃO
# ============================================================

def processar_divisao(nome_divisao):
    """
    Processa uma das divisões:

        train
        valid
        test
    """

    pasta_divisao = PASTA_DATASET / nome_divisao

    print()
    print("=" * 70)
    print(f"PROCESSANDO: {nome_divisao.upper()}")
    print("=" * 70)

    # Verifica se a pasta existe
    if not pasta_divisao.exists():
        print(f"AVISO: pasta não encontrada: {pasta_divisao}")
        return

    # --------------------------------------------------------
    # Localiza _darknet.labels
    # --------------------------------------------------------

    caminho_labels = pasta_divisao / "_darknet.labels"

    if not caminho_labels.exists():
        print(
            f"ERRO: arquivo _darknet.labels não encontrado em "
            f"{pasta_divisao}"
        )
        return

    # --------------------------------------------------------
    # Lê o mapeamento ID -> classe
    # --------------------------------------------------------

    classes = ler_classes(caminho_labels)

    print(f"Classes encontradas: {len(classes)}")

    # Mostra o mapeamento carregado
    for id_classe, nome_classe in classes.items():

        nome_limpo = limpar_nome_classe(nome_classe)

        print(
            f"  {id_classe:>3} -> "
            f"{nome_classe} -> "
            f"{nome_limpo}"
        )

    # --------------------------------------------------------
    # Define pasta de saída da divisão
    # --------------------------------------------------------

    pasta_divisao_saida = PASTA_SAIDA / nome_divisao

    pasta_divisao_saida.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Localiza imagens
    # --------------------------------------------------------

    imagens = [
        caminho
        for caminho in pasta_divisao.iterdir()
        if caminho.is_file()
        and caminho.suffix.lower() in EXTENSOES_IMAGEM
    ]

    print()
    print(f"Imagens encontradas: {len(imagens)}")

    # Contadores
    imagens_processadas = 0
    imagens_sem_anotacao = 0
    anotacoes_invalidas = 0
    copias_realizadas = 0

    # --------------------------------------------------------
    # Processa cada imagem
    # --------------------------------------------------------

    for caminho_imagem in sorted(imagens):

        # O arquivo de anotação possui o mesmo nome da imagem,
        # mas com extensão .txt.
        #
        # Exemplo:
        #
        # imagem001.jpg
        # imagem001.txt

        caminho_anotacao = caminho_imagem.with_suffix(".txt")

        # ----------------------------------------------------
        # Verifica se existe anotação
        # ----------------------------------------------------

        if not caminho_anotacao.exists():

            print(
                f"AVISO: anotação não encontrada para "
                f"{caminho_imagem.name}"
            )

            imagens_sem_anotacao += 1
            continue

        # ----------------------------------------------------
        # Lê TODAS as classes da imagem
        # ----------------------------------------------------

        ids_classes = ler_ids_classes_anotacao(
            caminho_anotacao
        )

        if not ids_classes:
            print(
                f"AVISO: nenhuma classe encontrada em "
                f"{caminho_anotacao.name}"
            )

            imagens_sem_anotacao += 1
            continue

        # ----------------------------------------------------
        # Copia a imagem para cada classe encontrada
        # ----------------------------------------------------

        for id_classe in sorted(ids_classes):

            # Verifica se o ID existe no _darknet.labels
            if id_classe not in classes:

                print(
                    f"ERRO: ID de classe {id_classe} não existe "
                    f"no arquivo _darknet.labels. "
                    f"Imagem: {caminho_imagem.name}"
                )

                anotacoes_invalidas += 1
                continue

            nome_classe_original = classes[id_classe]

            nome_classe_limpo = limpar_nome_classe(
                nome_classe_original
            )

            copiar_imagem_para_classe(
                caminho_imagem,
                pasta_divisao_saida,
                nome_classe_limpo
            )

            copias_realizadas += 1

        imagens_processadas += 1

        # Mostra progresso
        if imagens_processadas % 100 == 0:
            print(
                f"Processadas: "
                f"{imagens_processadas}/{len(imagens)}"
            )

    # --------------------------------------------------------
    # Resumo da divisão
    # --------------------------------------------------------

    print()
    print(f"Resumo de {nome_divisao}:")
    print(f"  Imagens encontradas:       {len(imagens)}")
    print(f"  Imagens processadas:       {imagens_processadas}")
    print(f"  Imagens sem anotação:      {imagens_sem_anotacao}")
    print(f"  IDs inválidos encontrados: {anotacoes_invalidas}")
    print(f"  Cópias realizadas:         {copias_realizadas}")


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():

    print("=" * 70)
    print("ORGANIZAÇÃO DO DATASET DE PLACAS DE TRÂNSITO")
    print("=" * 70)

    print()
    print(f"Dataset original: {PASTA_DATASET.resolve()}")
    print(f"Pasta de saída:   {PASTA_SAIDA.resolve()}")

    # Processa train, valid e test
    for divisao in DIVISOES:
        processar_divisao(divisao)

    print()
    print("=" * 70)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 70)

    print()
    print(
        f"O dataset reorganizado está em:"
        f"\n{PASTA_SAIDA.resolve()}"
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()