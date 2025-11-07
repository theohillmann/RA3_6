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


def salvar_arquivos_saida(arvore_atribuida, prefixo="saida", erros=None):
    """
    Save attributed tree to JSON file and generate Markdown reports.

    Args:
        arvore_atribuida: Attributed tree dictionary
        prefixo: File prefix for output (default: "saida")
        erros: List of semantic errors (optional)
    """
    json_path = f"{prefixo}_arvore_atribuida.json"
    tipos_path = f"{prefixo}_relatorio_tipos.md"
    erros_path = f"{prefixo}_relatorio_erros.md"

    # Save JSON file
    save_json_file(arvore_atribuida, json_path)
    print(f"✅ Árvore atribuída salva em: {json_path}")

    # Generate and save tipos report
    gerar_relatorio_tipos(arvore_atribuida, tipos_path)
    print(f"✅ Relatório de tipos salvo em: {tipos_path}")

    # Generate and save erros report
    if erros:
        gerar_relatorio_erros(erros, arvore_atribuida, erros_path)
        print(f"✅ Relatório de erros salvo em: {erros_path}")


# ============================================================================
# Markdown Report Generation
# ============================================================================


def gerar_relatorio_tipos(arvore_atribuida, filepath):
    """
    Generate a Markdown report with type inference table.

    Args:
        arvore_atribuida: Attributed tree dictionary
        filepath: Output file path for the report
    """
    lines = arvore_atribuida.get("lines", [])
    symbols = arvore_atribuida.get("symbols", {})

    # Build Markdown content
    md_lines = [
        "# Relatório de Tipos Inferidos\n",
        f"**Total de linhas analisadas:** {len(lines)}\n",
        f"**Data de geração:** {get_current_timestamp()}\n",
        "\n---\n",
        "\n## Tabela de Tipos por Linha\n",
        "\n| Linha | Contexto | Tipo Inferido | Notação Posfixa |",
        "|-------|----------|---------------|-----------------|",
    ]

    for line_info in lines:
        line_no = line_info.get("line", "?")
        context = line_info.get("context", "")
        tipo = line_info.get("type", "unknown")
        postfix = line_info.get("postfix", [])

        # Format postfix notation
        postfix_str = format_postfix_for_display(postfix)

        # Add type emoji
        tipo_display = format_type_with_emoji(tipo)

        # Escape pipes in context
        context_escaped = context.replace("|", "\\|")

        md_lines.append(
            f"| {line_no} | `{context_escaped}` | {tipo_display} | {postfix_str} |"
        )

    # Add symbol table section
    if symbols:
        md_lines.extend(
            [
                "\n\n---\n",
                "\n## Tabela de Símbolos\n",
                "\n| Nome | Tipo | Inicializada | Escopo |",
                "|------|------|--------------|--------|",
            ]
        )

        for name, props in sorted(symbols.items()):
            tipo = props.get("type", "unknown")
            init = "✅ Sim" if props.get("initialized") else "❌ Não"
            scope = props.get("scope", 0)

            md_lines.append(f"| `{name}` | `{tipo}` | {init} | {scope} |")

    # Add statistics section
    md_lines.extend(["\n\n---\n", "\n## Estatísticas\n"])

    # Count types
    type_counts = {}
    for line_info in lines:
        tipo = line_info.get("type", "unknown")
        type_counts[tipo] = type_counts.get(tipo, 0) + 1

    md_lines.append("\n### Distribuição de Tipos\n")
    for tipo, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        percentage = (count / len(lines) * 100) if lines else 0
        tipo_display = format_type_with_emoji(tipo)
        md_lines.append(f"- {tipo_display}: {count} ({percentage:.1f}%)")

    # Success rate
    success_count = sum(
        1 for line in lines if line.get("type") not in ["error", "unknown"]
    )
    success_rate = (success_count / len(lines) * 100) if lines else 0
    md_lines.append(f"\n### Taxa de Sucesso\n")
    md_lines.append(f"**{success_rate:.1f}%** das linhas foram tipadas com sucesso.\n")

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))


def gerar_relatorio_erros(erros, arvore_atribuida, filepath):
    """
    Generate a Markdown report with semantic errors.

    Args:
        erros: List of error messages
        arvore_atribuida: Attributed tree dictionary
        filepath: Output file path for the report
    """
    lines = arvore_atribuida.get("lines", [])

    # Build Markdown content
    md_lines = [
        "# Relatório de Erros Semânticos\n",
        f"**Total de erros encontrados:** {len(erros)}\n",
        f"**Data de geração:** {get_current_timestamp()}\n",
        "\n---\n",
    ]

    if not erros:
        md_lines.append("\n## ✅ Nenhum Erro Encontrado!\n")
        md_lines.append(
            "\nTodas as linhas foram analisadas com sucesso e não apresentaram erros semânticos.\n"
        )
    else:
        md_lines.append("\n## ❌ Erros Detectados\n")

        # Group errors by line
        errors_by_line = {}
        for error_msg in erros:
            line_no = extract_line_number(error_msg)
            if line_no not in errors_by_line:
                errors_by_line[line_no] = []
            errors_by_line[line_no].append(error_msg)

        # Display errors by line
        for line_no in sorted(errors_by_line.keys()):
            line_errors = errors_by_line[line_no]
            line_info = next((l for l in lines if l.get("line") == line_no), None)

            md_lines.append(f"\n### Linha {line_no}\n")

            if line_info:
                context = line_info.get("context", "")
                tipo = line_info.get("type", "unknown")
                md_lines.append(f"**Contexto:** `{context}`\n")
                md_lines.append(f"**Tipo Inferido:** `{tipo}`\n")

            md_lines.append("\n**Erros:**\n")
            for i, error_msg in enumerate(line_errors, 1):
                # Extract just the error message (remove line number prefix)
                clean_msg = extract_error_message(error_msg)
                md_lines.append(f"{i}. {clean_msg}")

        # Add summary section
        md_lines.extend(["\n\n---\n", "\n## Resumo de Erros\n"])

        # Categorize errors
        error_categories = categorize_errors(erros)

        md_lines.append("\n### Erros por Categoria\n")
        for category, count in sorted(error_categories.items(), key=lambda x: -x[1]):
            md_lines.append(f"- **{category}**: {count}")

        # Lines with errors
        lines_with_errors = len(errors_by_line)
        total_lines = len(lines)
        error_rate = (lines_with_errors / total_lines * 100) if total_lines else 0

        md_lines.append(f"\n### Estatísticas\n")
        md_lines.append(f"- **Linhas com erro:** {lines_with_errors}/{total_lines}")
        md_lines.append(f"- **Taxa de erro:** {error_rate:.1f}%")

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))


# ============================================================================
# Helper Functions for Reports
# ============================================================================


def format_type_with_emoji(tipo):
    """Add emoji to type for better visualization."""
    emoji_map = {
        "int": "🔢",
        "real": "🔢",
        "bool": "✅",
        "void": "⚪",
        "error": "❌",
        "unknown": "❓",
    }
    emoji = emoji_map.get(tipo, "")
    return f"{emoji} `{tipo}`"


def format_postfix_for_display(postfix):
    """Format postfix notation for table display."""
    if not postfix:
        return "—"

    tokens = []
    for token in postfix:
        if isinstance(token, dict):
            kind = token.get("kind", "?")
            value = token.get("value")
            if value is not None:
                tokens.append(f"{kind}({value})")
            else:
                tokens.append(kind)
        else:
            tokens.append(str(token))

    result = " ".join(tokens)
    # Truncate if too long
    if len(result) > 50:
        result = result[:47] + "..."
    return f"`{result}`"


def extract_line_number(error_msg):
    """Extract line number from error message."""
    import re

    match = re.search(r"Linha (\d+)", error_msg)
    if match:
        return int(match.group(1))
    return 0


def extract_error_message(error_msg):
    """Extract clean error message without line number prefix."""
    parts = error_msg.split(":", 1)
    if len(parts) > 1:
        msg = parts[1].strip()
        # Remove context if present
        if "\nContexto:" in msg:
            msg = msg.split("\nContexto:")[0].strip()
        return msg
    return error_msg


def categorize_errors(erros):
    """Categorize errors by type."""
    categories = {
        "Tipos Incompatíveis": 0,
        "Variável Não Declarada": 0,
        "Variável Não Inicializada": 0,
        "Operador Não Suportado": 0,
        "Aridade Incorreta": 0,
        "RES Inválido": 0,
        "Expressão Malformada": 0,
        "Outros": 0,
    }

    for error_msg in erros:
        msg_lower = error_msg.lower()

        if "invalid types" in msg_lower or "tipos" in msg_lower:
            categories["Tipos Incompatíveis"] += 1
        elif "not declared" in msg_lower or "não declarada" in msg_lower:
            categories["Variável Não Declarada"] += 1
        elif "before initialization" in msg_lower or "não inicializada" in msg_lower:
            categories["Variável Não Inicializada"] += 1
        elif "not supported" in msg_lower or "não suportado" in msg_lower:
            categories["Operador Não Suportado"] += 1
        elif "arity" in msg_lower or "aridade" in msg_lower:
            categories["Aridade Incorreta"] += 1
        elif "res" in msg_lower:
            categories["RES Inválido"] += 1
        elif "malformed" in msg_lower or "malformada" in msg_lower:
            categories["Expressão Malformada"] += 1
        else:
            categories["Outros"] += 1

    # Remove categories with zero count
    return {k: v for k, v in categories.items() if v > 0}


def get_current_timestamp():
    """Get current timestamp in readable format."""
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
