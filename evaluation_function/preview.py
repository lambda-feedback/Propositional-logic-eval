from typing import Any
from lf_toolkit.preview import Result, Params, Preview

from evaluation_function.domain.evaluators import *
from evaluation_function.domain.formula import *
from evaluation_function.parsing.tokenizer import *
from evaluation_function.parsing.tree_builder import *

def preview_function(response: Any, params: Params) -> Result:
    """
    Function used to preview a student response.
    ---
    The handler function passes three arguments to preview_function():

    - `response` which are the answers provided by the student.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you.
    """
    
    feedback   = None
    is_correct = False

    # tokenize response
    tokenizer = Tokenizer(response)
    tokens = []

    try:
        while True:
            token = tokenizer.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
    
    except ValueError as e:
        return Result(preview=Preview(feedback = str(e)))


    # parse tokens into Formula
    try:
        builder = TreeBuilder(tokens)
        formula = builder.build()
    
    except BuildError as e:
        return Result(preview=Preview(feedback = str(e)))

    return Result(preview=Preview(latex=response))
