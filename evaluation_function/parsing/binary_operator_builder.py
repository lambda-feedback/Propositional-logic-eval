from typing import Dict, Callable
from ..domain.formula import Formula, Conjunction, Disjunction, Implication, Biconditional, Xor
from .token_stream import TokenStream
from .token import TokenType
from .expression_builder import ExpressionBuilder


class BinaryOperatorBuilder(ExpressionBuilder):
    _PRECEDENCE: Dict[TokenType, int] = {
        TokenType.BICONDITIONAL: 1,
        TokenType.IMPLICATION: 2,
        TokenType.XOR: 3,
        TokenType.DISJUNCTION: 4,
        TokenType.CONJUNCTION: 5,
    }

    _OPERATOR_CONSTRUCTORS: Dict[TokenType, Callable[[Formula, Formula], Formula]] = {
        TokenType.CONJUNCTION: Conjunction,
        TokenType.DISJUNCTION: Disjunction,
        TokenType.IMPLICATION: Implication,
        TokenType.BICONDITIONAL: Biconditional,
        TokenType.XOR: Xor,
    }

    _RIGHT_ASSOCIATIVE: set = {TokenType.IMPLICATION}

    def __init__(self, primary_builder: ExpressionBuilder):
        self._primary_builder = primary_builder

    def build(self, stream: TokenStream) -> Formula:
        return self._build_binary_operator(stream, 1)

    def _build_binary_operator(self, stream: TokenStream, min_precedence: int) -> Formula:
        left = self._primary_builder.build(stream)

        while not stream.is_eof():
            token = stream.current_token
            if token is None:
                break

            if token.type == TokenType.RIGHT_PAREN:
                break

            if token.type not in self._PRECEDENCE:
                break

            op_precedence = self._PRECEDENCE[token.type]
            if op_precedence < min_precedence:
                break

            stream.advance()

            if token.type in self._RIGHT_ASSOCIATIVE:
                right = self._build_binary_operator(stream, op_precedence)
            else:
                right = self._build_binary_operator(stream, op_precedence + 1)

            constructor = self._OPERATOR_CONSTRUCTORS[token.type]
            left = constructor(left, right)

        return left
