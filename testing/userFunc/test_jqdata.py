# -*- coding: utf-8 -*-
"""JQData-本地量化数据
https://www.joinquant.com/help/api/help?name=JQData
"""
import unittest
from unittest import TestCase
from jqdatasdk import *
from userFunc import jqTestingbase
from userFunc import setdiff_sorted


class testJQdata(jqTestingbase):
    def test_get_query_count(self):
        self.assertTrue(is_auth(), "验证用户未成功！")
        print("JoinQuant 使用情况：", get_query_count())
        self.assertTrue(len(get_query_count()) > 0, "获取数据出错")

    def test_get_all_securities(self):
        """获取平台支持的所有股票、基金、指数、期货信息
        参数
            types: list: 用来过滤securities的类型, list元素可选: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof', 'fja', 'fjb', 'open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'。types为空时返回所有股票, 不包括基金,指数和期货
            date: 日期, 一个字符串或者 [datetime.datetime]/[datetime.date] 对象, 用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息
        """
        df = get_all_securities(types=[], date=None)
        self.assertTrue(len(df) > 1000)
        print(df.head(10))
        print(df.tail(10))
        # 退市的列表
        dfend = df[df['end_date'] < '2020-01-01']
        self.assertTrue(len(dfend) > 10)
        self.assertTrue(len(df) > len(dfend))
        print(dfend.head(10))
        print(dfend.tail(10))

    def test_get_all_securities2(self):
        # 将所有股票列表转换成数组
        stocks = list(get_all_securities(['stock']).index)
        # 获得所有指数列表
        get_all_securities(['index'])

        # 获得所有基金列表
        df = get_all_securities(['fund'])

        # 获取所有期货列表
        get_all_securities(['futures'])

        # 获得etf基金列表
        df = get_all_securities(['etf'])
        # 获得lof基金列表
        df = get_all_securities(['lof'])
        # 获得分级A基金列表
        df = get_all_securities(['fja'])
        # 获得分级B基金列表
        df = get_all_securities(['fjb'])

        # 获得2015年10月10日还在上市的所有股票列表
        get_all_securities(date='2015-10-10')
        # 获得2015年10月10日还在上市的 etf 和 lof 基金列表
        get_all_securities(['etf', 'lof'], '2015-10-10')

    def test_get_index_stocks(self):
        """获取指数成份股
        参数
            index_symbol: 指数代码
            date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,
            返回 返回股票代码的list
        """
        # 获取所有沪深300的股票
        stocks = get_index_stocks('000300.XSHG')
        day = '2015-10-15'
        stocks2 = get_index_stocks('000300.XSHG', day)
        print(stocks)
        self.assertTrue(len(stocks) == len(stocks2))
        stockdiff = setdiff_sorted(stocks2, stocks)
        self.assertTrue(len(stockdiff) > 0)
        print("{}之后退出指数的个股： {}".format(day, stockdiff))


if __name__ == '__main__':
    unittest.main()
