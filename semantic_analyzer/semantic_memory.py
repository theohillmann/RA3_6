from define_grammar.utils.types import TypeKind
from semantic_analyzer.utils.ast_utils import extract_rpn_from_ast


def analisarSemanticaMemoria(arvoreSintatica, tabela):
    """
    Validate memory (variable) initialization and usage.

    Operations:
    - Marks variables as initialized on STORE operations
    - Reports errors for REF (usage) of uninitialized variables
    - Validates basic operator types (focus on memory tracking)

    Args:
        arvoreSintatica: Parsed syntax tree
        tabela: Symbol table (modified in place to track initialization)

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
                handle_variable_reference(
                    token, stack, tabela, line_no, context, errors
                )

            elif token_type == "STORE":
                handle_variable_assignment(
                    token, stack, tabela, line_no, context, errors
                )

            elif token_type == "OP":
                operator = str(token[1])
                apply_operator(stack, operator, line_no, context, errors)

            elif token_type in ("WHILE", "IF"):
                # Control flow is checked in semantic_control module
                pass

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


# ============================================================================
# Variable Handling
# ============================================================================


def handle_variable_reference(token, stack, symbol_table, line_no, context, errors):
    """
    Handle variable reference (usage).

    Validates that the variable exists and is initialized before use.

    Args:
        token: Token tuple (type, name)
        stack: Type stack (modified in place)
        symbol_table: Symbol table for lookup
        line_no: Current line number
        context: Context string for errors
        errors: Error list to append to
    """
    var_name = str(token[1])
    symbol = symbol_table.lookup(var_name)

    if symbol is None or not symbol.initialized:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Memória '{var_name}' utilizada sem inicialização\n"
            f"Contexto: {context}"
        )
        stack.append(TypeKind.ERROR)
    else:
        stack.append(symbol.type)


def handle_variable_assignment(token, stack, symbol_table, line_no, context, errors):
    """
    Handle variable assignment (STORE operation).

    Marks the variable as initialized with the type from the stack top.

    Args:
        token: Token tuple (type, name)
        stack: Type stack (modified in place)
        symbol_table: Symbol table (modified to mark initialization)
        line_no: Current line number
        context: Context string for errors
        errors: Error list to append to
    """
    var_name = str(token[1])

    if not stack:
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Armazenamento em '{var_name}' sem valor na pilha\n"
            f"Contexto: {context}"
        )
        return

    value_type = stack.pop()

    if value_type in (TypeKind.ERROR, TypeKind.VOID):
        errors.append(
            f"ERRO SEMÂNTICO [Linha {line_no}]: Valor inválido armazenado em '{var_name}'\n"
            f"Contexto: {context}"
        )

    # Mark variable as initialized with the value's type
    symbol_table.mark_initialized(var_name, value_type)

    # Assignment expression produces the stored value
    stack.append(value_type)


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
