from itertools import product
from evaluation_function.propositional_logic import (
    Atom,
    Negation,
    Conjunction,
    Disjunction,
    Implication,
    Biconditional,
    Assignment,
    FormulaEvaluator,
)


def get_atoms(formula):
    atoms = set()
    
    if isinstance(formula, Atom):
        atoms.add(formula)
    elif hasattr(formula, "operand"):
        atoms.update(get_atoms(formula.operand))
    elif hasattr(formula, "left") and hasattr(formula, "right"):
        atoms.update(get_atoms(formula.left))
        atoms.update(get_atoms(formula.right))
    elif hasattr(formula, "formula"):
        atoms.update(get_atoms(formula.formula))
    
    return atoms


def are_equivalent(formula1, formula2):
    atoms1 = get_atoms(formula1)
    atoms2 = get_atoms(formula2)
    all_atoms = list(atoms1 | atoms2)
    
    for assignment_values in product([False, True], repeat=len(all_atoms)):
        assignment_dict = {atom: val for atom, val in zip(all_atoms, assignment_values)}
        assignment = Assignment(assignment_dict)
        
        evaluator1 = FormulaEvaluator(formula1, assignment)
        evaluator2 = FormulaEvaluator(formula2, assignment)
        
        result1 = evaluator1.evaluate()
        result2 = evaluator2.evaluate()
        
        if result1 != result2:
            return False
    
    return True


def main():
    p = Atom("p")
    q = Atom("q")
    
    print("=== Formula Equivalence Checking ===")
    print()
    
    equivalence_tests = [
        (
            "p → q",
            "¬p ∨ q",
            Implication(p, q),
            Disjunction(Negation(p), q)
        ),
        (
            "p ↔ q",
            "(p → q) ∧ (q → p)",
            Biconditional(p, q),
            Conjunction(Implication(p, q), Implication(q, p))
        ),
        (
            "¬(p ∧ q)",
            "¬p ∨ ¬q",
            Negation(Conjunction(p, q)),
            Disjunction(Negation(p), Negation(q))
        ),
        (
            "¬(p ∨ q)",
            "¬p ∧ ¬q",
            Negation(Disjunction(p, q)),
            Conjunction(Negation(p), Negation(q))
        ),
        (
            "p ∧ q",
            "q ∧ p",
            Conjunction(p, q),
            Conjunction(q, p)
        ),
    ]
    
    for name1, name2, formula1, formula2 in equivalence_tests:
        equivalent = are_equivalent(formula1, formula2)
        status = "✓ EQUIVALENT" if equivalent else "✗ NOT EQUIVALENT"
        print(f"{name1:20} ≡ {name2:25} {status}")
        print(f"  Formula 1: {formula1}")
        print(f"  Formula 2: {formula2}")
        print()


if __name__ == "__main__":
    main()
