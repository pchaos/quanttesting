# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QAQuery import  QA_fetch_stock_day, QA_fetch_stock_min
from QUANTAXIS.QAUtil import DATABASE
from qaHelper.fetcher import QueryMongodb as qm
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

    def test_get_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        array1 = qm.get(code, start, end)
        self.assertTrue(len(array1) > 0, "返回数据数量应该大于0。")
        array2 = QA_fetch_stock_day(code, start, end)
        self.assertTrue(len(array1) == len(array2), "和QA返回的数据,长度不一致")
        # 两种方式检测numpy数据一致性
        self.assertTrue(np.array_equal(array1, array2), "和QA返回的数据不一致{}".format(""))
        self.assertTrue((array1 == array2).all(), "和QA返回的数据不一致{}".format(np.setdiff1d(array1, array2, assume_unique=True)))


    def test_get_noData(self):
        code = '600001'  # 不存在的股票代码
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertTrue(isinstance(df, np.ndarray) and df.size == 1, "{}已退市，返回数据数量应该等于0,{}。".format(code, df))


if __name__ == '__main__':
    unittest.main()
