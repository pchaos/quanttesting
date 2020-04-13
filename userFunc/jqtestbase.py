# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/13 下午6:07

@File    : jqtestbase.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

import unittest
import datetime
import os
from jqdatasdk import *
from dotenv import load_dotenv
from .testbase import TestingBase


def getEnvVar(key):
    from os import sys, path

    # __file__ should be defined in this case
    DIRNAME = path.dirname(path.dirname(path.abspath(__file__)))
    if DIRNAME not in sys.path:
        sys.path.append(DIRNAME)
    load_dotenv(verbose=True)
    return os.getenv(key)


class jqTestingbase(TestingBase):

    @classmethod
    def userInit(cls):
        """用户初始化
        """
        # .env  文件中写入相应的参数
        userid = getEnvVar('jquserid')
        passwd = getEnvVar('jqpasswd')
        assert userid
        auth(userid, passwd)

    @classmethod
    def userEnd(cls):
        """class结束，用户释放资源
        """
        pass
