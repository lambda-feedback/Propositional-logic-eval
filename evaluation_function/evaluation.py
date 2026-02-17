from typing import Any
from lf_toolkit.evaluation import Result, Params

from evaluation_function.domain.evaluators import _extract_atoms, EquivalenceEvaluator, SatisfiabilityEvaluator, TautologyEvaluator
from evaluation_function.domain.formula import *

from evaluation_function.parsing.parser import formula_parser
from evaluation_function.parsing.tree_builder_error import BuildError

from evaluation_function.truth_table.evaluate import evaluate_truth_table


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
        return Result(
            is_correct=False,
            feedback_items=[("incorrect input", "missing answer object")]
        )

    if not isinstance(response, dict):
        return Result(
            is_correct=False,
            feedback_items=[("incorrect input", "missing response object")]
        )

        
    response_formula = response.get("formula", None)
    if not isinstance(response_formula, str):
        return Result(
            is_correct=False,
            feedback_items=[("incorrect input", "response must be type String")]
        )

    # parse response_formula into Formula
    try:
        formula = formula_parser(response_formula)
    
    except BuildError as e:
        return Result(
            is_correct=False,
            feedback_items=[(BuildError, str(e))]
        )
    except ValueError as e:
        return Result(
            is_correct=False,
            feedback_items=[(ValueError, str(e))]
        )



    # check if input is a truth table
    truth_table = response.get("truthTable", None)
    if truth_table is not None and isinstance(truth_table, dict):

        variables = truth_table.get("variables", [])
        cells = truth_table.get("cells", [])
        
        if not isinstance(variables, list) or not isinstance(cells, list):
            return Result(
                is_correct=False,
                feedback_items=[("incorrect input", "truthTable must contain 'variables' and 'cells' arrays")]
            )

        # tokenise answer 
        try:
            answer_formula = formula_parser(answer)
        
        except BuildError as e:
            return Result(
                is_correct=False,
                feedback_items=[("BuildError", str(e))]
            )
        except ValueError as e:
            return Result(
                is_correct=False,
                feedback_items=[("ValueError", str(e))]
            )

        num_atoms = len(_extract_atoms(answer_formula))
        
        # Evaluate the truth table
        truth_table_result = evaluate_truth_table(variables, cells, num_atoms)
        if not truth_table_result.is_correct:
            return truth_table_result


    
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


    if equivalence:

        # tokenise answer 
        try:
            answer_formula = formula_parser(answer)
        
        except BuildError as e:
            return Result(
                is_correct=False,
                feedback_items=[(BuildError, str(e))]
            )
        except ValueError as e:
            return Result(
                is_correct=False,
                feedback_items=[(ValueError, str(e))]
            )
        
        is_correct = EquivalenceEvaluator(formula, answer_formula).evaluate()
        

    elif tautology:
        is_correct = TautologyEvaluator(formula).evaluate()
    elif satisfiability:
        is_correct = SatisfiabilityEvaluator(formula).evaluate()

    return Result(is_correct=is_correct)