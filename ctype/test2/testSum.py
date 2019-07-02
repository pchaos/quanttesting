# -*- coding: utf-8 -*-

from ctypes import cdll
mydll = cdll.LoadLibrary('libtest.so')
print(mydll.sum(5, 3))