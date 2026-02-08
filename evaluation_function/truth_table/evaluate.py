
from lf_toolkit.evaluation import Result

from evaluation_function.domain.formula import (
    Formula,
    Atom
)


from evaluation_function.domain.evaluators import _extract_atoms, Assignment, FormulaEvaluator
from evaluation_function.domain.formula import *
from evaluation_function.parsing.parser import formula_parser

from evaluation_function.parsing.tree_builder_error import BuildError


def evaluate_truth_table(variables: list[str], cells: list[list[str]], num_atoms) -> Result:
    """
    Function used to evaluate truth table response
    ---
    
    - `variables` array of formula strings (columns of the truth table)
    - `cells` the 2D array containing only the truth/false values
    - `num_atoms` the number of atoms in the truth table

    returns True if truth table is valid
    """

    if len(variables) == 0:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, "no variables provided")]
        )
    
    if len(cells) == 0:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, "no cells provided")]
        )

    # find the atoms of the formula
    formulas = variables
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

    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if cells[i][j] == "tt":
                cells[i][j] = True
            elif cells[i][j] == "ff":
                cells[i][j] = False
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
    if len(cells) < 2 ** num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, f"missing combinations in truth table")]
        )
    if len(cells) > 2 ** num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, f"excessive combinations in truth table")]
        )


    unique_rows = set(tuple(row[cell] for cell in existing_atoms.values()) for row in cells)
    if len(unique_rows) != 2 ** num_atoms:
        return Result(
            is_correct=False,
            feedback_items=[(Exception, "duplicated assignment to atoms")]
        )

    
    # evaluate truth table row by row

    for i in range(len(cells)):
        atoms_mapping = {}
        for j in range(len(cells[i])):
            formula = formulas[j]

            if isinstance(formula, Atom):
                atoms_mapping[formula] = cells[i][j]
                continue

            assignment = Assignment(atoms_mapping)
            if FormulaEvaluator(formula, assignment).evaluate() != cells[i][j]:
                return Result(
                    is_correct=False,
                    feedback_items=[(Exception, "incorrect cell value")]
                )
            

    return Result(is_correct=True)
            