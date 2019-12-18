import pandas as pd
import numpy as np
import statsmodels
import talib as ta
import tushare as ts
import matplotlib.pyplot as plt
from matplotlib import rc

import seaborn as sns

from matplotlib import dates
import matplotlib as mpl
# 均线的使用 https://www.jianshu.com/p/55f13956f789

rc('mathtext', default='regular')
sns.set_style('white')
# %matplotlib
# myfont =mpl.font_manager.FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=14)
plt.rcParams["figure.figsize"] = (20, 10)
# MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
dw = ts.get_k_data("600600")
close = dw.close.values
dw['avg'] = ta.SMA(close, timeperiod=30)
dw['SMA'] = ta.MA(close, 30, matype=0)
dw['EMA'] = ta.MA(close, 30, matype=1)
dw['WMA'] = ta.MA(close, 30, matype=2)
dw['DEMA'] = ta.MA(close, 30, matype=3)
dw['TEMA'] = ta.MA(close, 30, matype=4)
dw[['close', 'avg', 'EMA', 'WMA', 'DEMA', 'TEMA']].plot()
plt.show()
print(dw[-10:])
