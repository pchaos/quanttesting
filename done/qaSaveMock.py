from QUANTAXIS.QAUtil import DATABASE, print_used_time
from QUANTAXIS.QASU.main import select_save_engine

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
