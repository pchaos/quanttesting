# -*- coding: utf-8 -*-
"""计算股票夏普比率
https://zhuanlan.zhihu.com/p/94058575
@Time    : 2020/3/1 上午10:22

@File    : test_sharp.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import QUANTAXIS as qa


class testsharp(unittest.TestCase):
    def test_sharp(self):
        plt.style.use('fivethirtyeight')
        end = datetime.datetime.now().today()
        start = end - datetime.timedelta(365)
        stock_data = qa.QA_fetch_index_day_adv('000001', start, end).data[['close']]
        benchmark_data = qa.QA_fetch_index_day_adv('399300', start, end).data[['close']]
        # Display summary for stock_data
        print('Stocks\n')
        # ... YOUR CODE FOR TASK 2 HERE ...
        print(stock_data.info())
        print(stock_data.head())
        # Display summary for benchmark_data
        print('\nBenchmarks\n')
        # ... YOUR CODE FOR TASK 2 HERE ...
        print(benchmark_data.info())
        print(benchmark_data.head())
        # visualize the stock_data
        # ... YOUR CODE FOR TASK 3 HERE ...
        stock_data.plot(title="Stock Data",subplots=True)


        # summarize the stock_data
        # ... YOUR CODE FOR TASK 3 HERE ...
        print(stock_data.describe())

        # plot the benchmark_data
        # ... YOUR CODE FOR TASK 4 HERE ...
        benchmark_data.plot(title="HS300")

        # summarize the benchmark_data
        # ... YOUR CODE FOR TASK 4 HERE ...
        print(benchmark_data.describe())

        # calculate daily stock_data returns
        stock_returns = stock_data.pct_change()

        # plot the daily returns
        # ... YOUR CODE FOR TASK 5 HERE ...
        stock_returns.plot()

        # summarize the daily returns
        # ... YOUR CODE FOR TASK 5 HERE ...
        print(stock_returns.describe())

        # calculate daily benchmark_data returns
        # ... YOUR CODE FOR TASK 6 HERE ...
        sp_returns = benchmark_data['close'].pct_change()

        # plot the daily returns
        # ... YOUR CODE FOR TASK 6 HERE ...
        sp_returns.plot()

        # summarize the daily returns
        # ... YOUR CODE FOR TASK 6 HERE ...
        print(sp_returns.describe())

        # calculate the difference in daily returns
        excess_returns = stock_returns.sub(sp_returns, axis=0)

        # plot the excess_returns
        # ... YOUR CODE FOR TASK 7 HERE ...
        excess_returns.plot()

        # summarize the excess_returns
        # ... YOUR CODE FOR TASK 7 HERE ...
        excess_returns.describe()

        # calculate the mean of excess_returns
        # ... YOUR CODE FOR TASK 8 HERE ...
        avg_excess_return = excess_returns.mean()
        # plot avg_excess_returns
        # ... YOUR CODE FOR TASK 8 HERE ...
        avg_excess_return.plot.bar(title='Mean of the Return Difference')

        # calculate the standard deviations
        sd_excess_return = excess_returns.std()

        # plot the standard deviations
        # ... YOUR CODE FOR TASK 9 HERE ...
        sd_excess_return.plot.bar(title='Standard Deviation of the Return Difference');

        # calculate the daily sharpe ratio
        daily_sharpe_ratio = daily_sharpe_ratio = avg_excess_return.div(sd_excess_return)

        # annualize the sharpe ratio
        annual_factor = np.sqrt(252)
        annual_sharpe_ratio = daily_sharpe_ratio.mul(annual_factor)

        # plot the annualized sharpe ratio
        # ... YOUR CODE FOR TASK 10 HERE ...
        annual_sharpe_ratio.plot.bar(title='Annualized Sharpe Ratio: Stocks vs HS300');

        plt.show()


if __name__ == '__main__':
    unittest.main()
