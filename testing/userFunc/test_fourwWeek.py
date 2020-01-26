# -*- coding: utf-8 -*-
"""四周规则及相关测试

@Time    : 2020/1/26 下午7:04

@File    : test_fourwWeek.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
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


class TestFOURWEEK(TestCase):

    def test_FOURWEEK(self):
        code = '000001'
        days = 600
        m, n = 20, 10
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(10)
        data = qa.QA_fetch_index_day_adv(code, start, end)
        # print(data.data.columns, type(data.data))
        dfind = data.add_func(FOURWEEK, m, n)
        self.assertTrue(len(dfind) > 0, '指标个数为零')
        if days > 300:
            # 出现标志的个数大于零
            self.assertTrue(len(dfind) > len(dfind[dfind['flag'] == 1]) > 0, '指标个数为零')
            self.assertTrue(len(dfind) == len(dfind[dfind['flag'] == 1]) + len(dfind[dfind['flag'] == -1]) + len(
                dfind[dfind['flag'] == 0]), '指标个数不匹配')
        print(dfind.iloc[-1])

    def test_FOURWEEK_plot(self):
        code = '000300'
        days = 600
        m, n = 20, 10
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(10)
        # 获取指数数据
        data = qa.QA_fetch_index_day_adv(code, start, end)
        pltFourWeek(code, data, m, n)


if __name__ == '__main__':
    unittest.main()
