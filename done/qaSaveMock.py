from functools import lru_cache
import random
from QUANTAXIS.QAUtil import DATABASE, print_used_time
from QUANTAXIS.QASU.main import select_save_engine
from QUANTAXIS.QAUtil import QASetting

__updated__ = "2021-08-14"


@print_used_time
def QA_SU_save_stock_xdxr_mock(engine, client=DATABASE):
    """save stock_xdxr

    Arguments:
        engine {[type]} -- [description]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    engine = select_save_engine(engine, paralleled=True)
    print(f'paralleled engine:{engine}')
    engine.QA_SU_save_stock_xdxr(client=client)


# @print_used_time
def for_sh_mock(code):
    """更新etf代码范围
    """
    if str(code)[0] == '6':
        return 'stock_cn'
    elif str(code)[0:3] in ['000', '880']:
        return 'index_cn'
    elif str(code)[0:2] in ['50', '51', '58']:
        # 增加50 58开头的代码
        #  print(f"etf {code}")
        return 'etf_cn'
    # 110×××120×××企业债券；
    # 129×××100×××可转换债券；
    # 113A股对应可转债 132
    elif str(code)[0:3] in ['102', '110', '113', '120', '122', '124',
                            '130', '132', '133', '134', '135', '136',
                            '140', '141', '143', '144', '147', '148']:
        return 'bond_cn'
    else:
        return 'undefined'


@lru_cache
def get_stock_ips():
    from multiprocessing import cpu_count
    from QUANTAXIS.QAFetch.QATdx import get_ip_list_by_multi_process_ping
    stock_ip_list = QASetting.stock_ip_list
    ips = get_ip_list_by_multi_process_ping(stock_ip_list, _type='stock')[
        :cpu_count() * 2 + 1]
    return ips


def get_mainmarket_ip(ip, port):
    """随机返回速度靠前的行情地址
    Arguments:
        ip {[type]} -- [description]
        port {[type]} -- [description]
    Returns:
        [type] -- [description]
    """

    global best_ip
    if ip is None and port is None:
        ips = get_stock_ips()
        n = len(ips)
        if n > 0:
            item = ips[random.randint(0, n - 1)]
            ip = item['ip']
            port = item['port']
    else:
        pass
    return ip, port
