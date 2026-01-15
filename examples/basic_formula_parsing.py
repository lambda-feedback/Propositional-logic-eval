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
    
    print("=== Basic Formula Parsing ===")
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
