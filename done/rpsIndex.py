# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/22 上午12:55

@File    : rpsIndex.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import datetime
import pandas as pd
import QUANTAXIS as qa
from QUANTAXIS.QAData import (QA_DataStruct_Index_day)
from userFunc.myFunction import read_zxg, setdiff_sorted
from userFunc import compressed_pickle, decompress_pickle
from userFunc import cal_ret, get_RPS, RPSIndex


def getIndexCalret(fileName, code, startDate, endDate):
    """从本地缓存获取指数。若本地没有，则从数据库读取，并且在本地保存一份

    Args:
        fileName:文件名
        code:代码
        startDate:起始日期
        endDate:截止日期

    Returns:

    """
    try:
        # 获取指数数据
        dataCalret = decompress_pickle(fileName)
    except Exception as e:
        data = qa.QA_fetch_index_day_adv(code, startDate, endDate)
        df = data.add_func(cal_ret)
        compressed_pickle(fileName, data.data)
        dataCalret = decompress_pickle(fileName)
        data2 = dataCalret
    return dataCalret


def getCode(fileName=None, excludeFileName='zxgExclude.txt') -> None:
    if fileName is None:
        fileName = '/tmp/code.pickle'
    try:
        code = decompress_pickle(fileName)
    except Exception as e:
        code = list(qa.QA_fetch_index_list_adv()['code'][:])
        codeexclude = read_zxg(excludeFileName)
        # 排除某些股票
        code = setdiff_sorted(code, codeexclude)
        compressed_pickle(fileName, code)

    days = 365 * 1.2
    # days = 365 * 10
    start = datetime.datetime.now() - datetime.timedelta(days)
    end = datetime.datetime.now() - datetime.timedelta(0)
    fileName = '/tmp/data{}.pickle'.format(days)
    data2 = getIndexCalret(fileName, code, start, end)
    return code, data2


def _getRPS(rpsday, dataFrame):
    # data = qa.QA_DataStruct_Index_day(self.data2)
    data = qa.QA_DataStruct_Index_day(dataFrame)
    df = data.add_func(cal_ret, *rpsday)
    matching = [s for s in df.columns if "MARKUP" in s]
    print(df.head())
    # 计算RPS
    dfg = df.groupby(level=0).apply(get_RPS, *rpsday)
    return dfg


def indexRPSMain():
    # 显示rps排名前10%的中文名称
    code, data2 = getCode(excludeFileName='../testing/userFunc/zxgExclude.txt')
    rpsday = [20, 50]
    days = 300 * 1.2
    start = datetime.datetime.now() - datetime.timedelta(days)
    end = datetime.datetime.now() - datetime.timedelta(0)
    # dfrps = _getRPS(rpsday, data2)
    rpsIndex = RPSIndex(code, start, end, rpsday)
    rpstopn = rpsIndex.rps()
    print(rpstopn.head(20))
    print(rpstopn.tail(10))
    # 排名前n%
    n = 10
    # fil = lambda x: (x['RPS20'] > 100 - n) | (x['RPS50'] > 100 - n)
    # fil = lambda x :[x['RPS{}'.format(item)] > 100-n  for item in rpsday]
    # rpstopn.loc[(rpstopn['RPS20'] > 100 - n) | (rpstopn['RPS50'] > 100 - n)]
    rpstopn = pd.concat([rpstopn.loc[(rpstopn[item] > 100 - n)] for item in rpstopn.columns])
    rpstopn.drop_duplicates(inplace=True)
    rpstopn2 = rpsIndex.rpsTopN(end, n)
    print(" 指数总数： {}，RPS排名前{}% 的个数{}：\n".format(len(code), n, len(rpstopn)))
    print("日期： {}".format(end))
    print("rpstopn", rpstopn.tail(10))
    print("rpstopn2", rpstopn2.head(10))
    #  todo rpstopn concat rpstopn2
    return rpstopn


def indexcnName(dftopn: pd.DataFrame):
    # 插入中文名称
    codetop = list(dftopn.index.levels[1])
    indexList = qa.QA_fetch_index_list_adv()
    # for c in codetop:
    #     # 打印股票代码及中文名8
    #     print(c, indexList.loc[c]['name'])
    print("排名靠前的数量：{}".format(len(codetop)))
    # 插入中文名
    dftopn.reset_index(inplace=True)
    #
    # dftopn['name'] = dftopn['code'].apply(lambda x: indexList.loc[x]['name'])
    dftopn.insert(1, 'name', dftopn['code'].apply(lambda x: indexList.loc[x]['name']))
    return dftopn.set_index(['date', 'code'])


if __name__ == '__main__':
    rpstop = indexRPSMain()
    rpstop = indexcnName(rpstop)
    # 保存到文件
    # rpstop.to_csv('/tmp/rpstop.csv', encoding='utf-8', index=True)
    rpstop.to_excel('/tmp/rpstop.xlsx', encoding='utf-8', index=True)
