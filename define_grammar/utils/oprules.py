from .types import TypeKind, is_numeric, promote, lub


class OpRule(object):
    def __init__(self, name: str, arity: int, checker, notes=""):
        self.name = name
        self.arity = arity
        self.checker = checker
        self.notes = notes


def check_binary_numeric(args):
    a, b = args
    if not (is_numeric(a) and is_numeric(b)):
        return TypeKind.ERROR
    return promote(a, b)


def check_div_integer(args):
    a, b = args
    return TypeKind.INT if a == TypeKind.INT and b == TypeKind.INT else TypeKind.ERROR


def check_div_real(args):
    a, b = args
    return TypeKind.REAL if (is_numeric(a) and is_numeric(b)) else TypeKind.ERROR


def check_mod(args):
    a, b = args
    return TypeKind.INT if (a == TypeKind.INT and b == TypeKind.INT) else TypeKind.ERROR


def check_pow(args):
    base, exp = args
    if not is_numeric(base):
        return TypeKind.ERROR
    if exp != TypeKind.INT:
        return TypeKind.ERROR
    return TypeKind.REAL if base == TypeKind.REAL else TypeKind.INT


def check_relational(args):
    a, b = args
    return TypeKind.BOOL if (is_numeric(a) and is_numeric(b)) else TypeKind.ERROR


def check_if(args):
    cond, t_then, t_else = args
    if cond != TypeKind.BOOL:
        return TypeKind.ERROR
    return lub(t_then, t_else)


def build_op_rules():
    op_rules = {
        "+": OpRule("+", 2, check_binary_numeric, "Addition with promotion"),
        "-": OpRule("-", 2, check_binary_numeric, "Subtraction with promotion"),
        "*": OpRule("*", 2, check_binary_numeric, "Multiplication with promotion"),
        "|": OpRule("|", 2, check_mod, "Integer Division (INT|INT=INT)"),
        "/": OpRule("/", 2, check_div_real, "Real Division (numeric/numeric=REAL)"),
        "%": OpRule("%", 2, check_mod, "Modulo (INT%INT=INT)"),
        "^": OpRule("^", 2, check_pow, "Exponentiation (Base numeric, Exponent INT)"),
        "IF": OpRule("if", 3, check_if, "If Expression (cond then else IF)"),
    }

    for op in ["<", "<=", ">", ">=", "==", "!="]:
        op_rules[op] = OpRule(
            op, 2, check_relational, "Relational Operator (return BOOL)"
        )

    return op_rules
