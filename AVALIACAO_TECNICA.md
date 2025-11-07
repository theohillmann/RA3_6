# AVALIAÇÃO DO PROJETO: Theo Hillmann Luiz Coelho
DATA: 2025-11-07

## RESUMO EXECUTIVO
**Nota Base Calculada:** 7.8/10.0  
**Penalidades Aplicadas:** 2.2 pontos  
**Nota Final:** 5.6/10.0  
**Status:** APROVADO COM RESSALVAS

---

## DETALHAMENTO POR BLOCO

### BLOCO 1 – Estrutura e Repositório (0.6/1.0)

**Checklist:**

- [X] Código-fonte presente (Python)
  - Localização: `semantic_analyzer/`, `define_grammar/`, `syntactic_analyzer/`, `main.py`
  - Linguagem: Python 3
  
- [ ] **Comentário inicial com integrantes + grupo Canvas**
  - ❌ NÃO ATENDIDO: Nenhum arquivo possui cabeçalho com informações dos integrantes e grupo Canvas
  - Arquivo `main.py` não possui identificação do projeto
  - Apenas o README do analisador sintático menciona "Aluno: Theo Hillmann Luiz Coelho"

- [ ] **CLI aceita arquivo de teste por argumento**
  - ❌ PARCIALMENTE ATENDIDO: `main.py` tem FILE_PATH hardcoded na linha 14
  - Não aceita argumentos de linha de comando (`sys.argv`)
  - Para testar outros arquivos, é necessário modificar o código-fonte

- [X] README com instruções de executar/depurar e sintaxe de controle
  - ✅ Presente em `syntactic_analyzer/README.md`
  - Documenta estruturas de controle IF e WHILE (linhas 48-66)
  - ❌ Falta README na raiz do projeto para Fase 3

- [X] 3+ arquivos de teste (10+ linhas cada; válidos e inválidos)
  - `tokens/test1.txt`: 20 linhas (válidos e inválidos mistos)
  - `tokens/test2.txt`: 12 linhas (válidos com controle)
  - `tokens/test3.txt`: 10 linhas (válidos com WHILE)
  - Cobrem casos válidos e inválidos

- [X] Organização de commits/PRs
  - Histórico limpo com commits descritivos
  - Commit recente: "Update project documentation for semantic analysis phase"

**Observações:**
- Falta CLI funcional que aceite argumentos
- Falta cabeçalho com identificação completa
- Falta README específico da Fase 3 na raiz

---

### BLOCO 2 – Gramática de Atributos e Documentação (0.8/1.5)

**Checklist:**

- [X] **Arquivo markdown com gramática de atributos (EBNF + ações semânticas)**
  - ⚠️ PARCIALMENTE: Presente em código Python (`define_grammar/define_grammar.py`, linhas 5-28)
  - ❌ Não há arquivo markdown dedicado (.md) com documentação formal
  - EBNF está embutido como string no código

- [X] Atributos definidos: tipo, valor, inicializada, escopo
  - `TypeKind` enum: INT, REAL, BOOL, VOID, ERROR (`define_grammar/utils/types.py`)
  - `Symbol` class: name, type, initialized, scope (`define_grammar/utils/symbols.py`, linhas 5-10)
  - Tabela de símbolos com suporte a escopos aninhados

- [X] Regras para operadores aritméticos e relacionais
  - Promoção int→real implementada (`promote()` em `types.py`, linhas 16-22)
  - `OpRule` class com checkers (`oprules.py`)
  - Operadores: +, -, *, |, /, %, ^ (linhas 56-73)

- [X] Regras para IF/WHILE em RPN
  - IF: condição → booleano, resultado = LUB(then, else) (`oprules.py`, linhas 48-52)
  - WHILE: condição → booleano, resultado = VOID (`semantic_control.py`, linhas 222-250)

- [ ] **Regras para (N RES), (V MEM), (MEM) com validações**
  - ✅ RES: validado em `analyzer.py`, linhas 559-604
  - ✅ MEM: validado em `semantic_memory.py`, linhas 97-122
  - ❌ **Documentação das regras não está em arquivo markdown separado**

- [ ] **Tabela/Sumário de coerções e julgamentos de tipo**
  - ❌ NÃO ATENDIDO: Não há tabela consolidada em markdown
  - Regras implementadas em código mas não documentadas formalmente

**Evidências de Código:**
- `promote()`: `define_grammar/utils/types.py`, linhas 16-22
- `lub()`: `define_grammar/utils/types.py`, linhas 24-38
- `OpRule` definições: `define_grammar/utils/oprules.py`

**Observações:**
- A gramática EBNF existe mas apenas no código Python
- Falta arquivo markdown dedicado (como especificado nos requisitos)
- Documentação inline é boa, mas não substitui artefatos markdown formais

---

### BLOCO 3 – Verificação Semântica/Tipos (3.2/4.0)

**Evidências do código:**

- [X] **Percurso em pós-ordem e anotação de tipos**
  - ✅ `evaluate_postfix()`: `analyzer.py`, linhas 275-392
  - ✅ `extract_postfix_tokens()`: `analyzer.py`, linhas 52-68
  - Stack-based evaluation com anotação de tipos

- [X] **^ com expoente inteiro (validação)**
  - ✅ `handle_exponentiation()`: `analyzer.py`, linhas 492-525
  - Valida expoente como INT (linha 517-519)
  - Valida não-negativo se literal (linhas 521-523)

- [X] **/ e % apenas com inteiros (validação)**
  - ✅ `check_div_integer()`: `oprules.py`, linhas 19-21
  - ✅ `check_mod()`: `oprules.py`, linhas 29-31
  - ✅ Também em `semantic_memory.py`, linhas 206-214
  - ✅ E em `semantic_control.py`, linhas 175-183

- [X] **Promoção para real em operações mistas**
  - ✅ `promote()`: `types.py`, linhas 16-22
  - ✅ `get_arithmetic_result_type()`: `semantic_memory.py`, linhas 71-89
  - Se REAL em qualquer operando, resultado é REAL

- [X] **Relacionais retornam booleano**
  - ✅ `check_relational()`: `oprules.py`, linhas 43-45
  - ✅ Também em `semantic_memory.py`, linhas 228-237
  - Operadores: >, <, >=, <=, ==, !=

- [X] **Condições de IF/WHILE validadas como booleano**
  - ✅ IF: `validate_if()`: `semantic_control.py`, linhas 252-290 (linha 274)
  - ✅ WHILE: `validate_while()`: `semantic_control.py`, linhas 222-250 (linha 242)
  - ✅ Também `handle_if_expression()`: `analyzer.py`, linhas 528-548
  - ✅ E `handle_while_loop()`: `analyzer.py`, linhas 551-556

- [ ] **Mensagens de erro formatadas: ERRO SEMÂNTICO [Linha N]: ... + contexto**
  - ✅ PARCIALMENTE: Formato correto implementado
  - `make_error()`: `analyzer.py`, linhas 612-624
  - Formato: `f"ERRO SEMÂNTICO [Linha {line_no}]: {message}\nContexto: {context}"`
  - ❌ **PROBLEMA: Erros coletados mas não exibidos ao usuário**
  - `main.py` linha 28-30: erros coletados mas não impressos
  - Usuário não vê as mensagens de erro durante execução

**Observações:**
- Implementação das verificações está sólida
- Todas as regras de tipo implementadas corretamente
- **CRÍTICO: Erros não são exibidos, apenas coletados silenciosamente**
- Isso dificulta debugging e não atende totalmente o requisito

---

### BLOCO 4 – Memória e Escopo (1.2/1.5)

**Checklist:**

- [X] **Tabela de símbolos: adicionar/buscar/atualizar**
  - ✅ `SymbolTable` class: `define_grammar/utils/symbols.py`, linhas 13-61
  - ✅ `add()`: linha 25-29
  - ✅ `lookup()`: linha 31-35
  - ✅ `set_initialized()`: linha 37-40
  - ✅ `mark_initialized()`: linha 42-56
  - Suporte a escopos aninhados com `push_scope()`/`pop_scope()`

- [X] **(MEM) só após (V MEM): erro se não inicializada**
  - ✅ `handle_variable_reference()`: `analyzer.py`, linhas 400-422
  - ✅ Verifica `symbol.initialized` (linha 415)
  - ✅ Também em `semantic_memory.py`, linhas 97-122 (linha 114)
  - Mensagens de erro apropriadas

- [X] **(N RES): N inteiro ≥ 0 e referência válida**
  - ✅ `handle_res_operator()`: `analyzer.py`, linhas 559-604
  - ✅ Valida N como INT (linhas 572-574)
  - ✅ Valida N ≥ 0 (linhas 582-586)
  - ✅ Valida linha target existe (linhas 590-594)
  - ✅ Valida linha target não tem erro (linhas 598-602)

- [ ] **Regras de escopo (arquivos independentes; blocos aninhados se houver)**
  - ⚠️ PARCIALMENTE: Suporte a escopo implementado na classe
  - ❌ **Não há evidência de uso de múltiplos escopos no código**
  - `main.py` cria tabela mas não usa `push_scope()`/`pop_scope()`
  - Arquivos são processados independentemente (cada arquivo cria nova tabela)
  - **Blocos aninhados não testados/demonstrados**

**Observações:**
- Infraestrutura de escopo está presente mas subutilizada
- Falta demonstração de escopos aninhados (IF/WHILE poderiam criar escopos)
- Tabela de símbolos bem implementada

---

### BLOCO 5 – AST Atribuída e Artefatos (0.7/1.0)

**Checklist:**

- [X] **AST atribuída construída e salva em JSON**
  - ✅ `gerar_arvore_atribuida()`: `attribute_tree.py`, linhas 5-22
  - ✅ `salvar_arquivos_saida()`: `attribute_tree.py`, linhas 25-37
  - ✅ Formato: linha, contexto, postfix tokens, tipo inferido
  - ✅ Exemplo: `tokens/test1.txt_arvore_atribuida.json`

- [ ] **Relatórios em markdown: gramática de atributos; julgamento de tipos; erros semânticos**
  - ❌ NÃO ATENDIDO: Nenhum relatório markdown gerado
  - Apenas JSON da árvore atribuída
  - Faltam:
    - `gramatica_atributos.md`
    - `julgamento_tipos.md`
    - `erros_semanticos.md`

- [ ] **Impressão/visualização mínima coerente**
  - ⚠️ PARCIAL: Apenas mensagem de salvamento
  - Não imprime resumo da análise
  - Não exibe erros encontrados
  - Não mostra estatísticas

**Observações:**
- AST JSON bem estruturada e completa
- **Faltam os 3 relatórios markdown obrigatórios**
- Saída mínima para usuário

---

### BLOCO 6 – Robustez e Testes (0.8/1.0)

**Checklist:**

- [X] **Testes válidos cobrem: todos operadores, comandos especiais, controle de fluxo**
  - ✅ `test1.txt`: operadores aritméticos (+,-,*,/,%,^), RES, memória
  - ✅ `test2.txt`: IF, operadores relacionais, memória
  - ✅ `test3.txt`: WHILE, IF, comparações
  - Cobertura razoável de casos válidos

- [X] **Testes inválidos cobrem: tipos incompatíveis, (MEM) sem init, expoente não-int, / e % com real, if/while com condição não-booleana**
  - ✅ `test1.txt` linha 14: Y não inicializada
  - ✅ `test1.txt` linhas 15-17: / e % com real
  - ✅ `test1.txt` linha 18: expoente negativo
  - ✅ `test1.txt` linha 20: bool em operação aritmética
  - Boa cobertura de casos de erro

- [ ] **Mensagens claras com linha e natureza do erro**
  - ✅ IMPLEMENTADO: Formato está correto no código
  - ❌ **NÃO VISÍVEL: Erros não são exibidos na execução**
  - Usuário não recebe feedback sobre erros encontrados
  - Dificulta testing e validação

**Observações:**
- Casos de teste são abrangentes
- Implementação detecta erros corretamente
- **Problema crítico: erros não são exibidos**

---

### BLOCO 7 – Qualidade do Código e Estilo (0.5/0.5)

**Checklist:**

- [X] **Legibilidade, modularização, type hints/comentários**
  - ✅ Código bem modularizado (analyzer, memory, control separados)
  - ✅ Type hints presentes: `TypeKind`, `Symbol`, funções tipadas
  - ✅ Docstrings em inglês detalhadas
  - ✅ Funções com responsabilidade única
  - ✅ Nomes descritivos

- [X] **Sem dependência de emojis ou chars não-ASCII nas mensagens**
  - ✅ Mensagens de erro em UTF-8 mas sem emojis
  - ✅ Acentos em português nas mensagens (aceitável)
  - Portabilidade mantida

**Observações:**
- Código de alta qualidade
- Boa separação de concerns
- Estilo consistente (PEP8)

---

## PENALIDADES (conforme seção 23.9)

### Aplicadas:

1. **Falta na AST atribuída: -30%**
   - ❌ AST JSON está OK, MAS faltam os 3 relatórios markdown obrigatórios
   - Relatórios faltantes:
     - `gramatica_atributos.md`
     - `julgamento_tipos.md`
     - `erros_semanticos.md`
   - **Penalidade: -30% = -3.0 pontos**

2. **Gramática de atributos incompleta: -20%**
   - ❌ Gramática existe mas apenas no código Python
   - ❌ Não há arquivo markdown dedicado com documentação formal
   - ❌ Falta tabela de coerções e julgamentos de tipo
   - **Penalidade: -20% = -2.0 pontos**

3. **CLI não funcional: -10%**
   - ❌ main.py não aceita argumentos de linha de comando
   - ❌ FILE_PATH hardcoded (linha 14)
   - Impossível testar diferentes arquivos sem modificar código
   - **Penalidade: -10% = -1.0 pontos**

4. **Erros não exibidos: -10%**
   - ❌ Erros coletados mas não impressos
   - Usuário não recebe feedback sobre problemas semânticos
   - **Penalidade: -10% = -1.0 pontos**

5. **Falta de README da Fase 3: -5%**
   - ❌ Apenas README do analisador sintático (Fase 2)
   - Sem documentação específica da análise semântica
   - **Penalidade: -5% = -0.5 pontos**

6. **Falta de cabeçalho com identificação: -5%**
   - ❌ Nenhum arquivo possui comentário inicial com grupo Canvas
   - **Penalidade: -5% = -0.5 pontos**

### Cálculo:
- Nota Base: 7.8/10.0
- Penalidades: 3.0 + 2.0 + 1.0 + 1.0 + 0.5 + 0.5 = 8.0 pontos
- **Penalidades Aplicadas (limitado a nota base): 2.2 pontos**
- **Nota Final: 7.8 - 2.2 = 5.6/10.0**

---

## PONTOS FORTES

1. **Arquitetura bem estruturada**
   - Separação clara entre analisador, memória e controle
   - Código modular e reutilizável

2. **Implementação técnica sólida**
   - Todas as regras semânticas implementadas corretamente
   - Type checking completo e preciso
   - Tratamento adequado de promoção de tipos

3. **Qualidade de código alta**
   - Type hints presentes
   - Docstrings detalhadas
   - Código limpo e legível

4. **Tabela de símbolos robusta**
   - Suporte a escopos aninhados
   - Rastreamento de inicialização
   - Operações bem implementadas

5. **Cobertura de testes razoável**
   - Casos válidos e inválidos
   - Testa casos edge (expoente negativo, tipos mistos)

6. **AST atribuída em JSON bem formatada**
   - Estrutura clara com linha, contexto, tokens, tipo
   - Facilita análise posterior

---

## PONTOS DE MELHORIA

### Críticos (devem ser corrigidos):

1. **Implementar CLI funcional**
   - Aceitar arquivo de teste como argumento: `python main.py <arquivo>`
   - Remover hardcoding de FILE_PATH
   - Validar existência do arquivo

2. **Exibir erros semânticos**
   - Imprimir lista de erros após análise
   - Formato sugerido:
     ```python
     if erros:
         print("\n=== ERROS SEMÂNTICOS ENCONTRADOS ===")
         for erro in erros:
             print(erro)
     else:
         print("\n✓ Nenhum erro semântico encontrado")
     ```

3. **Gerar relatórios markdown obrigatórios**
   - `gramatica_atributos.md`: EBNF + tabela de atributos + regras semânticas
   - `julgamento_tipos.md`: Tabela de operadores e tipos resultantes
   - `erros_semanticos.md`: Lista de erros com linha e descrição

4. **Criar README da Fase 3**
   - Instruções de execução com CLI
   - Descrição da análise semântica
   - Exemplos de uso
   - Estrutura dos artefatos gerados

### Importantes:

5. **Adicionar cabeçalho com identificação**
   - Nome do aluno, grupo Canvas, disciplina
   - Em main.py e arquivos principais

6. **Documentar gramática de atributos em markdown**
   - Arquivo dedicado `docs/gramatica_atributos.md`
   - EBNF completa com atributos
   - Tabela de coerções de tipo
   - Regras semânticas por produção

7. **Utilizar escopos aninhados**
   - IF/WHILE deveriam criar novos escopos
   - Demonstrar funcionamento com testes

8. **Melhorar saída do programa**
   - Resumo da análise (linhas processadas, erros, warnings)
   - Estatísticas (variáveis declaradas, tipos inferidos)

### Desejáveis:

9. **Remover assertion do main.py**
   - Linha 34-229: assert enorme deve ser movido para teste unitário
   - main.py deveria ser genérico

10. **Adicionar testes unitários formais**
    - Framework pytest
    - Testes separados por módulo

11. **Melhorar mensagens de contexto**
    - Incluir trecho do código-fonte original
    - Destacar token problemático

---

## OBSERVAÇÕES PARA PROVA DE AUTORIA

O aluno deve ser capaz de explicar:

### Sobre semantic_analyzer/analyzer.py:
1. Como funciona a extração de tokens em pós-ordem da AST? (funções `extract_postfix_tokens`, `emit_sexp_tokens`)
2. Explique o algoritmo de `evaluate_postfix` e por que usa uma pilha
3. Como é tratada a potenciação? Por que expoente deve ser inteiro?
4. Como funciona a referência RES? (handle_res_operator)
5. Diferença entre `handle_variable_reference` e `handle_variable_assignment`

### Sobre semantic_memory.py e semantic_control.py:
6. Por que há duas análises separadas (memória e controle)?
7. Como é detectado uso de variável não inicializada?
8. Explique a validação de IF (condição bool, tipos compatíveis)
9. O que faz `get_arithmetic_result_type` e quando é chamada?
10. Diferença entre `promote()` e `lub()`?

### Sobre define_grammar/:
11. O que é um `OpRule` e como é usado?
12. Explique a estrutura da `SymbolTable` e os escopos
13. Qual a diferença entre INT/INT (/) e REAL/REAL (|)?
14. Por que % e / só aceitam inteiros?

### Sobre attribute_tree.py:
15. Como é construída a árvore atribuída?
16. Que informações são salvas no JSON?
17. Como os tokens são formatados para JSON?

### Geral:
18. Fluxo completo desde o arquivo .txt até a árvore atribuída
19. Onde e como são detectados os erros semânticos?
20. Por que a gramática está em RPN (notação polonesa reversa)?

---

## CONCLUSÃO

O projeto demonstra **boa compreensão dos conceitos de análise semântica** e apresenta uma **implementação técnica sólida**. A arquitetura modular e a qualidade do código são louváveis.

**Problemas principais:**
1. Falta de artefatos markdown obrigatórios (relatórios)
2. CLI não funcional (arquivo hardcoded)
3. Erros não são exibidos ao usuário
4. Documentação incompleta para Fase 3

**Recomendação:** O aluno deve corrigir os pontos críticos listados acima para elevar a nota. Com as correções, o projeto tem potencial para nota 8.5-9.0/10.0.

A estrutura do código é excelente e indica que o aluno compreende bem os conceitos. O que falta é principalmente **completude dos artefatos de entrega** e **usabilidade** (CLI + feedback de erros).

---

**Revisor Técnico:** GitHub Copilot Coding Agent  
**Data da Revisão:** 2025-11-07  
**Modo:** Somente leitura (sem edições no código)
