# -*- coding: utf-8 -*-
import unittest
import pandas as pd

class QhBaseTestCase(unittest.TestCase):
    """测试基类
    """
    def differOneByOne(self, df1: pd.DataFrame, df2:pd.DataFrame):
        """两个dataframe逐个比较
        """
        oneByOne = []
        # 逐个比较，判断哪一天不匹配
        for i in range(len(df1)):
            for col in df1.columns:
                if df1[col][i] != df2[col][i]:
                    oneByOne.append([{"比较顺序": i}, col, df1[col][i], df2[col][i], df1.iloc[i]])
        return oneByOne
