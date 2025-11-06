from .utils import get_first_of_sequence
from .calcular_first import calcularFirst
from .calcular_follow import calcularFollow
from .constants import NON_TERMINALS, PRODUCTIONS, EPS, TERMINALS, START_SYMBOL


def construirGramatica():
    """
    Build the LL(1) grammar table and related sets.

    Returns:
        dict: Dictionary containing start symbol, nonterminals, terminals, productions, FIRST, FOLLOW, and LL(1) table.
    """
    first = calcularFirst()
    follow = calcularFollow(first)
    table = construirTabelaLL1(first, follow)

    return {
        "start": START_SYMBOL,
        "nonterminals": NON_TERMINALS,
        "terminals": TERMINALS,
        "productions": PRODUCTIONS,
        "FIRST": first,
        "FOLLOW": follow,
        "table": table,
    }


def construirTabelaLL1(first_sets, follow_sets):
    """
    Construct the LL(1) parsing table for the grammar.

    Args:
        first_sets (dict): FIRST sets for all nonterminals.
        follow_sets (dict): FOLLOW sets for all nonterminals.

    Returns:
        dict: LL(1) parsing table mapping nonterminals and lookahead terminals to productions.
    """
    table = {nonterminal: {} for nonterminal in NON_TERMINALS}
    for nonterminal, productions in PRODUCTIONS.items():
        for production in productions:
            first_of_prod = get_first_of_sequence(production, first_sets)
            for terminal in first_of_prod - {EPS}:
                if terminal in table[nonterminal]:
                    raise ValueError(
                        f"LL(1) Conflict: M[{nonterminal}, {terminal}] already defined."
                    )
                table[nonterminal][terminal] = production
            if EPS in first_of_prod:
                for follow_terminal in follow_sets[nonterminal]:
                    if follow_terminal in table[nonterminal]:
                        raise ValueError(
                            f"LL(1) Conflict: M[{nonterminal}, {follow_terminal}] already defined (via ε)."
                        )
                    table[nonterminal][follow_terminal] = [EPS]
    return table
