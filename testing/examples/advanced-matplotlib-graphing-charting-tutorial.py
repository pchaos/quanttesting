# -*- coding: utf-8 -*-
""" YAHOO api已经失效，改用QUANTAXIS
https://pythonprogramming.net/advanced-matplotlib-graphing-charting-tutorial/

@Time    : 2020/1/24 下午6:17

@File    : advanced-matplotlib-graphing-charting-tutorial.py

@author  : pchaos
@license : Copyright(C), yglib
@Contact : p19992003#gmail.com
"""

import urllib.request, urllib.error, urllib.parse
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
# from matplotlib.finance import candlestick_ohlc
from mpl_finance import candlestick_ohlc
import matplotlib
import pylab
import QUANTAXIS as qa

matplotlib.rcParams.update({'font.size': 9})


def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


def movingaverage(values, window):
    weigths = np.repeat(1.0, window) / window
    smas = np.convolve(values, weigths, 'valid')
    return smas  # as a numpy array


def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def graphData(stock, MA1, MA2):
    '''
        Use this to dynamically pull a stock:
    '''
    if stock.upper() == "EXIT" or stock == "0":
        return 1
    elif len(stock) < 6:
        stock = stock.zfill(6)
    try:
        stockFile =[]
        print('Currently Pulling', stock)
        try:
            if len(stock) == 6:
                df = qa.QA_fetch_stock_day_adv(stock, '2017-08-01', '2019-12-31').to_qfq()
            else:
                urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=10y/csv'
                sourceCode = urllib.request.urlopen(urlToVisit).read().decode()
                splitSource = sourceCode.split('\n')
                for eachLine in splitSource:
                    splitLine = eachLine.split(',')
                    if len(splitLine) == 6:
                        if 'values' not in eachLine:
                            stockFile.append(eachLine)
        except Exception as e:
            print(str(e), 'failed to organize pulled data.')
        stockFile = []
    except Exception as e:
        print(str(e), 'failed to pull pricing data')

    _plt(stock, df, MA1, MA2)
    return 0


def _plt(stock, df, MA1, MA2):
    try:
        SP = len(df[MA2 - 1:])
        if SP < MA1:
            raise Exception("未获取道数据，数据长度：{}".format(len(df)))
        dfa = df[-SP:].reset_index()[['date', 'open', 'high', 'low', 'close', 'volume']]
        dfa['date'] = mdates.date2num(
            dfa['date'].dt.date)
        dates = dfa.date.values
        closep = df.close.values
        # dfa.columns = ['date', 'code', 'openp', 'highp', 'lowp', 'closep', 'volume', 'amount','preclose', 'adj']
        Av1 = qa.MA(df.close, MA1).values
        Av2 = qa.MA(df.close, MA2).values

        # SP = len(date[MA2 - 1:])

        fig = plt.figure(facecolor='#07006d')

        # ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, axisbg='#07000d')
        ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
        candlestick_ohlc(ax1, quotes=dfa[['date', 'open', 'close', 'high',
                                          'low']].values, width=.6, colorup='#53c156', colordown='#ff1717')

        Label1 = str(MA1) + ' SMA'
        Label2 = str(MA2) + ' SMA'

        ax1.plot(dates, Av1[-SP:], '#e1edf9', label=Label1, linewidth=1.5)
        ax1.plot(dates, Av2[-SP:], '#4ee6fd', label=Label2, linewidth=1.5)

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
        rsi = rsiFunc(closep)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'

        ax0.plot(dates, rsi[-SP:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(dates, rsi[-SP:], 70, where=(rsi[-SP:] >= 70), facecolor=negCol, edgecolor=negCol,
                         alpha=0.5)
        ax0.fill_between(dates, rsi[-SP:], 30, where=(rsi[-SP:] <= 30), facecolor=posCol, edgecolor=posCol,
                         alpha=0.5)
        ax0.set_yticks([30, 70])
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('RSI')

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
        emaslow, emafast, macd = computeMACD(closep)
        ema9 = ExpMovingAverage(macd, nema)
        ax2.plot(dates, macd[-SP:], color='#4ee6fd', lw=2)
        ax2.plot(dates, ema9[-SP:], color='#e1edf9', lw=1)
        ax2.fill_between(dates, macd[-SP:] - ema9[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

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

        plt.suptitle(stock.upper(), color='w')
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)

        ax1.annotate('Big news!', (dates[510], Av1[510]),
                     xytext=(0.8, 0.9), textcoords='axes fraction',
                     arrowprops=dict(facecolor='white', shrink=0.05),
                     fontsize=14, color='w',
                     horizontalalignment='right', verticalalignment='bottom')

        plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.show()
        time.sleep(5)
        # fig.savefig('example.png', facecolor=fig.get_facecolor())

    except Exception as e:
        print('main loop exception', str(e))


if __name__ == '__main__':
    stock = "23"
    while True:
        if graphData(stock, 10, 50) > 0:
            break
        stock = input('Stock to plot: ')
