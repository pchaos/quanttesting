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

from .myFunction import getCodeList, ifupMA
from .myFunction import full_pickle, loosen_pickle
from .myFunction import compressed_pickle, decompress_pickle
from .myFunction import read_zxg
from .myFunction import xls2zxg
from .myFunction import xls2Code
from .myFunction import codeInETF
from .myFunction import etfAmountGreater
from .myFunction import codeInfo
from .myFunction import getRealFilename
from .myFunction import setdiff_sorted
from .myFunction import CMI
from .myFunction import RSV
from .myFunction import fourWeek, taoboshiIndicator
from .chCounts import CHCOUNTS, CHCOUNTS2
from .chCounts import CHCOUNTS3
from .chCounts import FOURWEEK, pltFourWeek
from .shouban import shouban
from .shouban import shoubanData
from .shouban import shoubanType
from .shouban import shoubanZDZG
from .rps import cal_ret
from .rps import get_RPS
from .rps import RPSIndex
from .qaETFstrategy import QAStrategyETFBase
from .qaETFQARisk import QAETF_Risk
from .qaIndexDatastruct import QAIndex_DataStruct_Day
from .comm import str2date, date2str
from .comm import is_all_chinese, is_contains_chinese
from .RSRS import getdata
from .RSRS import RSRS1, RSRS2, RSRS3, RSRS4
from .qatestbase import qaTestingBase
from .jqtestbase import jqTestingbase