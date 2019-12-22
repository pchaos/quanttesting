# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     羊驼策略
   Description :  https://www.itread01.com/content/1545582065.html
   羊駝策略
基本原理
在本策略中，每天按照收益率從小到大對股票池中的所有股票進行排序，起始時買入num_of_stocks只股票，然後每天在整個股票池中選出收益率前num_of_stocks，如果這些股票已持有，則繼續持有，如果未持有則買入，並賣掉收益率不是排在前num_of_stocks的股票
策略實現
選取市盈率在0~20之間的股票，作為待選股（若用所有股票，計算量過於龐大），一共332支股票

初始資金100萬，時間段為：2016-01-01~2018-05-01

設定策略引數，初始買入的股票數num_of_stocks，收益率計算所用天數period

其中收益率=昨天的收盤價/period天之前的收盤價

將股票池內的股票按照收益率排序，買入收益率最高的num_of_stocks只股票（num_of_stocks預設為10)各1000股。

之後的每天都將所有股票按收益率排序，如果股票池中有處於收益率前num_of_stocks而未持有的則買入，並賣掉收益率不處於前num_of_stocks的

   Author :
   date：          2019/9/4
-------------------------------------------------
   Change Activity:
                   2019/9/4:
-------------------------------------------------
"""

# coding: utf-8
# @author: lin
# @date: 2018/11/9


import QUANTAXIS as QA
import datetime
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('max_colwidth', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)


class Alpaca:
    def __init__(self, start_time, stop_time, n_stock=10, stock_init_cash=1000000, n_days_before=1):
        User = QA.QA_User(username='quantaxis', password='quantaxis')
        Portfolio = User.new_portfolio('qatestportfolio')
        Account = Portfolio.new_account(account_cookie='supersimple',
                                        init_cash=100000,
                                        init_hold={'601318': 1000},
                                        frequence=QA.FREQUENCE.THIRTY_MIN)
        Broker = QA.QA_BacktestBroker()
        QA.QA_SU_save_strategy(Account.account_cookie,
                               Account.portfolio_cookie, Account.account_cookie,
                               if_save=True)
        self.Account = QA.QA_Account()  # 初始化賬戶
        self.Account.reset_assets(stock_init_cash)  # 初始化賬戶
        self.Account.account_cookie = 'alpaca'
        self.Broker = QA.QA_BacktestBroker()
        self.time_quantum_list = ['-12-31', '-09-30', '-06-30', '-03-31']
        self.start_time = start_time
        self.stop_time = stop_time
        self.n_days_before = n_days_before
        self.stock_pool = []
        self.data = None
        self.ind = None
        self.n_stock = n_stock
        self.get_stock_pool()

    def get_financial_time(self):
        """
        得到此日期前一個財務資料的日期
        :return:
        """
        year = self.start_time[0:4]
        while (True):
            for day in self.time_quantum_list:
                the_financial_time = year + day
                if the_financial_time <= self.start_time:
                    return the_financial_time
            year = str(int(year) - 1)

    @staticmethod
    def get_assets_eps(stock_code, the_financial_time):
        """
        得到高階財務資料
        :param stock_code:
        :param the_financial_time: 離開始時間最近的財務資料的時間
        :return:
        """
        financial_report = QA.QA_fetch_financial_report(stock_code, the_financial_time)
        if financial_report is not None:
            return financial_report.iloc[0]['totalAssets'], financial_report.iloc[0]['EPS']
        return None, None

    def get_stock_pool(self):
        """
        選取哪些股票
        """
        stock_code_list = QA.QA_fetch_stock_list_adv().code.tolist()
        the_financial_time = self.get_financial_time()
        for stock_code in stock_code_list:
            # print(stock_code)
            assets, EPS = self.get_assets_eps(stock_code, the_financial_time)
            if assets is not None and EPS != 0:
                data = QA.QA_fetch_stock_day_adv(stock_code, self.start_time, self.stop_time)
                if data is None:
                    continue
                price = data.to_pd().iloc[0]['close']
                if 0 < price / EPS < 20:  # 滿足條件才新增進行排序
                    # print(price / EPS)
                    self.stock_pool.append(stock_code)

    # 成交量因子
    def alpaca(self, data):
        data['yesterday_price'] = 0
        data['previous_n_price'] = 0
        data.reset_index(inplace=True)   # 重置後，索引以數字
        for index, row in data.iterrows():
            yes_index = index - 1
            pre_n_index = index - (self.n_days_before+1)
            if yes_index >= 0:
                data.loc[index, 'yesterday_price'] = data.loc[yes_index, 'close']
            if pre_n_index >= 0:
                data.loc[index, 'previous_n_price'] = data.loc[pre_n_index, 'close']
        data['yield_rate'] = 0
        data['yield_rate'] = data['yesterday_price'] / data['previous_n_price']
        data.set_index(['date', 'code'], inplace=True)
        return data

    def solve_data(self):
        self.data = QA.QA_fetch_stock_day_adv(self.stock_pool, self.start_time, self.stop_time)
        self.ind = self.data.add_func(self.alpaca)

    def run(self):
        self.solve_data()
        for items in self.data.panel_gen:
            today_time = items.index[0][0]
            one_day_data = self.ind.loc[today_time]      # 得到有包含因子的DataFrame
            one_day_data['date'] = items.index[0][0]
            one_day_data.reset_index(inplace=True)
            one_day_data.sort_values(by='yield_rate', axis=0, ascending=False, inplace=True)
            today_stock = list(one_day_data.iloc[0:self.n_stock]['code'])
            one_day_data.set_index(['date', 'code'], inplace=True)
            one_day_data = QA.QA_DataStruct_Stock_day(one_day_data)  # 轉換格式，便於計算
            bought_stock_list = list(self.Account.hold.index)
            print("SELL:")
            for stock_code in bought_stock_list:
                # 如果直接在迴圈中對bought_stock_list操作，會跳過一些元素
                if stock_code not in today_stock:
                    try:
                        item = one_day_data.select_day(str(today_time)).select_code(stock_code)
                        order = self.Account.send_order(
                            code=stock_code,
                            time=today_time,
                            amount=self.Account.sell_available.get(stock_code, 0),
                            towards=QA.ORDER_DIRECTION.SELL,
                            price=0,
                            order_model=QA.ORDER_MODEL.MARKET,
                            amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )
                        self.Broker.receive_order(QA.QA_Event(order=order, market_data=item))
                        trade_mes = self.Broker.query_orders(self.Account.account_cookie, 'filled')
                        res = trade_mes.loc[order.account_cookie, order.realorder_id]
                        order.trade(res.trade_id, res.trade_price, res.trade_amount, res.trade_time)
                    except Exception as e:
                        print(e)
            print('BUY:')
            for stock_code in today_stock:
                try:
                    item = one_day_data.select_day(str(today_time)).select_code(stock_code)
                    order = self.Account.send_order(
                        code=stock_code,
                        time=today_time,
                        amount=1000,
                        towards=QA.ORDER_DIRECTION.BUY,
                        price=0,
                        order_model=QA.ORDER_MODEL.CLOSE,
                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    self.Broker.receive_order(QA.QA_Event(order=order, market_data=item))
                    trade_mes = self.Broker.query_orders(self.Account.account_cookie, 'filled')
                    res = trade_mes.loc[order.account_cookie, order.realorder_id]
                    order.trade(res.trade_id, res.trade_price, res.trade_amount, res.trade_time)
                except Exception as e:
                    print(e)
            self.Account.settle()
        Risk = QA.QA_Risk(self.Account)
        print(Risk.message)
        # plt.show()
        Risk.assets.plot()  # 總資產
        plt.show()
        Risk.benchmark_assets.plot()  # 基準收益的資產
        plt.show()
        Risk.plot_assets_curve()  # 兩個合起來的對比圖
        plt.show()
        Risk.plot_dailyhold()  # 每隻股票每天的買入量
        plt.show()


start = time.time()
sss = Alpaca('2017-01-01', '2018-01-01', 10)
stop = time.time()
print(stop - start)
print(len(sss.stock_pool))
sss.run()
stop2 = time.time()
print(stop2 - stop)
