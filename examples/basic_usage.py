from evaluation_function.propositional_logic import (
    Atom,
    Truth,
    Falsity,
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
    
    assignment = Assignment({p: True, q: False})
    
    print("=== Basic Formula Evaluation ===")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"Assignment: p=True, q=False")
    print()
    
    formulas = [
        ("p", p),
        ("q", q),
        ("⊤", Truth()),
        ("⊥", Falsity()),
        ("¬p", Negation(p)),
        ("p ∧ q", Conjunction(p, q)),
        ("p ∨ q", Disjunction(p, q)),
        ("p → q", Implication(p, q)),
        ("p ↔ q", Biconditional(p, q)),
    ]
    
    for name, formula in formulas:
        evaluator = FormulaEvaluator(formula, assignment)
        result = evaluator.evaluate()
        print(f"{name:15} = {result}")
    
    print()
    print("=== Different Assignment ===")
    assignment2 = Assignment({p: True, q: True})
    
    for name, formula in formulas:
        evaluator = FormulaEvaluator(formula, assignment2)
        result = evaluator.evaluate()
        print(f"{name:15} = {result}")


if __name__ == "__main__":
    main()
