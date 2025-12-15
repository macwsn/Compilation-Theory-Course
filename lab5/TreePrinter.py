from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    @addToClass(AST.Program)
    def printTree(self, indent=0):
        if self.instructions:
            return self.instructions.printTree(indent)
        return ""

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        result = []
        for instruction in self.instructions:
            result.append(instruction.printTree(indent))
        return "\n".join(result)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        s = "|  " * indent + self.op + "\n"
        s += self.left.printTree(indent + 1) + "\n"
        s += self.right.printTree(indent + 1)
        return s

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        s = "|  " * indent + self.op + "\n"
        s += self.left.printTree(indent + 1) + "\n"
        s += self.right.printTree(indent + 1)
        return s

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        s = "|  " * indent + self.op + "\n"
        s += self.left.printTree(indent + 1) + "\n"
        s += self.right.printTree(indent + 1)
        return s

    @addToClass(AST.If)
    def printTree(self, indent=0):
        s = "|  " * indent + "IF\n"
        s += self.condition.printTree(indent + 1) + "\n"
        s += "|  " * indent + "THEN\n"
        s += self.then_block.printTree(indent + 1)
        if self.else_block:
            s += "\n" + "|  " * indent + "ELSE\n"
            s += self.else_block.printTree(indent + 1)
        return s

    @addToClass(AST.While)
    def printTree(self, indent=0):
        s = "|  " * indent + "WHILE\n"
        s += self.condition.printTree(indent + 1) + "\n"
        s += self.body.printTree(indent + 1)
        return s

    @addToClass(AST.For)
    def printTree(self, indent=0):
        s = "|  " * indent + "FOR\n"
        s += self.var.printTree(indent + 1) + "\n"
        s += self.range.printTree(indent + 1) + "\n"
        s += self.body.printTree(indent + 1)
        return s

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        s = "|  " * indent + "RANGE\n"
        s += self.start.printTree(indent + 1) + "\n"
        s += self.end.printTree(indent + 1)
        return s

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        return "|  " * indent + "BREAK"

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        return "|  " * indent + "CONTINUE"

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        s = "|  " * indent + "RETURN\n"
        s += self.expr.printTree(indent + 1)
        return s

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        s = "|  " * indent + "PRINT\n"
        for i, val in enumerate(self.values):
            s += val.printTree(indent + 1)
            if i < len(self.values) - 1:
                s += "\n"
        return s

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        return "|  " * indent + str(self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        return "|  " * indent + str(self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        return "|  " * indent + '"' + self.value + '"'

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        return "|  " * indent + self.name

    @addToClass(AST.VectorElement)
    def printTree(self, indent=0):
        s = "|  " * indent + "REF\n"
        s += "|  " * (indent + 1) + self.name + "\n"
        s += "|  " * (indent + 1) + str(self.index)
        return s

    @addToClass(AST.MatrixElement)
    def printTree(self, indent=0):
        s = "|  " * indent + "REF\n"
        s += "|  " * (indent + 1) + self.name + "\n"
        s += "|  " * (indent + 1) + str(self.row) + "\n"
        s += "|  " * (indent + 1) + str(self.col)
        return s

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        s = "|  " * indent + "VECTOR\n"
        for i, row in enumerate(self.rows):
            s += row.printTree(indent + 1)
            if i < len(self.rows) - 1:
                s += "\n"
        return s

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        s = "|  " * indent + "VECTOR\n"
        for i, elem in enumerate(self.elements):
            s += elem.printTree(indent + 1)
            if i < len(self.elements) - 1:
                s += "\n"
        return s

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        s = "|  " * indent + self.name + "\n"
        s += "|  " * (indent + 1) + str(self.size)
        return s

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        s = "|  " * indent + "-\n"
        s += self.expr.printTree(indent + 1)
        return s

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        s = "|  " * indent + "TRANSPOSE\n"
        s += self.expr.printTree(indent + 1)
        return s