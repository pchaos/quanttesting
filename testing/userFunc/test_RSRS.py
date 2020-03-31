# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/27 下午1:03

@File    : test_RSRS.py

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
import scipy.stats as scs
import matplotlib.mlab as mlab
from userFunc import getdata
from userFunc import RSRS1, RSRS2, RSRS3, RSRS4


class testRSRS(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.code = '000300'
        dateStart = datetime.date(2005, 3, 1)
        dateEnd = datetime.date(2017, 3, 31)
        N = 18
        M = 600
        cls.hs300 = getdata(cls.code, dateStart, dateEnd, N, M)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.hs300 is not None:
            cls.hs300 = None

    def test_getdata(self):
        hs300 = self.hs300
        hs300.head()
        VHS300 = hs300.loc[2:]
        HS300 = hs300.reset_index(drop=True)
        print(HS300.head(10))

        # 斜率数据分布
        plt.figure(figsize=(15, 5))
        plt.hist(HS300['beta'], bins=100, range=None,
                 # normed=False,
                 density=False,
                 weights=None, cumulative=False,
                 bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color='r',
                 label='直方图', stacked=False)
        plt.show()

        # RSRS标准分和右偏变准分分布
        plt.figure(figsize=(15, 5))
        plt.hist(HS300['beta_norm'], bins=100, range=None,
                 density=False,
                 weights=None, cumulative=False,
                 bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color='y',
                 label='直方图', stacked=False)
        plt.show()
        plt.figure(figsize=(15, 5))
        plt.hist(HS300['RSRS_R2'], bins=100, range=None,
                 density=False,
                 weights=None, cumulative=False,
                 bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color='g',
                 label='直方图', stacked=False)
        plt.show()

        sta = scs.describe(HS300.beta)
        stew = sta[4]
        kurtosis = sta[5]

        sta1 = scs.describe(HS300.beta_norm)
        stew1 = sta1[4]
        kurtosis1 = sta1[5]

        sta2 = scs.describe(HS300.RSRS_R2)
        stew2 = sta2[4]
        kurtosis2 = sta2[5]

        print('斜率的均值:%s' % (HS300['beta'].mean()))
        print('斜率的标准差:%s' % (HS300['beta'].std()))
        print('斜率的偏度:%s' % (stew))
        print('斜率的峰度:%s' % (kurtosis))
        print('')
        print('斜率标准分的均值:%s' % (HS300['beta_norm'].mean()))
        print('斜率标准分的标准差:%s' % (HS300['beta_norm'].std()))
        print('斜率标准分的偏度:%s' % (stew1))
        print('斜率标准分的峰度:%s' % (kurtosis1))
        print('')
        print('斜率标准分的均值:%s' % (HS300['RSRS_R2'].mean()))
        print('斜率标准分的标准差:%s' % (HS300['RSRS_R2'].std()))
        print('斜率标准分的偏度:%s' % (stew2))
        print('斜率标准分的峰度:%s' % (kurtosis2))

        # 斜率指标过去250天均值曲线
        HS300['beta_mean'] = HS300.beta.rolling(250).mean().shift(1)
        for i in range(250):
            HS300.loc[i, 'beta_mean'] = HS300.loc[:i - 1, 'beta'].mean()
        result = HS300.loc[10:].copy()
        result = result.reset_index(drop=True)
        xtick = np.arange(0, result.shape[0], int(result.shape[0] / 7))
        xticklabel = pd.Series(result.date[xtick])
        # plt.figure(figsize=(15, 3))
        plt.figure(figsize=(15, 4))
        fig = plt.axes()
        plt.plot(np.arange(result.shape[0]), result.beta_mean, linewidth=3, color='black')

        fig.set_xticks(xtick)
        fig.set_xticklabels(xticklabel, rotation=45)
        plt.legend()
        plt.show()

    def test_RSRS1_RSRS4(self):
        code = self.code
        data = self.hs300
        result = RSRS1(data)
        num = result.flag.abs().sum() / 2
        nav = result.nav[result.shape[0] - 1]

        print('交易次数 = ', num)
        print('策略净值为= ', nav)

        xtick = np.arange(0, result.shape[0], int(result.shape[0] / 7))
        xticklabel = pd.Series(result.date[xtick])
        plt.figure(figsize=(15, 4))
        fig = plt.axes()
        plt.plot(np.arange(result.shape[0]), result.nav, label='RSRS1', linewidth=2, color='red')
        plt.plot(np.arange(result.shape[0]), result.close / result.close[0], color='yellow', label='HS300', linewidth=2)

        fig.set_xticks(xtick)
        fig.set_xticklabels(xticklabel, rotation=45)
        plt.legend()
        plt.show()

        result2 = RSRS2(self.hs300)
        num = result2.flag.abs().sum() / 2
        nav = result2.nav[result.shape[0] - 1]
        ret_year = (nav - 1)
        print('交易次数 = ', num)
        print('策略净值为= ', nav)

        result3 = RSRS3(data)
        num = result3.flag.abs().sum() / 2
        nav = result3.nav[result.shape[0] - 1]
        ret_year = (nav - 1)
        print('交易次数 = ', num)
        print('策略净值为= ', nav)

        dateStart = datetime.date(2005, 3, 1)
        dateEnd = datetime.date(2017, 3, 31)
        N = 16
        M = 300
        HS300 = getdata(code, dateStart, dateEnd, N, M)
        HS300 = HS300.loc[2:]
        HS300 = HS300.reset_index(drop=True)

        result4 = RSRS4(self.hs300)
        num = result4.flag.abs().sum() / 2
        nav = result4.nav[result.shape[0] - 1]
        ret_year = (nav - 1)
        print('交易次数 = ', num)
        print('策略净值为= ', nav)

        xtick = np.arange(0, result.shape[0], int(result.shape[0] / 7))
        xticklabel = pd.Series(result.date[xtick])
        plt.figure(figsize=(15, 3))
        fig = plt.axes()
        plt.plot(np.arange(result.shape[0]), result.nav, label='RSRS1', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result2.nav, label='RSRS2', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result3.nav, label='RSRS3', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result4.nav, label='RSRS4', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result.close / result.close[0], color='yellow', label='HS300', linewidth=2)

        fig.set_xticks(xtick)
        fig.set_xticklabels(xticklabel, rotation=45)
        plt.legend()
        plt.show()

    def test_RSRS_recent(self):
        # 四种策略时间更新到当前
        code = self.code
        dateStart = datetime.date(2005, 3, 1)
        dateEnd = datetime.date(2019, 12, 31)
        dateEnd = datetime.date(2020, 3, 20)
        self._RSRS(code, dateStart, dateEnd)

    def _RSRS(self, code, dateStart, dateEnd, label=""):
        N = 18
        M = 600
        rsrsDara = getdata(code, dateStart, dateEnd, N, M)
        rsrsDara = rsrsDara.loc[2:]
        rsrsDara = rsrsDara.reset_index(drop=True)
        rsrsDara.head()
        # 斜率指标策略
        result = RSRS1(rsrsDara)
        num = result.flag.abs().sum() / 2
        nav = result.nav[result.shape[0] - 1]
        print('交易次数 = ', num)
        print('策略净值为= ', nav)
        # 标准分策略
        result2 = RSRS2(rsrsDara)
        num = result2.flag.abs().sum() / 2
        nav = result2.nav[result.shape[0] - 1]
        ret_year = (nav - 1)
        print('交易次数 = ', num)
        print('策略净值为= ', nav)
        # 修正标准分策略
        result3 = RSRS3(rsrsDara)
        num = result3.flag.abs().sum() / 2
        nav = result3.nav[result.shape[0] - 1]
        ret_year = (nav - 1)
        print('交易次数 = ', num)
        print('策略净值为= ', nav)
        N = 16
        M = 300
        rsrsDara = getdata(code, dateStart, dateEnd, N, M)
        rsrsDara = rsrsDara.loc[2:]
        rsrsDara = rsrsDara.reset_index(drop=True)
        rsrsDara.head()
        result4 = RSRS4(rsrsDara)
        num = result4.flag.abs().sum() / 2
        nav = result4.nav[result.shape[0] - 1]
        ret_year = (nav - 1)
        print('交易次数 = ', num)
        print('策略净值为= ', nav)
        xtick = np.arange(0, result.shape[0], int(result.shape[0] / 7))
        xticklabel = pd.Series(result.date[xtick])
        plt.figure(figsize=(25, 8))
        fig = plt.axes()
        plt.plot(np.arange(result.shape[0]), result.nav, label='RSRS1', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result2.nav, label='RSRS2', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result3.nav, label='RSRS3', linewidth=2)
        plt.plot(np.arange(result.shape[0]), result4.nav, label='RSRS4', linewidth=1)
        plt.plot(np.arange(result.shape[0]), result.close / result.close[0], color='yellow', label=label, linewidth=1.5)
        fig.set_xticks(xtick)
        fig.set_xticklabels(xticklabel, rotation=25)
        plt.legend()
        plt.show()

    def test_RSRS_recent(self):
        # 四种策略时间更新到当前
        code = '399001'
        code = '000016'
        code = '399975'
        code = '399006'
        code = '399673'
        code = '399989'  # 中证医疗
        code = '399932'  # 中证消费
        code = '399986'  # 中证银行
        code = '880952'  # 中证银行

        dateStart = datetime.date(2005, 3, 1)
        # dateEnd = datetime.date(2019, 12, 31)
        # dateEnd = datetime.date(2020, 3, 20)
        dateEnd = datetime.datetime.now().date()
        self._RSRS(code, dateStart, dateEnd, label=code)


if __name__ == '__main__':
    unittest.main()