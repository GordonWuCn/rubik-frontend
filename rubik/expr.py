#


class Expr:
    def __add__(self, other):
        return Op('add', self, other)

    def __sub__(self, other):
        return Op('sub', self, other)

    def __mul__(self, other):
        return Op('mul', self, other)

    def __div__(self, other):
        return Op('div', self, other)

    def __le__(self, other):
        return Op('le', self, other)

    def __lt__(self, other):
        return Op('lt', self, other)

    def __ge__(self, other):
        return Op('ge', self, other)

    def __gt__(self, other):
        return Op('gt', self, other)

    def __eq__(self, other):
        return Op('eq', self, other)

    def __ne__(self, other):
        return Op('ne', self, other)

    def __lshift__(self, other):
        return Op('lshift', self, other)

    def __rshift__(self, other):
        return Op('rshift', self, other)


class Op(Expr):
    def __init__(self, op_type, lhs, rhs):
        self.op = op_type
        self.lhs = lhs
        self.rhs = rhs


class Field(Expr):
    def __init__(self, name):
        self.name = name
