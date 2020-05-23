from abc import ABC, abstractmethod

class Expression(ABC):

    @abstractmethod
    def get_value(self) -> float:
        pass

class Value(Expression):

    def __init__(self, value: float):
        self.value = value

    def get_value(self):
        return self.value

class Operation(Expression):

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

class AddOperation(Operation):

    def get_value(self):
        return self.left.get_value() + self.right.get_value()

class SubtractOperation(Operation):

    def get_value(self):
        return self.left.get_value() - self.right.get_value()

class MultiplyOperation(Operation):

    def get_value(self):
        return self.left.get_value() * self.right.get_value()

class DivideOperation(Operation):

    def get_value(self):
        return self.left.get_value() / self.right.get_value()

class UnknownOperation(Operation):

    def get_value(self):
        raise Exception("unknown operation")
