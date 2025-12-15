import sys
from sly import Lexer

class Scanner(Lexer):
    tokens = {DOTADD, DOTMUL, DOTDIV, DOTSUB,
              ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
              LEQ, GEQ, NEQ, EQ,
              IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT,
              INTNUM, FLOATNUM, STRING, ID}
    
    literals = {'+', '-', '*', '/', '=', '<', '>', 
                '(', ')', '[', ']', '{', '}',
                ':', ',', ';', "'"}
    
    ignore = ' \t'
    ignore_comment = r'\#.*'
    
    DOTADD = r'\.\+'
    DOTSUB = r'\.\-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    
    LEQ = r'<='
    GEQ = r'>='
    NEQ = r'!='
    EQ = r'=='
    
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        keywords = {
            'if': 'IF',
            'else': 'ELSE',
            'for': 'FOR',
            'while': 'WHILE',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'return': 'RETURN',
            'eye': 'EYE',
            'zeros': 'ZEROS',
            'ones': 'ONES',
            'print': 'PRINT'
        }
        t.type = keywords.get(t.value, 'ID')
        return t
    # @_(r'\d+\.\d*([eE][+-]?\d+)?|\.\d+([eE][+-]?\d+)?|\d+[eE][+-]?\d+')
    @_(r'(\d*\.\d+|\d+\.\d*)([eE][+-]?\d+)?|\d+[eE][+-]?\d+')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'"([^"\\]|\\.)*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        self.lineno += t.value.count('\n') # to dodano
        return t
    
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)
    
    def error(self, t):
        print(f"Line {self.lineno}: Illegal character '{t.value[0]}'")
        self.index += 1


if __name__ == '__main__':
    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    
    try:
        with open(filename, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    for tok in lexer.tokenize(text):
        if tok.type in lexer.literals:
            print(f"({tok.lineno}): {tok.value}({tok.value})")
        else:
            print(f"({tok.lineno}): {tok.type}({tok.value})")