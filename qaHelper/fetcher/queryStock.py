# -*- coding: utf-8 -*-

import datetime

import numpy
import pandas as pd
from pandas import DataFrame
from QUANTAXIS.QAUtil import (DATABASE)
from QUANTAXIS.QAData import (QA_DataStruct_Stock_day, QA_DataStruct_Stock_min)
from .query import QueryMongodb
from qaHelper.fetcher.classproperty import classproperty


class QueryStock(QueryMongodb):
    """股票数据接口（mongodb）

    """
    # 是否重新设置index
    _ifDropIndex = True
    _format = "pd"

    @classproperty
    def ifDropIndex(cls):
        return cls._ifDropIndex

    @ifDropIndex.setter
    def ifDropIndex(cls, value):
        cls._ifDropIndex = value

    @ifDropIndex.deleter
    def ifDropIndex(cls):
        del cls._ifDropIndex

    def __init__(self, collectionsDay=DATABASE.stock_day, collectionsMin=DATABASE.stock_min):
        self._collectionsDay = collectionsDay
        self._collectionsMin = collectionsMin

    @classmethod
    def getDay(cls, code, start, end, if_fq='00', frequence=9) -> DataFrame:
        '''

        :param code:  股票代码
        :param start: 开始日期
        :param end:   结束日期
        :param if_drop_index:
        :param collections: 默认数据库
        :return: 如果股票代码不存 或者开始结束日期不存在 在返回 None ，合法返回 QA_DataStruct_Stock_day 数据
        '''
        '获取股票日线'
        end = start if end is None else end
        start = str(start)[0:10]
        end = str(end)[0:10]

        if start == 'all':
            start = '1990-01-01'
            end = str(datetime.date.today())
        res = super(QueryStock, cls).getDay(code, start, end, if_fq, frequence)
        return res

    @classmethod
    def getMin(cls, code, start, end, if_fq='00', frequence=8) -> DataFrame:
        '''
        '获取股票分钟线'
        :param code:  字符串str eg 600085
        :param start: 字符串str 开始日期 eg 2011-01-01
        :param end:   字符串str 结束日期 eg 2011-05-01
        :param frequence: 整型 分钟线的类型 支持 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m 类型
        :param if_drop_index: Ture False ， dataframe drop index or not
        :param collections: mongodb 数据库
        :return: QA_DataStruct_Stock_min 类型
        '''
        # collections = DATABASE.stock_min
        # __data = [] 未使用
        #
        end = start if end is None else end
        if isinstance(start, str):
            if len(start) == 10:
                start = '{} 09:30:00'.format(start)

            if len(end) == 10:
                end = '{} 15:00:00'.format(end)

            if start == end:
                # 🛠 todo 如果相等，根据 frequence 获取开始时间的 时间段 QA_fetch_stock_min， 不支持start end是相等的
                print(
                    "QA Error QA_fetch_stock_min_adv parameter code=%s , start=%s, end=%s is equal, should have time span! "
                    % (code,
                       start,
                       end)
                )
                return None

        # 🛠 todo 报告错误 如果开始时间 在 结束时间之后

        res = super(QueryStock, cls).getMin(code, start, end, if_fq, frequence=frequence)
        return res

    @classmethod
    def _getStoring(cls, storing=None):
        return 'stock'
