#!/usr/bin/python

class Symbol:
    pass

class VariableSymbol(Symbol):
    def __init__(self, name, type, shape=None):
        self.name = name
        self.type = type  # 'int', 'float', 'vector', 'matrix', 'string'
        self.shape = shape  # None for scalars, (n,) for vectors, (m,n) for matrices

class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}
    
    def put(self, name, symbol):
        self.symbols[name] = symbol
    
    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.get(name)
        return None
    
    def getParentScope(self):
        return self.parent
    
    def pushScope(self, name):
        return SymbolTable(self, name)
    
    def popScope(self):
        return self.parent