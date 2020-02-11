# -*- coding: utf-8 -*-
"""抽取集思录中可转债、指数ETF数据
https://www.lizenghai.com/archives/24933.html

@Time    : 2020/2/9 下午11:52

@File    : jisilucbnew.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""

import pandas as pd
from selenium import webdriver


def jisilu(*args, **kwargs):
    for key, value in kwargs.items():
        pass
    url = kwargs['url']
    cssSelector = kwargs['cssSelector']
    cols = kwargs['cols']
    dropcols = kwargs['dropcols']
    sortedby = kwargs['sortedby']
    # 列名以结束
    colEnd = kwargs['colEnd']
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("–no-sandbox")
    options.add_argument("–disable-dev-shm-usage")
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.get(url)
    x = driver.find_element_by_css_selector(cssSelector).text
    y = x.find(colEnd)
    z = x[y + len(colEnd) + 1:].strip().split("\n")
    df1 = pd.DataFrame(columns=cols)
    for i in z:
        data = i.strip().split()
        if data[2].strip() == "!":
            data.pop(2)
        dic = dict()
        for j in range(len(cols)):
            dic.update({cols[j]: [data[j]]})
        df2 = pd.DataFrame(dic)
        df1 = df1.append(df2)
        df1 = df1.reset_index(drop=True)
        df1.sort_values(by=sortedby, ascending=True, axis=0, inplace=True)
        df1.drop(dropcols, axis=1, inplace=True)
    return df1


def jslcb():
    # 可转债
    jsl = {"url": "https://www.jisilu.cn/data/cbnew/#cb",
           "cols": ["代码", "转债名称", "现价", "涨跌幅", "正股名称", "正股价", "正股涨跌", "PB", "转股价", "转股价值", "溢价率", "纯债价值", "评级", "期权价值",
                    "回售触发价",
                    "强赎触发价", "转债占比", "机构持仓", "到期时间", "剩余年限", "到期税前收益", "到期税后收益", "回售收益", "成交额"],
           "dropcols": ["纯债价值", "期权价值", "机构持仓", "回售收益"],
           "cssSelector": "#flex_cb",
           "sortedby": "溢价率",
           "colEnd": "双低 操作"
           }
    return jisilu(**jsl)


def jslindex():
    # 指数ETF
    jsl = {"url": "https://www.jisilu.cn/data/etf/#index",
           "cols": ["代码", "名称", "现价", "涨跌幅", "成交额（万元）", "指数", "指数PE", "指数PB", "指数涨幅", "估值", "净值", "净值日期", "溢价率",
                    "最小申赎单位", "管托费",
                    "份额（万份）", "规模变化", "规模（亿元）", "操作"],
           "dropcols": ["管托费", "溢价率", "操作"],
           "cssSelector": "#flex_index",
           "sortedby": "成交额（万元）",
           "colEnd": "元) 操作"
           }
    return jisilu(**jsl)


if __name__ == "__main__":
    # 可转债
    # df = jslcb()
    # # df.to_excel("/tmp/jisilu.xls")
    # print(df)

    # 指数ETF
    df = jslindex()
    print(df)
