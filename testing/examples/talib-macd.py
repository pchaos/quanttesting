'''
Ta-lib计算MACD
'''
import pandas as pd
import numpy as np
import talib as ta
import tushare as ts
from matplotlib import rc
import matplotlib.pyplot as plt
import seaborn as sns

rc('mathtext', default='regular')
sns.set_style('white')
# %matplotlib
plt.rcParams["figure.figsize"] = (20, 10)

dw = ts.get_k_data("600600")
close = dw.close.values
dw['macd'], dw['macdsignal'], dw['macdhist'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
dw[['close','macd','macdsignal','macdhist']].plot()
plt.show()