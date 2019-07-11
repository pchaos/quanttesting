# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_CHCOUNTS
   Description :
   Author :       pchaos
   date：          2019/6/21
-------------------------------------------------
   Change Activity:
                   2019/6/21:
-------------------------------------------------
"""
from unittest import TestCase
from czsc.chCounts import *
import datetime
import os

def read_zxg(fname='zxg.txt'):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	if not fname.find(os.sep) > -1:
		fname = os.path.join(dir_path, fname)
	resultList = []
	if os.path.isfile(fname):
		with open(fname, 'r', encoding='UTF-8') as zxg:
			alist = zxg.readlines()
	for a in alist:
		resultList.append(a[0:6])
	return resultList


class TestCHCOUNTS(TestCase):
	def test_CHCOUNTS(self):
		code = '000001'
		df = qa.QA_fetch_stock_day_adv(code)
		chCounts = df.to_qfq().add_func(CHCOUNTS)
		self.assertTrue(len(chCounts) > 0, '指标为零')
		print(chCounts)

	def test_CHCOUNTS_codelist(self):
		# code列表
		code = ['000001', '600000', '000858']
		df = qa.QA_fetch_stock_day_adv(code)
		self.assertTrue(len(df.code) == len(code),
		                '有未获取到的代码 {} {}, {}:{}'.format(df.code, code,
		                                               len(df.code), len(code)))

		chCounts = df.to_qfq().add_func(CHCOUNTS)
		self.assertTrue(len(chCounts) > 0, '指标为零')
		print(chCounts)

	def test_CHCOUNTS_indexlist(self):
		# code列表
		code = ['399004', '000016', '399005']
		start = datetime.datetime.now() - datetime.timedelta(300)
		end = datetime.datetime.now() - datetime.timedelta(10)
		df = qa.QA_fetch_index_day_adv(code, start, end)
		self.assertTrue(len(df.code) == len(code),
		                '有未获取到的代码 {} {}, {}:{}'.format(df.code, code,
		                                               len(df.code), len(code)))

		chCounts = df.add_func(CHCOUNTS)
		self.assertTrue(len(chCounts) > 0, '指标为零')
		print(chCounts)
