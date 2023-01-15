# Python based Lambda Interpreter

### The input format is strictly restricted, illegal format will not be recoginized by the interpreter!

#### Notice that this interpreter can only interpret expressions. Commands are not considered, which makes the if branching consists only of expressions in either branches.

Conditional branching expression should be like:

`if (expr) then expr else expr`

All the lambda expression should be like this:

`\(ID.expr)`

Try out simple conditional branching:

`if (-10 > -1) then 30\*20 else 20%2`
