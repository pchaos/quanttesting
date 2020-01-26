# -*- coding: utf-8 -*-
"""使用Python画精美的股票K线图（含均线）
https://www.toutiao.com/i6733183318239478280/

@Time    : 2020/1/26 下午1:15

@File    : matplotlib_lib.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

# 先引入后面分析、可视化等可能用到的库
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
# df是使用tushare获取的沪深300数据
from matplotlib.gridspec import GridSpec
# 要重新安装 mpl_finance 代替matplotlib.finance才能用
import mpl_finance as mpf
import matplotlib.ticker as ticker
from matplotlib.pylab import date2num
import seaborn as sns
import time

# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
import tushare as ts
import QUANTAXIS as qa


# 代码和数据获取
def get_data(code, start='20190101', end='20190712'):
    # df=ts.pro_bar(ts_code=code,asset='I',adj='qfq', start_date=start, end_date=end)
    df = qa.QA_fetch_stock_day_adv(code, start=start, end=end).to_qfq()
    return df


# 设定日期格式
def format_date(x, pos):
    global date_tickers
    if x < 0 or x > len(date_tickers) - 1:
        return ''
    return date_tickers[int(x)]


def showall(df):
    # 提取原始日期格式
    df['dates'] = np.arange(0, len(df))
    df = df.reset_index()
    df['date2'] = df['date'].copy()
    df['date'] = df['date'].map(date2num)
    global date_tickers
    date_tickers = (df.date2).apply(lambda x: x.strftime('%Y%m%d')).values
    # 画子图
    figure = plt.figure(figsize=(12, 9))
    gs = GridSpec(3, 1)
    ax1 = plt.subplot(gs[:2, :])
    ax2 = plt.subplot(gs[2, :])
    # 画K线图
    mpf.candlestick_ochl(
        ax=ax1,
        quotes=df[['dates', 'open', 'close', 'high', 'low']].values,
        width=0.7,
        colorup='r',
        colordown='g',
        alpha=0.7)
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    # 画均线，均线可使用talib来计算
    for ma in ['5', '20', '30', '60', '120']:
        df[ma] = df.close.rolling(int(ma)).mean()
        ax1.plot(df['dates'], df[ma])
    ax1.legend()
    ax1.set_title('沪深300指数K线图', fontsize=15)
    ax1.set_ylabel('指数')
    # 画成交量
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    df['up'] = df.apply(lambda row: 1 if row['close'] >= row['open'] else 0, axis=1)
    ax2.bar(df.query('up == 1')['dates'], df.query('up == 1')['vol'], color='r', alpha=0.7)
    ax2.bar(df.query('up == 0')['dates'], df.query('up == 0')['vol'], color='g', alpha=0.7)
    ax2.set_ylabel('成交量')
    plt.show()
    time.sleep(2)


if __name__ == '__main__':
    date_tickers = None
    start, end = '2019-01-01', '2019-07-12'
    code = '000300'
    data = qa.QA_fetch_index_day_adv(code, start=start, end=end)
    df = data.data.reset_index().set_index(['date'])
    df = df.sort_index()[['open', 'close', 'high', 'low', 'vol']]
    print(df.head())
    # sns.set()
    df[['open', 'close', 'high', 'low']].plot(figsize=(12, 5))
    plt.title('沪深300指数', size=15)
    plt.show()
    time.sleep(2)

    showall(df)
