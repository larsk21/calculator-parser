from abc import ABC, abstractmethod
from typing import List

from calculator.token import Token, TokenType

class Input(ABC):

    def __init__(self):
        self._index = 0

    def get_index(self) -> int:
        return self._index

    @abstractmethod
    def next(self):
        self._index += 1

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def get_end(self):
        pass

    @abstractmethod
    def get_record(self):
        pass

    @abstractmethod
    def clear_record(self):
        pass

class StringInput(Input):

    def __init__(self, content: str):
        super().__init__()

        self._content = content
        self._record = ''

    def current(self) -> str:
        if self.get_index() < len(self._content):
            return self._content[self.get_index()]
        else:
            return self.get_end()

    def next(self):
        self._record += self.current()

        super().next()

    def get_end(self) -> str:
        return '\0'

    def get_record(self) -> str:
        return self._record

    def clear_record(self):
        self._record = ''

class TokenInput(Input):

    def __init__(self, content: List[Token]):
        super().__init__()

        self._content = content
        self._record = []

    def current(self) -> Token:
        if self.get_index() < len(self._content):
            return self._content[self.get_index()]
        else:
            return self.get_end()

    def next(self):
        self._record.append(self.current())

        super().next()

    def get_end(self) -> Token:
        return self._content[-1]

    def get_record(self) -> List[Token]:
        return self._record

    def clear_record(self):
        self._record = []
