from typing import Dict
from .utils import get_first_of_sequence
from .constants import NON_TERMINALS, TERMINALS, PRODUCTIONS, EPS


def calcularFirst():
    """
    Calculates the FIRST sets for all non-terminals in the grammar.

    Returns:
        dict: A dictionary mapping each symbol (non-terminal, terminal, or EPS) to its FIRST set.
    """
    first_sets = initialize_first_sets()
    update_first_sets(first_sets)
    return first_sets


def initialize_first_sets() -> Dict:
    """
    Initializes the FIRST sets for all non-terminals, terminals, and EPS.

    Returns:
        dict: A dictionary with each symbol mapped to its initial FIRST set.
    """
    first_sets = {non_terminal: set() for non_terminal in NON_TERMINALS}
    for terminal in TERMINALS:
        first_sets[terminal] = {terminal}
    first_sets[EPS] = {EPS}
    return first_sets


def update_first_sets(first_sets: Dict) -> None:
    """
    Iteratively updates the FIRST sets for all non-terminals until no changes occur in any set.

    Args:
        first_sets (dict): Dictionary mapping each symbol to its FIRST set. Modified in place.
    """
    changed = True
    while changed:
        changed = False
        for non_terminal, productions in PRODUCTIONS.items():
            previous_size = len(first_sets[non_terminal])
            for production in productions:
                add_production_first_set(non_terminal, production, first_sets)
            if len(first_sets[non_terminal]) > previous_size:
                changed = True


def add_production_first_set(non_terminal, production, first_sets):
    """
    Adds the FIRST set of a production to the FIRST set of a non-terminal.
    Handles the case where the production is EPS or a sequence of symbols.

    Args:
        non_terminal (str): The non-terminal to update.
        production (list): The production (list of symbols) to process.
        first_sets (dict): Dictionary mapping each symbol to its FIRST set. Modified in place.
    """
    if production == [EPS]:
        first_sets[non_terminal].add(EPS)
    else:
        sequence_first = get_first_of_sequence(production, first_sets)
        first_sets[non_terminal] |= sequence_first
