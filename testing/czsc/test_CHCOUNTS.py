# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_CHCOUNTS
   Description :
   Author :       pchaos
   date：          2019/6/21
-------------------------------------------------
   Change Activity:
                   2019/6/21:
-------------------------------------------------
"""
from unittest import TestCase
from czsc.chCounts import *


class TestCHCOUNTS(TestCase):
    def test_CHCOUNTS(self):
        code = '000001'
        df = qa.QA_fetch_stock_day_adv(code)
        chCounts = df.to_qfq().add_func(CHCOUNTS)
        self.assertTrue(len(chCounts) > 0, '指标为零')
        print(chCounts)
