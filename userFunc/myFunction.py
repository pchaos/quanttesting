# -*- coding: utf-8 -*-
import bz2
import pickle

try:
    # 在python3.x上已从cPickle更改cPickle为_pickle
    import _pickle as cPickle
except ImportError:
    import cpickle as cPickle
import os
import numpy as np
import pandas as pd
import QUANTAXIS as qa
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache


def setdiff_sorted(array1, array2, assume_unique=False):
    """find elements in one list that are not in the other
    list_1 = ["a", "b", "c", "d", "e"]
    list_2 = ["a", "f", "c", "m"]
    main_list = setdiff_sorted(list_2,list_1)
    main_list = setdiff_sorted(list_2,list_1, assume_unique=True)
    """
    ans = np.setdiff1d(array1, array2, assume_unique).tolist()
    if assume_unique:
        return sorted(ans)
    return ans


def getCodeList(isTesting=True, count=5000):
    """
    :param isTesting: 是否使用测试数据
    :param count: 返回最多结果集数量
    """
    if isTesting:
        # 2018.8首板个股，测试用，减少调试时间
        codelist = ['000023', '000068', '000407', '000561', '000590', '000593', '000608', '000610', '000626',
                    '000638',
                    '000657', '000659', '000663', '000669', '000677', '000705', '000759', '000766', '000780',
                    '000792',
                    '000815', '000852', '000885', '000909', '000913', '000921', '000928', '000931', '002006',
                    '002012',
                    '002034']
    else:
        codelist = qa.QA_fetch_stock_list_adv().code.tolist()
    return codelist[:count]


def read_zxg(filename='zxg.txt', length=6):
    """从文件filename读取自选股列表
    返回每行前length(默认：6）个字符（自动去除行首、行尾空格）;

    :param filename: 自选股文件名（默认：zxg.txt)
    """
    filename = getRealFilename(filename)
    resultList = alist = []
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='UTF-8') as zxg:
            alist = zxg.readlines()
    for a in alist:
        resultList.append(a.strip()[0:length])
    return resultList


def xls2zxg(xlsfile, zxgFile):
    """xls转换成文本
    """
    xlsfile = getRealFilename(xlsfile)
    try:
        df = pd.read_excel(xlsfile)
    except Exception as e:
        df = pd.read_csv(xlsfile, sep="\t", encoding="gbk", dtype={'证券代码': str})
    df.to_csv(zxgFile, index=False, sep=" ", header=None)


def xls2Code(xlsfile):
    """提取xlsfile文件中的股票代码
    """
    zxgfile = "/tmp/{}.txt".format(xlsfile)
    xls2zxg(xlsfile, zxgfile)
    return read_zxg(zxgfile, length=6)


def codeInETF(codes=[], filterStartWith=['159', '510', '512', '515', '513', '161', '162']):
    """股票代码过滤
    """
    return [item for item in codes if item.startswith(tuple(filterStartWith))]


def etfAmountGreater(code, startDate, endDate=None, amount=1000):
    """成交额大于等于amount(万元）"""
    df = qa.QA_fetch_index_day_adv(code, startDate, endDate)
    return df[df['amount'] >= amount * 10000]


def codeInfo(codes):
    """返回指数或etf对应的股票信息"""
    index = qa.QA_fetch_index_list_adv()
    etf = qa.QA_fetch_etf_list()
    return pd.concat([index[index['code'].isin(codes)], etf[etf['code'].isin(codes)]], axis=0)


def getRealFilename(filename):
    """返回第一个filename存在的文件名
    """
    try:
        # 当前目录
        dir_path = os.path.dirname(os.path.realpath(__file__))
    except:
        dir_path = os.path.dirname(os.path.realpath("./"))
    if not filename.find(os.sep) > -1:
        if os.path.exists(filename):
            # 当前目录优先
            pass
        else:
            # 如果文件名（fname）没有目录，则加上当前目录
            filename = os.path.join(dir_path, filename)
    return filename


# def read_zxg_not_in_file(filename='zxg.txt', length=6):

def full_pickle(title, data):
    """Saves the "data" with the "title" and adds the .pickle
    """
    pikd = open(title, 'wb')
    pickle.dump(data, pikd)
    pikd.close()


def loosen_pickle(file):
    """loads and returns a pickled objects
    """
    pikd = open(file, 'rb')
    data = pickle.load(pikd)
    pikd.close()
    return data


def compressed_pickle(title, data):
    """Pickle a file and then compress it into a file with extension
    """
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        cPickle.dump(data, f)


def decompress_pickle(file):
    """Load any compressed pickle file

    :param file: 文件名
    """
    if not os.path.exists(file):
        file = file + '.pbz2'
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data


def somefunc(cls):
    instances = {}

    def _wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return _wrapper


def CMI(data: pd.DataFrame, n=100):
    """如何把市场划分为趋势行情和震荡行情，也就成了这个策略的关键，恒温器策略引入了市场波动指数（Choppy Market Index），简称CMI
    它是一个用来判断市场走势类型的技术指标。通过计算当前收盘价与N周期前收盘价的差值与这段时间内价格波动的范围的比值，来判断目前的价格走势是趋势还是震荡。
    CMI的计算公式为：
    CMI=(abs(Close-ref(close,(n-1)))*100/(HHV(high,n)-LLV(low,n))
    其中，abs是绝对值，n是周期数。

    策略逻辑
    一般来说CMI的值在0~100区间，值越大，趋势越强。当CMI的值小于20时，策略认为市场处于震荡模式；当CMI的值大于等于20时，策略认为市场处于趋势模式。

    整个策略逻辑，可以简化的写成下面这样：

    如果CMI < 20，执行震荡策略；
    如果CMI ≥ 20，执行趋势策略；
    """
    close = data.close
    dict = {"CMI": np.abs((close - qa.REF(close, n - 1))) * 100 / (qa.HHV(data.high, n) - qa.LLV(data.low, n))}
    return pd.DataFrame(dict)


def RSV(data: pd.DataFrame, n=14):
    """RSV=（收盘价-最低价）/（最高价-最低价）
    RSV有何规律呢？很明显，在股价上涨趋势中，往往收盘价接近最高价，此时RSV值接近于1
    """
    dict = {"RSV": (data.close - data.low) / (data.high - data.low)}
    return pd.DataFrame(dict)


def ifupMA(data, n=[20]):
    """收盘站上n均线上

    """
    if isinstance(n, int):
        # 传进来的参数为整数类型时
        dict = {'MA{}'.format(n): (data.close - qa.MA(data.close, n)).dropna() > 0}
    elif isinstance(n, list):
        dict = {'MA{}'.format(i): data.close - qa.MA(data.close, i) for i in n}
    return pd.DataFrame(dict).dropna() > 0


def fourWeek(data, m=20, n=20):
    """四周规则
    　　只要价格涨过前四个日历周内的最高价，则平回空头头寸，开立多头头寸。
    　　只要价格跌过前四个周内(照日历算满)的最低价，则平回多头头寸，建立空头头寸。
    """

    def flag(x, preFlag):
        if x['close'] > x['hclose']:
            preFlag[0] = 1
        elif x['close'] < x['lclose']:
            preFlag[0] = -1
        return preFlag[0]

    def highLow(data, m=20, n=20):
        ''' 计算n周期最 fw.join(upma)高收盘价、最低收盘价

        :param data: dataFrame
        :param n: 计算最高收盘价周期; 默认：20
        :param n: 计算最低收盘价周期; 默认：20
        :return:
        '''
        high = qa.HHV(data['close'], m - 1)
        low = qa.LLV(data['close'], n - 1)
        return pd.DataFrame({'hclose': high.shift(1), 'lclose': low.shift(1), 'close': data.close})

    df = highLow(data, m, n)
    preFlag = [0]
    df['flag'] = df.apply(lambda x: flag(x, preFlag), axis=1);
    return pd.DataFrame({'flag': df['flag']})


def TBSIndicator(data, m=20, n=20, maday=50):
    """陶博士中期信号
    """

    def flag(x, preFlag):
        if x['flag'] > 0 and x['MA{}'.format(maday)]:
            # 中期入场信号
            preFlag[0] = 1
        # elif x['flag'] < 0 or x['MA{}'.format(maday)]:
        elif x['flag'] < 0 and x['MA{}'.format(maday)]:
            # 中期出场信号 跌破20日收盘最低价或者ma50
            preFlag[0] = -1
        return preFlag[0]

    fw = fourWeek(data, m, n)
    maday = 50
    upma = ifupMA(data, maday)
    preFlag = [0]
    result = fw.join(upma).apply(lambda x: flag(x, preFlag), axis=1)
    return pd.DataFrame({'flag': result})


def TBSMonthIndicator(data, m=10, n=20):
    """陶博士月线牛熊判断
    10月交叉20月均线
    """
    def flag(x, preFlag):
        if x['jc']:
            # 金叉
            preFlag[0] = 1
        elif x['sc']:
            # 死叉
            preFlag[0] = -1
        return preFlag[0]

    close = data['close']
    ma1 = qa.MA(close, m)
    ma2 = qa.MA(close, n)
    cross1 = qa.CROSS_STATUS(ma1, ma2)
    cross2 = qa.CROSS_STATUS(ma2, ma1)
    preFlag = [0]
    # 金叉 死叉
    result = pd.DataFrame({'jc': cross1, 'sc':cross2}, index=ma1.index).apply(lambda x: flag(x, preFlag), axis=1)
    return pd.DataFrame({'flag': result})