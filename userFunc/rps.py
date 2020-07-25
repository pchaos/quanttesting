# -*- coding: utf-8 -*-
"""
@Time    : 2020/1/28 下午7:11

@File    : rps.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import datetime
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from abc import ABCMeta
import QUANTAXIS as qa
from .comm import str2date, date2str


# 计算收益率
def cal_ret(dataFrame, *args, **kwargs):
    '''计算相对收益率
    days:   周 5;月:20;半年：120; 一年:250
    '''
    if len(args) == 0:
        args = tuple([20])
    close = dataFrame.close
    colName = 'MARKUP'
    cols = []
    for num in args:
        coln = '{}{}'.format(colName, num)
        dataFrame[coln] = close / close.shift(num)
        cols.append(coln)
    # return dataFrame.iloc[-max(args):, :].fillna(0)
    # return dataFrame[cols].iloc[max(args):, :]
    return dataFrame[cols].iloc[max(args):, :].dropna()


# 计算RPS
def get_RPS(dataFrame, *args, **kwargs):
    """收益率dataFrame计算RPS
    """
    i = 0
    # print("日期：{} 数量：{}".format(dataFrame.index.get_level_values(0)[0], len(dataFrame)))
    for col in dataFrame.columns:
        newcol = col.replace("MARKUP", "RPS", 1)
        if i > 0:
            df2 = getSingleRPS(dataFrame, col, newcol)
            df[newcol] = df2[newcol]
        else:
            df = getSingleRPS(dataFrame, col, newcol)
        i += 1
    return df


def getSingleRPS(dataFrame, col, newcol):
    df = pd.DataFrame(dataFrame[col].sort_values(ascending=False).dropna())
    dfcount = len(df)
    # range间隔-100.，这样就不用乘以100%了
    df['n'] = range(dfcount * 100, 0, -100)
    df[newcol] = df['n'] / dfcount
    # 删除index date
    return df.reset_index().set_index(['code'])[[newcol]]


class RPSAbs(metaclass=ABCMeta):
    """计算RPS基础类
    """

    def __init__(self, codes=[], startDate=datetime.date.today(), endDate=None, rpsday=[20, 50]):
        self._codes = codes
        self._startDate = startDate
        self._endDate = endDate
        self._rpsday = rpsday
        self._rps = None

    @property
    def codes(self):
        """代码列表（list）"""
        return self._codes

    @codes.setter
    def codes(self, value):
        self._codes = value

    def __repr__(self):
        return '{0}->{1}'.format(self._codes, len(self._codes))

    @abstractmethod
    def _fetchData(self):
        """获取QA_DataStruct
        @return QA_DataStruct
        """
        # data = qa.QA_fetch_index_day_adv(self.__codes, self.__startDate, self.__endDate)
        # return None

    def rps(self, reCaculate=True) -> pd.DataFrame:
        """计算rps
        @return pd.DataFrame
        """
        if reCaculate:
            # 需要重新计算
            self._rps = None
        if self._rps is None:
            self._getRPS()
        return self._rps

    def rpsTopN(self, theday: datetime.datetime, percentN=5) -> pd.DataFrame:
        """RPS排名前percentN%的数据
        """
        rps = self._getRPS()
        lastday = theday = str2date(date2str(theday))
        while 1:
            # 定位最近的rps数据
            dfn = []
            try:
                df = rps.loc[(slice(pd.Timestamp(theday), pd.Timestamp(lastday))), :]
                if len(df) > 0:
                    # 排名前N%的指数
                    for col in df.columns:
                        # dfn.append(df.sort_values(by=col, ascending=False).reset_index().head(int(len(df) / (100 / percentN))))
                        dfn.append(np.round(df[df[col] >= 100 - percentN], decimals=4))
                    dftopn = pd.concat(dfn).drop_duplicates()
                    # print(dftopn)
                    break
                lastday = theday
                theday = theday - datetime.timedelta(1)
            except Exception as e:
                theday = theday - datetime.timedelta(1)
        # rps平均值
        dftopn['AVERAGERPS'] = dftopn.sum(axis=1) / len(df.columns)
        return np.round(dftopn, decimals=2)

    def rpsTopN2(self, startday: datetime.datetime, lastday=None, percentN=5) -> pd.DataFrame:
        """RPS排名前percentN%的数据
        """
        rps = self._getRPS()
        if lastday is None:
            lastday = startday = str2date(date2str(startday))
        else:
            startday = str2date(date2str(startday))
        while 1:
            # 定位最近的rps数据
            dfn = []
            try:
                df = rps.loc[(slice(pd.Timestamp(startday), pd.Timestamp(lastday))), :]
                if len(df) > 0:
                    # 排名前N%的指数
                    dftopn = pd.concat([df.loc[(rps[item] >= 100 - percentN)] for item in df.columns]).sort_index()
                    df = dftopn.reset_index()
                    dftopn = df.drop_duplicates(subset=df.columns).set_index(['date', 'code']).sort_index()
                    # df.drop_duplicates(subset=df.columns).sort_values(by=dftopn.columns[0], ascending=False).set_index(
                    #     ['date', 'code']).sort_index()
                    # dftopn.drop_duplicates(inplace=True)
                    # dftopn.sort_values(by=dftopn.columns[0], ascending=False, inplace=True)
                    # print(dftopn)
                    break
                lastday = startday
                startday = startday - datetime.timedelta(1)
            except Exception as e:
                startday = startday - datetime.timedelta(1)
        # rps平均值
        dftopn['AVERAGERPS'] = dftopn.sum(axis=1) / len(dftopn.columns)
        return np.round(dftopn, decimals=2)

    def _getRPS(self):
        if self._rps is None:
            # 未计算rps，则先计算rps
            data = self._fetchData()
            df = data.add_func(cal_ret, *(self._rpsday))
            self._rps = df.groupby(level=0).apply(get_RPS, *(self._rpsday))
        return self._rps

    def selectCode(self, code):
        """查询相应的代码
        """
        rps = self._getRPS()
        return rps.loc[(slice(None), code), :]


class RPSIndex(RPSAbs):
    """计算index RPS
    """

    def _getRPS2(self):
        """ 未完成功能
        完成后功能等同原_getRPS

        Returns:

        """
        if self._rps is None:
            # 未计算rps，则先计算rps
            data = self._fetchData()
            dataFrame = pd.DataFrame(data.data['close'])
            colName = 'RPS'
            cols = []
            for num in self._rpsday:
                coln = '{}{}'.format(colName, num)
                # dataFrame[coln] = data.close.groupby(level=0).rank(axis=1, pct=True) * 100
                dataFrame[coln] = data.close.groupby(level=1).pct_change(periods=num).groupby(level=0).rank(axis=1, pct=True, ascending=True)  * 100
                cols.append(coln)
            if 'close' in dataFrame.columns:
                del dataFrame['close']

            # self._rps = dataFrame[cols].iloc[max(self._rpsday):, :].dropna().reset_index().sort_values(cols[0], ascending=False).set_index(["date", "code"])
            self._rps = dataFrame[cols].iloc[max(self._rpsday):, :].dropna()
            # self._rps.reset_index().sort_values('RPS20', ascending=False).set_index(["date", "code"])
        return self._rps

    def _fetchData(self):
        """
        @return QA_DataStruct_Index_day
        """
        data = qa.QA_fetch_index_day_adv(self._codes, self._startDate, self._endDate)
        return data


class RPSStock(RPSAbs):
    def _fetchData(self):
        """
        @return QA_DataStruct_stock_day
        """
        data = qa.QA_fetch_stock_day_adv(self._codes, self._startDate, self._endDate)
        return data
