from typing import Dict, List, Optional
from .types import TypeKind


class Symbol:
    def __init__(self, name: str, symbol_type: TypeKind, initialized: bool, scope: int):
        self.name = name
        self.type = symbol_type
        self.initialized = initialized
        self.scope = scope


class SymbolTable:

    def __init__(self):
        self.scope = [dict()]

    def push_scope(self):
        self.scope.append({})

    def pop_scope(self):
        if len(self.scope) > 1:
            self.scope.pop()

    def add(self, name: str, symbol_type: TypeKind, initialized: bool) -> Symbol:
        current = len(self.scope) - 1
        symbol = Symbol(name, symbol_type, initialized, current)
        self.scope[current][name] = symbol
        return symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scope):
            if name in scope:
                return scope[name]
        return None

    def set_initialized(self, name: str):
        symbol = self.lookup(name)
        if symbol:
            symbol.initialized = True

    def mark_initialized(
        self, name: str, symbol_type: Optional[TypeKind] = None
    ) -> Symbol:
        symbol = self.lookup(name)
        if symbol is None:
            if symbol_type is None:
                from .types import TypeKind

                symbol_type = TypeKind.ERROR
            symbol = self.add(name, symbol_type, True)
        else:
            if symbol_type is not None:
                symbol.type = symbol_type
            symbol.initialized = True
        return symbol

    def is_initialized(self, name: str) -> bool:
        symbol = self.lookup(name)
        return bool(symbol and symbol.initialized)
