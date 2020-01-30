# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/28 下午10:19

@File    : test_rps.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import datetime
import QUANTAXIS as qa
from userFunc import cal_ret
from userFunc import full_pickle, loosen_pickle, compressed_pickle, decompress_pickle
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache


class testRPS(unittest.TestCase):
    def setUp(self) -> None:
        fileName = '/tmp/code.pickle'
        try:
            self.code = decompress_pickle(fileName)
        except Exception as e:
            self.code = list(qa.QA_fetch_index_list_adv()['code'][:])
            compressed_pickle(fileName, self.code)

        # days = 365 * 2
        days = 365 * 10
        self.start = datetime.datetime.now() - datetime.timedelta(days)
        self.end = datetime.datetime.now() - datetime.timedelta(10)
        try:
            # 获取指数数据
            fileName = '/tmp/data{}.pickle'.format(days)
            self.data2 = loosen_pickle(fileName)
        except Exception as e:
            data = qa.QA_fetch_index_day_adv(self.code, self.start, self.end)
            df = data.add_func(cal_ret)
            full_pickle(fileName, data.data)
            self.data2 = loosen_pickle(fileName)
            data2 = loosen_pickle(fileName)

    def tearDown(self) -> None:
        pass

    def test_cal_ret(self):
        # code = '000300'
        code = self.code

        qadata = qa.QA_DataStruct_Index_day(self.data2)
        df2 = qadata.add_func(cal_ret)
        start, end = self.start, self.end
        data = qa.QA_fetch_index_day_adv(code, start, end)
        df = data.add_func(cal_ret)
        self.assertTrue(df.equals(df2))
        print(df.head(), "\n", df2.head())

    def test_cal_ret_withargs(self):
        # code = '000300'
        code = self.code
        rpsday = [20, 50]
        data = qa.QA_DataStruct_Index_day(self.data2)
        df = data.add_func(cal_ret, *rpsday)
        matching = [s for s in df.columns if "MARKUP" in s]
        self.assertTrue(len(matching) == len(rpsday), '计算周期不在返回的字段中')
        print(df.head())


if __name__ == '__main__':
    unittest.main()
