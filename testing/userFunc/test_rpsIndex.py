# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/15 下午2:21

@File    : test_rpsIndex.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import datetime
import time
import matplotlib.pyplot as plt
import QUANTAXIS as qa
from userFunc import cal_ret, get_RPS
from userFunc import full_pickle, loosen_pickle, compressed_pickle, decompress_pickle
from userFunc import RPSIndex
from userFunc import read_zxg


class TestRPSIndex(unittest.TestCase):
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
        self.end = datetime.datetime.now() - datetime.timedelta(0)
        fileName = '/tmp/data{}.pickle'.format(days)
        self.data2 = self.getIndexCalret(fileName, self.code, self.start, self.end)

    def getIndexCalret(self, readFromfile, code, startDate, endDate):
        try:
            # 获取指数数据
            dataCalret = decompress_pickle(readFromfile)
        except Exception as e:
            data = qa.QA_fetch_index_day_adv(code, startDate, endDate)
            df = data.add_func(cal_ret)
            compressed_pickle(readFromfile, data.data)
            dataCalret = decompress_pickle(readFromfile)
            data2 = dataCalret
        return dataCalret

    def test_rps_class(self):
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50]
        dfrps = self._getRPS(rpsday, self.data2)
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.rps()
        self.assertTrue(dfrps.equals(rps), "{} {}".format(dfrps.head(), rps.head()))

    def test_rps_class_multi_rpsday(self):
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50, 120]
        dfrps = self._getRPS(rpsday, self.data2)
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.rps()
        self.assertTrue(dfrps.equals(rps), "RPS计算不匹配：\n{} {}".format(dfrps.head(), rps.head()))
        print(rps.tail())

    def test_rps_class_selectCode(self):
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50, 89]
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.selectCode(code[0])
        print(rps.tail())
        rps.plot()
        rps.plot(x='RPS20', y='RPS{}'.format(rpsday[1]))
        rps.plot(x='RPS20', y='RPS{}'.format(rpsday[2]))
        plt.show()

    def _getRPS(self, rpsday, dataFrame):
        # data = qa.QA_DataStruct_Index_day(self.data2)
        data = qa.QA_DataStruct_Index_day(dataFrame)
        df = data.add_func(cal_ret, *rpsday)
        matching = [s for s in df.columns if "MARKUP" in s]
        self.assertTrue(len(matching) == len(rpsday), '计算周期不在返回的字段中')
        print(df.head())
        # 计算RPS
        dfg = df.groupby(level=0).apply(get_RPS, *rpsday)
        return dfg

    def test_rps_ETF_selectCode(self):
        # 显示rps排名前10%的中文名称
        fn = 'zxgETF.txt'
        # code列表
        code = read_zxg(fn)
        rpsday = [20, 50]
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.selectCode(code)
        # print(rps.tail())
        print(rps)

    def test_rps_ETFTOPN(self):
        # 显示rps排名前10%的中文名称
        fn = 'zxgETF.txt'
        # code列表
        code = read_zxg(fn)
        rpsday = [20, 50]
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.rpsTopN(self.end)
        # print(rps.tail())

        # rps['PRS']= rps['']
        print(rps)

if __name__ == '__main__':
    unittest.main()
