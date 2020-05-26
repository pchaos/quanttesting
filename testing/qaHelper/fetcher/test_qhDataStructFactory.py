# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_index_day_adv, QA_fetch_index_min_adv
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_index_day, QA_fetch_index_min
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_future_day, QA_fetch_future_min
from QUANTAXIS.QAData import (QA_DataStruct_Stock_day, QA_DataStruct_Stock_min)
from QUANTAXIS.QAData import (QA_DataStruct_Index_day, QA_DataStruct_Index_min)
from QUANTAXIS.QAData import (QA_DataStruct_Future_day, QA_DataStruct_Future_min)
from QUANTAXIS.QAUtil import DATABASE
from .qhtestbase import QhBaseTestCase
from qaHelper.fetcher import QueryStock as qm
from qaHelper.fetcher import QueryIndex as qmi
# from qaHelper.fetcher import QueryMongodbFuture as qmf
from qaHelper.fetcher import QhDataStructFactory as qd


class TestQhDataStructFactory(QhBaseTestCase):
    def test_data_struct_stock(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        if df is not None:
            df = df.set_index(['date', 'code'], drop=True)
        ds = qd().dataStruct(df)
        ds2 = QA_DataStruct_Stock_day(df)

        self.assertIsInstance(ds, QA_DataStruct_Stock_day)
        self.assertIsInstance(ds2, QA_DataStruct_Stock_day)

    def test_data_struct_min_stock(self):
        code = '000001'
        days = 10 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end, frequence='1min')
        if df is not None and len(df.index.names) == 1:
            df = df.set_index(['date', 'code'], drop=True)
        ds = qd(frequence=8).dataStruct(df)
        ds2 = QA_DataStruct_Stock_min(df)

        self.assertIsInstance(ds, QA_DataStruct_Stock_min)
        self.assertIsInstance(ds2, QA_DataStruct_Stock_min)

    def test_data_struct_index(self):
        """指数（或etf）DataStruture
        """
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qmi.get(code, start, end)
        if df is not None:
            df = df.set_index(['date', 'code'], drop=True)
        ds = qd(type='index').dataStruct(df)
        ds2 = QA_DataStruct_Index_day(df)

        self.assertIsInstance(ds, QA_DataStruct_Index_day)
        self.assertIsInstance(ds2, QA_DataStruct_Index_day)

    # def test_data_struct_future(self):
    #     """期货（或etf）DataStruture
    #     """
    #     code = 'RUL8'
    #     days = 365 * 1.2
    #     start = datetime.datetime.now() - datetime.timedelta(days)
    #     end = datetime.datetime.now() - datetime.timedelta(0)
    #     df = qmf.get(code, start, end)
    #     if df is not None:
    #         df = df.set_index(['date', 'code'], drop=True)
    #     ds = qd(type='future').dataStruct(df)
    #     ds2 = QA_DataStruct_Future_day(df)
    #
    #     self.assertIsInstance(ds, QA_DataStruct_Future_day)
    #     self.assertIsInstance(ds2, QA_DataStruct_Future_day)


if __name__ == '__main__':
    unittest.main()
