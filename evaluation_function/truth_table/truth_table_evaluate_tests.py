import unittest
from evaluation_function.truth_table.evaluate import evaluate_truth_table


class TestEvaluateTruthTable(unittest.TestCase):

    def test_empty_input(self):
        """Test that empty input returns False with appropriate error"""
        result = evaluate_truth_table([], 0)
        self.assertFalse(result.is_correct)
        # self.assertEqual(len(result.feedback_items), 1)
        # self.assertIn("no input", str(result.feedback_items[0][1]))

    def test_only_header_row(self):
        """Test that providing only formulas without values returns False"""
        result = evaluate_truth_table([["p"]], 1)
        self.assertFalse(result.is_correct)
        # self.assertIn("Must provide names and its truth values", str(result.feedback_items[0][1]))

    def test_simple_valid_truth_table_one_atom(self):
        """Test a valid truth table with one atom"""
        input_table = [
            ["p"],
            ["tt"],
            ["ff"]
        ]
        result = evaluate_truth_table(input_table, 1)
        self.assertTrue(result.is_correct)

    def test_valid_truth_table_two_atoms(self):
        """Test a valid truth table with two atoms and a compound formula"""
        input_table = [
            ["p", "q", "p ∧ q"],
            ["tt", "tt", "tt"],
            ["tt", "ff", "ff"],
            ["ff", "tt", "ff"],
            ["ff", "ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertTrue(result.is_correct)

    def test_valid_truth_table_with_or(self):
        """Test a valid truth table with OR operation"""
        input_table = [
            ["p", "q", "p ∨ q"],
            ["tt", "tt", "tt"],
            ["tt", "ff", "tt"],
            ["ff", "tt", "tt"],
            ["ff", "ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertTrue(result.is_correct)

    def test_valid_truth_table_with_implication(self):
        """Test a valid truth table with implication"""
        input_table = [
            ["p", "q", "p → q"],
            ["tt", "tt", "tt"],
            ["tt", "ff", "ff"],
            ["ff", "tt", "tt"],
            ["ff", "ff", "tt"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertTrue(result.is_correct)

    def test_valid_truth_table_with_negation(self):
        """Test a valid truth table with negation"""
        input_table = [
            ["p", "¬p"],
            ["tt", "ff"],
            ["ff", "tt"]
        ]
        result = evaluate_truth_table(input_table, 1)
        self.assertTrue(result.is_correct)

    def test_invalid_formula_syntax(self):
        """Test that invalid formula syntax is caught"""
        input_table = [
            ["p", "q ∧"],
            ["tt", "tt"],
            ["ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertFalse(result.is_correct)
        # self.assertIn("formula in column 2 incorrect", str(result.feedback_items[0][1]))

    def test_undefined_atom_in_formula(self):
        """Test that using an undefined atom in a formula is caught"""
        input_table = [
            ["p", "p ∧ q"],
            ["tt", "tt"],
            ["ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertFalse(result.is_correct)
        # self.assertIn("undefined", str(result.feedback_items[0][1]))

    def test_invalid_cell_value(self):
        """Test that invalid cell values are caught"""
        input_table = [
            ["p"],
            ["true"],
            ["ff"]
        ]
        result = evaluate_truth_table(input_table, 1)
        self.assertFalse(result.is_correct)
        # self.assertIn("invalid", str(result.feedback_items[0][1]))

    def test_missing_combinations(self):
        """Test that missing combinations are detected"""
        input_table = [
            ["p", "q"],
            ["tt", "tt"],
            ["tt", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertFalse(result.is_correct)
        # self.assertIn("missing combinations", str(result.feedback_items[0][1]))

    def test_excessive_combinations(self):
        """Test that excessive combinations are detected"""
        input_table = [
            ["p", "q"],
            ["tt", "tt"],
            ["tt", "ff"],
            ["ff", "tt"],
            ["ff", "ff"],
            ["tt", "tt"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertFalse(result.is_correct)
        # self.assertIn("excessive combinations", str(result.feedback_items[0][1]))

    def test_duplicate_assignments(self):
        """Test that duplicate assignments are detected"""
        input_table = [
            ["p", "q"],
            ["tt", "tt"],
            ["tt", "ff"],
            ["tt", "tt"],
            ["ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertFalse(result.is_correct)
        # self.assertIn("duplicated assignment", str(result.feedback_items[0][1]))

    def test_incorrect_cell_evaluation(self):
        """Test that incorrect cell values are detected"""
        input_table = [
            ["p", "q", "p ∧ q"],
            ["tt", "tt", "ff"],  # Should be tt
            ["tt", "ff", "ff"],
            ["ff", "tt", "ff"],
            ["ff", "ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertFalse(result.is_correct)
        # self.assertIn("incorrect cell value", str(result.feedback_items[0][1]))

    def test_wrong_number_of_atoms(self):
        """Test when num_atoms doesn't match the actual atoms in table"""
        input_table = [
            ["p", "q"],
            ["tt", "tt"],
            ["tt", "ff"],
            ["ff", "tt"],
            ["ff", "ff"]
        ]
        result = evaluate_truth_table(input_table, 3)
        self.assertFalse(result.is_correct)

    def test_complex_formula(self):
        """Test a valid truth table with a complex formula"""
        input_table = [
            ["p", "q", "(p → q) ∧ (q → p)"],
            ["tt", "tt", "tt"],
            ["tt", "ff", "ff"],
            ["ff", "tt", "ff"],
            ["ff", "ff", "tt"]
        ]
        result = evaluate_truth_table(input_table, 2)
        self.assertTrue(result.is_correct)


if __name__ == '__main__':
    unittest.main()
