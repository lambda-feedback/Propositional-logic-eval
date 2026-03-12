from typing import Any
import json
from lf_toolkit.evaluation import Result, Params

from evaluation_function.domain.evaluators import _extract_atoms, EquivalenceEvaluator, SatisfiabilityEvaluator, TautologyEvaluator
from evaluation_function.domain.formula import *

from evaluation_function.parsing.parser import formula_parser
from evaluation_function.parsing.tree_builder_error import BuildError

from evaluation_function.truth_table.evaluate import evaluate_truth_table

_JSON_STRING_NOTE = ("note", "Response was received as a JSON string and was parsed.")


def _feedback_with_json_note(feedback_items: list, response_was_json_string: bool) -> list:
    if not response_was_json_string:
        return feedback_items
    return list(feedback_items) + [_JSON_STRING_NOTE]


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

    response_was_json_string = isinstance(response, str)
    try:
        if response_was_json_string:
            response = json.loads(response)

        if not isinstance(answer, dict):
            return Result(
                is_correct=False,
                feedback_items=_feedback_with_json_note(
                    [("incorrect input", "missing answer object")],
                    response_was_json_string,
                )
            )

        if not isinstance(response, dict):
            return Result(
                is_correct=False,
                feedback_items=_feedback_with_json_note(
                    [("incorrect input", "missing response object")],
                    response_was_json_string,
                )
            )

        response_formula = response.get("formula", None)
        if not isinstance(response_formula, str):
            return Result(
                is_correct=False,
                feedback_items=_feedback_with_json_note(
                    [("incorrect input", "response must be type String")],
                    response_was_json_string,
                )
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
                feedback_items=_feedback_with_json_note(
                    [("invalid param", "please select a param")],
                    response_was_json_string,
                )
            )
        if num_selected > 1:
            return Result(
                is_correct=False,
                feedback_items=_feedback_with_json_note(
                    [("invalid param", "please only select 1 param")],
                    response_was_json_string,
                )
            )

        # Truth table mode: validate response truth table if present
        response_truth_table = response.get("truthTable", None)
        if has_truth_table:
            if response_truth_table is None or not isinstance(response_truth_table, dict):
                return Result(
                    is_correct=False,
                    feedback_items=_feedback_with_json_note(
                        [("incorrect input", "truthTable required when answer expects truth table")],
                        response_was_json_string,
                    )
                )
            variables = response_truth_table.get("variables", [])
            cells = response_truth_table.get("cells", [])

            if not isinstance(variables, list) or not isinstance(cells, list):
                return Result(
                    is_correct=False,
                    feedback_items=_feedback_with_json_note(
                        [("incorrect input", "truthTable must contain 'variables' and 'cells' arrays")],
                        response_was_json_string,
                    )
                )

            num_atoms = len(_extract_atoms(formula))
            truth_table_result = evaluate_truth_table(variables, cells, num_atoms)
            if not truth_table_result.is_correct:
                return Result(
                    is_correct=False,
                    feedback_items=_feedback_with_json_note(
                        getattr(truth_table_result, "feedback_items", []) or [],
                        response_was_json_string,
                    )
                )

        is_correct = False
        feedback = []

        if has_equivalence:
            answer_formula = formula_parser(equivalent)
            ev = EquivalenceEvaluator(formula, answer_formula)
            is_correct, counterex = ev.evaluate_with_counterexample()
            if not is_correct:
                feedback.append((
                    "equivalence",
                    "Your formula is not equivalent to the target."
                ))
                if counterex:
                    if counterex.get("reason"):
                        feedback.append(("counterexample", counterex["reason"]))
                    elif counterex.get("assignment") is not None:
                        # Use plain atom names only (assignment is already name -> bool)
                        asn = ", ".join(f"{k}={counterex['assignment'][k]}" for k in sorted(counterex["assignment"]))
                        feedback.append((
                            "counterexample",
                            f"Under assignment ({asn}) your formula evaluates to {counterex['response_value']}."
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
            return Result(
                is_correct=False,
                feedback_items=_feedback_with_json_note(feedback, response_was_json_string),
            )
        return Result(is_correct=is_correct)

    except Exception as e:
        return Result(
            is_correct=False,
            feedback_items=_feedback_with_json_note([("Error", str(e))], response_was_json_string),
        )