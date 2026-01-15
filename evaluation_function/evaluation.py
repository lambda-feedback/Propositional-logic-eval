from typing import Any
from lf_toolkit.evaluation import Result, Params

from evaluation_function.propositional_logic.formula import *


def parse_response(response: str) -> tuple[bool, Formula | str]:

    response = response.strip()
    
    # binaryOperators = ["↔","→","∨","∧"]
    # TODO: keep this mapping somewhere else for maintainability
    binaryOperators = {
        "↔" : Biconditional,
        "→" : Implication,
        "∨" : Disjunction,
        "∧" : Conjunction
    }

    for binaryOperator in binaryOperators.keys():

        if binaryOperator in response:
            split_index = response.rindex(binaryOperator)

            left  = response[:split_index]
            right = response[split_index+1:]

            # check left and right not empty strings
            if not left:
                return (False, f"missing text on left of {binaryOperator}")
            elif not right:
                return (False, f"missing text on right of {binaryOperator}")
            
            parse_left = parse_response(left)
            parse_right = parse_response(right)

            error = False
            err_msgs = []

            if not parse_left[0]:
                error = True
                err_msgs.append(parse_left[1])

            if not parse_right[0]:
                error = True
                err_msgs.append(parse_right[1])
            
            if error:
                return (False, err_msgs.join("\n"))
            
            # both sides are find and valid
            result = binaryOperators[binaryOperator](parse_left[1], parse_right[1])
            return (True, result)
    

    # TODO: keep this mapping somewhere else for maintainability
    unaryOperators = {
        "¬" : Negation
    }

    for unaryOperator in unaryOperators.keys():

        #unary operator must syntactically be at the start of the string
        if response[0] == unaryOperator:
            
            right = response[1:]
            #check not empty
            if not right:
                return (False, f"missing text on right of {unaryOperator}")

            parse_right = parse_response(right)
            if not parse_right[0]:
                return parse_right
            
            result = unaryOperators[unaryOperator](parse_right[1])
            return (True, result)
    
    # check if the formual is just True or Falsity
    
    singletons = { # not sure what the official term for these symbols is
        "⊤" : Truth,
        "⊥" : Falsity
    }

    for singleton in singletons:

        if len(response) > 1 and singleton in response:
            return (False, f"not allowed to use {singleton} in the atom identifier")

        elif response == singleton:
            result = singletons[singleton]()
            return (True, result)
    
    # response is likely an atom identifier
    
    return (True, Atom(response))


        
    


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


    if not isinstance(answer, str):
        raise Exception("Answer must be a string/text.")
    

    if not isinstance(response, str):
        return Result(
            is_correct=False,
            feedback="Please enter a string/text."
        )

    
    # this can be "equivilance", "tautology", "satisfiability"
    #potnetially can be switched with classes
    action = params.get("action", None)
    
    feedback   = None
    is_correct = False

    pl_formula = parse_response(response) 

    #swtich on action       

    return Result(is_correct=False)