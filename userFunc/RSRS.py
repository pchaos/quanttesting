# -*- coding: utf-8 -*-
"""RSRS(阻力支撑相对强度)择时策略
https://zhuanlan.zhihu.com/p/33501881

@Time    : 2020/3/26 下午3:27

@File    : RSRS.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

import pandas as pd
import os
import datetime
import numpy as np
import statsmodels.formula.api as sml
import matplotlib.pyplot as plt
import QUANTAXIS as qa
import tushare as ts
import scipy.stats as scs
import matplotlib.mlab as mlab


def getdata(code, dateStart, dateEnd, N: int, M: int):
    """N：回归的时间长度，同研报
M：算标准分的实际长度，同研报
"""
    hs300 = qa.QA_fetch_index_day_adv(code, start=dateStart, end=dateEnd)
    hs300 = hs300.data[['date_stamp', 'high', 'low', 'open', 'close']].reset_index()

    # 斜率
    hs300['beta'] = 0
    hs300['R2'] = 0
    for i in range(1, len(hs300) - 1):
        df_ne = hs300.loc[i - N + 1:i, :]
        model = sml.ols(formula='high~low', data=df_ne)
        result = model.fit()

        hs300.loc[i + 1, 'beta'] = result.params[1]
        hs300.loc[i + 1, 'R2'] = result.rsquared
    # 日收益率
    hs300['ret'] = hs300.close.pct_change(1)

    # 标准分
    hs300['beta_norm'] = (hs300['beta'] - hs300.beta.rolling(M).mean().shift(1)) / hs300.beta.rolling(M).std().shift(1)
    for i in range(M):
        betastd = hs300.loc[:i - 1, 'beta'].std()
        if betastd == 0:
            hs300.loc[i, 'beta_norm'] = 0
        else:
            hs300.loc[i, 'beta_norm'] = (hs300.loc[i, 'beta'] - hs300.loc[:i - 1, 'beta'].mean()) / hs300.loc[:i - 1,
                                                                                                    'beta'].std()
    hs300.loc[2, 'beta_norm'] = 0
    hs300['RSRS_R2'] = hs300.beta_norm * hs300.R2
    hs300 = hs300.fillna(0)

    # 右偏标准分
    hs300['beta_right'] = hs300.RSRS_R2 * hs300.beta
    return (hs300)


def RSRS1(HS300, S1=1.0, S2=0.8):
    data = HS300.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'beta'] > S1 and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'beta'] < S2 and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


def RSRS2(HS300, S=0.7):
    """标准分策略
    """
    data = HS300.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'beta_norm'] > S and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'beta_norm'] < -S and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


def RSRS3(HS300, S=0.7):
    """修正标准分策略
    """
    data = HS300.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'RSRS_R2'] > S and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'RSRS_R2'] < -S and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


def RSRS4(HS300, S=0.7):
    """右偏标准分策略
    """
    data = HS300.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'beta_right'] > S and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'beta_right'] < -S and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


if __name__ == '__main__':
    pass