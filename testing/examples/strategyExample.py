#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
https://www.cnblogs.com/onepiece-andy/p/python-strategy.html
"""
__author__ = 'Andy'
'''
大话设计模式
设计模式——策略模式
策略模式(strategy):它定义了算法家族,分别封装起来,让他们之间可以相互替换,此模式让算法的变化,不会影响到使用算法的客户
'''
import random

# 现金收费抽象类
class CashSuper(object):

    def accept_cash(self, money):
        pass


# 正常收费子类
class CashNormal(CashSuper):

    def accept_cash(self, money):
        return money


# 打折收费子类
class CashRebate(CashSuper):

    def __init__(self, discount=1):
        self.discount = discount

    def accept_cash(self, money):
        return money * self.discount


# 返利收费子类
class CashReturn(CashSuper):

    def __init__(self, money_condition=0, money_return=0):
        self.money_condition = money_condition
        self.money_return = money_return

    def accept_cash(self, money):
        if money >= self.money_condition:
            return money - (money / self.money_condition) * self.money_return
        return money


# 具体策略类
class Context(object):

    def __init__(self, csuper):
        self.csuper = csuper

    def GetResult(self, money):
        return self.csuper.accept_cash(money)


def test():
    moneys = [100, 1000, 500]
    # money = input("原价: ")
    # 随机
    money = random.choice(moneys)
    strategy = {}
    strategy[1] = Context(CashNormal())
    strategy[2] = Context(CashRebate(0.8))
    strategy[3] = Context(CashReturn(100, 10))
    print("策略类型：\n{}".format(strategy))
    # mode = input("选择折扣方式: 1) 原价 2) 8折 3) 满100减10: ")
    mode = random.choice(range(1, 3))
    try:
        mode = int(mode)
    except Exception as e:
        pass
    if mode in strategy:
        csuper = strategy[mode]
    else:
        print("不存在的折扣方式: {}".format(mode))
        csuper = strategy[1]
    print("原价：{}, 折扣方式： {}, 需要支付: {}".format(money, mode, csuper.GetResult(money)))


if __name__ == '__main__':
    for i in range(10):
        test()
