# -*- coding: utf-8 -*-
"""
https://github.com/yutiansut/QAStrategy

@Time    : 2020/1/30 下午12:40

@File    : test_ccistrategy.py

@author  : yutiansuit
@license : Copyright(C), yutiansuit
@Contact : p19992003#gmail.com
"""

from QAStrategy import QAStrategyCTABase
import QUANTAXIS as QA
import uuid

class CCI(QAStrategyCTABase):
    def on_bar(self, bar):
        """你的大部分策略逻辑都是在此写的
        """
        res = self.cci()
        print(res.iloc[-1])
        if res.CCI[-1] < -100:
            print('LONG')
            if self.positions.volume_long == 0:
                self.send_order('BUY', 'OPEN', price=bar['close'], volume=1)
            if self.positions.volume_short > 0:
                self.send_order('BUY', 'CLOSE', price=bar['close'], volume=1)

        elif res.CCI[-1] > 100:
            print('SHORT')
            if self.positions.volume_short == 0:
                self.send_order('SELL', 'OPEN', price=bar['close'], volume=1)
            if self.positions.volume_long > 0:
                self.send_order('SELL', 'CLOSE', price=bar['close'], volume=1)

    def cci(self, ):
        """你可以自定义你想要的函数
        """
        return QA.QA_indicator_CCI(self.market_data, 61)

    def risk_check(self):
        pass

if __name__ == '__main__':
    strategy_id = str(uuid.uuid4())
    # strategy = CCI(code='rb2005', frequence='1min',
    strategy = CCI(code='rb2001', frequence='5min', strategy_id=strategy_id)
    strategy.debug()
    # 策略回测
    # strategy.run_backtest()

    # 策略模拟
    # strategy.debug_sim()
