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
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import pylab

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


def pltFourWeek(title, qadata, n1, n2, delaySeconds=5):
    """画四周指标
    Param: title 图片标题
        qadata 股票数据

    """
    try:
        SP = len(qadata[n2 - 1:])
        if SP < n1:
            raise Exception("未获取道数据，数据长度：{}".format(len(qadata)))
        dfa = qadata[-SP:].reset_index()[['date', 'open', 'high', 'low', 'close', 'volume']]
        dfa['date'] = mdates.date2num(
            dfa['date'].dt.date)
        dates = dfa.date.values
        Av1 = qa.MA(qadata.close, n1).values
        Av2 = qa.MA(qadata.close, n2).values

        # SP = len(date[MA2 - 1:])

        fig = plt.figure(figsize=(22, 15), facecolor='#07006d')

        # ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, axisbg='#07000d')
        ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
        candlestick_ohlc(ax1, quotes=dfa[['date', 'open', 'close', 'high',
                                          'low']].values, width=0.3, colorup='g', colordown='r')

        Label1 = str(n1) + ' SMA'
        Label2 = str(n2) + ' SMA'

        ax1.plot(dates, Av1[-SP:], '#e1edf9', label=Label1, linewidth=1.)
        ax1.plot(dates, Av2[-SP:], '#4ee6fd', label=Label2, linewidth=1.)

        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price and Volume')

        maLeg = plt.legend(loc=9, ncol=2, prop={'size': 7},
                           fancybox=True, borderaxespad=0.)
        maLeg.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color='w')

        volumeMin = 0

        # ax0 = plt.subplot2grid((6, 4), (0, 0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        ax0 = plt.subplot2grid((6, 4), (0, 0), sharex=ax1, rowspan=1, colspan=4)
        fourweek = qadata.add_func(FOURWEEK)
        fwCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'

        ax0.plot(dates, fourweek[-SP:], fwCol, linewidth=1.0)
        # ax0.axhline(70, color=negCol)
        # ax0.axhline(30, color=posCol)
        # ax0.fill_between(dates, fourweek[-SP:], 70, where=(fourweek[-SP:] > 0), facecolor=negCol, edgecolor=negCol,
        #                  alpha=0.5)
        # ax0.fill_between(dates, fourweek[-SP:], 30, where=(fourweek[-SP:] < 0), facecolor=posCol, edgecolor=posCol,
        #                  alpha=0.5)
        # ax0.set_yticks([30, 70])
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('FourWeek')

        ax1v = ax1.twinx()
        ax1v.fill_between(dates, volumeMin, dfa.volume.values, facecolor='#00ffe8', alpha=.4)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.grid(False)
        ###Edit this to 3, so it's a bit larger
        ax1v.set_ylim(0, 3 * dfa.volume.max())
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')
        # ax2 = plt.subplot2grid((6, 4), (5, 0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        ax2 = plt.subplot2grid((6, 4), (5, 0), sharex=ax1, rowspan=1, colspan=4)
        fillcolor = '#00ffe8'
        nslow = 26
        nfast = 12
        nema = 9
        macd = qa.MACD(qadata.close,nfast, nslow, nema)['MACD']
        ema9 = qa.EMA(macd, nema)
        ax2.plot(dates, macd[-SP:], color='#4ee6fd', lw=2)
        ax2.plot(dates, ema9[-SP:], color='#e1edf9', lw=1)
        ax2.fill_between(dates, macd.values[-SP:] - ema9.values[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel('MACD', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        plt.suptitle(title.upper(), color='w')
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)

        # ax1.annotate('Big news!', (dates[210], Av1[210]),
        #              xytext=(0.8, 0.9), textcoords='axes fraction',
        #              arrowprops=dict(facecolor='yellow', shrink=0.05),
        #              fontsize=14, color='w',
        #              horizontalalignment='right', verticalalignment='bottom')

        plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.show()
        time.sleep(delaySeconds)
        # fig.savefig('example.png', facecolor=fig.get_facecolor())

    except Exception as e:
        print('main loop exception', str(e))
