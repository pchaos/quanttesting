# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/26 下午11:51

@File    : qaETFstrategy.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import uuid
import datetime
import json
import requests
import pandas as pd
import QUANTAXIS as qa
import QUANTAXIS as QA
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, RUNNING_ENVIRONMENT, ORDER_DIRECTION
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

    def x1(self, item):
        self.latest_price[item.name[1]] = item['close']
        if str(item.name[0])[0:10] != str(self.running_time)[0:10]:
            self.on_dailyclose()
            self.on_dailyopen()
            print('backtest: Settle!')
            self.acc.settle()
        self._on_1min_bar()
        self._market_data.append(item)
        self.running_time = str(item.name[0])
        self.on_bar(item)

    def send_order(self, direction='BUY', offset='OPEN', code=None, price=3925, volume=10, order_id='', ):

        towards = eval('ORDER_DIRECTION.{}_{}'.format(direction, offset))
        order_id = str(uuid.uuid4()) if order_id == '' else order_id

        if self.market_type == QA.MARKET_TYPE.STOCK_CN:
            """
            在此对于股票的部分做一些转换
            """
            if towards == ORDER_DIRECTION.SELL_CLOSE:
                towards = ORDER_DIRECTION.SELL
            elif towards == ORDER_DIRECTION.BUY_OPEN:
                towards = ORDER_DIRECTION.BUY

        if isinstance(price, float):
            pass
        elif isinstance(price, pd.Series):
            price = price.values[0]

        if self.running_mode == 'sim':

            QA.QA_util_log_info(
                '============ {} SEND ORDER =================='.format(order_id))
            QA.QA_util_log_info('direction{} offset {} price{} volume{}'.format(
                direction, offset, price, volume))

            if self.check_order(direction, offset):
                self.last_order_towards = {'BUY': '', 'SELL': ''}
                self.last_order_towards[direction] = offset
                now = str(datetime.datetime.now())

                order = self.acc.send_order(
                    code=code, towards=towards, price=price, amount=volume, order_id=order_id)
                order['topic'] = 'send_order'
                self.pub.pub(
                    json.dumps(order), routing_key=self.strategy_id)

                self.acc.make_deal(order)
                self.bar_order['{}_{}'.format(direction, offset)] = self.bar_id
                if self.send_wx:
                    for user in self.subscriber_list:
                        QA.QA_util_log_info(self.subscriber_list)
                        try:
                            "oL-C4w2WlfyZ1vHSAHLXb2gvqiMI"
                            """http://www.yutiansut.com/signal?user_id=oL-C4w1HjuPRqTIRcZUyYR0QcLzo&template=xiadan_report&\
                                        strategy_id=test1&realaccount=133496&code=rb1910&order_direction=BUY&\
                                        order_offset=OPEN&price=3600&volume=1&order_time=20190909
                            """

                            requests.post(
                                'http://www.yutiansut.com/signal?user_id={}&template={}&strategy_id={}&realaccount={}&code={}&order_direction={}&order_offset={}&price={}&volume={}&order_time={}'.format(
                                    user, "xiadan_report", self.strategy_id, self.acc.user_id, code, direction, offset,
                                    price, volume, now))
                        except Exception as e:
                            QA.QA_util_log_info(e)

            else:
                QA.QA_util_log_info('failed in ORDER_CHECK')

        elif self.running_mode == 'backtest':

            self.bar_order['{}_{}'.format(direction, offset)] = self.bar_id
            # mock
            oldMarketType = self.acc.market_type
            self.acc.market_type = MARKET_TYPE.STOCK_CN
            self.acc.receive_simpledeal(
                code=code, trade_time=self.running_time, trade_towards=towards, trade_amount=volume, trade_price=price,
                order_id=order_id)
            self.acc.market_type = oldMarketType
            # self.positions = self.acc.get_position(self.code)

    def getPostion(self, code):
        # mock
        self.acc.market_type = MARKET_TYPE.STOCK_CN
        pos= self.acc.get_position(code)
        self.acc.market_type = MARKET_TYPE.INDEX_CN
        return pos
