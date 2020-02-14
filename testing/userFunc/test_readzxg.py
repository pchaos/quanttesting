# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/3 下午5:52

@File    : test_readzxg.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import os
import QUANTAXIS as qa
from userFunc import read_zxg
from userFunc import xls2zxg, xls2Code, code2ETF, etfAmountGreater


class testReadZXG(unittest.TestCase):
    def test_read_zxg(self):
        """测试读取自选股列表
        """
        fn = 'zxg.txt'
        # code列表
        code = read_zxg(fn)
        if len(code) == 0:
            # 自选股为空
            self.assertTrue(not os.path.exists(fn), "找到文件：{}".format(fn))
        else:
            self.assertTrue(os.path.exists(fn), "没找到文件：{}".format(fn))
            print("自选列表：{}".format(code))

    def test_readzxg_name(self):
        """代码对应的指数名称
        """
        fn = 'zxg.txt'
        # code列表
        code = read_zxg(fn)
        data = qa.QA_fetch_index_list_adv()
        print(data.columns)
        # print(data[['code', 'name']])
        for c in code:
            print(c, data.loc[c]['name'])

    def test_xls2zxg(self):
        xlsfile = "担保品20200210.xls"
        zxgfile = "/tmp/{}.txt".format(xlsfile)
        xls2zxg(xlsfile, zxgfile)
        codes = read_zxg(zxgfile, length=15)
        self.assertTrue(len(codes) > 10, "读取数量太少：{}".format(codes))
        print(codes[:10])
        for code in codes:
            if code.startswith("159"):
                print(code)

    def test_xls2Code(self):
        xlsfile = "担保品20200210.xls"
        zxgfile = "/tmp/{}.txt".format(xlsfile)
        xls2zxg(xlsfile, zxgfile)
        codes = read_zxg(zxgfile)
        self.assertTrue(len(codes) > 10, "读取数量太少：{}".format(codes))
        print(codes[:10])
        codes2 = xls2Code(xlsfile)
        self.assertTrue(codes == codes2, "返回结果不想等")
        for code in codes2:
            self.assertTrue(len(code) == 6)

    def test_code2ETF(self):
        xlsfile = "担保品20200210.xls"
        codes = xls2Code(xlsfile)
        # ETF列表
        codeETF = code2ETF(codes)
        self.assertTrue(len(codes) > len(codeETF))
        print(len(codeETF), codeETF[:10], codeETF[-10:])

    def test_etfAmountGreater(self):
        # 成交额大于等于amount(万元）
        xlsfile = "担保品20200210.xls"
        codes = xls2Code(xlsfile)
        # ETF列表
        codeETF = code2ETF(codes)
        # 日期
        startDate = '2020-02-07'
        # 成交金额大于amount
        amount = 1100
        df = etfAmountGreater(codeETF, startDate, amount=amount)
        df2 = qa.QA_fetch_index_day_adv(codeETF, startDate)
        self.assertTrue(len(df2.data) > len(df.data))
        print("{} :{}".format(len(df), len(df2)), df[:10], df2[-10:])
        print(df.code)


if __name__ == '__main__':
    unittest.main()
