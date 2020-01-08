from unittest import TestCase
import unittest
#  import datetime
import QUANTAXIS as qa
#  import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def shouban(dataFrame):
    """ 首板

    """
    close = dataFrame['close']
    tj1 = close > qa.REF(close, 1) * 1.098
    tj2 = qa.COUNT(tj1, 30) == 1
    # 涨停 并且 最近30交易日涨停次数为1，则标记1,否则标记0
    sb = pd.DataFrame({'tj1': tj1, 'tj2': tj2}).apply(lambda x: 1 if x['tj1'] and x['tj2'] else 0, axis=1)
    # sb = tj1 && tj2 && qa.COUNT(CLOSE) > 50
    dict = {'SB': sb}
    return pd.DataFrame(dict)


def shoubanData(dataFrame):
    """ 首板指标计算
    次日均涨	位置 次日高幅 次日低幅 次日涨幅 次日量比
    JJZF, WZ, ZGZF, ZDDF, ZF, LB
    位置：涨停日收盘价相对60日最低收盘价涨幅（c涨停/C60日最低-1）*100%
    次日量比10均：v/ma（v，10） ; v10日均算的是涨停日
    """
    close = dataFrame['close']
    H = dataFrame['high']
    L = dataFrame['low']
    V = dataFrame['volume']
    AMO = dataFrame['amount']
    n = -1  # 次日数据
    # 位置
    wz = close / qa.LLV(close, 60) - 1
    # 次日涨幅
    zf = qa.REF(close, n) / close - 1
    # 次日高幅
    zgzf = qa.REF(H, n) / close - 1
    # 次日跌幅
    zddf = qa.REF(L, n) / close - 1
    # 次日量比
    lb = qa.REF(V, n) / V
    # 次日量比v10
    crlbv10 = qa.REF(V, -1) / qa.MA(V, 10)

    cjjj = AMO / V / 100
    # 次日均涨
    jjzf = qa.REF(cjjj, n) / close - 1
    dict = {'JJZF': jjzf, 'WZ': wz, 'ZGZF': zgzf, 'ZDDF': zddf, 'ZF': zf, 'LB': lb,
            "CRLBV10": crlbv10}
    return pd.DataFrame(dict)


def shoubanType(dataFrame):
    """首板类型（首次涨停，k线形态）
    0、非首板相关
    10、一字涨停（涨停第一天绝对一字涨停收盘，O=C=H=L>ref(c,1)*1.098）
    21、实体阳线涨停，涨停次日收十字，或收长上影线且涨幅小于3%， 或收长下影线且涨幅小于2%
    22、实体阳线涨停，涨停次日收阴实线
    23、实体阳线涨停，涨停次日收实体阳线或涨幅大于3%
    24、实体阳线涨停，涨停次日孕育k线（未创新高新低，H<ref(H,1) and L>ref(L,1)）
    30、其他类型
    """

    def sbtype(x):
        # 计算首板第一天、第二天的类型。一字板在首板第一天判断，其他类型在首板第二天判断
        if x.SB == 0:
            # 非首板 不用判断类型
            return 0
        # 首板
        if x.zf > 1.03:
            # 涨幅大于3%
            if x.zf > 1.098 and x.H == x.L:
                # 一字涨停
                return 10
            else:
                return 23
        elif x.zf > 1.0:
            # 收盘价介于0%～3%之间
            return 21
        elif x.H <= x.preH and x.L >= x.preL:
            # 收盘价小于前一天收盘价
            return 24
        elif x.close > x.preL:
            return 22
        else:
            return 30

    def sbtype2(x):
        # 合并首板类型技术指标到首板当天
        if x.t1 == 0 or x.t1 == 10:
            # 非首板 不用判断类型
            if x.t1 == 10 and x.t2 != 0:
                # 连续涨停的，第二个不用标记
                print("", x.t2)
                return 10
            else:
                return 0
        else:
            # 复制首板第二天
            return x.t2

    close = dataFrame['close']
    op = dataFrame['open']  # 开盘价
    # 首板
    tj1 = close > qa.REF(close, 1) * 1.098
    tj2 = qa.COUNT(tj1, 30) == 1
    # 涨停 并且 最近30交易日涨停次数为1，则标记1,否则标记0
    sb = pd.DataFrame({'tj1': tj1, 'tj2': tj2}).apply(lambda x: 1 if x['tj1'] and x['tj2'] else 0, axis=1)
    # 首板及首板第二天标记为1
    # dict = {'SB': sb + sb.shift(-1).fillna(0)}

    H = dataFrame['high']
    L = dataFrame['low']
    # 首板第二天收盘价涨幅
    zf = close / qa.REF(close, 1)
    # 计算首板第一天、第二天的类型
    sbt = pd.DataFrame({'zf': zf, 'H': H, "L": L, "preH": qa.REF(H, 1), "preL": qa.REF(L, 1), 'close': close,
                        'SB': sb + sb.shift(1).fillna(0)}).apply(lambda row: sbtype(row),
                                                                 axis=1)
    # 合并首板类型技术指标到首板当天
    sbt = pd.DataFrame({'t1': sbt, 't2': sbt.shift(-1)}).apply(lambda row: sbtype2(row),
                                                               axis=1)
    dict = {'TYPE': sbt}
    # 返回整数类型
    df = pd.DataFrame(dict).fillna(0).astype('int')
    # 首板次日开盘涨幅
    df['CRKFZF'] = (op / qa.REF(close, 1) - 1).shift(-1)
    return df
