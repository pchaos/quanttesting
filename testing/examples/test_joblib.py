# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/1 下午2:33

@File    : test_joblib.py

@author  : pchaos
@Contact : p19992003#gmail.com
"""
import unittest
from joblib import Parallel, delayed
import time, math


def my_fun(i):
    """ We define a simple function here.
    """
    time.sleep(1)
    return math.sqrt(i ** 2)


def my_fun_2p(i, j):
    """ We define a simple function with two parameters.
    """
    time.sleep(0.5)
    return math.sqrt(i ** j)


class MyTestCase(unittest.TestCase):
    def test_my_fun(self):
        num = 10
        start = time.time()
        result = []
        for i in range(num):
            result.append(my_fun(i))

        end = time.time()

        print('{:.4f} s'.format(end - start))

        start = time.time()
        # n_jobs is the number of parallel jobs
        Parallel(n_jobs=2)(delayed(my_fun)(i) for i in range(num))
        end = time.time()
        print('{:.4f} s'.format(end - start))

    def test_my_fun_2p(self):
        j_num = 3
        num = 10
        start = time.time()
        for i in range(num):
            for j in range(j_num):
                my_fun_2p(i, j)

        end = time.time()
        print('{:.4f} s'.format(end - start))

        start = time.time()
        # n_jobs is the number of parallel jobs
        Parallel(n_jobs=2)(delayed(my_fun_2p)(i, j) for i in range(num) for j in range(j_num))
        end = time.time()
        print('{:.4f} s'.format(end - start))


if __name__ == '__main__':
    unittest.main()
