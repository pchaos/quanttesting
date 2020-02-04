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
import pandas as pd
import QUANTAXIS as qa
from userFunc import cal_ret, get_RPS
from userFunc import full_pickle, loosen_pickle, compressed_pickle, decompress_pickle
from userFunc import str2date
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache


class testRPS(unittest.TestCase):
    def setUp(self) -> None:
        fileName = '/tmp/code.pickle'
        try:
            self.code = decompress_pickle(fileName)
        except Exception as e:
            self.code = list(qa.QA_fetch_index_list_adv()['code'][:])
            compressed_pickle(fileName, self.code)

        days = 365 * 1.2
        # days = 365 * 10
        self.start = datetime.datetime.now() - datetime.timedelta(days)
        self.end = datetime.datetime.now() - datetime.timedelta(10)
        try:
            # 获取指数数据
            fileName = '/tmp/data{}.pickle'.format(days)
            # self.data2 = loosen_pickle(fileName)
            self.data2 = decompress_pickle(fileName)
        except Exception as e:
            data = qa.QA_fetch_index_day_adv(self.code, self.start, self.end)
            df = data.add_func(cal_ret)
            compressed_pickle(fileName, data.data)
            self.data2 = decompress_pickle(fileName)
            data2 = self.data2

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
        # 截断数据的数量
        cutted = (len(qadata.data) - len(df)) / len(qadata.code)
        self.assertTrue(19 <= cutted <= 20, "截断数据数量不是默认值（20）：{}".format(cutted))

    def test_cal_ret_withargs(self):
        # code = '000300'
        code = self.code
        rpsday = [20, 50]
        print('code counts: {}'.format(len(code)))
        dfrps = self.getRPS(rpsday)
        print(dfrps.head(10))
        print(dfrps.tail(10))
        print(dfrps[dfrps['RPS20'] > 90][dfrps['RPS50'] > 90][dfrps['RPS50'] > 95].tail(10))
        # 保存计算的RPS

    def getRPS(self, rpsday):
        data = qa.QA_DataStruct_Index_day(self.data2)
        df = data.add_func(cal_ret, *rpsday)
        matching = [s for s in df.columns if "MARKUP" in s]
        self.assertTrue(len(matching) == len(rpsday), '计算周期不在返回的字段中')
        print(df.head())
        # 计算RPS
        dfg = df.groupby(level=0).apply(get_RPS, *rpsday)
        return dfg

    def test_rps_name(self):
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50]
        dfrps = self.getRPS(rpsday)
        theday = datetime.date.today()
        while 1:
            # 定位最近的rps数据
            try:
                df = dfrps.loc[(slice(pd.Timestamp(theday), pd.Timestamp(theday))), :]
                if len(df) > 0:
                    # 排名前10%的指数
                    dftop10 = df.reset_index().head(int(len(df) / 10))
                    print(dftop10)
                    code = list(dftop10['code'])
                    break
                theday = theday - datetime.timedelta(1)
            except Exception as e:
                pass
        indexList = qa.QA_fetch_index_list_adv()
        print(indexList.columns)
        for c in code:
            print(c, indexList.loc[c]['name'])


if __name__ == '__main__':
    unittest.main()
