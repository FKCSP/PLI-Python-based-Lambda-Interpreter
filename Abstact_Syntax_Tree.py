class BinOps(object):
    def __init__ (self, first, second, ops):
        self.first = first
        self.second = second
        self.ops = ops

    def __str__(self):
        return str(self.first) + ' ' + self.ops + ' ' + str(self.second)


class UniOps(object):
    def __init__(self, first, ops):
        self.first = first
        self.ops = ops

    def __str__(self):
        return self.ops + str(self.first)


class CondBranch(object):
    def __init__(self, cond, expr1, expr2):
        self.cond = cond
        self.expr1 = expr1
        self.expr2 = expr2

    def __str__(self):
        return 'if ('+ str(self.cond) + ') then ' + str(self.expr1) + ' else ' + str(self.expr2)


class Variable(object):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __eq__ (self, other):
        if isinstance(other, Variable):
            if other.name == self.name:
                return True
        return False


class Application():
    def __init__ (self, first, second):
        self.first = first
        self.second = second

    def __str__ (self):
        left = '('+str(self.first)+')'
        right = str(self.second) if (isinstance(self.second, int) or isinstance(self.second, Variable) or isinstance(self.second, Abstraction)) else '('+str(self.second)+')'
        return left + ' ' + right

    def __eq__(self, other):
        if isinstance(other, Application):
            return (other.first == self.first) and \
                (other.second == self.second)
        return False


class Abstraction():
    def __init__ (self, var: Variable, body):
        self.variable = var
        self.body = body

    def __str__(self):
        return '\\(' + str(self.variable) + '.' + str(self.body) + ')'


class Recursive():
    def __init__(self, var1: Variable, var2: Variable, body):
        self.var1 = var1
        self.var2 = var2
        self.body = body
        self.lamb = Abstraction(var2, body)

    def __str__(self):
        return 'rec ' + str(self.var1) + '.\\(' + str(self.var2) + '.' + str(self.body) +')'
