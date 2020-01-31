# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/28 下午7:11

@File    : rps.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import pandas as pd


# 计算收益率
def cal_ret(dataFrame, *args, **kwargs):
    '''计算收益率
    days:周 5;月:20;半年：120; 一年:250
    '''
    if len(args) == 0:
        args = tuple([20])
    close = dataFrame.close
    colName = 'MARKUP'
    cols = []
    for num in args:
        coln = '{}{}'.format(colName, num)
        dataFrame[coln] = close / close.shift(num)
        cols.append(coln)
    # return dataFrame.iloc[-max(args):, :].fillna(0)
    return dataFrame[cols].iloc[max(args):, :]


# 计算RPS
def get_RPS(dataFrame, *args, **kwargs):
    i = 0
    # print("日期：{} 数量：{}".format(dataFrame.index.get_level_values(0)[0], len(dataFrame)))
    for col in dataFrame.columns:
        newcol = col.replace("MARKUP", "RPS", 1)
        if i > 0:
            df2= getSingleRPS(dataFrame, col, newcol)
            df[newcol] = df2[newcol]
        else:
            df = getSingleRPS(dataFrame, col, newcol)
        i += 1
    return df


def getSingleRPS(dataFrame, col, newcol):
    df = pd.DataFrame(dataFrame[col].sort_values(ascending=False).dropna())
    dfcount = len(df)
    # range间隔-100.，这样就不用乘以100%了
    df['n'] = range(dfcount * 100, 0, -100)
    df[newcol] = df['n'] / dfcount
    # 删除index date
    return df.reset_index().set_index(['code'])[[newcol]]
