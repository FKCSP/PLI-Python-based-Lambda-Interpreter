# Python based Lambda Interpreter

## Prerequisites

PIL is developed based on python package PLY("https://github.com/dabeaz/ply")

Use the following command to install depencies:

`pip install PLY`

## Run

You can run PLI in the project repository directly via:

`python main.py`

## Rules



## Conventions

### Here are a few conventions you should notice when using PLI:

- The input format is strictly restricted, illegal format will not be recoginized by the interpreter, you can refer to the **Examples** for a quick start.

- Notice that this interpreter can only interpret expressions, commands will not be parsed.

- All expressions appeared in the Lambda expression are required to be closed, which means no free vars are allowed.

## Examples

### Conditional branching expression should be like:

`if (expr) then expr else expr`

### All the lambda expression should be like:

`\(x.x)`

### The first term of function application should be in brackets`(E) E`:

`(\(x.x + 10)) 5`
