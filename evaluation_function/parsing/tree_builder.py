from typing import List, Optional
from ..domain.formula import Formula
from .token import Token, TokenType
from .token_stream import TokenStream
from .expression_builder import ExpressionBuilder
from .primary_builder import PrimaryBuilder
from .binary_operator_builder import BinaryOperatorBuilder
from .tree_builder_error import BuildError

class TreeBuilder:
    def __init__(self, tokens: List[Token], expression_builder: Optional[ExpressionBuilder] = None):
        self._stream = TokenStream(tokens)
        if expression_builder is None:
            self._expression_builder = self._create_default_builder()
        else:
            self._expression_builder = expression_builder

    def _create_default_builder(self) -> ExpressionBuilder:
        binary_builder = BinaryOperatorBuilder(None)
        primary_builder = PrimaryBuilder(binary_builder)
        binary_builder._primary_builder = primary_builder
        return binary_builder

    def build(self) -> Formula:
        if self._stream.is_eof():
            raise BuildError("Empty input", 0)

        formula = self._expression_builder.build(self._stream)

        if not self._stream.is_eof():
            token = self._stream.current_token
            if token is not None and token.type != TokenType.EOF:
                raise BuildError(
                    f"Unexpected token {token.type.name} after expression",
                    token.position
                )

        return formula
