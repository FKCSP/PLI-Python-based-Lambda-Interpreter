import copy
from my_parser import parser
from operator import (add, sub, mul, truediv, mod, lt, le, eq, ne, gt, ge)
from Abstact_Syntax_Tree import Variable, Application, Abstraction, BinOps, UniOps, CondBranch, Recursive

ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "%": mod,
    ">": gt,
    ">=": ge,
    "<": lt,
    "<=": le,
    "==": eq,
    "!=": ne
}

def substitute(uTerm, uToSubstitute, uNewTerm):
    if isinstance(uTerm, int):
        return copy.deepcopy(uTerm)
    elif isinstance(uTerm, Variable):
        if uTerm.name == uToSubstitute.name:
            return copy.deepcopy(uNewTerm)

    elif isinstance(uTerm, Application):
        uTerm.first = substitute(uTerm.first, uToSubstitute, uNewTerm)
        uTerm.second = substitute(uTerm.second, uToSubstitute, uNewTerm)

    elif isinstance(uTerm, Abstraction):
        if uTerm.variable == uToSubstitute:
            uTerm.variable = substitute(uTerm.variable, uToSubstitute, uNewTerm)
        uTerm.body = substitute(uTerm.body, uToSubstitute, uNewTerm)

    elif isinstance(uTerm, UniOps):
        uTerm.first = substitute(uTerm.first, uToSubstitute, uNewTerm)

    elif isinstance(uTerm, BinOps):
        uTerm.first = substitute(uTerm.first, uToSubstitute, uNewTerm)
        uTerm.second = substitute(uTerm.second, uToSubstitute, uNewTerm)

    elif isinstance(uTerm, CondBranch):
        uTerm.cond = substitute(uTerm.cond, uToSubstitute, uNewTerm)
        uTerm.expr1 = substitute(uTerm.expr1, uToSubstitute, uNewTerm)
        uTerm.expr2 = substitute(uTerm.expr2, uToSubstitute, uNewTerm)

    return copy.deepcopy(uTerm)

def substitute_rec(uTerm, uToSubstitute, uNewTerm):
    if isinstance(uTerm, int):
        return copy.deepcopy(uTerm)
    elif isinstance(uTerm, Variable):
        if uTerm.name == uToSubstitute.name:
            return copy.deepcopy(uNewTerm)
    elif isinstance(uTerm, Application):
        uTerm.first = substitute_rec(uTerm.first, uToSubstitute, uNewTerm)
        uTerm.second = substitute_rec(uTerm.second, uToSubstitute, uNewTerm)
    elif isinstance(uTerm,Abstraction):
        if uTerm.variable.name == uToSubstitute.name:
            return copy.deepcopy(uTerm)
        uTerm.body = substitute_rec(uTerm.body, uToSubstitute, uNewTerm)
    elif isinstance(uTerm, UniOps):
        uTerm.first = substitute_rec(uTerm.first, uToSubstitute, uNewTerm)
    elif isinstance(uTerm, BinOps):
        uTerm.first = substitute_rec(uTerm.first, uToSubstitute, uNewTerm)
        uTerm.second = substitute_rec(uTerm.second, uToSubstitute, uNewTerm)
    elif isinstance(uTerm, CondBranch):
        uTerm.cond = substitute_rec(uTerm.cond, uToSubstitute, uNewTerm)
        uTerm.expr1 = substitute_rec(uTerm.expr1, uToSubstitute, uNewTerm)
        uTerm.expr2 = substitute_rec(uTerm.expr2, uToSubstitute, uNewTerm)
    return copy.deepcopy(uTerm)


def recur_reduction(obj, y, Ast):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, Variable):
        return obj if obj.name != y.name else Ast
    elif isinstance(obj, CondBranch):
        obj.cond = recur_reduction(obj.cond, y, Ast)
        if isinstance(obj.cond, int):
            return recur_reduction(obj.expr1, y, Ast) if obj.cond else recur_reduction(obj.expr2, y, Ast)
        return obj
    elif isinstance(obj, UniOps):
        obj.first = recur_reduction(obj.first, y, Ast)
        return interpret(obj)
    elif isinstance(obj, BinOps):
        obj.first = recur_reduction(obj.first, y, Ast)
        obj.second = recur_reduction(obj.second, y, Ast)
    elif isinstance(obj, Application):
        obj = beta_reduction(obj)
        
    return interpret(obj)


def beta_reduction(obj):
    if isinstance(obj.first, Variable) or isinstance(obj.first, int):
        second = interpret(obj.second)
        return Application(obj.first, second)
    elif isinstance(obj.first, Abstraction):
        second = interpret(obj.second)
        t =  substitute(obj.first.body, obj.first.variable, second)
        return interpret(t)
    elif isinstance(obj.first, Recursive):
        Abs = obj.first.lamb
        reduced_abs = interpret(obj.first)
        second = interpret(obj.second)
        t = substitute_rec(reduced_abs.body, reduced_abs.variable, second)
        print(t)
        return recur_reduction(t, obj.first.var1, Abs)

    elif isinstance(obj.first, BinOps) or isinstance(obj.first, UniOps) or isinstance(obj.first, CondBranch):
        obj.first = interpret(obj.first)
        obj.second = interpret(obj.second)
        return interpret(copy.deepcopy(obj))
    else:
        # left most
        obj.first = interpret(obj.first)
        return beta_reduction(copy.deepcopy(obj))


def interpret(obj):
    if isinstance(obj, Variable) or isinstance(obj, Abstraction) or isinstance(obj, int):
        return obj

    elif isinstance(obj, Recursive):
        obj.body = substitute(obj.body, obj.var1, obj.lamb)
        Abs = Abstraction(obj.var2, obj.body)
        return Abs

    elif isinstance(obj, BinOps):
        first, second = interpret(obj.first), interpret(obj.second)
        if isinstance(first, int) and isinstance(second, int):
            return ops[obj.ops](first, second)
        obj.first, obj.second = parser.parse(str(first)), parser.parse(str(second))
        return obj

    elif isinstance(obj, UniOps):
        first = interpret(obj.first)
        if isinstance(first, int):
            return -first if obj.ops == "-" else first
        obj.first = parser.parse(str(first))
        return obj

    elif isinstance(obj, CondBranch):
        obj.cond = interpret(obj.cond)
        if isinstance(obj.cond, int):
            return interpret(obj.expr1) if obj.cond else interpret(obj.expr2)
        return obj

    elif isinstance(obj, Application):
        return beta_reduction(obj)