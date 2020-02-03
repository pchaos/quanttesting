# -*- coding: utf-8 -*-
import bz2
import pickle
try:
    # 在python3.x上已从cPickle更改cPickle为_pickle
    import _pickle as cPickle
except ImportError:
    import cpickle as cPickle
import os
import QUANTAXIS as qa
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache


def getCodeList(isTesting=True, count=5000):
    """
    :param isTesting: 是否使用测试数据
    :param count: 返回最多结果集数量
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

def read_zxg(filename='zxg.txt', length=6):
    """从文件filename读取自选股列表
    返回每行前length(默认：6）个字符（自动去除行首、行尾空格）;

    :param filename: 自选股文件名（默认：zxg.txt)
    """
    try:
        # 当前目录
        dir_path = os.path.dirname(os.path.realpath(__file__))
    except:
        dir_path = os.path.dirname(os.path.realpath("./"))
    if not filename.find(os.sep) > -1:
        if os.path.exists(filename):
            # 当前目录优先
            pass
        else:
            # 如果文件名（fname）没有目录，则加上当前目录
            filename = os.path.join(dir_path, filename)
    resultList= alist = []
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='UTF-8') as zxg:
            alist = zxg.readlines()
    for a in alist:
        resultList.append(a.strip()[0:length])
    return resultList

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

    :param file: 文件名
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
