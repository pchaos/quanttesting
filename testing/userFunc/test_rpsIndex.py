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
import pandas as pd
import os
import matplotlib.pyplot as plt
import QUANTAXIS as qa
from userFunc import cal_ret, get_RPS
from userFunc import full_pickle, loosen_pickle, compressed_pickle, decompress_pickle
from userFunc import RPSIndex
from userFunc import read_zxg
from userFunc import codeInfo
from testing.qaHelper.fetcher.qhtestbase import QhBaseTestCase


class TestRPSIndex(QhBaseTestCase):
    def setUp(self) -> None:
        # 是否删除临时文件
        # self.deltmp = True
        self.deltmp = False

        fileName = '/tmp/indexCode.pickle'
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

    def tearDown(self) -> None:
        try:
            if self.deltmp:
                import os
                myCmd = 'rm /tmp/*.pbz2'
                os.system(myCmd)
        except Exception as e:
            pass

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
        """
        如果测试有错误，删除临时目录pickle文件
        """
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50]
        dfrps = self._getRPS(rpsday, self.data2)
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.rps()
        try:
            self.assertTrue(dfrps.sort_values(dfrps.columns[0], ascending=False).equals(rps),
                            "排序后不相等 {} {}".format(dfrps, rps))
        except:
            self.assertTrue(dfrps.equals(rps), "不相等 {} {}".format(dfrps, rps))
        # self.assertTrue(dfrps.equals(rps), "{} {}".format(dfrps.head(), rps.head()))
        print(rps.tail())
        print(rps.head(20))

    def test_rps_class_multi_rpsday(self):
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50, 120]
        dfrps = self._getRPS(rpsday, self.data2)
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        rps = rpsIndex.rps()
        try:
            self.assertTrue(dfrps.sort_values(dfrps.columns[0], ascending=False).equals(rps),
                            "排序后不相等 {} {}".format(dfrps, rps))
        except:
            self.assertTrue(dfrps.equals(rps), "不相等 {} {}".format(dfrps, rps))
        print(rps.tail())

    def test_rps_class_selectCode(self):
        # 显示rps排名前10%的ETF中文名称
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
        # 显示rps排名前10%的ETF中文名称
        fn = 'zxgETF.txt'
        # code列表
        code = read_zxg(fn)
        rpsday = [20, 50]
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        n = 10
        rps = rpsIndex.rpsTopN(self.end, n)
        self.assertTrue(len(rps) > 0)

        print(rps)
        print("总数： {}".format(len(rps)))
        dfInfo = codeInfo(list(rps.index.levels[1]))
        print(dfInfo.name)

    def test_RPSIndex_rpsTopN2(self):
        # 显示rps排名前10%的ETF中文名称
        fn = 'zxgETF.txt'
        # code列表
        code = read_zxg(fn)
        rpsday = [20, 50]
        end = self.end
        # end = "2020-06-24"
        rpsIndex = RPSIndex(code, self.start, end, rpsday)
        n = 10
        rps = rpsIndex.rpsTopN2(startday=end, percentN=n)
        rps2 = rpsIndex.rpsTopN(end, n)
        self.assertTrue(len(rps) > 0)
        self.assertTrue(len(rps) == len(rps2), "长度不同 {} {}\n{} {}".format(len(rps), len(rps2), rps, rps2))
        try:
            self.assertTrue(rps.sort_values(rps.columns[0], ascending=False).equals(rps2),
                            "排序后不相等 {} {}".format(rps, rps2))
        except:
            self.assertTrue(rps.equals(rps2), "不相等 {} {}".format(rps, rps2))
        print(rps)
        print("总数： {}".format(len(rps)))
        dfInfo = codeInfo(list(rps.index.levels[1]))
        print(dfInfo.name)

    def test_RPSIndex_rpsTopN2_2(self):
        #  一段时间内，显示rps排名前10%的ETF中文名称
        fn = 'zxgETF.txt'
        # code列表
        code = read_zxg(fn)
        rpsday = [20, 50]
        rpsIndex = RPSIndex(code, self.start, self.end, rpsday)
        n = 10
        start = self.end - datetime.timedelta(10)
        rps = rpsIndex.rpsTopN2(startday=start, lastday=self.end, percentN=n)
        self.assertTrue(len(rps) > 0)
        # for day in reversed(rps.index.levels[0]):
        for day in rps.index.levels[0]:
            if day == pd.to_datetime(datetime.date(2020, 6, 30)):
                continue
            print("对比日期： {}".format(day))
            rps2 = rpsIndex.rpsTopN(day, n)
            df = rps.loc[(slice(pd.Timestamp(day), pd.Timestamp(day))), :]
            self.assertTrue(len(df) == len(rps2), "长度不同 {} {}\n{} {}".format(len(df), len(rps2), rps, rps2))
            try:
                obo = self.differOneByOne(df, rps2)
                self.assertTrue(len(obo) == 0, "{} {}".format(df, rps2))
                self.assertTrue(df.equals(rps2), "不相等 {} {}".format(df, rps2))
            except Exception as e:
                df = df.sort_values(by=df.columns[0], ascending=False, inplace=False)
                obo = self.differOneByOne(df, rps2)
                self.assertTrue(len(obo) == 0, "{} {}".format(df, rps2))
                self.assertTrue(df.equals(rps2), "不相等 {} {}".format(df, rps2))
        print(rps)
        print("总数： {}".format(len(rps)))
        dfInfo = codeInfo(list(rps.index.levels[1]))
        print(dfInfo.name)

    def test_readExcel(self):
        """ 找出新进入强势区间的板块
        注意：产生rps文件时，要取前40%的数据
        """
        filename = '/tmp/rpstop.xlsx'
        sheetName = "rps"
        if os.path.exists(filename):
            #
            df = pd.read_excel(filename, sheet_name=sheetName, index_col=[0, 1], converters={'code': str})
            # df = pd.read_excel(filename, sheet_name=shedf['RPS10']> 95 & df['RPS10'].shift() < 95etName + "1", converters={'code': str})
            colname = df.columns[1]
            n = 90
            day = df.index.levels[0][-1]
            dftop = df[(df[colname].groupby(level=1).shift() < n) & (df[colname] >= n)]
            # dfp = dftop.loc[(slice(pd.Timestamp(day), pd.Timestamp(day))), :]
            dfp = dftop.loc[(slice(pd.Timestamp(day), pd.Timestamp(day))), :].reset_index(drop=False)
            dfp['code'] = dfp.code.apply(lambda x: str(x).zfill(6))
            dfp.set_index(['date', 'code'], inplace=True)
            codes = dfp.index.levels[1]
            print(dfp)
            day = df.index.levels[0][-2]
            print("前一日rps强度")
            dfp2 =df.loc[(slice(pd.Timestamp(day), pd.Timestamp(day))), :].reset_index(drop=False)
            dfp2['code'] = dfp2.code.apply(lambda x: str(x).zfill(6))
            dfp2.set_index(['date', 'code'], inplace=True)
            dfp2 = dfp2.loc[(slice(pd.Timestamp(day), pd.Timestamp(day)), codes), :]
            print(dfp2, "\n长度：", len(dfp2))
            self.assertTrue(len(dfp) == len(dfp2), "{} {}".format(len(dfp), len(dfp2)))


if __name__ == '__main__':
    import subprocess

    list_files = subprocess.run(["ls", "-l"])
    print("The exit code was: %d" % list_files.returncode)

    unittest.main()
