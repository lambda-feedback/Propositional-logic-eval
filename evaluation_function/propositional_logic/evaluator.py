from typing import Mapping
from .formula import (
    Formula,
    Atom,
    Truth,
    Falsity,
    Negation,
    Conjunction,
    Disjunction,
    Implication,
    Biconditional,
)


class Assignment:
    def __init__(self, assignment: Mapping[Atom, bool]):
        self._assignment = dict(assignment)

    def get(self, atom: Atom) -> bool:
        if atom not in self._assignment:
            raise ValueError(f"Atom {atom.name} not found in assignment")
        return self._assignment[atom]

    def __contains__(self, atom: Atom) -> bool:
        return atom in self._assignment


class FormulaEvaluator:
    def __init__(self, formula: Formula, assignment: Assignment):
        self._formula = formula
        self._assignment = assignment

    def evaluate(self) -> bool:
        return self._evaluate_formula(self._formula)

    def _evaluate_formula(self, formula: Formula) -> bool:
        if isinstance(formula, Atom):
            return self._assignment.get(formula)
        if isinstance(formula, Truth):
            return True
        if isinstance(formula, Falsity):
            return False
        if isinstance(formula, Negation):
            return not self._evaluate_formula(formula.operand)
        if isinstance(formula, Conjunction):
            return self._evaluate_formula(formula.left) and self._evaluate_formula(formula.right)
        if isinstance(formula, Disjunction):
            return self._evaluate_formula(formula.left) or self._evaluate_formula(formula.right)
        if isinstance(formula, Implication):
            return not self._evaluate_formula(formula.left) or self._evaluate_formula(formula.right)
        if isinstance(formula, Biconditional):
            return self._evaluate_formula(formula.left) == self._evaluate_formula(formula.right)
        raise TypeError(f"Unknown formula type: {type(formula)}")
