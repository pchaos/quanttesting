# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/10 上午12:18

@File    : test_myFunction.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
from unittest import TestCase
import pandas as pd
import os
import datetime
import numpy as np
import statsmodels.formula.api as sml
import matplotlib.pyplot as plt
import QUANTAXIS as qa
from userFunc import qaTestingbase, CMI

class testMyFunction(qaTestingbase):
    def test_cmi(self):
        cmi = CMI(self.dataFrame)
        self.assertTrue(len(cmi) > 0)
        print(cmi)


if __name__ == '__main__':
    unittest.main()
