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
from jqdatasdk import *
from dotenv import load_dotenv
from .testbase import TestingBase

def getEnvVar(key):
    load_dotenv(verbose=True)
    return os.getenv(key)

class jqTestingbase(unittest.TestCase):

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
