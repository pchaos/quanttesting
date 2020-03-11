# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/11 上午11:48

@File    : test_hmaStategy.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

import QUANTAXIS as QA
from QAStrategy.qastockbase import QAStrategyStockBase
from QUANTAXIS import CROSS
import pprint
import talib
import datetime
import numpy as np
import pandas as pd
from qaenv import (eventmq_ip, eventmq_password, eventmq_port,
                   eventmq_username, mongo_ip)


def Timeline_Integral_with_cross_before(Tm, ):
    """
    计算时域金叉/死叉信号的累积卷积和(死叉(1-->0)不清零，金叉(0-->1)清零)
	这个我一直不会写成 lambda 或者 apply 的形式，只能用 for循环，谁有兴趣可以指导一下
    """
    T = [Tm[0]]
    for i in range(1, len(Tm)):
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


class HMA_Strategy(QAStrategyStockBase):
    def __init__(self, code=['000001'], frequence='1min', strategy_id='QA_STRATEGY', risk_check_gap=1,
                 portfolio='default',
                 start='2019-01-01', end='2019-10-21', send_wx=False, market_type='stock_cn',
                 data_host=eventmq_ip, data_port=eventmq_port, data_user=eventmq_username,
                 data_password=eventmq_password,
                 trade_host=eventmq_ip, trade_port=eventmq_port, trade_user=eventmq_username,
                 trade_password=eventmq_password,
                 taskid=None, mongo_ip=mongo_ip):
        super().__init__(code=code, frequence=frequence, strategy_id=strategy_id, risk_check_gap=risk_check_gap,
                         portfolio=portfolio,
                         start=start, end=end, send_wx=send_wx, market_type=market_type,
                         data_host=eventmq_ip, data_port=eventmq_port, data_user=eventmq_username,
                         data_password=eventmq_password,
                         trade_host=eventmq_ip, trade_port=eventmq_port, trade_user=eventmq_username,
                         trade_password=eventmq_password,
                         taskid=taskid, mongo_ip=mongo_ip)
        klines = QA.QA_fetch_stock_day_adv(code, start, end)
        self._hma = klines.add_func(hma_cross_func)

    def on_bar(self, data):
        res = self.hma(data)
        # print(res.iloc[-1])

        code = data.name[1]
        if (res['HMA_RETURN'][-1] > 0) and (
                res['MA30_CROSS_JX'][-1] < res['MA30_CROSS_SX'][-1]):
            print('LONG')
            # if self.positions.volume_long == 0:
            if self.acc.get_position(code).volume_long == 0:
                self.send_order('BUY', 'OPEN', code=code, price=data['close'], volume=100)

        elif (res['HMA_RETURN'][-1] < 0) and (
                res['MA30_CROSS_JX'][-1] > res['MA30_CROSS_SX'][-1]):
            print('SHORT')

            if self.acc.get_position(code).volume_long > 0:
                self.send_order('SELL', 'CLOSE',code=code, price=data['close'], volume=100)

    def hma(self, data):
        # 这里我想加一个add_func的指标，不知道怎么做
        print(data)
        day = data.name[0]
        code = data.name[1]
        return self._hma.loc[(slice(pd.Timestamp(day - datetime.timedelta(60)), pd.Timestamp(day)), code), :]

    def risk_check(self):
        pass
        # pprint.pprint(self.qifiacc.message)


if __name__ == '__main__':
    codes = ["000001", "000002", "600000"]
    strategy = HMA_Strategy(
        code=codes,
        frequence='day',
        strategy_id="QA_STRATEGY_DEMO",
        risk_check_gap=1,
        portfolio="hma_super_trend",
        start="2019-10-01",
        end="2020-03-09", )
    strategy.debug()
    # strategy.run_backtest()
