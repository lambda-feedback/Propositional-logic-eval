# YourFunctionName

This evaluation function checks if the inputted respons is a valid formula within Propositional Logic.

Select the sort of evlauation you want to using the check box. Make sure to only select 1.


## Inputs

```json
{
  "response": { "formula": "<str>", "truthTable": null | { "variables": ["<str>"], "cells": [[ "<str>" ]] } },
  "answer": {
    "satisability": true | false,
    "tautology": true | false,
    "equivalent": null | "<str>",
    "truthTable": null | { }
  },
  "params": { }
}
```

Exactly one of `satisability`, `tautology`, `equivalent` (non-null), or `truthTable` (non-null) must be set in `answer` to choose the evaluation mode.

### `truthTable`

When `answer.truthTable` is not null, uses truth table evaluation (response must include `truthTable` with `variables` and `cells`).

### `equivalent`

When `answer.equivalent` is a string, checks if response formula and that formula are equivalent.

### `tautology`

When `answer.tautology` is true, checks if response formula is a tautology.

### `satisability`

When `answer.satisability` is true, checks if response formula is satisfiable.

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