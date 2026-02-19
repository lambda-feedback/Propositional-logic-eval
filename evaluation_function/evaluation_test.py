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
        answer = {"satisability": False, "tautology": True, "equivalent": None, "truthTable": None}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_check_tautology_fail(self):
        response = {"formula": "p ∧ ¬p"}
        answer = {"satisability": False, "tautology": True, "equivalent": None, "truthTable": None}
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
        answer = {"satisability": False, "tautology": True, "equivalent": None, "truthTable": None}
        params = Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))
        self.assertIn("feedback", result)

    def test_missing_formula_field(self):
        response = {"wrongField": "p"}
        answer = {"satisability": False, "tautology": True, "equivalent": None, "truthTable": None}
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

