
from evaluation_function.domain.formula import (
    Formula,
    Atom
)


from evaluation_function.domain.evaluators import _extract_atoms
from evaluation_function.domain.formula import *
from evaluation_function.parsing.parser import formula_parser

from evaluation_function.parsing.tree_builder_error import BuildError


# assume table sent through is of type list[list[str]]
def evaluate(input: list[list[str]]) -> bool:

    if len(input) == 0:
        raise Exception("no input was given")
    elif len(input) == 1:
        raise Exception("Must provide names and its truth values")

    # find the atoms of the formula
    formulas = input[0]
    existing_atoms = set()

    for i in range(len(formulas)):
        formula_string = formulas[i]
        error_message = f"formula in column {i+1} incorrect: "

        # parse tokens into Formula
        try:
            formula = formula_parser(formula_string)
        
        except BuildError as e:
            raise Exception(error_message + str(e))
        except ValueError as e:
            raise Exception(error_message + str(e))

        # formula is valid
        
        # if formula is an atom, keep track of it
        if isinstance(formula, Atom):
            existing_atoms.add(formula)
        
        # otherwise check all atoms in formula is to the left on the table (i.e all atoms in formula has been defined)
        else:
            current_atoms = _extract_atoms(formula)
            
            for atom in current_atoms:

                # if an atom is undefined, erro
                if atom not in existing_atoms:
                    raise Exception(f"in column {i+1}, atom {atom} in formula {formula_string} is undefined")
    
    # all formula and its order in the table is valid

    
                
        








    
