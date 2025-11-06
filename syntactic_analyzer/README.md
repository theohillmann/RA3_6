# Analisador Sintático

## Informações Institucionais
- **Instituição**: PUC PR
- **Curso**: Engenharia de Computação
- **Disciplina**: Linguagens formais e Compiladores
- **Professor**: Frank Alcantara
- **Aluno**: Theo Hillmann Luiz Coelho
- **Período**: 2025/2

## Descrição
Este projeto implementa um analisador sintático completo, incluindo construção de gramática, cálculo de conjuntos FIRST e FOLLOW, análise de tokens e geração de árvore sintática.

## Documentação Formal

### Gramática
```
E -> T E'
E' -> + T E' | - T E' | ε
T -> F T'
T' -> * F T' | / F T' | % F T' | ^ F T' | ε
F -> ( E ) | num | id | RES | MEM | X
```

### Conjuntos FIRST
- FIRST(E) = { (, num, id, RES, MEM, X }
- FIRST(E') = { +, -, ε }
- FIRST(T) = { (, num, id, RES, MEM, X }
- FIRST(T') = { *, /, %, ^, ε }
- FIRST(F) = { (, num, id, RES, MEM, X }

### Conjuntos FOLLOW
- FOLLOW(E) = { $, ) }
- FOLLOW(E') = { $, ) }
- FOLLOW(T) = { +, -, $, ) }
- FOLLOW(T') = { +, -, $, ) }
- FOLLOW(F) = { *, /, %, ^, +, -, $, ) }

### Tabela LL(1)
| Não-terminal | ( | num | id | RES | MEM | X | + | - | * | / | % | ^ | ) | $ |
|--------------|---|-----|-----|-----|-----|---|---|---|---|---|---|---|---|---|
| E | E→TE' | E→TE' | E→TE' | E→TE' | E→TE' | E→TE' | | | | | | | | |
| E' | | | | | | | E'→+TE' | E'→-TE' | | | | | E'→ε | E'→ε |
| T | T→FT' | T→FT' | T→FT' | T→FT' | T→FT' | T→FT' | | | | | | | | |
| T' | | | | | | | T'→ε | T'→ε | T'→*FT' | T'→/FT' | T'→%FT' | T'→^FT' | T'→ε | T'→ε |
| F | F→(E) | F→num | F→id | F→RES | F→MEM | F→X | | | | | | | | |

### Estruturas de Controle

O analisador suporta as seguintes estruturas de controle:

1. **Condicional (if)**
```
( condição then-expr else-expr if )
```
- `condição`: expressão booleana (usando operadores >, <, ==)
- `then-expr`: expressão executada se condição for verdadeira
- `else-expr`: expressão executada se condição for falsa

2. **Loop (while)**
```
( condição expr while )
```
- `condição`: expressão booleana que controla o loop
- `expr`: expressão executada enquanto condição for verdadeira

## Estrutura do Projeto

```
.
├── main.py                 # Ponto de entrada do programa
├── build_grammar/         # Módulo de construção da gramática
│   ├── build_grammar.py   # Construção da gramática
│   ├── calcular_first.py  # Cálculo do conjunto FIRST
│   ├── calcular_follow.py # Cálculo do conjunto FOLLOW
│   ├── constants.py       # Constantes do projeto
│   └── utils.py          # Funções utilitárias
├── gerar_arvore/         # Módulo de geração da árvore sintática
│   └── gerar_arvore.py   # Geração e visualização da árvore
├── ler_tokens/           # Módulo de leitura de tokens
│   └── ler_tokens.py     # Processamento de arquivos de tokens
├── parsear/             # Módulo de análise sintática
│   └── parsear.py       # Implementação do parser
└── tokens/              # Arquivos de teste
    ├── test1.json      # Arquivo de tokens de teste 1
    ├── test1.txt       # Resultado esperado do teste 1
    ├── test2.json      # Arquivo de tokens de teste 2
    ├── test2.txt       # Resultado esperado do teste 2
    ├── test3.json      # Arquivo de tokens de teste 3
    └── test3.txt       # Resultado esperado do teste 3
```

## Funcionalidades

- Construção automática de gramática
- Cálculo de conjuntos FIRST e FOLLOW
- Análise de tokens de entrada
- Geração de árvore sintática
- Visualização da árvore de análise
- Suporte a múltiplos arquivos de teste

## Como Usar

1. Certifique-se de ter Python instalado em seu sistema

2. Clone o repositório:
```bash
git clone https://github.com/theohillmann/RA2_6.git
cd RA2_6
```

3. Execute o programa com um arquivo de tokens:
```bash
python main.py tokens/test1.txt
```

## Formato dos Arquivos de Entrada

Os arquivos de tokens devem estar no formato txt e seguir a estrutura esperada pelo analisador. Exemplos podem ser encontrados no diretório `tokens/`.

## Estrutura de Módulos

### build_grammar/
- **build_grammar.py**: Responsável pela construção da gramática
- **calcular_first.py**: Implementa o algoritmo de cálculo do conjunto FIRST
- **calcular_follow.py**: Implementa o algoritmo de cálculo do conjunto FOLLOW
- **constants.py**: Define constantes utilizadas no projeto
- **utils.py**: Funções auxiliares para manipulação da gramática

### gerar_arvore/
- **gerar_arvore.py**: Implementa a geração e visualização da árvore sintática

### ler_tokens/
- **ler_tokens.py**: Processa e valida os arquivos de tokens de entrada

### parsear/
- **parsear.py**: Implementa o analisador sintático

## Testes

O diretório `tokens/` contém arquivos de teste para validar o funcionamento do analisador:
- `test1.txt`, `test2.txt`, `test3.txt`: Arquivos com expressões válidas para teste
- `test4.txt`: Arquivo com casos de teste de erro para validar o tratamento de erros do analisador



Projeto desenvolvido para a disciplina de Compiladores - PUCPR
