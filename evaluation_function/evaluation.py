from typing import Any
from lf_toolkit.evaluation import Result, Params

from evaluation_function.domain.evaluators import *
from evaluation_function.domain.formula import *
from evaluation_function.parsing.tokenizer import *
from evaluation_function.parsing.tree_builder import *


def evaluation_function(
    response: Any,
    answer: Any,
    params: Params,
) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """


    # if not isinstance(answer, str):
    #     raise Exception("Answer must be a string/text.")
    

    if not isinstance(response, str):
        return Result(
            is_correct=False,
            feedback_items=[("incorrect input", "resposne must be type String")]
        )

    
    # check only one of "equivilance", "tautology", "satisfiability" is selected
    
    equivalence = params.get("equivalence", False)
    tautology = params.get("tautology", False)
    satisfiability = params.get("satisfiability", False)


    #check that 1 and only 1 param is selected
    num_selected = sum([equivalence, tautology, satisfiability])

    if num_selected == 0:
        return Result(
            is_correct=False,
            feedback_items=[("invalid param", "please select a param")]
        )
    elif num_selected > 1:
        return Result(
            is_correct=False,
            feedback_items=[("invalid param", "please only select 1 param")]
        )


    
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
        return Result(
            is_correct=False,
            feedback_items=[(ValueError, str(e))]
        )


    # parse tokens into Formula
    try:
        builder = TreeBuilder(tokens)
        formula = builder.build()
    
    except BuildError as e:
        return Result(
            is_correct=False,
            feedback_items=[(BuildError, str(e))]
        )


    if equivalence:
        
        answer_tokenizer = Tokenizer(answer)
        answer_tokens = []

        # tokenise answer 
        try:
            while True:
                answer_token = answer_tokenizer.next_token()
                answer_tokens.append(answer_token)
                if answer_token.type == TokenType.EOF:
                    break
        
        except ValueError as e:
            return Result(
                is_correct=False,
                feedback_items=[(ValueError, str(e))]
            )
        
        # parse answer tokens into Formula
        try:
            answer_builder = TreeBuilder(answer_tokens)
            answer_formula = answer_builder.build()
        
        except BuildError as e:
            return Result(
                is_correct=False,
                feedback_items=[(BuildError, str(e))]
            )
        
        is_correct = EquivalenceEvaluator(formula, answer_formula).evaluate()
        

    elif tautology:
        is_correct = TautologyEvaluator(formula).evaluate()
    elif satisfiability:
        is_correct = SatisfiabilityEvaluator(formula).evaluate()

    return Result(is_correct=is_correct)