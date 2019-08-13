#

class Stat:
    pass

class If:
    def __init__(self, guard):
        self.guard = guard

    def __rshift__(self, stat):
        return IfElseStat(self.guard, stat)


class Else:
    pass


class IfStatElse:
    def __init__(self, if_else):
        self.guard = if_else.guard
        self.true = if_else.true

    def __rshift__(self, stat):
        return IfElseStat(self.guard, self.true, stat)


class IfElseStat(Stat):
    def __init__(self, guard, true, false=None):
        self.guard = guard
        self.true = true
        self.false = false

    def __rshift__(self, else_obj):
        assert self.false is None and isinstance(else_obj, Else)
        return IfStatElse(self)
