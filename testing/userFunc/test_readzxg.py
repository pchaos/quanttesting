# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/3 下午5:52

@File    : test_readzxg.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import os
from userFunc import read_zxg

class testReadZXG(unittest.TestCase):
    def test_read_zxg(self):
        """测试读取自选股列表
        """"
        fn = 'zxg.txt'
        # code列表
        code = read_zxg(fn)
        if len(code) == 0:
            # 自选股为空
            self.assertTrue(not os.path.exists(fn), "找到文件：{}".format(fn))
        else:
            self.assertTrue(os.path.exists(fn), "没找到文件：{}".format(fn))
            print("自选列表：{}".format(code))


if __name__ == '__main__':
    unittest.main()
