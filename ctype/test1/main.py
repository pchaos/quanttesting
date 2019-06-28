# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       pchaos
   date：          2019/6/27
-------------------------------------------------
   Change Activity:
                   2019/6/27:
-------------------------------------------------
"""
import platform
from ctypes import *

if platform.system() == 'Windows':
	libc = cdll.LoadLibrary('msvcrt.dll')
elif platform.system() == 'Linux':
	libc = cdll.LoadLibrary('libc.so.6')

libc.printf('Hello ctypes!\n')


class Bottles(object):
	def __init__(self, number):
		self._as_parameter_ = number  # here only accept integer, string, unicode string


bottles = Bottles(42)
libc.printf('%d bottles of beer\n', bottles)
