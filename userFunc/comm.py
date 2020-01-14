# -*- coding: utf-8 -*-
import pandas as pd
import QUANTAXIS as qa


def ifupMA(data, n=[20]):
    """收盘站上n均线上

    """
    if isinstance(n, int):
        # 传进来的参数为整数类型时
        return (data.close - qa.MA(data.close, n)).dropna() > 0
    elif isinstance(n, list):
        dict = {'MA{}'.format(i): data.close - qa.MA(data.close, i) for i in n}
        return pd.DataFrame(dict).dropna() > 0
