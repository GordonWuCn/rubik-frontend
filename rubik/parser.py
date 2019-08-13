#

from rubik.layout import Layout
from rubik.expr import Cursor


class Connectionless:
    def __init__(self):
        self.cursor = Cursor()

    def __setattr__(self, name, obj):
        if name == 'header':
            self.set_header(obj)
        else:
            super().__setattr__(name, obj)

    def set_header(self, raw_layout):
        super().__setattr__('header', Layout.wrap_raw(raw_layout))
