# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv, QA_fetch_stock_min_adv
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day, QA_fetch_stock_min
from QUANTAXIS.QAUtil import DATABASE
from qaHelper.fetcher import QueryMongodb_adv as qm
from .qhtestbase import QhBaseTestCase


class testQuery(QhBaseTestCase):
    def test_collections(self):
        collections = qm.collections
        self.assertTrue(collections.name == DATABASE.stock_day.name, "数据表名应该相同")

        qm.collections = DATABASE.stock_min
        self.assertTrue(collections.name != qm.collections.name)
        print("原始表名：{}，\n改变后表名：{}".format(collections, qm.collections))

        qm.collections = collections
        self.assertTrue(collections.name == qm.collections.name)

    def test_get(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertTrue(len(df) > days // 10, "返回数据数量应该大于0。")
        print(df.tail())

    def test_get_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        df2 = QA_fetch_stock_day(code, start, end, format='pd')
        self.assertTrue(len(df) == len(df2), "和QA返回的数据,长度不一致")
        # 两种方式检测numpy数据一致性
        obo = self.differOneByOne(df, df2)
        self.assertTrue(df.equals(df2), "和QA返回的数据不一致{}".format(obo))

    def test_get_noData(self):
        code = '600001'  # 不存在的股票代码
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertTrue(df is None, "{}已退市，2020年返回数据数量应该等于0,{}。".format(code, df))

    def test_getMin(self):
        code = '000001'
        days = 30 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end, frequence='1min')
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        print(df.tail(10))

    def test_getMin_datetimestr(self):
        code = '000001'
        days = 30 * 1.2
        start = str(datetime.datetime.now() - datetime.timedelta(days))[:10]
        end = str(datetime.datetime.now() - datetime.timedelta(0))[:10]
        df = qm.get(code, start, end, frequence='1min')
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        print(df.tail(10))
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df2 = qm.get(code, start, end, frequence='1min')
        # str化后的时间为开盘时间，
        self.assertTrue(len(df) >= len(df2))
        data1, data2 = df, df2
        if len(data1) > len(data2):
            data1 = data1[-len(data2):]
            print("array1f的长度比array2长")
        elif len(data1) < len(data2):
            data2 = data2[-len(data1):]
            print("array2的长度比array1长")
        self.assertTrue(data1.equals(data2), "截取相同长度后的数据应该相同")

    def test_getMin_diffQA(self):
        code = '000001'
        days = 20 * 1.2
        start = str(datetime.datetime.now() - datetime.timedelta(days))
        end = str(datetime.datetime.now() - datetime.timedelta(0))
        df = qm.get(code, start, end, frequence='1min')
        df2 = QA_fetch_stock_min(code, start, end=end, format='pd', frequence='1min')
        # todo df的长度比df2长。未找出原因
        data1, data2 = df, df2
        self.assertTrue(len(data1) == len(data2), "和QA返回的分钟线数据长度不一致:{}:{}".format(len(data1), len(data2)))
        if len(data1) > len(data2):
            print("array1f的长度比array2长")
            data1 = data1[-len(data2):]
        elif len(data1) < len(data2):
            print("array2的长度比array1长")
            data2 = data2[-len(data1):]
        # todo  连续获取分钟数据时，不定时返回结果不想等。报错
        obo = self.differOneByOne(data1, data2)
        self.assertTrue(data1.equals(data2),
                        "和QA返回的分钟线数据不一致:{}".format(obo))

    def test_getAdv(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.getAdv(code, start, end)
        self.assertTrue(len(df) > days // 10, "返回数据数量应该大于0。")
        print(df.data.tail())

    def test_getAdv_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.getAdv(code, start, end)
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        df2 = QA_fetch_stock_day_adv(code, start, end)
        self.assertTrue(len(df) == len(df2), "和QA返回的数据,长度不一致")
        # 两种方式检测numpy数据一致性
        obo = self.differOneByOne(df.data, df2.data)
        self.assertTrue(np.array_equal(df, df2), "和QA返回的数据不一致{}".format(obo))

if __name__ == '__main__':
    unittest.main()
