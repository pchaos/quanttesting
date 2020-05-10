# -*- coding: utf-8 -*-
"""

"""
import datetime
import pandas as pd
from retrying import retry
from pytdx.hq import TdxHq_API
from QUANTAXIS.QAFetch.QATdx import get_mainmarket_ip, select_best_ip
from QUANTAXIS.QAFetch.base import _select_market_code, _select_index_code, _select_type, _select_bond_market_code
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_date_stamp,
                              QA_util_date_str2int, QA_util_date_valid,
                              QA_util_get_real_date, QA_util_get_real_datelist,
                              QA_util_future_to_realdatetime, QA_util_tdxtimestamp,
                              QA_util_future_to_tradedatetime,
                              QA_util_get_trade_gap, QA_util_log_info,
                              QA_util_time_stamp, QA_util_web_ping,
                              exclude_from_stock_ip_list, future_ip_list,
                              stock_ip_list, trade_date_sse)
from .fetcher import Fetcher
from .classproperty import classproperty


class TDX(Fetcher):
    ip = ""
    port = 0
    _api = None

    def __init__(self, ip=None, port=None):
        # self.ip = ip
        # self.port = port
        self._getAPI(ip, port)

    # @classproperty
    @classmethod
    def _getAPI(cls, ip=None, port=None):
        # select_best_ip()
        cls.ip, cls.port = get_mainmarket_ip(ip, port)
        cls._api = TdxHq_API()
        return cls._api

    @classproperty
    def tdxapi(cls):
        if not cls._api:
            cls._api = cls._getAPI()
        return cls._api

    @classmethod
    @retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
    def getMin(cls, code, start, end, if_fq='00',
               frequence=9):
        # type_ = ''
        start = str(start)[0:10]
        today_ = datetime.date.today()
        lens = QA_util_get_trade_gap(start, today_)
        _, type_, multiplicator = cls.getReverseFrequence(frequence)
        lens = lens * multiplicator
        if lens > 20800:
            lens = 20800
        with cls.tdxapi.connect(cls.ip, cls.port) as api:
            data = pd.concat(
                [api.to_df(
                    api.get_security_bars(
                        frequence, _select_market_code(
                            str(code)),
                        str(code),
                        (int(lens / 800) - i) * 800, 800)) for i
                    in range(int(lens / 800) + 1)], axis=0, sort=False)
            data = data \
                       .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                             inplace=False) \
                       .assign(datetime=pd.to_datetime(data['datetime']),
                               code=str(code),
                               date=data['datetime'].apply(lambda x: str(x)[0:10]),
                               date_stamp=data['datetime'].apply(
                                   lambda x: QA_util_date_stamp(x)),
                               time_stamp=data['datetime'].apply(
                                   lambda x: QA_util_time_stamp(x)),
                               type=type_).set_index('datetime', drop=False,
                                                     inplace=False)[start:end]
            return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))

    @classmethod
    @retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
    def getDay(cls, code, start_date, end_date, if_fq='00',
               frequence=9):
        """获取日线及以上级别的数据

        Arguments:
            code {str:6} -- code 是一个单独的code 6位长度的str
            start_date {str:10} -- 10位长度的日期 比如'2017-01-01'
            end_date {str:10} -- 10位长度的日期 比如'2018-01-01'
        Keyword Arguments:
            if_fq {str} -- '00'/'bfq' -- 不复权 '01'/'qfq' -- 前复权 '02'/'hfq' -- 后复权 '03'/'ddqfq' -- 定点前复权 '04'/'ddhfq' --定点后复权
            frequency {int} -- K线周期
                0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
                5 周K线
                6 月K线
                7 1分钟
                8 1分钟K线
                9 日K线
                10 季K线
                11 年K线
            ip {str} -- [description] (default: None) ip可以通过select_best_ip()函数重新获取
            port {int} -- [description] (default: {None})
        Returns:
            pd.DataFrame/None -- 返回的是dataframe,如果出错比如只获
            取了一天,而当天停牌,返回None
        Exception:
            如果出现网络问题/服务器拒绝, 会出现socket:time out 尝试再次获取/更换ip即可, 本函数不做处理
        """
        try:
            with cls.tdxapi.connect(cls.ip, cls.port, time_out=0.7) as api:
                start_date = str(start_date)[0:10]
                today_ = datetime.date.today()
                lens = QA_util_get_trade_gap(start_date, today_)

                data = pd.concat([api.to_df(
                    api.get_security_bars(frequence, _select_market_code(
                        code), code, (int(lens / 800) - i) * 800, 800)) for i in
                    range(int(lens / 800) + 1)], axis=0, sort=False)

                # 这里的问题是: 如果只取了一天的股票,而当天停牌, 那么就直接返回None了
                if len(data) < 1:
                    return None
                data = data[data['open'] != 0]

                data = data.assign(
                    date=data['datetime'].apply(lambda x: str(x[0:10])),
                    code=str(code),
                    date_stamp=data['datetime'].apply(
                        lambda x: QA_util_date_stamp(str(x)[0:10]))) \
                    .set_index('date', drop=False, inplace=False)

                end_date = str(end_date)[0:10]
                data = data.drop(
                    ['year', 'month', 'day', 'hour', 'minute', 'datetime'],
                    axis=1)[
                       start_date:end_date]
                if if_fq in ['00', 'bfq']:
                    return data
                else:
                    print('CURRENTLY NOT SUPPORT REALTIME FUQUAN')
                    return None
                    # xdxr = QA_fetch_get_stock_xdxr(code)
                    # if if_fq in ['01','qfq']:
                    #     return QA_data_make_qfq(data,xdxr)
                    # elif if_fq in ['02','hfq']:
                    #     return QA_data_make_hfq(data,xdxr)
        except Exception as e:
            if isinstance(e, TypeError):
                print('1、Tushare内置的pytdx版本和QUANTAXIS使用的pytdx 版本不同, 请重新安装pytdx以解决此问题.{}:{}'.format(cls.ip, cls.port))
                print('pip uninstall pytdx\npip install pytdx')
                print('2、或者此时间段无数据。')
            else:
                print(e)

    @classmethod
    def get(cls, code, start, end, if_fq='00',
            frequence='day'):
        """通达信历史数据

        Args:
            code:
            start:
            end:
            if_fq:
            frequence: K线周期
                0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
                5 周K线
                6 月K线
                7 1分钟
                8 1分钟K线
                9 日K线
                10 季K线
                11 年K线

        Returns:

        """
        frequence = cls.getFrequence(frequence)
        if 5 <= frequence != 8:
            #日线以上周期
            return cls.getDay(code, start, end, if_fq, frequence)
        else:
            # 日线以下周期
            return cls.getMin(code, start, end, if_fq, frequence)
