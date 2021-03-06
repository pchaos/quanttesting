# -*- coding: utf-8 -*-
"""多进程保存日线数据
使用mock替换原function为新的函数

@Time    : 2020/2/5 上午12:12

@File    : qasaveDay.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

from QUANTAXIS.QACmd import QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_etf_day, \
    QA_SU_save_stock_xdxr, QA_SU_save_etf_list, QA_SU_save_index_list, QA_SU_save_stock_list, \
    QA_SU_save_stock_block
from QUANTAXIS.QAFetch.QATdx import for_sh
from QUANTAXIS.QAFetch import QATdx
from qaSaveMock import QA_SU_save_stock_xdxr_mock, for_sh_mock

from mock import Mock

__updated__ = "2021-06-15"


def save_day(paralleled=True):
    """多进程保存日线数据
    """
    QA_SU_save_index_list('tdx')
    QA_SU_save_index_day('tdx', paralleled=paralleled)
    QA_SU_save_etf_list('tdx')
    QA_SU_save_etf_day('tdx', paralleled=paralleled)
    QA_SU_save_stock_list('tdx')
    QA_SU_save_stock_block('tdx')
    QA_SU_save_stock_day('tdx', paralleled=paralleled)
    # 使用mock多进程下载xdxr数据
    QA_SU_save_stock_xdxr('tdx')


if __name__ == '__main__':
    old_QA_SU_save_stock_xdxr = QA_SU_save_stock_xdxr
    QA_SU_save_stock_xdxr = Mock(side_effect=QA_SU_save_stock_xdxr_mock)
    old_for_sh = QATdx.for_sh
    QATdx.for_sh = Mock(side_effect=for_sh_mock)
    # save_day(False)
    save_day(True)
    # QA_SU_save_etf_list('tdx')
    # QA_SU_save_etf_day('tdx', paralleled=True)
    # 还原版本
    QA_SU_save_stock_xdxr = old_QA_SU_save_stock_xdxr
    QATdx.for_sh = old_for_sh
