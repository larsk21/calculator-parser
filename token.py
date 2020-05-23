from enum import Enum

class TokenType(Enum):
    ERROR = 0
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    LPAREN = 5
    RPAREN = 6
    NUMBER = 7
    END = 127

class Token:
    def __init__(self, token_type: TokenType, pos: int, value=None):
        self.token_type = token_type
        self.pos = pos
        self.value = value

    def numeric_value(self) -> float:
        value = self.value

        if value[-1] in ['f', 'F', 'l', 'L']:
            value = value[0:-1]

        return float(value)

    def __str__(self):
        if self.value is None:
            return '<' + self.token_type.name.lower() + '>'
        else:
            return '<' + self.token_type.name.lower() + ': ' + str(self.value) + '>'
