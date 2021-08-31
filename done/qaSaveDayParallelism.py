# -*- coding: utf-8 -*-
"""多进程保存日线数据
使用mock替换原function为新的函数

@Time    : 2020/2/5 上午12:12

@File    : qaSaveDayParallelism.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

import time
from QUANTAXIS.QACmd import QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_etf_day, \
    QA_SU_save_stock_xdxr, QA_SU_save_etf_list, QA_SU_save_index_list, QA_SU_save_stock_list, \
    QA_SU_save_stock_block, \
    QA_SU_save_etf_min, QA_SU_save_index_min
from QUANTAXIS.QAFetch.QATdx import for_sh
from QUANTAXIS.QAFetch import QATdx
from mock import Mock
from qaSaveMock import QA_SU_save_stock_xdxr_mock, for_sh_mock, get_mainmarket_ip
import pytdx_base_socket_client_mock

__updated__ = "2021-06-16"


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


def save_xdxr(parallele=True):
    # 使用mock多进程下载xdxr数据
    QA_SU_save_stock_xdxr('tdx')


def save_etf_min(paralleled=True):
    QA_SU_save_etf_min('tdx')


def save_index_min():
    """保存指数分钟数据
    """
    QA_SU_save_index_min('tdx')


def weekday():
    from datetime import datetime, date
    dayOfWeek = datetime.today().weekday()
    return dayOfWeek


if __name__ == '__main__':
    # starting time
    start = time.time()

    old_QA_SU_save_stock_xdxr = QA_SU_save_stock_xdxr
    QA_SU_save_stock_xdxr = Mock(side_effect=QA_SU_save_stock_xdxr_mock)
    old_for_sh = QATdx.for_sh
    QATdx.for_sh = Mock(side_effect=for_sh_mock)
    old_get_mainmarket_ip = QATdx.get_mainmarket_ip
    QATdx.get_mainmarket_ip = Mock(side_effect=get_mainmarket_ip)
    #  bsc.to_df = Mock(side_effect=pytdx_base_socket_client_mock._to_df)
    # save_day(False)
    save_day(True)
    if weekday() % 6 == 1:
        #  if weekday() % 2 == 1:
        # 周2、4、6保存分钟数据
        save_etf_min()
    if weekday() % 4 == 0:
        #  if weekday() % 4 == 0:
        # 周1、5保存分钟数据
        #  QA_SU_save_index_min('tdx')
        save_index_min()
        print(f"save index min done")
    elif weekday() % 7 == 2:
        # 周三下载xdxr
        save_xdxr()
    # 还原版本
    QA_SU_save_stock_xdxr = old_QA_SU_save_stock_xdxr
    QATdx.for_sh = old_for_sh
    QATdx.get_mainmarket_ip = old_get_mainmarket_ip

    # end time
    end = time.time()
    # total time taken
    print(f"Runtime of the program is {end - start}")
