# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from datetime import datetime
import time
import QUANTAXIS as qa
from userFunc import ifupMA


class testIfupMA(TestCase):
    def test_ifup_ma_int(self):
        # 获取全市场股票 list格式
        code = self.getCodeList()

        # 获取全市场数据 QADataStruct格式
        data = qa.QA_fetch_stock_day_adv(code, '2019-01-01', '2020-01-06').to_qfq()

        # apply到 QADataStruct上
        ind = data.add_func(ifupMA, 20)

        # 对于指标groupby 日期 求和
        df = ind.dropna().groupby(level=0).sum()
        print(df.tail(10))
        # %matplotlib
        df.plot()
        self.assertTrue(len(ind) > 0)

    def test_ifup_ma_list(self):
        # 获取全市场股票 list格式
        code = self.getCodeList()

        # 获取全市场数据 QADataStruct格式
        data = qa.QA_fetch_stock_day_adv(code, '2019-01-01', '2020-01-06').to_qfq()

        # apply到 QADataStruct上
        ind = data.add_func(ifupMA, [20, 60])

        # 对于指标groupby 日期 求和
        df = ind.dropna().groupby(level=0).sum()
        print(df.tail(10))
        # %matplotlib
        df.plot()
        # time.sleep(3)
        self.assertTrue(len(ind) > 0)

    def getCodeList(self, isTesting=True, count=5000):
        """
        isTesting: 是否使用测试数据
        count： 返回最多结果集数量
        """
        if isTesting:
            # 2018.8首板个股，测试用，减少调试时间
            codelist = ['000023', '000068', '000407', '000561', '000590', '000593', '000608', '000610', '000626',
                        '000638',
                        '000657', '000659', '000663', '000669', '000677', '000705', '000759', '000766', '000780',
                        '000792',
                        '000815', '000852', '000885', '000909', '000913', '000921', '000928', '000931', '002006',
                        '002012',
                        '002034']
        else:
            codelist = qa.QA_fetch_stock_list_adv().code.tolist()
        return codelist[:count]

if __name__ == '__main__':
    unittest.main()
