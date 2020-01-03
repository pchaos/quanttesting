# -*- coding: utf-8 -*-
from unittest import TestCase
import unittest
#  import datetime
import QUANTAXIS as qa
#  import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta


def shouban(dataFrame):
    """ 首板

    """
    close = dataFrame['close']
    tj1 = close > qa.REF(close, 1) * 1.098
    tj2 = qa.COUNT(tj1, 30) == 1
    sb = pd.DataFrame({'tj1': tj1, 'tj2': tj2}).apply(lambda x: 1 if x['tj1'] and x['tj2'] else 0, axis=1)
    # sb TestCase= tj1 && tj2 && qa.COUNT(CLOSE) > 50
    dict = {'SB': sb}
    return pd.DataFrame(dict)


def shoubanData(dataFrame):
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


class testShouBan(TestCase):
    """
    首板
    """

    def setup(self):
        print("starting")
        qa.QA_util_log_info('首板')

    def teardown(self):
        print("done")

    def testShouBan(self):
        codelist = qa.QA_fetch_stock_list_adv().code.tolist()[:5]
        data = qa.QA_fetch_stock_day_adv(codelist, '2018-04-01', '2018-10-21').to_qfq()
        ind = data.add_func(shouban)
        print("ind:", ind)
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = inc.get_timerange('2018-08-01', '2018-08-31')
        df = df[df['SB'] == 1].reset_index(drop=False)
        print("inc", inc.get_code(codelist[-1]))
        # qa.debug("indicator")
        self.assertTrue(len(ind) > 0, "")

    def testShouBanData(self):
        codelist = qa.QA_fetch_stock_list_adv().code.tolist()[:5]
        codelist = ['000023', '000068', '000407', '000561', '000590', '000593', '000608', '000610', '000626', '000638',
                    '000657', '000659', '000663', '000669', '000677', '000705', '000759', '000766', '000780', '000792',
                    '000815', '000852', '000885', '000909', '000913', '000921', '000928', '000931', '002006', '002012',
                    '002034']

        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData)
        print("ind:", ind.tail(10))
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = inc.get_timerange('2018-08-01', '2018-08-31')
        df.loc[('2018-8-29', codelist[2])]
        df = self.getShouBan(codelist)
        codelist = sorted(df.code)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData)
        inc = qa.QA_DataStruct_Indicators(ind)
        dfind = inc.get_timerange('2018-08-01', '2018-08-31')
        dfind.loc[('2018-8-29', codelist[2])]
        dfind.loc[(df.iloc[1].date.strftime('%Y-%m-%d'), codelist[2])]
        print("inc", inc.get_code(codelist[-1]))
        # qa.debug("indicator")
        self.assertTrue(len(ind) > 0, "")

    def testShouOutput201808(self):
        codelist = qa.QA_fetch_stock_list_adv().code.tolist()[:500]
        df = self.getShouBan(codelist)
        codelist = sorted(df.code)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData)
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
        # qa.debug("indicator")
        self.assertTrue(len(ind) > 0, "")

    def aatestShouOutput(self):
        dayslong = ['2017-01-01', '2019-10-31']
        daylist = []
        firstday = datetime.strptime(dayslong[0], '%Y-%m-%d')
        lastday = datetime.strptime(dayslong[1], '%Y-%m-%d')
        date_after_month = firstday + relativedelta(months=1)
        while date_after_month <= lastday:
            pass
        codelist = qa.QA_fetch_stock_list_adv().code.tolist()[:500]
        df = self.getShouBan(codelist)
        codelist = sorted(df.code)
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(shoubanData)
        inc = qa.QA_DataStruct_Indicators(ind)
        dfind = inc.get_timerange('2018-08-01', '2018-08-31')
        dfind.loc[('2018-8-29', codelist[2])]
        dfind.loc[(df.iloc[1].date.strftime('%Y-%m-%d'), codelist[2])]
        print("code   次日均涨	位置 次日高幅 次日低幅 次日涨幅 次日量比")
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
            # code, d.JJZF,'2018-10-21' d.WZ, d.ZGZF, d.ZDDF, d.ZF, d.LB))
            a = ["%.2f" % i for i in d]
            a.append(code)
            alist.append(a)
            # alist.append("{}{}".format(code, ", %.2f"*len(d) % tuple(d)))
            print(code, ", %.2f" * len(d) % tuple(d))

        dfc = pd.DataFrame(alist, columns=["次日均涨", "位置", "次日高幅", "次日低幅", "次日涨幅", "次日量比", "股票代码"])
        dfc.to_csv("/tmp/d.csv", index=False)
        print("inc", inc.get_code(codelist[-1]))
        # qa.debug("indicator")
        self.assertTrue(len(ind) > 0, "")

    def getShouBan(self, codelist, startday='2018-04-01', endday='2018-10-21'):
        if isinstance(startday, datetime):
            startday = startday.date.strftime('%Y-%m-%d')
        data = qa.QA_fetch_stock_day_adv(codelist, startday , endday).to_qfq()
        ind = data.add_func(shouban)
        inc = qa.QA_DataStruct_Indicators(ind)
        # inc.get_timerange('2018-08-01','2018-08-31',codelist[0])
        # inc.get_code(codelist[-1])
        df = inc.get_timerange('2018-08-01', '2018-08-31')
        df = df[df['SB'] == 1].reset_index(drop=False)
        return df


if __name__ == '__main__':
    unittest.main()
