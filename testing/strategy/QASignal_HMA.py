import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QAhuobi import FIRST_PRIORITY
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from QUANTAXIS.QAIndicator.talib_numpy import *
from QUANTAXIS.QAIndicator.base import *
import mpl_finance as mpf
import matplotlib.dates as mdates

def Timeline_Integral_with_cross_before(Tm,):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零) 
	这个我一直不会写成 lambda 或者 apply 的形式，只能用 for循环，谁有兴趣可以指导一下
    """
    T = [Tm[0]]
    for i in range(1,len(Tm)):
        T.append(T[i - 1] + 1) if (Tm[i] != 1) else T.append(0)
    return np.array(T)


def hma_cross_func(data):
    """
    HMA均线金叉指标
    """
    HMA10 = talib.WMA(2 * talib.WMA(data.close, int(10 / 2)) - talib.WMA(data.close, 10), int(np.sqrt(10)))
    MA30 = talib.MA(data.close, 30)
    
    MA30_CROSS = pd.DataFrame(columns=['MA30_CROSS', 'MA30_CROSS_JX', 'MA30_CROSS_SX'], index=data.index)
    MA30_CROSS_JX = CROSS(HMA10, MA30)
    MA30_CROSS_SX = CROSS(MA30, HMA10)
    MA30_CROSS['MA30_CROSS'] = np.where(MA30_CROSS_JX.values == 1, 1, np.where(MA30_CROSS_SX.values == 1, -1, 0))
    MA30_CROSS['MA30_CROSS_JX'] = Timeline_Integral_with_cross_before(MA30_CROSS_JX)
    MA30_CROSS['MA30_CROSS_SX'] = Timeline_Integral_with_cross_before(MA30_CROSS_SX)
    MA30_CROSS['HMA_RETURN'] = np.log(HMA10 / pd.Series(HMA10).shift(1))
    MA30_CROSS = MA30_CROSS.assign(HMA10=HMA10)
    return MA30_CROSS

if __name__ == '__main__':
    from QUANTAXIS.QAAnalysis.QAAnalysis_signal import *

    data_day = QA.QA_fetch_index_day_adv('000905', '2015-01-01','2020-03-30')
    
    hma_croos_day = data_day.add_func(hma_cross_func).reset_index([1])

    dealpool = ((hma_croos_day['HMA_RETURN'].values < 0) & (hma_croos_day['MA30_CROSS_JX'].values > hma_croos_day['MA30_CROSS_SX'].values))
    bootstrap = ((hma_croos_day['HMA_RETURN'].values > 0) & (hma_croos_day['MA30_CROSS_SX'].values > hma_croos_day['MA30_CROSS_JX'].values))
    strategy_POSITION = pd.DataFrame(columns=['BOOTSRTAP'], index=data_day.index.get_level_values(level=0))
    strategy_POSITION['BOOTSRTAP'] = np.where(bootstrap == True, 
                                            1, 
                                            np.where(dealpool == True, 
                                                    -1, 
                                                    np.where((hma_croos_day['HMA_RETURN'].values < 0), 
                                                            -1, 0)))

    # 为了处理 Position 信号抖动，使用 Rolling 过滤，无指向性的用 ATR 趋势策略填充  策略 1 加仓 0 不动， -1 减仓
    strategy_POSITION = strategy_POSITION.assign(BOOTSRTAP_R5=
                                                 strategy_POSITION['BOOTSRTAP'].rolling(4).apply(lambda x: 
                                                                                    x.sum(), raw=False).apply(lambda x:
                                                                                                                0 if np.isnan(x) else int(x)))
    # 策略 Rolling合并后 1 加仓 0 不动， -1 直接清仓
    strategy_POSITION['BOOTSRTAP_R5'] = np.where((hma_croos_day['HMA_RETURN'].values > 0) & (strategy_POSITION['BOOTSRTAP_R5'].values > 0), 
                      1, 
                      np.where((hma_croos_day['HMA_RETURN'].values < 0) & (strategy_POSITION['BOOTSRTAP_R5'].values < 0), 
                               -1, 
                               0)) # 这里 0 是代表本策略中无指向性的，为了降低代码复杂度去掉了 ATR 策略部分

    # 策略信号部分到此结束

    # 这四行是我自己用来看收益率，因为我不会做到QABacktest和QAStrategy来评估策略好坏。只能自己写个简单版的。
    strategy_POSITION['returns'] = np.nan_to_num(np.log(data_day.close / data_day.close.shift(1)), nan=0)
    strategy_POSITION['strategy_R5'] = np.where(strategy_POSITION['BOOTSRTAP_R5'].shift(1).values > 0, 1, 0) * strategy_POSITION['returns'].shift(1)
    print(strategy_POSITION[['returns', 'BOOTSRTAP_R5', 'strategy_R5']].tail(60))
    strategy_POSITION[['returns', 'strategy_R5']].dropna().cumsum().apply(np.exp).plot(figsize=(10, 6))

    plt.figure(figsize = (22,9))
    ax1 = plt.subplot(111)
    mpf.candlestick2_ochl(ax1, data_day.data.open.values, data_day.data.close.values, data_day.data.high.values, data_day.data.low.values, width = 0.6, colorup = 'r', colordown = 'green', alpha = 0.5)
    DATETIME_LABEL=data_day.index.get_level_values(level=0).to_series().apply(lambda x: x.strftime("%Y-%m-%d")[2:13])

    ax1.set_xticks(range(0, len(DATETIME_LABEL), round(len(data_day)/12)))
    ax1.set_xticklabels(DATETIME_LABEL[::round(len(data_day)/12)])

    plt.plot(DATETIME_LABEL, data_day.close, 'c', linewidth = 0.6, alpha = 0.75)

    ax1.plot(DATETIME_LABEL, 
             np.where((strategy_POSITION['BOOTSRTAP_R5'].values > 0), 
                      hma_croos_day['HMA10'].values, np.nan), 
             lw=2, color='lime', alpha=0.6)
    ax1.plot(DATETIME_LABEL, 
             np.where((strategy_POSITION['BOOTSRTAP_R5'].values > 0), 
                      hma_croos_day['HMA10'].values, np.nan), 
             'g*', alpha = 0.8)
    ax1.plot(DATETIME_LABEL, 
             np.where((strategy_POSITION['BOOTSRTAP_R5'].values < 0), 
                      hma_croos_day['HMA10'].values, np.nan), 
             'rx', alpha=0.8)
    plt.show()
