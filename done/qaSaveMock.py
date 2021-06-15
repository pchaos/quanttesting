from QUANTAXIS.QAUtil import DATABASE, print_used_time
from QUANTAXIS.QASU.main import select_save_engine

__updated__ = "2021-06-15"


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
    if str(code)[0] == '6':
        return 'stock_cn'
    elif str(code)[0:3] in ['000', '880']:
        return 'index_cn'
    elif str(code)[0:2] in ['50', '51', '58']:
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
