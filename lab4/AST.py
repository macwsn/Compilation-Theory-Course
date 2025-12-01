class Node:
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self):
        self.instructions = []
    
    def add(self, instruction):
        self.instructions.append(instruction)

# (+, -, , /, .+, .-, ., ./) 
class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

# (<, >, <=, >=, ==, !=)
class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

#  (=, +=, -=, *=, /=)
class Assignment(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class If(Node):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class For(Node):
    def __init__(self, var, range_expr, body):
        self.var = var
        self.range = range_expr
        self.body = body


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Break(Node):
    pass


class Continue(Node):
    pass


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Print(Node):
    def __init__(self, values):
        self.values = values


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class VectorElement(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index


class MatrixElement(Node):
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col


class Matrix(Node):
    def __init__(self, rows):
        self.rows = rows


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class MatrixFunction(Node):
    def __init__(self, name, size):
        self.name = name
        self.size = size


class UnaryMinus(Node):
    def __init__(self, expr):
        self.expr = expr


class Transposition(Node):
    def __init__(self, expr):
        self.expr = expr