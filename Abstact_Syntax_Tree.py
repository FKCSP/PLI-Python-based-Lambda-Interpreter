'''
whnf is short for weak head normal form: which means the expression can no longer be simplief further. The work 'weak' means that although the inner part may not be its simplest form: for example: lambda x: 1+1 is in whnf! While 1+1 is not.
'''
class BiArith (object):
    def __init__ (self, first, second, ops):
        self.first = first
        self.second = second
        self.ops = ops

class UniArith (object):
    def __init__ (self, first, ops):
        self.first = first
        self.ops = ops

class Variable (object):
    def __init__ (self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __eq__ (self, other):
        if isinstance(other, Variable):
            if other.name == self.name:
                return True
        return False

    def iswhnf(self):
        return True


class Application():
    def __init__ (self, first, second):
        self.first = first
        self.second = second

    def __str__ (self):
        return str(self.first) + str(self.second)

    def __eq__(self, other):
        if isinstance(other, Application):
            return (other.first == self.first) and \
                (other.second == self.second)
        return False

    def iswhnf(self):
        if isinstance(self.first, Abstraction) :
            return False
        elif isinstance(self.first, Application) :
            return self._first.iswhnf()
        else:
            return True


class Abstraction():
    def __init__ (self, var: Variable, body):
        self.variable = var
        self.body = body

    def __str__(self):
        return '(\\' + str(self.variable) + '.' + str(self.body) + ')'

    def __eq__ (self, other):
        if isinstance(other, Abstraction):
            return (other.variable == self.variable) and \
                (other.body == self.body)
        return False

    def iswhnf(self):
        return True
