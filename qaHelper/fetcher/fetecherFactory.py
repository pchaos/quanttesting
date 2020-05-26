# -*- coding: utf-8 -*-

# from .fetcher import Fetcher
# from .query import QueryMongodb
from .queryStock import QueryStock as Stock
from .queryIndex import QueryIndex as Index

class FecherFactory(object):
    def createFetcher(self, typ='stock'):
        """

        Args:
            typ: str "stock" "index" "future"

        Returns:

        """
        targetclass = typ.capitalize()
        return globals()[targetclass]()