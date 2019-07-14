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
import QUANTAXIS as qa
import matplotlib.pyplot as plt


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


def readstkData(stockcode, sday, eday):
	''' 返回

	:param stockcode:
	:param sday:
	:param eday:
	:return:
	'''
	returndata = qa.QA_fetch_index_day_adv(stockcode, sday, eday).data

	# Wash data
	# returndata = returndata.sort_index()
	# returndata.index.name = 'DateTime'
	returndata.drop('amount', axis=1, inplace=True)
	return returndata[['open', 'high', 'close', 'low', 'volume']]


class TestCHCOUNTS(TestCase):
	def test_CHCOUNTS(self):
		code = '000001'
		df = qa.QA_fetch_stock_day_adv(code)
		print(df.data.columns, type(df.data))
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
		self._test_index_day_adv(code, end, start)

	def _test_index_day_adv(self, code, end, start):
		df = qa.QA_fetch_index_day_adv(code, start, end)
		self.assertTrue(len(df.code) == len(code),
		                '有未获取到的代码 {} {}, {}:{}'.format(df.code, code,
		                                               len(df.code), len(code)))
		chCounts = df.add_func(CHCOUNTS)
		self.assertTrue(len(chCounts) > 0, '指标为零')
		print(chCounts)

	def test_CHCOUNTS_indexlist(self):
		# code列表
		code = read_zxg()
		start = datetime.datetime.now() - datetime.timedelta(300)
		end = datetime.datetime.now() - datetime.timedelta(10)
		self._test_index_day_adv(code, end, start)

	def test_readstkData(self):
		# https://zhuanlan.zhihu.com/p/29519040
		from matplotlib import dates as mdates
		import mpl_finance as mpf
		from mpl_finance import candlestick_ohlc
		from matplotlib import ticker as mticker
		import pylab
		code = ['399004']
		MA1 = 10
		MA2 = 50
		start = datetime.datetime.now() - datetime.timedelta(300)
		end = datetime.datetime.now() - datetime.timedelta(10)
		days = readstkData(code, start, end)
		# print(days)
		daysreshape = days.reset_index()
		daysreshape['DateTime'] = mdates.date2num(
			daysreshape['date'].astype(datetime.date))
		daysreshape.drop('volume', axis=1, inplace=True)
		daysreshape.drop('date', axis=1, inplace=True)
		# print(daysreshape)
		daysreshape = daysreshape.reindex(
			columns=['DateTime', 'open', 'high', 'low', 'close'])

		Av1 = qa.MA(daysreshape.close, MA1)
		Av2 = qa.MA(daysreshape.close, MA2)
		SP = len(daysreshape.DateTime.values[MA2 - 1:])
		fig = plt.figure(facecolor='#07000d', figsize=(15, 10))

		plt.style.use('dark_background')
		ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
		# ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, axisbg='#07000d')
		candlestick_ohlc(ax1, daysreshape.values[-SP:], width=.6,
		                 colorup='#ff1717', colordown='#53c156')
		Label1 = str(MA1) + ' SMA'
		Label2 = str(MA2) + ' SMA'

		ax1.plot(daysreshape.DateTime.values[-SP:], Av1[-SP:], '#e1edf9',
		         label=Label1, linewidth=1.5)
		ax1.plot(daysreshape.DateTime.values[-SP:], Av2[-SP:], '#4ee6fd',
		         label=Label2, linewidth=1.5)
		ax1.grid(True, color='w')
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		ax1.yaxis.label.set_color("w")
		ax1.spines['bottom'].set_color("#5998ff")
		ax1.spines['top'].set_color("#5998ff")
		ax1.spines['left'].set_color("#5998ff")
		ax1.spines['right'].set_color("#5998ff")
		ax1.tick_params(axis='y', colors='w')
		plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
		ax1.tick_params(axis='x', colors='w')
		plt.ylabel('Stock price and Volume')
		fig.show()

		maLeg = plt.legend(loc=9, ncol=2, prop={'size': 7},
		                   fancybox=True, borderaxespad=0.)
		maLeg.get_frame().set_alpha(0.4)
		textEd = pylab.gca().get_legend().get_texts()
		pylab.setp(textEd[0:5], color='w')

		ax0 = plt.subplot2grid((6, 4), (0, 0), sharex=ax1, rowspan=1, colspan=4)
		rsi = qa.DIFF(daysreshape.close, MA1)
		rsiCol = '#c1f9f7'
		posCol = '#386d13'
		negCol = '#8f2020'

		ax0.plot(daysreshape.DateTime.values[-SP:], rsi[-SP:], rsiCol,
		         linewidth=1.5)
		ax0.axhline(70, color=negCol)
		ax0.axhline(30, color=posCol)
		ax0.fill_between(daysreshape.DateTime.values[-SP:], rsi[-SP:], 70,
		                 where=(rsi[-SP:] >= 70), facecolor=negCol,
		                 edgecolor=negCol, alpha=0.5)
		ax0.fill_between(daysreshape.DateTime.values[-SP:], rsi[-SP:], 30,
		                 where=(rsi[-SP:] <= 30), facecolor=posCol,
		                 edgecolor=posCol, alpha=0.5)
		ax0.set_yticks([30, 70])
		ax0.yaxis.label.set_color("w")
		ax0.spines['bottom'].set_color("#5998ff")
		ax0.spines['top'].set_color("#5998ff")
		ax0.spines['left'].set_color("#5998ff")
		ax0.spines['right'].set_color("#5998ff")
		ax0.tick_params(axis='y', colors='w')
		ax0.tick_params(axis='x', colors='w')
		plt.ylabel('RSI')
