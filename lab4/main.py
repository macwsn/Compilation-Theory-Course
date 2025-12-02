import sys
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "test.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    file.close()

    scanner = Scanner()
    parser = Mparser()
    ast = parser.parse(scanner.tokenize(text))

    if ast is None:
        print("Parsing failed")
        sys.exit(1)

    print("\n=== Semantic Analysis ===\n")
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)
    
    if typeChecker.errors:
        print(f"\nFound {len(typeChecker.errors)} semantic error(s)")
    else:
        print("\nNo semantic errors found")