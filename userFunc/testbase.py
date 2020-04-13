# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/13 下午6:08

@File    : testbase.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import datetime
from abc import ABC, abstractmethod

class TestingBase(unittest.TestCase, ABC):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestingBase, cls).setUpClass()
        cls.userInit()

    @classmethod
    @abstractmethod
    def userInit(cls):
        """用户初始化
        """
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        super(TestingBase, cls).tearDownClass()
        cls.userEnd()

    @classmethod
    @abstractmethod
    def userEnd(cls):
        """class结束，用户释放资源
        """
        pass
