# -*- coding: utf-8 -*- #
"""画图函数 self.plot(name, data, format)

获取当前code self.get_code()

self.ind2str(ind, ind_type)

获取品种所在的交易所 self.get_exchange(code)

获取品种持仓 self.get_positions(code)

获取当前现金 self.get_cash()

获取某个品种的marketdata self.get_code_marketdata(code)

获取当前的maretdata切片 self.get_current_marketdata()

订阅数据 (实时模拟用/ 回测不需要) self.subscribe_data(code, frequence, data_host, data_port, data_user, data_password, model='py')

用当日tick数据进行回测(期货) self.debug_currenttick(freq)

用历史tick数据进行回测(期货) self.debug_histick(freq)

使用t0模式进行回测 self.debug_t0()

回测(不存储账户数据的模式) self.debug()

回测(存储账户数据的模式) self.run_backtest()

实时模拟(阻塞形式 不能同时多开很多个) self.run_sim()

实时模拟(非阻塞模式 可以同时开很多个) self.debug_sim()

Account
你需要注意的是, self.acc 在不同的模式下是不一样的

在回测模式: self.acc是一个实例化的 QUANTAXIS.QAAccountPro 类

在模拟模式: self.acc是一个实例化的 qifiaccount 账户

实时的账户的历史成交 self.acc.trade 回测的账户的历史成交 self.acc.history_table

QAPosition
如果你需要查询当前的仓位:  positions.cur_vol  / positions.hold_detail

如果你需要查询仓位的全部信息:  self.positons.static_message

如果你需要知道详细的基于当前价格的动态信息:  self.position.realtime_message

positions.volume_long  #当前持的多单

positions.volume_short #当前持仓的空单数量

positions.volume_long_today #今日多单数量

positions.volume_long_his #今日多单数量

positions.volume_short_today #今日空单数量

positions.volume_short_his #今日空单数量

positions.position_price_long  # 基于结算价计算的多头成本价

positions.position_cost_long   # 基于结算价计算的多头总成本(总市值)

positions.position_price_short  # 基于结算价计算的空头开仓均价

positions.position_cost_short # 基于结算价计算的空头成本

positions.open_price_long  # 基于开仓价计算的多头开仓价

positions.open_cost_long  # 基于开仓价计算的多头开仓价

positions.open_price_short  # 基于开仓价计算的多头开仓价空头开仓价

positions.open_cost_short  # 基于开仓价计算的多头开仓价空头成本

"""
import datetime
import pandas as pd
import QUANTAXIS as QA
# from QUANTAXIS.QAARP import QA_Risk, QA_User
# from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread
# from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, RUNNING_ENVIRONMENT, ORDER_DIRECTION
# from QAPUBSUB.consumer import subscriber_topic, subscriber_routing
# from QAPUBSUB.producer import publisher_routing
# from QAStrategy.qactabase import QAStrategyCTABase
# from QIFIAccount import QIFI_Account
from qaenv import (eventmq_ip, eventmq_password, eventmq_port,
                   eventmq_username, mongo_ip)
from userFunc import QAStrategyETFBase


class strategy(QAStrategyETFBase):
    def __init__(self, code=['159901'], frequence='1min', strategy_id='QA_STRATEGY', risk_check_gap=1,
                 portfolio='default',
                 start='2019-01-01', end='2019-10-21', send_wx=False, market_type='index_cn',
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


    def user_init(self):
        self.cutsCount = 10
        klines = QA.QA_fetch_index_day_adv(self.code, self.start, self.end)
        self._cci = QA.QA_indicator_CCI(klines, 14)

    def on_bar(self, data):
        # print(data)
        # print(self.get_positions(self.code[0]))
        # print(self.market_data)

        code = data.name[1]
        # print('---------------under is 当前全市场的market_data --------------')
        #
        # print(self.get_current_marketdata())
        # print('---------------under is 当前品种的market_data --------------')
        # print(self.get_code_marketdata(code))
        # print(code)
        # print(self.running_time)
        # input()
        res = self.cci(data)

        # print(res.iloc[-1])
        # print(res.CCI.tail(10))

        # self.positions = self.acc.get_position(self.code)
        if self.buyCondition(res):
            # 买
            # if self.acc.get_position(code).volume_long == 0:
            self.send_order('BUY', 'OPEN', code=code, price=data['close'], volume=self.getPerVolume(data.close))
            print('---------------under is buy info --------------')
            self.accuntInfo(code, data, res)
        elif self.sellCondition(res):
            # 卖
            if self.getPostion(code).volume_long > 0:
                # 计算成交股数
                vol = self.getPerVolume(data.close)
                vol = vol if vol <= self.getPostion(code).volume_long else self.getPostion(code).volume_long
                self.send_order('SELL', 'CLOSE', code=code, price=data['close'],
                                volume=vol)
                print('---------------under is SELL info --------------')
                self.accuntInfo(code, data, res)
        else:
            # print(res.CCI[-1], end=';')
            pass

    def accuntInfo(self, code, data, res):
        print("sell:{} {} vol:{} cci: {} {} {}".format(code, data['close'], self.getPerVolume(data.close),
                                                       round(res.CCI[-1], 1), round(res.CCI[-2], 1),
                                                       datetime.datetime.fromtimestamp(data.date_stamp)))
        print(self.get_code_marketdata(code)[['close', 'vol']].tail(3))
        print(self.get_positions(code))
        print("交易记录: {}".format(self.acc.trade))
        print("交易记录: {}".format(self.acc.trade[code].sum()))

    def cci(self, data):
        day = data.name[0]
        code = data.name[1]
        return self._cci.loc[(slice(pd.Timestamp(day - datetime.timedelta(60)), pd.Timestamp(day)), code), :]

    def getPerVolume(self, price):
        """计算每次买入的数量
        """
        return round(self.acc.cash[0] / self.cutsCount / price, -2)

    def buyCondition(self, res):
        # CCI升破-100时买入
        try:
            return res.CCI[-1] > -100 and res.CCI[-2] < -100
        except Exception as e:
            print(e)
            print("res.CCI: {}".format(res.CCI[-1]))
            return False

    def sellCondition(self, res):
        # CCI超过100后，跌破100时卖出
        try:
            return res.CCI[-1] < 100 and res.CCI[-2] > 100
        except Exception as e:
            return False


if __name__ == '__main__':
    s = strategy(code=['515050', '159952', '515000'], frequence='day', start='2019-08-01', end='2020-02-10', strategy_id='xetf2')
    s.debug()
    # s.run_backtest()
    # print(s.market_data)
    # s.risk_check()
    s = None
    print("Done.")

    """
    
    portfolio with user_cookie  USER_QoZ8TDrF  already exist!!
    < QA_AccountPRO x market: stock_cn>
    stock_cn
    backtest: Settle!
    open      9.390000e+00
    high      9.420000e+00
    low       9.160000e+00
    close     9.190000e+00
    volume    5.393860e+05
    amount    4.986951e+08
    Name: (2019-01-02 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                    open  high   low  close    volume       amount
    2019-01-02 000001  9.39  9.42  9.16   9.19  539386.0  498695104.0
    ---------------under is 当前全市场的market_data --------------
                    open  high   low  close    volume       amount
    2019-01-02 000001  9.39  9.42  9.16   9.19  539386.0  498695104.0
    ---------------under is 当前品种的market_data --------------
                    open  high   low  close    volume       amount
    2019-01-02 000001  9.39  9.42  9.16   9.19  539386.0  498695104.0
    000001
    
    open      2.383000e+01
    high      2.409000e+01
    low       2.367000e+01
    close     2.390000e+01
    volume    2.470100e+05
    amount    5.893846e+08
    Name: (2019-01-02 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close    volume       amount
    2019-01-02 000001   9.39   9.42   9.16   9.19  539386.0  498695104.0
            000002  23.83  24.09  23.67  23.90  247010.0  589384576.0
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-02 000001   9.39   9.42   9.16   9.19  539386.0  498695104.0
            000002  23.83  24.09  23.67  23.90  247010.0  589384576.0
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-02 000002  23.83  24.09  23.67   23.9  247010.0  589384576.0
    000002
    
    backtest: Settle!
    open      9.180000e+00
    high      9.330000e+00
    low       9.150000e+00
    close     9.280000e+00
    volume    4.155370e+05
    amount    3.844577e+08
    Name: (2019-01-03 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close    volume       amount
    2019-01-02 000001   9.39   9.42   9.16   9.19  539386.0  498695104.0
            000002  23.83  24.09  23.67  23.90  247010.0  589384576.0
    2019-01-03 000001   9.18   9.33   9.15   9.28  415537.0  384457696.0
    ---------------under is 当前全市场的market_data --------------
                    open  high   low  close    volume       amount
    2019-01-03 000001  9.18  9.33  9.15   9.28  415537.0  384457696.0
    ---------------under is 当前品种的market_data --------------
                    open  high   low  close    volume       amount
    2019-01-02 000001  9.39  9.42  9.16   9.19  539386.0  498695104.0
    2019-01-03 000001  9.18  9.33  9.15   9.28  415537.0  384457696.0
    000001
    
    open      2.379000e+01
    high      2.450000e+01
    low       2.371000e+01
    close     2.407000e+01
    volume    2.223530e+05
    amount    5.363333e+08
    Name: (2019-01-03 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close    volume       amount
    2019-01-02 000001   9.39   9.42   9.16   9.19  539386.0  498695104.0
            000002  23.83  24.09  23.67  23.90  247010.0  589384576.0
    2019-01-03 000001   9.18   9.33   9.15   9.28  415537.0  384457696.0
            000002  23.79  24.50  23.71  24.07  222353.0  536333280.0
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-03 000001   9.18   9.33   9.15   9.28  415537.0  384457696.0
            000002  23.79  24.50  23.71  24.07  222353.0  536333280.0
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-02 000002  23.83  24.09  23.67  23.90  247010.0  589384576.0
    2019-01-03 000002  23.79  24.50  23.71  24.07  222353.0  536333280.0
    000002
    
    backtest: Settle!
    open      9.240000e+00
    high      9.820000e+00
    low       9.220000e+00
    close     9.750000e+00
    volume    1.481159e+06
    amount    1.422150e+09
    Name: (2019-01-04 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
    ---------------under is 当前全市场的market_data --------------
                    open  high   low  close     volume        amount
    2019-01-04 000001  9.24  9.82  9.22   9.75  1481159.0  1.422150e+09
    ---------------under is 当前品种的market_data --------------
                    open  high   low  close     volume        amount
    2019-01-02 000001  9.39  9.42  9.16   9.19   539386.0  4.986951e+08
    2019-01-03 000001  9.18  9.33  9.15   9.28   415537.0  3.844577e+08
    2019-01-04 000001  9.24  9.82  9.22   9.75  1481159.0  1.422150e+09
    000001
    
    open      2.391000e+01
    high      2.500000e+01
    low       2.385000e+01
    close     2.493000e+01
    volume    3.777270e+05
    amount    9.270117e+08
    Name: (2019-01-04 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close     volume        amount
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-02 000002  23.83  24.09  23.67  23.90  247010.0  589384576.0
    2019-01-03 000002  23.79  24.50  23.71  24.07  222353.0  536333280.0
    2019-01-04 000002  23.91  25.00  23.85  24.93  377727.0  927011712.0
    000002
    
    backtest: Settle!
    open      9.840000e+00
    high      9.850000e+00
    low       9.630000e+00
    close     9.740000e+00
    volume    8.656870e+05
    amount    8.411664e+08
    Name: (2019-01-07 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
    ---------------under is 当前全市场的market_data --------------
                    open  high   low  close    volume       amount
    2019-01-07 000001  9.84  9.85  9.63   9.74  865687.0  841166400.0
    ---------------under is 当前品种的market_data --------------
                    open  high   low  close     volume        amount
    2019-01-02 000001  9.39  9.42  9.16   9.19   539386.0  4.986951e+08
    2019-01-03 000001  9.18  9.33  9.15   9.28   415537.0  3.844577e+08
    2019-01-04 000001  9.24  9.82  9.22   9.75  1481159.0  1.422150e+09
    2019-01-07 000001  9.84  9.85  9.63   9.74   865687.0  8.411664e+08
    000001
    
    open      2.529000e+01
    high      2.553000e+01
    low       2.499000e+01
    close     2.505000e+01
    volume    4.271540e+05
    amount    1.077909e+09
    Name: (2019-01-07 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close    volume        amount
    2019-01-07 000001   9.84   9.85   9.63   9.74  865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05  427154.0  1.077909e+09
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume        amount
    2019-01-02 000002  23.83  24.09  23.67  23.90  247010.0  5.893846e+08
    2019-01-03 000002  23.79  24.50  23.71  24.07  222353.0  5.363333e+08
    2019-01-04 000002  23.91  25.00  23.85  24.93  377727.0  9.270117e+08
    2019-01-07 000002  25.29  25.53  24.99  25.05  427154.0  1.077909e+09
    000002
    
    backtest: Settle!
    open      9.730000e+00
    high      9.740000e+00
    low       9.620000e+00
    close     9.660000e+00
    volume    4.023880e+05
    amount    3.892478e+08
    Name: (2019-01-08 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
    ---------------under is 当前全市场的market_data --------------
                    open  high   low  close    volume       amount
    2019-01-08 000001  9.73  9.74  9.62   9.66  402388.0  389247808.0
    ---------------under is 当前品种的market_data --------------
                    open  high   low  close     volume        amount
    2019-01-02 000001  9.39  9.42  9.16   9.19   539386.0  4.986951e+08
    2019-01-03 000001  9.18  9.33  9.15   9.28   415537.0  3.844577e+08
    2019-01-04 000001  9.24  9.82  9.22   9.75  1481159.0  1.422150e+09
    2019-01-07 000001  9.84  9.85  9.63   9.74   865687.0  8.411664e+08
    2019-01-08 000001  9.73  9.74  9.62   9.66   402388.0  3.892478e+08
    000001
    
    open      2.505000e+01
    high      2.520000e+01
    low       2.463000e+01
    close     2.500000e+01
    volume    2.143820e+05
    amount    5.336044e+08
    Name: (2019-01-08 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
            000002  25.05  25.20  24.63  25.00   214382.0  5.336044e+08
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-08 000001   9.73   9.74   9.62   9.66  402388.0  389247808.0
            000002  25.05  25.20  24.63  25.00  214382.0  533604352.0
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume        amount
    2019-01-02 000002  23.83  24.09  23.67  23.90  247010.0  5.893846e+08
    2019-01-03 000002  23.79  24.50  23.71  24.07  222353.0  5.363333e+08
    2019-01-04 000002  23.91  25.00  23.85  24.93  377727.0  9.270117e+08
    2019-01-07 000002  25.29  25.53  24.99  25.05  427154.0  1.077909e+09
    2019-01-08 000002  25.05  25.20  24.63  25.00  214382.0  5.336044e+08
    000002
    
    backtest: Settle!
    open      9.740000e+00
    high      1.008000e+01
    low       9.700000e+00
    close     9.940000e+00
    volume    1.233486e+06
    amount    1.229465e+09
    Name: (2019-01-09 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
            000002  25.05  25.20  24.63  25.00   214382.0  5.336044e+08
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
    ---------------under is 当前全市场的market_data --------------
                    open   high  low  close     volume        amount
    2019-01-09 000001  9.74  10.08  9.7   9.94  1233486.0  1.229465e+09
    ---------------under is 当前品种的market_data --------------
                    open   high   low  close     volume        amount
    2019-01-02 000001  9.39   9.42  9.16   9.19   539386.0  4.986951e+08
    2019-01-03 000001  9.18   9.33  9.15   9.28   415537.0  3.844577e+08
    2019-01-04 000001  9.24   9.82  9.22   9.75  1481159.0  1.422150e+09
    2019-01-07 000001  9.84   9.85  9.63   9.74   865687.0  8.411664e+08
    2019-01-08 000001  9.73   9.74  9.62   9.66   402388.0  3.892478e+08
    2019-01-09 000001  9.74  10.08  9.70   9.94  1233486.0  1.229465e+09
    000001
    
    open      2.540000e+01
    high      2.588000e+01
    low       2.511000e+01
    close     2.533000e+01
    volume    3.401400e+05
    amount    8.670814e+08
    Name: (2019-01-09 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
            000002  25.05  25.20  24.63  25.00   214382.0  5.336044e+08
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
            000002  25.40  25.88  25.11  25.33   340140.0  8.670814e+08
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close     volume        amount
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
            000002  25.40  25.88  25.11  25.33   340140.0  8.670814e+08
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume        amount
    2019-01-02 000002  23.83  24.09  23.67  23.90  247010.0  5.893846e+08
    2019-01-03 000002  23.79  24.50  23.71  24.07  222353.0  5.363333e+08
    2019-01-04 000002  23.91  25.00  23.85  24.93  377727.0  9.270117e+08
    2019-01-07 000002  25.29  25.53  24.99  25.05  427154.0  1.077909e+09
    2019-01-08 000002  25.05  25.20  24.63  25.00  214382.0  5.336044e+08
    2019-01-09 000002  25.40  25.88  25.11  25.33  340140.0  8.670814e+08
    000002
    
    backtest: Settle!
    open      9.870000e+00
    high      1.020000e+01
    low       9.860000e+00
    close     1.010000e+01
    volume    1.071817e+06
    amount    1.079711e+09
    Name: (2019-01-10 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
            000002  25.05  25.20  24.63  25.00   214382.0  5.336044e+08
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
            000002  25.40  25.88  25.11  25.33   340140.0  8.670814e+08
    2019-01-10 000001   9.87  10.20   9.86  10.10  1071817.0  1.079711e+09
    ---------------under is 当前全市场的market_data --------------
                    open  high   low  close     volume        amount
    2019-01-10 000001  9.87  10.2  9.86   10.1  1071817.0  1.079711e+09
    ---------------under is 当前品种的market_data --------------
                    open   high   low  close     volume        amount
    2019-01-02 000001  9.39   9.42  9.16   9.19   539386.0  4.986951e+08
    2019-01-03 000001  9.18   9.33  9.15   9.28   415537.0  3.844577e+08
    2019-01-04 000001  9.24   9.82  9.22   9.75  1481159.0  1.422150e+09
    2019-01-07 000001  9.84   9.85  9.63   9.74   865687.0  8.411664e+08
    2019-01-08 000001  9.73   9.74  9.62   9.66   402388.0  3.892478e+08
    2019-01-09 000001  9.74  10.08  9.70   9.94  1233486.0  1.229465e+09
    2019-01-10 000001  9.87  10.20  9.86  10.10  1071817.0  1.079711e+09
    000001
    
    open      2.522000e+01
    high      2.556000e+01
    low       2.503000e+01
    close     2.511000e+01
    volume    2.246490e+05
    amount    5.689526e+08
    Name: (2019-01-10 00:00:00, 000002), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
            000002  25.05  25.20  24.63  25.00   214382.0  5.336044e+08
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
            000002  25.40  25.88  25.11  25.33   340140.0  8.670814e+08
    2019-01-10 000001   9.87  10.20   9.86  10.10  1071817.0  1.079711e+09
            000002  25.22  25.56  25.03  25.11   224649.0  5.689526e+08
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close     volume        amount
    2019-01-10 000001   9.87  10.20   9.86  10.10  1071817.0  1.079711e+09
            000002  25.22  25.56  25.03  25.11   224649.0  5.689526e+08
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close    volume        amount
    2019-01-02 000002  23.83  24.09  23.67  23.90  247010.0  5.893846e+08
    2019-01-03 000002  23.79  24.50  23.71  24.07  222353.0  5.363333e+08
    2019-01-04 000002  23.91  25.00  23.85  24.93  377727.0  9.270117e+08
    2019-01-07 000002  25.29  25.53  24.99  25.05  427154.0  1.077909e+09
    2019-01-08 000002  25.05  25.20  24.63  25.00  214382.0  5.336044e+08
    2019-01-09 000002  25.40  25.88  25.11  25.33  340140.0  8.670814e+08
    2019-01-10 000002  25.22  25.56  25.03  25.11  224649.0  5.689526e+08
    000002
    
    backtest: Settle!
    open      1.011000e+01
    high      1.022000e+01
    low       1.005000e+01
    close     1.020000e+01
    volume    6.963640e+05
    amount    7.080018e+08
    Name: (2019-01-11 00:00:00, 000001), dtype: float64
    < QAPOSITION 000001 amount 0/0 >
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
            000002  23.83  24.09  23.67  23.90   247010.0  5.893846e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  3.844577e+08
            000002  23.79  24.50  23.71  24.07   222353.0  5.363333e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
            000002  23.91  25.00  23.85  24.93   377727.0  9.270117e+08
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
            000002  25.29  25.53  24.99  25.05   427154.0  1.077909e+09
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
            000002  25.05  25.20  24.63  25.00   214382.0  5.336044e+08
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
            000002  25.40  25.88  25.11  25.33   340140.0  8.670814e+08
    2019-01-10 000001   9.87  10.20   9.86  10.10  1071817.0  1.079711e+09
            000002  25.22  25.56  25.03  25.11   224649.0  5.689526e+08
    2019-01-11 000001  10.11  10.22  10.05  10.20   696364.0  7.080018e+08
    ---------------under is 当前全市场的market_data --------------
                        open   high    low  close    volume       amount
    2019-01-11 000001  10.11  10.22  10.05   10.2  696364.0  708001792.0
    ---------------under is 当前品种的market_data --------------
                        open   high    low  close     volume        amount
    2019-01-02 000001   9.39   9.42   9.16   9.19   539386.0  4.986951e+08
    2019-01-03 000001   9.18   9.33   9.15   9.28   415537.0  self.account.daily_cash.set_index('date').cash3.844577e+08
    2019-01-04 000001   9.24   9.82   9.22   9.75  1481159.0  1.422150e+09
    2019-01-07 000001   9.84   9.85   9.63   9.74   865687.0  8.411664e+08
    2019-01-08 000001   9.73   9.74   9.62   9.66   402388.0  3.892478e+08
    2019-01-09 000001   9.74  10.08   9.70   9.94  1233486.0  1.229465e+09
    2019-01-10 000001   9.87  10.20   9.86  10.10  1071817.0  1.079711e+09
    2019-01-11 000001  10.11  10.22  10.05  10.20   696364.0  7.080018e+08
    """
