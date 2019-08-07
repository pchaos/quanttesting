# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     chCount
   Description : 缠中说禅均线强度
   Author :       pchaos
   date：          2019/6/21
-------------------------------------------------
   Change Activity:
                   2019/6/21:
-------------------------------------------------
"""
import QUANTAXIS as qa
import pandas as pd


def CHCOUNTS(data):
	""" 均线强弱
	:param data:
	:return:
	"""
	nlist = [5, 13, 21, 34, 55, 89, 144, 233]
	counts = pd.DataFrame([0] * len(data), columns=['counts'])
	counts.index = data.index
	for N in nlist:
		var = qa.MA(data['close'], N) <= data['close']
		# var.index = range(len(var.index))
		counts['counts'] = counts['counts'] + var.apply(lambda x: 1 if x else 0)
	return pd.DataFrame({'chCounts': counts['counts']})


def CHCOUNTS2(data):
	""" 均线强弱
	（和CHCOUNTS返回结果相同）
	:param data:
	:return:
	"""
	nlist = [5, 13, 21, 34, 55, 89, 144, 233]
	for N in nlist:
		var = qa.MA(data['close'], N) <= data['close']
		if N == nlist[0]:
			counts = var.apply(lambda x: 1 if x else 0)
		else:
			# var.index = rangcolumnse(len(var.index))
			counts += var.apply(lambda x: 1 if x else 0)
	return pd.DataFrame({'chCounts': counts})


class CHCOUNT():
	_counts = 0


