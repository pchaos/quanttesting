# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/8 下午9:34

@File    : mock-myclass.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""


class MyClass():
    def my_method(self):
        pass


class SomeOtherClassThatUsesMyClass():
    def method_under_test(self):
        myclass = MyClass()
        return myclass.my_method()
