# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/1 下午9:05

@File    : qaETFQARisk.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
from QUANTAXIS.QAARP import QA_Risk


class QAETF_Risk(QA_Risk):
    @property
    def market_value(self):
        """每日每个股票持仓市值表

        Returns:
            pd.DataFrame -- 市值表
        """
        if self.account.daily_hold is not None:
            if self.market_data.index.names[0] == None:
                self.market_data.index.names = ['date', 'code']
            if self.if_fq:

                return (
                        self.market_data.to_qfq().pivot('close').fillna(
                            method='ffill'
                        ) * self.account.daily_hold.apply(abs)
                ).fillna(method='ffill')
            else:
                return (
                        self.market_data.pivot('close').fillna(method='ffill') *
                        self.account.daily_hold.apply(abs)
                ).fillna(method='ffill')
        else:
            return None
    # pass
