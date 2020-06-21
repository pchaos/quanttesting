# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/28 下午10:19

@File    : test_xrps.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import datetime
import pandas as pd
import QUANTAXIS as qa
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache
from userFunc import cal_ret, get_RPS
from userFunc import full_pickle, loosen_pickle, compressed_pickle, decompress_pickle
from userFunc import str2date
from userFunc import read_zxg
from userFunc import setdiff_sorted
from userFunc.jqtestbase import TestingBase
from testing.qaHelper.fetcher.qhtestbase import QhBaseTestCase


# class testRPS(unittest.TestCase):
class testRPS(QhBaseTestCase):
    def setUp(self) -> None:
        fileName = '/tmp/code.pickle'
        try:
            self.code = decompress_pickle(fileName)
        except Exception as e:
            self.code = list(qa.QA_fetch_index_list_adv()['code'][:])
            compressed_pickle(fileName, self.code)

        days = 300 * 1.2
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
        dfrps = self._getRPS(rpsday, self.data2)
        print(dfrps.head(10))
        print(dfrps.tail(10))
        print(dfrps[dfrps['RPS20'] > 90][dfrps['RPS50'] > 90][dfrps['RPS50'] > 95].tail(10))
        # 保存计算的RPS

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

    def test_rps_name(self):
        # 显示rps排名前10%的中文名称
        code = self.code
        rpsday = [20, 50]
        dfrps = self._getRPS(rpsday, self.data2)
        theday = datetime.date.today()
        dftop10 = self._getRPSTopN(code, dfrps, theday)
        code = list(dftop10['code'])
        indexList = qa.QA_fetch_index_list_adv()
        print(indexList.columns)
        for c in code:
            print(c, indexList.loc[c]['name'])

    def _getRPSTopN(self, code, dfrps, theday, n=10):
        """RPS排名前N%的数据"""
        while 1:
            # 定位最近的rps数据
            dfn = []
            try:
                df = dfrps.loc[(slice(pd.Timestamp(theday), pd.Timestamp(theday))), :]
                if len(df) > 0:
                    # 排名前N%的指数
                    for col in df.columns:
                        dfn.append(df.sort_values(by=col, ascending=False).reset_index().head(int(len(df) / (100 / n))))
                    dftopn = pd.concat(dfn, ignore_index=True).drop_duplicates()
                    # print(dftopn)
                    break
                theday = theday - datetime.timedelta(1)
            except Exception as e:
                theday = theday - datetime.timedelta(1)
        return dftopn

    def _getRPSTopN2(self, code, dfrps, start, end=None, n=10):
        """RPS排名前N%的数据"""
        while 1:
            # 定位最近的rps数据
            df = pd.DataFrame()
            try:
                if end is None:
                    end = start
                # df = dfrps.loc[(slice(pd.Timestamp(start), pd.Timestamp(end)), slice(None)), :]
                df = dfrps.sort_index().loc[(slice(pd.Timestamp(start), pd.Timestamp(end)), slice(None)), :]
                if len(df) > 0:
                    break
                start = start - datetime.timedelta(1)
            except Exception as e:
                start = start - datetime.timedelta(1)
        return df.drop_duplicates()

    def test_rps_name_exclude(self):
        """880035 创业涨跌
880025 中小涨跌
880005 涨跌家数
880928 抗流感
880655 医疗器械
880630 半导体
880410 医药商业
880654 医药商业
000857 500医药
880880 近期强势
399676 深医药EW
880491 半导体
399976 CS新能车
880653 生物制品
399441 生物医药
880402 生物制药
000121 医药主题
000131 上证高新
399993 CSWD生科
880773 最近闪崩
880878 百元股
880403 中成药
880652 中药
399803 工业4.0
000075 医药等权
399678 深次新股
880398 医疗保健
399674 深A医药
399667 创业板G
880920 免疫治疗
399989 中证医疗
880927 抗癌
000863 CS精准医
000109 380医药
880913 基因概念
399685 深成医药
880966 消费电子
880557 生物疫苗
000991 全指医药
880952 芯片
880400 医药
399618 深证医药
880024 中小均价
399647 深医药50
399386 1000医药
000037 上证医药
000841 800医药
399295 创业蓝筹
000808 医药生物
000933 中证医药
880642 视听器材
399673 创业板50
880854 预高送转
399417 新能源车
880902 特斯拉
399249 综企指数
880716 光刻机
399808 中证新能
880534 锂电池
880556 IP变现
880961 小米概念
399811 CSSW电子
880608 动物保健
880870 两年新股
399412 国证新能
399643 创业新兴
880836 配股股
399635 创业板EW
399326 成长40
880944 无人驾驶
880574 苹果概念
399017 SME创新
399638 深证环保
880935 智能电视
399691 创业专利
399804 中证体育
880590 网络游戏
880942 虚拟现实
399682 深成工业
880780 融资增加
399388 1000信息
399016 深证创新
399339 深证科技
排名靠前的数量：83
"""
        # 显示rps排名前10%的中文名称(去除某些品种)
        code = self.code
        codeexclude = read_zxg('zxgExclude.txt')
        # 排除某些股票
        code = setdiff_sorted(code, codeexclude)
        rpsday = [20, 50]
        # rpsday = [20, 50, 120]
        data = self.data2
        data = data.loc[(slice(None), code), :]
        dfrps = self._getRPS(rpsday, data)
        theday = datetime.date.today()
        # rps排名前5%
        dftopn = self._getRPSTopN(code, dfrps, theday, n=5)
        codetop = list(dftopn['code'])
        indexList = qa.QA_fetch_index_list_adv()
        for c in codetop:
            # 打印股票代码及中文名
            print(c, indexList.loc[c]['name'])
        print("排名靠前的数量：{}".format(len(codetop)))
        # 插入中文名
        dftopn.insert(2, 'name', dftopn['code'].apply(lambda x: indexList.loc[x]['name']))
        print(dftopn.head(10))
        # 保存到文件
        dftopn.to_csv('/tmp/rpstop.csv', encoding='utf-8', index=False)

    def test_rps_name_exclude_topn2(self):
        """
        """
        # 显示rps排名前10%的中文名称(去除某些品种)
        code = self.code
        codeexclude = read_zxg('zxgExclude.txt')
        # 排除某些股票
        code = setdiff_sorted(code, codeexclude)
        rpsday = [20, 50]
        # rpsday = [20, 50, 120]
        data = self.data2
        data = data.loc[(slice(None), code), :]
        dfrps = self._getRPS(rpsday, data)
        theday = datetime.date.today()
        n = 5
        dfrpstopn2 = pd.concat([dfrps.loc[(dfrps[item] >= 100 - n)] for item in dfrps.columns]).sort_index()
        # rps排名前5%
        dftopn = self._getRPSTopN(code, dfrps, theday, n=n)
        codetop = list(dftopn['code'])
        # index列表 用于处理中文名称
        indexList = qa.QA_fetch_index_list_adv()
        # for c in codetop:
        #     # 打印股票代码及中文名
        #     print(c, indexList.loc[c]['name'])
        # print("排名靠前的数量：{}".format(len(codetop)))
        # 插入中文名
        dftopn.insert(2, 'name', dftopn['code'].apply(lambda x: indexList.loc[x]['name']))
        print(dftopn.head(10))
        # dfrpstopn2 = self._getRPSTopN2(code, dfrpstopn2, theday, theday, n)
        dfrpstopn2 = self._getRPSTopN2(code, dfrpstopn2, theday, theday, n)
        dftopn2 = dfrpstopn2.reset_index()
        dftopn2.insert(2, 'name', dftopn2['code'].apply(lambda x: indexList.loc[x]['name']))
        codetop2 = list(dftopn2['code'])
        difflist = self.diffList(codetop, codetop2)
        self.assertTrue(len(difflist) <= 1, "代码差别： {}".format(difflist))
        if len(difflist) > 0:
            print(difflist)
            if difflist in codetop:
                dftopn= dftopn[dftopn['code'] != difflist[0]]
            else:
                dftopn2= dftopn2[dftopn2['code'] != difflist[0]].reset_index(drop=True)

        obo = self.differOneByOne(dftopn2.sort_values(['code']), dftopn.sort_values(['code']).reset_index(drop=True))
        self.assertTrue(len(obo) == 0, "{}".format(obo))


if __name__ == '__main__':
    unittest.main()
