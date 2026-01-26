import unittest

from .preview import Params, preview_function

class TestPreviewFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practice to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use preview_function() to check your algorithm works
    as it should.
    """

    def test_preview(self):
        response, params = "A", Params()
        result = preview_function(response, params)

        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])
    
    def test_successful_and(self):
        response, params = "P ∧ Q", Params()
        result = preview_function(response, params)
        self.assertEqual(response, result.get("preview").get("latex"))
        self.assertEqual(response, result.get("preview").get("sympy"))
    
    def test_successful_or(self):
        response, params = "P ∨ Q", Params()
        result = preview_function(response, params)
        self.assertEqual(response, result.get("preview").get("latex"))
        self.assertEqual(response, result.get("preview").get("sympy"))
    
    def test_successful_not(self):
        response, params = "¬P", Params()
        result = preview_function(response, params)
        self.assertEqual(response, result.get("preview").get("latex"))
        self.assertEqual(response, result.get("preview").get("sympy"))
    
    def test_successful_implies(self):
        response, params = "P → Q", Params()
        result = preview_function(response, params)
        self.assertEqual(response, result.get("preview").get("latex"))
        self.assertEqual(response, result.get("preview").get("sympy"))
    
    def test_successful_biconditional(self):
        response, params = "P ↔ Q", Params()
        result = preview_function(response, params)
        self.assertEqual(response, result.get("preview").get("latex"))
        self.assertEqual(response, result.get("preview").get("sympy"))
    
    def test_complex_expression(self):
        response, params = "(P ∧ Q) → (R ∨ S)", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])
    
    def test_nested_negation(self):
        response, params = "¬(¬P)", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])
    
    def test_multiple_operators(self):
        response, params = "P ∧ Q ∧ R", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])
    
    def test_parentheses(self):
        response, params = "(P ∧ Q) ∨ (R ∧ S)", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])
    
    def test_empty_string(self):
        response, params = "", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
    
    def test_invalid_syntax(self):
        response, params = "P ∧∧ Q", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
    
    def test_single_variable(self):
        response, params = "X", Params()
        result = preview_function(response, params)
        self.assertEqual(response, result.get("preview").get("latex"))
        self.assertEqual(response, result.get("preview").get("sympy"))
    
    def test_multi_character_variable(self):
        response, params = "P1 ∧ Q2", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])
    
    def test_de_morgans_law_expression(self):
        response, params = "¬(P ∧ Q) ↔ (¬P ∨ ¬Q)", Params()
        result = preview_function(response, params)
        self.assertIn("preview", result)
        self.assertIsNotNone(result["preview"])


