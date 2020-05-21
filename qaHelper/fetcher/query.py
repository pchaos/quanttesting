# -*- coding: utf-8 -*-

import datetime

import numpy
import pandas as pd
from pandas import DataFrame
from QUANTAXIS.QAUtil import (
    DATABASE,
    QA_Setting,
    QA_util_date_stamp,
    QA_util_date_valid,
    QA_util_dict_remove_key,
    QA_util_log_info,
    QA_util_code_tolist,
    QA_util_date_str2int,
    QA_util_date_int2str,
    QA_util_sql_mongo_sort_DESCENDING,
    QA_util_time_stamp,
    QA_util_to_json_from_pandas,
    trade_date_sse
)
from .fetcher import Fetcher
from .classproperty import classproperty


class QueryMongodb(Fetcher):
    # 默认数据库表名
    _collectionsDay = DATABASE.stock_day
    _collectionsMin = DATABASE.stock_min

    @classproperty
    def collectionsDay(cls):
        return cls._collectionsDay

    @collectionsDay.setter
    def collectionsDay(cls, value):
        if cls._collectionsDay.name != value.name:
            cls._collectionsDay = value

    @collectionsDay.deleter
    def collectionsDay(cls):
        del cls._collectionsDay

    @classproperty
    def collectionsMin(cls):
        """分钟线使用的mongodb collections
        """
        return cls._collectionsMin

    @collectionsMin.setter
    def collectionsMin(cls, value):
        if cls._collectionsMin.name != value.name:
            cls._collectionsMin = value

    @collectionsMin.deleter
    def collectionsMin(cls):
        del cls._collectionsMin

    @classmethod
    def getDay(cls, code, start, end, if_fq='00', frequence=9):
        """'获取股票日线'

        Returns:
            [type] -- [description]

            感谢@几何大佬的提示
            https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/#return-the-specified-fields-and-the-id-field-only

        """
        collections = cls.collectionsDay
        if not isinstance(start, str) and (len(start) != 10):
            start = str(start)[0:10]
            end = str(end)[0:10]
        # code= [code] if isinstance(code,str) else code

        # code checking
        code = QA_util_code_tolist(code)

        if QA_util_date_valid(end):

            cursor = collections.find(
                {
                    'code': {
                        '$in': code
                    },
                    "date_stamp":
                        {
                            "$lte": QA_util_date_stamp(end),
                            "$gte": QA_util_date_stamp(start)
                        }
                },
                {"_id": 0},
                batch_size=10000
            )
            # res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

            res = pd.DataFrame([item for item in cursor])
            try:
                res = res.assign(
                    volume=res.vol,
                    date=pd.to_datetime(res.date)
                ).drop_duplicates((['date',
                                    'code'])).query('volume>1').set_index(
                    'date',
                    drop=False
                )
                if not('up_count' in res.columns):
                    res = res.loc[:,
                          [
                              'code',
                              'open',
                              'high',
                              'low',
                              'close',
                              'volume',
                              'amount',
                              'date'
                          ]]
                # else:
                #     res = res.loc[:,
                #           [
                #               'code',
                #               'open',
                #               'high',
                #               'low',
                #               'close',
                #               'volume',
                #               'amount',
                #               'date',
                #               'up_count',
                #               'down_count'
                #           ]]
            except:
                res = None
            if cls.format in ['P', 'p', 'pandas', 'pd']:
                return res
            elif cls.format in ['json', 'dict']:
                return QA_util_to_json_from_pandas(res)
            # 多种数据格式
            elif cls.format in ['n', 'N', 'numpy']:
                return numpy.asarray(res)
            elif cls.format in ['list', 'l', 'L']:
                return numpy.asarray(res).tolist()
            else:
                print(
                    "QA Error QA_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" "
                    % cls.format
                )
                return None
        else:
            QA_util_log_info(
                'QA Error getDay data parameter start=%s end=%s is not right'
                % (start,
                   end)
            )

    @classmethod
    def getMin(cls, code, start, end, if_fq='00', frequence=8):
        collections = cls.collectionsMin
        '获取股票分钟线'
        _, type_, _ = cls.getReverseFrequence(frequence)

        _data = []
        # code checking
        code = QA_util_code_tolist(code)

        cursor = collections.find(
            {
                'code': {
                    '$in': code
                },
                "time_stamp":
                    {
                        "$gte": QA_util_time_stamp(start),
                        "$lte": QA_util_time_stamp(end)
                    },
                'type': type_
            },
            {"_id": 0},
            batch_size=10000
        )

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.assign(
                volume=res.vol,
                datetime=pd.to_datetime(res.datetime)
            ).query('volume>1').drop_duplicates(['datetime',
                                                 'code']).set_index(
                'datetime',
                drop=False
            )
            # return res
        except:
            res = None
        if cls.format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif cls.format in ['json', 'dict']:
            return QA_util_to_json_from_pandas(res)
        # 多种数据格式
        elif cls.format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif cls.format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print(
                "QA Error QA_fetch_stock_min format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" "
                % cls.format
            )
            return None
