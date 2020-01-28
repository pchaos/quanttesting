# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/27 下午8:20

@File    : RPS_demo.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

import time
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt

# 正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

token = 'd70bc77d70657f395ec8700c06bca462f9c3293fd4f34afd3be91995'
ts.set_token(token)
pro = ts.pro_api()

df = pro.stock_basic(exchange='', list_status='L',
                     fields='ts_code,symbol,name,area,industry,list_date')
print(len(df))

# 排除掉新股次新股，这里是只考虑2017年1月1日以前上市的股票
df = df[df['list_date'].apply(int).values < 20170101]
len(df)

codes = df.ts_code.values
names = df.name.values
# 构建一个字典方便调用
stockNum=200
# code_name = dict(zip(names, codes))
code_name = dict(zip(names[:stockNum], codes[:stockNum]))


# 使用tushare获取上述股票周价格数据并转换为周收益率
# 设定默认起始日期为2018年1月5日，结束日期为2019年3月19日
# 日期可以根据需要自己改动
def get_data(code, start='20180101', end='20190319'):
    df = pro.daily(ts_code=code, start_date=start, end_date=end, fields='trade_date,close')
    # 将交易日期设置为索引值
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()
    # 计算收益率
    return df.close


# 构建一个空的dataframe用来装数据
data = pd.DataFrame()
for name, code in code_name.items():
    data[name] = get_data(code)


data.to_csv('daily_data.csv',encoding='utf-8')
# data=pd.read_csv('stock_data.csv',encoding='gbk',index_col='trade_date')
# data.index=(pd.to_datetime(data.index)).strftime('%Y%m%d')

# 计算收益率
def cal_ret(df, w=5):
    '''w:周5;月20;半年：120; 一年250
    '''
    df = df / df.shift(w) - 1
    return df.iloc[w:, :].fillna(0)


ret120 = cal_ret(data, w=120)


# 计算RPS
def get_RPS(ser):
    df = pd.DataFrame(ser.sort_values(ascending=False))
    df['n'] = range(1, len(df) + 1)
    df['rps'] = (1 - df['n'] / len(df)) * 100
    return df


# 计算每个交易日所有股票滚动w日的RPS
def all_RPS(data):
    dates = (data.index).strftime('%Y%m%d')
    RPS = {}
    for i in range(len(data)):
        RPS[dates[i]] = pd.DataFrame(get_RPS(data.iloc[i]).values, columns=['收益率', '排名', 'RPS'],
                                     index=get_RPS(data.iloc[i]).index)
    return RPS


rps120 = all_RPS(ret120)


# 获取所有股票在某个期间的RPS值
def all_data(rps, ret):
    df = pd.DataFrame(np.NaN, columns=ret.columns, index=ret.index)
    for date in ret.index:
        date = date.strftime('%Y%m%d')
        d = rps[date]
        for c in d.index:
            df.loc[date, c] = d.loc[c, 'RPS']
    return df


# 构建一个以前面收益率为基础的空表
df_new = pd.DataFrame(np.NaN, columns=ret120.columns, index=ret120.index)

# 计算所有股票在每一个交易日的向前120日滚动RPS值。对股票价格走势和RPS进行可视化。

for date in df_new.index:
    date = date.strftime('%Y%m%d')
    d = rps120[date]
    for c in d.index:
        df_new.loc[date, c] = d.loc[c, 'RPS']


def plot_rps(stock):
    plt.subplot(211)
    data[stock][120:].plot(figsize=(16, 16), color='r')
    plt.title(stock + '股价走势', fontsize=15)
    plt.yticks(fontsize=12)
    plt.xticks([])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.subplot(212)
    df_new[stock].plot(figsize=(16, 8), color='b')
    plt.title(stock + 'RPS相对强度', fontsize=15)
    my_ticks = pd.date_range('2018-06-9', '2019-3-31', freq='m')
    plt.xticks(my_ticks, fontsize=12)
    plt.yticks(fontsize=12)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.show()
    time.sleep(0.1)


# 查看2018年7月31日-2019年3月19日每月RPS情况。下面仅列出每个月RPS排名前十的股票，里面出现不少熟悉的“妖股”身影
dates = ['20180731', '20180831', '20180928', '20181031', '20181130', '20181228', '20190131', '20190228', '20190319']
df_rps = pd.DataFrame()
for date in dates:
    df_rps[date] = rps120[date].index[:50]
    print(df_rps[date])

# plot_rps('东方通信')
# plot_rps('华业资本')
# plot_rps('顺鑫农业')
plot_rps('万科A')
# for name in code_name:
#     plot_rps(name)