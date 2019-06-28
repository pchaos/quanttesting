# -*- coding: utf-8 -*-
import platform
import ctypes
from ctype.test1 import *


class Point(ctypes.Structure):
	_fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]

	def __init__(self, lib, x=None, y=None):
		if x:
			self.x = x
			self.y = y
		else:
			get_point = wrap_function(lib, 'get_point', Point, None)
			self = get_point()

		self.show_point_func = wrap_function(lib, 'show_point', None, [Point])
		self.move_point_func = wrap_function(lib, 'move_point', None, [Point])
		self.move_point_ref_func = wrap_function(lib, 'move_point_by_ref', None,
		                                         [ctypes.POINTER(Point)])

	def __repr__(self):
		return '({0}, {1})'.format(self.x, self.y)

	def show_point(self):
		self.show_point_func(self)

	def move_point(self):
		self.move_point_func(self)

	def move_point_by_ref(self):
		self.move_point_ref_func(self)


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
	# libc.printf(' Hello ctypes!        \n')

	libc = ctypes.CDLL('./libpoint.so')
	print(libc)
	p = Point(libc, 1, 2)
	p.move_point()