# -*- coding: utf-8 -*-
"""index etf

"""

import datetime

import numpy
import pandas as pd
from QUANTAXIS.QAUtil import (
    DATABASE)
from .queryStock import QueryStock


class QueryIndex(QueryStock):
    _collectionsDay = DATABASE.index_day
    _collectionsMin = DATABASE.index_min

    def __init__(self, collectionsDay=DATABASE.index_day, collectionsMin=DATABASE.index_min):
        self._collectionsDay = collectionsDay
        self._collectionsMin = collectionsMin

    @classmethod
    def _getStoring(cls, storing=None):
        return 'index'
