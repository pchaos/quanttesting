# -*- coding: utf-8 -*-
import ctypes
from ctype.test1 import *

class Line(ctypes.Structure):
    _fields_ = [('start', Point), ('end', Point)]

    def __init__(self, lib):
        get_line = wrap_function(lib, 'get_line', Line, None)
        line = get_line()
        self.start = line.start
        self.end = line.end
        self.show_line_func = wrap_function(lib, 'show_line', None, [Line])
        self.move_line_func = wrap_function(lib, 'move_line_by_ref', None,
                                            [ctypes.POINTER(Line)])

    def __repr__(self):
        return '{0}->{1}'.format(self.start, self.end)

    def show_line(self):
        self.show_line_func(self)

    def moveLine(self):
        self.move_line_func(self)


if __name__ == '__main__' and __package__ is None:
    from os import sys, path

    # __file__ should be defined in this case
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)
