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


def FOURWEEK(data, m=20, n=10):
    ''' 四周规则
    具体规则是：

    当今天的收盘价，大于过去m(默认：20)个交易日中的最高价时，以收盘价买入；
    买入后，当收盘价小于过去n(默认：10)个交易日中的最低价时，以收盘价卖出。

海龟们也永远不会知道一笔交易最后会赚钱还是赔钱。每一笔交易都有可能赚钱，但可能性最大的结果是赔钱。有些交易会得到4R到5R的中等回报，有些则会是12R、20R甚至是30R的大捷。但最终看来，胜利的成果足以弥补失败的损失，我们总会赢利。
像海龟一样思考

    1.重要的是现在：不要对过去念念不忘，也不要去预测未来。前者对你无益，后者是徒劳的。
    2.从概率角度思考问题，不要预测：不要试图作出正确的预测，唯有使用概率对你有利的方法，你才能在长期内获得成功。
    3.对你自己的交易负责：不要把你的错误和失败归咎于其他人、市场、你的经纪人等等。要对自己的错误负责，从錯误中学习。

交易世界是粉碎这个坏习惯的好地方。说到底，交易只是你和市场之间的事，你在市场面前无所隐瞒。如果你做得很好，长期下来你会看到好的结果。如果你做得很糟糕，长期下来你会赔钱。

    :param data:
    :return:
    '''

    def flag(x, preFlag):
        if x['close'] > x['hhigh']:
            preFlag[0] = 1
        elif x['close'] < x['llow']:
            preFlag[0] = -1
        return preFlag[0]

    df = highLow(data, m, n)
    preFlag = [0]
    df['flag'] = df.apply(lambda x:flag(x, preFlag), axis=1);
    return pd.DataFrame({'flag': df['flag']})


def highLow(data, m=20, n=10):
    ''' 计算n周期最高收盘价、最低收盘价

    :param data: dataFrame
    :param n: 计算最高收盘价周期; 默认：20
    :param n: 计算最低收盘价周期; 默认：10
    :return:
    '''
    high = qa.HHV(data['close'], n)
    low = qa.LLV(data['close'], n)
    return pd.DataFrame({'hhigh': high.shift(1), 'llow': low.shift(1), 'close': data.close})
