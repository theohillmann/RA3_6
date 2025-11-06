from syntactic_analyzer.build_grammar.constants import START_SYMBOL, EPS, END


class SyntaxErrorLL1(SyntaxError):
    """Custom exception for LL(1) parsing errors"""

    pass


def parsear(tokens, ll1_table, debug=False):
    """
    LL(1) Descending Parser (with stack), guided by the ll1_table.

    Args:
        tokens (list): List of strings ending with "$" (e.g., ["(", "real", "real", "+", ")", "$"])
        ll1_table (dict): Dict[NonTerminal][terminal] = production (list of symbols)
        debug (bool): Whether to print debug information

    Returns:
        list: List of pairs (NonTerminal, production) applied, in order

    Raises:
        SyntaxErrorLL1: On syntax error
    """
    nonterminals = set(ll1_table.keys())
    parsing_stack = [END, START_SYMBOL]
    current_index = 0
    derivation_steps = []
    step_count = 0

    while parsing_stack:
        stack_top = parsing_stack.pop()
        current_token = get_lookahead(tokens, current_index)

        if debug:
            print_debug_info(
                step_count, stack_top, current_token, tokens, current_index
            )
            step_count += 1

        if stack_top == END:
            if handle_end_marker(stack_top, current_token, tokens, current_index):
                return derivation_steps

        production = handle_nonterminal(
            stack_top, current_token, nonterminals, ll1_table, parsing_stack
        )
        if production is not None:
            derivation_steps.append((stack_top, production))
            continue

        new_index = handle_terminal(stack_top, current_token, tokens, current_index)
        if new_index is not None:
            current_index = new_index
            continue

    if get_lookahead(tokens, current_index) != END:
        raise SyntaxErrorLL1(
            f"Error: remaining tokens after emptying stack: {tokens[current_index:]}"
        )

    return derivation_steps


def get_lookahead(tokens, current_index):
    """Get the current token or END_MARKER if at the end"""
    return tokens[current_index] if current_index < len(tokens) else END


def print_debug_info(step_count, stack_top, current_token, tokens, current_index):
    """Print debug information during parsing"""
    print(
        f"[step {step_count}] STACK(top popped)={stack_top} | "
        f"lookahead={current_token} | rest={tokens[current_index:]}"
    )


def handle_end_marker(stack_top, current_token, tokens, current_index):
    """Handle the end marker case in parsing"""
    if current_token == END:
        return True
    raise SyntaxErrorLL1(
        f"Error: remaining tokens after analysis: {tokens[current_index:]}"
    )


def is_nonterminal(symbol, nonterminals):
    """Check if a symbol is a non-terminal"""
    return symbol in nonterminals


def handle_nonterminal(
    stack_top, current_token, nonterminals, ll1_table, parsing_stack
):
    """Handle non-terminal symbols during parsing"""
    if not is_nonterminal(stack_top, nonterminals):
        return None

    parsing_table_row = ll1_table.get(stack_top, {})
    production = parsing_table_row.get(current_token)

    if production is None:
        expected_tokens = sorted(list(parsing_table_row.keys()))
        raise SyntaxErrorLL1(
            f"Syntax error: unexpected symbol '{current_token}' while expanding {stack_top}. "
            f"Expected one of: {expected_tokens}"
        )

    if not is_epsilon_production(production):
        for symbol in reversed(production):
            parsing_stack.append(symbol)

    return production


def is_epsilon_production(production):
    """Check if a production is an epsilon production"""
    return len(production) == 1 and production[0] == EPS


def handle_terminal(stack_top, current_token, tokens, current_index):
    """Handle terminal symbols during parsing"""
    if stack_top == EPS:
        return current_index

    if stack_top == current_token:
        return current_index + 1

    raise SyntaxErrorLL1(
        f"Error: expected terminal '{stack_top}', but found '{current_token}'. "
        f"Input context: {tokens[max(0, current_index-3):current_index+3]}"
    )


if __name__ == "__main__":
    from build_grammar.build_grammar import (
        construirGramatica,
    )

    g = construirGramatica()
    table = g["table"]
    tests = [
        ["(", "real", "real", "+", ")", "$"],
        [
            "(",
            "(",
            "memid",
            "memid",
            "+",
            ")",
            "(",
            "memid",
            "memid",
            "*",
            ")",
            "/",
            ")",
            "$",
        ],
        ["(", "int", "res", ")", "$"],
        [
            "(",
            "(",
            "memid",
            "memid",
            "+",
            ")",
            "(",
            "memid",
            ")",
            "(",
            "memid",
            ")",
            "if",
            ")",
            "$",
        ],
        ["(", "(", "memid", ")", "(", "memid", ")", "while", ")", "$"],
        ["(", "int", "v", "memid", ")", "$"],
        ["(", "memid", "memid", "+", "memid", ")", "$"],
        ["(", "real", "real", "+", "$"],
        ["(", "+", ")", "$"],
        ["(", "memid", "memid", ">", ")", "$"],
        [
            "(",
            "(",
            "memid",
            "memid",
            ">",
            ")",
            "(",
            "memid",
            ")",
            "(",
            "memid",
            ")",
            "if",
            ")",
            "$",
        ],
    ]

    for tokens in tests:
        print("\nParsing tokens:", tokens)
        try:
            deriv = parsear(tokens, table, debug=False)
            print("\n✅ Expression accepted.")
            print("Derivation:")
            for A, prod in deriv:
                print(f"{A} -> {' '.join(prod)}")
        except SyntaxErrorLL1 as e:
            print("❌", e)
