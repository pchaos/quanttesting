# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/19 下午11:46

@File    : strategyabs.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

from abc import ABC, abstractmethod
import pandas as pd
import pymongo
from qaenv import (eventmq_amqp, eventmq_ip, eventmq_password, eventmq_port,
                   eventmq_username, mongo_ip, mongo_uri)
from QUANTAXIS.QAARP import QA_Risk, QA_User
import QUANTAXIS as qa


class StrategyAbs(ABC):
    @abstractmethod
    def algorithm(self, order):
        """算法
        """
        pass

    @property
    def bar_id(self):
        return len(self._market_data)

    @abstractmethod
    def run(self):
        pass


class StrategyDebug(StrategyAbs):
    def __init__(self):
        self.running_mode = 'backtest'
        self.quotation = None
        self.indicator = None

    def quotation(self, code, start, end, frequence, market, source=DATASOURCE.TDX, output=OUTPUT_FORMAT.DATAFRAME):
        pass

    def run(self):
        self.database = pymongo.MongoClient(mongo_ip).QUANTAXIS
        user = QA_User(username="admin", password='admin')
        port = user.new_portfolio(self.portfolio)
        self.acc = port.new_accountpro(
            account_cookie=self.strategy_id, init_cash=self.init_cash, market_type=self.market_type)
        self.positions = self.acc.get_position(self.code)

        print(self.acc)
        print(self.acc.market_type)
        data = self.quotation(self.code.upper(), self.start, self.end, source=qa.DATASOURCE.MONGO,
                               frequence=self.frequence, market=self.market_type, output=qa.OUTPUT_FORMAT.DATASTRUCT)
        data.data.apply(self.x1, axis=1)

    def x1(self, item):
        self.latest_price[item.name[1]] = item['close']
        if str(item.name[0])[0:10] != str(self.running_time)[0:10]:
            self.on_dailyclose()
            self.on_dailyopen()
            if self.market_type == qa.MARKET_TYPE.STOCK_CN:
                print('backtest: Settle!')
                self.acc.settle()
        self._on_1min_bar()
        self._market_data.append(item)
        self.running_time = str(item.name[0])
        self.on_bar(item)
