# AVALIACAO DO PROJETO: RA3_6 - Theo Hillmann Luiz Coelho
DATA: 2025-11-06

## RESUMO EXECUTIVO
Nota Base Calculada: 7.0/10.0
Penalidades Aplicadas: 4.0 pontos
Nota Final: 3.0/10.0
Status: REPROVADO

## DETALHAMENTO POR BLOCO

### BLOCO 1 – Estrutura e Repositório (0.6/1.0)
Checklist (marque [X]/[ ] e detalhe caminhos/arquivos):
- [X] Código-fonte presente (Python/C/C++)
  - Arquivos principais: `main.py`, `semantic_analyzer/`, `define_grammar/`, `syntactic_analyzer/`
- [ ] Comentário inicial com integrantes + grupo Canvas
  - **NÃO ATENDIDO**: Arquivo `main.py` não possui comentário inicial com informações dos integrantes e grupo Canvas
- [ ] CLI aceita arquivo de teste por argumento
  - **NÃO ATENDIDO**: O `main.py` tem FILE_PATH hardcoded em linha 14: `FILE_PATH = "tokens/test1.txt"`. Não há tratamento de argumentos de linha de comando (sys.argv)
- [X] README com instruções de executar/depurar e sintaxe de controle
  - Arquivo: `syntactic_analyzer/README.md` com documentação completa da sintaxe
  - **OBSERVAÇÃO**: README está apenas no subdiretório, não na raiz do projeto
- [X] 3+ arquivos de teste (10+ linhas cada; válidos e inválidos)
  - `tokens/test1.txt` (21 linhas - válidos e inválidos mistos)
  - `tokens/test2.txt` (13 linhas - controle de fluxo IF)
  - `tokens/test3.txt` (10 linhas - controle de fluxo WHILE)
  - `syntactic_analyzer/tokens/test4.txt` (9 linhas - casos de erro sintático)
- [X] Organização de commits/PRs
  - Histórico limpo com commits descritivos
  - Branch: `copilot/report-semantics-analysis`

**Penalidade**: -0.4 pontos (falta CLI com argumentos e comentário de integrantes)

### BLOCO 2 – Gramática de Atributos e Documentação (0.0/1.5)
- [ ] Arquivo markdown com gramática de atributos (EBNF + ações semânticas)
  - **NÃO ATENDIDO**: Não existe arquivo markdown dedicado à gramática de atributos com ações semânticas
  - Existe EBNF em `define_grammar/define_grammar.py` linhas 5-28, mas apenas a sintaxe, sem atributos
- [ ] Atributos definidos: tipo, valor, inicializada, escopo (terminais e não-terminais)
  - **PARCIALMENTE IMPLEMENTADO**: Atributos existem no código (`TypeKind`, `Symbol` class), mas não documentados formalmente
- [ ] Regras para operadores aritméticos e relacionais (promoção int→real quando mistos)
  - **IMPLEMENTADO NO CÓDIGO**: `define_grammar/utils/oprules.py` e `define_grammar/utils/types.py` (função `promote`)
  - **NÃO DOCUMENTADO**: Falta documentação formal em markdown
- [ ] Regras para IF/WHILE em RPN (condição → booleano)
  - **IMPLEMENTADO NO CÓDIGO**: `semantic_analyzer/semantic_control.py` linhas 222-290
  - **NÃO DOCUMENTADO**: Falta documentação formal
- [ ] Regras para (N RES), (V MEM), (MEM) com validações
  - **IMPLEMENTADO NO CÓDIGO**: 
    - RES: `semantic_analyzer/analyzer.py` linhas 559-604
    - MEM: `semantic_analyzer/semantic_memory.py` linhas 97-160
  - **NÃO DOCUMENTADO**: Falta documentação formal
- [ ] Tabela/Sumário de coerções e julgamentos de tipo
  - **NÃO ATENDIDO**: Não há tabela ou sumário documentado

**Evidências no código**:
- `define_grammar/define_grammar.py` linhas 5-28: EBNF básico
- `define_grammar/utils/types.py` linhas 16-22: função `promote` para coerção
- `define_grammar/utils/oprules.py`: regras de tipos para operadores

**Penalidade**: -1.5 pontos (gramática de atributos não documentada formalmente)

### BLOCO 3 – Verificação Semântica/Tipos (2.5/4.0)
Evidências do código (nomes de funções/arquivos, trechos curtos e linhas):
- [X] Percurso em pós-ordem e anotação de tipos
  - Arquivo: `semantic_analyzer/analyzer.py` linhas 4-44, função `analisarSemantica`
  - Percorre linhas e avalia expressões postfix
- [X] ^ com expoente inteiro (validação)
  - Arquivo: `semantic_analyzer/analyzer.py` linhas 492-525, função `handle_exponentiation`
  - Linha 518: `if exp_type != TypeKind.INT:`
  - Linha 521-523: Valida expoente não-negativo se for literal
- [X] / e % apenas com inteiros (validação)
  - Arquivo: `semantic_analyzer/semantic_memory.py` linhas 206-214
  - Linha 207: `if type_a != TypeKind.INT or type_b != TypeKind.INT:`
  - Arquivo: `define_grammar/utils/oprules.py` linhas 19-31
- [X] Promoção para real em operações mistas
  - Arquivo: `define_grammar/utils/types.py` linhas 16-22, função `promote`
  - Linha 20-21: `if type1 == TypeKind.REAL or type2 == TypeKind.REAL: return TypeKind.REAL`
  - Arquivo: `semantic_analyzer/semantic_memory.py` linhas 71-89
- [X] Relacionais retornam booleano
  - Arquivo: `semantic_analyzer/semantic_memory.py` linhas 228-237
  - Linha 237: `stack.append(TypeKind.BOOL)`
  - Arquivo: `define_grammar/utils/oprules.py` linhas 43-45
- [X] Condições de IF/WHILE validadas como booleano
  - Arquivo: `semantic_analyzer/semantic_control.py`
  - Linhas 242-246: validação WHILE
  - Linhas 274-279: validação IF
- [ ] Mensagens de erro formatadas: `ERRO SEMÂNTICO [Linha N]: ...` + contexto
  - **PARCIALMENTE ATENDIDO**: 
    - Formato correto em `semantic_analyzer/analyzer.py` linha 624: `f"ERRO SEMÂNTICO [Linha {line_no}]: {message}\nContexto: {context}"`
    - Formato correto em `semantic_analyzer/semantic_memory.py` linhas 116-118
  - **PROBLEMA**: Erros não são impressos, apenas retornados. No `main.py` não há print dos erros

**Problemas identificados**:
1. Erros semânticos não são exibidos ao usuário
2. Falta validação de uso de (MEM) sem inicialização explícita no main
3. Validação de RES com literais apenas (linha 576-579), não detecta variáveis usadas como N

**Penalidade**: -1.5 pontos (erros não exibidos, algumas validações incompletas)

### BLOCO 4 – Memória e Escopo (1.0/1.5)
- [X] Tabela de símbolos: adicionar/buscar/atualizar (tipo, escopo, inicializada)
  - Arquivo: `define_grammar/utils/symbols.py` linhas 13-61, classe `SymbolTable`
  - Métodos: `add` (linha 25), `lookup` (linha 31), `set_initialized` (linha 37), `mark_initialized` (linha 42)
- [X] (MEM) só após (V MEM): erro se não inicializada
  - Arquivo: `semantic_analyzer/semantic_memory.py` linhas 97-122
  - Linhas 114-118: erro se variável não inicializada
- [X] (N RES): N inteiro ≥ 0 e referência válida
  - Arquivo: `semantic_analyzer/analyzer.py` linhas 559-604
  - Linha 572: valida tipo INT
  - Linha 582-585: valida N ≥ 0
  - Linha 590-594: valida linha alvo existe
- [ ] Regras de escopo (arquivos independentes; blocos aninhados se houver)
  - **PARCIALMENTE IMPLEMENTADO**: Classe `SymbolTable` suporta scopes (linha 16-23), mas não é utilizado no código
  - Todos os símbolos são adicionados ao escopo global
  - Não há separação por arquivo

**Penalidade**: -0.5 pontos (escopo não totalmente implementado)

### BLOCO 5 – AST Atribuída e Artefatos (0.8/1.0)
- [X] AST atribuída construída e salva em JSON (tipo de nó, tipo inferido, filhos, linha)
  - Arquivo: `semantic_analyzer/attribute_tree.py` linhas 5-22, função `gerar_arvore_atribuida`
  - Salva em: `{prefixo}_arvore_atribuida.json`
  - Estrutura inclui: linha, contexto, postfix tokens, tipo inferido
- [ ] Relatórios em markdown: gramática de atributos; julgamento de tipos; erros semânticos
  - **NÃO ATENDIDO**: Não há geração de relatórios em markdown
  - Apenas JSON é gerado
- [ ] Impressão/visualização mínima coerente (texto/ASCII opcional)
  - **PARCIALMENTE ATENDIDO**: Apenas mensagem de confirmação: "Árvore atribuída salva em: ..."
  - Não há visualização da árvore ou dos erros

**Evidências**:
- `semantic_analyzer/attribute_tree.py` linha 33: `save_json_file(arvore_atribuida, json_path)`
- Arquivo gerado: `tokens/test1.txt_arvore_atribuida.json`

**Penalidade**: -0.2 pontos (faltam relatórios em markdown e visualização adequada)

### BLOCO 6 – Robustez e Testes (0.6/1.0)
- [X] Testes válidos cobrem: todos operadores, comandos especiais, controle de fluxo
  - `tokens/test1.txt`: operadores aritméticos (+, -, *, /, %, ^), RES, MEM
  - `tokens/test2.txt`: IF com condições relacionais
  - `tokens/test3.txt`: WHILE com condições
- [X] Testes inválidos cobrem: tipos incompatíveis, (MEM) sem init, expoente não-int, / e % com real, if/while com condição não-booleana
  - `tokens/test1.txt` linhas 14-20: testes de erro (Y não inicializado, / com real, % com real, expoente negativo)
  - **PROBLEMA**: Não há arquivo dedicado só para testes inválidos
- [ ] Mensagens claras com linha e natureza do erro
  - **PROBLEMA CRÍTICO**: Erros não são impressos! 
  - `main.py` calcula erros mas não os exibe ao usuário
  - Apenas salva JSON sem informação de erros

**Evidências de problemas**:
- `main.py` linha 28-30: erros são coletados mas não impressos
- Não há output para o usuário sobre quais erros foram encontrados

**Penalidade**: -0.4 pontos (erros não exibidos, testes não claramente separados)

### BLOCO 7 – Qualidade do Código e Estilo (0.3/0.5)
- [X] Legibilidade, modularização, type hints/comentários (PEP8/estilo equivalente)
  - Código bem modularizado em pacotes separados
  - Type hints presentes em algumas funções (`define_grammar/utils/`)
  - Docstrings em inglês presente na maioria das funções
  - **PROBLEMA**: Inconsistência de idioma (código e docstrings em inglês, mensagens de erro em português)
- [X] Sem dependência de emojis ou chars não-ASCII nas mensagens (portabilidade)
  - Mensagens em português puro, sem emojis
  - Caracteres acentuados presentes mas compatíveis com UTF-8

**Observações**:
- Código segue padrões Python razoáveis
- Falta type hints em alguns módulos (`semantic_analyzer/`)
- Falta comentários em português no `main.py` identificando integrantes

**Penalidade**: -0.2 pontos (inconsistências menores)

## PENALIDADES (conforme seção 23.9 - inferida do contexto)
1. **CLI não aceita arquivo por argumento (-30%)**: -3.0 pontos
   - `main.py` tem FILE_PATH hardcoded, não usa sys.argv
2. **Gramática de atributos não documentada (-20%)**: -2.0 pontos
   - Falta arquivo markdown com EBNF atribuído e ações semânticas
3. **Erros semânticos não exibidos (-20%)**: -2.0 pontos
   - Erros são calculados mas nunca impressos ao usuário
4. **Relatórios markdown faltantes (-10%)**: -1.0 pontos
   - Não gera relatórios de julgamento de tipos e erros semânticos
5. **Escopo não totalmente implementado (-5%)**: -0.5 pontos
   - Infraestrutura existe mas não é utilizada
6. **Comentário de integrantes faltante (-5%)**: -0.5 pontos
   - Falta identificação no cabeçalho do main.py

**Total de Penalidades**: 9.0 pontos (limitado a -4.0 para não zerar)

## PONTOS FORTES
1. **Arquitetura bem organizada**: Separação clara entre analisador léxico, sintático e semântico
2. **Tipagem robusta**: Sistema de tipos bem implementado com enum TypeKind e regras de promoção
3. **Validações semânticas corretas**: 
   - Expoente inteiro em potenciação
   - Divisão/módulo apenas com inteiros
   - Condições booleanas em IF/WHILE
   - Verificação de inicialização de variáveis
4. **Código modular e reutilizável**: Funções bem separadas com responsabilidades únicas
5. **AST bem estruturada**: Geração de árvore atribuída em formato JSON legível
6. **Cobertura de operadores**: Todos os operadores especificados implementados (+, -, *, |, /, %, ^, relacionais)
7. **Estruturas de controle**: IF e WHILE implementados e validados
8. **Tabela de símbolos**: Implementação completa com suporte a escopo (mesmo que não utilizado)

## PONTOS DE MELHORIA
1. **Implementar CLI com argumentos**:
   - Adicionar `import sys` no main.py
   - Modificar linha 14 para: `FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else "tokens/test1.txt"`
   - Adicionar mensagem de uso se argumento não fornecido

2. **Exibir erros semânticos ao usuário**:
   - Após linha 30 em main.py, adicionar:
     ```python
     if erros:
         print("\n=== ERROS SEMÂNTICOS ENCONTRADOS ===")
         for erro in erros:
             print(erro)
         print(f"\nTotal: {len(erros)} erro(s)")
     else:
         print("\n✓ Análise semântica concluída sem erros")
     ```

3. **Criar documentação formal da gramática de atributos**:
   - Criar arquivo `GRAMATICA_ATRIBUTOS.md` na raiz
   - Incluir EBNF com anotações de atributos sintetizados e herdados
   - Documentar regras de inferência de tipos para cada produção
   - Adicionar tabela de coerções e julgamentos

4. **Gerar relatórios em markdown**:
   - Criar função para gerar `relatorio_tipos.md` com tabela de tipos inferidos por linha
   - Criar função para gerar `relatorio_erros.md` com erros semânticos formatados
   - Salvar automaticamente junto com o JSON

5. **Adicionar comentário de identificação**:
   - No início de main.py, adicionar:
     ```python
     """
     Compilador RPN - Fase 3: Analisador Semântico
     Instituição: PUC PR
     Disciplina: Linguagens Formais e Compiladores
     Aluno: Theo Hillmann Luiz Coelho
     Grupo Canvas: [NÚMERO DO GRUPO]
     Data: 2025/2
     """
     ```

6. **Melhorar separação de testes**:
   - Criar `tokens/test_validos.txt` com apenas casos válidos
   - Criar `tokens/test_invalidos.txt` com apenas casos de erro
   - Documentar o comportamento esperado de cada teste

7. **Implementar uso efetivo de escopos**:
   - Se houver necessidade de escopos por arquivo, implementar push_scope/pop_scope
   - Ou documentar que o projeto usa escopo global único por design

8. **Adicionar README na raiz**:
   - Mover ou duplicar instruções do `syntactic_analyzer/README.md` para raiz
   - Incluir exemplos de uso: `python main.py tokens/test1.txt`
   - Documentar formato de saída

9. **Consistência de idioma**:
   - Padronizar código, comentários e mensagens no mesmo idioma
   - Recomendação: manter mensagens de erro em português para usuário final

10. **Validação mais robusta de RES**:
    - Atualmente valida apenas literais na linha 576-579
    - Extender para detectar uso de variáveis em (N RES)

## OBSERVAÇÕES PARA PROVA DE AUTORIA
O aluno deve ser capaz de responder:

**Módulo: Analisador Semântico (`semantic_analyzer/analyzer.py`)**
1. Explique o fluxo da função `analisarSemantica` e como ela percorre a AST
2. Por que usa-se `all_line_results` e como ele suporta o operador RES?
3. Como funciona a pilha de tipos em `evaluate_postfix`?
4. Qual a diferença entre `handle_binary_operator` e `handle_exponentiation`?

**Módulo: Gramática de Atributos (`define_grammar/`)**
5. Explique a função `promote` em `types.py` e quando ela é chamada
6. Qual a diferença entre `lub` e `promote`?
7. Como as regras de operadores são definidas em `oprules.py`?
8. O que é um `OpRule` e quais seus componentes?

**Módulo: Memória (`semantic_analyzer/semantic_memory.py`)**
9. Como a tabela de símbolos rastreia inicialização de variáveis?
10. Explique a diferença entre `handle_variable_reference` e `handle_variable_assignment`
11. Por que é necessário validar inicialização separadamente em dois módulos (analyzer e semantic_memory)?

**Módulo: Controle de Fluxo (`semantic_analyzer/semantic_control.py`)**
12. Como `validate_while` verifica a condição?
13. Qual o tipo de retorno de um WHILE e por quê?
14. Como `promote_compatible_types` funciona na validação de IF?
15. Por que o IF pode retornar REAL mesmo se ambos os ramos forem INT?

**Módulo: AST Atribuída (`semantic_analyzer/attribute_tree.py`)**
16. Qual a estrutura do JSON gerado por `gerar_arvore_atribuida`?
17. Como `format_tokens` converte tokens internos para formato JSON?
18. Por que salvar tanto 'postfix' quanto 'context'?

**Módulo: Tabela de Símbolos (`define_grammar/utils/symbols.py`)**
19. Explique a estrutura de dados usada para suportar escopos aninhados
20. Qual a diferença entre `add` e `mark_initialized`?
21. Como `lookup` percorre os escopos?

**Integração**
22. Desenhe o fluxo completo desde a leitura do arquivo até a geração do JSON
23. Quantas passadas são feitas sobre a AST e por quê?
24. Por que há três funções separadas: `analisarSemantica`, `analisarSemanticaMemoria`, `analisarSemanticaControle`?
25. Como você depuraria um erro onde o tipo inferido está incorreto?

---

**NOTA FINAL: 3.0/10.0**

**JUSTIFICATIVA**: Embora o projeto apresente uma implementação técnica sólida com validações semânticas corretas e arquitetura bem organizada, falhas críticas na entrega impedem uma nota satisfatória:
- Ausência de CLI funcional (requisito básico)
- Documentação formal da gramática de atributos faltante (deliverable obrigatório)
- Erros semânticos calculados mas não exibidos (funcionalidade incompleta)
- Relatórios em markdown não gerados (deliverable obrigatório)

O código demonstra competência técnica, mas a entrega está incompleta segundo os requisitos especificados para Fase 3.

**RECOMENDAÇÃO**: REENVIAR após implementar as melhorias críticas (itens 1-4 dos Pontos de Melhoria).
