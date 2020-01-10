# -*- coding: utf-8 -*-
import QUANTAXIS as qa

def ifupMA(data, n=20):
    """收盘站上n均线上
    """
    return (data.close-qa.MA(data.close, n)).dropna() > 0