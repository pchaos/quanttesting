# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/26 下午11:51

@File    : qaETFstrategy.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import QUANTAXIS as qa
from QAStrategy.qastockbase import QAStrategyStockBase
from QUANTAXIS.QAARP import QA_Risk
from qaenv import (eventmq_ip, eventmq_password, eventmq_port,
                   eventmq_username, mongo_ip)


class strategyETF(QAStrategyStockBase):
    def __init__(self, code=['159901'], frequence='1min', strategy_id='QA_STRATEGY', risk_check_gap=1,
                 portfolio='default',
                 start='2019-01-01', end='2019-10-21', init_cash=1000000, send_wx=False, market_type='index_cn',
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
        self.market_type = market_type

    def run_backtest(self):
        self.debug()
        self.acc.save()

        risk = QA_Risk(self.acc, if_fq=False, market_data=self.market_data)
        risk.save()

