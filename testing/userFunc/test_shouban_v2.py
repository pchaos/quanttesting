# -*- coding: utf-8 -*-
"""
2020 01 08 首次涨停（首板）第二版本

"""
from unittest import TestCase
import unittest
#  import datetime
import QUANTAXIS as qa
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache
#  import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from userFunc import shouban, shoubanData, shoubanType


class testShouBan(TestCase):
    """
    首板测试类
    """

    # cache = None

    def setUp(self):
        print("starting")
        qa.QA_util_log_info('首板')
        self.cache = qacache()

    def tearDown(self):
        print("done")
        self.cache = None

    def testshoubanType(self):
        """ 测试首板涨停类型
        2018年8月首板一字涨停测试数据：
    date    code  TYPE
 2018-08-01  002006    10
 2018-08-02  002006    10
 2018-08-13  000705    10
 2018-08-15  000657    10
 2018-08-16  000931    10

 首板类型：
        date    code  TYPE
0  2018-08-01  000909    22
1  2018-08-01  002006    10
2  2018-08-02  000885    22
3  2018-08-03  000780    22
4  2018-08-03  002012    22
5  2018-08-06  000068    23
6  2018-08-06  000610    23
7  2018-08-06  000626    23
8  2018-08-07  000407    23
9  2018-08-08  000852    21
10 2018-08-10  000659    21
11 2018-08-13  000705    10
12 2018-08-14  000023    21
13 2018-08-14  000663    23
14 2018-08-15  000638    22
15 2018-08-15  000657    10
16 2018-08-15  000928    21
17 2018-08-16  000931    10
18 2018-08-20  000561    21
19 2018-08-20  000759    21
20 2018-08-21  000608    21
21 2018-08-21  000815    21
22 2018-08-22  000766    23
23 2018-08-23  000677    22
24 2018-08-23  000913    23
25 2018-08-24  000590    23
26 2018-08-29  000792    24
27 2018-08-29  002034    22
28 2018-08-30  000669    23
29 2018-08-30  000921    22
30 2018-08-31  000593    23
"""
        # 获取股票代码列表（最多num个）
        num = 100
        codelist = self.getCodeList(count=num)
        # 获取股票代码列表对应的日线数据（前复权）
        data = qa.QA_fetch_stock_day_adv(codelist, '2018-04-01', '2018-10-21').to_qfq()
        # 计算首板
        ind = data.add_func(shoubanType)
        # print("ind:", ind)
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        # 获取时间段内的shoubanType计算数据
        df = self.getTimeRange(inc, '2018-08-01', '2018-08-31')
        # 返回首板对应的日期及代码
        df = df[df['TYPE'] > 0].reset_index(drop=False)
        # print("inc QA_DataStruct_Indicators", inc.get_code(codelist[-1]))
        print("首板类型：", df)
        dfresult = df[df['TYPE'] == 10]
        print("首板一字涨停：{}\n".format(type(dfresult)), dfresult)
        # 2018.8 一字板数据
        testingResult = [
            ['2018-08-01', '002006'],
            ['2018-08-13', '000705'],
            ['2018-08-15', '000657'],
            ['2018-08-16', '000931']]
        dftest = pd.DataFrame(columns=['date', 'code'], data=testingResult)
        dftest['date'] = pd.to_datetime(dftest['date'].astype('str'))
        dftest['TYPE'] = [10] * len(dftest)
        print("测试数据", dftest)
        if len(testingResult) == len(dftest):
            # 测试数据数量匹配 验证计算指标是否也匹配
            self.assertTrue(
                dftest[['date', 'code', 'TYPE']].equals(dfresult[['date', 'code', 'TYPE']].reset_index(drop=True)),
                "返回结果不同：\n{} {}".format(dftest, dfresult))

    def testShouBan(self):
        """测试首板 shouban
        """
        # 获取股票代码列表（最多num个）
        num = 100
        codelist = self.getCodeList(count=num)
        # 获取股票代码列表对应的日线数据（前复权）
        data = qa.QA_fetch_stock_day_adv(codelist, '2018-04-01', '2018-10-21').to_qfq()
        # 计算首板
        ind = data.add_func(shouban)
        print("ind:", ind)
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        # 获取时间段内的shouban计算数据
        df = self.getTimeRange(inc, '2018-08-01', '2018-08-31')
        # 返回首板对应的日期及代码
        df = df[df['SB'] == 1].reset_index(drop=False)
        print("inc", inc.get_code(codelist[-1]))
        self.assertTrue(len(ind) > 0, "")
        self.assertTrue(df.dtypes.loc['SB'] == 'int', "返回的数据类型为：{}".format(df.dtypes))

    def testShouBanData(self):
        """测试首板指标 shoubanData
        股票代码,首板日期,次日均涨,位置,次日高幅,次日低幅,次日涨幅,次日量比
000023,2018-08-14,0.0509,-0.1663,0.1002,0.0069,0.0138,2.14
000068,2018-08-06,0.011,-0.1533,0.0593,-0.0386,0.0326,1.45
000407,2018-08-07,0.0377,-0.157,0.0976,-0.0044,0.031,1.83
000561,2018-08-20,0.0051,-0.056,0.0346,-0.0236,0.0189,1.65
000590,2018-08-24,0.0826,-0.111,0.1005,0.0199,0.1005,3.33
000593,2018-08-31,0.0609,-0.1119,0.1003,0.0031,0.1003,2.47
000608,2018-08-21,0.0614,-0.1864,0.0976,0.0081,0.0142,3.9
000610,2018-08-06,0.0888,-0.2149,0.0997,0.0438,0.0997,1.67
000626,2018-08-06,0.061,-0.1797,0.1005,0.0198,0.1005,2.12
000638,2018-08-15,0.0262,-0.2226,0.0998,-0.0327,-0.0327,1.51
        """
        # 获取股票代码列表（最多num个）
        num = 100
        codelist = self.getCodeList(count=num, isTesting=False)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData)
        print("ind:", ind.tail(10))
        inc = qa.QA_DataStruct_Indicators(ind)
        startdate, enddate = '2018-08-01', '2018-08-31'
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = self.getTimeRange(inc, startdate, enddate)
        df.loc[('2018-8-29', codelist[2])]
        df = self.getShouBan(codelist, data, startdate, enddate)
        codelist = sorted(df.code)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData)
        inc = qa.QA_DataStruct_Indicators(ind)
        dfind = self.getTimeRange(inc, startdate, enddate)
        dfind.loc[('2018-8-29', codelist[0])]
        dfind.loc[(df.iloc[1].date.strftime('%Y-%m-%d'), codelist[0])]
        # print("inc", inc.get_code(codelist[-1]))
        df = inc.get_timerange(startdate, enddate, codelist[0])
        dfc = list(df.columns)
        print(df[dfc[:len(dfc) - 1]])
        self.assertTrue(len(df) > 0, "")

    def testShouOutput201808(self):
        """测试2018年8月首板数据
        """
        # 获取股票代码列表（最多num个）
        num = 500
        # codelist = self.getCodeList(count=num)
        codelist = self.getCodeList(count=num, isTesting=False)
        startdate = datetime.strptime('2017-08-01', '%Y-%m-%d')
        endday = '2018-10-21'
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        # 月初 月末
        startdate, enddate = '2018-08-01', '2018-08-31'
        df = self.getShouBan(codelist, data, startdate, enddate)
        codelist = sorted(df.code.drop_duplicates())
        data = data.select_code(codelist)
        ind = data.add_func(shoubanData)
        inc = qa.QA_DataStruct_Indicators(ind)
        dfind = self.getTimeRange(inc, startdate, enddate)
        dfind.loc[('2018-8-29', codelist[2])]
        print("code   次日均涨	位置 次日高幅 次日低里僧幅 次日涨幅 次日量比")
        for i in range(len(df.index) - 1):
            dt = df.iloc[i].date.strftime('%Y-%m-%d')
            if startdate <= dt <= enddate:
                d = dfind.loc[(df.iloc[i].date.strftime('%Y-%m-%d'),
                               df.iloc[i].code)]
                print(df.iloc[i].code, d.JJZF, d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB)
        # 按照代码顺序
        print("code   次日均涨	位置 次日高幅 次日低幅 次日涨幅 次日量比 开盘价 均价")
        alist = []
        for code in codelist:
            d1 = df.loc[df.code == code].loc[df.date.between(startdate, enddate)]
            if len(d1) == 0:
                # 未搜索到对应股票len(a)
                print("未搜索到对应股票:{}".format(df.loc[df.code == code]))
                continue
            d = dfind.loc[(pd.to_datetime(d1.date.values[0]).strftime('%Y-%m-%d'), d1.code.values[0])]
            # d=dfind.loc[(d1.date.strftime('%Y-%m-%d'), d1.code)]
            # print("{} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f}".format(
            # code, d.JJZF, d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB))
            a = ["%.4f" % i for i in d]
            a.append(code)
            alist.append(a)
            # alist.append("{}{}".format(code, ", %.2f"*len(d) % tuple(d)))
            print(code, ", %.4f" * len(d) % tuple(d))

        dfc = pd.DataFrame(alist,
                           columns=["次日均涨", "位置", "次日开盘", "次日高幅", "次日低幅", "次日涨幅", "次日量比", "次日量比v10均", "开盘价", "均价",
                                    "首板类型", "股票代码"])
        # self.roundData(dfc, ['次日量比', '次日量比10均', "开盘价", "均价"], 2)
        # self.roundData(dfc, ['次日均涨', "位置", '次日开盘', "次日高幅", "次日低幅", "次日涨幅"], 4)
        # dfc['首板类型'] = dfc['首板类型'].astype('int')
        dfc.to_csv("/tmp/d.csv", index=False)
        print("inc", inc.get_code(codelist[-1]))
        self.assertTrue(len(ind) > 0, "")

    def getCodeList(self, isTesting=True, count=5000):
        """
        isTesting: 是否使用测试数据
        count： 返回最多结果集数量
        """
        if isTesting:
            # 2018.8首板个股，测试用，减少调试时间
            codelist = ['000023', '000068', '000407', '000561', '000590', '000593', '000608', '000610', '000626',
                        '000638',
                        '000657', '000659', '000663', '000669', '000677', '000705', '000759', '000766', '000780',
                        '000792',
                        '000815', '000852', '000885', '000909', '000913', '000921', '000928', '000931', '002006',
                        '002012',
                        '002034']
        else:
            codelist = qa.QA_fetch_stock_list_adv().code.tolist()
        return codelist[:count]

    def testShouOutput(self):
        # 获取股票代码列表（最多num个）
        num = 8000
        num = 5000
        isTesting = False
        # codelist = self.getCodeList(count=num)
        codelist = self.getCodeList(isTesting=isTesting, count=num)
        # codelist = self.getCodeList(isSB=True)
        # dayslong = ['2018-01-01', '2018-12-31']  # 2018年
        # dayslong = ['2019-01-01', '2019-12-31']  # 2019年
        dayslong = ['2020-01-01', '2020-01-31']
        # 月初 月末
        firstday = self.str2date(dayslong[0])
        date_after_month = firstday + relativedelta(months=1) + relativedelta(days=-1)
        lastday = self.str2date(dayslong[1])
        # 获取起始时间之前一年的数据，否则可能因停牌过长不能计算起涨点相对60均线涨幅
        data = qa.QA_fetch_stock_day_adv(codelist, firstday - relativedelta(months=7),
                                         lastday + relativedelta(months=2)).to_qfq()
        while date_after_month <= lastday:
            # 每个月计算单独一次
            print("计算首板... {}-{}".format(firstday, date_after_month))
            df = self.getShouBan(codelist, data, startday=firstday, endday=date_after_month)
            if len(df) == 0:
                print("no data {}".format(self.date2str(firstday)))
                date_after_month, firstday = self.nextMonth(firstday)
                continue
            # 按照代码顺序
            codelist = sorted(df.code.drop_duplicates())
            startdate, enddate = self.date2str(firstday), self.date2str(date_after_month)
            print("首板指标...")
            dataInd = data.select_code(codelist).select_time_with_gap(date_after_month + relativedelta(months=1), 9999,
                                                                      "<=")
            sblist = self.getshoubanInd(codelist, df, dataInd, startdate, enddate)
            date_after_month, firstday = self.nextMonth(firstday)
            self.assertTrue((isTesting or len(sblist) >= 0) or len(sblist) > 0, "首板个数为零")

    def nextMonth(self, firstday):
        """计算firstday的下一个月
        返回下月底、下月初
        """
        firstday = firstday + relativedelta(months=1)
        date_after_month = firstday + relativedelta(months=1) + relativedelta(days=-1)
        return date_after_month, firstday

    def str2date(self, dayStr):
        if isinstance(dayStr, str):
            return datetime.strptime(dayStr, '%Y-%m-%d')
        else:
            return dayStr

    def getshoubanInd(self, codelist, df, data, startdate, enddate):
        print(startdate, enddate)
        # inc = self.cache.get('shoubanDataIndcator')
        # if inc is None:
        if len(data) == 0:
            # 没有数据则返回空
            return pd.DataFrame()
        ind = data.add_func(shoubanData)
        inc = qa.QA_DataStruct_Indicators(ind)
        # self.cache.set('shoubanDataIndcator', inc)
        # ind = data.add_func(shoubanData)
        # inc = qa.QA_DataStruct_Indicators(ind)
        print("code   次日均涨	位置 次日开盘 次日高幅 次日低幅 次日涨幅 次日量比 次日量比10均 首板类型")
        alist = []
        edate = self.date2str(self.str2date(enddate) + relativedelta(days=10))
        for code in codelist:
            # dfind = self.getTimeRange(inc, startdate, self.str2date(enddate) + relativedelta(days=15), code)
            dfind = self.getTimeRange(inc, startdate, self.str2date(enddate), code)
            d1 = df.loc[df.code == code]
            if (len(d1)) == 0:
                continue
            assert len(d1) == 1, "首板个数：{}".format(len(d1))
            # 首板日期
            d1date = pd.to_datetime(d1.date.values[0])
            if not (self.str2date(startdate) <= d1date <= self.str2date(enddate)):
                continue
            d = dfind.loc[(d1date.strftime('%Y-%m-%d'), d1.code.values[0])]
            # d=dfind.loc[(d1.date.strftime('%Y-%m-%d'), d1.code)]
            # print("{} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f}".format(dfind
            # code, d.JJZF, d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB, d.CRLBV10))
            # 涨停板位置
            a = [item for item in d]
            a.insert(0, code)
            a.insert(1, self.date2str(d1date))
            alist.append(a)
            print(code, ", %.4f" * len(d) % tuple(d))
        dfc = pd.DataFrame(alist,
                           columns=["股票代码", "首板日期", "次日均涨", "位置", "次日开盘", "次日高幅", "次日低幅", "次日涨幅", "次日量比", "次日量比10均",
                                    "开盘价", "均价", "首板类型"])
        self.roundData(dfc, ['次日量比', '次日量比10均', "开盘价", "均价"], 2)
        self.roundData(dfc, ['次日均涨', "位置", '次日开盘', "次日高幅", "次日低幅", "次日涨幅"], 4)
        dfc['首板类型'] = dfc['首板类型'].astype('int')
        dfc.to_csv("/tmp/sb{}.csv".format(self.date2str(startdate)), index=False)
        # print("inc", inc.get_code(codelist[-1]))
        # self.assertTrue(len(ind) > 0, "{}-{} 无数据".format(startdate, enddate))
        return alist

    def roundData(self, dfc, columns, n=2):
        """数据四舍五入道小数n位
        """
        if isinstance(columns, str):
            dfc[columns] = dfc[columns].apply(lambda x: round(x, n))
        elif isinstance(columns, list):
            for col in columns:
                dfc[col] = dfc[col].apply(lambda x: round(x, n))

    def getTimeRange(self, inc, startdate, enddate, code=None, isBugfixed=False):
        if isBugfixed:
            # 源码中bug修复时，使用以下代码
            dfindicator = inc.get_timerange(startdate, enddate, code)  # QAUANTAXIS源码中有bug，code不起作用

        else:
            # 源码中bug未修复时，使用以下代码
            if code is None:  # QAUANTAXIS源码中有bug，code为空时，不返回数据
                dfindicator = inc.data.loc[(slice(pd.Timestamp(startdate),
                                                  pd.Timestamp(self.str2date(enddate)))), :]
            else:
                dfindicator = inc.data.loc[(slice(pd.Timestamp(startdate),
                                                  pd.Timestamp(self.str2date(enddate))), code),
                              :]
        return dfindicator

    def getShouBan(self, codelist, qaData, startday='2018-01-01', endday='2018-01-31'):
        """计算首板指标
        """
        startday = self.date2str(startday)
        endday = self.date2str(endday)
        inc = self.cache.get('shoubanIndcator')
        if inc is None:
            if len(qaData) == 0:
                # 没有数据则返回空
                return pd.DataFrame()
            ind = qaData.add_func(shouban)
            inc = qa.QA_DataStruct_Indicators(ind)
            self.cache.set('shoubanIndcator', inc)

        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = self.getTimeRange(inc, startday, endday)
        df = df[df['SB'] == 1].reset_index(drop=False)
        return df

    def date2str(self, startday):
        if isinstance(startday, datetime):
            startday = startday.strftime('%Y-%m-%d')
        return startday

    def testAddPercent(self):
        """保存的csv重新计算（原百分数数字，变为纯数字）后保存
            保存的文件名后加上“.num"
        """
        import os
        path = '/tmp'

        files = []
        # 获取path目录下csv文件列表
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.csv' in file:
                    if not file.endswith('.csv#'):
                        files.append(os.path.join(r, file))

        if len(files) > 0:
            # "次日均涨", "位置", "次日高幅", "次日低幅", "次日涨幅"除以100，另存为"原文件名.num.csv“
            for f in files:
                print(f)
                df = pd.read_csv(f, converters={'股票代码': str})
                df['次日均涨'] = round(df['次日均涨'] / 100, 4)
                df['位置'] = round(df['位置'] / 100, 4)
                df['次日高幅'] = round(df['次日高幅'] / 100, 4)
                df['次日低幅'] = round(df['次日低幅'] / 100, 4)
                df['次日涨幅'] = round(df['次日涨幅'] / 100, 4)
                df.to_csv("{}.num.csv".format(os.path.splitext(f)[0]), index=False)

            self.assertTrue(len(files) > 0)


if __name__ == '__main__':
    unittest.main()
