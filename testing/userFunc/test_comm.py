# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
import QUANTAXIS as qa
from userFunc import ifupMA

class testIfupMA(TestCase):
    def test_ifup_ma(self):
        # 获取全市场股票 list格式
        code = qa.QA_fetch_stock_list_adv().code.tolist()

        # 获取全市场数据 QADataStruct格式
        data = qa.QA_fetch_stock_day_adv(code, '2019-01-01', '2020-01-06').to_qfq()

        # apply到 QADataStruct上
        ind = data.add_func(ifupMA,20)

        # 对于指标groupby 日期 求和
        ind.dropna().groupby(level=0).sum()

        self.assertTrue(len(ind) > 0)


if __name__ == '__main__':
    unittest.main()
