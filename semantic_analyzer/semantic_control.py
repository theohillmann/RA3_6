from define_grammar.utils.types import TypeKind
from semantic_analyzer.utils.ast_utils import extract_rpn_from_ast


def analisarSemanticaControle(arvoreSintatica, tabela):
    """
    Validate control flow structures in the syntax tree.

    Validates:
    - WHILE: condition must be BOOL, result is VOID
    - IF: condition must be BOOL, branches must be type-compatible

    Args:
        arvoreSintatica: Parsed syntax tree
        tabela: Symbol table with initialized variables

    Returns:
        List of error messages
    """
    errors = []
    lines = extract_rpn_from_ast(arvoreSintatica)

    for entry in lines:
        line_no = entry["line"]
        context = entry["context"]
        tokens = entry["tokens"]

        stack = []

        for token in tokens:
            token_type = token[0]

            if token_type == "INT":
                stack.append(TypeKind.INT)

            elif token_type == "REAL":
                stack.append(TypeKind.REAL)

            elif token_type == "REF":
                var_name = str(token[1])
                var_type = lookup_variable_type(var_name, tabela)
                stack.append(var_type)

            elif token_type == "STORE":
                var_name = str(token[1])
                var_type = lookup_variable_type(var_name, tabela)
                stack.append(var_type)

            elif token_type == "OP":
                operator = str(token[1])
                apply_operator(stack, operator, line_no, context, errors)

            elif token_type == "WHILE":
                validate_while(stack, line_no, context, errors)

            elif token_type == "IF":
                validate_if(stack, line_no, context, errors)

    return errors


# ============================================================================
# Type Checking Utilities
# ============================================================================


def is_numeric(type_kind):
    """Check if a type is numeric (int or real)."""
    return type_kind in (TypeKind.INT, TypeKind.REAL)


def get_arithmetic_result_type(type_a, type_b):
    """
    Determine result type of arithmetic operation.

    Returns:
        - ERROR if either operand is ERROR or non-numeric
        - REAL if either operand is REAL
        - INT if both operands are INT
    """
    if type_a == TypeKind.ERROR or type_b == TypeKind.ERROR:
        return TypeKind.ERROR

    if not is_numeric(type_a) or not is_numeric(type_b):
        return TypeKind.ERROR

    if type_a == TypeKind.REAL or type_b == TypeKind.REAL:
        return TypeKind.REAL

    return TypeKind.INT


def promote_compatible_types(type_a, type_b):
    """
    Promote compatible types for IF branches.

    Returns:
        - Same type if both match
        - REAL if both are numeric (int/real promotion)
        - ERROR if incompatible
    """
    if type_a == type_b:
        return type_a

    if is_numeric(type_a) and is_numeric(type_b):
        return TypeKind.REAL

    return TypeKind.ERROR


# ============================================================================
# Symbol Table Helpers
# ============================================================================


def lookup_variable_type(var_name, symbol_table):
    """
    Look up variable type in symbol table.

    Args:
        var_name: Variable name
        symbol_table: Symbol table to search

    Returns:
        Variable type or ERROR if not found
    """
    symbol = symbol_table.lookup(var_name)
    return symbol.type if symbol else TypeKind.ERROR


# ============================================================================
# Operator Handling
# ============================================================================


def apply_operator(stack, operator, line_no, context, errors):
    """
    Apply an operator to the type stack and check type correctness.

    Args:
        stack: Type stack (modified in place)
        operator: Operator string
        line_no: Current line number
        context: Context string for errors
        errors: Error list to append to
    """
    if len(stack) < 2:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Operação '{operator}' com operandos insuficientes\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)
        return

    type_b = stack.pop()
    type_a = stack.pop()

    # Arithmetic operators: +, -, *
    if operator in {"+", "-", "*"}:
        result = get_arithmetic_result_type(type_a, type_b)
        stack.append(result)

    # Real division: |
    elif operator == "|":
        if not is_numeric(type_a) or not is_numeric(type_b):
            errors.append(
                f"ERRO SEMÂNTICO [Linha {line_no}]: Divisão real requer operandos numéricos\n"
                f"Contexto: {context}"
            )
            stack.append(TypeKind.ERROR)
        else:
            stack.append(TypeKind.REAL)

    # Integer division and modulo: /, %
    elif operator in {"/", "%"}:
        if type_a != TypeKind.INT or type_b != TypeKind.INT:
            errors.append(
                f"ERRO SEMÂNTICO [Linha {line_no}]: Operador '{operator}' requer operandos inteiros\n"
                f"Contexto: {context}"
            )
            stack.append(TypeKind.ERROR)
        else:
            stack.append(TypeKind.INT)

    # Exponentiation: ^
    elif operator == "^":
        if not is_numeric(type_a) or type_b != TypeKind.INT:
            errors.append(
                f"ERRO SEMÂNTICO [Linha {line_no}]: Potenciação requer base numérica e expoente inteiro\n"
                f"Contexto: {context}"
            )
            stack.append(TypeKind.ERROR)
        else:
            result = TypeKind.REAL if type_a == TypeKind.REAL else TypeKind.INT
            stack.append(result)

    # Relational operators: >, <, >=, <=, ==, !=
    elif operator in {">", "<", ">=", "<=", "==", "!="}:
        if not is_numeric(type_a) or not is_numeric(type_b):
            errors.append(
                f"ERRO SEMÂNTICO [Linha {line_no}]: Operador relacional '{operator}' requer operandos numéricos\n"
                f"Contexto: {context}"
            )
            stack.append(TypeKind.ERROR)
        else:
            stack.append(TypeKind.BOOL)

    # Unknown operator
    else:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Operador '{operator}' não reconhecido\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)


# ============================================================================
# Control Flow Validation
# ============================================================================


def validate_while(stack, line_no, context, errors):
    """
    Validate WHILE structure: expects [condition, body] on stack.

    Args:
        stack: Type stack (modified in place)
        line_no: Current line number
        context: Context string for errors
        errors: Error list to append to
    """
    if len(stack) < 2:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Estrutura WHILE inválida (operandos insuficientes)\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)
        return

    condition_type = stack.pop()

    if condition_type != TypeKind.BOOL:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Condição do WHILE deve ser booleana\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)
    else:
        stack.append(TypeKind.VOID)


def validate_if(stack, line_no, context, errors):
    """
    Validate IF structure: expects [condition, then_branch, else_branch] on stack.

    Args:
        stack: Type stack (modified in place)
        line_no: Current line number
        context: Context string for errors
        errors: Error list to append to
    """
    if len(stack) < 3:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Estrutura IF inválida (operandos insuficientes)\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)
        return

    else_type = stack.pop()
    then_type = stack.pop()
    condition_type = stack.pop()

    if condition_type != TypeKind.BOOL:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Condição do IF deve ser booleana\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)
        return

    result_type = promote_compatible_types(then_type, else_type)

    if result_type == TypeKind.ERROR:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Ramos do IF possuem tipos incompatíveis\n"
            f"Contexto: {context}"
        )

    stack.append(result_type)
