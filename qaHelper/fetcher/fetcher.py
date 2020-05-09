# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

# import QUANTAXIS as qa

FREQUENCE = {5: 0, 15: 1, 30: 2, 60: 3, "w": 5, "m": 6, 1: 8, "d": 9,
             "5m": 0, "15m": 1, "30m": 2, "60m": 3, "week": 5, "month": 6, "1m": 8, "day": 9,
             "5min": 0, "15min": 1, "30min": 2, "60min": 3, "1min": 8,
             "five": 0, "fifteen": 1, "half": 2, "1h": 3, "one": 8,
             "q": 10, "quarter": 10,
             "y": 11, "year": 11
             }

REVERSEFREQUENCE = {0: "5min", 1: "15min", 2: "30min", 3: "60min", 5: "week",
                    6: "month", 8: "1min", 9: "day", 10: "quarter", 11: "year"}


class Fetcher(ABC):
    @classmethod
    def getFrequence(cls, frequence: str):
        # if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
        #     frequence = 9
        # elif frequence in ['w', 'W', 'Week', 'week']:
        #     frequence = 5
        # elif frequence in ['month', 'M', 'm', 'Month']:
        #     frequence = 6
        # elif frequence in ['Q', 'Quarter', 'q']:
        #     frequence = 10
        # elif frequence in ['y', 'Y', 'year', 'Year']:
        #     frequence = 11
        # elif str(frequence) in ['5', '5m', '5min', 'five']:
        #     frequence = 0
        # elif str(frequence) in ['1', '1m', '1min', 'one']:
        #     frequence = 8
        # elif str(frequence) in ['15', '15m', '15min', 'fifteen']:
        #     frequence = 1
        # elif str(frequence) in ['30', '30m', '30min', 'half']:
        #     frequence = 2
        # elif str(frequence) in ['60', '60m', '60min', '1h']:
        #     frequence = 3

        return FREQUENCE.get(frequence)

    @classmethod
    def getReverseFrequence(cls, frequence: int):
        return REVERSEFREQUENCE.get(frequence)

    @classmethod
    @abstractmethod
    def get(cls, code, start_date, end_date, if_fq='00',
            frequence='day'):
        pass
