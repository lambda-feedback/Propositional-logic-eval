from enum import Enum


class TokenType(Enum):
    ATOM = "ATOM"
    TRUTH = "TRUTH"
    FALSITY = "FALSITY"
    NEGATION = "NEGATION"
    CONJUNCTION = "CONJUNCTION"
    DISJUNCTION = "DISJUNCTION"
    IMPLICATION = "IMPLICATION"
    BICONDITIONAL = "BICONDITIONAL"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    EOF = "EOF"


class Token:
    def __init__(self, token_type: TokenType = None, value: str = "", position: int = -1):
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', {self.position})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value
