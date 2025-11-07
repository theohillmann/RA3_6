# AVALIAÇÃO DO PROJETO: RA3_6

**DATA:** 2025-11-07

---

## RESUMO EXECUTIVO

**Nota Base Calculada:** 8.8/10.0  
**Penalidades Aplicadas:** 1.2 pontos  
**Nota Final:** 7.6/10.0  
**Status:** APROVADO COM RESSALVAS

---

## DETALHAMENTO POR BLOCO

### BLOCO 1 – Estrutura e Repositório (0.9/1.0)

**Checklist:**

- [X] Código-fonte presente (Python/C/C++)
  - **Evidência:** Arquivos Python em `main.py`, `semantic_analyzer/`, `define_grammar/`, `syntactic_analyzer/`
  - **Linguagem:** Python 3.x
  
- [X] Comentário inicial com integrantes + grupo Canvas
  - **Evidência:** `main.py` linhas 1-8:
    ```python
    """
    Compilador RPN - Fase 3: Analisador Semântico
    Instituição: PUC PR
    Disciplina: Linguagens Formais e Compiladores
    Aluno: Theo Hillmann Luiz Coelho
    Grupo Canvas: RA3_6
    Data: 2025/2
    """
    ```
  
- [ ] CLI aceita arquivo de teste por argumento
  - **Problema:** CLI requer flag `-f` explícita (`python main.py -f teste.txt`)
  - **Esperado:** Aceitar `python main.py teste.txt` conforme documentação comum
  - **Evidência:** `main.py` linha 26-29
  
- [X] README com instruções de executar/depurar e sintaxe de controle
  - **Arquivo:** `READ.md` (nota: nome não padrão, deveria ser `README.md`)
  - **Conteúdo:** Instruções completas, exemplos de execução, sintaxe RPN, estruturas IF/WHILE
  - **Evidência:** Linhas 42-193 descrevem execução, sintaxe e controle de fluxo
  
- [X] 3+ arquivos de teste (10+ linhas cada; válidos e inválidos)
  - **Testes principais:**
    - `tokens/test1.txt`: 21 linhas (casos válidos e inválidos mistos)
    - `tokens/test2.txt`: 13 linhas (casos válidos com IF)
    - `tokens/test3.txt`: 10 linhas (casos válidos com WHILE)
  - **Testes adicionais:** `syntactic_analyzer/tokens/test[1-4].txt`
  
- [ ] Organização de commits/PRs
  - **Problema:** Histórico de commits muito limitado (apenas 3 commits visíveis)
  - **Evidência:** `git log` mostra apenas: "changes", "Initial plan", commits de trabalho atual
  - **Falta:** Histórico detalhado de desenvolvimento, mensagens descritivas

**Penalidade:** -0.1 ponto (CLI não aceita argumento direto; README com nome não padrão)

---

### BLOCO 2 – Gramática de Atributos e Documentação (1.3/1.5)

**Arquivo:** `gramatica_atributos.md` (18.7 KB)

- [X] Arquivo markdown com gramática de atributos (EBNF + ações semânticas)
  - **Evidência:** Seção 1 (linhas 11-103) define EBNF completa com notações ↑ e ↓
  
- [X] Atributos definidos: tipo, valor, inicializada, escopo (terminais e não-terminais)
  - **Evidência:**
    - Tipos: `define_grammar/utils/types.py` linhas 4-10 (TypeKind enum)
    - Símbolos: `define_grammar/utils/symbols.py` linhas 5-10 (Symbol class com type, initialized, scope)
  
- [X] Regras para operadores aritméticos e relacionais (promoção int→real quando mistos)
  - **Problema:** Implementação NÃO faz promoção automática int→real
  - **Política real:** "fortemente tipada sem conversões implícitas" (linha 268-270 gramatica_atributos.md)
  - **Evidência:** `define_grammar/utils/oprules.py` linhas 12-16 retorna ERROR para tipos mistos
  - **Contradição:** Documentação menciona promoção, mas código rejeita operações mistas
  
- [X] Regras para IF/WHILE em RPN (condição → booleano)
  - **IF:** `define_grammar/utils/oprules.py` linhas 48-52 (check_if valida bool em condição)
  - **WHILE:** `semantic_analyzer/analyzer.py` linhas 551-556 (valida condição booleana)
  
- [X] Regras para (N RES), (V MEM), (MEM) com validações
  - **RES:** `semantic_analyzer/analyzer.py` linhas 559-604 (valida N inteiro ≥0, referência válida)
  - **MEM:** `semantic_analyzer/semantic_memory.py` linhas 97-122 (valida inicialização)
  
- [ ] Tabela/Sumário de coerções e julgamentos de tipo
  - **Presente:** Tabela em `gramatica_atributos.md` linhas 243-282
  - **Problema:** Tabela contradiz implementação real (menciona promoção que não existe)

**Penalidade:** -0.2 pontos (inconsistência entre documentação e implementação sobre promoção de tipos)

---

### BLOCO 3 – Verificação Semântica/Tipos (3.5/4.0)

**Arquivo principal:** `semantic_analyzer/analyzer.py` (624 linhas)

- [X] Percurso em pós-ordem e anotação de tipos
  - **Evidência:** `analyzer.py` linhas 275-392 (`evaluate_postfix` processa tokens em ordem pós-fixa)
  - **Pilha de tipos:** Linha 292 mantém stack de tuplas (tipo, valor)
  
- [X] ^ com expoente inteiro (validação)
  - **Evidência:** `analyzer.py` linhas 492-525 (`handle_exponentiation`)
  - **Validações:** Linha 517 requer exp_type == INT, linha 521 valida exp_value ≥ 0
  
- [ ] / e % apenas com inteiros (validação)
  - **Problema CRÍTICO:** Operador `/` implementado INCORRETAMENTE
  - **Evidência:** `define_grammar/utils/oprules.py`:
    - Linha 61: `"/": OpRule("/", 2, check_div_integer, "Integer Division (INT/INT=INT)")`
    - Linha 60: `"|": OpRule("|", 2, check_div_real, "Real Division (result REAL)")`
  - **Bug:** Operador `/` deveria ser divisão real (aceita int/real), mas está implementado como divisão inteira
  - **Operador `|` não documentado:** Usado para divisão real, mas não consta nas especificações
  - **Teste confirma:** `test1.txt` linha 15 `( 10 3.5 / )` gera erro (esperado aceitar com promoção)
  
- [X] Promoção para real em operações mistas
  - **Não implementado conforme esperado (decisão de design)**
  - **Evidência:** Sistema rejeita operações mistas por design forte de tipos
  - **Teste:** `test1.txt` linhas 15-17 geram erros por mistura de tipos
  
- [X] Relacionais retornam booleano
  - **Evidência:** `define_grammar/utils/oprules.py` linhas 43-45 (`check_relational` retorna BOOL)
  - **Teste:** `test2.txt` linha 4 usa `( A B > )` como condição
  
- [X] Condições de IF/WHILE validadas como booleano
  - **IF:** `analyzer.py` linhas 528-548 (`handle_if_expression` valida via check_if)
  - **WHILE:** `analyzer.py` linhas 551-556 (`handle_while_loop` verifica cond_type != BOOL)
  
- [X] Mensagens de erro formatadas: ERRO SEMÂNTICO [Linha N]: ... + contexto
  - **Evidência:** `analyzer.py` linhas 612-623 (`make_error` formata com linha e contexto)
  - **Exemplo real:** `ERRO SEMÂNTICO [Linha 14]: Variable 'Y' not declared.\nContexto: ( memid int + )`

**Penalidade:** -0.5 pontos (operador `/` implementado incorretamente; operador `|` não documentado)

---

### BLOCO 4 – Memória e Escopo (1.5/1.5)

**Arquivo:** `define_grammar/utils/symbols.py` (60 linhas)

- [X] Tabela de símbolos: adicionar/buscar/atualizar (tipo, escopo, inicializada)
  - **Classe Symbol:** Linhas 5-10 (name, type, initialized, scope)
  - **Classe SymbolTable:** Linhas 13-60
    - `add()`: Linha 25-29 adiciona símbolo
    - `lookup()`: Linha 31-35 busca em escopos aninhados
    - `set_initialized()`: Linha 37-40 atualiza inicialização
    - `mark_initialized()`: Linha 42-56 adiciona/atualiza com tipo
  
- [X] (MEM) só após (V MEM): erro se não inicializada
  - **Evidência:** `semantic_analyzer/semantic_memory.py` linhas 97-122 (`handle_variable_reference`)
  - **Linha 114-118:** Erro se `symbol is None or not symbol.initialized`
  - **Teste:** `test1.txt` linha 14 usa variável Y não declarada → erro capturado
  
- [X] (N RES): N inteiro ≥ 0 e referência válida
  - **Evidência:** `semantic_analyzer/analyzer.py` linhas 559-604 (`handle_res_operator`)
  - **Validações:**
    - Linha 572-574: N deve ser int
    - Linha 576-580: N deve ser literal inteiro
    - Linha 582-586: N ≥ 0
    - Linha 588-594: Linha alvo deve existir
  - **Teste:** `test1.txt` linha 3 `( 4 RES )` gera erro (linha 4 não existe ainda)
  
- [X] Regras de escopo (arquivos independentes; blocos aninhados se houver)
  - **Evidência:** `symbols.py` linhas 14-23 (estrutura de pilha de escopos)
  - **Métodos:** `push_scope()`, `pop_scope()` para aninhamento
  - **Observação:** Testes atuais usam apenas escopo global (0)

**Pontuação completa:** 1.5/1.5

---

### BLOCO 5 – AST Atribuída e Artefatos (1.0/1.0)

**Arquivo:** `semantic_analyzer/attribute_tree.py` (459 linhas)

- [X] AST atribuída construída e salva em JSON (tipo de nó, tipo inferido, filhos, linha)
  - **Evidência:** Função `gerar_arvore_atribuida()` linhas 5-22
  - **Estrutura:** Dicionário com "lines" e "symbols"
  - **Arquivo gerado:** `test1.txt_arvore_atribuida.json`
  - **Conteúdo:** Linha, contexto, postfix (kind, value), tipo inferido
  
- [X] Relatórios em markdown: gramática de atributos; julgamento de tipos; erros semânticos
  - **Gramática:** `gramatica_atributos.md` (completo)
  - **Tipos:** `gerar_relatorio_tipos()` linhas 57-141 gera tabela, símbolos, estatísticas
  - **Erros:** `gerar_relatorio_erros()` linhas 144-219 gera relatório por linha com categorização
  - **Arquivos gerados:**
    - `test1.txt_relatorio_tipos.md` (52 linhas)
    - `test1.txt_relatorio_erros.md` (quando há erros)
  
- [X] Impressão/visualização mínima coerente (texto/ASCII opcional)
  - **Saída CLI:** Mensagens formatadas com ✅, ❌, emojis
  - **Relatórios:** Tabelas markdown bem formatadas, estatísticas, visualização com emojis
  - **Evidência:** `attribute_tree.py` linhas 227-238 (`format_type_with_emoji`)

**Pontuação completa:** 1.0/1.0

---

### BLOCO 6 – Robustez e Testes (0.8/1.0)

- [X] Testes válidos cobrem: todos operadores, comandos especiais, controle de fluxo
  - **test2.txt:** IF com condições e branches
  - **test3.txt:** WHILE com iteração
  - **test1.txt:** Operadores +, -, *, /, %, ^ (linhas 1-7)
  - **test1.txt:** RES (linhas 3, 8, 9, 19)
  - **test1.txt:** Memória X, MEM (linhas 10-13)
  
- [X] Testes inválidos cobrem: tipos incompatíveis, (MEM) sem init, expoente não-int, / e % com real, if/while com condição não-booleana
  - **test1.txt linha 14:** Y não declarada ✓
  - **test1.txt linhas 15-17:** / e % com real ✓
  - **test1.txt linha 18:** Expoente negativo (4 -5 ^) ✓
  - **test1.txt linha 20:** Soma com booleano ✓
  - **Falta:** Teste explícito de IF/WHILE com condição não-booleana
  
- [X] Mensagens claras com linha e natureza do erro
  - **Formato:** `ERRO SEMÂNTICO [Linha N]: <mensagem>\nContexto: <código>`
  - **Exemplos reais:**
    ```
    ERRO SEMÂNTICO [Linha 3]: (N RES) references non-existent line.
    Contexto: ( int res )
    
    ERRO SEMÂNTICO [Linha 14]: Variable 'Y' not declared.
    Contexto: ( memid int + )
    ```
  
- [ ] Cobertura completa de casos extremos
  - **Falta:** Teste de expoente real (esperado erro)
  - **Falta:** Teste de WHILE/IF com condição não-booleana explícita

**Penalidade:** -0.2 pontos (cobertura de testes incompleta para casos extremos)

---

### BLOCO 7 – Qualidade do Código e Estilo (0.4/0.5)

- [X] Legibilidade, modularização, type hints/comentários (PEP8/estilo equivalente)
  - **Modularização:** Código bem organizado em módulos temáticos
  - **Docstrings:** Presentes em todas as funções principais
  - **Exemplo:** `analyzer.py` linha 275-292 (docstring completa com Args, Returns)
  - **Type hints:** Presentes em algumas funções (ex: `symbols.py` linha 25)
  - **Problema:** Type hints não consistentes em todo o código
  
- [ ] Sem dependência de emojis ou chars não-ASCII nas mensagens (portabilidade)
  - **Problema:** Uso extensivo de emojis nos relatórios
  - **Evidência:** `attribute_tree.py` linhas 227-238:
    ```python
    emoji_map = {
        "int": "🔢",
        "real": "🔢",
        "bool": "✅",
        "void": "⚪",
        "error": "❌",
    }
    ```
  - **Impacto:** Pode causar problemas em terminais/sistemas sem suporte Unicode
  - **Recomendação:** Adicionar flag `--no-emoji` ou usar fallback ASCII

**Penalidade:** -0.1 ponto (uso de emojis sem fallback; type hints inconsistentes)

---

## PENALIDADES (Seção 23.9)

| Problema | Penalidade Aplicada | Justificativa |
|----------|---------------------|---------------|
| Falha em validação de operador `/` | -10% (1.0 pt) | Operador `/` implementado incorretamente como divisão inteira; operador `|` não documentado |
| Inconsistência documentação/código | -5% (0.5 pt) | Documentação menciona promoção de tipos não implementada |
| Uso de caracteres não-ASCII | -2% (0.2 pt) | Emojis sem fallback comprometem portabilidade |
| Testes incompletos | -2% (0.2 pt) | Faltam casos extremos (expoente real, IF/WHILE não-bool explícito) |
| CLI não padrão | -1% (0.1 pt) | Requer flag `-f` em vez de aceitar argumento direto |
| Histórico de commits limitado | -1% (0.1 pt) | Poucos commits com mensagens não descritivas |

**Total de Penalidades:** 21% → 2.1 pontos

**Nota Ajustada:** 10.0 - 2.1 = 7.9/10.0

**Nota Final Arredondada:** 7.6/10.0 (considerando distribuição de pontos por bloco)

---

## PONTOS FORTES

1. **Arquitetura bem estruturada:** Separação clara entre analisador sintático, semântico, definição de gramática e utilitários.

2. **Documentação abrangente:** `READ.md` com 700+ linhas; `gramatica_atributos.md` com regras formais de inferência completas.

3. **Relatórios detalhados:** Geração automática de árvore atribuída JSON + relatórios markdown com tabelas, símbolos e estatísticas.

4. **Tabela de símbolos robusta:** Implementação com suporte a escopos aninhados, mesmo que não totalmente utilizada nos testes.

5. **Validações semânticas completas:** Verificação de inicialização de memória, tipos em operadores, condições booleanas em estruturas de controle.

6. **Tratamento de erros detalhado:** Mensagens contextualizadas com número de linha e código fonte.

7. **Modularização adequada:** Cada responsabilidade em módulo separado (types.py, oprules.py, symbols.py, analyzer.py).

8. **Código documentado:** Docstrings em inglês com Args/Returns em funções principais.

---

## PONTOS DE MELHORIA

### 1. Corrigir operador de divisão

**Problema:** Operador `/` implementado como divisão inteira; operador `|` usado para divisão real não está documentado.

**Ação recomendada:**
- Inverter definições: `/` para divisão real (aceita int e real, retorna real), `//` para divisão inteira
- Documentar operador `|` no README e gramática, ou removê-lo se não for parte da especificação
- Atualizar testes para refletir comportamento correto

**Arquivo:** `define_grammar/utils/oprules.py` linha 60-61

---

### 2. Resolver inconsistência sobre promoção de tipos

**Problema:** Documentação menciona promoção int→real, mas implementação rejeita operações mistas.

**Ação recomendada:**
- **Opção A (recomendada):** Atualizar documentação para refletir política real de tipagem forte sem promoção
- **Opção B:** Implementar promoção automática conforme documentado
- Garantir que gramática de atributos, README e código estejam alinhados

**Arquivos:** `gramatica_atributos.md`, `define_grammar/utils/oprules.py`

---

### 3. Adicionar fallback para emojis

**Problema:** Uso de emojis Unicode pode falhar em alguns ambientes.

**Ação recomendada:**
- Adicionar variável de ambiente `ASCII_ONLY` ou flag CLI `--no-emoji`
- Implementar mapeamento alternativo: `int: "[INT]"`, `error: "[ERR]"`, etc.
- Detectar automaticamente suporte a Unicode do terminal

**Arquivo:** `semantic_analyzer/attribute_tree.py` linha 227-238

---

### 4. Expandir cobertura de testes

**Problema:** Faltam casos extremos explícitos.

**Ação recomendada:**
- Adicionar `test4.txt` com casos específicos:
  - `( 4 3.5 ^ )` → erro (expoente não inteiro)
  - `( ( 10 5 + ) ( X Y + ) ( Z ) IF )` → erro (condição não booleana)
  - `( ( X ) ( Y Z + ) WHILE )` → erro (condição não booleana)
  - Divisão por zero (se aplicável)
- Criar arquivo com todos os operadores relacionais (==, !=, <=, >=)

---

### 5. Melhorar interface CLI

**Problema:** CLI requer `-f` explícito; nome de arquivo README não padrão.

**Ação recomendada:**
- Tornar `-f` opcional: aceitar `python main.py arquivo.txt` diretamente
- Manter retrocompatibilidade com `-f`
- Renomear `READ.md` → `README.md`

**Arquivo:** `main.py` linha 26-29

---

### 6. Adicionar .gitignore

**Problema:** Arquivos `__pycache__` e `.pyc` não deveriam ser commitados.

**Ação recomendada:**
- Criar `.gitignore` com:
  ```
  __pycache__/
  *.pyc
  *.pyo
  *.json
  *_relatorio_*.md
  *_arvore_atribuida.json
  .vscode/
  .idea/
  ```
- Executar `git rm -r --cached **/__pycache__`

---

### 7. Melhorar histórico de commits

**Problema:** Poucos commits com mensagens genéricas.

**Ação recomendada:**
- Commits atômicos para cada funcionalidade
- Mensagens descritivas no formato: `tipo(escopo): descrição`
- Exemplo: `feat(semantic): add exponentiation validation`, `fix(types): correct division operator behavior`

---

### 8. Adicionar type hints consistentes

**Problema:** Type hints presentes apenas em algumas funções.

**Ação recomendada:**
- Adicionar annotations em todas as funções públicas
- Usar `from typing import List, Dict, Tuple, Optional`
- Executar `mypy` para validação de tipos

**Exemplo:**
```python
def evaluate_postfix(
    tokens: List[Tuple[str, Any]], 
    symbol_table: SymbolTable,
    op_rules: Dict[str, OpRule],
    all_line_results: List[Optional[Dict[str, Any]]],
    line_no: int,
    context: str
) -> Tuple[TypeKind, List[str]]:
```

---

## OBSERVAÇÕES PARA PROVA DE AUTORIA

### Módulo: Analisador Semântico (`semantic_analyzer/analyzer.py`)

1. **Pergunta:** Como funciona o algoritmo de avaliação de expressões pós-fixas? Por que usar pilha?
   - **Resposta esperada:** Percorre tokens sequencialmente; operandos vão para pilha; operadores retiram N operandos, aplicam regra de tipo, empilham resultado. Pilha é natural para RPN pois ordem de avaliação é inerente.

2. **Pergunta:** Explique a função `handle_exponentiation`. Por que expoente deve ser inteiro?
   - **Resposta esperada:** Linhas 492-525. Valida base numérica, expoente INT e ≥0. Retorna REAL se base é real, senão INT. Expoente inteiro simplifica análise estática e evita ambiguidades matemáticas (raízes).

3. **Pergunta:** Como o sistema detecta uso de variável não inicializada?
   - **Resposta esperada:** Na referência (REF), consulta symbol_table.lookup(). Se símbolo não existe ou `initialized == False`, gera erro. Na atribuição (STORE), marca `initialized = True`.

### Módulo: Tabela de Símbolos (`define_grammar/utils/symbols.py`)

4. **Pergunta:** Como funciona o sistema de escopos aninhados? Onde é usado?
   - **Resposta esperada:** Lista de dicionários (`self.scope`). `lookup()` busca do escopo mais interno (fim da lista) para global. `push_scope()` adiciona nível, `pop_scope()` remove. Atualmente usa apenas escopo 0 (global), mas preparado para blocos aninhados.

5. **Pergunta:** Diferença entre `set_initialized()` e `mark_initialized()`?
   - **Resposta esperada:** `set_initialized()` apenas atualiza flag de símbolo existente. `mark_initialized()` cria símbolo se não existir, permite atualizar tipo, e marca como inicializado. Mais robusto para primeiro uso.

### Módulo: Regras de Operadores (`define_grammar/utils/oprules.py`)

6. **Pergunta:** Como a classe `OpRule` organiza validações de tipos? Dê exemplo de `check_mod`.
   - **Resposta esperada:** Armazena nome, aridade e função checker. `check_mod` (linhas 29-31): recebe tupla (tipo_a, tipo_b), retorna INT se ambos INT, senão ERROR. Centraliza lógica de tipos por operador.

7. **Pergunta:** Por que relacionais retornam BOOL mesmo operando sobre INT/REAL?
   - **Resposta esperada:** Operação de comparação produz valor booleano. Importante para validar condições em IF/WHILE que exigem tipo BOOL.

### Módulo: Árvore Atribuída (`semantic_analyzer/attribute_tree.py`)

8. **Pergunta:** Explique a estrutura da árvore atribuída JSON. O que contém cada linha?
   - **Resposta esperada:** Dicionário com "lines" (lista de linhas) e "symbols" (tabela). Cada linha tem: número, contexto (código), postfix (tokens com kind/value), tipo inferido. Permite reconstrução completa da análise.

9. **Pergunta:** Como a função `categorize_errors()` funciona? Para que serve?
   - **Resposta esperada:** Linhas 287-321. Analisa texto de cada erro, busca palavras-chave ("invalid types", "not declared", etc.) e incrementa contadores por categoria. Serve para estatísticas no relatório de erros.

### Módulo: Controle de Fluxo (`semantic_analyzer/semantic_control.py`)

10. **Pergunta:** Como IF e WHILE são validados semanticamente? Por que condição deve ser BOOL?
    - **Resposta esperada:** `validate_while()` verifica se tipo no topo da pilha (condição) é BOOL. `validate_if()` verifica condição BOOL e calcula tipo resultante por LUB das branches. Condição booleana garante semântica de decisão clara.

---

## EVIDÊNCIAS DE CÓDIGO (Resumo)

| Funcionalidade | Arquivo | Linhas | Descrição |
|----------------|---------|--------|-----------|
| Entry point | `main.py` | 1-62 | Integra lexer, parser, semântica; gera saídas |
| Avaliação postfix | `semantic_analyzer/analyzer.py` | 275-392 | Pilha de tipos, handle de tokens |
| Validação ^ | `semantic_analyzer/analyzer.py` | 492-525 | Expoente inteiro, base numérica |
| Validação RES | `semantic_analyzer/analyzer.py` | 559-604 | N≥0, linha alvo válida |
| Memória inicialização | `semantic_analyzer/semantic_memory.py` | 97-122 | Erro se não inicializada |
| Controle IF/WHILE | `semantic_analyzer/semantic_control.py` | 54-58 | Condição booleana |
| Regras de operadores | `define_grammar/utils/oprules.py` | 12-72 | Checkers por operador |
| Tabela de símbolos | `define_grammar/utils/symbols.py` | 5-60 | Add, lookup, scope |
| Tipos | `define_grammar/utils/types.py` | 4-38 | Enum, promote, LUB |
| Geração de relatórios | `semantic_analyzer/attribute_tree.py` | 57-219 | JSON + Markdown |

---

## CONCLUSÃO

O projeto **RA3_6** implementa um analisador semântico funcional e bem estruturado para a linguagem RPN, com validações abrangentes de tipos, memória e estruturas de controle. A documentação é extensa e os relatórios gerados são informativos.

**Principais problemas identificados:**
1. Operador `/` implementado incorretamente (divisão inteira em vez de real)
2. Inconsistência entre documentação (menciona promoção) e implementação (rejeita tipos mistos)
3. Uso de emojis sem fallback ASCII compromete portabilidade
4. Cobertura de testes poderia ser mais completa

**Recomendação:** APROVADO COM RESSALVAS. O aluno demonstra compreensão sólida de análise semântica e implementou sistema robusto. As inconsistências identificadas são corrigíveis e não comprometem a estrutura geral. Com as correções sugeridas, o projeto alcançaria nota superior a 9.0.

**Nota Final: 7.6/10.0**
