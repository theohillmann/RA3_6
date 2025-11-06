from .utils.symbols import SymbolTable
from .utils.oprules import build_op_rules
from .utils.types import TypeKind, promote, lub, is_numeric

EBNF_DOC = """
program        ::= { line } ;
line           ::= expr | stmt ;
expr           ::= atom
                 | "(" expr expr binop ")"
                 | "(" expr expr relop ")"
                 | "(" expr expr expr "IF" ")"
                 | "(" expr expr "WHILE" ")"
                 | "(" int_lit "RES" ")"
                 | "(" expr mem_store ")"
                 | "(" mem_ref ")"
                 ;
stmt           ::= "(" expr expr "WHILE" ")"
                 | "(" expr expr expr "IF" ")"
                 | "(" expr mem_store ")"
                 ;
atom           ::= int_lit | real_lit | mem_ref ;
mem_ref        ::= "MEM" | IDENT_UPPER ;
mem_store      ::= mem_ref ;
binop          ::= "+" | "-" | "*" | "|" | "/" | "%" | "^" ;
relop          ::= ">" | "<" | ">=" | "<=" | "==" | "!=" ;
int_lit        ::= DIGITS ;
real_lit       ::= DIGITS "." DIGITS ;
"""

NOTES = {
    "mem": "Uso de (MEM) exige inicialização prévia; (V MEM) define tipo e marca inicializado.",
    "res": "(N RES) exige N inteiro ≥ 0 e obtém o tipo da linha referida.",
    "controle": "IF e WHILE em RPN; IF tipa por LUB(then, else); WHILE é comando (void).",
}

NOTES = {
    "mem": "(MEM) requires prior initialization; (V MEM) defines type and marks as initialized.",
    "res": "(N RES) requires N to be an integer ≥ 0 and gets the type of the referenced line.",
    "control": "IF and WHILE in RPN; IF types by LUB(then, else); WHILE is a command (void).",
}


def definirGramaticaAtributos():
    """
    Returns a package with:
        - op_rules: dict token -> OpRule
        - relational_ops: set of relational operators
        - ebnf_doc: EBNF as a string
        - notes: documentation notes
        - symbol_table: Symbol Table with global scope
        - TypeKind: enum with types
        - helpers: type utilities
    """
    op_rules = build_op_rules()
    relational_ops = {">", "<", ">=", "<=", "==", "!="}
    symbol_table = SymbolTable()

    return {
        "op_rules": op_rules,
        "relational_ops": relational_ops,
        "ebnf_doc": EBNF_DOC,
        "notes": NOTES,
        "symbol_table": symbol_table,
        "TypeKind": TypeKind,
        "helpers": {"promote": promote, "lub": lub, "is_numeric": is_numeric},
    }
