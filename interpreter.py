import copy
from Abstact_Syntax_Tree import Variable, Application, Abstraction

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
