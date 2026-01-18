from typing import Any
from lf_toolkit.evaluation import Result, Params

from evaluation_function.domain.evaluators import *
from evaluation_function.domain.formula import *
from evaluation_function.parsing.tokenizer import *
from evaluation_function.parsing.tree_builder import *


# def parse_response(response: str) -> tuple[bool, Formula | str]:

#     response = response.strip()
    
#     # binaryOperators = ["↔","→","∨","∧"]
#     # TODO: keep this mapping somewhere else for maintainability
#     binaryOperators = {
#         "↔" : Biconditional,
#         "→" : Implication,
#         "∨" : Disjunction,
#         "∧" : Conjunction
#     }

#     for binaryOperator in binaryOperators.keys():

#         if binaryOperator in response:
#             split_index = response.rindex(binaryOperator)

#             left  = response[:split_index]
#             right = response[split_index+1:]

#             # check left and right not empty strings
#             if not left:
#                 return (False, f"missing text on left of {binaryOperator}")
#             elif not right:
#                 return (False, f"missing text on right of {binaryOperator}")
            
#             parse_left = parse_response(left)
#             parse_right = parse_response(right)

#             error = False
#             err_msgs = []

#             if not parse_left[0]:
#                 error = True
#                 err_msgs.append(parse_left[1])

#             if not parse_right[0]:
#                 error = True
#                 err_msgs.append(parse_right[1])
            
#             if error:
#                 return (False, err_msgs.join("\n"))
            
#             # both sides are find and valid
#             result = binaryOperators[binaryOperator](parse_left[1], parse_right[1])
#             return (True, result)
    

#     # TODO: keep this mapping somewhere else for maintainability
#     unaryOperators = {
#         "¬" : Negation
#     }

#     for unaryOperator in unaryOperators.keys():

#         #unary operator must syntactically be at the start of the string
#         if response[0] == unaryOperator:
            
#             right = response[1:]
#             #check not empty
#             if not right:
#                 return (False, f"missing text on right of {unaryOperator}")

#             parse_right = parse_response(right)
#             if not parse_right[0]:
#                 return parse_right
            
#             result = unaryOperators[unaryOperator](parse_right[1])
#             return (True, result)
    
#     # check if the formual is just True or Falsity
    
#     singletons = { # not sure what the official term for these symbols is
#         "⊤" : Truth,
#         "⊥" : Falsity
#     }

#     for singleton in singletons:

#         if len(response) > 1 and singleton in response:
#             return (False, f"not allowed to use {singleton} in the atom identifier")

#         elif response == singleton:
#             result = singletons[singleton]()
#             return (True, result)
    
#     # response is likely an atom identifier
    
#     return (True, Atom(response))


        
    


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
    if not (equivalence ^ tautology ^ satisfiability):

        if not (equivalence or tautology or satisfiability):
            #no params selected
            return Result(
                is_correct=False,
                feedback_items=[("invalid param", "please select a param")]
            )
        
        # more than one param selected
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