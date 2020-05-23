from enum import Enum, auto
from typing import List

from calculator.helper import char_range
from calculator.input import StringInput
from calculator.token import Token, TokenType

# ranges
digits = list(char_range('0', '9'))
exponent = ['e', 'E']
sign = ['+', '-']
suffix = ['f', 'F', 'l', 'L']

# expect functions
def expect_char(input: StringInput, expected: str):
    if input.current() != expected:
        raise Exception("Expected input '" + str(expected) + "' at positition " + str(input.get_index()))

    input.next()

def expect_range(input: StringInput, expected: List[str], name: str):
    if input.current() not in expected:
        raise Exception("Expected " + name + " at position " + str(input.get_index()))

    input.next()

def expect_other(input: StringInput, name: str):
    raise Exception("Expected " + name + " at position " + str(input.get_index()))

# parse functions for all tokens
def parse_plus(input: StringInput) -> Token:
    index = input.get_index()

    expect_char(input, '+')

    return Token(TokenType.PLUS, index)

def parse_minus(input: StringInput) -> Token:
    index = input.get_index()

    expect_char(input, '-')

    return Token(TokenType.MINUS, index)

def parse_star(input: StringInput) -> Token:
    index = input.get_index()

    expect_char(input, '*')

    return Token(TokenType.STAR, index)

def parse_slash(input: StringInput) -> Token:
    index = input.get_index()

    expect_char(input, '/')

    return Token(TokenType.SLASH, index)

def parse_lparen(input: StringInput) -> Token:
    index = input.get_index()

    expect_char(input, '(')

    return Token(TokenType.LPAREN, index)

def parse_rparen(input: StringInput) -> Token:
    index = input.get_index()

    expect_char(input, ')')

    return Token(TokenType.RPAREN, index)

def parse_number(input: StringInput) -> Token:
    index = input.get_index()
    input.clear_record()

    if input.current() == '.':
        input.next()

        expect_range(input, digits, 'digit')
    elif input.current() in digits:
        input.next()

        while input.current() in digits:
            input.next()

        expect_char(input, '.')
    else:
        expect_other(input, 'digit or \'.\'')

    while input.current() in digits:
        input.next()

    if input.current() in suffix:
        input.next()

        return Token(TokenType.NUMBER, index, input.get_record())
    elif input.current() in exponent:
        input.next()

        if input.current() in sign:
            input.next()

            expect_range(input, digits, 'digit')
        elif input.current() in digits:
            input.next()
        else:
            expect_other(input, 'sign or digit')

        while input.current() in digits:
            input.next()

        if input.current() in suffix:
            input.next()

        return Token(TokenType.NUMBER, index, input.get_record())
    else:
        return Token(TokenType.NUMBER, index, input.get_record())

# main functions
def parse_next_token(input: StringInput) -> Token:
    while input.current() == ' ':
        input.next()

    index = input.get_index()

    parse = {
        '+': parse_plus,
        '-': parse_minus,
        '*': parse_star,
        '/': parse_slash,
        '(': parse_lparen,
        ')': parse_rparen
    }.get(input.current(), parse_number)

    try:
        return parse(input)
    except Exception as e:
        while input.current() not in [' ', input.get_end()]:
            input.next()

        return Token(TokenType.ERROR, index, e.args[0])

def parse(string: str) -> List[Token]:
    tokens = []

    input = StringInput(string)
    while input.current() != input.get_end():
        tokens.append(parse_next_token(input))
    tokens.append(Token(TokenType.END, input.get_index()))

    return tokens

def parse_interactive(string: str) -> List[Token]:
    tokens = parse(string)
    errors = [token.value for token in tokens if token.token_type == TokenType.ERROR]

    if errors:
        for error in errors:
            print(error)
    else:
        return tokens
