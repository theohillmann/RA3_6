from define_grammar.utils.types import TypeKind


def analisarSemantica(arvore_por_linha, grammar_pkg):
    """
    Perform semantic analysis on parsed program lines.

    Args:
        arvore_por_linha: Dictionary mapping context strings to program ASTs
        grammar_pkg: Dictionary containing 'op_rules' and 'symbol_table'

    Returns:
        Tuple of (types_per_line, errors, annotations)
    """
    op_rules = grammar_pkg["op_rules"]
    symbol_table = grammar_pkg["symbol_table"]

    types_per_line = []
    errors = []
    annotations = []
    all_line_results = [None]  # 1-indexed list of line results

    for line_no, (context_str, program_ast) in enumerate(
        arvore_por_linha.items(), start=1
    ):
        tokens = extract_postfix_tokens(program_ast)

        line_type, line_errors = evaluate_postfix(
            tokens, symbol_table, op_rules, all_line_results, line_no, context_str
        )

        types_per_line.append(line_type)
        errors.extend(line_errors)

        line_info = {
            "line": line_no,
            "context": context_str,
            "tokens": tokens,
            "type": line_type,
        }
        annotations.append(line_info)
        all_line_results.append(line_info)

    return types_per_line, errors, annotations


# ============================================================================
# AST Navigation and Token Extraction
# ============================================================================


def extract_postfix_tokens(program_ast):
    """
    Extract postfix tokens from a program AST.

    Args:
        program_ast: Root node of the abstract syntax tree

    Returns:
        List of tokens in postfix order
    """
    sexp = find_node(program_ast, "SEXP")
    if sexp is None:
        return []

    tokens = []
    emit_sexp_tokens(sexp, tokens)
    return tokens


def find_node(node, label):
    """
    Recursively find the first node with the given label.

    Args:
        node: Current AST node (dict)
        label: Label string to search for

    Returns:
        First matching node or None
    """
    if not isinstance(node, dict):
        return None

    if node.get("label") == label:
        return node

    for child in node.get("children", []):
        result = find_node(child, label)
        if result is not None:
            return result

    return None


def find_immediate_child(node, label):
    """
    Find an immediate child node with the given label.

    Args:
        node: Parent node
        label: Label to search for

    Returns:
        Matching child or None
    """
    for child in node.get("children", []):
        if child.get("label") == label:
            return child
    return None


def has_descendant_label(node, label):
    """
    Check if node has a descendant (or is itself) with the given label.

    Args:
        node: Root node to search from
        label: Label to search for

    Returns:
        True if label found anywhere in subtree
    """
    if node.get("label") == label:
        return True

    for child in node.get("children", []):
        if has_descendant_label(child, label):
            return True

    return False


# ============================================================================
# Token Emission from AST
# ============================================================================


def emit_sexp_tokens(sexp_node, tokens):
    """
    Emit tokens from an SEXP node into the tokens list.

    Args:
        sexp_node: SEXP AST node
        tokens: Output list to append tokens to
    """
    form = find_immediate_child(sexp_node, "FORM")
    if form:
        emit_form_tokens(form, tokens)


def emit_form_tokens(form_node, tokens):
    """
    Emit tokens from a FORM node in postfix order.

    FORM structure: STACKTERM [TAIL1 [TAIL2]]
    Handles assignments, binary ops, relational ops, IF, WHILE, and RES.

    Args:
        form_node: FORM AST node
        tokens: Output list to append tokens to
    """

    # Emit first operand
    stackterm = find_immediate_child(form_node, "STACKTERM")
    if stackterm:
        emit_stackterm_tokens(stackterm, tokens)

    # Check for TAIL1 (continuation)
    tail1 = find_immediate_child(form_node, "TAIL1")
    if not tail1:
        return

    # Handle assignment pattern: STACKTERM ; mem_store(IDENT)
    mem_store = find_immediate_child(tail1, "mem_store")
    if mem_store:
        ident = find_node(mem_store, "IDENT")
        name = ident.get("lexeme", "?") if ident else "?"
        tokens.append(("STORE", name))
        return

    # Handle RES pattern: STACKTERM ; res
    if find_immediate_child(tail1, "res"):
        tokens.append(("RES",))
        return

    # Handle binary/relational/IF/WHILE patterns
    # Emit second operand from TAIL1
    stackterm2 = find_immediate_child(tail1, "STACKTERM")
    if stackterm2:
        emit_stackterm_tokens(stackterm2, tokens)

    # Find TAIL2 (can be sibling in FORM or nested in TAIL1)
    tail2 = find_immediate_child(form_node, "TAIL2")
    if not tail2:
        tail2 = find_immediate_child(tail1, "TAIL2") or find_node(tail1, "TAIL2")

    if not tail2:
        return

    # Handle binary operators
    op_node = find_node(tail2, "OP")
    if op_node:
        for child in op_node.get("children", []):
            op_label = child.get("label")
            if op_label:
                tokens.append(("OP", op_label))
        return

    # Handle IF: emit else branch and IF token
    stackterm3 = find_immediate_child(tail2, "STACKTERM") or find_node(
        tail2, "STACKTERM"
    )
    if stackterm3:
        emit_stackterm_tokens(stackterm3, tokens)
        if has_descendant_label(tail2, "IF"):
            tokens.append(("IF",))
        return

    # Handle WHILE
    if has_descendant_label(tail2, "WHILE"):
        tokens.append(("WHILE",))


def emit_stackterm_tokens(stackterm_node, tokens):
    """
    Emit tokens from a STACKTERM node.

    STACKTERM can contain:
    - An immediate SEXP (sub-expression)
    - A VALUE with INT_LIT, REAL_LIT, or IDENT

    Args:
        stackterm_node: STACKTERM AST node
        tokens: Output list to append tokens to
    """
    # Check for nested SEXP first
    inner_sexp = find_immediate_child(stackterm_node, "SEXP")
    if inner_sexp:
        emit_sexp_tokens(inner_sexp, tokens)
        return

    # Check for VALUE node
    value = find_immediate_child(stackterm_node, "VALUE")
    if not value:
        # Fallback: deep search for SEXP
        deep_sexp = find_node(stackterm_node, "SEXP")
        if deep_sexp:
            emit_sexp_tokens(deep_sexp, tokens)
        return

    # Emit integer literal
    int_lit = find_immediate_child(value, "INT_LIT")
    if int_lit and "lexeme" in int_lit:
        tokens.append(("INT", int(int_lit["lexeme"])))
        return

    # Emit real literal
    real_lit = find_immediate_child(value, "REAL_LIT")
    if real_lit and "lexeme" in real_lit:
        tokens.append(("REAL", float(real_lit["lexeme"])))
        return

    # Emit identifier reference
    ident = find_immediate_child(value, "IDENT")
    if ident and "lexeme" in ident:
        tokens.append(("REF", ident["lexeme"]))


# ============================================================================
# Postfix Expression Evaluator
# ============================================================================


def evaluate_postfix(
    tokens, symbol_table, op_rules, all_line_results, line_no, context
):
    """
    Evaluate types of a postfix expression and check for semantic errors.

    Args:
        tokens: List of postfix tokens
        symbol_table: Symbol table for variable lookup
        op_rules: Dictionary of operator type rules
        all_line_results: List of results from previous lines (for RES)
        line_no: Current line number
        context: Context string for error messages

    Returns:
        Tuple of (result_type, errors_list)
    """
    stack = []  # Stack of (type, value) tuples
    errors = []

    def pop_operands(count):
        """Pop count operands from stack, padding with ERROR if insufficient."""
        if len(stack) < count:
            errors.append(
                make_error(line_no, "Insufficient operands on stack.", context)
            )
            missing = count - len(stack)
            result = stack[:] + [(TypeKind.ERROR, None)] * missing
            stack.clear()
            return result

        operands = stack[-count:]
        del stack[-count:]
        return operands

    for token in tokens:
        token_type = token[0]

        # Integer literal
        if token_type == "INT":
            stack.append((TypeKind.INT, token[1]))

        # Real literal
        elif token_type == "REAL":
            stack.append((TypeKind.REAL, token[1]))

        # Variable reference
        elif token_type == "REF":
            var_name = token[1]
            result_type = handle_variable_reference(
                var_name, symbol_table, line_no, context, errors
            )
            stack.append((result_type, None))

        # Variable assignment
        elif token_type == "STORE":
            var_name = token[1]
            (value_type, _) = pop_operands(1)[0]
            handle_variable_assignment(
                var_name, value_type, symbol_table, line_no, context, errors
            )
            stack.append((value_type, None))

        # Binary/relational operators
        elif token_type == "OP":
            operator = token[1]

            # Special case: exponentiation
            if operator == "^":
                result_type = handle_exponentiation(stack, line_no, context, errors)
                stack.append((result_type, None))
                continue

            # General binary operators
            result_type = handle_binary_operator(
                operator, stack, op_rules, line_no, context, errors, pop_operands
            )
            stack.append((result_type, None))

        # IF expression
        elif token_type == "IF":
            (cond_type, _), (then_type, _), (else_type, _) = pop_operands(3)
            result_type = handle_if_expression(
                cond_type, then_type, else_type, op_rules, line_no, context, errors
            )
            stack.append((result_type, None))

        # WHILE loop
        elif token_type == "WHILE":
            (cond_type, _), (body_type, _) = pop_operands(2)
            handle_while_loop(cond_type, line_no, context, errors)
            stack.append((TypeKind.VOID, None))

        # RES (result reference)
        elif token_type == "RES":
            result_type = handle_res_operator(
                stack, all_line_results, line_no, context, errors
            )
            stack.append((result_type, None))

        # Unknown token
        else:
            errors.append(make_error(line_no, f"Unknown token: {token}", context))
            stack.append((TypeKind.ERROR, None))

    # Determine final type
    if len(stack) == 0:
        return TypeKind.VOID, errors

    if len(stack) > 1:
        errors.append(
            make_error(
                line_no, "Malformed expression (excess items on stack).", context
            )
        )

    final_type, _ = stack[-1]
    return final_type, errors


# ============================================================================
# Semantic Handlers
# ============================================================================


def handle_variable_reference(var_name, symbol_table, line_no, context, errors):
    """
    Handle a variable reference, checking declaration and initialization.

    Returns:
        Type of the variable (or ERROR)
    """
    symbol = symbol_table.lookup(var_name)

    if symbol is None:
        errors.append(
            make_error(line_no, f"Variable '{var_name}' not declared.", context)
        )
        return TypeKind.ERROR

    if not symbol.initialized:
        errors.append(
            make_error(
                line_no, f"Variable '{var_name}' used before initialization.", context
            )
        )

    return symbol.type


def handle_variable_assignment(
    var_name, value_type, symbol_table, line_no, context, errors
):
    """
    Handle variable assignment, including type coercion and initialization.
    """
    symbol = symbol_table.lookup(var_name)

    if symbol is None:
        # Declare new variable with inferred type
        symbol_table.add(var_name, value_type, True)
    else:
        # Check type compatibility (allow int -> real coercion)
        if symbol.type == TypeKind.REAL and value_type == TypeKind.INT:
            symbol_table.set_initialized(var_name)
        elif symbol.type == value_type:
            symbol_table.set_initialized(var_name)
        else:
            errors.append(
                make_error(
                    line_no,
                    f"Type mismatch in assignment to '{var_name}' "
                    f"(expected {symbol.type.value}, got {value_type.value}).",
                    context,
                )
            )
            symbol_table.set_initialized(var_name)


def handle_binary_operator(
    operator, stack, op_rules, line_no, context, errors, pop_operands
):
    """
    Handle a binary operator, checking type rules.

    Returns:
        Result type
    """
    rule = op_rules.get(operator)

    if rule is None:
        errors.append(
            make_error(line_no, f"Operator '{operator}' not supported.", context)
        )
        return TypeKind.ERROR

    if rule.arity != 2:
        errors.append(
            make_error(line_no, f"Unexpected arity for '{operator}'.", context)
        )
        return TypeKind.ERROR

    (type_b, _), (type_a, _) = pop_operands(2)
    result_type = rule.checker((type_a, type_b))

    if result_type == TypeKind.ERROR:
        errors.append(
            make_error(
                line_no,
                f"Invalid types for '{operator}' ({type_a.value}, {type_b.value}).",
                context,
            )
        )

    return result_type


def handle_exponentiation(stack, line_no, context, errors):
    """
    Handle exponentiation operator with special rules:
    - Base: int or real
    - Exponent: int (non-negative if literal)
    - Result: real if base is real, else int

    Returns:
        Result type
    """
    if len(stack) < 2:
        errors.append(
            make_error(line_no, "Exponentiation requires two operands.", context)
        )
        return TypeKind.ERROR

    (exp_type, exp_value) = stack.pop()
    (base_type, base_value) = stack.pop()

    if base_type not in (TypeKind.INT, TypeKind.REAL):
        errors.append(
            make_error(line_no, "Base of exponentiation must be numeric.", context)
        )
        return TypeKind.ERROR

    if exp_type != TypeKind.INT:
        errors.append(make_error(line_no, "Exponent must be integer.", context))
        return TypeKind.ERROR

    if isinstance(exp_value, int) and exp_value < 0:
        errors.append(make_error(line_no, "Exponent must be non-negative.", context))
        return TypeKind.ERROR

    return TypeKind.REAL if base_type == TypeKind.REAL else TypeKind.INT


def handle_if_expression(
    cond_type, then_type, else_type, op_rules, line_no, context, errors
):
    """
    Handle IF expression type checking.

    Returns:
        Result type
    """
    result_type = op_rules["IF"].checker((cond_type, then_type, else_type))

    if result_type == TypeKind.ERROR:
        errors.append(
            make_error(
                line_no,
                "Invalid types in IF (condition must be bool; branches must be compatible).",
                context,
            )
        )

    return result_type


def handle_while_loop(cond_type, line_no, context, errors):
    """
    Handle WHILE loop type checking.
    """
    if cond_type != TypeKind.BOOL:
        errors.append(make_error(line_no, "WHILE condition must be boolean.", context))


def handle_res_operator(stack, all_line_results, line_no, context, errors):
    """
    Handle RES operator: (N RES) references the result of line (current - N).

    Returns:
        Type of referenced line (or ERROR)
    """
    if not stack:
        errors.append(make_error(line_no, "RES requires N on stack.", context))
        return TypeKind.ERROR

    (n_type, n_value) = stack.pop()

    if n_type != TypeKind.INT:
        errors.append(make_error(line_no, "N in (N RES) must be integer.", context))
        return TypeKind.ERROR

    if not isinstance(n_value, int):
        errors.append(
            make_error(line_no, "N in (N RES) must be integer literal.", context)
        )
        return TypeKind.ERROR

    if n_value < 0:
        errors.append(
            make_error(line_no, "N in (N RES) must be non-negative.", context)
        )
        return TypeKind.ERROR

    target_line = line_no - n_value

    if target_line < 1 or target_line >= len(all_line_results):
        errors.append(
            make_error(line_no, "(N RES) references non-existent line.", context)
        )
        return TypeKind.ERROR

    line_info = all_line_results[target_line]

    if line_info is None or line_info["type"] == TypeKind.ERROR:
        errors.append(
            make_error(line_no, "(N RES) references invalid expression.", context)
        )
        return TypeKind.ERROR

    return line_info["type"]


# ============================================================================
# Utilities
# ============================================================================


def make_error(line_no, message, context):
    """
    Format a semantic error message.

    Args:
        line_no: Line number where error occurred
        message: Error message
        context: Context string

    Returns:
        Formatted error string
    """
    return f"ERRO SEMÂNTICO [Linha {line_no}]: {message}\nContexto: {context}"
