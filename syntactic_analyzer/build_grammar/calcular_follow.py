from .utils import get_first_of_sequence
from .constants import NON_TERMINALS, PRODUCTIONS, EPS, START_SYMBOL, END


def calcularFollow(first_sets):
    """Calculates the FOLLOW sets for all non-terminals in the grammar.

    Args:
        first_sets (dict): Dictionary mapping non-terminals to their FIRST sets.

    Returns:
        dict: Dictionary mapping non-terminals to their FOLLOW sets.
    """
    follow_sets = initialize_follow_sets()
    changed = True
    while changed:
        changed = False
        for lhs_non_terminal, productions in PRODUCTIONS.items():
            for production in productions:
                before = follow_sets.copy()
                add_follow_from_production(
                    lhs_non_terminal, production, first_sets, follow_sets
                )
                # Check if any FOLLOW set changed
                if any(follow_sets[nt] != before[nt] for nt in NON_TERMINALS):
                    changed = True
    return follow_sets


def initialize_follow_sets():
    """Initializes the FOLLOW sets for all non-terminals in the grammar.

    Returns:
        dict: A dictionary mapping non-terminals to their FOLLOW sets.
    """
    FOLLOW = {non_terminal: set() for non_terminal in NON_TERMINALS}
    FOLLOW[START_SYMBOL].add(END)
    return FOLLOW


def add_follow_from_production(lhs_non_terminal, production, first_sets, follow_sets):
    """Updates the FOLLOW sets for non-terminals found in a production.

    Args:
        lhs_non_terminal (str): The left-hand side non-terminal of the production.
        production (list): The sequence of grammar symbols in the production.
        first_sets (dict): Dictionary mapping non-terminals to their FIRST sets.
        follow_sets (dict): Dictionary mapping non-terminals to their FOLLOW sets.

    Returns:
        None
    """
    for index, symbol in enumerate(production):
        if symbol in NON_TERMINALS:
            update_follow_for_non_terminal_in_production(
                lhs_non_terminal, production, index, first_sets, follow_sets
            )


def update_follow_for_non_terminal_in_production(
    lhs_non_terminal, production, index, first_sets, follow_sets
):
    """Updates the FOLLOW set for a specific non-terminal in a production.

    Args:
        lhs_non_terminal (str): The left-hand side non-terminal of the production.
        production (list): The sequence of grammar symbols in the production.
        index (int): The index of the non-terminal in the production.
        first_sets (dict): Dictionary mapping non-terminals to their FIRST sets.
        follow_sets (dict): Dictionary mapping non-terminals to their FOLLOW sets.

    Returns:
        bool: True if the FOLLOW set was changed, False otherwise.
    """
    non_terminal = production[index]
    following_sequence = production[index + 1 :]
    first_of_following = get_first_of_sequence(following_sequence, first_sets)
    previous_follow_size = len(follow_sets[non_terminal])
    follow_sets[non_terminal] |= first_of_following - {EPS}
    if (not following_sequence) or (EPS in first_of_following):
        follow_sets[non_terminal] |= follow_sets[lhs_non_terminal]
    return len(follow_sets[non_terminal]) > previous_follow_size
