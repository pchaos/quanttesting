# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod, ABCMeta
import pandas as pd
from QUANTAXIS.QAData import (QA_DataStruct_Stock_day, QA_DataStruct_Stock_min)
from .classproperty import classproperty

# import QUANTAXIS as qa

# 周期
PERIODS = {5: 0, 15: 1, 30: 2, 60: 3, "w": 5, "m": 6, 1: 8, "d": 9,
           "W": 5, "M": 6, 1: 8, "D": 9,
           "5m": 0, "15m": 1, "30m": 2, "60m": 3, "week": 5, "month": 6, "1m": 8, "day": 9,
           "5M": 0, "15M": 1, "30M": 2, "60M": 3, "WEEK": 5, "MONTH": 6, "1M": 8, "DAY": 9,
           "Week": 5, "Month": 6, "Day": 9,
           "5min": 0, "15min": 1, "30min": 2, "60min": 3, "1min": 8,
           "5Min": 0, "15Min": 1, "30Min": 2, "60Min": 3, "1Min": 8,
           "5MIN": 0, "15MIN": 1, "30MIN": 2, "60MIN": 3, "1MIN": 8,
           "five": 0, "fifteen": 1, "half": 2, "1h": 3, "one": 8,
           "q": 10, "quarter": 10,
           "Q": 10, "QUARTER": 10,
           "y": 11, "year": 11,
           "Y": 11, "YEAR": 11
           }

REVERSPERIODS = {0: "5min", 1: "15min", 2: "30min", 3: "60min", 5: "week",
                 6: "month", 8: "1min", 9: "day", 10: "quarter", 11: "year"}
# 股票周期倍数
PERIODSLENS = {0: 48, 1: 16, 2: 8, 3: 4, 5: 1,
               6: 1, 8: 240, 9: 1, 10: 1, 11: 1}


class Fetcher(ABC, metaclass=ABCMeta):
    """

    """
    # 返回数据格式
    _format = "numpy"

    @classproperty
    def format(cls):
        return cls._format

    @format.setter
    def format(cls, value):
        if cls._format != value:
            cls._format = value

    @format.deleter
    def format(cls):
        del cls._format

    @classmethod
    def getFrequence(cls, frequence: str):
        """股票周期

        返回一分钟周期对应的数字：getFrequence('1min')

        返回日线周期对应的数字：getFrequence('d')

        Args:
            frequence: FREQUENCE = {5: 0, 15: 1, 30: 2, 60: 3, "w": 5, "m": 6, 1: 8, "d": 9,
             "5m": 0, "15m": 1, "30m": 2, "60m": 3, "week": 5, "month": 6, "1m": 8, "day": 9,
             "5min": 0, "15min": 1, "30min": 2, "60min": 3, "1min": 8,
             "five": 0, "fifteen": 1, "half": 2, "1h": 3, "one": 8,
             "q": 10, "quarter": 10,
             "y": 11, "year": 11
             }

        Returns:返回周期对应的整数类型

        """
        # if isinstance(frequence, str):
        #     # 字符串统一转换成小写字母.（会引起速度变慢两倍）
        #     frequence = frequence.lower()
        return PERIODS.get(frequence)

    @classmethod
    def getReverseFrequence(cls, frequence: int):
        """返回周期标准写法

        Args:
            frequence: 取值范围：REVERSEFREQUENCE = {0: "5min", 1: "15min", 2: "30min", 3: "60min", 5: "week",
                    6: "month", 8: "1min", 9: "day", 10: "quarter", 11: "year"}

        Returns: Tuple(周期，周期标准写法， 周期倍数）

        """
        return frequence, REVERSPERIODS.get(frequence), PERIODSLENS.get(frequence)

    @classmethod
    def getAdv(cls, code, start, end, if_fq='00', frequence='day'):
        """返回QA_DataStruct_Stock结构
        """
        if isinstance(frequence , str):
            frequence = cls.getFrequence(frequence)
        res = cls.get(code, start, end, if_fq, frequence)
        if res is None:
            # 🛠 todo 报告是代码不合法，还是日期不合法
            print(
                "QA Error getAdv parameter code=%s , start=%s, end=%s call get return None"
                % (code,
                   start,
                   end)
            )
            return None
        else:
            if isinstance(res, pd.DataFrame):
                res_reset_index = res.set_index(['date', 'code'], drop=cls.ifDropIndex)
                if 5 <= frequence != 8:
                    # 日线以上周期
                    return QA_DataStruct_Stock_day(res_reset_index)
                else:
                    return QA_DataStruct_Stock_min(res_reset_index)
            else:
                return None

    @classmethod
    def get(cls, code, start, end, if_fq='00',
            frequence='day'):
        """通达信历史数据

        Args:
            code:
            start:
            end:
            if_fq:
            frequence: K线周期
                0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
                5 周K线
                6 月frequence = cls.getFrequence(frequence)K线
                7 1分钟
                8 1分钟K线
                9 日K线
                10 季K线
                11 年K线

        Returns:

        """
        if isinstance(frequence , str):
            frequence = cls.getFrequence(frequence)
        if 5 <= frequence != 8:
            #日线以上周期
            return cls.getDay(code, start, end, if_fq, frequence)
        else:
            # 日线以下周期
            return cls.getMin(code, start, end, if_fq, frequence)


    @classmethod
    @abstractmethod
    def getDay(cls, code, start_date, end_date, if_fq, frequence):
        """获取日线及以上级别的数据

        Arguments:
            code {str:6} -- code 是一个单独的code 6位长度的str
            start_date {str:10} -- 10位长度的日期 比如'2017-01-01'
            end_date {str:10} -- 10位长度的日期 比如'2018-01-01'
        Keyword Arguments:
            if_fq {str} -- '00'/'bfq' -- 不复权 '01'/'qfq' -- 前复权 '02'/'hfq' -- 后复权 '03'/'ddqfq' -- 定点前复权 '04'/'ddhfq' --定点后复权
            frequency {int} -- K线周期
                0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
                5 周K线
                6 月K线
                7 1分钟
                8 1分钟K线
                9 日K线
                10 季K线
                11 年K线
            ip {str} -- [description] (default: None) ip可以通过select_best_ip()函数重新获取
            port {int} -- [description] (default: {None})
        Returns:
            pd.DataFrame/None -- 返回的是dataframe,如果出错比如只获
            取了一天,而当天停牌,返回None
        Exception:
            如果出现网络问题/服务器拒绝, 会出现socket:time out 尝试再次获取/更换ip即可, 本函数不做处理
        """
        pass

    @classmethod
    @abstractmethod
    def getMin(cls, code, start, end, if_fq, frequence):
        pass
