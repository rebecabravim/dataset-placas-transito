# Dataset de Placas de Trânsito

Este repositório contém o dataset de placas de trânsito utilizado no projeto de Visão Computacional.

O dataset foi obtido a partir do Roboflow no formato YOLO/Darknet. As imagens estão acompanhadas de arquivos de anotação que identificam as classes e as posições dos objetos presentes em cada imagem.

## Estrutura do dataset

O dataset original está dividido em três conjuntos: `train`, `valid` e `test`. Além dessas pastas, o projeto possui a pasta `placas_organizadas`, gerada pelo script de reorganização das imagens por classe.

A estrutura geral do projeto é:

```text
dataset/

│
├── train/
│   ├── _darknet.labels
│   ├── imagem_001.jpg
│   ├── imagem_001.txt
│   ├── imagem_002.jpg
│   ├── imagem_002.txt
│   └── ...
│
├── valid/
│   ├── _darknet.labels
│   ├── imagem_101.jpg
│   ├── imagem_101.txt
│   └── ...
│
├── test/
│   ├── _darknet.labels
│   ├── imagem_201.jpg
│   ├── imagem_201.txt
│   └── ...
│
└── placas_organizadas/
    │
    ├── train/
    │   ├── Classe_1/
    │   │   ├── imagem_001.jpg
    │   │   └── ...
    │   ├── Classe_2/
    │   │   ├── imagem_002.jpg
    │   │   └── ...
    │   └── ...
    │
    ├── valid/
    │   ├── Classe_1/
    │   ├── Classe_2/
    │   └── ...
    │
    └── test/
        ├── Classe_1/
        ├── Classe_2/
        └── ...
```

As pastas `train`, `valid` e `test` correspondem ao dataset original:

* `train`: imagens utilizadas para treinamento do modelo.
* `valid`: imagens utilizadas para validação durante o desenvolvimento.
* `test`: imagens utilizadas para avaliação final do modelo.

Cada conjunto possui seu próprio arquivo `_darknet.labels`, além dos arquivos `.txt` correspondentes às imagens.

A pasta `placas_organizadas` é uma estrutura derivada do dataset original. Ela é utilizada para organizar as imagens de acordo com as classes encontradas nas anotações. Essa organização facilita etapas posteriores de análise e processamento do dataset.

A pasta `placas_organizadas` mantém a separação entre `train`, `valid` e `test`, de modo que uma imagem pertencente ao conjunto de treinamento continue dentro de `train`, uma imagem de validação continue dentro de `valid` e uma imagem de teste continue dentro de `test`.

A reorganização não substitui nem modifica o dataset original. As imagens são copiadas para as respectivas pastas de classe.

## Arquivo `_darknet.labels`

O arquivo `_darknet.labels` contém a lista de classes do dataset.

Cada linha representa uma classe, e a posição da linha determina o ID da classe.

A numeração começa em `0`.

Exemplo:

```text
-A-12- Intersecao em circulo
-A-13a- Confluencia a esquerda
...
-R-1- Pare
...
```

Nesse exemplo, a primeira linha possui ID `0`, a segunda possui ID `1` e assim sucessivamente.

Portanto:

```text
ID 0 → -A-12- Intersecao em circulo
ID 1 → -A-13a- Confluencia a esquerda
...
ID 51 → determinada classe
ID 61 → determinada classe
```

É importante **não alterar a ordem das classes no `_darknet.labels`**, pois os IDs utilizados pelos arquivos de anotação dependem diretamente dessa ordem.

## Arquivos `.txt` das imagens

Cada imagem possui um arquivo `.txt` correspondente com o mesmo nome.

Por exemplo:

```text
imagem_001.jpg
imagem_001.txt
```

O arquivo `.txt` contém as anotações dos objetos presentes na imagem utilizando o formato YOLO.

Cada linha representa um objeto identificado na imagem:

```text
ID_CLASSE CENTRO_X CENTRO_Y LARGURA ALTURA
```

Por exemplo:

```text
61 0.731891 0.266134 0.302702 0.445979
51 0.728918 0.725567 0.312200 0.453711
```

O primeiro valor de cada linha é o **ID da classe**.

Os quatro valores seguintes representam a posição e o tamanho da caixa delimitadora (`bounding box`) no formato YOLO:

```text
classe centro_x centro_y largura altura
```

As coordenadas são normalizadas, ou seja, seus valores ficam entre `0` e `1`.

## Uma imagem pode possuir várias classes

Uma mesma imagem pode conter mais de um objeto e, consequentemente, mais de uma classe.

Por exemplo:

```text
imagem_001.txt

61 0.731891 0.266134 0.302702 0.445979
51 0.728918 0.725567 0.312200 0.453711
```

Essa imagem possui objetos das classes `61` e `51`.

Por isso, ao reorganizar o dataset por classe, a imagem deve aparecer nas duas classes.

Exemplo:

```text
placas_organizadas/
└── train/
    ├── A-12_Intersecao_em_circulo/
    │   └── imagem_001.jpg
    │
    └── R-1_Pare/
        └── imagem_001.jpg
```

A imagem é **copiada**, e não movida. Dessa forma, uma ocorrência de uma classe não elimina a ocorrência de outra classe presente na mesma imagem.

## Regras importantes para o grupo

Não modificar a ordem das linhas do `_darknet.labels`.

Não alterar os IDs das classes manualmente.

Não assumir que cada imagem possui apenas uma classe.

Sempre ler todas as linhas do arquivo `.txt` correspondente à imagem.

Não excluir os arquivos `.txt`, pois eles contêm as informações de anotação necessárias para identificar os objetos.

A relação entre os arquivos deve ser preservada:

```text
imagem.jpg
imagem.txt
```

O nome-base deve ser o mesmo.

## Organização por classes

Para facilitar algumas etapas de análise e processamento, o projeto possui um script que reorganiza as imagens em pastas de acordo com as classes encontradas nas anotações.

A estrutura gerada é:

```text
placas_organizadas/
│
├── train/
│   ├── Classe_1/
│   ├── Classe_2/
│   └── ...
│
├── valid/
│   ├── Classe_1/
│   ├── Classe_2/
│   └── ...
│
└── test/
    ├── Classe_1/
    ├── Classe_2/
    └── ...
```

Os nomes das pastas são derivados dos nomes presentes no `_darknet.labels`, com limpeza dos caracteres e substituição dos espaços por `_`.

Por exemplo:

```text
-R-1- Pare
```

pode resultar em:

```text
R-1_Pare
```

Essa reorganização não altera o dataset original.

### Imagens sem anotação

Algumas imagens podem possuir um arquivo `.txt` vazio. Isso significa que não há nenhuma classe anotada para aquela imagem.

Nesse caso, a imagem **não é copiada para nenhuma pasta de classe**, pois não existe uma classe que possa ser associada a ela.

O arquivo original permanece no dataset de origem.

## Contagem de arquivos

O projeto também possui um script destinado à conferência da quantidade de arquivos após a reorganização do dataset.

O script percorre as pastas `train`, `valid` e `test` dentro de `placas_organizadas` e contabiliza os arquivos existentes em cada pasta de classe.

O resultado é exibido no terminal e também salvo em um arquivo:

```text
contagem_arquivos.txt
```

O relatório apresenta a quantidade de arquivos por classe e os totais de cada divisão.

As classes são apresentadas em **ordem decrescente de quantidade de arquivos**, facilitando a identificação das classes com maior e menor quantidade de imagens.

É importante observar que o **total de arquivos nas pastas de classes pode ser maior que a quantidade de imagens originais**. Isso ocorre porque uma mesma imagem pode possuir objetos de várias classes e, nesse caso, é copiada para cada uma das classes correspondentes.

## Fluxo dos dados

A relação entre os arquivos pode ser resumida da seguinte forma:

```text
_darknet.labels
       │
       │ define
       ▼
ID da classe ───────────────► Nome da classe
       ▲
       │
       │ utilizado por
       │
imagem.txt
       │
       │ contém
       ▼
Classe + Bounding Box
       │
       │ está associado a
       ▼
imagem.jpg
```

Portanto, para interpretar uma imagem corretamente, é necessário considerar os três elementos:

```text
_darknet.labels
       +
imagem.txt
       +
imagem.jpg
```

O `_darknet.labels` informa **o que significa cada ID**.

O `.txt` informa **quais objetos aparecem na imagem e onde estão localizados**.

O `.jpg` é a **imagem propriamente dita** na qual os objetos foram identificados.

## Exemplo completo

Considere:

```text
train/
├── _darknet.labels
├── placa_001.jpg
└── placa_001.txt
```

O arquivo `_darknet.labels` possui:

```text
Classe A
Classe B
Classe C
...
Classe 51
...
Classe 61
```

E `placa_001.txt` possui:

```text
61 0.73 0.26 0.30 0.44
51 0.72 0.72 0.31 0.45
```

Isso significa que `placa_001.jpg` possui dois objetos anotados: um pertencente à classe `61` e outro pertencente à classe `51`.

O processamento deve considerar ambos os objetos.

## Resumo

A estrutura básica do dataset segue a regra:

```text
train/
valid/
test/
    │
    ├── _darknet.labels
    ├── imagem.jpg
    └── imagem.txt
```

Após a reorganização, é criada uma estrutura adicional:

```text
placas_organizadas/

    │

    ├── train/

    │   ├── Classe_1/

    │   ├── Classe_2/

    │   └── ...

    │

    ├── valid/

    │   ├── Classe_1/

    │   ├── Classe_2/

    │   └── ...

    │

    └── test/

        ├── Classe_1/

        ├── Classe_2/

        └── ...
```

A correspondência é:

```text
posição no _darknet.labels
          ↓
      ID da classe
          ↓
primeiro valor de cada linha do .txt
          ↓
classe do objeto na imagem
```

Uma imagem pode possuir uma ou várias anotações e, portanto, uma ou várias classes.

Qualquer processamento do dataset deve preservar essa relação para evitar perda ou associação incorreta das classes.
