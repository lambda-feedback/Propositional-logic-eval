
from lf_toolkit.evaluation import Result

from evaluation_function.domain.formula import (
    Formula,
    Atom
)


from evaluation_function.domain.evaluators import _extract_atoms, Assignment, FormulaEvaluator
from evaluation_function.domain.formula import *
from evaluation_function.parsing.parser import formula_parser

from evaluation_function.parsing.tree_builder_error import BuildError


# assume table sent through is of type list[list[str]]
def evaluate_truth_table(input: list[list[str]], num_atoms) -> Result:
    """
    Function used to evaluate truth table response
    ---
    
    - `input` the 2D array containing the formuals and the cells of the truth table
    - `num_atoms` the number of atoms in the truth table

    returns True if truth table is valid
    """

    if len(input) == 0:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, "no input was given")]
        )
        
    elif len(input) == 1:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, "Must provide names and its truth values")]
        )

    # find the atoms of the formula
    formulas = input[0]
    existing_atoms = {}

    for i in range(len(formulas)):
        formula_string = formulas[i]
        error_message = f"formula in column {i+1} incorrect: "

        # parse tokens into Formula
        try:
            formula = formula_parser(formula_string)
        
        except BuildError as e:
            return Result(
                is_correct=False,
                feedback_items=[(BuildError, error_message + str(e))]
            )
        except ValueError as e:
            return Result(
                is_correct=False,
                feedback_items=[(ValueError, error_message + str(e))]
            )

        # formula is valid
        
        # if formula is an atom, keep track of it
        if isinstance(formula, Atom):
            existing_atoms[formula] = i
        
        # otherwise check all atoms in formula is to the left on the table (i.e all atoms in formula has been defined)
        else:
            current_atoms = _extract_atoms(formula)
            
            for atom in current_atoms:

                # if an atom is undefined, erro
                if atom not in existing_atoms:
                    return Result(
                        is_correct=False,
                        feedback_items=[(Exception, f"in column {i+1}, atom {atom} in formula {formula_string} is undefined")]
                    )
        
        # replace strings with 
        formulas[i] = formula
    
    # all formula and its order in the table is valid====

    # check all the cells are valid:

    for i in range(1, len(input)):
        for j in range(len(input[i])):
            if input[i][j] == "tt":
                input[i][j] = True
            elif input[i][j] == "ff":
                input[i][j] = False
            else:
                return Result(
                    is_correct=False,
                    feedback_items=[(Exception, f"cell in column {j+1} row {i+1} invalid")]
                )


    # check that every combination of the atoms is stated in the truth table.

    if len(existing_atoms) != num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, f"missing combinations in truth table")]
        )
    if len(input) - 1 < 2 ** num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, f"missing combinations in truth table")]
        )
    if len(input) - 1 > 2 ** num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, f"excessive combinations in truth table")]
        )


    unique_rows = set(tuple(row[cell] for cell in existing_atoms.values()) for row in input[1:])
    if len(unique_rows) != 2 ** num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, "duplicated assignment to atoms")]
        )

    
    # evaluate truth table row by row

    for i in range(1, len(input)):
        atoms_mapping = {}
        for j in range(len(input[i])):
            formula = formulas[j]

            if isinstance(formula, Atom):
                atoms_mapping[formula] = input[i][j]
                continue

            assignment = Assignment(atoms_mapping)
            if FormulaEvaluator(formula, assignment).evaluate() != input[i][j]:
                return Result(
                    is_correct=False,
                    feedback_items=[(Exception, "incorrect cell value")]
                )
            

    return Result(is_correct=True)
            