# Sistema de Cálculo de Rotas entre Cidades

## 1. Pré-requisitos

- Python 3 instalado no computador.
- Terminal ou editor de código capaz de executar arquivos Python.

Não é necessário instalar bibliotecas externas, pois o programa utiliza apenas bibliotecas nativas do Python (`heapq` e `sys`).

Para verificar se o Python está instalado, execute no terminal:

```bash
python --version
```

Resultado esperado (versão utilizada no desenvolvimento):

```text
Python 3.14.6
```

## 2. Como executar o código

1. Baixe ou clone o repositório.
2. Abra o terminal na pasta onde está localizado o arquivo `rotas_dijkstra.py`.
3. Execute o seguinte comando:

```bash
python rotas_dijkstra.py
```

O menu principal será exibido no terminal.

## 3. Comandos e informações para utilizar o programa

O programa apresenta um menu com as seguintes opções:

| Opção | Ação |
|---|---|
| 1 | Cadastrar uma cidade |
| 2 | Cadastrar uma estrada entre duas cidades |
| 3 | Listar cidades e estradas cadastradas |
| 4 | Calcular a menor rota entre duas cidades |
| 5 | Verificar se existe uma rota entre duas cidades |
| 6 | Remover uma estrada |
| 7 | Remover uma cidade |
| 8 | Encerrar o programa |

Para utilizar as funcionalidades, basta digitar o número correspondente à opção desejada e pressionar `Enter`.

Quando solicitado, informe os IDs das cidades e as distâncias das estradas em quilômetros. Para distâncias decimais, é possível utilizar ponto ou vírgula.

Para executar os 10 testes automatizados, utilize:

```bash
python rotas_dijkstra.py --teste
```

Os 10 testes automatizados verificam se as principais funcionalidades do sistema estão funcionando corretamente, incluindo o cálculo de rotas, a remoção de cidades e estradas, o tratamento de entradas inválidas e a identificação de situações sem conexão. Eles são executados automaticamente, sem necessidade de interação do usuário.

Resultado esperado:

```text
Todos os 10 testes passaram.
```

## 4. Funcionamento do código

O programa utiliza um grafo não direcionado para representar as cidades e as estradas.

- Cada cidade é representada por um vértice, identificado por um número.
- Cada estrada é representada por uma aresta que conecta duas cidades.
- O peso de cada aresta corresponde à distância entre as cidades, em quilômetros.
- As conexões são armazenadas em listas de adjacência, utilizando dicionários do Python.


Para calcular a menor rota, o sistema utiliza o algoritmo de Dijkstra, que verifica as distâncias entre as cidades e identifica o caminho de menor custo até o destino informado.

O algoritmo utiliza uma fila de prioridade para processar primeiro as cidades com menor distância acumulada.

O sistema já inicia com cidades e estradas previamente cadastradas para demonstrar seu funcionamento.

**Observação:** os dados cadastrados durante a execução ficam armazenados apenas na memória e são perdidos quando o programa é encerrado.

## 5. Membros do grupo

Hugo Rafael Soares Carelli - 27799
Matheus Henrique Machado Saraiva - 27177
