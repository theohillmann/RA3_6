"""
Compilador RPN - Fase 3: Analisador Semântico
Instituição: PUC PR
Disciplina: Linguagens Formais e Compiladores
Aluno: Theo Hillmann Luiz Coelho
Grupo Canvas: RA3_6
Data: 2025/2
"""

import json
import argparse

from define_grammar.define_grammar import definirGramaticaAtributos
from semantic_analyzer.analyzer import analisarSemantica
from syntactic_analyzer.main import main as syntactic_main
from semantic_analyzer.semantic_memory import analisarSemanticaMemoria
from semantic_analyzer.semantic_control import analisarSemanticaControle
from define_grammar.utils.symbols import SymbolTable
from semantic_analyzer.attribute_tree import (
    salvar_arquivos_saida,
    gerar_arvore_atribuida,
)


parser = argparse.ArgumentParser(description="Run syntactic and semantic analyzers")
parser.add_argument(
    "-f", "--file", dest="FILE_PATH", help="Path to the token file (txt)"
)
args = parser.parse_args()

FILE_PATH = args.FILE_PATH

grammar = definirGramaticaAtributos()
st = grammar["symbol_table"]
table = SymbolTable()

with open(FILE_PATH, "r") as file:
    source_lines = [ln.strip() for ln in file if ln.strip()]

syntactic_main(FILE_PATH, debug=False, source_lines=source_lines)

with open(FILE_PATH.replace("txt", "json"), "r") as file:
    ast = json.load(file)

types, errors, anot = analisarSemantica(ast, grammar)

errors += analisarSemanticaMemoria(ast, table)
errors += analisarSemanticaControle(ast, table)

arvore_atribuida = gerar_arvore_atribuida(anot, table)
prefixo = FILE_PATH.replace(".json", "")

if errors:
    print("\n=== ERROS SEMÂNTICOS ENCONTRADOS ===")
    for erro in errors:
        print(erro)
    print(f"\nTotal: {len(errors)} erro(s)")
else:
    print("\n✓ Análise semântica concluída sem erros")

salvar_arquivos_saida(arvore_atribuida, prefixo=prefixo)
