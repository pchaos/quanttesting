# -*- coding: utf-8 -*-
import platform
import ctypes
from ctypes import *
from ctype.test1 import *


class Point(Structure):
    _fields_ = [('x', c_int), ('y', c_int)]

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)


def myfunc(x):
    x = x + 2


y = 9
myfunc(y)
print("this is y", y)


def mylistfunc(x):
    x.append("more data")


z = list()
mylistfunc(z)
print("this is z", z)

if __name__ == '__main__' and __package__ is None:
    from os import sys, path

    # __file__ should be defined in this case
    PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(PARENT_DIR)

    if platform.system() == 'Windows':
        libc = cdll.LoadLibrary('msvcrt.dll')
    elif platform.system() == 'Linux':
        libc = cdll.LoadLibrary('libc.so.6')

    print(libc)
    libc = ctypes.CDLL('./libpoint.so')
    p = Point(1, 2)
    print("Point in Python is", p)
    libc.show_point(p)
    libc.move_point(p)
    print("Point in Python is", p)
    print()

    # --- Pass by value ---
    print("Pass by value")
    move_point = wrap_function(libc, 'move_point', None, [Point])
    a = Point(5, 6)
    print("Point in Python is", a)
    move_point(a)
    print("Point in Python is", a)
    print()

    # --- Pass by reference ---
    print("Pass by reference")
    move_point_by_ref = wrap_function(libc, 'move_point_by_ref', None,
                                      [ctypes.POINTER(Point)])
    a = Point(5, 6)
    print("Point in Python is", a)
    move_point_by_ref(a)
    print("Point in Python is", a)
