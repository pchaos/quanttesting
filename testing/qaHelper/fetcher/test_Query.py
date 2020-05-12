# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
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
        print("改变表名：{}".format(qm.collections))

        qm.collections = collections
        self.assertTrue(collections.name == qm.collections.name)


if __name__ == '__main__':
    unittest.main()
