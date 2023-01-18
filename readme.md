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

- Arithmetic operation takes precedence over function application, so please add brackets to arithmetic operations if necessary. eg. `\(x.x+x)(2+3)` and `\(x.x+x)2+3` are different.

- If the expression e3 of `if (e1) then e2 else e3` is not NAT, Variable or function application, it should be parenthesized as well. eg. `\(x. if (x==0) then 1 else (x-1))`.

- We set a limit on the recursion depth, so the function application with too deep recursion depth may report an error. For recursive functions with infinite loops, `RecursionError` will be returned. eg. `(rec y. \(x. if (x>0) then 0 else (y)(x-1))) 0`

### The whole shift reduce rules are as follows

```
E | F
  | E F
  | E + E | E - E | E * E | E / E | E % E
  | E < E | E <= E | E > E | E >= E | E == E | E != E
  | -E | +E
  | IF (E) THEN E ELSE E
F | ID
  | NAT
  | (E)
  | lambda ( ID . E )
  | rec ID . lambda ( ID . E )
```

Input that cannot be completely reduced by the rules will cause an error.

### How to use

```
arithmetic operations or comparisons: eg.2+4*8 or x/3+9
conditional branch: if (e1) then e2 else e3
function abstraction: \(x. expr) or \(x.\(y.x+y))
function application(left associative): e1 e2 
recursive function: rec y.\(x. expr)
```

## Examples

### Arithmetic Operation

`>>> 3+4*2`

`11`

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

`\(x.x)`

### Function Application(The first term should be braced)

`>>> f x`

`f x`

`>>> \(x.x + 10) 5`

`15`

`>>> \(x. if (x>0) then x else -x) (-1)`

`1`

`>>> \(x.\(y. x y)) \(x.x+x)`

`\(y.\(x.x + x) y)`

### Recursive Function

Factorial function

`>>> rec y. \(x. if (x>0) then y(x-1)*x else 1)`

`\(x.if (x > 0) then (rec y.\(x.if (x > 0) then y (x - 1) * x else 1)) (x - 1) * x else 1)`

`>>> (rec y. \(x. if (x>0) then y(x-1)*x else 1)) z`

`if (z > 0) then (rec y.\(x.if (x > 0) then y (x - 1) * x else 1)) (z - 1) * z else 1`

`>>> (rec y. \(x. if (x>0) then y(x-1)*x else 1)) 5`

`120`

Fibonacci function

`>>> (rec y. \(x. if (x==0) then 1 else (if (x==1) then 1 else ((y)(x-1)+(y)(x-2))) ) ) 4`

`5`

Functions which may have infinite loops

`>>> (rec y. \(x. if (x>0) then 0 else y(x-1))) 1`

`0`

`>>> (rec y. \(x. if (x>0) then 0 else y(x-1))) 0`

`RecursionError: maximum recursion depth exceeded`

## More testcases

We provide more test cases, find them in **test_cases.txt**

You can run them by typing the following command in PLI's CLI:

`run test_cases.txt`
