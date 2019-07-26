# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_tdx_dayline
   Description :
   Author :       pchaos
   date：          2019/7/26
-------------------------------------------------
   Change Activity:
                   2019/7/26:
-------------------------------------------------
"""
from unittest import TestCase
import unittest
import os, time
from tdx import get_dayline_by_fid, sh_path, sz_path

__author__ = 'pchaos'


class Test_tdx_dayline(TestCase):
	def setUp(self):
		self._started_at = time.time()

	def tearDown(self):
		elapsed = time.time() - self._started_at
		print('{} ({}s)'.format(self.id(), round(elapsed, 3)))

	def test_get_dayline_by_fid(self):
		print('sh demo')
		code = 'sh000001'
		dlist = get_dayline_by_fid(code)
		print('{} length: {}'.format(code, len(dlist)))

		dlist[0].display()
		dlist[-1].display()
		self.assertTrue(len(dlist)) ==0, '{} stays {} days'.format(code, len(dlist))

	def test_readFileOnce(self):
		""" 一次性读取整个文件
		"""
		from struct import unpack
		code = 'sz000680'
		ofile = open(os.path.join(sz_path, '{}.day'.format(code)), 'rb')
		buf = ofile.read()
		ofile.close()

		num = len(buf)
		no = num // 32
		b = 0
		e = 32
		line = ''

		for i in range(no):
			a = unpack('IIIIIfII', buf[b:e])
			line = str(a[0]) + ' ' + str(a[1] / 100.0) + ' ' + str(
				a[2] / 100.0) + ' ' + str(a[3] / 100.0) + ' ' + str(
				a[4] / 100.0) + ' ' + str(a[5] / 10.0) + ' ' + str(
				a[6]) + ' ' + str(a[7]) + ' ' + '\n'
			# print(line)
			b = b + 32
			e = e + 32

	def test_readFileOnce_multitimes(self):
		n=1000
		for i in range(n):
			self.test_readFileOnce()

	def test_readFileOnebyone(self):
		""" 循环读取整个文件
		"""
		from struct import unpack
		code = 'sz000680'
		ofile = open(os.path.join(sz_path, '{}.day'.format(code)), 'rb')
		buf = ofile.read()
		line = ''
		while 1:
			rd = ofile.read(32)
			if not rd: break
			# print i, len(rd)
			a = unpack('IIIIIfII', rd)
			line = str(a[0]) + ' ' + str(a[1] / 100.0) + ' ' + str(
				a[2] / 100.0) + ' ' + str(a[3] / 100.0) + ' ' + str(
				a[4] / 100.0) + ' ' + str(a[5] / 10.0) + ' ' + str(
				a[6]) + ' ' + str(a[7]) + ' ' + '\n'

		ofile.close()

	def test_readFileOnebyone_multitimes(self):
		''' 循环测试读取数据文件的时间

		:return:
		'''
		n=1000
		for i in range(n):
			self.test_readFileOnebyone()

if __name__ == '__main__':
    unittest.main()