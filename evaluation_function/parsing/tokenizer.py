from typing import List, Optional
from .character_stream import CharacterStream
from .token_matcher import TokenMatcher, SingleCharTokenMatcher, AtomTokenMatcher, EOFTokenMatcher
from .token import Token, TokenType


class Tokenizer:
    def __init__(self, text: str, matchers: Optional[List[TokenMatcher]] = None):
        self._stream = CharacterStream(text)
        self._matchers: List[TokenMatcher] = matchers or self._create_default_matchers()

    def _create_default_matchers(self) -> List[TokenMatcher]:
        return [
            SingleCharTokenMatcher("⊤", TokenType.TRUTH),
            SingleCharTokenMatcher("⊥", TokenType.FALSITY),
            SingleCharTokenMatcher("¬", TokenType.NEGATION),
            SingleCharTokenMatcher("∧", TokenType.CONJUNCTION),
            SingleCharTokenMatcher("∨", TokenType.DISJUNCTION),
            SingleCharTokenMatcher("→", TokenType.IMPLICATION),
            SingleCharTokenMatcher("↔", TokenType.BICONDITIONAL),
            SingleCharTokenMatcher("⊕", TokenType.XOR),
            SingleCharTokenMatcher("(", TokenType.LEFT_PAREN),
            SingleCharTokenMatcher(")", TokenType.RIGHT_PAREN),
            AtomTokenMatcher(),
            EOFTokenMatcher(),
        ]

    def _skip_whitespace(self):
        while self._stream.current_char is not None and self._stream.current_char.isspace():
            self._stream.advance()

    def next_token(self) -> Token:
        self._skip_whitespace()

        for matcher in self._matchers:
            if matcher.matches(self._stream):
                return matcher.create_token(self._stream)

        char = self._stream.current_char
        position = self._stream.position
        raise ValueError(f"Unexpected character '{char}' at position {position}")
