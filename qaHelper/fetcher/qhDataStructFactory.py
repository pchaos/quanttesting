# -*- coding: utf-8 -*-
"""QA_Struture工厂模式

"""

import pandas as pd
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Index_day, QA_DataStruct_Index_min
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Stock_day, QA_DataStruct_Stock_min
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Future_day, QA_DataStruct_Future_min
from QUANTAXIS.QAUtil import DATABASE


class QhDataStructFactory(object):
    """QA_DataStruct工厂类

    """

    def __init__(self, frequence=9, type='stock'):
        """

        Args:
            frequence: 周期
            type: ‘stock’：股票
                ‘index’：指数或etf
                ‘future’：期货
                ‘auto’：自动识别
        """
        if type == 'stock':
            if 5 <= frequence != 8:
                # 日线以上周期
                self._dataStruct = lambda df, dtype=type, if_fq='bfq': QA_DataStruct_Stock_day(df, dtype=type,
                                                                                               if_fq=if_fq)
            else:
                self._dataStruct = lambda df, dtype=type, if_fq='bfq': QA_DataStruct_Stock_min(df, dtype=type,
                                                                                               if_fq=if_fq)
        elif type == 'index':
            if 5 <= frequence != 8:
                # 日线以上周期
                self._dataStruct = lambda df, dtype=type, if_fq='bfq': QA_DataStruct_Index_day(df, dtype=type,
                                                                                               if_fq=if_fq)
            else:
                self._dataStruct = lambda df, dtype=type, if_fq='bfq': QA_DataStruct_Index_min(df, dtype=type,
                                                                                               if_fq=if_fq)
        elif type == 'future':
            if 5 <= frequence != 8:
                # 日线以上周期
                self._dataStruct = lambda df, dtype=type, if_fq='bfq': QA_DataStruct_Future_day(df, dtype=type,
                                                                                                if_fq=if_fq)
            else:
                self._dataStruct = lambda df, dtype=type, if_fq='bfq': QA_DataStruct_Future_min(df, dtype=type,
                                                                                                if_fq=if_fq)
        else:
            raise Exception("不支持的类型")

    def dataStruct(self, df: pd.DataFrame, if_fq='bfq'):
        """返回QA_Struture结构数据

        Args:
            df: pd.DataFrame格式数据 。

        Returns:

        """
        if df is not None and len(df.index.names) == 1:
            # 设置index
            df = df.set_index(['date', 'code'], drop=True)
        return self._dataStruct(df)
