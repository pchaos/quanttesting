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
# import os.path as path
# import sys
# PARENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
# if PARENT_DIR not in sys.path:
#     sys.path.append(PARENT_DIR)
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


def getCode(fileName=None, excludeFileName='zxgExclude.txt'):
    """返回代码 及代码对应的数据

    Args:
        fileName:
        excludeFileName:

    Returns:

    """
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


def indexRPSMain(n=10):
    # 显示rps排名前10%的中文名称
    # 股票代码
    code, data2 = getCode(excludeFileName='../testing/userFunc/zxgExclude.txt')
    rpsday = [10, 20, 50]
    # rpsday = [20, 50]
    days = 300 * 1.2
    start = datetime.datetime.now() - datetime.timedelta(days)
    end = datetime.datetime.now() - datetime.timedelta(0)
    # dfrps = _getRPS(rpsday, data2)
    rpsIndex = RPSIndex(code, start, end, rpsday)
    rpstopn = rpsIndex.rps()
    print(rpstopn.head(20))
    print(rpstopn.tail(10))
    # 排名前n%
    # n = 40
    # fil = lambda x: (x['RPS20'] > 100 - n) | (x['RPS50'] > 100 - n)
    # fil = lambda x :[x['RPS{}'.format(item)] > 100-n  for item in rpsday]
    # rpstopn.loc[(rpstopn['RPS20'] > 100 - n) | (rpstopn['RPS50'] > 100 - n)]
    rpstopn = pd.concat([rpstopn.loc[(rpstopn[item] > 100 - n)] for item in rpstopn.columns])
    rpstopn.drop_duplicates(inplace=True)
    # rpstopn2 = rpsIndex.rpsTopN(end, n)
    rpstopn2 = rpsIndex.rpsTopN2(start, end, n)
    print(" 指数总数： {}，RPS排名前{}% 的个数{}：\n".format(len(code), n, len(rpstopn)))
    print("日期： {}".format(end))
    print("rpstopn", rpstopn.tail(10))
    print("rpstopn2", rpstopn2.head(10))
    #  todo rpstopn concat rpstopn2
    return rpstopn2


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


def save2Excel(dataFrame, filename, sheetName):
    """
    保存excel，设定列宽

    Args:
        dataFrame:
        filename:
        sheetName:

    Returns:

    """
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    # rpstop.to_excel(filename, encoding='utf-8', sheet_name=sheetName, index=True)
    if not isinstance(sheetName, list):
        dataFrame.to_excel(writer, encoding='utf-8', sheet_name=sheetName, index=True, float_format="%.2f")
        # 不合并单元格保存
        # dataFrame.to_excel(writer, encoding='utf-8', sheet_name=sheetName + "1", index=True, float_format="%.2f", merge_cells=False)
        worksheet = writer.sheets[sheetName]
        # 设置列宽
        for idx, col in enumerate(dataFrame):  # loop through all columns
            series = dataFrame[col]
            max_len = max((
                # series.astype(str).map(len).max(),  # len of largest item
                series.astype(str).str.len().max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            )) + 2  # adding a little extra space
            indexlen = len(dataFrame.index.names)
            worksheet.set_column(idx + indexlen, idx + indexlen, max_len)  # set column width
        worksheet.set_column(0, 0, 23)  # set column width
        writer.save()
    else:
        # 多dataframe保存到excel
        assert len(dataFrame) == len(sheetName)
        income_sheets = {}
        for i in range(len(sheetName)):
            income_sheets[sheetName[i]] = dataFrame[i]
        for sheet_name in income_sheets.keys():
            df = income_sheets[sheet_name]
            df.to_excel(writer, encoding='utf-8', sheet_name=sheet_name, index=True, float_format="%.2f")
            worksheet = writer.sheets[sheet_name]
            # 设置列宽
            for idx, col in enumerate(df):  # loop through all columns
                series = df[col]
                max_len = max((
                    # series.astype(str).map(len).max(),  # len of largest item
                    series.astype(str).str.len().max(),  # len of largest item
                    len(str(series.name))  # len of column name/header
                )) + 2  # adding a little extra space
                indexlen = len(df.index.names)
                worksheet.set_column(idx + indexlen, idx + indexlen, max_len)  # set column width
            worksheet.set_column(0, 0, 23)  # set column width

        writer.save()


if __name__ == '__main__':
    # 单个dataframeexcel保存
    # rpstop = indexRPSMain(n=40)
    # rpstop = indexcnName(rpstop)
    # # 保存到文件C
    # filename = '/tmp/rpstop.xlsx'
    # sheetName = "rps"
    # save2Excel(rpstop, filename, sheetName)

    # 多个dataframe保存excel
    rpstop = indexRPSMain(n=40)
    rpstop = indexcnName(rpstop)
    # 保存到文件
    filename = '/tmp/rpstop.xlsx'
    sheetName = "rps"
    rpstop2 = indexRPSMain(n=10)
    rpstop2 = indexcnName(rpstop2)
    # 保存到文件
    filename = '/tmp/rpstop.xlsx'
    sheetName2 = "rpsTop10"
    save2Excel([rpstop, rpstop2], filename, [sheetName, sheetName2])

    # TODO 查找新进入top 10%的板块
