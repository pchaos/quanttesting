# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/1 下午9:28

@File    : qaETFdatastruct.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

from QUANTAXIS import QA_DataStruct_Day


class QAIndex_DataStruct_Day(QA_DataStruct_Day):
    def __init__(self, data, dtype='unknown_day', if_fq='bfq'):
        '''
        '''
        super().__init__(data, dtype, if_fq)
        if self.data.index.names[0] == None:
            self.data.index.names = ['date', 'code']

    def pivot(self, column_):
        """增加对于多列的支持"""
        if isinstance(column_, str):
            try:
                # index 名称; self.data.index.names=['date', 'code']
                idx = self.data.index.names
                if len(idx) >= 2:
                    return self.data.reset_index().pivot(
                        index=idx[0],
                        columns=idx[1],
                        values=column_
                    )
                else:
                    return self.data.reset_index().pivot(
                        index='datetime',
                        columns='code',
                        values=column_
                    )
            except:
                return self.data.reset_index().pivot(
                    index='date',
                    columns='code',
                    values=column_
                )
        elif isinstance(column_, list):
            try:
                idx = self.data.index.names
                if len(idx) >= 2:
                    return self.data.reset_index().pivot_table(
                        index=idx[0],
                        columns=idx[1],
                        values=column_
                    )
                else:
                    return self.data.reset_index().pivot_table(
                        index='datetime',
                        columns='code',
                        values=column_
                    )
            except:
                return self.data.reset_index().pivot_table(
                    index='date',
                    columns='code',
                    values=column_
                )
