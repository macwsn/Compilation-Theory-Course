import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator
import numpy as np

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack(Memory("global"))
    
    @on('node')
    def visit(self, node):
        pass
    
    @when(AST.Program)
    def visit(self, node):
        return node.instructions.accept(self)
    
    @when(AST.Instructions)
    def visit(self, node):
        result = None
        for instruction in node.instructions:
            result = instruction.accept(self)
        return result
    
    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '.+': np.add,
            '.-': np.subtract,
            '.*': np.multiply,
            './': np.divide,
        }
        
        if node.op in ops:
            return ops[node.op](left, right)
        return None
    
    @when(AST.RelExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        ops = {
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '>': operator.gt,
            '<=': operator.le,
            '>=': operator.ge,
        }
        
        if node.op in ops:
            return ops[node.op](left, right)
        return None
    
    @when(AST.Assignment)
    def visit(self, node):
        value = node.right.accept(self)
        
        if isinstance(node.left, AST.Variable):
            var_name = node.left.name
            
            if node.op == '=':
                self.memory_stack.set(var_name, value)
            else:
                current = self.memory_stack.get(var_name)
                ops = {
                    '+=': operator.add,
                    '-=': operator.sub,
                    '*=': operator.mul,
                    '/=': operator.truediv,
                }
                if node.op in ops:
                    new_value = ops[node.op](current, value)
                    self.memory_stack.set(var_name, new_value)
        
        elif isinstance(node.left, AST.VectorElement):
            var_name = node.left.name
            index = node.left.index
            vec = self.memory_stack.get(var_name)
            vec[index] = value
        
        elif isinstance(node.left, AST.MatrixElement):
            var_name = node.left.name
            row = node.left.row
            col = node.left.col
            mat = self.memory_stack.get(var_name)
            mat[row, col] = value
        
        return value
    
    @when(AST.If)
    def visit(self, node):
        condition = node.condition.accept(self)
        if condition:
            return node.then_block.accept(self)
        elif node.else_block:
            return node.else_block.accept(self)
        return None
    
    @when(AST.While)
    def visit(self, node):
        result = None
        try:
            while node.condition.accept(self):
                try:
                    result = node.body.accept(self)
                except ContinueException:
                    continue
        except BreakException:
            pass
        return result
    
    @when(AST.For)
    def visit(self, node):
        result = None
        range_obj = node.range.accept(self)
        var_name = node.var.name
        
        try:
            for i in range_obj:
                self.memory_stack.set(var_name, i)
                try:
                    result = node.body.accept(self)
                except ContinueException:
                    continue
        except BreakException:
            pass
        
        return result
    
    @when(AST.Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return range(int(start), int(end) + 1)
    
    @when(AST.Break)
    def visit(self, node):
        raise BreakException()
    
    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.Return)
    def visit(self, node):
        value = node.expr.accept(self)
        raise ReturnValueException(value)
    
    @when(AST.Print)
    def visit(self, node):
        values = []
        for val in node.values:
            result = val.accept(self)
            if isinstance(result, np.ndarray):
                values.append(str(result))
            else:
                values.append(str(result))
        print(' '.join(values))
    
    @when(AST.IntNum)
    def visit(self, node):
        return node.value
    
    @when(AST.FloatNum)
    def visit(self, node):
        return node.value
    
    @when(AST.String)
    def visit(self, node):
        return node.value
    
    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)
    
    @when(AST.VectorElement)
    def visit(self, node):
        vec = self.memory_stack.get(node.name)
        return vec[node.index]
    
    @when(AST.MatrixElement)
    def visit(self, node):
        mat = self.memory_stack.get(node.name)
        return mat[node.row, node.col]
    
    @when(AST.Vector)
    def visit(self, node):
        elements = [elem.accept(self) for elem in node.elements]
        return np.array(elements)
    
    @when(AST.Matrix)
    def visit(self, node):
        rows = []
        for row in node.rows:
            row_data = row.accept(self)
            rows.append(row_data)
        return np.array(rows)
    
    @when(AST.MatrixFunction)
    def visit(self, node):
        if isinstance(node.size, tuple):
            rows, cols = node.size
        else:
            rows = cols = node.size
        
        if node.name == 'zeros':
            return np.zeros((rows, cols))
        elif node.name == 'ones':
            return np.ones((rows, cols))
        elif node.name == 'eye':
            return np.eye(rows, cols)
        return None
    
    @when(AST.UnaryMinus)
    def visit(self, node):
        value = node.expr.accept(self)
        return -value
    
    @when(AST.Transposition)
    def visit(self, node):
        mat = node.expr.accept(self)
        return mat.T