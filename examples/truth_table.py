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


def generate_truth_table(atoms, formula):
    print(f"=== Truth Table for: {formula} ===")
    print()
    
    header = " | ".join([atom.name for atom in atoms] + ["Result"])
    separator = "-" * len(header)
    print(header)
    print(separator)
    
    for assignment_values in product([False, True], repeat=len(atoms)):
        assignment_dict = {atom: val for atom, val in zip(atoms, assignment_values)}
        assignment = Assignment(assignment_dict)
        evaluator = FormulaEvaluator(formula, assignment)
        result = evaluator.evaluate()
        
        row = " | ".join([str(val) for val in assignment_values] + [str(result)])
        print(row)
    
    print()


def main():
    p = Atom("p")
    q = Atom("q")
    
    formulas = [
        ("p ∧ q", Conjunction(p, q)),
        ("p ∨ q", Disjunction(p, q)),
        ("p → q", Implication(p, q)),
        ("p ↔ q", Biconditional(p, q)),
        ("¬(p ∧ q)", Negation(Conjunction(p, q))),
        ("(p → q) ∧ (q → p)", Conjunction(Implication(p, q), Implication(q, p))),
    ]
    
    for name, formula in formulas:
        generate_truth_table([p, q], formula)
    
    print("\n=== Three Variable Example ===")
    r = Atom("r")
    formula = Implication(Conjunction(p, q), r)
    generate_truth_table([p, q, r], formula)


if __name__ == "__main__":
    main()
