# -*- coding: utf-8 -*-

# from .fetcher import Fetcher
# from .query import QueryMongodb
from .queryStock import QueryStock as Stock
from .queryIndex import QueryIndex as Index
from .TDX import TDX as Tdx

class FecherFactory(object):
    def createFetcher(self, typ='stock'):
        """获取金融数据接口

        df = F().createFetcher('stock').get(code, start, end)

        Args:
            typ: 类型 str "stock" "index" "future"

        Returns: 对应的fetcher子类

        """
        targetclass = typ.capitalize()
        return globals()[targetclass]()