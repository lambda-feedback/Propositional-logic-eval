
from evaluation_function.domain.formula import *
from evaluation_function.parsing.tokenizer import *
from evaluation_function.parsing.tree_builder import *

def formula_parser(input: str) -> Formula:

    # tokenize input
    tokenizer = Tokenizer(input)
    tokens = []

    token = Token()
    while token.type != TokenType.EOF:
        token = tokenizer.next_token()
        tokens.append(token)
    
    # parse tokens into Formula
    builder = TreeBuilder(tokens)
    formula = builder.build()

    return formula