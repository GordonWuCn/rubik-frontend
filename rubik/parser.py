#

from rubik.layout import Layout


class Connectionless:
    def __setattr__(self, name, obj):
        if name == 'header':
            self.set_header(obj)
        else:
            super().__setattr__(name, obj)

    def set_header(self, raw_layout):
        super().__setattr__('header', Layout.wrap_raw(raw_layout))

