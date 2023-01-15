import copy
from Abstact_Syntax_Tree import Variable, Application, Abstraction

def substitute(uTerm, uToSubstitute, uNewTerm):
    if isinstance(uTerm, Variable):
        if uTerm.name == uToSubstitute.name:
            return copy.deepcopy(uNewTerm)
    elif isinstance(uTerm, Application):
        uTerm.first = substitute(uTerm.first, uToSubstitute, uNewTerm)
        uTerm.second = substitute(uTerm.second, uToSubstitute, uNewTerm)

    elif isinstance (uTerm, Abstraction):
        if uTerm._variable == uToSubstitute:
            uTerm._variable = substitute (uTerm._variable, uToSubstitute, uNewTerm)
        uTerm._body = substitute (uTerm._body, uToSubstitute, uNewTerm)

    return copy.deepcopy (uTerm)


def beta_reduce (uTerm):
    if isinstance (uTerm, Variable):
        return uTerm

    elif isinstance (uTerm, Abstraction):
        return uTerm

    ## leftmost-outermost choice of redex
    elif isinstance (uTerm, Application):
        ## outermost
        if isinstance (uTerm._first, Abstraction):
            return substitute (uTerm._first._body,
                               uTerm._first._variable,
                               uTerm._second)
        else:
            ## leftmost
            new_first = beta_reduce (uTerm._first)
            if new_first != uTerm._first:
                uTerm._first = new_first
                return uTerm
            else:
                uTerm._second = beta_reduce (uTerm._second)
                return uTerm



def multi_step_beta_reduce(uTerm):
    if isinstance (uTerm, Variable) or isinstance (uTerm, Abstraction):
        return uTerm

    elif isinstance(uTerm, Application):
        t = uTerm
        reductions = []

        while (True):
            t_str = str(t)
            new_t = beta_reduce(t)
            new_t_str = str(new_t)

            if new_t.iswhnf() :
                for b, a in reductions:
                    print(b, " -> ", a)
                return new_t
            else:
                reductions.append ((t_str, new_t_str))
                t = new_t
