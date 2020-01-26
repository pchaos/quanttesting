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
import unittest
from userFunc import *
import datetime
import os
import QUANTAXIS as qa
import matplotlib.pyplot as plt
import talib as ta
import pandas as pd
from userFunc import getCodeList


def read_zxg(fname='zxg.txt'):
    """读取自选股列表
    """
    try:
        # 当前目录
        dir_path = os.path.dirname(os.path.realpath(__file__))
    except:
        dir_path = os.path.dirname(os.path.realpath("./"))
    if not fname.find(os.sep) > -1:
        # 如果文件名（fname）没有目录，则加上当前目录
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
    data = qa.QA_fetch_index_day_adv(stockcode, sday, eday).data

    # Wash data
    # returndata = returndata.sort_index()
    # returndata.index.name = 'DateTime'
    data.drop('amount', axis=1, inplace=True)
    return data[['open', 'high', 'close', 'low', 'volume']]


class TestCHCOUNTS(TestCase):
    def test_CHCOUNTS(self):
        code = '000001'
        df = qa.QA_fetch_stock_day_adv(code)
        print(df.data.columns, type(df.data))
        chCounts = df.to_qfq().add_func(CHCOUNTS)
        self.assertTrue(len(chCounts) > 0, '指标为零')
        self.assertFalse(
            len(chCounts['chCounts'] > 5) > len(chCounts['chCounts'] > 8))
        self.assertTrue(len(chCounts[chCounts['chCounts'] > 8]) == 0, '缠中说禅均线强度最多为8')
        self.assertTrue(len(chCounts[chCounts['chCounts'] < 0]) == 0, '缠中说禅均线强度最少为0')
        self.assertTrue(len(chCounts) == len(
            (chCounts['chCounts'] < 9) & (chCounts['chCounts'] >= 0)),
                        '0 <= 缠中说禅均线强度 < 9')
        print(chCounts)

    def test_CHCOUNTS2(self):
        code = '000001'
        df = qa.QA_fetch_stock_day_adv(code)
        print(df.data.columns, type(df.data))
        data = df.to_qfq()
        chCounts = data.add_func(CHCOUNTS)
        chCounts2 = data.add_func(CHCOUNTS2)
        self.assertTrue(len(chCounts2) > 0, '指标为零')
        self.assertTrue(chCounts.equals(chCounts2), '两种方式返回结果不相等')

    # print(chCounts2)

    def test_CHCOUNTS3(self):
        code = '000001'
        data = qa.QA_fetch_stock_day_adv(code).to_qfq()
        chCounts, chCounts2 = self.__checkIndicator(data)
        diffs = self.diffOneByOne(chCounts, chCounts2)
        self.assertTrue(chCounts.equals(chCounts2), '两种方式返回结果不相等 {}'.format(diffs))

    def __checkIndicator(self, df):
        print(df.data.columns, type(df.data))
        chCounts = df.add_func(CHCOUNTS)
        chc = qa.QA_DataStruct_Indicators(chCounts)
        chCounts2 = df.add_func(CHCOUNTS3)
        chc2 = qa.QA_DataStruct_Indicators(chCounts2)
        self.assertTrue(len(chCounts2) > 0, '指标为零')
        self.assertTrue(len(chCounts2) == len(chCounts), '计算结果个数不同')
        return chCounts, chCounts2

    def test_CHCOUNTS3_codelist(self):
        code = getCodeList(count=10, isTesting=False)
        df = qa.QA_fetch_stock_day_adv(code).to_qfq()
        chCounts, chCounts2 = self.__checkIndicator(df)
        diffs = self.diffOneByOne(chCounts, chCounts2)
        self.assertTrue(chCounts.equals(chCounts2), '两种方式返回结果不相等 {}'.format(diffs))

    def diffOneByOne(self, chCounts, chCounts2):
        oneByOne = []
        # 逐个比较，判断哪一天不匹配
        for i in range(len(chCounts)):
            if chCounts.chCounts[i] != chCounts2.chCounts[i]:
                # print(chCounts.chCounts[i], chCounts2.chCounts[i])
                oneByOne.append([{"比较顺序": i}, chCounts.chCounts[i], chCounts2.chCounts[i]])
        return oneByOne

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

    def _test_index_day_adv(self, code, start, end):
        df = qa.QA_fetch_index_day_adv(code, start, end)
        self.assertTrue(len(df.code) == len(code),
                        '有未获取到的代码 {} {}, {}:{}'.format(df.code, code,
                                                       len(df.code), len(code)))
        chCounts = df.add_func(CHCOUNTS)
        self.assertTrue(len(chCounts) > 0, '指标为零')
        # print(chCounts)
        return chCounts

    def test_CHCOUNTS_indexlist(self):
        '''
        :return:
                                   chCounts
            date       code
            2018-10-08 000016         0
                       399001         0
                       399004         0
                       399005         0
            2018-10-09 000016         0
                       399001         0
                       399004         0
                       399005         0
            2018-10-10 000016         0
                       399001         0
                       399004         0
                       399005         0

        '''
        # code列表
        code = read_zxg()
        start = datetime.datetime.now() - datetime.timedelta(300)
        end = datetime.datetime.now() - datetime.timedelta(10)
        self._test_index_day_adv(code, start, end)

    def test_CHCOUNTS_std(self):
        # code列表
        code = read_zxg()
        start = datetime.datetime.now() - datetime.timedelta(300)
        end = datetime.datetime.now() - datetime.timedelta(10)
        chcounts = self._test_index_day_adv(code, start, end)
        chcounts.groupby('date').mean()
        chcounts.groupby('date').agg('std')
        chcounts.agg('std')
        print("type chcounts.groupby('date').agg('std')): {}".format(
            type(chcounts.groupby('date').agg('std'))))
        print("type chcounts.agg('std')): {}".format(type(chcounts.agg('std'))))
        chcounts.reset_index(inplace=True)
        dd = chcounts
        chcounts.set_index('date', inplace=True)

        chcountsstd = chcounts.groupby('date').agg('std')['chCounts']
        for d in chcountsstd.index[-5:]:
            df1 = chcounts.chCounts.loc[d] > chcounts.chCounts.loc[d].mean() + \
                  chcountsstd.loc[d]
            df1 = chcounts.chCounts.loc[d] > chcounts.chCounts.loc[d].mean() + \
                  chcountsstd.loc[d]
            # df1.columns = [['TF']]
            df2 = chcounts.chCounts.loc[d]
            # df2.columns = [['chCouints']]
            df = pd.concat([df1, df2], axis=1)
            df.columns = [['TF', 'chCounts']]
            print(pd.concat([df1, df2], axis=1))
            # 当天各指数缠中说禅均质平均值+STD
            stdHigh = df[chcounts.chCounts.loc[d] >
                         chcounts.chCounts.loc[d].mean() +
                         chcountsstd.loc[d]]
            self.assertTrue(len(df) > 3 * len(stdHigh),
                            '当天各指数个数/len(当天各指数缠中说禅均质平均值+STD) > 3')

    def test_readstkData(self):
        # https://zhuanlan.zhihu.com/p/29519040
        from matplotlib import dates as mdates
        import mpl_finance as mpf
        from mpl_finance import candlestick_ohlc
        from matplotlib import ticker as mticker
        import numpy as np
        import pylab
        from matplotlib.pylab import date2num

        def format_date(x, pos):
            # 处理所有的节假日包括周末，在这里都会显示为空白
            if x < 0 or x > len(date_tickers) - 1:
                return ''
            return date_tickers[int(x)].strftime('%y-%m-%d')

        code = ['399004']
        MA1 = 10
        MA2 = 50
        start = datetime.datetime.now() - datetime.timedelta(300)
        end = datetime.datetime.now() - datetime.timedelta(10)
        days = readstkData(code, start, end)
        # print(days)
        daysreshape = days.reset_index()
        daysreshape['DateTime'] = daysreshape['date'].dt.date
        daysreshape['DateTime2'] = mdates.date2num(
            daysreshape['DateTime'])
        daysreshape.drop('volume', axis=1, inplace=True)
        daysreshape.drop('date', axis=1, inplace=True)
        # print(daysreshape)
        daysreshape = daysreshape.reindex(
            columns=['DateTime', 'open', 'high', 'low', 'close'])
        daysreshape['dates'] = np.arange(0, len(daysreshape))

        date_tickers = daysreshape.DateTime

        # 汉字
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']

        Av1 = qa.MA(daysreshape.close, MA1)
        Av2 = qa.MA(daysreshape.close, MA2)
        SP = len(daysreshape.DateTime.values[MA2 - 1:])
        fig = plt.figure(facecolor='#07000d', figsize=(15, 10))

        # plt.style.use('dark_background')
        # ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
        ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4,
                               facecolor='#07000d')
        candlestick_ohlc(ax1, quotes=daysreshape[
                                         ['dates', 'open', 'close', 'high',
                                          'low']].values[-SP:], width=.7,
                         colorup='r', colordown='g', alpha=0.7)
        # colorup='#ff1717', colordown='#53c156')
        ax1.set_title('指数k线', fontsize=20);

        Label1 = str(MA1) + ' SMA'
        Label2 = str(MA2) + ' SMA'

        dates = daysreshape['dates']
        ax1.plot(dates.values[-SP:], Av1[-SP:], '#e1edf9',
                 label=Label1, linewidth=1.5)
        ax1.plot(dates.values[-SP:], Av2[-SP:], '#4ee6fd',
                 label=Label2, linewidth=1.5)
        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(20))
        # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
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

    # maLeg = plt.legend(loc=9, ncol=2, prop={'size': 7},
    #                    fancybox=True, borderaxespad=0.)
    # maLeg.get_frame().set_alpha(0.4)
    # textEd = pylab.gca().get_legend().get_texts()
    # pylab.setp(textEd[0:5], color='w')

    # ax0 = plt.subplot2grid((6, 4), (0, 0), sharex=ax1, rowspan=1, colspan=4)
    # rsi = ta.RSI(daysreshape.close.values, MA1)
    # rsiCol = '#c1f9f7'
    # posCol = '#386d13'
    # negCol = '#8f2020'
    #
    # ax0.plot(days.values[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
    # ax0.axhline(70, color=negCol)
    # ax0.axhline(30, color=posCol)
    # ax0.fill_between(dates.values[-SP:], rsi[-SP:], 70,
    #                  where=(rsi[-SP:] >= 70), facecolor=negCol,
    #                  edgecolor=negCol, alpha=0.5)
    # ax0.fill_between(dates.values[-SP:], rsi[-SP:], 30,
    #                  where=(rsi[-SP:] <= 30), facecolor=posCol,
    #                  edgecolor=posCol, alpha=0.5)
    # ax0.set_yticks([30, 70])
    # ax0.yaxis.label.set_color("w")
    # ax0.spines['bottom'].set_color("#5998ff")
    # ax0.spines['top'].set_color("#5998ff")
    # ax0.spines['left'].set_color("#5998ff")
    # ax0.spines['right'].set_color("#5998ff")
    # ax0.tick_params(axis='y', colors='w')
    # ax0.tick_params(axis='x', colors='w')
    # plt.ylabel('RSI')
    # fig.show()

if __name__ == '__main__':
    unittest.main()
