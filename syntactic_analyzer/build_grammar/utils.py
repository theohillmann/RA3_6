from .constants import EPS
from typing import List, Dict, Set


def get_first_of_sequence(sequence: List, first_sets: Dict) -> Set:
    """
    Computes the FIRST set for a sequence of symbols.

    Args:
        sequence (list): The sequence of symbols to process.
        first_sets (dict): Dictionary mapping each symbol to its FIRST set.

    Returns:
        set: A set containing the FIRST symbols of the sequence.
    """
    if not sequence:
        return {EPS}
    result = set()
    for i, symbol in enumerate(sequence):
        result |= first_sets[symbol] - {EPS}
        if EPS not in first_sets[symbol]:
            break
        if i == len(sequence) - 1:
            result.add(EPS)
    return result
