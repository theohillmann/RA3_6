_REL_OPS = {">", "<", ">=", "<=", "==", "!="}
_ARITH_OPS = {"+", "-", "*", "|", "/", "%", "^"}


def extract_rpn_from_ast(arvoreSintatica):
    """
    Convert PROGRAM AST(s) into a list of line dictionaries with RPN tokens.

    Args:
        arvoreSintatica: Single PROGRAM dict or list of PROGRAM dicts

    Returns:
        List of dictionaries with 'line', 'context', and 'tokens' keys
        Example: [{"line": 1, "context": "( int int + )", "tokens": [('INT',10), ('INT',8), ('OP','+')]}]
    """
    programs = (
        arvoreSintatica if isinstance(arvoreSintatica, list) else [arvoreSintatica]
    )
    out_all = []
    line_no = 1

    for prog in programs:
        if not prog or _label(prog) != "PROGRAM":
            continue

        for line_node in _collect_lines(prog):
            sexp = _sexp_of_line(line_node)
            tokens = []
            if sexp:
                _emit_from_SEXP(sexp, tokens)

            context = _build_context_string(tokens)
            out_all.append({"line": line_no, "context": context, "tokens": tokens})
            line_no += 1

    return out_all


# ============================================================================
# AST Navigation Helpers
# ============================================================================


def _label(node):
    """Get the label of an AST node."""
    return node.get("label", "")


def _children(node):
    """Get the children list of an AST node."""
    return node.get("children", []) or []


def _find_child(node, wanted):
    """
    Find first immediate child with the given label.

    Args:
        node: Parent AST node
        wanted: Label to search for

    Returns:
        Child node or empty dict if not found
    """
    for child in _children(node):
        if _label(child) == wanted:
            return child
    return {}


def _find_children(node, wanted):
    """
    Find all immediate children with the given label.

    Args:
        node: Parent AST node
        wanted: Label to search for

    Returns:
        List of matching child nodes
    """
    return [child for child in _children(node) if _label(child) == wanted]


def _collect_lines(program_node):
    """
    Collect all LINE nodes from a PROGRAM tree.

    Args:
        program_node: Root PROGRAM node

    Returns:
        List of LINE nodes
    """
    result = []

    def dfs_lines(node):
        if not node:
            return
        if _label(node) == "LINE":
            result.append(node)
            return
        for child in _children(node):
            dfs_lines(child)

    dfs_lines(program_node)
    return result


def _sexp_of_line(line_node):
    """
    Extract SEXP node from LINE node.

    Args:
        line_node: LINE AST node

    Returns:
        SEXP node or empty dict
    """
    return _find_child(line_node, "SEXP")


# ============================================================================
# Token Extraction
# ============================================================================


def _value_token(value_node):
    """
    Extract token from VALUE node.

    VALUE can be:
    - INT_LIT -> ('INT', int_value)
    - REAL_LIT -> ('REAL', float_value)
    - IDENT -> ('REF', variable_name) - memory reference

    Args:
        value_node: VALUE AST node

    Returns:
        Token tuple (type, value)
    """
    kids = _children(value_node)
    if not kids:
        return ("ERROR", None)

    kid = kids[0]
    lab = _label(kid)

    if lab == "INT_LIT":
        return ("INT", int(kid.get("lexeme", "0")))

    if lab == "REAL_LIT":
        return ("REAL", float(kid.get("lexeme", "0")))

    if lab == "IDENT":
        return ("REF", str(kid.get("lexeme", "")))

    return ("ERROR", None)


def _emit_from_STACKTERM(st_node, out):
    """
    Emit tokens from STACKTERM node: VALUE | SEXP.

    Args:
        st_node: STACKTERM AST node
        out: List to append tokens to
    """
    kids = _children(st_node)
    if not kids:
        return

    kid = kids[0]
    lab = _label(kid)

    if lab == "VALUE":
        out.append(_value_token(kid))
    elif lab == "SEXP":
        _emit_from_SEXP(kid, out)


def _emit_from_TAIL2(tail2_node, out):
    """
    Emit tokens from TAIL2 node.

    TAIL2 can be:
    - OP (binary operator with symbol as single child)
    - WHILE
    - STACKTERM + IF (IF with else branch)

    Args:
        tail2_node: TAIL2 AST node
        out: List to append tokens to
    """
    # Handle IF with else branch (STACKTERM for else)
    st_terms = _find_children(tail2_node, "STACKTERM")
    for st in st_terms:
        _emit_from_STACKTERM(st, out)

    # Check for operator
    op_node = _find_child(tail2_node, "OP")
    if op_node:
        op_kids = _children(op_node)
        if op_kids:
            sym = _label(op_kids[0])
            if sym in _REL_OPS or sym in _ARITH_OPS:
                out.append(("OP", sym))
            else:
                out.append(("ERROR", None))
        return

    # Check for WHILE
    if _find_child(tail2_node, "WHILE"):
        out.append(("WHILE",))
        return

    # Check for IF
    if _find_child(tail2_node, "IF"):
        out.append(("IF",))
        return


def _emit_from_TAIL1(tail1_node, out):
    """
    Emit tokens from TAIL1 node.

    TAIL1 can be:
    - mem_store IDENT -> ('STORE', 'IDENT')
    - STACKTERM + TAIL2 -> second operand + operator/control flow

    Args:
        tail1_node: TAIL1 AST node
        out: List to append tokens to
    """
    # Check for assignment (mem_store)
    ms = _find_child(tail1_node, "mem_store")
    if ms:
        ident = _find_child(ms, "IDENT")
        name = str(ident.get("lexeme", "")) if ident else ""
        out.append(("STORE", name))
        return

    # Check for binary operation or control flow
    st = _find_child(tail1_node, "STACKTERM")
    if st:
        _emit_from_STACKTERM(st, out)
        t2 = _find_child(tail1_node, "TAIL2")
        if t2:
            _emit_from_TAIL2(t2, out)


def _emit_from_FORM(form_node, out):
    """
    Emit tokens from FORM node: STACKTERM [TAIL1].

    Args:
        form_node: FORM AST node
        out: List to append tokens to
    """
    # Emit first operand
    st = _find_child(form_node, "STACKTERM")
    if st:
        _emit_from_STACKTERM(st, out)

    # Emit continuation (operator, assignment, control flow)
    t1 = _find_child(form_node, "TAIL1")
    if t1:
        _emit_from_TAIL1(t1, out)


def _emit_from_SEXP(sexp_node, out):
    """
    Emit tokens from SEXP node: "(" FORM ")".

    Args:
        sexp_node: SEXP AST node
        out: List to append tokens to
    """
    form = _find_child(sexp_node, "FORM")
    if form:
        _emit_from_FORM(form, out)


# ============================================================================
# Context String Generation
# ============================================================================


def _build_context_string(tokens):
    """
    Build a human-readable context string from tokens.

    Args:
        tokens: List of token tuples

    Returns:
        Context string like "( int int + )"
    """
    ctx_parts = []

    for token in tokens:
        token_type = token[0]

        if token_type == "INT":
            ctx_parts.append("int")
        elif token_type == "REAL":
            ctx_parts.append("real")
        elif token_type == "REF":
            ctx_parts.append("memid")
        elif token_type == "STORE":
            ctx_parts.append("mem_store")
        elif token_type == "OP":
            ctx_parts.append(str(token[1]))
        elif token_type == "WHILE":
            ctx_parts.append("while")
        elif token_type == "IF":
            ctx_parts.append("if")
        else:
            ctx_parts.append(token_type.lower())

    return "( " + " ".join(ctx_parts) + " )"
