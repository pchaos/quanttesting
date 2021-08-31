# -*- coding: utf-8 -*-
"""pytdx补丁
使用方法（import本文件）：
import pytdx_base_socket_client_mock
"""
import pandas as pd
from mock import Mock
from mock import patch
from pytdx.base_socket_client import BaseSocketClient as bsc

__updated__ = "2021-08-31"

def _to_df(v):
    if isinstance(v, list):
        return pd.DataFrame(data=v).dropna()
    elif isinstance(v, dict):
        return pd.DataFrame(data=[v, ]).dropna()
    else:
        return pd.DataFrame(data=[{'value': v}]).dropna()

#
#  print(f"mocking {bsc}")

bsc.to_df=Mock(side_effect=_to_df)
