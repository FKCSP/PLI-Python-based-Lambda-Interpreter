# Python based Lambda Interpreter

## Prerequisites

PIL is developed based on python package PLY ("https://github.com/dabeaz/ply")

Use the following command to install dependencies:

`pip install PLY`

## Run

You can run PLI in the project repository directly via:

`python main.py`

## Conventions

### Here are a few conventions you should notice when using PLI

- PLI's small step semantic striclty follows the **_call by value_** rule.

- The input format is strictly restricted, illegal format will not be recoginized, you can refer to the **_rules_** below or **_Examples_** for a quick start.

- Notice that this interpreter can only interpret expressions, commands are not supported.

- All expressions appeared in the Lambda expression are required to be closed, which means no free vars are allowed.

- Only integer operations are supported temporarily.

### The whole shift reduce rules are as follows

```
E | ID
  | NAT
  | IF (E) THEN E ELSE E
  | (E)
  | (E) E
  | LAMBDA ( ID . E )
  | REC ID . LAMBDA ( ID . E )
  | E + E | E - E | E * E | E / E | E % E
  | E < E | E <= E | E > E | E >= E | E == E | E != E
  | -E | +E
```

Input that cannot be completely reduced by the rules will cause an error.

## Examples

### Arithmetic Operation

`>>> 3+4*2`

`8`

`>>> 5*9+9/2-8%5`

`46`

### Comparison

`>>> 3*8 < 10-4`

`0`

### IF expression

`>>> if (10 * 9 > 80) then 1 else 0`

`1`

### Function Abstraction(note that the brackets are mandatory)

`>>> \(x.x)`

`(\x.x)`

### Function Application(The first term should be braced)

`>>> (\(x.x + 10)) 5`

`15`

`>>> (\(x. if (x>0) then x else -x)) (-1)`

`1`

### Recursive Function

Factorial function

`>>> (rec y. \(x. if (x>0) then (y)(x-1)*x else 1)) 4`

`24`

Fibonacci function

`>>> (rec y. \(x. if (x==0) then 1 else (if (x==1) then 1 else ((y)(x-1)+(y)(x-2))) ) ) 4`

`5`

### Complicated Ones

`>>> ((\(f.\(x. (f) x))) \(x. x+x) ) 2`

`4`

## More testcases

To view more tricky test cases, find them in **test_cases.txt**

You can run those cases by typing the following command in CLI:

`run test_cases.txt`
