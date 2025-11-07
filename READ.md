# Analisador Semântico com Gramática de Atributos

## Informações Institucionais
- **Instituição**: PUC PR
- **Curso**: Engenharia de Computação
- **Disciplina**: Linguagens Formais e Compiladores
- **Professor**: Frank Alcantara
- **Aluno**: Theo Hillmann Luiz Coelho
- **Período**: 2025/2

---

## 📋 Sumário

1. [Descrição](#-descrição)
2. [Como Usar](#-como-usar)
3. [Estrutura do Projeto](#-estrutura-do-projeto)
4. [Formato de Entrada](#-formato-de-entrada)
5. [Formato de Saída](#-formato-de-saída)
6. [Gramática Formal](#-gramática-formal)
7. [Regras de Inferência de Tipos](#-regras-de-inferência-de-tipos)
8. [Tabela de Coerções](#-tabela-de-coerções)
9. [Exemplos de Análise](#-exemplos-de-análise)
10. [Tratamento de Erros](#-tratamento-de-erros)
11. [Testes](#-testes)

---

## 📋 Descrição

Este projeto implementa um **analisador semântico completo** com gramática de atributos para uma linguagem de expressões em notação polonesa reversa (RPN). O sistema realiza:

- ✅ Análise sintática (parsing LL(1))
- ✅ Análise semântica com inferência de tipos
- ✅ Verificação de uso de memória (variáveis)
- ✅ Verificação de estruturas de controle (IF, WHILE)
- ✅ Geração de árvore sintática atribuída
- ✅ Relatórios detalhados em Markdown e JSON

---

## 🚀 Como Usar

### Requisitos
- Python 3.8 ou superior

### Instalação

```bash
git clone https://github.com/theohillmann/RA3_6.git
cd RA3_6
```

### Execução

Execute o analisador com um arquivo de entrada:

```bash
python main.py tokens/test1.txt
```

### Exemplos de Uso

```bash
# Teste básico com operações aritméticas
python main.py tokens/test1.txt

# Teste com estruturas de controle
python main.py tokens/test2.txt

# Teste com casos de erro
python main.py tokens/test3.txt
```

### Saída Esperada

```
✅ Árvore atribuída salva em: test1_arvore_atribuida.json
✅ Relatório de tipos salvo em: test1_relatorio_tipos.md
✅ Relatório de erros salvo em: test1_relatorio_erros.md
```

---

## 📁 Estrutura do Projeto

```
RA3_6/
├── main.py                          # Ponto de entrada principal
├── README.md                        # Esta documentação
│
├── define_grammar/                  # Definição da gramática de atributos
│   ├── define_grammar.py           # Gramática e regras semânticas
│   └── utils/                      
│       ├── symbols.py              # Tabela de símbolos
│       ├── oprules.py              # Regras de operadores
│       └── types.py                # Sistema de tipos
│
├── syntactic_analyzer/              # Analisador sintático LL(1)
│   ├── main.py                     # Parser principal
│   ├── build_grammar/              # Construção da gramática
│   ├── parsear/                    # Implementação do parser
│   ├── ler_tokens/                 # Leitura de tokens
│   └── gerar_arvore/               # Geração da AST
│
├── semantic_analyzer/               # Analisador semântico
│   ├── analyzer.py                 # Análise semântica principal
│   ├── semantic_memory.py          # Verificação de memória
│   ├── semantic_control.py         # Verificação de controle
│   └── attribute_tree.py           # Árvore atribuída e relatórios
│
└── tokens/                          # Arquivos de teste
    ├── test1.txt                   # Teste básico
    ├── test2.txt                   # Teste intermediário
    └── test3.txt                   # Teste com erros
```

---

## 📝 Formato de Entrada

### Sintaxe da Linguagem

A linguagem usa **notação polonesa reversa (RPN)** com parênteses:

#### Operações Aritméticas
```lisp
( 10 8 + )          ; Adição: 10 + 8 = 18
( 35 13 - )         ; Subtração: 35 - 13 = 22
( 5 6 * )           ; Multiplicação: 5 * 6 = 30
( 27 9 / )          ; Divisão: 27 / 9 = 3
( 17 6 % )          ; Módulo: 17 % 6 = 5
( 4 3 ^ )           ; Potência: 4^3 = 64
```

#### Operações Relacionais
```lisp
( 10 5 < )          ; Menor que: 10 < 5 = 0 (falso)
( 10 5 > )          ; Maior que: 10 > 5 = 1 (verdadeiro)
( 10 10 == )        ; Igual: 10 == 10 = 1
( 5 10 <= )         ; Menor ou igual: 5 <= 10 = 1
( 10 5 >= )         ; Maior ou igual: 10 >= 5 = 1
( 10 5 != )         ; Diferente: 10 != 5 = 1
```

#### Uso de Memória (Variáveis)
```lisp
( 55 X )            ; Armazena 55 na variável X
( X 7 - )           ; Usa X: X - 7 = 48
( 12 MEM )          ; Armazena 12 em MEM
( MEM 3 / )         ; Usa MEM: MEM / 3 = 4
```

#### Referência de Resultado (RES)
```lisp
( 10 8 + )          ; Linha 1: resultado = 18
( 1 RES )           ; Linha 2: referencia linha 1 = 18
( 2 RES )           ; Linha 3: referencia linha 2 = 18
```

#### Estruturas de Controle
```lisp
; IF (condicional ternário)
( condição then-expr else-expr IF )

; WHILE (loop)
( condição body-expr WHILE )
```

### Exemplo Completo de Entrada

```lisp
( 10 8 + )
( 35 13 - )
( 4 RES )
( 5 6 * )
( 27 9 / )
( 17 6 % )
( 4 3 ^ )
( ( 4 RES ) 2 * )
( 80 ( 4 RES ) + )
( 55 X )
( X 7 - )
( 12 MEM )
( MEM 3 / )
( Y 3 + )
( 10 3.5 / )
( 10 3.5 % )
( 3.5 2 % )
( 4 5 ^ )
( 1 RES )
( 10 ( 12 1 < ) + )
```

---

## 📊 Formato de Saída

O analisador gera **três arquivos** de saída:

### 1. Árvore Atribuída (JSON)

**Arquivo:** `<prefixo>_arvore_atribuida.json`

```json
{
  "lines": [
    {
      "line": 1,
      "context": "( 10 8 + )",
      "postfix": [
        {"kind": "INT", "value": 10},
        {"kind": "INT", "value": 8},
        {"kind": "OP", "value": "+"}
      ],
      "type": "int"
    },
    {
      "line": 2,
      "context": "( 35 13 - )",
      "postfix": [
        {"kind": "INT", "value": 35},
        {"kind": "INT", "value": 13},
        {"kind": "OP", "value": "-"}
      ],
      "type": "int"
    },
    {
      "line": 10,
      "context": "( 55 X )",
      "postfix": [
        {"kind": "INT", "value": 55},
        {"kind": "STORE", "value": "X"}
      ],
      "type": "int"
    }
  ],
  "symbols": {
    "X": {
      "type": "int",
      "initialized": true,
      "scope": 0
    },
    "MEM": {
      "type": "int",
      "initialized": true,
      "scope": 0
    }
  }
}
```

**Estrutura:**
- **`lines`**: Lista de linhas analisadas
  - `line`: Número da linha
  - `context`: Código fonte original
  - `postfix`: Tokens em notação posfixa
  - `type`: Tipo inferido (`int`, `real`, `bool`, `void`, `error`)
- **`symbols`**: Tabela de símbolos
  - `type`: Tipo da variável
  - `initialized`: Se foi inicializada
  - `scope`: Nível de escopo

### 2. Relatório de Tipos (Markdown)

**Arquivo:** `<prefixo>_relatorio_tipos.md`

```markdown
# Relatório de Tipos Inferidos

**Total de linhas analisadas:** 20
**Data de geração:** 2025-11-06 23:55:35

---

## Tabela de Tipos por Linha

| Linha | Contexto | Tipo Inferido | Notação Posfixa |
|-------|----------|---------------|-----------------|
| 1 | `( 10 8 + )` | 🔢 `int` | `INT(10) INT(8) OP(+)` |
| 2 | `( 35 13 - )` | 🔢 `int` | `INT(35) INT(13) OP(-)` |
| 3 | `( 4 RES )` | ❌ `error` | `INT(4) RES` |
| 4 | `( 5 6 * )` | 🔢 `int` | `INT(5) INT(6) OP(*)` |
| 10 | `( 55 X )` | 🔢 `int` | `INT(55) STORE(X)` |

---

## Tabela de Símbolos

| Nome | Tipo | Inicializada | Escopo |
|------|------|--------------|--------|
| `MEM` | `int` | ✅ Sim | 0 |
| `X` | `int` | ✅ Sim | 0 |

---

## Estatísticas

### Distribuição de Tipos
- 🔢 `int`: 17 (85.0%)
- ❌ `error`: 3 (15.0%)

### Taxa de Sucesso
**85.0%** das linhas foram tipadas com sucesso.
```

### 3. Relatório de Erros (Markdown)

**Arquivo:** `<prefixo>_relatorio_erros.md`

```markdown
# Relatório de Erros Semânticos

**Total de erros encontrados:** 5
**Data de geração:** 2025-11-06 23:55:35

---

## ❌ Erros Detectados

### Linha 3
**Contexto:** `( 4 RES )`
**Tipo Inferido:** `error`

**Erros:**
1. (N RES) references non-existent line.

### Linha 14
**Contexto:** `( Y 3 + )`
**Tipo Inferido:** `error`

**Erros:**
1. Variable 'Y' not declared.

### Linha 15
**Contexto:** `( 10 3.5 / )`
**Tipo Inferido:** `error`

**Erros:**
1. Invalid types for '/' (int, real).

---

## Resumo de Erros

### Erros por Categoria
- **Tipos Incompatíveis**: 3
- **Variável Não Declarada**: 1
- **RES Inválido**: 1

### Estatísticas
- **Linhas com erro:** 5/20
- **Taxa de erro:** 25.0%
```

---

## 📚 Gramática Formal

### EBNF com Anotações de Atributos

**Notação:**
- **↑** indica atributo **sintetizado** (calculado de baixo para cima)
- **↓** indica atributo **herdado** (passado de cima para baixo)

#### Gramática Principal

```ebnf
program        ::= { line } ;
line           ::= expr | stmt ;

expr           ::= atom
                 | "(" expr expr binop ")"
                 | "(" expr expr relop ")"
                 | "(" expr expr expr "IF" ")"
                 | "(" expr expr "WHILE" ")"
                 | "(" int_lit "RES" ")"
                 | "(" expr mem_store ")"
                 | "(" mem_ref ")"
                 ;

stmt           ::= "(" expr expr "WHILE" ")"
                 | "(" expr expr expr "IF" ")"
                 | "(" expr mem_store ")"
                 ;

atom           ::= int_lit | real_lit | mem_ref ;
mem_ref        ::= "MEM" | IDENT_UPPER ;
mem_store      ::= ">>" mem_ref ;
binop          ::= "+" | "-" | "*" | "/" | "%" | "^" ;
relop          ::= ">" | "<" | ">=" | "<=" | "==" | "!=" ;
```

#### Produções com Atributos

```ebnf
<E>↑tipo, ↑valor, ↑posfixa ::= "(" <E'>↑tipo, ↑valor, ↑posfixa ")"
                             { E.tipo := E'.tipo
                               E.valor := E'.valor
                               E.posfixa := E'.posfixa }

<E'>↑tipo, ↑valor, ↑posfixa ::= <NUM>↑tipo, ↑valor <OP>↑op
                              { E'.tipo := NUM.tipo
                                E'.valor := NUM.valor
                                E'.posfixa := [NUM] + [OP] }

                             | <NUM>↑tipo, ↑valor <E1>↑tipo, ↑valor, ↑posfixa <OP>↑op
                              { E'.tipo := inferir_tipo(NUM.tipo, E1.tipo, OP.op)
                                E'.valor := aplicar_op(NUM.valor, E1.valor, OP.op)
                                E'.posfixa := [NUM] + E1.posfixa + [OP] }

                             | <NUM>↑tipo, ↑valor <MEM_STORE>↑id
                              { E'.tipo := NUM.tipo
                                E'.valor := NUM.valor
                                E'.posfixa := [NUM] + [STORE(MEM_STORE.id)]
                                MEMORY := MEMORY ∪ {MEM_STORE.id → NUM.valor} }

                             | <MEMID>↑id, ↑tipo, ↑valor <OP>↑op
                              { verificar(MEMID.id ∈ MEMORY)
                                E'.tipo := MEMID.tipo
                                E'.valor := MEMID.valor
                                E'.posfixa := [REF(MEMID.id)] + [OP] }

                             | <MEMID>↑id, ↑tipo, ↑valor <E1>↑tipo, ↑valor, ↑posfixa <OP>↑op
                              { verificar(MEMID.id ∈ MEMORY)
                                E'.tipo := inferir_tipo(MEMID.tipo, E1.tipo, OP.op)
                                E'.valor := aplicar_op(MEMID.valor, E1.valor, OP.op)
                                E'.posfixa := [REF(MEMID.id)] + E1.posfixa + [OP] }

<NUM>↑tipo, ↑valor ::= <INT>↑valor
                     { NUM.tipo := "int"
                       NUM.valor := INT.valor }

                    | <REAL>↑valor
                     { NUM.tipo := "real"
                       NUM.valor := REAL.valor }
```

---

## 🔍 Regras de Inferência de Tipos

### Tipos Básicos

```
Γ ⊢ n : int          (n é literal inteiro)

Γ ⊢ r : real         (r é literal real)
```

### Operações Aritméticas Binárias (+, -, *, /)

#### Regra [OP-INT]
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────── [OP-INT]
Γ ⊢ (e₁ e₂ op) : int
```

#### Regra [OP-REAL]
```
Γ ⊢ e₁ : real   Γ ⊢ e₂ : real
─────────────────────────────── [OP-REAL]
Γ ⊢ (e₁ e₂ op) : real
```

#### Regra [OP-MIXED-ERROR]
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : real
─────────────────────────────── [OP-MIXED-ERROR]
Γ ⊢ (e₁ e₂ op) : error

Γ ⊢ e₁ : real   Γ ⊢ e₂ : int
─────────────────────────────── [OP-MIXED-ERROR]
Γ ⊢ (e₁ e₂ op) : error
```

### Operação Módulo (%)

#### Regra [MOD-INT]
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────── [MOD-INT]
Γ ⊢ (e₁ e₂ %) : int
```

#### Regra [MOD-ERROR]
```
Γ ⊢ e₁ : T₁     Γ ⊢ e₂ : T₂     T₁ = real ∨ T₂ = real
──────────────────────────────────────────────────── [MOD-ERROR]
Γ ⊢ (e₁ e₂ %) : error
```

### Operação Potência (^)

#### Regra [POW-INT]
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────── [POW-INT]
Γ ⊢ (e₁ e₂ ^) : int
```

#### Regra [POW-REAL]
```
Γ ⊢ e₁ : real   Γ ⊢ e₂ : real
─────────────────────────────── [POW-REAL]
Γ ⊢ (e₁ e₂ ^) : real
```

### Operações Relacionais (<, >, =, <=, >=, !=)

#### Regra [REL-INT]
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────── [REL-INT]
Γ ⊢ (e₁ e₂ rel_op) : int
```

#### Regra [REL-ERROR]
```
Γ ⊢ e₁ : T₁     Γ ⊢ e₂ : T₂     T₁ ≠ T₂
──────────────────────────────────────── [REL-ERROR]
Γ ⊢ (e₁ e₂ rel_op) : error
```

### Resultado da Última Operação (RES)

#### Regra [RES-OK]
```
Γ ⊢ e : T    resultado_anterior : T_res    T = T_res
──────────────────────────────────────────────────── [RES-OK]
Γ ⊢ (e res) : T
```

#### Regra [RES-ERROR]
```
Γ ⊢ e : T    resultado_anterior : T_res    T ≠ T_res
──────────────────────────────────────────────────── [RES-ERROR]
Γ ⊢ (e res) : error
```

#### Regra [RES-NO-PREV]
```
resultado_anterior = ∅
──────────────────────────────────────────────────── [RES-NO-PREV]
Γ ⊢ (e res) : error
```

### Armazenamento em Memória

#### Regra [MEM-STORE]
```
Γ ⊢ e : T
─────────────────────────────── [MEM-STORE]
Γ, x : T ⊢ (e >> x) : T
```

### Referência de Memória

#### Regra [MEM-REF]
```
x : T ∈ Γ
─────────────────────────────── [MEM-REF]
Γ ⊢ x : T
```

#### Regra [MEM-REF-ERROR]
```
x ∉ Γ
─────────────────────────────── [MEM-REF-ERROR]
Γ ⊢ x : error
```

---

## 📋 Tabela de Coerções

### Compatibilidade de Tipos por Operação

| Operação | Tipo e₁ | Tipo e₂ | Tipo Resultado | Regra Aplicada |
|----------|---------|---------|----------------|----------------|
| `+`, `-`, `*`, `/` | `int` | `int` | `int` | OP-INT |
| `+`, `-`, `*`, `/` | `real` | `real` | `real` | OP-REAL |
| `+`, `-`, `*`, `/` | `int` | `real` | **`error`** | OP-MIXED-ERROR |
| `+`, `-`, `*`, `/` | `real` | `int` | **`error`** | OP-MIXED-ERROR |
| `%` | `int` | `int` | `int` | MOD-INT |
| `%` | `int` | `real` | **`error`** | MOD-ERROR |
| `%` | `real` | `int` | **`error`** | MOD-ERROR |
| `%` | `real` | `real` | **`error`** | MOD-ERROR |
| `^` | `int` | `int` | `int` | POW-INT |
| `^` | `real` | `real` | `real` | POW-REAL |
| `^` | `int` | `real` | **`error`** | OP-MIXED-ERROR |
| `^` | `real` | `int` | **`error`** | OP-MIXED-ERROR |
| `<`, `>`, `=`, `<=`, `>=`, `!=` | `int` | `int` | `int` (bool) | REL-INT |
| `<`, `>`, `=`, `<=`, `>=`, `!=` | `real` | `real` | `real` (bool) | REL-INT |
| `<`, `>`, `=`, `<=`, `>=`, `!=` | `int` | `real` | **`error`** | REL-ERROR |
| `<`, `>`, `=`, `<=`, `>=`, `!=` | `real` | `int` | **`error`** | REL-ERROR |

### Política de Coerção

**Política Adotada:** Não há coerção automática de tipos.

A linguagem é **fortemente tipada** e **não admite conversões implícitas**.

#### Exemplos de Tipagem

| Expressão | Tipo Resultante | Status |
|-----------|-----------------|--------|
| `(10 8 +)` | `int` | ✅ Válido |
| `(3.5 2.0 *)` | `real` | ✅ Válido |
| `(10 3.5 /)` | `error` | ❌ Erro (mistura int e real) |
| `(3.5 2 %)` | `error` | ❌ Erro (% não aceita real) |
| `(10 20 <)` | `int` | ✅ Válido (resultado booleano) |
| `(4 3 ^)` | `int` | ✅ Válido |

### Regras Semânticas Adicionais

#### Regra de Escopo
```
∀ x ∈ MEMID : x deve ser declarado antes do uso
```

**Exemplo:**
```lisp
❌ ( Y 3 + )     # Erro: Y não foi declarado
✅ ( 55 Y )      # Declaração de Y
✅ ( Y 3 + )     # Agora é válido
```

#### Regra de Inicialização
```
∀ x ∈ MEMORY : x deve ter um valor atribuído antes da primeira leitura
```

**Exemplo:**
```lisp
✅ ( 10 X )      # X recebe 10
✅ ( X 5 + )     # Leitura válida de X
```

#### Regra de Controle de Fluxo
```
resultado_anterior é atualizado apenas após operações bem-sucedidas

resultado_anterior : T₁  →  (e op) : T₂  →  resultado_anterior : T₂
```

**Exemplo:**
```lisp
( 10 8 + )       # resultado_anterior := int (18)
( 4 RES )        # ✅ válido: tipo compatível
( 10 3.5 / )     # ❌ erro de tipo, resultado_anterior não muda
( 4 RES )        # ✅ ainda válido: usa resultado anterior
```

---

## 💡 Exemplos de Análise

### Exemplo 1: Operação Simples

**Entrada:**
```lisp
( 10 8 + )
```

**Derivação:**
```
E → ( E' )
  E'.tipo = int
  E'.valor = 18
  E'.posfixa = [INT(10), INT(8), OP(+)]
  
E' → NUM E1 OP
  NUM.tipo = int
  NUM.valor = 10
  
  E1 → NUM
    NUM.tipo = int
    NUM.valor = 8
  
  OP.op = +
  
  Cálculo de atributos:
    inferir_tipo(int, int, +) = int      [OP-INT]
    aplicar_op(10, 8, +) = 18
    E'.posfixa = [INT(10)] + [INT(8)] + [OP(+)]
```

**Resultado:**
```json
{
  "tipo": "int",
  "valor": 18,
  "posfixa": [
    {"kind": "INT", "value": 10},
    {"kind": "INT", "value": 8},
    {"kind": "OP", "value": "+"}
  ]
}
```

### Exemplo 2: Erro de Tipo

**Entrada:**
```lisp
( 10 3.5 / )
```

**Derivação:**
```
E → ( E' )
  E'.tipo = error
  
E' → NUM E1 OP
  NUM.tipo = int
  NUM.valor = 10
  
  E1 → NUM
    NUM.tipo = real
    NUM.valor = 3.5
  
  OP.op = /
  
  Cálculo de atributos:
    inferir_tipo(int, real, /) = error  [OP-MIXED-ERROR]
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 15]: Invalid types for '/' (int, real).
Contexto: ( 10 3.5 / )
```

### Exemplo 3: Uso de Memória

**Entrada:**
```lisp
( 55 X )
( X 7 - )
```

**Derivação Linha 1:**
```
E → ( E' )
  E'.tipo = int
  E'.valor = 55
  E'.posfixa = [INT(55), STORE(X)]
  
E' → NUM MEM_STORE
  NUM.tipo = int
  NUM.valor = 55
  
  MEM_STORE → >> MEMID
    MEMID.id = X
    MEM_STORE.id = X
  
  Ação semântica:
    MEMORY := MEMORY ∪ {X → (int, 55)}  [MEM-STORE]
```

**Derivação Linha 2:**
```
E → ( E' )
  E'.tipo = int
  E'.valor = 48
  E'.posfixa = [REF(X), INT(7), OP(-)]
  
E' → MEMID E1 OP
  MEMID.id = X
  verificar(X ∈ MEMORY) ✅
  MEMID.tipo = int
  MEMID.valor = 55
  
  E1 → NUM
    NUM.tipo = int
    NUM.valor = 7
  
  OP.op = -
  
  Cálculo de atributos:
    inferir_tipo(int, int, -) = int      [OP-INT]
    aplicar_op(55, 7, -) = 48
```

**Estado da memória:**
```json
{
  "symbols": {
    "X": {
      "type": "int",
      "initialized": true,
      "scope": 0
    }
  }
}
```

### Exemplo 4: Uso de RES

**Entrada:**
```lisp
( 10 8 + )
( 1 RES )
```

**Derivação Linha 1:**
```
E → ( E' )
  E'.tipo = int
  E'.valor = 18
  
  resultado_anterior := (int, 18)
```

**Derivação Linha 2:**
```
E → ( E' )
  
E' → NUM OP
  NUM.tipo = int
  NUM.valor = 1
  
  OP.op = RES
  
  Verificação:
    resultado_anterior : int
    target_line = 2 - 1 = 1
    linha[1].tipo = int
    
  Cálculo:
    E'.tipo = int  [RES-OK]
    E'.valor = 18
```

### Exemplo 5: Expressão Aninhada

**Entrada:**
```lisp
( ( 10 5 + ) 2 * )
```

**Derivação:**
```
E → ( E' )                                    [nível externo]
  
  E' → NUM E1 OP
    NUM → E_interno
      
      E_interno → ( E'_interno )             [nível interno]
        E'_interno → NUM E1_interno OP
          NUM.tipo = int, valor = 10
          E1_interno → NUM
            NUM.tipo = int, valor = 5
          OP.op = +
          
        inferir_tipo(int, int, +) = int
        aplicar_op(10, 5, +) = 15
        E'_interno.tipo = int
        E'_interno.valor = 15
        
      E_interno.tipo = int
      E_interno.valor = 15
    
    NUM.tipo = int
    NUM.valor = 15
    
    E1 → NUM
      NUM.tipo = int, valor = 2
    
    OP.op = *
    
    inferir_tipo(int, int, *) = int
    aplicar_op(15, 2, *) = 30
    
  E'.tipo = int
  E'.valor = 30
  E'.posfixa = [INT(10), INT(5), OP(+), INT(2), OP(*)]
```

**Resultado:**
```json
{
  "tipo": "int",
  "valor": 30,
  "posfixa": [
    {"kind": "INT", "value": 10},
    {"kind": "INT", "value": 5},
    {"kind": "OP", "value": "+"},
    {"kind": "INT", "value": 2},
    {"kind": "OP", "value": "*"}
  ]
}
```

---

## 🐛 Tratamento de Erros

O analisador detecta e reporta os seguintes tipos de erro:

### Erros de Tipo

#### Operações entre tipos incompatíveis
```lisp
( 10 3.5 / )
```
**Erro:** `Invalid types for '/' (int, real)`

#### Operador % com números reais
```lisp
( 10.5 2 % )
```
**Erro:** `Invalid types for '%' (real, int)`

#### Operações relacionais com tipos diferentes
```lisp
( 10 3.5 < )
```
**Erro:** `Invalid types for '<' (int, real)`

### Erros de Memória

#### Variável não declarada
```lisp
( Y 3 + )
```
**Erro:** `Variable 'Y' not declared`

#### Variável usada antes de ser inicializada
```lisp
( X 5 + )
```
**Erro:** `Variable 'X' used before initialization`

#### Atribuição de tipo incompatível
```lisp
( 10 X )
( 3.5 X )
```
**Erro:** `Type mismatch in assignment to 'X' (expected int, got real)`

### Erros de Controle

#### Condição de IF/WHILE não booleana
```lisp
( 10 20 30 IF )
```
**Erro:** `IF condition must be boolean`

#### RES referenciando linha inexistente
```lisp
( 10 RES )
```
**Erro:** `(N RES) references non-existent line`

#### RES com argumento não inteiro
```lisp
( 3.5 RES )
```
**Erro:** `N in (N RES) must be integer`

### Erros Sintáticos

#### Expressões malformadas
```lisp
( 10 + )
```
**Erro:** `Insufficient operands on stack`

#### Operandos insuficientes
```lisp
( + )
```
**Erro:** `Insufficient operands on stack`

#### Tokens desconhecidos
```lisp
( 10 8 @ )
```
**Erro:** `Unknown token: @`

---

## 🧪 Testes

### Arquivos de Teste Incluídos

| Arquivo | Descrição | Linhas | Erros Esperados |
|---------|-----------|--------|-----------------|
| `test1.txt` | Operações básicas, memória, RES | 20 | 5 erros |
| `test2.txt` | Estruturas de controle (IF, WHILE) | ~15 | 0-2 erros |
| `test3.txt` | Casos de erro diversos | ~10 | 5+ erros |

### Executar Todos os Testes

```bash
# Teste 1: Operações básicas
python main.py tokens/test1.txt

# Teste 2: Estruturas de controle
python main.py tokens/test2.txt

# Teste 3: Casos de erro
python main.py tokens/test3.txt
```

### Conteúdo do test1.txt

```lisp
( 10 8 + )          # Linha 1: int (18)
( 35 13 - )         # Linha 2: int (22)
( 4 RES )           # Linha 3: error (linha inexistente)
( 5 6 * )           # Linha 4: int (30)
( 27 9 / )          # Linha 5: int (3)
( 17 6 % )          # Linha 6: int (5)
( 4 3 ^ )           # Linha 7: int (64)
( ( 4 RES ) 2 * )   # Linha 8: int (128)
( 80 ( 4 RES ) + )  # Linha 9: int (110)
( 55 X )            # Linha 10: int (declara X)
( X 7 - )           # Linha 11: int (48)
( 12 MEM )          # Linha 12: int (declara MEM)
( MEM 3 / )         # Linha 13: int (4)
( Y 3 + )           # Linha 14: error (Y não declarada)
( 10 3.5 / )        # Linha 15: error (mistura int/real)
( 10 3.5 % )        # Linha 16: error (% com real)
( 3.5 2 % )         # Linha 17: error (% com real)
( 4 5 ^ )           # Linha 18: int (1024)
( 1 RES )           # Linha 19: int (18)
( 10 ( 12 1 < ) + ) # Linha 20: error (< retorna bool)
```

### Análise Esperada do test1.txt

**Linhas Corretas:** 15 (75%)
- Linhas: 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 18, 19

**Linhas com Erro:** 5 (25%)
- Linha 3: RES inválido
- Linha 14: Variável não declarada
- Linha 15: Tipos incompatíveis (int / real)
- Linha 16: % com real
- Linha 17: % com real
- Linha 20: Operação relacional em contexto aritmético

---

## 🎯 Funcionalidades

### Análise Sintática
- ✅ Parser LL(1) com tabela de análise
- ✅ Construção automática de gramática
- ✅ Cálculo de conjuntos FIRST e FOLLOW
- ✅ Geração de árvore sintática abstrata (AST)

### Análise Semântica
- ✅ **Inferência de tipos** com atributos sintetizados
- ✅ **Verificação de tipos** para operações aritméticas e relacionais
- ✅ **Tabela de símbolos** para gerenciamento de variáveis
- ✅ **Verificação de escopo** e inicialização
- ✅ **Suporte a RES** (referência de resultados anteriores)
- ✅ **Estruturas de controle** (IF, WHILE)
- ✅ **Detecção de erros** com mensagens descritivas

### Sistema de Tipos
- `int`: Números inteiros
- `real`: Números reais (ponto flutuante)
- `bool`: Valores booleanos (representados como int: 0 ou 1)
- `void`: Comandos sem valor de retorno
- `error`: Erros de tipo

### Relatórios
- ✅ **JSON**: Árvore sintática atribuída completa
- ✅ **Markdown**: Relatório de tipos com tabelas e estatísticas
- ✅ **Markdown**: Relatório de erros categorizado
- ✅ **Emojis**: Visualização intuitiva de tipos e status

---

## 🛠️ Desenvolvimento

### Módulos Principais

#### `main.py`
Ponto de entrada principal que coordena:
1. Leitura do arquivo de entrada
2. Análise sintática
3. Análise semântica (tipos, memória, controle)
4. Geração da árvore atribuída
5. Geração dos relatórios

#### `semantic_analyzer/analyzer.py`
- Análise semântica principal
- Avaliação de expressões em notação posfixa
- Inferência de tipos
- Detecção de erros semânticos

#### `semantic_analyzer/semantic_memory.py`
- Verificação de declaração de variáveis
- Verificação de inicialização
- Gerenciamento de escopo

#### `semantic_analyzer/semantic_control.py`
- Verificação de estruturas de controle (IF, WHILE)
- Validação de condições booleanas

#### `semantic_analyzer/attribute_tree.py`
- Geração da árvore sintática atribuída
- Geração de relatórios em Markdown e JSON
- Formatação de saída com emojis e tabelas

#### `define_grammar/utils/symbols.py`
- Implementação da tabela de símbolos
- Gerenciamento de escopo
- Lookup de variáveis

#### `define_grammar/utils/types.py`
- Sistema de tipos (`TypeKind` enum)
- Funções auxiliares: `promote()`, `lub()`, `is_numeric()`

#### `define_grammar/utils/oprules.py`
- Regras de operadores
- Verificação de aridade
- Checagem de tipos para cada operador

---

## 📖 Apêndice: Funções Auxiliares

### `inferir_tipo(T₁, T₂, op)`

```python
def inferir_tipo(t1: str, t2: str, op: str) -> str:
    """
    Infere o tipo resultante de uma operação binária.
    
    Retorna:
        - "int" para operações válidas entre inteiros
        - "real" para operações válidas entre reais
        - "error" para combinações inválidas
    """
    
    # Operação módulo: apenas int + int
    if op == '%':
        if t1 == 'int' and t2 == 'int':
            return 'int'
        return 'error'
    
    # Operações aritméticas: tipos devem ser iguais
    if op in ['+', '-', '*', '/', '^']:
        if t1 == t2:
            return t1
        return 'error'
    
    # Operações relacionais: tipos devem ser iguais
    if op in ['<', '>', '=', '<=', '>=', '!=']:
        if t1 == t2:
            return 'int'  # Resultado booleano representado como int
        return 'error'
    
    return 'error'
```

### `aplicar_op(v₁, v₂, op)`

```python
def aplicar_op(v1: float, v2: float, op: str) -> float:
    """
    Aplica o operador aos valores.
    
    Nota: Chamado apenas quando inferir_tipo retorna um tipo válido.
    """
    
    operacoes = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else float('inf'),
        '%': lambda a, b: a % b if b != 0 else 0,
        '^': lambda a, b: a ** b,
        '<': lambda a, b: 1 if a < b else 0,
        '>': lambda a, b: 1 if a > b else 0,
        '=': lambda a, b: 1 if a == b else 0,
        '<=': lambda a, b: 1 if a <= b else 0,
        '>=': lambda a, b: 1 if a >= b else 0,
        '!=': lambda a, b: 1 if a != b else 0,
    }
    
    return operacoes[op](v1, v2)
```

