from typing import Any
import json
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


    try:
        if not isinstance(answer, dict):
            return Result(
                is_correct=False,
                feedback_items=[("incorrect input", f"missing answer object. got {answer}")]
            )

        # If response is a string, parse it as JSON
        if isinstance(response, str):
            response = json.loads(response)

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

        formula = formula_parser(response_formula)

        # Answer shape: satisfiability (bool), tautology (bool), equivalent (None|str), validTruthTable (bool)
        satisfiability = answer.get("satisfiability", False) is True
        tautology = answer.get("tautology", False) is True
        equivalent = answer.get("equivalent")
        if equivalent is not None and not isinstance(equivalent, str):
            equivalent = None
        elif equivalent is not None and isinstance(equivalent, str) and equivalent.strip() == "":
            equivalent = None
            
        has_truth_table = answer.get("validTruthTable", False) is True
        has_equivalence = equivalent is not None

        num_selected = sum([satisfiability, tautology, has_equivalence, has_truth_table])

        if num_selected == 0:
            return Result(
                is_correct=False,
                feedback_items=[("invalid param", "please select a param")]
            )
        if num_selected > 1:
            return Result(
                is_correct=False,
                feedback_items=[("invalid param", "please only select 1 param")]
            )

        # Truth table mode: validate response truth table if present
        response_truth_table = response.get("truthTable", None)
        if has_truth_table:
            if response_truth_table is None or not isinstance(response_truth_table, dict):
                return Result(
                    is_correct=False,
                    feedback_items=[("incorrect input", "truthTable required when answer expects truth table")]
                )
            variables = response_truth_table.get("variables", [])
            cells = response_truth_table.get("cells", [])

            if not isinstance(variables, list) or not isinstance(cells, list):
                return Result(
                    is_correct=False,
                    feedback_items=[("incorrect input", "truthTable must contain 'variables' and 'cells' arrays")]
                )

            num_atoms = len(_extract_atoms(formula))
            truth_table_result = evaluate_truth_table(variables, cells, num_atoms)
            if not truth_table_result.is_correct:
                return truth_table_result

        is_correct = False
        feedback = []

        if has_equivalence:
            answer_formula = formula_parser(equivalent)
            ev = EquivalenceEvaluator(formula, answer_formula)
            is_correct, counterex = ev.evaluate_with_counterexample()
            if not is_correct:
                feedback.append((
                    "equivalence",
                    f"Comparing your formula \"{response_formula}\" with expected \"{equivalent}\". They are not equivalent."
                ))
                if counterex:
                    if counterex.get("reason"):
                        feedback.append(("counterexample", counterex["reason"]))
                    elif counterex.get("assignment") is not None:
                        asn = ", ".join(f"{k}={counterex['assignment'][k]}" for k in sorted(counterex["assignment"]))
                        feedback.append((
                            "counterexample",
                            f"Under assignment ({asn}): your formula = {counterex['response_value']}, expected formula = {counterex['expected_value']}."
                        ))
        elif tautology:
            ev = TautologyEvaluator(formula)
            is_correct, counterex = ev.evaluate_with_counterexample()
            if not is_correct:
                feedback.append((
                    "tautology",
                    f"Formula \"{response_formula}\" is not a tautology."
                ))
                if counterex:
                    asn = ", ".join(f"{k}={counterex['assignment'][k]}" for k in sorted(counterex["assignment"]))
                    feedback.append((
                        "counterexample",
                        f"Under assignment ({asn}) the formula evaluates to False."
                    ))
        elif satisfiability:
            is_correct = SatisfiabilityEvaluator(formula).evaluate()
            if not is_correct:
                feedback.append((
                    "satisfiability",
                    f"Formula \"{response_formula}\" is not satisfiable: no assignment of the atoms makes it true."
                ))
        elif has_truth_table:
            is_correct = True  # already validated above

        if feedback:
            return Result(is_correct=False, feedback_items=feedback)
        return Result(is_correct=is_correct)

    except Exception as e:
        return Result(
            is_correct=False,
            feedback_items=[("Error", str(e))]
        )