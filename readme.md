# Python based Lambda Interpreter

## Prerequisites

PIL is developed based on python package PLY ("https://github.com/dabeaz/ply")

Use the following command to install depencies:

`pip install PLY`

## Run

You can run PLI in the project repository directly via:

`python main.py`

## Conventions

### Here are a few conventions you should notice when using PLI

- PLI's small step semantic striclty follows the call by value rule.

- The input format is strictly restricted, illegal format will not be recoginized, you can refer to the **rules** below or **Examples** for a quick start.

- Notice that this interpreter can only interpret expressions, commands are not supported.

- All expressions appeared in the Lambda expression are required to be closed, which means no free vars are allowed.

### The whole shift reduce rules are as follows

'''
E | ID
| NAT
| IF (E) THEN E ELSE E
| (E)
| (E) E
| LAMBDA ( ID . E )
| REC ID . LAMBDA ( ID . E )
| E + E | E - E | E \* E | E / E | E % E
| E < E | E <= E | E > E | E >= E | E == E | E != E
| -E | +E
'''

Input that cannot be completely reduced be the rules will cause an error.

## Examples

### IF expression

`>>> if (10 * 9 > 80) then 1 else 0`

`>>> 1`

### Function Abstraction(note that the brackets are mandatory)

`>>> \(x.x)`

`>>> \(x.x)`

### Function Application(The first term should be braced)

`>>> (\(x.x + 10)) 5`

`>>> 15`

### Complicated Ones

`>>> ((\(f.\(x. (f) x))) \(x. x+x) ) 2`
`>>> 4`

## More testcases

To view more tricky test cases, find them in **test_cases.txt**

You can run those cases by typing the following command in CLI:

`run test_cases.txt`
