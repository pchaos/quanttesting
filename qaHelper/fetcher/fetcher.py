# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

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


class Fetcher(ABC):
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
    @abstractmethod
    def get(cls, code, start_date, end_date, if_fq='00',
            frequence='day'):
        pass
