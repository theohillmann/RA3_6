import json
from define_grammar.utils.types import TypeKind


def gerar_arvore_atribuida(anotacoes, symbol_table):
    """
    Build the attributed syntax tree structure.

    Args:
        anotacoes: List of line annotations with tokens and types
        symbol_table: Symbol table with final variable states

    Returns:
        Dictionary containing attributed tree with lines and symbols
    """
    lines = build_annotated_lines(anotacoes)
    symbols = extract_symbol_table(symbol_table)

    return {
        "lines": lines,
        "symbols": symbols,
    }


def salvar_arquivos_saida(arvore_atribuida, prefixo="saida"):
    """
    Save attributed tree to JSON file.

    Args:
        arvore_atribuida: Attributed tree dictionary
        prefixo: File prefix for output (default: "saida")
    """
    json_path = f"{prefixo}_arvore_atribuida.json"

    save_json_file(arvore_atribuida, json_path)

    print(f"Árvore atribuída salva em: {json_path}")


# ============================================================================
# Line Processing
# ============================================================================


def build_annotated_lines(annotations):
    """
    Build list of annotated lines from semantic analysis.

    Args:
        annotations: List of annotation dictionaries

    Returns:
        List of line dictionaries with context, tokens, and types
    """
    lines = []

    for info in annotations:
        line_no = info.get("line")
        context = info.get("context")
        tokens = info.get("tokens", [])
        line_type = info.get("type")

        type_string = convert_type_to_string(line_type)
        formatted_tokens = format_tokens(tokens)

        lines.append(
            {
                "line": line_no,
                "context": context,
                "postfix": formatted_tokens,
                "type": type_string,
            }
        )

    return lines


def convert_type_to_string(type_value):
    """
    Convert TypeKind enum to string representation.

    Args:
        type_value: TypeKind enum or other value

    Returns:
        String representation of the type
    """
    if isinstance(type_value, TypeKind):
        return type_value.value
    return str(type_value)


def format_tokens(tokens):
    """
    Format token list into JSON-friendly structure.

    Args:
        tokens: List of token tuples

    Returns:
        List of token dictionaries
    """
    formatted = []

    for token in tokens:
        # Handle non-tuple tokens
        if not isinstance(token, (list, tuple)):
            formatted.append({"kind": str(token)})
            continue

        # Handle single-element tuples
        if len(token) == 1:
            formatted.append({"kind": token[0]})

        # Handle two-element tuples (kind, value)
        elif len(token) == 2:
            formatted.append({"kind": token[0], "value": token[1]})

        # Fallback for unusual token structures
        else:
            formatted.append({"raw": list(token)})

    return formatted


# ============================================================================
# Symbol Table Extraction
# ============================================================================


def extract_symbol_table(symbol_table):
    """
    Extract symbol table state into dictionary format.

    Args:
        symbol_table: Symbol table object with scope information

    Returns:
        Dictionary mapping variable names to their properties
    """
    symbols = {}

    for scope_dict in symbol_table.scope:
        for name, symbol in scope_dict.items():
            symbols[name] = {
                "type": symbol.type.value,
                "initialized": bool(symbol.initialized),
                "scope": symbol.scope,
            }

    return symbols


# ============================================================================
# File I/O
# ============================================================================


def save_json_file(data, filepath):
    """
    Save data to JSON file with UTF-8 encoding.

    Args:
        data: Data structure to serialize
        filepath: Output file path
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
