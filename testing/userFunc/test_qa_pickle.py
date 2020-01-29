# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/28 下午10:19

@File    : test_qa_pickle.py

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

class testQAPickle(unittest.TestCase):
    def test_cal_ret(self):
        # code = '000300'
        fileName ='/tmp/code.pickle'
        try:
            code = decompress_pickle(fileName)
        except Exception as e:
            code = list(qa.QAFetch.QATdx.QA_fetch_get_stock_list('index')['code'][:])
            compressed_pickle(fileName, code)
        days = 600
        rpsday = [20, 50]
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(10)

        # 获取指数数据
        data = qa.QA_fetch_index_day_adv(code, start, end)
        df = data.add_func(cal_ret)
        fileName = '/tmp/data.pickle'
        full_pickle(fileName, data.data)
        data2 = loosen_pickle(fileName)
        self.assertTrue(data.data.equals(data2))
        qadata= qa.QAData(data2)

if __name__ == '__main__':
    unittest.main()
