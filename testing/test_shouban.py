# -*- coding: utf-8 -*-
from unittest import TestCase
import unittest
#  import datetime
import QUANTAXIS as qa
#  import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def shouban(dataFrame):
    """ 首板

    """
    close = dataFrame['close']
    tj1 = close > qa.REF(close, 1) * 1.098
    tj2 = qa.COUNT(tj1, 30) == 1
    # 涨停 并且 最近30交易日涨停次数为1，则标记1,否则标记0
    sb = pd.DataFrame({'tj1': tj1, 'tj2': tj2}).apply(lambda x: 1 if x['tj1'] and x['tj2'] else 0, axis=1)
    # sb = tj1 && tj2 && qa.COUNT(CLOSE) > 50
    dict = {'SB': sb}
    return pd.DataFrame(dict)


def shoubanData_v1(dataFrame):
    """ 首板指标计算
    次日均涨	位置 次日高幅 次日低幅 次日涨幅 次日量比
    JJZF, WZ, ZGZF, ZDDF, ZF, LB
    位置：涨停日收盘价相对60日最低收盘价涨幅（c涨停/C60日最低-1）*100%
    次日量比：v/ma（v，10） ;v10日均算的是涨停日
    """
    close = dataFrame['close']
    H = dataFrame['high']
    L = dataFrame['low']
    V = dataFrame['volume']
    AMO = dataFrame['amount']
    # 位置
    wz = (close / qa.MA(close, 120) - 1) * 100
    # 次日涨幅
    zf = round((close / qa.REF(close, 1) - 1) * 100, 2);
    # 次日高幅
    zgzf = (H / qa.REF(close, 1) - 1) * 100;
    # 次日跌幅
    zddf = (L / qa.REF(close, 1) - 1) * 100;
    # 量比
    lb = round(V / qa.REF(V, 1), 2);
    # 次日均涨
    cjjj = AMO / V / 100;
    jjzf = (cjjj / qa.REF(close, 1) - 1) * 100;
    dict = {'JJZF': jjzf, 'WZ': wz, 'ZGZF': zgzf, 'ZDDF': zddf, 'ZF': zf, 'LB': lb}
    return pd.DataFrame(dict)


def shoubanType(dataFrame):
    """首板类型（首次涨停，k线形态）
    0、非首板相关
    10、一字涨停（涨停第一天绝对一字涨停收盘，O=C=H=L>ref(c,1)*1.098）
    21、实体阳线涨停，涨停次日收十字，或收长上影线且涨幅小于3%， 或收长下影线且涨幅小于2%
    22、实体阳线涨停，涨停次日收阴实线
    23、实体阳线涨停，涨停次日收实体阳线或涨幅大于3%
    24、实体阳线涨停，涨停次日孕育k线（未创新高新低，H<ref(H,1) and L>ref(L,1)）
    30、其他类型
    """

    def sbtype(x):
        # 计算首板第一天、第二天的类型。一字板在首板第一天判断，其他类型在首板第二天判断
        if x.SB == 0:
            # 非首板 不用判断类型
            return 0
        # 首板
        if x.zf > 1.03:
            # 涨幅大于3%
            if x.zf > 1.098 and x.H == x.L:
                # 一字涨停
                return 10
            else:
                return 23
        elif x.zf > 1.0:
            # 收盘价介于0%～3%之间
            return 21
        elif x.H <= x.preH and x.L >= x.preL:
            # 收盘价小于前一天收盘价
            return 24
        elif x.close > x.preL:
            return 22
        else:
            return 30

    def sbtype2(x):
        # 合并首板类型技术指标到首板当天
        if x.t1 == 0 or x.t1 == 10:
            # 非首板 不用判断类型
            if x.t1 == 10 and x.t2 != 0:
                # 连续涨停的，第二个不用标记
                print("", x.t2)
                return 10
            else:
                return 0
        else:
            # 复制首板第二天
            return x.t2

    close = dataFrame['close']
    op = dataFrame['open']  # 开盘价
    # 首板
    tj1 = close > qa.REF(close, 1) * 1.098
    tj2 = qa.COUNT(tj1, 30) == 1
    # 涨停 并且 最近30交易日涨停次数为1，则标记1,否则标记0
    sb = pd.DataFrame({'tj1': tj1, 'tj2': tj2}).apply(lambda x: 1 if x['tj1'] and x['tj2'] else 0, axis=1)
    # 首板及首板第二天标记为1
    # dict = {'SB': sb + sb.shift(-1).fillna(0)}

    H = dataFrame['high']
    L = dataFrame['low']
    # 首板第二天收盘价涨幅
    zf = close / qa.REF(close, 1)
    # 计算首板第一天、第二天的类型
    sbt = pd.DataFrame({'zf': zf, 'H': H, "L": L, "preH": qa.REF(H, 1), "preL": qa.REF(L, 1), 'close': close,
                        'SB': sb + sb.shift(1).fillna(0)}).apply(lambda row: sbtype(row),
                                                                 axis=1)
    # 合并首板类型技术指标到首板当天
    sbt = pd.DataFrame({'t1': sbt, 't2': sbt.shift(-1)}).apply(lambda row: sbtype2(row),
                                                               axis=1)
    dict = {'TYPE': sbt}
    # 返回整数类型
    df = pd.DataFrame(dict).fillna(0).astype('int')
    # 首板次日开盘涨幅
    df['CRKFZF'] = (op / qa.REF(close, 1) - 1).shift(-1)
    return df


class testShouBan(TestCase):
    """
    首板
    """

    def setup(self):
        print("starting")
        qa.QA_util_log_info('首板')

    def teardown(self):
        print("done")

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
        # 获取股票代码列表（5个或者更多）
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
        # 获取股票代码列表（5个或者更多）
        codelist = self.getCodeList(count=5)
        # 获取股票代码列表对应的日线数据（前复权）
        data = qa.QA_fetch_stock_day_adv(codelist, '2018-04-01', '2018-10-21').to_qfq()
        # 计算首板
        ind = data.add_func(shouban)
        print("ind:", ind)
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        # 获取时间段内的shouban计算数据
        # df = inc.get_timerange('2018-08-01', '2018-08-31')
        df = self.getTimeRange(inc, '2018-08-01', '2018-08-31')
        # 返回首板对应的日期及代码
        df = df[df['SB'] == 1].reset_index(drop=False)
        print("inc", inc.get_code(codelist[-1]))
        self.assertTrue(len(ind) > 0, "")

    def testShouBanData(self):
        """测试首板指标 shoubanData
        """
        # codelist = qa.QA_fetch_stock_list_adv().code.tolist()[:5]
        codelist = self.getCodeList()

        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData_v1)
        print("ind:", ind.tail(10))
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = inc.get_timerange('2018-08-01', '2018-08-31')
        df.loc[('2018-8-29', codelist[2])]
        df = self.getShouBan(codelist)
        codelist = sorted(df.code)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData_v1)
        inc = qa.QA_DataStruct_Indicators(ind)
        dfind = inc.get_timerange('2018-08-01', '2018-08-31')
        dfind.loc[('2018-8-29', codelist[0])]
        dfind.loc[(df.iloc[1].date.strftime('%Y-%m-%d'), codelist[0])]
        # print("inc", inc.get_code(codelist[-1]))
        df = inc.get_timerange('2018-08-01', '2018-08-31', codelist[0])
        print(df)
        # 2018-08-15 000023 5.094597 - 15.386906 10.015291 0.688073 1.38 2.14
        self.assertTrue(len(df) > 0, "")

    def testShouOutput201808(self):
        codelist = self.getCodeList()
        startdate = datetime.strptime('2017-08-01', '%Y-%m-%d')
        df = self.getShouBan(codelist, startdate)
        codelist = sorted(df.code)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData_v1)
        inc = qa.QA_DataStruct_Indicators(ind)
        dfind = inc.get_timerange('2018-08-01', '2018-08-31')
        dfind.loc[('2018-8-29', codelist[2])]
        dfind.loc[(df.iloc[1].date.strftime('%Y-%m-%d'), codelist[2])]
        print("code   次日均涨	位置 次日高幅 次日低里僧幅 次日涨幅 次日量比")
        for i in range(len(df.index) - 1):
            d = dfind.loc[(df.iloc[i].date.strftime('%Y-%m-%d'),
                           df.iloc[i].code)]
            print(df.iloc[i].code, d.JJZF, d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB)
        # 按照代码顺序
        print("code   次日均涨	位置 次日高幅 次日低幅 次日涨幅 次日量比")
        alist = []
        for code in codelist:
            d1 = df.loc[df.code == code]
            d = dfind.loc[(pd.to_datetime(d1.date.values[0]).strftime('%Y-%m-%d'), d1.code.values[0])]
            # d=dfind.loc[(d1.date.strftime('%Y-%m-%d'), d1.code)]
            # print("{} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f} {0:0.2f}".format(
            # code, d.JJZF, d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB))
            a = ["%.2f" % i for i in d]
            a.append(code)
            alist.append(a)
            # alist.append("{}{}".format(code, ", %.2f"*len(d) % tuple(d)))
            print(code, ", %.2f" * len(d) % tuple(d))

        dfc = pd.DataFrame(alist, columns=["次日均涨", "位置", "次日高幅", "次日低幅", "次日涨幅", "次日量比", "股票代码"])
        dfc.to_csv("/tmp/d.csv", index=False)
        print("inc", inc.get_code(codelist[-1]))
        self.assertTrue(len(ind) > 0, "")

    def getCodeList(self, isSB=True, count=5000):
        if isSB:
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
        codelist = self.getCodeList(isSB=False)
        # codelist = self.getCodeList(isSB=False, count=1000)
        # codelist = self.getCodeList(isSB=True)
        # dayslong = ['2018-01-01', '2018-03-31']
        dayslong = ['2018-01-01', '2019-10-31']
        daylist = []
        # 月初 月末
        firstday = self.str2date(dayslong[0])
        date_after_month = firstday + relativedelta(months=1) + relativedelta(days=-1)
        lastday = self.str2date(dayslong[1])
        # 获取起始时间之前一年的数据，否则可能因停牌过长不能计算起涨点相对120均线涨幅
        data = qa.QA_fetch_stock_day_adv(codelist, firstday - relativedelta(months=12),
                                         lastday + relativedelta(months=2)).to_qfq()
        while date_after_month <= lastday:
            print("首板...")
            df = self.getShouBan(codelist, data, startday=firstday, endday=date_after_month)
            if len(df) == 0:
                print("no data {}".format(self.date2str(firstday)))
                firstday = firstday + relativedelta(months=1)
                date_after_month = firstday + relativedelta(months=1) + relativedelta(days=-1)
                continue
            # 按照代码顺序
            codelist = sorted(df.code)
            startdate, enddate = self.date2str(firstday), self.date2str(date_after_month)
            print("首板指标...")
            sblist = self.getshoubanInd(codelist, df, data, startdate, enddate)
            firstday = firstday + relativedelta(months=1)
            date_after_month = firstday + relativedelta(months=1) + relativedelta(days=-1)
            self.assertTrue(len(sblist) > 0, "首板个数为零")

    def str2date(self, dayStr):
        if isinstance(dayStr, str):
            return datetime.strptime(dayStr, '%Y-%m-%d')
        else:
            return dayStr

    def getshoubanInd(self, codelist, df, data, startdate, enddate):
        print(startdate, enddate)
        ind = data.add_func(shoubanData_v1)
        inc = qa.QA_DataStruct_Indicators(ind)
        print("code   次日均涨	位置 次日高幅 次日低幅 次日涨幅 次日量比")
        alist = []
        edate = self.date2str(self.str2date(enddate) + relativedelta(days=10))
        for code in codelist:
            dfind = self.getTimeRange(inc, startdate, self.str2date(enddate) + relativedelta(days=15), code)
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
            # code, d.JJZF, d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB))
            # 涨停板位置
            wz = d.WZ
            # 首次涨停涨停第二个交易日，公式计算值 "次日均涨"位置", ", "次日高幅", "次日低幅", "次日涨幅", "次日量比"
            d = dfind.shift(-1).loc[(d1date.strftime('%Y-%m-%d'), d1.code.values[0])]
            d.WZ = wz
            a = ["%.2f" % i for i in d]
            a.insert(0, code)
            a.insert(1, self.date2str(d1date))
            alist.append(a)
            print(code, ", %.2f" * len(d) % tuple(d))
        dfc = pd.DataFrame(alist, columns=["股票代码", "首板日期", "次日均涨", "位置", "次日高幅", "次日低幅", "次日涨幅", "次日量比"])
        dfc.to_csv("/tmp/sb{}.csv".format(self.date2str(startdate)), index=False)
        # print("inc", inc.get_code(codelist[-1]))
        self.assertTrue(len(ind) > 0, "")
        return alist

    def getTimeRange(self, inc, startdate, enddate, code=None, isBugfixed=False):
        if isBugfixed:
            # 源码中bug修复时，使用以下代码
            dfindicator = inc.get_timerange(startdate, enddate, code)  # QAUANTAXIS源码中有bug，code不起作用

        else:
            # 源码中bug未修复时，使用以下代码
            if code is None:  # QAUANTAXIS源码中有bug，code为空时，不返回数据
                dfindicator = inc.data.loc[(slice(pd.Timestamp(startdate),
                                                  pd.Timestamp(self.str2date(enddate) + relativedelta(days=15)))), :]
            else:
                dfindicator = inc.data.loc[(slice(pd.Timestamp(startdate),
                                                  pd.Timestamp(self.str2date(enddate) + relativedelta(days=15))), code),
                              :]
        return dfindicator

    def getShouBan(self, codelist, qaData, startday='2018-04-01', endday='2018-10-21'):
        startday = self.date2str(startday)
        endday = self.date2str(endday)
        data = qaData.select_time(self.str2date(startday) - relativedelta(months=3),
                                  self.str2date(endday) + relativedelta(days=75))
        if len(data) == 0:
            # 没有数据则返回空
            return pd.DataFrame()
        # data = qa.QA_fetch_stock_day_adv(codelist, startday, endday).to_qfq()
        ind = data.add_func(shouban)
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = inc.get_timerange(startday, endday)
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
