import unittest
from unittest import TestCase
import datetime
import pandas as pd
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_day, QA_fetch_get_stock_min
from qaHelper.fetcher import Fetcher


class testFetcher(TestCase):
    def test_get_frequence(self):
        # 1分钟
        peroid = Fetcher.getFrequence(1)
        peroid2 = Fetcher.getFrequence("1min")
        self.assertTrue(peroid == peroid2 == 8)
        # print("周期：", peroid)

        # 日间周期
        peroid = Fetcher.getFrequence('D')
        peroid2 = Fetcher.getFrequence("day")
        self.assertTrue(peroid == peroid2 == 9)
        peroid = Fetcher.getFrequence('Day')
        peroid2 = Fetcher.getFrequence("DAY")
        self.assertTrue(peroid == peroid2 == 9)

    def test_getReverseFrequence(self):
        peroid = 8
        frequence, type_, multiplicator = Fetcher.getReverseFrequence(peroid)
        self.assertTrue(multiplicator == 240, "1min倍数为240")

if __name__ == '__main__':
    unittest.main()
