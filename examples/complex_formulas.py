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


def main():
    p = Atom("p")
    q = Atom("q")
    r = Atom("r")
    
    assignment = Assignment({p: True, q: False, r: True})
    
    print("=== Complex Nested Formulas ===")
    print(f"Assignment: p=True, q=False, r=True")
    print()
    
    complex_formulas = [
        (
            "¬(p ∧ q)",
            Negation(Conjunction(p, q))
        ),
        (
            "(p → q) → r",
            Implication(Implication(p, q), r)
        ),
        (
            "p ∧ (q ∨ r)",
            Conjunction(p, Disjunction(q, r))
        ),
        (
            "(p ∧ q) ∨ (p ∧ r)",
            Disjunction(
                Conjunction(p, q),
                Conjunction(p, r)
            )
        ),
        (
            "p ↔ (q ↔ r)",
            Biconditional(p, Biconditional(q, r))
        ),
        (
            "((p → q) ∧ (q → r)) → (p → r)",
            Implication(
                Conjunction(
                    Implication(p, q),
                    Implication(q, r)
                ),
                Implication(p, r)
            )
        ),
        (
            "¬(p ∨ q) ↔ (¬p ∧ ¬q)",
            Biconditional(
                Negation(Disjunction(p, q)),
                Conjunction(Negation(p), Negation(q))
            )
        ),
    ]
    
    for name, formula in complex_formulas:
        evaluator = FormulaEvaluator(formula, assignment)
        result = evaluator.evaluate()
        print(f"{name:35} = {result}")
        print(f"  Formula: {formula}")
        print()


if __name__ == "__main__":
    main()
