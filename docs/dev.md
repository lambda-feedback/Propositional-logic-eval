# YourFunctionName

This evaluation function checks if the inputted respons is a valid formula within Propositional Logic.

Select the sort of evlauation you want to using the check box. Make sure to only select 1.


## Inputs

```json
{
  "response":"<str>",
  "answer":"<str>",
  "params": {
    "truthTable": "<bool>",
    "equivalence": "<bool>",
    "tautology": "<bool>",
    "satisfiability": "<bool>",
  }
}
```

### `truthTable`

uses the evaluation for truth tables

### `equivalence`

checks if response formula and answer formula are equivalent

### `tautology`

checks if response formula is a tautology

### `satisfiability`

checks if response formula is satisfiabiable

## Outputs

```json
{
  "is_correct": "<bool>",
  "feedback_items": "<str>"
}
```

### `is_correct`

boolean of the correctness of response

### `feedback_items`

the list of errors that occurred in the evaluation process