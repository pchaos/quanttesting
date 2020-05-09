# -*- coding: utf-8 -*-
"""
@Time    : 2020/4/22 上午12:55

@File    : rpsIndex.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import datetime
import QUANTAXIS as qa
from userFunc import compressed_pickle, decompress_pickle
from userFunc import cal_ret, get_RPS, RPSIndex


def getIndexCalret(readFromfile, code, startDate, endDate):
    try:
        # 获取指数数据
        dataCalret = decompress_pickle(readFromfile)
    except Exception as e:
        data = qa.QA_fetch_index_day_adv(code, startDate, endDate)
        df = data.add_func(cal_ret)
        compressed_pickle(readFromfile, data.data)
        dataCalret = decompress_pickle(readFromfile)
        data2 = dataCalret
    return dataCalret


def getCode() -> None:
    fileName = '/tmp/code.pickle'
    try:
        code = decompress_pickle(fileName)
    except Exception as e:
        code = list(qa.QA_fetch_index_list_adv()['code'][:])
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
    code, data2 = getCode()
    rpsday = [20, 50]
    days = 365 * 1.2
    start = datetime.datetime.now() - datetime.timedelta(days)
    end = datetime.datetime.now() - datetime.timedelta(0)
    # dfrps = _getRPS(rpsday, data2)
    rpsIndex = RPSIndex(code, start, end, rpsday)
    rpstopn = rpsIndex.rps()
    print(rpstopn.tail())
    print(rpstopn.head(20))
    # 排名前n%
    n = 10
    rpstopn = rpsIndex.rpsTopN(end, n)
    print("指数总数： {}，RPS排名前{}% 的个数{}：\n".format(len(code), n, len(rpstopn)), rpstopn)


if __name__ == '__main__':
    indexRPSMain()
