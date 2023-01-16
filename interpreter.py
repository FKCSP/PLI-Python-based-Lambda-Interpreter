import copy
from my_parser import parser
from operator import (add, sub, mul, truediv, mod, lt, le, eq, ne, gt, ge)  
from Abstact_Syntax_Tree import Variable, Application, Abstraction, BiArith, UniArith, CondBranch

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

    return copy.deepcopy(uTerm)


def base_step(obj):
    if isinstance(obj, Variable) or isinstance(obj, Abstraction):
        return obj

    ## leftmost-outermost choice of redex
    elif isinstance(obj, Application):
        ## outermost
        if isinstance(obj.first, Abstraction):
            return substitute(uTerm.first.body, uTerm.first.variable, uTerm.second)
        else:
            ## leftmost
            new_first = base_step(uTerm._first)
            if new_first != uTerm.first:
                uTerm.first = newfirst
                return uTerm
            else:
                uTerm.second = base_step(uTerm.second)
                return uTerm



def beta_reduction(obj):
    if isinstance(obj, Variable) or isinstance(obj, Abstraction):
        return obj

    elif isinstance(obj, Application):
        t = obj
        reductions = []

        while (True):
            t_str = str(t)
            new_t = base_step(t)
            new_t_str = str(new_t)

            if new_t.iswhnf() :
                for b, a in reductions:
                    print(b, " -> ", a)
                return new_t
            else:
                reductions.append((t_str, new_t_str))
                t = new_t

def interpret(obj):
    if isinstance(obj, Variable) or isinstance(obj, Abstraction) or isinstance(obj, int):
        return obj

    elif isinstance(obj, BiArith):
        first, second = interpret(obj.first), interpret(obj.second)
        if isinstance(first, int) and isinstance(second, int):
            return ops[obj.ops](first, second)
        first, second = parser.parse(str(first)), parser.parse(str(second))
        return str(first)+obj.ops+str(second)

    elif isinstance(obj, UniArith):
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
    
