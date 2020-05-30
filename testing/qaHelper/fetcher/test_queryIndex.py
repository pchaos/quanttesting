# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_index_day_adv, QA_fetch_index_min_adv
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_index_day, QA_fetch_index_min
from QUANTAXIS.QAData import (QA_DataStruct_Index_day, QA_DataStruct_Index_min)
from QUANTAXIS.QAUtil import DATABASE
from qaHelper.fetcher import QueryIndex as qm
from .qhtestbase import QhBaseTestCase


class testQueryIndex(QhBaseTestCase):
    def test_collections(self):
        collections = qm.collectionsDay
        self.assertTrue(collections.name == DATABASE.index_day.name, "数据表名应该相同")

        qm.collectionsMin = DATABASE.index_min
        self.assertTrue(collections.name != qm.collectionsMin.name)
        print("原始表名：{}，\n改变后表名：{}".format(collections, qm.collectionsMin))

        qm.collectionsDay = collections
        self.assertTrue(collections.name == qm.collectionsDay.name)

    def test_get(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertIsInstance(df, pd.DataFrame,"应返回类型：pd.DataFrame，实际返回数据类型：{}".format(type(df)))
        self.assertTrue(len(df) > days // 10, "返回数据数量应该大于0。")
        print(df.tail())

    def test_get_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = (datetime.datetime.now() - datetime.timedelta(days)).date()
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        df2 = QA_fetch_index_day(code, start, end, format='pd')
        self.assertTrue(len(df) == len(df2), "和QA返回的数据,长度不一致{}:{}".format(len(df) , len(df2)))
        # 两种方式检测DataFrame数据一致性
        obo = self.differOneByOne(df, df2)
        # # df df2之间的区别
        # df2 = df2.loc[:,
        #       [
        #           'code',
        #           'open',
        #           'high',
        #           'low',
        #           'close',
        #           'volume',
        #           'amount',
        #           'date'
        #       ]]
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
        self.assertTrue(len(df[df['close'] > 1000]) > days // 10)
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
        df2 = QA_fetch_index_min(code, start, end=end, format='pd', frequence='1min')
        # todo df的长度比df2长。未找出原因
        data1, data2 = df, df2
        self.assertTrue(len(data1) == len(data2), "和QA返回的分钟线数据长度不一致:{}:{}".format(len(data1), len(data2)))
        if len(data1) > len(data2):
            print("array1f的长度比array2长")
            data1 = data1[-len(data2):]
        elif len(data1) < len(data2):
            print("array2的长度比array1长")
            data2 = data2[-len(data1):]
        obo = self.differOneByOne(data1, data2)
        self.assertTrue(data1.equals(data2),
                        "和QA返回的分钟线数据不一致:{}".format(obo))

    def test_getAdv(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.getAdv(code, start, end)
        self.assertIsInstance(df, QA_DataStruct_Index_day,"应返回类型：QA_DataStruct_Stock_day，实际返回数据类型：{}".format(type(df)))
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
        df2 = QA_fetch_index_day_adv(code, start, end)
        self.assertTrue(len(df.data) == len(df2.data), "和QA返回的数据,长度不一致{} {}".format(len(df.data) , len(df2.data)))
        # 两种方式检测numpy数据一致性
        obo = self.differOneByOne(df.data, df2.data)
        self.assertTrue(df.data.equals(df2.data), "和QA返回的数据不一致{}".format(obo))

    def test__get_getNumpy(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        self.assertIsInstance(df, pd.DataFrame, "应返回类型：pd.DataFrame，实际返回数据类型：{}".format(type(df)))
        arrary = qm.getNumpy(code, start, end)
        self.assertIsInstance(arrary, np.ndarray, "应返回类型：np.ndarray，实际返回数据类型：{}".format(type(arrary)))
        self.assertTrue(len(arrary) > days // 10, "返回数据数量应该大于0。")

if __name__ == '__main__':
    unittest.main()