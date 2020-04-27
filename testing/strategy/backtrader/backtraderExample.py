# -*- coding: utf-8 -*-
"""backtrader test
https://www.backtrader.com/docu/quickstart/quickstart/

"""
import backtrader as bt

import unittest
from unittest import TestCase

class test_backertrader(TestCase):

    def test_from0_100(self):
        cerebro = bt.Cerebro()

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.run()

        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


    def test_set_cach(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.run()

        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    test_backertrader.run()