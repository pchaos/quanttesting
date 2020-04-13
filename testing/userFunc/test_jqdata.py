# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from jqdatasdk import *
from userFunc import jqTestingbase

class testJQdata(jqTestingbase):
    def test_get_query_count(self):
        self.assertTrue(is_auth(), "验证用户未成功！")
        print("JoinQuant 使用情况：", get_query_count())
        self.assertTrue(len(get_query_count()) > 0, "获取数据出错")

if __name__ == '__main__':
    unittest.main()