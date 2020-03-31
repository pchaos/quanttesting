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

标准分=(观察分−均值)/标准差

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
            hs300.loc[i, 'beta_norm'] = (hs300.loc[i, 'beta'] - hs300.loc[:i - 1, 'beta'].mean()) / betastd
    hs300.loc[2, 'beta_norm'] = 0
    hs300['RSRS_R2'] = hs300.beta_norm * hs300.R2
    hs300 = hs300.fillna(0)

    # 右偏标准分
    hs300['beta_right'] = hs300.RSRS_R2 * hs300.beta
    return (hs300)


def RSRS1(dataFame, Sbuy=1.0, Ssell=0.8):
    """斜率指标交易策略
    """
    data = dataFame.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'beta'] > Sbuy and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'beta'] < Ssell and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    # cumprod 累乘
    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


def RSRS2(dataFrame, Sbuy=0.7, Ssell=-0.7):
    """标准分策略
    """
    data = dataFrame.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'beta_norm'] > Sbuy and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'beta_norm'] < Ssell and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


def RSRS3(dataFrame, Sbuy=0.7, Ssell=-0.7):
    """修正标准分策略
    """
    data = dataFrame.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓标准分策略：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'RSRS_R2'] > Sbuy and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'RSRS_R2'] < Ssell and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)


def RSRS4(dataFrame, Sbuy=0.7, Ssell=-0.7):
    """右偏标准分策略
    """
    data = dataFrame.copy()
    data['flag'] = 0  # 买卖标记
    data['position'] = 0  # 持仓标记
    position = 0  # 是否持仓，持仓：1，不持仓：0
    for i in range(1, data.shape[0] - 1):

        # 开仓
        if data.loc[i, 'beta_right'] > Sbuy and position == 0:
            data.loc[i, 'flag'] = 1
            data.loc[i + 1, 'position'] = 1
            position = 1
        # 平仓
        elif data.loc[i, 'beta_right'] < Ssell and position == 1:
            data.loc[i, 'flag'] = -1
            data.loc[i + 1, 'position'] = 0
            position = 0

        # 保持
        else:
            data.loc[i + 1, 'position'] = data.loc[i, 'position']

    data['nav'] = (1 + data.close.pct_change(1).fillna(0) * data.position).cumprod()

    return (data)
