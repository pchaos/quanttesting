# -*- coding: utf-8 -*-
""" 期货相关
@Time    : 2020/2/21 下午4:50

@File    : test_quantaxis_future.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import QUANTAXIS as qa


class MyTestCase(unittest.TestCase):
    def test_fetch_future_list(self):
        """所有期货主力连续代码
        """
        codelist = qa.QA_fetch_future_list()
        codes = codelist[codelist.code.apply(lambda x: x.endswith('L8'))]
        self.assertTrue(len(codes) > 10, "所有期货主力连续代码数量太小")
        print(codes)

    def test_fetch_future_list(self):
        """实时对应的主力合约
        """
        fd = qa.QA_fetch_get_future_domain()
        self.assertTrue(len(fd) > 10, "实时对应的主力合约数量太少")
        print(fd)


if __name__ == '__main__':
    unittest.main()
