# -*- coding: utf-8 -*-
"""多进程保存日线数据

@Time    : 2020/2/5 上午12:12

@File    : qasaveDay.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

from QUANTAXIS.QACmd import QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_etf_day, \
    QA_SU_save_stock_xdxr, QA_SU_save_etf_list, QA_SU_save_index_list, QA_SU_save_stock_list, \
    QA_SU_save_stock_block


def save_day(paralleled=True):
    """多进程保存日线数据
    """
    QA_SU_save_index_day('tdx', paralleled=paralleled)
    QA_SU_save_etf_list('tdx')
    QA_SU_save_etf_day('tdx', paralleled=paralleled)
    QA_SU_save_index_list('tdx')
    QA_SU_save_stock_list('tdx')
    QA_SU_save_stock_block('tdx')
    QA_SU_save_stock_day('tdx', paralleled=paralleled)
    QA_SU_save_stock_xdxr('tdx')


if __name__ == '__main__':
    # save_day(False)
    save_day(True)
