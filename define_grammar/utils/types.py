from enum import Enum


class TypeKind(Enum):
    INT = "int"
    REAL = "real"
    BOOL = "bool"
    VOID = "void"
    ERROR = "error"

NUMERIC = {TypeKind.INT, TypeKind.REAL}

def is_numeric(type_kind: TypeKind) -> bool:
    return type_kind in NUMERIC

def promote(type1: TypeKind, type2: TypeKind) -> TypeKind:
    """Promote int * real -> real, else keep the same type."""
    if TypeKind.ERROR in [type1, type2]:
        return TypeKind.ERROR
    if type1 == TypeKind.REAL or type2 == TypeKind.REAL:
        return TypeKind.REAL
    return TypeKind.INT

def lub(type1: TypeKind, type2: TypeKind) -> TypeKind:
    """
    Compute the least upper bound of two types.
    
    - int and int -> int
    - real and real -> real
    - int and real -> real
    - any other combination -> error
    """
    if type1 == type2:
        return type1

    if {type1, type2} == {TypeKind.INT, TypeKind.REAL}:
        return TypeKind.REAL
    return TypeKind.ERROR