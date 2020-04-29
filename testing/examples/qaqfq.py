# -*- coding: utf-8 -*-
# 前复权
import pandas as pd
import QUANTAXIS as QA

code = '600841'
date_start = '2016-01-22'
date_end = '2020-04-29'
ds = QA.QA_fetch_stock_day_adv(code, date_start, date_end)
ds_qfq = QA.QAData.data_fq.QA_data_stock_to_fq(ds.data, 'qfq')
ds_qfq = ds.to_qfq()
print(ds_qfq.close)
if isinstance(ds_qfq, pd.DataFrame):
    df = ds_qfq[['close']].join(ds.data.rename(columns={'close': 'preClose'})[['preClose']])
else:
    df = ds_qfq.data[['close']].join(ds.data.rename(columns={'close': 'preClose'})[['preClose']])
print((df[df.eval('close-preClose') > 0.001].tail(10)))
print((df[df.eval('close-preClose') == 0]))
# ds.plot()
