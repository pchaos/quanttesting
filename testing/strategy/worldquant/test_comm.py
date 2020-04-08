# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/8 下午11:25

@File    : test_comm.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
from unittest import TestCase
import datetime
import QUANTAXIS as qa
from strategy.worldquant import get_alpha, Alphas


class testComm(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        code = '000300'
        dateStart = datetime.date(2015, 3, 1)
        dateEnd = datetime.date(2017, 3, 31)
        cls.df = qa.QA_fetch_index_day_adv(code, start=dateStart, end=dateEnd).data

    def test_get_alpha001(self):
        alpha= Alphas(self.df)
        a = alpha.alpha001()
        self.assertTrue(len(a) > 100)
        print(a)

    # def test_get_alpha(self):
    #     alpha = get_alpha(self.df)
    #     self.assertTrue(len(alpha) > 100)
    #     print(alpha)


if __name__ == '__main__':
    unittest.main()
