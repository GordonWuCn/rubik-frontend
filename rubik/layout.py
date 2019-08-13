#

from rubik.stat import IfElseStat
from rubik.expr import Expr, Field


class Bit(Expr):
    def __init__(self, length, const=None):
        self.length = length
        self.const = const


class layout:
    pass


class Layout:
    @staticmethod
    def wrap_raw(raw):
        if isinstance(raw, type) and issubclass(raw, layout):
            return StructLayout(raw)
        elif isinstance(raw, IfElseStat):
            return IfElseLayout(raw.guard, raw.true, raw.false)
        elif isinstance(raw, Layout):
            return raw
        else:
            assert False

    def __add__(self, raw_other):
        return self.add_impl(self.wrap_raw(raw_other))

    def add_impl(self, other):
        return SeqLayout([self, other])

    def __getattr__(self, name):
        return Field(name)


class StructLayout(Layout):
    def __init__(self, layout_type):
        self.layout_type = layout_type

    def iter_field(self):
        for name, field in self.layout_type.__dict__.items():
            if not name.startswith('_'):
                yield name, field


class SeqLayout(Layout):
    def __init__(self, layout_list):
        self.layout_list = layout_list

    def add_impl(self, other):
        return SeqLayout(self.layout_list + [other])


class IfElseLayout(Layout):
    def __init__(self, guard, true, false):
        self.guard = guard
        self.true = self.wrap_raw(true)
        self.false = self.wrap_raw(false)


class While:
    def __init__(self, guard):
        self.guard = guard

    def __rshift__(self, any):
        return WhileAnyLayout(self.guard, any.choice_list)


class Any(Layout):
    def __init__(self, *choice_list):
        self.choice_list = [self.wrap_raw(choice) for choice in choice_list]


class WhileAnyLayout(Layout):
    def __init__(self, guard, choice_list):
        self.guard = guard
        self.choice_list = choice_list
