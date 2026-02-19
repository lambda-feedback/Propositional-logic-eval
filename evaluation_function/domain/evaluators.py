from itertools import product, permutations
from typing import Mapping, Set
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


def _extract_atoms(formula: Formula) -> Set[Atom]:
    atoms = set()
    
    if isinstance(formula, Atom):
        atoms.add(formula)
    elif isinstance(formula, (Truth, Falsity)):
        pass
    elif isinstance(formula, Negation):
        atoms.update(_extract_atoms(formula.operand))
    elif isinstance(formula, (Conjunction, Disjunction, Implication, Biconditional)):
        atoms.update(_extract_atoms(formula.left))
        atoms.update(_extract_atoms(formula.right))
    
    return atoms


class EquivalenceEvaluator:
    """Checks if two formulas are equivalent up to renaming of atoms (so e.g. 's' and 'p' are equivalent)."""

    def __init__(self, formula1: Formula, formula2: Formula):
        self._formula1 = formula1
        self._formula2 = formula2

    def evaluate(self) -> bool:
        ok, _ = self.evaluate_with_counterexample()
        return ok

    def evaluate_with_counterexample(self) -> tuple[bool, dict | None]:
        """Returns (are_equivalent, counterexample_or_none). Equivalent = same truth behaviour under some renaming of atoms."""
        atoms1 = sorted(_extract_atoms(self._formula1), key=lambda a: a.name)
        atoms2 = sorted(_extract_atoms(self._formula2), key=lambda a: a.name)

        if len(atoms1) != len(atoms2):
            return False, {
                "assignment": {},
                "response_value": None,
                "expected_value": None,
                "reason": f"different number of atoms: {len(atoms1)} vs {len(atoms2)}",
            }

        n = len(atoms1)
        first_counterexample = None
        for perm in permutations(range(n)):
            # perm[j] = index in atoms2 that atoms1[j] is renamed to; so atoms1[j] gets value of atoms2[perm[j]]
            for assignment_values in product([False, True], repeat=n):
                assignment2_dict = {atoms2[i]: assignment_values[i] for i in range(n)}
                assignment1_dict = {atoms1[j]: assignment_values[perm[j]] for j in range(n)}
                a1 = Assignment(assignment1_dict)
                a2 = Assignment(assignment2_dict)
                v1 = FormulaEvaluator(self._formula1, a1).evaluate()
                v2 = FormulaEvaluator(self._formula2, a2).evaluate()
                if v1 != v2:
                    if first_counterexample is None:
                        first_counterexample = {
                            "assignment": {atoms2[i].name: assignment_values[i] for i in range(n)},
                            "response_value": v1,
                            "expected_value": v2,
                        }
                    break
            else:
                return True, None

        return False, first_counterexample


class SatisfiabilityEvaluator:
    def __init__(self, formula: Formula):
        self._formula = formula

    def evaluate(self) -> bool:
        atoms = _extract_atoms(self._formula)
        all_atoms = list(atoms)
        
        for assignment_values in product([False, True], repeat=len(all_atoms)):
            assignment_dict = {atom: val for atom, val in zip(all_atoms, assignment_values)}
            assignment = Assignment(assignment_dict)
            
            evaluator = FormulaEvaluator(self._formula, assignment)
            if evaluator.evaluate():
                return True
        
        return False


class TautologyEvaluator:
    def __init__(self, formula: Formula):
        self._formula = formula

    def evaluate(self) -> bool:
        ok, _ = self.evaluate_with_counterexample()
        return ok

    def evaluate_with_counterexample(self) -> tuple[bool, dict | None]:
        """Returns (is_tautology, counterexample_or_none). Counterexample has assignment and formula_value."""
        atoms = _extract_atoms(self._formula)
        all_atoms = list(atoms)

        for assignment_values in product([False, True], repeat=len(all_atoms)):
            assignment_dict = {atom: val for atom, val in zip(all_atoms, assignment_values)}
            assignment = Assignment(assignment_dict)

            evaluator = FormulaEvaluator(self._formula, assignment)
            val = evaluator.evaluate()
            if not val:
                assignment_str = {atom.name: v for atom, v in assignment_dict.items()}
                return False, {"assignment": assignment_str, "formula_value": val}
        return True, None
