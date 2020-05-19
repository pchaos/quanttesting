# -*- coding: utf-8 -*-
"""QA_Struture工厂模式

"""

import  pandas as pd
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Index_day, QA_DataStruct_Index_min
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Stock_day, QA_DataStruct_Stock_min
from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Future_day, QA_DataStruct_Future_min
from QUANTAXIS.QAUtil import DATABASE

class QHDataStructFactory(object):
    def __init__(self, frequence= 9, type= 'stock'):
        """

        Args:
            frequence: 周期
            type: ‘stock’：股票
                ‘index’：指数或etf
                ‘auto’：自动识别
        """
        if type =='stock':
            if 5 <= frequence != 8:
               # 日线以上周期
                self._dataStruct = QA_DataStruct_Stock_day
            else:
                self._dataStruct = QA_DataStruct_Stock_min
        elif type == 'index':
            if 5 <= frequence != 8:
               # 日线以上周期
                self._dataStruct = QA_DataStruct_Index_day
            else:
                self._dataStruct = QA_DataStruct_Index_min
        elif type == 'future':
            if 5 <= frequence != 8:
               # 日线以上周期
                self._dataStruct = QA_DataStruct_Future_day
            else:
                self._dataStruct = QA_DataStruct_Future_min

    def dataStruct(self, df:pd.DataFrame):
        """返回QA_Struture结构数据

        Args:
            df: pd.DataFrame格式数据 。

        Returns:

        """
        return self._dataStruct(df)