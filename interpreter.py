import copy
from my_parser import parser
from operator import (add, sub, mul, truediv, mod, lt, le, eq, ne, gt, ge)
from Abstact_Syntax_Tree import Variable, Application, Abstraction, BinOps, UniOps, CondBranch

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
    if isinstance(uTerm, Variable):
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


def base_step(obj):
    if isinstance(obj, Variable) or isinstance(obj, Abstraction):
        return obj

    ## leftmost-outermost choice of redex
    elif isinstance(obj, Application):
        ## outermost
        if isinstance(obj.second, Application):
            return substitute(obj.first.body, obj.first.variable, obj.second)
        else:
            ## leftmost
            new_first = base_step(obj._first)
            if new_first != obj.first:
                obj.first = new_first
                return obj
            else:
                obj.second = base_step(obj.second)
                return obj


def beta_reduction(obj):
    if isinstance(obj.first, Variable) or isinstance(obj.first, int):
        second = interpret(obj.second)
        return Application(obj.first, second)
    if isinstance(obj.first, Abstraction):
        second = interpret(obj.second)
        t =  substitute(obj.first.body, obj.first.variable, second)
        return interpret(t)
    if isinstance(obj.first, BinOps) or isinstance(obj.first, UniOps) or isinstance(obj.first, CondBranch):
        obj.first = interpret(obj.first)
        obj.second = interpret(obj.second)
        return interpret(copy.deepcopy(obj))
    else:
        obj.first = interpret(obj.first)
        return beta_reduction(copy.deepcopy(obj))
        # left most


def interpret(obj):
    if isinstance(obj, Variable) or isinstance(obj, Abstraction) or isinstance(obj, int):
        return obj

    elif isinstance(obj, BinOps):
        first, second = interpret(obj.first), interpret(obj.second)
        if isinstance(first, int) and isinstance(second, int):
            return ops[obj.ops](first, second)
        first, second = parser.parse(str(first)), parser.parse(str(second))
        return str(first)+obj.ops+str(second)

    elif isinstance(obj, UniOps):
        first = interpret(obj.first)
        if isinstance(first, int):
            return -first if obj.ops == "-" else first
        first = parser.parse(str(first))
        return obj.ops+str(first)

    elif isinstance(obj, CondBranch):
        cond = interpret(obj.cond)
        if isinstance(cond,int):
            return interpret(obj.expr1) if cond else interpret(obj.expr2)
        return 'if '+str(cond)+ ' then '+str(obj.expr1) + ' else '+str(obj.expr2)

    elif isinstance(obj, Application):
        return beta_reduction(obj)