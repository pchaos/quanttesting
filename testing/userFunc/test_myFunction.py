# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/10 上午12:18

@File    : test_myFunction.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
from unittest import TestCase
import pandas as pd
import os
import datetime
import numpy as np
import statsmodels.formula.api as sml
import matplotlib.pyplot as plt
import QUANTAXIS as qa
from userFunc import qaTestingBase, CMI, RSV
from userFunc import fourWeek, TBSIndicator, TBSMonthIndicator


class testMyFunction(qaTestingBase):
    def test_cmi(self):
        cmi = CMI(self.dataFrame)
        self.assertTrue(len(cmi) > 0)
        self.assertTrue(len(cmi[cmi['CMI'] > 100]) == 0, "CMI数值介于0～100之间")
        self.assertTrue(len(cmi[cmi['CMI'] < 0]) == 0, "CMI数值介于0～100之间")
        print(cmi.tail(10))

    def test_RSV(self):
        alg = RSV(self.dataFrame)
        self.assertTrue(len(alg) > 0)
        self.assertTrue(len(alg[alg['RSV'] > 100]) == 0, "RSV数值介于0～100之间")
        self.assertTrue(len(alg[alg['RSV'] < 0]) == 0, "RSV数值介于0～100之间")
        print(alg.tail(10))
        print(alg[alg['RSV'] > 80])

    def test_fourWeek(self):
        code = '000001'
        days = 600
        m, n = 20, 10
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(1)
        data = qa.QA_fetch_index_day_adv(code, start, end)
        # print(data.data.columns, type(data.data))
        dfind = data.add_func(fourWeek, m, n)
        self.assertTrue(len(dfind) > 0, '指标个数为零')
        if days > 300:
            # 出现标志的个数大于零
            self.assertTrue(len(dfind) > len(dfind[dfind['flag'] == 1]) > 0, '指标个数为零')
            self.assertTrue(len(dfind) == len(dfind[dfind['flag'] == 1]) + len(dfind[dfind['flag'] == -1]) + len(
                dfind[dfind['flag'] == 0]), '指标个数不匹配')
        print(dfind.iloc[-1])
        # 指标变向
        print(dfind[dfind.shift(1)['flag'] != dfind['flag']].iloc[-30:])

    def test_taoboshiIndicator(self):
        """ 陶博士中期信号 ???
        2019-01-18 399006     1
        2019-04-26 399006    -1
        2019-06-21 399006     1
        2019-08-09 399006    -1
        2019-08-16 399006     1
        2019-09-27 399006    -1
        2019-10-25 399006     1
        2019-11-15 399006    -1
        2019-12-06 399006     1
        2020-03-13 399006    -1
        """
        code = '399006'  # 创业板指数
        # code = '000001'  # 上证指数
        # code = '399001' # 深证指数
        # code = '399106' # 深证综指
        days = 750
        m, n, maday = 20, 20, 50
        self._taoboshiIndicator(code, days, m, n, maday, resample='d')
        m, n, maday = 4, 4, 10
        self._taoboshiIndicator(code, days, m, n, maday, resample='w')

    def _taoboshiIndicator(self, code, days, m, n, maday=None, resample='d', indicator=TBSIndicator):
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(1)
        data = qa.QA_fetch_index_day_adv(code, start, end)
        if resample.upper() == 'W':
            # 转换为周线数据
            data = qa.QA_DataStruct_Day(data.week)
        elif resample.upper() == 'M':
            data = qa.QA_DataStruct_Day(data.month)
        if not maday:
            dfind = data.add_func(indicator, m, n)
        else:
            dfind = data.add_func(indicator, m, n, maday)
        self.assertTrue(len(dfind) > 0, '指标个数为零')
        if days > 300:
            # 出现标志的个数大于零
            self.assertTrue(len(dfind) > len(dfind[dfind['flag'] == 1]) > 0, '指标个数为零')
            self.assertTrue(len(dfind) == len(dfind[dfind['flag'] == 1]) + len(dfind[dfind['flag'] == -1]) + len(
                dfind[dfind['flag'] == 0]), '指标个数不匹配')
        print(dfind.iloc[-1])
        # 指标变向
        print(dfind[dfind.shift(1)['flag'] != dfind['flag']].iloc[-30:])

    def test_TBSMonthIndicator(self):
        """"""
        code = '399006'  # 创业板指数
        # code = '000001'  # 上证指数
        # code = '399001' # 深证指数
        code = '399106' # 深证综指
        days = 13650
        m, n = 10, 20
        self._taoboshiIndicator(code, days, m,  n,  resample='m', indicator=TBSMonthIndicator)


if __name__ == '__main__':
    unittest.main()
