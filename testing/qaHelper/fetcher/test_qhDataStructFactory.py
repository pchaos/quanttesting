# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_index_day_adv, QA_fetch_index_min_adv
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_index_day, QA_fetch_index_min
from QUANTAXIS.QAData import (QA_DataStruct_Stock_day, QA_DataStruct_Stock_min)
from QUANTAXIS.QAData import (QA_DataStruct_Index_day, QA_DataStruct_Index_min)
from QUANTAXIS.QAUtil import DATABASE
from .qhtestbase import QhBaseTestCase
from qaHelper.fetcher import QueryMongodbStock as qm
from qaHelper.fetcher import QhDataStructFactory as qd

class TestQHDataStructFactory(QhBaseTestCase):
    def test_data_struct(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end)
        if df is not None:
            df = df.set_index(['date', 'code'], drop=True)
        ds =qd().dataStruct(df)
        ds2 = QA_DataStruct_Stock_day(df)

        self.assertIsInstance(ds, QA_DataStruct_Stock_day)
        self.assertIsInstance(ds2, QA_DataStruct_Stock_day)