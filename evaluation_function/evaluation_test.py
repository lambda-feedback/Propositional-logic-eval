import unittest

from .evaluation import Params, evaluation_function

class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_evaluation_default(self):
        response = {"formula": "Hello, World"}
        answer = "Hello, World"  # invalid: answer must be dict
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), False)

    def test_check_tautology(self):
        response = {"formula": "p ∨ ¬p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_check_tautology_fail(self):
        response = {"formula": "p ∧ ¬p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    def test_check_satisfiability(self):
        response = {"formula": "p ∧ q"}
        answer = {"satisfiability": True, "tautology": False, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_check_satisfiability_fail(self):
        response = {"formula": "p ∧ ¬p"}
        answer = {"satisfiability": True, "tautology": False, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    def test_check_equivalence(self):
        response = {"formula": "p ∧ q"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "p ∧ (q ∨ q)", "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_check_equivalence_fail(self):
        response = {"formula": "p ∧ q"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "p", "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    def test_check_equivalence_different_atoms(self):
        """Formulas with same structure but different atom names (e.g. 's' vs 'p') are equivalent up to renaming."""
        response = {"formula": "s"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "p", "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_truth_table_valid(self):
        response = {
            "formula": "p ∧ q",
            "truthTable": {
                "variables": ["p", "q", "p ∧ q"],
                "cells": [
                    ["tt", "tt", "tt"],
                    ["tt", "ff", "ff"],
                    ["ff", "tt", "ff"],
                    ["ff", "ff", "ff"]
                ]
            }
        }
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": True}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_truth_table_invalid(self):
        response = {
            "formula": "p ∧ q",
            "truthTable": {
                "variables": ["p", "q", "p ∧ q"],
                "cells": [
                    ["tt", "tt", "ff"],  # Wrong value
                    ["tt", "ff", "ff"],
                    ["ff", "tt", "ff"],
                    ["ff", "ff", "ff"]
                ]
            }
        }
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": True}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    def test_invalid_response_type(self):
        response = "just a string"  # Invalid type
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))
        self.assertIn("feedback", result)

    def test_missing_formula_field(self):
        response = {"wrongField": "p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    def test_no_params_selected(self):
        response = {"formula": "p"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    def test_multiple_params_selected(self):
        response = {"formula": "p"}
        answer = {"satisfiability": True, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    # --- Equivalence (extra) ---

    def test_equivalence_same_structure_three_atoms(self):
        """Same structure with different atom names: (a ∧ b) ∧ c vs (p ∧ q) ∧ r."""
        response = {"formula": "(a ∧ b) ∧ c"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "(p ∧ q) ∧ r", "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_equivalence_different_number_of_atoms(self):
        """Single atom vs binary: not equivalent (different structure)."""
        response = {"formula": "p"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "p ∧ q", "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))
        self.assertIn("feedback", result)

    def test_equivalence_negation_same_structure(self):
        """¬s vs ¬p: equivalent up to renaming."""
        response = {"formula": "¬s"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "¬p", "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_equivalence_implication_same_structure(self):
        """a → b vs p → q: equivalent up to renaming."""
        response = {"formula": "a → b"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "p → q", "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_equivalence_failure_includes_feedback(self):
        """When equivalence fails, feedback should mention formulas and counterexample."""
        response = {"formula": "p ∨ q"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": "p ∧ q", "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))
        feedback = result.get("feedback_items", result.get("feedback", []))
        feedback_str = str(feedback).lower()
        self.assertTrue("equivalent" in feedback_str or "formula" in feedback_str or "counterexample" in feedback_str)

    # --- Tautology (extra) ---

    def test_tautology_implication_self(self):
        """p → p is a tautology."""
        response = {"formula": "p → p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_tautology_fail_single_atom(self):
        """Single atom p is not a tautology."""
        response = {"formula": "p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_tautology_failure_includes_feedback(self):
        """Tautology failure should include feedback."""
        response = {"formula": "p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))
        self.assertIn("feedback", result)

    # --- Satisfiability (extra) ---

    def test_satisfiability_disjunction(self):
        """p ∨ q is satisfiable."""
        response = {"formula": "p ∨ q"}
        answer = {"satisfiability": True, "tautology": False, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_satisfiability_failure_includes_feedback(self):
        """Unsatisfiable formula should return False and include feedback."""
        response = {"formula": "p ∧ ¬p"}
        answer = {"satisfiability": True, "tautology": False, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))
        self.assertIn("feedback", result)

    # --- Truth table (extra) ---

    def test_truth_table_required_but_missing(self):
        """When answer expects truth table but response has no truthTable, should fail."""
        response = {"formula": "p ∧ q"}
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": True}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_truth_table_single_atom(self):
        """Truth table for single atom p: 2 rows."""
        response = {
            "formula": "p",
            "truthTable": {
                "variables": ["p"],
                "cells": [["tt"], ["ff"]]
            }
        }
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": True}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_truth_table_invalid_cell_token(self):
        """Cell value that is not tt/ff should fail."""
        response = {
            "formula": "p",
            "truthTable": {
                "variables": ["p"],
                "cells": [["tt"], ["invalid"]]
            }
        }
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": True}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_truth_table_missing_combinations(self):
        """Only one row for two atoms should fail (missing combinations)."""
        response = {
            "formula": "p ∧ q",
            "truthTable": {
                "variables": ["p", "q", "p ∧ q"],
                "cells": [["tt", "tt", "tt"]]
            }
        }
        answer = {"satisfiability": False, "tautology": False, "equivalent": None, "validTruthTable": True}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))

    # --- Input / validation (extra) ---

    def test_answer_not_dict(self):
        """Answer must be a dict; string answer gives incorrect."""
        response = {"formula": "p"}
        answer = 42
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_response_as_json_string(self):
        """Response can be a JSON string (parsed before use)."""
        response = '{"formula": "p ∨ ¬p"}'
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_formula_not_string(self):
        """Response formula must be a string."""
        response = {"formula": 123}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_truth_table_mode_with_truth_table_false(self):
        """validTruthTable False means we are not in truth table mode."""
        response = {"formula": "p ∨ ¬p"}
        answer = {"satisfiability": False, "tautology": True, "equivalent": None, "validTruthTable": False}
        params = Params()
        result = evaluation_function(response, answer, params).to_dict()
        self.assertTrue(result.get("is_correct"))

