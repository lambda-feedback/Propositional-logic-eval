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
        response, answer, params = "Hello, World", "Hello, World", Params()

        result = evaluation_function(response, answer, params).to_dict()

        self.assertEqual(result.get("is_correct"), False)
        self.assertFalse(len(result.get("feedback", [])) == 0)

    def test_check_tautology(self):
        
        response, answer, params = "p ∨ ¬p", "", {"tautology": True}

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))

    def test_check_tautology_fail(self):
        
        response, answer, params = "p ∧ ¬p", "", {"tautology": True}

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    
    def test_check_satisfiability(self):
        
        response, answer, params = "p ∧ q", "", {"satisfiability": True}

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))
    
    def test_check_satisfiability_fail(self):
        
        response, answer, params = "p ∧ ¬p", "", {"satisfiability": True}

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))

    
    def test_check_equivalence(self):
        
        response, answer, params = "p ∧ q", "p ∧ (q ∨ q)", {"equivalence": True}

        result = evaluation_function(response, answer, params).to_dict()

        self.assertTrue(result.get("is_correct"))
    
    def test_check_equivalence_fail(self):
        
        response, answer, params = "p ∧ q", "p", {"equivalence": True}

        result = evaluation_function(response, answer, params).to_dict()

        self.assertFalse(result.get("is_correct"))
    
