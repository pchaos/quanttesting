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
from abc import ABC, abstractmethod
import QUANTAXIS as qa
from .comm import str2date, date2str


# 计算收益率
def cal_ret(dataFrame, *args, **kwargs):
    '''计算收益率
    days:周 5;月:20;半年：120; 一年:250
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
    return dataFrame[cols].iloc[max(args):, :]


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


class RPSAbs(ABC):
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
        return None

    def rps(self):
        data = self._fetchData()
        df = data.add_func(cal_ret, *(self._rpsday))
        self._rps = df.groupby(level=0).apply(get_RPS, *(self._rpsday))
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
                        dfn.append(round(df[df[col] >= 100 - percentN], 2))
                    dftopn = pd.concat(dfn).drop_duplicates()
                    # print(dftopn)
                    break
                lastday = theday
                theday = theday - datetime.timedelta(1)
            except Exception as e:
                theday = theday - datetime.timedelta(1)
        # rps平均值
        dftopn['AVERAGERPS'] = round(dftopn.sum(axis=1) / len(df.columns), 2)
        return dftopn

    def _getRPS(self):
        if self._rps is None:
            # 未计算rps，则先计算rps
            self.rps()
        return self._rps

    def selectCode(self, code):
        """查询相应的代码
        """
        rps = self._getRPS()
        return rps.loc[(slice(None), code), :]


class RPSIndex(RPSAbs):
    """计算index RPS
    """

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
