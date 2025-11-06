from typing import List
from syntactic_analyzer.build_grammar.constants import END

VALID_SINGLE_TOKENS = {
    "(",
    ")",
    "res",
    "v",
    "if",
    "while",
    "+",
    "-",
    "*",
    "|",
    "/",
    "%",
    "^",
    ">",
    "<",
    ">=",
    "<=",
    "==",
    "!=",
}


def lerTokens(input_file: str) -> List[List[str]]:
    """
    Reads a file with ONE EXPRESSION PER LINE and returns
    a list of normalized token vectors (each ends with '$').
    """
    tokenized_lines: List[List[str]] = []
    with open(input_file, "r", encoding="utf-8") as file:
        for line_number, current_line in enumerate(file, start=1):
            current_line = current_line.strip()
            if not current_line:
                continue
            try:
                tokenized_lines.append(_normalize_line_to_tokens(current_line))
            except ValueError as error:
                raise ValueError(f"[line {line_number}] {error}")
    return tokenized_lines


def _normalize_line_to_tokens(input_line: str) -> List[str]:
    line_parts = [part for part in input_line.strip().split() if part]
    if not line_parts:
        return [END]
    tokens = [_normalize_lexeme_to_token(part) for part in line_parts]
    tokens = _mark_mem_store(tokens)
    tokens.append(END)
    return tokens


def _normalize_lexeme_to_token(lexeme: str) -> str:
    """
    Converts a raw lexeme to the grammar terminal (without regex):
      - numbers → "int"/"real"
      - keywords (case-insensitive) → "res" | "v" | "if" | "while"
      - parentheses/operators (incl. relational) → as they are (if valid)
      - identifiers → "memid"
    """
    cleaned_lexeme = lexeme.strip()
    if not cleaned_lexeme:
        raise ValueError("empty lexeme")

    keyword = cleaned_lexeme.lower()
    if keyword in {"res", "v", "if", "while"}:
        return keyword

    if cleaned_lexeme in VALID_SINGLE_TOKENS:
        return cleaned_lexeme

    if _is_integer_lexeme(cleaned_lexeme):
        return "int"
    if _is_real_number_lexeme(cleaned_lexeme):
        return "real"

    if _is_memory_identifier_lexeme(cleaned_lexeme):
        return "memid"

    raise ValueError(f"Invalid/unsupported lexeme: '{lexeme}'")


def _is_sign(character: str) -> bool:
    return character in "+-"


def _is_integer_lexeme(text: str) -> bool:
    if not text:
        return False
    start_index = 1 if _is_sign(text[0]) and len(text) > 1 else 0
    if start_index == len(text):
        return False
    return all(char.isdigit() for char in text[start_index:])


def _is_real_number_lexeme(text: str) -> bool:
    if not text:
        return False
    start_index = 1 if _is_sign(text[0]) and len(text) > 1 else 0
    number_part = text[start_index:]
    if number_part.count(".") != 1:
        return False
    integer_part, decimal_part = number_part.split(".", 1)
    if not integer_part or not decimal_part:
        return False
    return integer_part.isdigit() and decimal_part.isdigit()


def _is_memory_identifier_lexeme(text: str) -> bool:
    if not text or not text[0].isalpha():
        return False
    for character in text[1:]:
        if not (character.isalnum() or character == "_"):
            return False
    return True


def _mark_mem_store(tokens: list[str]) -> list[str]:
    """
    Marca '( STACKTERM memid )' como '( STACKTERM mem_store )'
    inclusive quando STACKTERM é uma SEXP aninhada.
    Regra:
      - dentro de cada SEXP, primeiro processa recursivamente o conteúdo,
      - depois, se o conteúdo finaliza com 'memid' e o prefixo é exatamente 1 STACKTERM,
        substitui por 'mem_store'.
    """
    out = []
    i = 0
    n = len(tokens)

    def is_stackterm_prefix(seq: list[str]) -> bool:
        # 1) Simples: int | real | memid
        if len(seq) == 1 and seq[0] in ("int", "real", "memid"):
            return True
        # 2) Única SEXP: começa com '(' e fecha exatamente no fim
        if seq and seq[0] == "(":
            depth = 0
            for k, t in enumerate(seq):
                if t == "(":
                    depth += 1
                elif t == ")":
                    depth -= 1
                    if depth == 0 and k != len(seq) - 1:
                        return False  # fechou antes do fim → tem mais de um item
            return depth == 0
        return False

    while i < n:
        t = tokens[i]
        if t != "(":
            out.append(t)
            i += 1
            continue

        # Copia '(' e captura conteúdo até ')'
        out.append("(")
        i += 1
        depth = 1
        inner = []
        j = i
        while j < n and depth > 0:
            tj = tokens[j]
            if tj == "(":
                depth += 1
            elif tj == ")":
                depth -= 1
                if depth == 0:
                    break
            if depth > 0:
                inner.append(tj)
            j += 1

        # 🔁 processa recursivamente o conteúdo antes de decidir
        inner = _mark_mem_store(inner)

        # Se inner termina com memid e o prefixo é UM STACKTERM → é store
        if inner and inner[-1] == "memid" and is_stackterm_prefix(inner[:-1]):
            out.extend(inner[:-1])
            out.append("mem_store")
        else:
            out.extend(inner)

        out.append(")")
        i = j + 1

    return out


if __name__ == "__main__":
    input_file_path = "/Users/theocoelho/Documents/academico/faculdade/10 periodo/compiladores/RA2_6/tokens/test1.txt"
    print(lerTokens(input_file_path))
