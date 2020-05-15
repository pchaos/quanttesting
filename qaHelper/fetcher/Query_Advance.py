# -*- coding: utf-8 -*-

import datetime

import numpy
import pandas as pd
from pandas import DataFrame
from QUANTAXIS.QAData import (QA_DataStruct_Stock_day)
from .Query import QueryMongodb
from qaHelper.fetcher.classproperty import classproperty


class QueryMongodb_adv(QueryMongodb):
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
        cls.format = 'pd'
        res = super(QueryMongodb_adv, cls).getDay(code, start, end, if_fq, frequence)
        if res is None:
            # 🛠 todo 报告是代码不合法，还是日期不合法
            print(
                "QA Error QA_fetch_stock_day_adv parameter code=%s , start=%s, end=%s call QA_fetch_stock_day return None"
                % (code,
                   start,
                   end)
            )
            return None
        else:
            res_reset_index = res.set_index(['date', 'code'], drop=cls.ifDropIndex)
            # if res_reset_index is None:
            #     print("QA Error QA_fetch_stock_day_adv set index 'datetime, code' return None")
            #     return None
            return QA_DataStruct_Stock_day(res_reset_index)
