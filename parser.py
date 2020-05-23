from typing import List

from calculator.ast import *
from calculator.input import Input, TokenInput
from calculator.token import Token, TokenType

class ParserError:

    def __init__(self, message, pos, target=False):
        self.message = message
        self.pos = pos
        self.target = target

    def print(self, context=None, preview=10, postview=5):
        pmsg = self.message + " at position " + str(self.pos)

        if context:
            start = max(0, self.pos - preview)
            mid = min(len(context), self.pos + 1)
            end = min(len(context), self.pos + 1 + postview)

            pmsg += "        \"" + context[start:self.pos]

            if self.target:
                pmsg += "[" + context[self.pos] + "]"
            else:
                if self.pos < len(context):
                    pmsg += "[x] " + context[self.pos]
                else:
                    pmsg += "[x]"

            pmsg += context[mid:end] + "\""

        print(pmsg)

def expect(input: TokenInput, errors: List[ParserError], token_type: TokenType, representation: str):
    if input.current().token_type != token_type:
        errors.append(ParserError("Expected '" + representation + "'", input.current().pos))
    else:
        input.next()

# parse functions for all non-terminals
def parse_E(input: TokenInput, errors: List[ParserError]) -> Expression:
    left = parse_T(input, errors)
    operation = parse_E_(input, errors, left)

    if operation is None:
        return left
    else:
        return operation

def parse_E_(input: TokenInput, errors: List[ParserError], left: Expression) -> Expression:
    def parse_E_1():
        input.next() # PLUS

        right = parse_T(input, errors)
        operation = AddOperation(left, right)

        return parse_E_(input, errors, operation)
    def parse_E_2():
        input.next() # MINUS

        right = parse_T(input, errors)
        operation = SubtractOperation(left, right)

        return parse_E_(input, errors, operation)
    def parse_E_3(): # RPAREN or END
        return None
    def parse_E_4():
        errors.append(ParserError("Expected operator", input.current().pos))

        right = parse_T(input, errors)
        operation = UnknownOperation(left, right)

        return parse_E_(input, errors, operation)

    parse = {
        TokenType.PLUS: parse_E_1,
        TokenType.MINUS: parse_E_2,
        TokenType.RPAREN: parse_E_3,
        TokenType.END: parse_E_3
    }.get(input.current().token_type, parse_E_4)

    return parse()

def parse_T(input: TokenInput, errors: List[ParserError]) -> Expression:
    left = parse_F(input, errors)
    operation = parse_T_(input, errors, left)

    if operation is None:
        return left
    else:
        return operation

def parse_T_(input: TokenInput, errors: List[ParserError], left: Expression) -> Expression:
    def parse_T_1():
        input.next() # STAR

        right = parse_F(input, errors)
        operation = MultiplyOperation(left, right)

        return parse_T_(input, errors, operation)
    def parse_T_2():
        input.next() # SLASH

        right = parse_F(input, errors)
        operation = DivideOperation(left, right)

        return parse_T_(input, errors, operation)
    def parse_T_3(): # PLUS, MINUS, RPAREN or END
        return None
    def parse_T_4():
        errors.append(ParserError("Expected operator", input.current().pos))

        right = parse_F(input, errors)
        operation = UnknownOperation(left, right)

        return parse_T_(input, errors, operation)

    parse = {
        TokenType.STAR: parse_T_1,
        TokenType.SLASH: parse_T_2,
        TokenType.PLUS: parse_T_3,
        TokenType.MINUS: parse_T_3,
        TokenType.RPAREN: parse_T_3,
        TokenType.END: parse_T_3
    }.get(input.current().token_type, parse_T_4)

    return parse()

def parse_F(input: TokenInput, errors: List[ParserError]) -> Expression:
    def parse_F_1():
        input.next() # LPAREN

        operation = parse_E(input, errors)
        expect(input, errors, TokenType.RPAREN, ')')

        return operation
    def parse_F_2(): # NUMBER
        value =  Value(input.current().numeric_value())
        input.next()

        return value
    def parse_F_3():
        errors.append(ParserError("Expected number or expression in parentheses", input.current().pos))

    parse = {
        TokenType.LPAREN: parse_F_1,
        TokenType.NUMBER: parse_F_2
    }.get(input.current().token_type, parse_F_3)

    return parse()

# main functions
def parse(tokens: List[Token]) -> (Expression, List[ParserError]):
    input = TokenInput(tokens)

    errors = []
    expr = parse_E(input, errors)

    while input.current().token_type != TokenType.END:
        while input.current().token_type == TokenType.RPAREN:
            errors.append(ParserError("Invalid ')'", input.current().pos, target=True))

            input.next()

        if input.current().token_type in [TokenType.PLUS, TokenType.MINUS, TokenType.NUMBER]:
            expr = parse_E_(input, errors, expr)
        elif input.current().token_type in [TokenType.STAR, TokenType.SLASH]:
            expr = parse_T_(input, errors, expr)

    return (expr, errors)

def parse_interactive(tokens: List[Token], code: str) -> Expression:
    (expr, errors) = parse(tokens)

    if errors:
        for error in errors:
            error.print(code)
    else:
        return expr
