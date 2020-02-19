# -*- coding: utf-8 -*-

import QUANTAXIS as QA
import matplotlib.pyplot as plt

code = ['600650',
        '600652',
        '600654',
        '600676',
        '600687',
        '600726',
        '600759',
        '600871',
        '600959',
        '600978',
        '601010',
        '601016',
        '601018',
        '601258',
        '603117']

data = QA.QA_fetch_stock_day_adv(code, '2017-01-01', '2020-01-01')

fig = plt.figure(figsize=(12, 8))
data.groupby(level=1).close.apply(lambda x: x.plot())
plt.show()
