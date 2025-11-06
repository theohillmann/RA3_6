from typing import List, Dict, Any
import re


EPS = "ε"


class Node:
    def __init__(self, label: str, lexeme: str = None):
        self.label: str = label
        self.lexeme: str = lexeme
        self.children: List["Node"] = []

    def to_dict(self) -> Dict[str, Any]:
        base = {"label": self.label}
        if self.lexeme is not None:
            base["lexeme"] = self.lexeme
        if self.children:
            base["children"] = [c.to_dict() for c in self.children]
        return base


_ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_INT_RE = re.compile(r"^\d+$")
_REAL_RE = re.compile(r"^\d+\.\d+$")

_RESERVED = {
    "int",
    "real",
    "if",
    "while",
    "RES",
    "res",
    "v",
    "+",
    "-",
    "*",
    "/",
    "%",
    "^",
    "|",
    ">",
    "<",
    ">=",
    "<=",
    "==",
    "!=",
    "(",
    ")",
}


def _tokenize_from_str(s: str) -> List[str]:
    return re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|\d+\.\d+|\d+|==|!=|>=|<=|[-+/*%^|><]|\(|\)", s or ""
    )


def split_source_queues_from_line(line: str):
    toks = _tokenize_from_str(line or "")
    ids, ints, reals = [], [], []
    for t in toks:
        if t in ("(", ")") or t in _RESERVED:
            continue
        if _REAL_RE.match(t):
            reals.append(t)
            continue
        if _INT_RE.match(t):
            ints.append(t)
            continue
        if _ID_RE.match(t):
            ids.append(t)
            continue
    return {"ids": ids, "ints": ints, "reals": reals}


def gerarArvore(
    derivacao: List[tuple],
    start_symbol: str,
    source_lines: List[str],  # << agora recebe a LISTA
    expr_index: int,  # << índice da expressão (0-based)
) -> Node:
    """
    Reconstrói a AST a partir da derivação, usando source_lines[expr_index]
    para extrair IDENT/INT_LIT/REAL_LIT na ordem em que aparecem.
    """
    if not derivacao:
        raise ValueError("Derivação vazia.")
    if not isinstance(source_lines, list):
        raise TypeError("source_lines deve ser List[str].")
    if expr_index < 0 or expr_index >= len(source_lines):
        raise IndexError(
            f"expr_index fora do intervalo: {expr_index} (len={len(source_lines)})"
        )

    queues = split_source_queues_from_line(source_lines[expr_index])

    root = Node(start_symbol)
    stack: List[Node] = [root]
    lhs_set = {A for (A, _) in derivacao}

    for lhs, rhs in derivacao:
        if not stack:
            raise ValueError(f"Pilha esgotada antes de expandir {lhs} -> {rhs}")
        current = stack.pop()
        if current.label != lhs:
            raise ValueError(
                f"Inconsistência: topo='{current.label}', produção para='{lhs}'."
            )

        if len(rhs) == 1 and rhs[0] == EPS:
            continue

        children: List[Node] = []
        i = 0
        while i < len(rhs):
            sym = rhs[i]
            if sym == "mem_store":
                name = queues["ids"].pop(0) if queues["ids"] else "__UNKNOWN__"
                store = Node("mem_store")
                store.children.append(Node("IDENT", lexeme=name))
                children.append(store)
                i += 1
                continue

            if sym == "memid":
                name = queues["ids"].pop(0) if queues["ids"] else "__UNKNOWN__"
                child = Node("IDENT", lexeme=name)
            elif sym == "int":
                val = queues["ints"].pop(0) if queues["ints"] else None
                child = Node("INT_LIT", lexeme=val)
            elif sym == "real":
                val = queues["reals"].pop(0) if queues["reals"] else None
                child = Node("REAL_LIT", lexeme=val)
            elif sym == "if":
                child = Node("IF")
            elif sym == "while":
                child = Node("WHILE")
            else:
                child = Node(sym)

            children.append(child)
            i += 1

        current.children.extend(children)
        for ch in reversed(children):
            if ch.label in lhs_set:
                stack.append(ch)

    if any(n.label in lhs_set for n in stack):
        raise ValueError("Sobrou não-terminal para expandir ao final.")
    return root


def print_tree(node: Node, indent: str = "", is_last: bool = True) -> None:
    connector = "└─ " if is_last else "├─ "
    extra = f" [{node.lexeme}]" if getattr(node, "lexeme", None) else ""
    print(indent + connector + node.label + extra)
    new_indent = indent + ("   " if is_last else "│  ")
    for i, child in enumerate(node.children):
        print_tree(child, new_indent, i == len(node.children) - 1)


if __name__ == "__main__":
    derivacao = [
        ("PROGRAM", ["LINES"]),
        ("LINES", ["LINE", "LINES"]),
        ("LINE", ["SEXP"]),
        ("SEXP", ["(", "FORM", ")"]),
        ("FORM", ["STACKTERM", "TAIL1"]),
        # --- cond: ( A B > )
        ("STACKTERM", ["SEXP"]),
        ("SEXP", ["(", "FORM", ")"]),
        ("FORM", ["STACKTERM", "TAIL1"]),
        ("STACKTERM", ["VALUE"]),
        ("VALUE", ["memid"]),  # A
        ("TAIL1", ["STACKTERM", "TAIL2"]),
        ("STACKTERM", ["VALUE"]),
        ("VALUE", ["memid"]),  # B
        ("TAIL2", ["OP"]),
        ("OP", [">"]),
        # --- TAIL1 externo escolhe STACKTERM TAIL2 (há then/else)
        ("TAIL1", ["STACKTERM", "TAIL2"]),
        # --- then: ( ( A B + ) v R )
        ("STACKTERM", ["SEXP"]),
        ("SEXP", ["(", "FORM", ")"]),
        ("FORM", ["STACKTERM", "TAIL1"]),
        ("STACKTERM", ["SEXP"]),
        ("SEXP", ["(", "FORM", ")"]),
        ("FORM", ["STACKTERM", "TAIL1"]),
        ("STACKTERM", ["VALUE"]),
        ("VALUE", ["memid"]),  # A
        ("TAIL1", ["STACKTERM", "TAIL2"]),
        ("STACKTERM", ["VALUE"]),
        ("VALUE", ["memid"]),  # B
        ("TAIL2", ["OP"]),
        ("OP", ["+"]),
        ("TAIL1", ["v", "memid"]),  # v R
        # --- TAIL2 externo escolhe STACKTERM if  (else + 'if')
        ("TAIL2", ["STACKTERM", "if"]),
        # --- else: ( 0 v R )
        ("STACKTERM", ["SEXP"]),
        ("SEXP", ["(", "FORM", ")"]),
        ("FORM", ["STACKTERM", "TAIL1"]),
        ("STACKTERM", ["VALUE"]),
        ("VALUE", ["int"]),  # 0
        ("TAIL1", ["v", "memid"]),  # v R
        # --- fim das linhas
        ("LINES", ["ε"]),
    ]
    tree = gerarArvore(derivacao, start_symbol="PROGRAM")
    # print(tree)
    print_tree(tree)
