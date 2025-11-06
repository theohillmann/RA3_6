EPS = "ε"
END = "$"

START_SYMBOL = "PROGRAM"

TERMINALS = {
    "(",
    ")",
    "int",
    "real",
    "memid",
    "mem_store",
    "res",
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
    END,
}

NON_TERMINALS = {
    "PROGRAM",
    "LINES",
    "LINE",
    "SEXP",
    "FORM",
    "TAIL1",
    "TAIL2",
    "STACKTERM",
    "VALUE",
    "OP",
}

PRODUCTIONS = {
    "PROGRAM": [["LINES"]],
    "LINES": [["LINE", "LINES"], [EPS]],
    "LINE": [["SEXP"]],
    "SEXP": [["(", "FORM", ")"]],
    "FORM": [["STACKTERM", "TAIL1"]],
    "TAIL1": [["STACKTERM", "TAIL2"], ["res"], ["mem_store"], ["ε"]],
    "TAIL2": [["OP"], ["STACKTERM", "if"], ["while"]],
    "STACKTERM": [["VALUE"], ["SEXP"]],
    "VALUE": [["int"], ["real"], ["memid"]],
    "OP": [
        ["+"],
        ["-"],
        ["*"],
        ["|"],
        ["/"],
        ["%"],
        ["^"],
        [">"],
        ["<"],
        [">="],
        ["<="],
        ["=="],
        ["!="],
    ],
}
