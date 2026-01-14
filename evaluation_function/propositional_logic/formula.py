from abc import ABC, abstractmethod
from typing import Any


class Formula(ABC):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Atom(Formula):
    def __init__(self, name: str):
        if not name:
            raise ValueError("Atom name cannot be empty")
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Atom):
            return False
        return self._name == other._name

    def __hash__(self) -> int:
        return hash(("Atom", self._name))

    def __repr__(self) -> str:
        return f"Atom('{self._name}')"


class Truth(Formula):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Truth)

    def __hash__(self) -> int:
        return hash("Truth")

    def __repr__(self) -> str:
        return "⊤"


class Falsity(Formula):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Falsity)

    def __hash__(self) -> int:
        return hash("Falsity")

    def __repr__(self) -> str:
        return "⊥"


class UnaryOperator(Formula):
    def __init__(self, operand: Formula):
        if not isinstance(operand, Formula):
            raise TypeError("Operand must be a Formula")
        self._operand = operand

    @property
    def operand(self) -> Formula:
        return self._operand

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._operand == other._operand

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._operand))


class Negation(UnaryOperator):
    def __repr__(self) -> str:
        return f"¬{self._operand}"


class BinaryOperator(Formula):
    def __init__(self, left: Formula, right: Formula):
        if not isinstance(left, Formula):
            raise TypeError("Left operand must be a Formula")
        if not isinstance(right, Formula):
            raise TypeError("Right operand must be a Formula")
        self._left = left
        self._right = right

    @property
    def left(self) -> Formula:
        return self._left

    @property
    def right(self) -> Formula:
        return self._right

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._left == other._left and self._right == other._right

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._left, self._right))

    @abstractmethod
    def _operator_symbol(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"({self._left} {self._operator_symbol()} {self._right})"


class Conjunction(BinaryOperator):
    def _operator_symbol(self) -> str:
        return "∧"


class Disjunction(BinaryOperator):
    def _operator_symbol(self) -> str:
        return "∨"


class Implication(BinaryOperator):
    def _operator_symbol(self) -> str:
        return "→"


class Biconditional(BinaryOperator):
    def _operator_symbol(self) -> str:
        return "↔"
