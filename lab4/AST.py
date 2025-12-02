class Node:
    def __init__(self):
        self.lineno = 0
    
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, instructions):
        super().__init__()
        self.instructions = instructions


class Instructions(Node):
    def __init__(self):
        super().__init__()
        self.instructions = []
    
    def add(self, instruction):
        self.instructions.append(instruction)

# (+, -, , /, .+, .-, ., ./) 
class BinExpr(Node):
    def __init__(self, op, left, right, lineno=0):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

# (<, >, <=, >=, ==, !=)
class RelExpr(Node):
    def __init__(self, op, left, right, lineno=0):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

#  (=, +=, -=, *=, /=)
class Assignment(Node):
    def __init__(self, op, left, right, lineno=0):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class If(Node):
    def __init__(self, condition, then_block, else_block=None, lineno=0):
        super().__init__()
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
        self.lineno = lineno


class While(Node):
    def __init__(self, condition, body, lineno=0):
        super().__init__()
        self.condition = condition
        self.body = body
        self.lineno = lineno


class For(Node):
    def __init__(self, var, range_expr, body, lineno=0):
        super().__init__()
        self.var = var
        self.range = range_expr
        self.body = body
        self.lineno = lineno


class Range(Node):
    def __init__(self, start, end, lineno=0):
        super().__init__()
        self.start = start
        self.end = end
        self.lineno = lineno


class Break(Node):
    def __init__(self, lineno=0):
        super().__init__()
        self.lineno = lineno


class Continue(Node):
    def __init__(self, lineno=0):
        super().__init__()
        self.lineno = lineno


class Return(Node):
    def __init__(self, expr, lineno=0):
        super().__init__()
        self.expr = expr
        self.lineno = lineno


class Print(Node):
    def __init__(self, values, lineno=0):
        super().__init__()
        self.values = values
        self.lineno = lineno


class IntNum(Node):
    def __init__(self, value, lineno=0):
        super().__init__()
        self.value = value
        self.lineno = lineno


class FloatNum(Node):
    def __init__(self, value, lineno=0):
        super().__init__()
        self.value = value
        self.lineno = lineno


class String(Node):
    def __init__(self, value, lineno=0):
        super().__init__()
        self.value = value
        self.lineno = lineno


class Variable(Node):
    def __init__(self, name, lineno=0):
        super().__init__()
        self.name = name
        self.lineno = lineno


class VectorElement(Node):
    def __init__(self, name, index, lineno=0):
        super().__init__()
        self.name = name
        self.index = index
        self.lineno = lineno


class MatrixElement(Node):
    def __init__(self, name, row, col, lineno=0):
        super().__init__()
        self.name = name
        self.row = row
        self.col = col
        self.lineno = lineno


class Matrix(Node):
    def __init__(self, rows, lineno=0):
        super().__init__()
        self.rows = rows
        self.lineno = lineno


class Vector(Node):
    def __init__(self, elements, lineno=0):
        super().__init__()
        self.elements = elements
        self.lineno = lineno


class MatrixFunction(Node):
    def __init__(self, name, size, lineno=0):
        super().__init__()
        self.name = name
        self.size = size
        self.lineno = lineno


class UnaryMinus(Node):
    def __init__(self, expr, lineno=0):
        super().__init__()
        self.expr = expr
        self.lineno = lineno


class Transposition(Node):
    def __init__(self, expr, lineno=0):
        super().__init__()
        self.expr = expr
        self.lineno = lineno