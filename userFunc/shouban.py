#  import datetime
import QUANTAXIS as qa
import numpy as np
import pandas as pd
from datetime import datetime


# from dateutil.relativedelta import relativedelta


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
    首板指标的计算指标都放在首板当天。（便于查询）
    次日均涨	位置 次日开盘涨幅 次日高幅 次日低幅 次日涨幅 次日量比 次日量比v10 次日开盘价 涨停板日的均价 类型
    JJZF, WZ, ZGZF, ZDDF, ZF, LB

    2020 01 17
    1、首板后10日之内的最低价/涨停板日涨停价
    2、首板后10日之内最高价/涨停板日涨停板最高价

    2020 01 08
    位置：涨停日收盘价相对60日最低收盘价涨幅（c涨停/C60日最低-1）*100%
    次日量比10均：v/ma（v，10） ; v10日均算的是涨停日

    """
    close = dataFrame['close']
    op = dataFrame['open']  # 开盘价
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
    crlbv10 = qa.REF(V, n) / qa.MA(V, 10)
    # 涨停板日的均价
    cjjj = AMO / V / 100 / qa.REF(close, 1)
    # 次日均涨
    jjzf = qa.REF(cjjj, n) - 1
    # 首板次日开盘涨幅
    crkpzf = op.shift(n) / close - 1
    # 涨停类型
    sbType = shoubanType(dataFrame)
    # 首板后10日之内的最低价/涨停板日涨停价
    ll10 = qa.LLV(L, 10).shift(-10) / close - 1
    # 首板后10日之内最高价/涨停板日涨停板最高价
    hh10 = qa.HHV(H, 10).shift(-10) / close - 1
    dict = {'JJZF': jjzf, 'WZ': wz, 'CRKPZF': crkpzf, 'ZGZF': zgzf, 'ZDDF': zddf, 'ZF': zf, 'LB': lb,
            "CRLBV10": crlbv10, 'OPEN': op / qa.REF(close, 1), 'JJ': cjjj, 'TYPE': sbType['TYPE'], "LL10": ll10,
            "HH10": hh10}
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
                # print("", x.t2)
                return 10
            else:
                return 0
        else:
            # 复制首板第二天
            return x.t2

    close = dataFrame['close']
    # op = dataFrame['open']  # 开盘价
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
    # 计算首板第一天、第二天的类型教程
    sbt = pd.DataFrame({'zf': zf, 'H': H, "L": L, "preH": qa.REF(H, 1), "preL": qa.REF(L, 1), 'close': close,
                        'SB': sb + sb.shift(1).fillna(0)}).apply(lambda row: sbtype(row),
                                                                 axis=1)
    # 合并首板类型技术指标到首板当天
    sbt = pd.DataFrame({'t1': sbt, 't2': sbt.shift(-1)}).apply(lambda row: sbtype2(row), axis=1)
    dict = {'TYPE': sbt}
    # 返回整数类型
    return pd.DataFrame(dict).fillna(0).astype('int')


def shoubanZDZG1(dataFrame, sbDate, n=10):
    """ 首板后n天最大跌幅 最大涨幅
    dataFrame: 当个股票的pandas数据
    dbDate : 首板日期
    n： 首板后n天最大跌幅 最大涨幅

    最大跌幅(TDX公式)
    SBJL:BARSLAST(SB),NODRAW;
    SBLV:=IF(1<SBJL AND SBJL<11,L,DRAWNULL);{取距离涨停日后10日每天的低价}
    SBHV:=IF(0<=SBJL AND SBJL<11,HHV(H,SBJL+1),DRAWNULL);{取距离涨停日后10日内当日到涨停日的最高价}
    SBDFLV:=IF(1<SBJL AND SBJL<11,(SBLV/REF(SBHV,1)-1)*100,DRAWNULL);{距离涨停日后10日跌幅=当日最低价/上日最高价}
    SBDF:=IF(1<SBJL AND SBJL<11,LLV(SBDFLV,SBJL),DRAWNULL);{距离涨停日后10日跌幅的最大值}
    SBDFX:={跌幅记录点}
    (SBDF<REF(SBDF,1) AND SBDF=REFX(SBDF,1)){最大跌幅大于昨日 且等于明日}
    OR (SBJL=2 AND SBDF=REFX(SBDF,1) AND SBDF<0){或涨停后第二日 且最大等于明日，且小于0}
    OR(SBJL=2 AND REFX(H,1)>REFX(H,2)){或涨停后第二日 且明日最高价高于后日最高价}
    OR (SBJL=2 AND L<REFX(L,1)),NODRAW;{或涨停后第二日 且明日最高价高于后日最高价}
    DRAWNUMBER(SBDFX=1 AND SBDFLV<0 ,L,SBDF) COLORGREEN;{记录跌幅}
    """
    # 首板n天的数据
    data = dataFrame[['high', 'low']].loc[(slice(pd.Timestamp(sbDate), datetime.now())), :][:n + 1]
    j = 0
    # 2维numpy array
    tmp = np.array([(np.NaN, np.nan, np.nan, np.nan)] * len(dataFrame))
    for i in data.index:
        # 取距离涨停日后10日内当日到涨停日的最高价
        tmp[j, 0] = qa.HHV(data.high[:j + 1], j + 1)[j]
        if j > 1:
            tmp[j, 1] = qa.LLV(data.low[1:j + 1], j)[j - 1] / tmp[j - 1, 0] - 1
        j += 1
    # data['SBDFLV'] = 0
    data['SBHV'] = list(tmp[:, 0])
    # 距离涨停日后10日跌幅=当日最低价/上日最高价
    data['SBDFLV'] = (qa.REF(data.low, -1) / data['SBHV']).shift(1) - 1
    # 距离涨停日后10日跌幅的最大值
    j = 0
    for i in data.index:
        if j > 1:
            # 距离涨停日后10日跌幅的最大值
            tmp[j, 2] = qa.LLV(data.SBDFLV[1:j + 1], j)[j - 1]
        j += 1
    data['SBDF'] = list(tmp[:, 2])
    sbdf = data.SBDF
    j = 2
    # (SBJL=2 AND SBDF=REFX(SBDF,1) AND SBDF<0){或涨停后第二日 且最大等于明日，且小于0}
    #     OR(SBJL=2 AND REFX(H,1)>REFX(H,2)){或涨停后第二日 且明日最高价高于后日最高价}
    #     OR (SBJL=2 AND L<REFX(L,1)),NODRAW;{或涨停后第二日 且明日最高价高于后日最高价}
    tmp[j, 3] = (data.SBDF[j] == data.SBDF[j + 1] and data.SBDF[j] < 0) | (data.high[j + 1] > data.high[j + 2]) \
                | (data.low[j] < data.low[j + 1])
    # 跌幅记录点 最大跌幅大于昨日 且等于明日
    data['SBDFX'] = (qa.REF(sbdf, -1) < sbdf).shift(1).fillna(False) & (
            sbdf == qa.REF(sbdf, -1)).fillna(False)
    data['SBDFX'][j] | True if tmp[j, 3] else False

    dict = {'SBDF': data.SBDF}
    return pd.DataFrame(dict)


def shoubanZDZG(dataFrame, sbDate, n=10, percent=0.05):
    """ 首板后n天最大跌幅 最大涨幅
    dataFrame: 当个股票的pandas数据
    dbDate : 首板日期
    n： 首板后n天最大跌幅、最大涨幅; 默认值：10

    计算n周期内最大跌幅：
    计算n周期内最大跌幅、最大涨幅

逻辑：
1.低点比第二日低，就用低点除以前一日到涨停日的最高点算跌幅，如果跌幅大于-3%，就记为低点
2.以此低点后的交易日，只要高点比第二天高，就计算涨幅，在限定日期内，取最大值为限定日期的最大涨幅
在首板后n个交易日（这里先取n=10），每次超过5%(可调整)的跌幅，算日后的反弹，在n个交易日里面，找到反弹涨幅最大的，然后在找出这个涨幅对应的跌幅

涨停板第二天，我们是判断日，这天就算跌幅大于5%，也是不能买入了，所以从涨停板第三日也就是T+2开始判断是否较高点跌幅大于5%，然后判断从这个跌幅的最低点反弹，看反弹的涨幅，我们取涨幅最大的那个，对应的跌幅，记录下来

    最大跌幅(TDX公式) (供参考，此公式有点不准）
    SBJL:BARSLAST(SB),NODRAW;
    SBLV:=IF(1<SBJL AND SBJL<11,L,DRAWNULL);{取距离涨停日后10日每天的低价}
    SBHV:=IF(0<=SBJL AND SBJL<11,HHV(H,SBJL+1),DRAWNULL);{取距离涨停日后10日内当日到涨停日的最高价}
    SBDFLV:=IF(1<SBJL AND SBJL<11,(SBLV/REF(SBHV,1)-1)*100,DRAWNULL);{距离涨停日后10日跌幅=当日最低价/上日最高价}
    SBDF:=IF(1<SBJL AND SBJL<11,LLV(SBDFLV,SBJL),DRAWNULL);{距离涨停日后10日跌幅的最大值}
    SBDFX:={跌幅记录点}
    (SBDF<REF(SBDF,1) AND SBDF=REFX(SBDF,1)){最大跌幅大于昨日 且等于明日}
    OR (SBJL=2 AND SBDF=REFX(SBDF,1) AND SBDF<0){或涨停后第二日 且最大等于明日，且小于0}
    OR(SBJL=2 AND REFX(H,1)>REFX(H,2)){或涨停后第二日 且明日最高价高于后日最高价}
    OR (SBJL=2 AND L<REFX(L,1)),NODRAW;{或涨停后第二日 且明日最高价高于后日最num高价}
    DRAWNUMBER(SBDFX=1 AND SBDFLV<0 ,L,SBDF) COLORGREEN;{记录跌幅}
    """
    # 首板n天的数据
    data = dataFrame[['high', 'low']].loc[(slice(pd.Timestamp(sbDate), datetime.now())), :][: n + 2]
    j = 0
    k = 0  # 最高价时的顺序号
    h, l = 0.0, 0.0  # 临时保存最高价、最低价
    ll = 0
    lowk = 0  # 低点所在位置顺序号
    dd = False  # 是否出现低点
    # 2维numpy array; 相对最高价 相对最低价 相对前高跌幅 相对前低涨幅 原始的最大跌幅
    tmp = np.array([(np.NaN, np.NaN, np.NaN, np.NaN, np.NaN)] * len(data))
    for i in range(len(data)):
        # 取距离涨停日后n日内当日到涨停日的最高价  # 碰到新低，高点重新开始计数
        tmp[j, 0] = qa.HHV(data.high[ll:j + 1], j - ll + 1)[j - ll]
        if j > 0:
            #
            if dd:
                # 有低点以后，低点判断要以修改低点后的数据为准
                minlow = tmp[j - 1, 1]
                tmp[j, 1] = qa.LLV(data.low[lowk:j + 1], j - lowk)[j - lowk]
                tmp[j, 1] = minlow if minlow < tmp[j, 1] else tmp[j, 1]
            else:
                tmp[j, 1] = qa.LLV(data.low[1:j + 1], j)[j - 1]
            if tmp[j, 1] < tmp[j - 1, 1]:
                # 创新低
                ll = j
            # data.high[li:j + 1]
            # 某天最低价/截止前一天最高价
            preh = max(tmp[:j, 0])
            # tmp[j, 2] = data.low[j] / tmp[j - 1, 0]
            tmp[j, 2] = data.low[j] / preh
            tmp[j, 4] = tmp[j, 2]  # 原始的最大跌幅
            # 某天最高价/截止前一天最低价
            # tmp[j, 3] = tmp[j, 0] / tmp[j - 1, 1]
            tmp[j, 3] = data.high[j] / tmp[j - 1, 1]
            try:
                # 类似底分型
                cona = (tmp[j - 1, 1] >= tmp[j, 1]) and (
                            data.low[j] < data.low[j - 1] or (data.low[j] == data.low[j - 1]) and data.high[j] <
                            data.high[j - 1]) and (
                               data.low[j + 1] > data.low[j] or data.high[j + 1] >= data.high[j])
                # T+2开始判断是否较高点跌幅大于5%
                conb = tmp[j, 2] < 1 - percent and j > 1
            except Exception as e:
                # 数据不完整时，设置判断条件为False， 不作为低点
                cona = conb = False
            if ((not dd) and cona and j > 1) or (not dd and conb):
                # 判断低点
                dd = True
                # if (not cona) and tmp[j, 2] < 1 - percent:
                if 1 or conb:
                    # 第一次低点，需要重新计算最低最高价
                    for ii in range(1, j + 1):
                        tmp[ii, 1] = data.low[j]
                        preh = max(tmp[:ii, 0])
                        # tmp[j, 2] = data.low[j] / tmp[j - 1, 0]
                        tmp[ii, 2] = data.low[ii] / preh
                        tmp[ii, 3] = 1
                lowk = j

        if j > 2 and dd and (j - ll + 1) < n:
            if tmp[j, 3] > h:
                # if (tmp[j - 1, 1] >= tmp[j, 1]) and (tmp[j, 0] >= tmp[j - 1, 0]):
                k, h = j, tmp[j, 3]
                ll = k
        j += 1
        if j > n:
            # 大于n天,不计算
            break
    if k > 0:
        # 能计算最大跌幅 连板的会找不出最大涨幅 返回 0,0
        l = min(tmp[1:k, 2])
        for i in range(1, len(data)):
            if l == tmp[i, 4]:
                lowk = i
                break
        h -= 1
        l -= 1
    dict = {'SBDF': [l], 'SBZF': [h], 'lowK': lowk, 'highK': [k]}
    return pd.DataFrame(dict)
