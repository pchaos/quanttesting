# -*- coding: utf-8 -*-

import unittest
import datetime
import pandas as pd
import numpy as np
from .qhtestbase import QhBaseTestCase
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_index_day, QA_fetch_index_min
from qaHelper import F


class TestFetecherFactory(QhBaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._qm = F().createFetcher('index')

    def test_get(self):
        code = '000001'
        days = 365 * 1.2
        start = (datetime.datetime.now() - datetime.timedelta(days)).date()
        end = (datetime.datetime.now() - datetime.timedelta(0)).date()
        df = F().createFetcher('stock').get(code, start, end)
        self.assertIsInstance(df, pd.DataFrame,"应返回类型：pd.DataFrame，实际返回数据类型：{}".format(type(df)))
        self.assertTrue(len(df) > days // 10, "返回数据数量应该大于0。")
        print(df.tail())

    def test_get_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = (datetime.datetime.now() - datetime.timedelta(days)).date()
        end = (datetime.datetime.now() - datetime.timedelta(0)).date()
        qm = self._qm
        df = qm.get(code, start, end)
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        df2 = QA_fetch_index_day(code, start, end, format='pd')
        self.assertTrue(len(df) == len(df2), "和QA返回的数据,长度不一致{}:{}".format(len(df) , len(df2)))
        # 两种方式检测DataFrame数据一致性
        obo = self.differOneByOne(df, df2)
        self.assertTrue(df.equals(df2), "和QA返回的数据不一致{}".format(obo))

    def test_get_noData(self):
        code = '600001'  # 不存在的股票代码
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        qm = self._qm
        df = qm.get(code, start, end)
        self.assertTrue(df is None, "{}已退市，2020年返回数据数量应该等于0,{}。".format(code, df))

    def test_getMin(self):
        code = '000001'
        days = 30 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        qm = self._qm
        df = qm.get(code, start, end, frequence='1min')
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        print(df.tail(10))


if __name__ == '__main__':
    unittest.main()