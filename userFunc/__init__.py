# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     talibfunctions.py
   Description :
   Author :       pchaos
   date：          2019/6/21
-------------------------------------------------
   Change Activity:
                   2019/6/21:
-------------------------------------------------
"""
__author__ = 'pchaos'

from .myFunction import getCodeList
from .myFunction import full_pickle, loosen_pickle
from .myFunction import compressed_pickle, decompress_pickle
from .myFunction import read_zxg
from .myFunction import xls2zxg
from .myFunction import xls2Code
from .myFunction import code2ETF
from .myFunction import etfAmountGreater
from .myFunction import getRealFilename
from .myFunction import setdiff_sorted
from .chCounts import CHCOUNTS, CHCOUNTS2
from .chCounts import CHCOUNTS3
from .chCounts import FOURWEEK, pltFourWeek
from .shouban import shouban
from .shouban import shoubanData
from .shouban import shoubanType
from .shouban import shoubanZDZG
from .rps import cal_ret
from .rps import get_RPS

from .comm import ifupMA
from .comm import str2date
from .comm import is_all_chinese, is_contains_chinese