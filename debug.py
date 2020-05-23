import calculator.lexer as lexer
import calculator.parser as parser

code = '(5.0 6. 1.) * 8.0'
tokens = lexer.parse_interactive(code)
if tokens:
    expr = parser.parse_interactive(tokens, code)
if expr:
    print(expr.get_value())
