# -*- coding: utf-8 -*-
""" testunit 基础类

@Time    : 2020/4/10 上午1:03

@File    : testbase.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import datetime
import QUANTAXIS as qa

class qaTestingbase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(qaTestingbase, cls).setUpClass()
        cls.userInit()

    @classmethod
    def userInit(cls):
        """用户初始化
        """
        cls.code = '000300'
        dateStart = datetime.date(2005, 3, 1)
        dateEnd = datetime.date(2017, 3, 31)
        cls.dataFrame = qa.QA_fetch_index_day_adv(cls.code, start=dateStart, end=dateEnd)

    @classmethod
    def tearDownClass(cls) -> None:
        super(qaTestingbase, cls).tearDownClass()
        cls.userEnd()

    @classmethod
    def userEnd(cls):
        """class结束，用户释放资源
        """
        if cls.dataFrame is not None:
            cls.dataFrame = None

