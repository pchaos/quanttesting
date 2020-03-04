# -*- coding: utf-8 -*-
import pandas as pd
import datetime
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


def str2date(dateStr, format='%Y-%m-%d'):
    if isinstance(dateStr, str):
        return datetime.strptime(dateStr, format)
    else:
        return dateStr

def date2str(startdate, format='%Y-%m-%d'):
    if isinstance(startdate, datetime):
        startdate = startdate.strftime(format)
    return startdate

#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False