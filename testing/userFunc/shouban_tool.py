# -*- coding: utf-8 -*-
"""首板工具箱
合并csv文件
"""

import os
import pandas as pd
from datetime import datetime


def getCvsFilelist(path):
    """获取path目录下csv文件列表
    不包含后缀为'.csv#'的文件
    """
    files = []
    # 获取path目录下csv文件列表
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                if not file.endswith('.csv#'):
                    files.append(os.path.join(r, file))
    return files


def mergeAll(path='./'):
    # 从csv文件读入数据，合并为一个文件
    files = getCvsFilelist(path)
    result = []
    if len(files) > 0:
        # 目录下有文件
        for f in files:
            if len(os.path.basename(f)) == 16:
                print('处理文件{}'.format(f))
                # 类似“sb2018-08-01.csv”，这样的文件名
                df = pd.read_csv(f, converters={'股票代码': str})
                result.append(df)

    return pd.concat(result)


if __name__ == '__main__':
    target = 'all.csv'
    path = './'
    # path = '/tmp'
    merge = mergeAll(path)
    # 保存为csv文件
    merge.to_csv(os.path.join(path, target), index=False)
