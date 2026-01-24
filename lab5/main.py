import sys
import ply.yacc as yacc
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "triangle.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    scanner = Scanner()
    parser = Mparser()
    text = file.read()

    # Parse
    tokens = scanner.tokenize(text)
    ast = parser.parse(tokens)
    
    if ast is None:
        print("Parsing failed")
        sys.exit(1)

    # Type checking
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    
    # Only interpret if no errors
    if not typeChecker.errors:
        interpreter = Interpreter()
        try:
            ast.accept(interpreter)
        except Exception as e:
            print(f"Runtime error: {e}")
    else:
        print("Type checking failed, interpretation skipped")