# -*- coding: utf-8 -*-
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
