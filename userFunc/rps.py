# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/28 下午7:11

@File    : rps.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""


# 计算收益率
def cal_ret(dataFrame, *args, **kwargs):
    '''计算收益率
    days:周 5;月:20;半年：120; 一年:250
    '''
    if len(args) == 0:
        args = tuple([20])
    close = dataFrame.close
    colName ='MARKUP'
    cols =[]
    for num in args:
        coln = '{}{}'.format(colName, num)
        dataFrame[coln] = close / close.shift(num)
        cols.append(coln)
    # return dataFrame.iloc[-max(args):, :].fillna(0)
    return dataFrame[cols].iloc[-max(args):, :]

