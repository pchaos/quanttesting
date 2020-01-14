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
        #  收盘价站上均线
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


def CHCOUNTS3(data):
    """ 均线强弱

    （和CHCOUNTS返回结果相同）
    :param data:
    :return:
    """
    nlist = [5, 13, 21, 34, 55, 89, 144, 233]
    close = data.close
    dict = {'MA{}'.format(n): close >= qa.MA(data.close, n) for n in nlist}
    return pd.DataFrame({'chCounts': pd.DataFrame(dict).sum(axis=1)})


class CHCOUNT():
    _counts = 0


def FOURWEEK(data):
    ''' 四周规则

    :param data:
    :return:
    '''
    weeks = [20, 10]
    high = qa.HHV(data['close'], weeks[0])
    low = qa.LLV(data['close'], weeks[0])
    return pd.DataFrame({'high': high.shift(1), 'low': low.shift(1)})
