# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_day, QA_fetch_get_stock_min
from QUANTAXIS.QAUtil import DATABASE
from qaHelper.fetcher import QueryMongodb as qm


class testQuery(TestCase):
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

    def test_get_noData(self):
        code = '600001'  # 不存在的股票代码
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertTrue(isinstance(df, np.ndarray) and df.size == 1, "{}已退市，返回数据数量应该等于0,{}。".format(code, df))


if __name__ == '__main__':
    unittest.main()
