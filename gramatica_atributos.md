# Documentação Formal da Gramática de Atributos

## Sumário
1. [EBNF com Anotações de Atributos](#1-ebnf-com-anotações-de-atributos)
2. [Regras de Inferência de Tipos](#2-regras-de-inferência-de-tipos)
3. [Tabela de Coerções e Julgamentos](#3-tabela-de-coerções-e-julgamentos)
4. [Exemplos de Derivação com Atributos](#4-exemplos-de-derivação-com-atributos)

---

## 1. EBNF com Anotações de Atributos

### Notação:
- **↑** indica atributo **sintetizado** (calculado de baixo para cima)
- **↓** indica atributo **herdado** (passado de cima para baixo)

### Gramática Principal

```ebnf
<E>↑tipo, ↑valor, ↑posfixa ::= "(" <E'>↑tipo, ↑valor, ↑posfixa ")"
                             { E.tipo := E'.tipo
                               E.valor := E'.valor
                               E.posfixa := E'.posfixa }
```

### Produções de E'

#### Produção 1: Operador Unário
```ebnf
<E'>↑tipo, ↑valor, ↑posfixa ::= <NUM>↑tipo, ↑valor <OP>↑op
                              { E'.tipo := NUM.tipo
                                E'.valor := NUM.valor
                                E'.posfixa := [NUM] + [OP] }
```

#### Produção 2: Operador Binário
```ebnf
<E'>↑tipo, ↑valor, ↑posfixa ::= <NUM>↑tipo, ↑valor <E1>↑tipo, ↑valor, ↑posfixa <OP>↑op
                              { E'.tipo := inferir_tipo(NUM.tipo, E1.tipo, OP.op)
                                E'.valor := aplicar_op(NUM.valor, E1.valor, OP.op)
                                E'.posfixa := [NUM] + E1.posfixa + [OP] }
```

#### Produção 3: Armazenamento em Memória
```ebnf
<E'>↑tipo, ↑valor, ↑posfixa ::= <NUM>↑tipo, ↑valor <MEM_STORE>↑id
                              { E'.tipo := NUM.tipo
                                E'.valor := NUM.valor
                                E'.posfixa := [NUM] + [STORE(MEM_STORE.id)]
                                MEMORY := MEMORY ∪ {MEM_STORE.id → NUM.valor} }
```

#### Produção 4: Referência de Memória (Unário)
```ebnf
<E'>↑tipo, ↑valor, ↑posfixa ::= <MEMID>↑id, ↑tipo, ↑valor <OP>↑op
                              { verificar(MEMID.id ∈ MEMORY)
                                E'.tipo := MEMID.tipo
                                E'.valor := MEMID.valor
                                E'.posfixa := [REF(MEMID.id)] + [OP] }
```

#### Produção 5: Referência de Memória (Binário)
```ebnf
<E'>↑tipo, ↑valor, ↑posfixa ::= <MEMID>↑id, ↑tipo, ↑valor <E1>↑tipo, ↑valor, ↑posfixa <OP>↑op
                              { verificar(MEMID.id ∈ MEMORY)
                                E'.tipo := inferir_tipo(MEMID.tipo, E1.tipo, OP.op)
                                E'.valor := aplicar_op(MEMID.valor, E1.valor, OP.op)
                                E'.posfixa := [REF(MEMID.id)] + E1.posfixa + [OP] }
```

### Produções de NUM

```ebnf
<NUM>↑tipo, ↑valor ::= <INT>↑valor
                     { NUM.tipo := "int"
                       NUM.valor := INT.valor }

                    | <REAL>↑valor
                     { NUM.tipo := "real"
                       NUM.valor := REAL.valor }
```

### Produções de OP

```ebnf
<OP>↑op ::= "+" | "-" | "*" | "/" | "%" | "^" 
          | "<" | ">" | "=" | "<=" | ">=" | "!="
          { OP.op := operador_lido }
```

### Produções de Memória

```ebnf
<MEM_STORE>↑id ::= ">>" <MEMID>↑id
                 { MEM_STORE.id := MEMID.id }

<MEMID>↑id, ↑tipo, ↑valor ::= ID
                            { MEMID.id := ID.lexema
                              verificar(ID.lexema ∈ MEMORY)
                              MEMID.tipo := tipo_em_memoria(ID.lexema)
                              MEMID.valor := valor_em_memoria(ID.lexema) }
```

---

## 2. Regras de Inferência de Tipos

### 2.1. Tipos Básicos

```
Γ ⊢ n : int          (n é literal inteiro)

Γ ⊢ r : real         (r é literal real)
```

### 2.2. Operações Aritméticas Binárias (+, -, *, /)

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

### 2.3. Operação Módulo (%)

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

### 2.4. Operação Potência (^)

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

### 2.5. Operações Relacionais (<, >, =, <=, >=, !=)

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

### 2.6. Resultado da Última Operação (res)

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

### 2.7. Armazenamento em Memória

#### Regra [MEM-STORE]
```
Γ ⊢ e : T
─────────────────────────────── [MEM-STORE]
Γ, x : T ⊢ (e >> x) : T
```

> **Nota:** `x` é o identificador de memória

### 2.8. Referência de Memória

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

## 3. Tabela de Coerções e Julgamentos

### 3.1. Compatibilidade de Tipos por Operação

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

### 3.2. Política de Coerção

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

### 3.3. Julgamentos de Contexto

#### 3.3.1. Contexto de Memória

**Ambiente:**
```
Γ = {X : int, MEM : int}
```

**Julgamentos:**

```
✅ Γ ⊢ (55 >> X) : int          [válido: armazena 55 em X]
✅ Γ ⊢ (X 7 -) : int            [válido: X existe em Γ]
❌ Γ ⊢ (Y 3 +) : error          [erro: Y ∉ Γ]
```

#### 3.3.2. Contexto de Resultado Anterior

**Estado 1:** `resultado_anterior = int` (valor: 18)

```
✅ Γ ⊢ (4 res) : int            [válido: compatível com resultado anterior]
```

**Estado 2:** `resultado_anterior = ∅`

```
❌ Γ ⊢ (4 res) : error          [erro: sem resultado anterior disponível]
```

### 3.4. Regras Semânticas Adicionais

#### Regra de Escopo
```
∀ x ∈ MEMID : x deve ser declarado antes do uso
```

**Exemplo:**
```python
❌ (Y 3 +)     # Erro: Y não foi declarado
✅ (55 >> Y)   # Declaração de Y
✅ (Y 3 +)     # Agora é válido
```

#### Regra de Inicialização
```
∀ x ∈ MEMORY : x deve ter um valor atribuído antes da primeira leitura
```

**Exemplo:**
```python
✅ (10 >> X)   # X recebe 10
✅ (X 5 +)     # Leitura válida de X
```

#### Regra de Controle de Fluxo
```
resultado_anterior é atualizado apenas após operações bem-sucedidas

resultado_anterior : T₁  →  (e op) : T₂  →  resultado_anterior : T₂
```

**Exemplo:**
```python
(10 8 +)       # resultado_anterior := int (18)
(4 res)        # ✅ válido: tipo compatível
(10 3.5 /)     # ❌ erro de tipo, resultado_anterior não muda
(4 res)        # ✅ ainda válido: usa resultado anterior
```

---

## 4. Exemplos de Derivação com Atributos

### Exemplo 1: Operação Simples

**Entrada:** `(10 8 +)`

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

Resultado:
  tipo: int
  valor: 18
  posfixa: [INT(10), INT(8), OP(+)]
```

### Exemplo 2: Erro de Tipo

**Entrada:** `(10 3.5 /)`

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
    
Resultado:
  tipo: error
  erro: "Tipos incompatíveis: int e real em operação /"
```

### Exemplo 3: Armazenamento em Memória

**Entrada:** `(55 >> X)`

**Derivação:**
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
    
Resultado:
  tipo: int
  valor: 55
  posfixa: [INT(55), STORE(X)]
  
Estado da memória:
  MEMORY = {X : int = 55}
```

### Exemplo 4: Referência de Memória

**Entrada:** `(X 7 -)`

**Pré-condição:** `MEMORY = {X : int = 55}`

**Derivação:**
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
    E'.posfixa = [REF(X)] + [INT(7)] + [OP(-)]

Resultado:
  tipo: int
  valor: 48
  posfixa: [REF(X), INT(7), OP(-)]
```

### Exemplo 5: Uso de `res`

**Entrada:** 
```
Linha 1: (10 8 +)
Linha 2: (4 res)
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
  NUM.valor = 4
  
  OP.op = res
  
  Verificação:
    resultado_anterior : int
    NUM.tipo = int
    int = int ✅  [RES-OK]
    
  Cálculo:
    aplicar_op(4, 18, res) = 22
    E'.tipo = int
    
Resultado:
  tipo: int
  valor: 22
```

### Exemplo 6: Expressão Aninhada

**Entrada:** `((10 5 +) 2 *)`

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

Resultado:
  tipo: int
  valor: 30
  posfixa: [INT(10), INT(5), OP(+), INT(2), OP(*)]
```

---

## Apêndice A: Funções Auxiliares

### inferir_tipo(T₁, T₂, op)

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

### aplicar_op(v₁, v₂, op)

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

---

## Apêndice B: Gramática Abstrata (AST)

### Estrutura de Nós

```python
Node = {
    "type": str,           # Tipo do nó
    "value": any,          # Valor (para folhas)
    "children": [Node],    # Filhos (para não-terminais)
    "attributes": {        # Atributos calculados
        "tipo": str,       # Tipo inferido
        "valor": any,      # Valor calculado
        "posfixa": [Token] # Notação posfixa
    }
}
```

### Exemplo de AST Atribuído

Para a expressão `(10 8 +)`:

```json
{
  "type": "E",
  "children": [
    {
      "type": "E'",
      "children": [
        {
          "type": "NUM",
          "value": 10,
          "attributes": {
            "tipo": "int",
            "valor": 10
          }
        },
        {
          "type": "NUM",
          "value": 8,
          "attributes": {
            "tipo": "int",
            "valor": 8
          }
        },
        {
          "type": "OP",
          "value": "+",
          "attributes": {
            "op": "+"
          }
        }
      ],
      "attributes": {
        "tipo": "int",
        "valor": 18,
        "posfixa": [
          {"kind": "INT", "value": 10},
          {"kind": "INT", "value": 8},
          {"kind": "OP", "value": "+"}
        ]
      }
    }
  ],
  "attributes": {
    "tipo": "int",
    "valor": 18,
    "posfixa": [
      {"kind": "INT", "value": 10},
      {"kind": "INT", "value": 8},
      {"kind": "OP", "value": "+"}
    ]
  }
}
```

---

## Apêndice C: Mensagens de Erro

### Catálogo de Erros Semânticos

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| `ERR-001` | Tipos incompatíveis em operação aritmética | `(10 3.5 +)` |
| `ERR-002` | Operador módulo com operandos não-inteiros | `(10.5 2 %)` |
| `ERR-003` | Variável não declarada | `(X 5 +)` sem X na memória |
| `ERR-004` | Uso de `res` sem resultado anterior | `(4 res)` na primeira linha |
| `ERR-005` | Tipos incompatíveis com `res` | `(10 res)` quando resultado anterior é real |
| `ERR-006` | Tipos incompatíveis em operação relacional | `(10 3.5 <)` |

---

**Documento gerado para:** RA3_6 - Analisador Semântico com Gramática de Atributos  
**Autor:** theohillmann  
**Data:** 2025-11-06  
**Versão:** 1.0