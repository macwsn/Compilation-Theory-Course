from sly import Parser
from scanner import Scanner
import AST

class Mparser(Parser):

    tokens = Scanner.tokens

    start = 'program'
    
    debugfile = 'parser_new.out'
    expected_shift_reduce = 1

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '='),
        ('nonassoc', '<', '>', 'LEQ', 'GEQ', 'NEQ', 'EQ'),
        ('left', '+', '-'),
        ('left', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ('left', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', "'"),
    )

    @_('instructions_opt')
    def program(self, p):
        return AST.Program(p.instructions_opt)

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return AST.Instructions()

    @_('instructions instruction')
    def instructions(self, p):
        p.instructions.add(p.instruction)
        return p.instructions

    @_('instruction')
    def instructions(self, p):
        instructions = AST.Instructions()
        instructions.add(p.instruction)
        return instructions

    @_('"{" instructions "}"')
    def instruction(self, p):
        return p.instructions

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p.condition, p.instruction, lineno=p.lineno)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.If(p.condition, p.instruction0, p.instruction1, lineno=p.lineno)

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p.condition, p.instruction, lineno=p.lineno)

    @_('FOR ID "=" range_expr instruction')
    def instruction(self, p):
        return AST.For(AST.Variable(p.ID, lineno=p.lineno), p.range_expr, p.instruction, lineno=p.lineno)
    
    @_('expression ":" expression')
    def range_expr(self, p):
        return AST.Range(p.expression0, p.expression1, lineno=p.lineno)

    @_('ID "=" expression ";"')
    def instruction(self, p):
        return AST.Assignment('=', AST.Variable(p.ID, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('ID ADDASSIGN expression ";"')
    def instruction(self, p):
        return AST.Assignment('+=', AST.Variable(p.ID, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('ID SUBASSIGN expression ";"')
    def instruction(self, p):
        return AST.Assignment('-=', AST.Variable(p.ID, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('ID MULASSIGN expression ";"')
    def instruction(self, p):
        return AST.Assignment('*=', AST.Variable(p.ID, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('ID DIVASSIGN expression ";"')
    def instruction(self, p):
        return AST.Assignment('/=', AST.Variable(p.ID, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('ID "[" INTNUM "]" "=" expression ";"')
    def instruction(self, p):
        return AST.Assignment('=', AST.VectorElement(p.ID, p.INTNUM, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('ID "[" INTNUM "," INTNUM "]" "=" expression ";"')
    def instruction(self, p):
        return AST.Assignment('=', AST.MatrixElement(p.ID, p.INTNUM0, p.INTNUM1, lineno=p.lineno), p.expression, lineno=p.lineno)

    @_('BREAK ";"')
    def instruction(self, p):
        return AST.Break(lineno=p.lineno)

    @_('CONTINUE ";"')
    def instruction(self, p):
        return AST.Continue(lineno=p.lineno)

    @_('RETURN expression ";"')
    def instruction(self, p):
        return AST.Return(p.expression, lineno=p.lineno)

    @_('PRINT print_list ";"')
    def instruction(self, p):
        return AST.Print(p.print_list, lineno=p.lineno)

    @_('print_list "," print_item')
    def print_list(self, p):
        return p.print_list + [p.print_item]
    
    @_('print_item')
    def print_list(self, p):
        return [p.print_item]

    @_('STRING')
    def print_item(self, p):
        return AST.String(p.STRING, lineno=p.lineno)
    
    @_('expression')
    def print_item(self, p):
        return p.expression

    @_('expression EQ expression')
    def condition(self, p):
        return AST.RelExpr('==', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression NEQ expression')
    def condition(self, p):
        return AST.RelExpr('!=', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression LEQ expression')
    def condition(self, p):
        return AST.RelExpr('<=', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression GEQ expression')
    def condition(self, p):
        return AST.RelExpr('>=', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression "<" expression')
    def condition(self, p):
        return AST.RelExpr('<', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression ">" expression')
    def condition(self, p):
        return AST.RelExpr('>', p.expression0, p.expression1, lineno=p.lineno)

    @_('expression "+" expression')
    def expression(self, p):
        return AST.BinExpr('+', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression "-" expression')
    def expression(self, p):
        return AST.BinExpr('-', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression "*" expression')
    def expression(self, p):
        return AST.BinExpr('*', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression "/" expression')
    def expression(self, p):
        return AST.BinExpr('/', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression DOTADD expression')
    def expression(self, p):
        return AST.BinExpr('.+', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression DOTSUB expression')
    def expression(self, p):
        return AST.BinExpr('.-', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression DOTMUL expression')
    def expression(self, p):
        return AST.BinExpr('.*', p.expression0, p.expression1, lineno=p.lineno)
    
    @_('expression DOTDIV expression')
    def expression(self, p):
        return AST.BinExpr('./', p.expression0, p.expression1, lineno=p.lineno)

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        return AST.UnaryMinus(p.expression, lineno=p.lineno)
    
    @_('expression "\'"')
    def expression(self, p):
        return AST.Transposition(p.expression, lineno=p.lineno)

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('ID')
    def expression(self, p):
        return AST.Variable(p.ID, lineno=p.lineno)

    @_('ID "[" INTNUM "]"')
    def expression(self, p):
        return AST.VectorElement(p.ID, p.INTNUM, lineno=p.lineno)
    
    @_('ID "[" INTNUM "," INTNUM "]"')
    def expression(self, p):
        return AST.MatrixElement(p.ID, p.INTNUM0, p.INTNUM1, lineno=p.lineno)

    @_('INTNUM')
    def expression(self, p):
        return AST.IntNum(p.INTNUM, lineno=p.lineno)
    
    @_('FLOATNUM')
    def expression(self, p):
        return AST.FloatNum(p.FLOATNUM, lineno=p.lineno)

    @_('"[" inner_lists "]"')
    def expression(self, p):
        # Check if we have nested lists (matrix) or flat list (vector)
        if all(isinstance(item, AST.Vector) for item in p.inner_lists):
            # All items are vectors - this is a matrix
            return AST.Matrix(p.inner_lists, lineno=p.lineno)
        else:
            # Flat list - this is a vector
            return AST.Vector(p.inner_lists, lineno=p.lineno)

    @_('inner_lists "," inner_item')
    def inner_lists(self, p):
        return p.inner_lists + [p.inner_item]
    
    @_('inner_item')
    def inner_lists(self, p):
        return [p.inner_item]

    @_('"[" elem_list "]"')
    def inner_item(self, p):
        # Nested brackets - this is a vector (row of matrix)
        return AST.Vector(p.elem_list, lineno=p.lineno)
    
    @_('elem')
    def inner_item(self, p):
        # Direct element - for flat vectors
        return p.elem

    @_('elem_list "," elem')
    def elem_list(self, p):
        return p.elem_list + [p.elem]
    
    @_('elem')
    def elem_list(self, p):
        return [p.elem]

    @_('INTNUM')
    def elem(self, p):
        return AST.IntNum(p.INTNUM, lineno=p.lineno)
    
    @_('FLOATNUM')
    def elem(self, p):
        return AST.FloatNum(p.FLOATNUM, lineno=p.lineno)

    @_('STRING')
    def expression(self, p):
        return AST.String(p.STRING, lineno=p.lineno)
    
    @_('ID')
    def elem(self, p):
        return AST.Variable(p.ID, lineno=p.lineno)

    @_('ZEROS "(" matrix_size ")"')
    def expression(self, p):
        return AST.MatrixFunction('zeros', p.matrix_size, lineno=p.lineno)
    
    @_('ZEROS "(" matrix_size "," matrix_size ")"')
    def expression(self, p):
        return AST.MatrixFunction('zeros', (p.matrix_size0, p.matrix_size1), lineno=p.lineno)

    @_('ONES "(" matrix_size ")"')
    def expression(self, p):
        return AST.MatrixFunction('ones', p.matrix_size, lineno=p.lineno)
    
    @_('ONES "(" matrix_size "," matrix_size ")"')
    def expression(self, p):
        return AST.MatrixFunction('ones', (p.matrix_size0, p.matrix_size1), lineno=p.lineno)

    @_('EYE "(" matrix_size ")"')
    def expression(self, p):
        return AST.MatrixFunction('eye', p.matrix_size, lineno=p.lineno)
    
    @_('EYE "(" matrix_size "," matrix_size ")"')
    def expression(self, p):
        return AST.MatrixFunction('eye', (p.matrix_size0, p.matrix_size1), lineno=p.lineno)

    @_('INTNUM')
    def matrix_size(self, p):
        return p.INTNUM
    
    @_('"-" INTNUM')
    def matrix_size(self, p):
        return -p.INTNUM

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            print("Unexpected end of input")