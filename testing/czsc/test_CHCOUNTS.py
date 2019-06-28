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
import datetime


class TestCHCOUNTS(TestCase):
    def test_CHCOUNTS(self):
        code = '000001'
        df = qa.QA_fetch_stock_day_adv(code)
        chCounts = df.to_qfq().add_func(CHCOUNTS)
        self.assertTrue(len(chCounts) > 0, '指标为零')
        print(chCounts)

    def test_CHCOUNTS_codelist(self):
        # code列表
        code = ['000001', '600000', '000858']
        df = qa.QA_fetch_stock_day_adv(code)
        self.assertTrue(len(df.code) == len(code),
                        '有未获取到的代码 {} {}, {}:{}'.format(df.code, code,
                                                       len(df.code), len(code)))

        chCounts = df.to_qfq().add_func(CHCOUNTS)
        self.assertTrue(len(chCounts) > 0, '指标为零')
        print(chCounts)

    def test_CHCOUNTS_indexlist(self):
        # code列表
        code = ['399004', '000016', '399005']
        start = datetime.datetime.now() - datetime.timedelta(250)
        df = qa.QA_fetch_index_day_adv(code, start)
        self.assertTrue(len(df.code) == len(code),
                        '有未获取到的代码 {} {}, {}:{}'.format(df.code, code,
                                                       len(df.code), len(code)))

        chCounts = df.add_func(CHCOUNTS)
        self.assertTrue(len(chCounts) > 0, '指标为零')
        print(chCounts)

