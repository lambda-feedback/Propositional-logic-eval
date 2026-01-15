from evaluation_function.evaluation import parse_response

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
    
    print("=== Complex Formula Parsing ===")
    print()

    formulas = [
        ("p ∧ q ∨ q", Disjunction(Conjunction(p, q), q)),
        # ("p ∨ q",     Disjunction(p, q)),
        ("p → p ∨ q", Implication(p, Disjunction(p, q))),
        ("p ↔ p → p", Biconditional(p, Implication(p, p))),
        ("p ↔ p ↔ p ↔ p", Biconditional(Biconditional(Biconditional(p, p), p), p)),
        ("p ∧ q → ¬p ∨ q", Implication((Conjunction(p, q)), Disjunction(Negation(p), q)))
    ]

    passed = 0

    for name, formula in formulas:
        result = None

        try:
            result = parse_response(name)[1]
        except Exception as e:
            reslt = e

        if formula != result:
            print()
            print("failed!!!!!!!!!!!!!!!!!!!!!!")
            print(f"formula:  {name}")
            print(f"expected: {formula}")
            print(f"actual:   {result}")
        else:
            print("passed")
            passed += 1

    print()
    print("=== Result ===")
    print(f"{passed}/{len(formulas)}")
    

if __name__ == "__main__":
    main()
