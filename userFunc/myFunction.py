# -*- coding: utf-8 -*-
import bz2
import pickle
import _pickle as cPickle
import os
import QUANTAXIS as qa
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache


def getCodeList(isTesting=True, count=5000):
    """
    isTesting: 是否使用测试数据
    count： 返回最多结果集数量
    """
    if isTesting:
        # 2018.8首板个股，测试用，减少调试时间
        codelist = ['000023', '000068', '000407', '000561', '000590', '000593', '000608', '000610', '000626',
                    '000638',
                    '000657', '000659', '000663', '000669', '000677', '000705', '000759', '000766', '000780',
                    '000792',
                    '000815', '000852', '000885', '000909', '000913', '000921', '000928', '000931', '002006',
                    '002012',
                    '002034']
    else:
        codelist = qa.QA_fetch_stock_list_adv().code.tolist()
    return codelist[:count]


def full_pickle(title, data):
    """Saves the "data" with the "title" and adds the .pickle
    """
    pikd = open(title, 'wb')
    pickle.dump(data, pikd)
    pikd.close()


def loosen_pickle(file):
    """loads and returns a pickled objects
    """
    pikd = open(file, 'rb')
    data = pickle.load(pikd)
    pikd.close()
    return data


def compressed_pickle(title, data):
    """Pickle a file and then compress it into a file with extension
    """
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        cPickle.dump(data, f)


def decompress_pickle(file):
    """Load any compressed pickle file
    """
    if not os.path.exists(file):
        file = file +'.pbz2'
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data


def somefunc(cls):
    instances = {}

    def _wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return _wrapper
