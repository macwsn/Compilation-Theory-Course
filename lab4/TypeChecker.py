#!/usr/bin/python

import AST
from SymbolTable import SymbolTable, VariableSymbol

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "root")
        self.loop_depth = 0
        self.errors = []
        
        self.ttype = {
            # Arithmetic operations: +, -, *, /
            '+': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('vector', 'vector'): ('vector', 'same_size'),
                ('matrix', 'matrix'): ('matrix', 'same_size'),
            },
            '-': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('vector', 'vector'): ('vector', 'same_size'),
                ('matrix', 'matrix'): ('matrix', 'same_size'),
            },
            '*': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('matrix', 'matrix'): ('matrix', 'matrix_mul'),
            },
            '/': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
            },
            # Element-wise operations: .+, .-, .*, ./
            '.+': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('vector', 'vector'): ('vector', 'same_size'),
                ('matrix', 'matrix'): ('matrix', 'same_size'),
            },
            '.-': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('vector', 'vector'): ('vector', 'same_size'),
                ('matrix', 'matrix'): ('matrix', 'same_size'),
            },
            '.*': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('vector', 'vector'): ('vector', 'same_size'),
                ('matrix', 'matrix'): ('matrix', 'same_size'),
            },
            './': {
                ('int', 'int'): ('int', None),
                ('int', 'float'): ('float', None),
                ('float', 'int'): ('float', None),
                ('float', 'float'): ('float', None),
                ('vector', 'vector'): ('vector', 'same_size'),
                ('matrix', 'matrix'): ('matrix', 'same_size'),
            },
        }

    def error(self, msg, lineno=0):
        self.errors.append(f"Line {lineno}: {msg}")
        print(f"Line {lineno}: {msg}")

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_BinExpr(self, node):
        left_info = self.visit(node.left)
        right_info = self.visit(node.right)
        op = node.op
        
        if left_info is None or right_info is None:
            return None
        
        left_type, left_shape = left_info
        right_type, right_shape = right_info
        
        if op in self.ttype:
            key = (left_type, right_type)
            if key not in self.ttype[op]:
                self.error(f"Invalid operands for {op}: {left_type} and {right_type}", node.lineno)
                return None
            
            result_type, constraint = self.ttype[op][key]

            if constraint == 'same_size':
                if left_shape != right_shape:
                    self.error(f"Incompatible shapes for {op}: {left_shape} and {right_shape}", node.lineno)
                    return None
                return (result_type, left_shape)
            
            elif constraint == 'matrix_mul':
                if left_shape is None or right_shape is None:
                    return (result_type, None)
                if len(left_shape) == 2 and len(right_shape) == 2:
                    if left_shape[1] != right_shape[0]:
                        self.error(f"Matrix multiplication: incompatible dimensions {left_shape} and {right_shape}", node.lineno)
                        return None
                    return (result_type, (left_shape[0], right_shape[1]))
                return (result_type, None)
            
            else:
                return (result_type, left_shape if left_shape else right_shape)
        
        return None

    def visit_RelExpr(self, node):
        left_info = self.visit(node.left)
        right_info = self.visit(node.right)
        
        if left_info is None or right_info is None:
            return ('int', None)
        
        left_type, left_shape = left_info
        right_type, right_shape = right_info
        
        if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
            self.error(f"Relational operator {node.op} requires scalar operands", node.lineno)
        
        return ('int', None)

    def visit_Assignment(self, node):
        right_info = self.visit(node.right)
        
        if right_info is None:
            return None
        
        right_type, right_shape = right_info

        if isinstance(node.left, AST.Variable):
            var_name = node.left.name
            
            if node.op == '=':

                symbol = VariableSymbol(var_name, right_type, right_shape)
                self.symbol_table.put(var_name, symbol)
            else:
                # Compound assignment (+=, -=, *=, /=) - variable must exist
                symbol = self.symbol_table.get(var_name)
                if symbol is None:
                    self.error(f"Variable '{var_name}' not defined", node.lineno)
                else:
                    op_base = node.op[0]  # Get '+', '-', '*', '/'
                    left_type, left_shape = symbol.type, symbol.shape

                    if op_base in self.ttype:
                        key = (left_type, right_type)
                        if key not in self.ttype[op_base]:
                            self.error(f"Invalid compound assignment {node.op}: {left_type} and {right_type}", node.lineno)
                        elif left_type in ['vector', 'matrix'] and left_shape != right_shape:
                            self.error(f"Incompatible shapes for {node.op}: {left_shape} and {right_shape}", node.lineno)

        elif isinstance(node.left, (AST.MatrixElement, AST.VectorElement)):
            self.visit(node.left)
        
        return right_info

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.then_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_While(self, node):
        self.visit(node.condition)
        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1

    def visit_For(self, node):
        range_info = self.visit(node.range)

        if isinstance(node.var, AST.Variable):
            symbol = VariableSymbol(node.var.name, 'int', None)
            self.symbol_table.put(node.var.name, symbol)
        
        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1

    def visit_Range(self, node):
        start_info = self.visit(node.start)
        end_info = self.visit(node.end)
        
        if start_info and start_info[0] not in ['int', 'float']:
            self.error(f"Range start must be numeric", node.lineno)
        
        if end_info and end_info[0] not in ['int', 'float']:
            self.error(f"Range end must be numeric", node.lineno)
        
        return ('int', None)

    def visit_Break(self, node):
        if self.loop_depth == 0:
            self.error("Break statement outside loop", node.lineno)

    def visit_Continue(self, node):
        if self.loop_depth == 0:
            self.error("Continue statement outside loop", node.lineno)

    def visit_Return(self, node):
        self.visit(node.expr)

    def visit_Print(self, node):
        for val in node.values:
            self.visit(val)

    def visit_IntNum(self, node):
        return ('int', None)

    def visit_FloatNum(self, node):
        return ('float', None)

    def visit_String(self, node):
        return ('string', None)

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.error(f"Variable '{node.name}' not defined", node.lineno)
            return None
        return (symbol.type, symbol.shape)

    def visit_VectorElement(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.error(f"Variable '{node.name}' not defined", node.lineno)
            return None
        
        if symbol.type not in ['vector', 'matrix']:
            self.error(f"Variable '{node.name}' is not indexable", node.lineno)
            return None
        
        # Check bounds - indeksy są 0-based
        index = node.index
        if symbol.shape:
            if symbol.type == 'vector':
                size = symbol.shape[0]
                if index < 0 or index >= size:
                    self.error(f"Index {index} out of bounds for vector of size {size}", node.lineno)
            elif symbol.type == 'matrix':
                rows = symbol.shape[0]
                if index < 0 or index >= rows:
                    self.error(f"Row index {index} out of bounds for matrix with {rows} rows", node.lineno)
        
        if symbol.type == 'vector':
            return ('float', None)
        else:  # matrix
            if symbol.shape and len(symbol.shape) == 2:
                return ('vector', (symbol.shape[1],))
            return ('vector', None)

    def visit_MatrixElement(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.error(f"Variable '{node.name}' not defined", node.lineno)
            return None
        
        if symbol.type != 'matrix':
            self.error(f"Variable '{node.name}' is not a matrix", node.lineno)
            return None
        
        # Check bounds - indeksy są 0-based
        row = node.row
        col = node.col
        if symbol.shape and len(symbol.shape) == 2:
            rows, cols = symbol.shape
            if row < 0 or row >= rows:
                self.error(f"Row index {row} out of bounds for matrix with {rows} rows", node.lineno)
            if col < 0 or col >= cols:
                self.error(f"Column index {col} out of bounds for matrix with {cols} columns", node.lineno)
        
        return ('float', None)

    def visit_Matrix(self, node):
        if not node.rows:
            return ('matrix', (0, 0))

        row_sizes = []
        for i, row in enumerate(node.rows):
            if not isinstance(row, AST.Vector):
                self.error(f"Matrix row {i} is not a vector", node.lineno)
                continue
            
            row_info = self.visit(row)
            if row_info and row_info[1]:
                row_sizes.append(row_info[1][0])
            else:
                row_sizes.append(len(row.elements))

        if row_sizes and len(set(row_sizes)) > 1:
            self.error(f"Matrix rows have different sizes: {set(row_sizes)}", node.lineno)
            return ('matrix', None)
        
        if row_sizes:
            return ('matrix', (len(node.rows), row_sizes[0]))
        return ('matrix', (len(node.rows), 0))

    def visit_Vector(self, node):
        if not node.elements:
            return ('vector', (0,))
        
        for elem in node.elements:
            self.visit(elem)
        
        return ('vector', (len(node.elements),))

    def visit_MatrixFunction(self, node):
        size_value = node.size

        if isinstance(size_value, tuple):
            rows, cols = size_value
            if rows <= 0 or cols <= 0:
                self.error(f"Matrix function '{node.name}' requires positive dimensions, got ({rows}, {cols})", node.lineno)
                return None
            return ('matrix', (rows, cols))
        else:
            if size_value <= 0:
                self.error(f"Matrix function '{node.name}' requires positive size, got {size_value}", node.lineno)
                return None
            return ('matrix', (size_value, size_value))

    def visit_UnaryMinus(self, node):
        expr_info = self.visit(node.expr)
        if expr_info is None:
            return None
        
        expr_type, expr_shape = expr_info
        if expr_type not in ['int', 'float', 'vector', 'matrix']:
            self.error(f"Unary minus not applicable to {expr_type}", node.lineno)
            return None
        
        return expr_info

    def visit_Transposition(self, node):
        expr_info = self.visit(node.expr)
        if expr_info is None:
            return None
        
        expr_type, expr_shape = expr_info
        if expr_type != 'matrix':
            self.error(f"Transpose only applicable to matrices, not {expr_type}", node.lineno)
            return None

        if expr_shape and len(expr_shape) == 2:
            return ('matrix', (expr_shape[1], expr_shape[0]))
        return ('matrix', None)