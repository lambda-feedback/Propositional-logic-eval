from itertools import product
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
    def __init__(self, formula1: Formula, formula2: Formula):
        self._formula1 = formula1
        self._formula2 = formula2

    def evaluate(self) -> bool:
        atoms1 = _extract_atoms(self._formula1)
        atoms2 = _extract_atoms(self._formula2)
        all_atoms = list(atoms1 | atoms2)
        
        for assignment_values in product([False, True], repeat=len(all_atoms)):
            assignment_dict = {atom: val for atom, val in zip(all_atoms, assignment_values)}
            assignment = Assignment(assignment_dict)
            
            evaluator1 = FormulaEvaluator(self._formula1, assignment)
            evaluator2 = FormulaEvaluator(self._formula2, assignment)
            
            if evaluator1.evaluate() != evaluator2.evaluate():
                return False
        
        return True


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
        atoms = _extract_atoms(self._formula)
        all_atoms = list(atoms)
        
        for assignment_values in product([False, True], repeat=len(all_atoms)):
            assignment_dict = {atom: val for atom, val in zip(all_atoms, assignment_values)}
            assignment = Assignment(assignment_dict)
            
            evaluator = FormulaEvaluator(self._formula, assignment)
            if not evaluator.evaluate():
                return False
        
        return True
