from sly import Parser
from scanner import Scanner
import AST

class Mparser(Parser):

    tokens = Scanner.tokens

    start = 'program'
    
    #debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
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

    @_('instruction')
    def instructions(self, p):
        instructions = AST.Instructions()
        instructions.add(p.instruction)
        return instructions

    @_('instruction instructions')
    def instructions(self, p):
        p.instructions.instructions.insert(0, p.instruction)
        return p.instructions

    @_('assignment ";"',
       'statement ";"')
    def instruction(self, p):
        return p[0]

    @_('"{" instructions "}"')
    def instruction(self, p):
        return p.instructions

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p.condition, p.instruction)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.If(p.condition, p.instruction0, p.instruction1)

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p.condition, p.instruction)

    @_('FOR var "=" range instruction')
    def instruction(self, p):
        return AST.For(p.var, p.range, p.instruction)

    @_('expression ":" expression')
    def range(self, p):
        return AST.Range(p.expression0, p.expression1)

    @_('expression EQ expression')
    def condition(self, p):
        return AST.RelExpr('==', p.expression0, p.expression1)
    
    @_('expression NEQ expression')
    def condition(self, p):
        return AST.RelExpr('!=', p.expression0, p.expression1)
    
    @_('expression LEQ expression')
    def condition(self, p):
        return AST.RelExpr('<=', p.expression0, p.expression1)
    
    @_('expression GEQ expression')
    def condition(self, p):
        return AST.RelExpr('>=', p.expression0, p.expression1)
    
    @_('expression "<" expression')
    def condition(self, p):
        return AST.RelExpr('<', p.expression0, p.expression1)
    
    @_('expression ">" expression')
    def condition(self, p):
        return AST.RelExpr('>', p.expression0, p.expression1)

    @_('MULASSIGN')
    def assignment_op(self, p):
        return '*='
    
    @_('DIVASSIGN')
    def assignment_op(self, p):
        return '/='
    
    @_('SUBASSIGN')
    def assignment_op(self, p):
        return '-='
    
    @_('ADDASSIGN')
    def assignment_op(self, p):
        return '+='
    
    @_('"="')
    def assignment_op(self, p):
        return '='

    @_('var assignment_op expression')
    def assignment(self, p):
        return AST.Assignment(p.assignment_op, p.var, p.expression)
    
    @_('matrix_element assignment_op expression')
    def assignment(self, p):
        return AST.Assignment(p.assignment_op, p.matrix_element, p.expression)
    
    @_('vector_element assignment_op expression')
    def assignment(self, p):
        return AST.Assignment(p.assignment_op, p.vector_element, p.expression)

    @_('matrix_function_name "(" INTNUM ")"')
    def matrix_function(self, p):
        return AST.MatrixFunction(p.matrix_function_name, p.INTNUM)

    @_('EYE')
    def matrix_function_name(self, p):
        return 'eye'
    
    @_('ONES')
    def matrix_function_name(self, p):
        return 'ones'
    
    @_('ZEROS')
    def matrix_function_name(self, p):
        return 'zeros'

    @_('"[" vectors "]"')
    def matrix(self, p):
        return AST.Matrix(p.vectors)

    @_('vectors "," vector')
    def vectors(self, p):
        return p.vectors + [p.vector]
    
    @_('vector')
    def vectors(self, p):
        return [p.vector]

    @_('"[" variables "]"')
    def vector(self, p):
        return AST.Vector(p.variables)

    @_('variables "," variable')
    def variables(self, p):
        return p.variables + [p.variable]
    
    @_('variable')
    def variables(self, p):
        return [p.variable]

    @_('number')
    def variable(self, p):
        return p.number
    
    @_('var')
    def variable(self, p):
        return p.var
    
    @_('element')
    def variable(self, p):
        return p.element

    @_('vector_element')
    def element(self, p):
        return p.vector_element
    
    @_('matrix_element')
    def element(self, p):
        return p.matrix_element

    @_('ID "[" INTNUM "]"')
    def vector_element(self, p):
        return AST.VectorElement(p.ID, p.INTNUM)

    @_('ID "[" INTNUM "," INTNUM "]"')
    def matrix_element(self, p):
        return AST.MatrixElement(p.ID, p.INTNUM0, p.INTNUM1)

    @_('ID')
    def var(self, p):
        return AST.Variable(p.ID)

    @_('INTNUM')
    def number(self, p):
        return AST.IntNum(p.INTNUM)
    
    @_('FLOATNUM')
    def number(self, p):
        return AST.FloatNum(p.FLOATNUM)

    @_('STRING')
    def string(self, p):
        return AST.String(p.STRING)

    @_('expression "+" expression')
    def expression(self, p):
        return AST.BinExpr('+', p.expression0, p.expression1)
    
    @_('expression "-" expression')
    def expression(self, p):
        return AST.BinExpr('-', p.expression0, p.expression1)
    
    @_('expression "*" expression')
    def expression(self, p):
        return AST.BinExpr('*', p.expression0, p.expression1)
    
    @_('expression "/" expression')
    def expression(self, p):
        return AST.BinExpr('/', p.expression0, p.expression1)
    
    @_('expression DOTADD expression')
    def expression(self, p):
        return AST.BinExpr('.+', p.expression0, p.expression1)
    
    @_('expression DOTSUB expression')
    def expression(self, p):
        return AST.BinExpr('.-', p.expression0, p.expression1)
    
    @_('expression DOTMUL expression')
    def expression(self, p):
        return AST.BinExpr('.*', p.expression0, p.expression1)
    
    @_('expression DOTDIV expression')
    def expression(self, p):
        return AST.BinExpr('./', p.expression0, p.expression1)

    @_('num_expression')
    def expression(self, p):
        return p.num_expression
    
    @_('matrix')
    def expression(self, p):
        return p.matrix
    
    @_('matrix_function')
    def expression(self, p):
        return p.matrix_function
    
    @_('uminus')
    def expression(self, p):
        return p.uminus
    
    @_('transposition')
    def expression(self, p):
        return p.transposition
    
    @_('matrix_element')
    def expression(self, p):
        return p.matrix_element
    
    @_('vector_element')
    def expression(self, p):
        return p.vector_element

    @_('number')
    def num_expression(self, p):
        return p.number
    
    @_('var')
    def num_expression(self, p):
        return p.var

    @_('"-" expression %prec UMINUS')
    def uminus(self, p):
        return AST.UnaryMinus(p.expression)

    @_('expression "\'"')
    def transposition(self, p):
        return AST.Transposition(p.expression)

    @_('BREAK')
    def statement(self, p):
        return AST.Break()

    @_('CONTINUE')
    def statement(self, p):
        return AST.Continue()

    @_('RETURN expression')
    def statement(self, p):
        return AST.Return(p.expression)

    @_('PRINT print_vals')
    def statement(self, p):
        return AST.Print(p.print_vals)

    @_('print_vals "," print_val')
    def print_vals(self, p):
        return p.print_vals + [p.print_val]
    
    @_('print_val')
    def print_vals(self, p):
        return [p.print_val]

    @_('string')
    def print_val(self, p):
        return p.string
    
    @_('expression')
    def print_val(self, p):
        return p.expression

    # Error handling
    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            print("Unexpected end of input")